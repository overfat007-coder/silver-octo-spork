package main

import (
	"bufio"
	"bytes"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"sort"
	"strings"
	"syscall"
	"unsafe"
)

type Panel struct {
	path    string
	entries []os.DirEntry
	cursor  int
	search  string
}

type App struct {
	panels      [2]*Panel
	active      int
	clipboard   string
	pendingOp   string
	message     string
	stdinReader *bufio.Reader
	origTerm    *syscall.Termios
}

func NewApp(cwd string) (*App, error) {
	left := &Panel{path: cwd}
	right := &Panel{path: cwd}
	app := &App{panels: [2]*Panel{left, right}, stdinReader: bufio.NewReader(os.Stdin)}
	if err := left.LoadEntries(); err != nil {
		return nil, err
	}
	if err := right.LoadEntries(); err != nil {
		return nil, err
	}
	return app, nil
}

func (p *Panel) LoadEntries() error {
	items, err := os.ReadDir(p.path)
	if err != nil {
		return err
	}
	sort.Slice(items, func(i, j int) bool {
		iInfo, iErr := items[i].Info()
		jInfo, jErr := items[j].Info()
		iDir := iErr == nil && iInfo.IsDir()
		jDir := jErr == nil && jInfo.IsDir()
		if iDir != jDir {
			return iDir
		}
		return strings.ToLower(items[i].Name()) < strings.ToLower(items[j].Name())
	})
	if p.search != "" {
		filtered := make([]os.DirEntry, 0, len(items))
		q := strings.ToLower(p.search)
		for _, e := range items {
			if strings.Contains(strings.ToLower(e.Name()), q) {
				filtered = append(filtered, e)
			}
		}
		items = filtered
	}
	p.entries = items
	if len(p.entries) == 0 {
		p.cursor = 0
		return nil
	}
	if p.cursor >= len(p.entries) {
		p.cursor = len(p.entries) - 1
	}
	if p.cursor < 0 {
		p.cursor = 0
	}
	return nil
}

func (a *App) Run() error {
	if err := a.captureOriginalTerm(); err != nil {
		return err
	}

	if err := enableRawMode(); err != nil {
		return err
	}
	defer disableRawMode(a.origTerm)

	for {
		a.render()
		key, err := a.readKey()
		if err != nil {
			if err == io.EOF {
				return nil
			}
			return err
		}
		if shouldQuit := a.handleKey(key); shouldQuit {
			fmt.Print("\033[2J\033[H")
			return nil
		}
	}
}

func (a *App) captureOriginalTerm() error {
	fd := int(os.Stdin.Fd())
	termios, err := getTermios(fd)
	if err != nil {
		return err
	}
	a.origTerm = termios
	return nil
}

func enableRawMode() error {
	fd := int(os.Stdin.Fd())
	termios, err := getTermios(fd)
	if err != nil {
		return err
	}
	newState := *termios
	newState.Iflag &^= syscall.IGNBRK | syscall.BRKINT | syscall.PARMRK | syscall.ISTRIP | syscall.INLCR | syscall.IGNCR | syscall.ICRNL | syscall.IXON
	newState.Lflag &^= syscall.ECHO | syscall.ECHONL | syscall.ICANON | syscall.ISIG | syscall.IEXTEN
	newState.Cflag &^= syscall.CSIZE | syscall.PARENB
	newState.Cflag |= syscall.CS8
	newState.Cc[syscall.VMIN] = 1
	newState.Cc[syscall.VTIME] = 0
	return setTermios(fd, &newState)
}

func disableRawMode(term *syscall.Termios) {
	if term == nil {
		return
	}
	_ = setTermios(int(os.Stdin.Fd()), term)
}

func getTermios(fd int) (*syscall.Termios, error) {
	term := &syscall.Termios{}
	_, _, errno := syscall.Syscall6(syscall.SYS_IOCTL, uintptr(fd), uintptr(syscall.TCGETS), uintptr(unsafe.Pointer(term)), 0, 0, 0)
	if errno != 0 {
		return nil, errno
	}
	return term, nil
}

func setTermios(fd int, state *syscall.Termios) error {
	_, _, errno := syscall.Syscall6(syscall.SYS_IOCTL, uintptr(fd), uintptr(syscall.TCSETS), uintptr(unsafe.Pointer(state)), 0, 0, 0)
	if errno != 0 {
		return errno
	}
	return nil
}

func (a *App) readKey() (string, error) {
	b, err := a.stdinReader.ReadByte()
	if err != nil {
		return "", err
	}
	if b == 27 {
		next, err := a.stdinReader.Peek(2)
		if err == nil && len(next) == 2 && next[0] == '[' {
			_, _ = a.stdinReader.ReadByte()
			arrow, _ := a.stdinReader.ReadByte()
			switch arrow {
			case 'A':
				return "up", nil
			case 'B':
				return "down", nil
			case 'C':
				return "right", nil
			case 'D':
				return "left", nil
			}
		}
		return "esc", nil
	}
	return string(b), nil
}

func (a *App) handleKey(key string) bool {
	panel := a.panels[a.active]
	a.message = ""

	switch {
	case key == "q":
		return true
	case key == "\t":
		a.active = 1 - a.active
	case key == "j" || key == "down":
		if panel.cursor < len(panel.entries)-1 {
			panel.cursor++
		}
		a.pendingOp = ""
	case key == "k" || key == "up":
		if panel.cursor > 0 {
			panel.cursor--
		}
		a.pendingOp = ""
	case key == "h" || key == "left":
		a.pendingOp = ""
		parent := filepath.Dir(panel.path)
		if parent != panel.path {
			panel.path = parent
			panel.cursor = 0
			_ = panel.LoadEntries()
		}
	case key == "l" || key == "right":
		a.pendingOp = ""
		a.enterSelected(panel)
	case key == "y":
		if a.pendingOp == "y" {
			a.copySelected(panel)
			a.pendingOp = ""
		} else {
			a.pendingOp = "y"
			a.message = "y pressed: complete with yy"
		}
	case key == "d":
		if a.pendingOp == "d" {
			a.deleteSelected(panel)
			a.pendingOp = ""
		} else {
			a.pendingOp = "d"
			a.message = "d pressed: complete with dd"
		}
	case key == "p":
		a.pendingOp = ""
		a.pasteClipboard(panel)
	case key == "/":
		a.pendingOp = ""
		a.search(panel)
	case key == "esc":
		a.pendingOp = ""
		panel.search = ""
		_ = panel.LoadEntries()
	default:
		a.pendingOp = ""
	}

	return false
}

func (a *App) selectedPath(panel *Panel) string {
	if len(panel.entries) == 0 {
		return ""
	}
	return filepath.Join(panel.path, panel.entries[panel.cursor].Name())
}

func (a *App) enterSelected(panel *Panel) {
	path := a.selectedPath(panel)
	if path == "" {
		return
	}
	info, err := os.Stat(path)
	if err != nil {
		a.message = err.Error()
		return
	}
	if info.IsDir() {
		panel.path = path
		panel.cursor = 0
		_ = panel.LoadEntries()
	}
}

func (a *App) copySelected(panel *Panel) {
	path := a.selectedPath(panel)
	if path == "" {
		a.message = "nothing to copy"
		return
	}
	a.clipboard = path
	a.message = fmt.Sprintf("copied: %s", filepath.Base(path))
}

func (a *App) deleteSelected(panel *Panel) {
	path := a.selectedPath(panel)
	if path == "" {
		a.message = "nothing to delete"
		return
	}
	if err := os.RemoveAll(path); err != nil {
		a.message = fmt.Sprintf("delete failed: %v", err)
		return
	}
	a.message = fmt.Sprintf("deleted: %s", filepath.Base(path))
	_ = panel.LoadEntries()
}

func (a *App) pasteClipboard(panel *Panel) {
	if a.clipboard == "" {
		a.message = "clipboard empty"
		return
	}
	base := filepath.Base(a.clipboard)
	dst := filepath.Join(panel.path, base)
	dst = makeUniquePath(dst)
	if err := copyPath(a.clipboard, dst); err != nil {
		a.message = fmt.Sprintf("paste failed: %v", err)
		return
	}
	a.message = fmt.Sprintf("pasted: %s", filepath.Base(dst))
	_ = panel.LoadEntries()
}

func (a *App) search(panel *Panel) {
	disableRawMode(a.origTerm)
	fmt.Printf("\n/search: ")
	query, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	query = strings.TrimSpace(query)
	_ = enableRawMode()
	panel.search = query
	panel.cursor = 0
	if err := panel.LoadEntries(); err != nil {
		a.message = err.Error()
		return
	}
	a.message = fmt.Sprintf("search filter: %q", query)
}

func (a *App) render() {
	fmt.Print("\033[2J\033[H")
	fmt.Println("vimfm (q quit, tab switch panel, hjkl/arrows move, yy copy, p paste, dd delete, / search)")

	left := a.renderPanel(a.panels[0], a.active == 0, "LEFT")
	right := a.renderPanel(a.panels[1], a.active == 1, "RIGHT")

	max := len(left)
	if len(right) > max {
		max = len(right)
	}
	for i := 0; i < max; i++ {
		l := ""
		r := ""
		if i < len(left) {
			l = left[i]
		}
		if i < len(right) {
			r = right[i]
		}
		fmt.Printf("%-70s %s\n", l, r)
	}

	fmt.Println(strings.Repeat("-", 120))
	preview := BuildPreview(a.selectedPath(a.panels[a.active]))
	fmt.Println("Preview:")
	fmt.Println(preview)
	fmt.Println(strings.Repeat("-", 120))
	fmt.Println("Status:", a.message)
}

func (a *App) renderPanel(panel *Panel, active bool, label string) []string {
	header := fmt.Sprintf("[%s] %s", label, panel.path)
	if panel.search != "" {
		header += "  (filter: " + panel.search + ")"
	}
	if active {
		header = "\033[1;37;44m" + header + "\033[0m"
	}
	lines := []string{header}
	limit := 18
	start := 0
	if panel.cursor >= limit {
		start = panel.cursor - limit + 1
	}
	end := start + limit
	if end > len(panel.entries) {
		end = len(panel.entries)
	}
	for idx := start; idx < end; idx++ {
		e := panel.entries[idx]
		full := filepath.Join(panel.path, e.Name())
		info, err := e.Info()
		if err != nil {
			continue
		}
		name := colorizeName(full, info)
		size := HumanSize(info.Size())
		marker := "  "
		if idx == panel.cursor {
			marker = "> "
		}
		lines = append(lines, fmt.Sprintf("%s%-42s %8s", marker, name, size))
	}
	if len(panel.entries) == 0 {
		lines = append(lines, "  <empty>")
	}
	return lines
}

func copyPath(src, dst string) error {
	info, err := os.Stat(src)
	if err != nil {
		return err
	}
	if info.IsDir() {
		if err := os.MkdirAll(dst, info.Mode().Perm()); err != nil {
			return err
		}
		entries, err := os.ReadDir(src)
		if err != nil {
			return err
		}
		for _, e := range entries {
			if err := copyPath(filepath.Join(src, e.Name()), filepath.Join(dst, e.Name())); err != nil {
				return err
			}
		}
		return nil
	}
	return copyFile(src, dst, info.Mode())
}

func copyFile(src, dst string, mode os.FileMode) error {
	in, err := os.Open(src)
	if err != nil {
		return err
	}
	defer in.Close()
	out, err := os.OpenFile(dst, os.O_CREATE|os.O_WRONLY|os.O_TRUNC, mode.Perm())
	if err != nil {
		return err
	}
	defer out.Close()
	if _, err := io.Copy(out, in); err != nil {
		return err
	}
	return nil
}

func makeUniquePath(path string) string {
	if _, err := os.Stat(path); os.IsNotExist(err) {
		return path
	}
	ext := filepath.Ext(path)
	base := strings.TrimSuffix(path, ext)
	for i := 1; i < 1000; i++ {
		candidate := fmt.Sprintf("%s_copy%d%s", base, i, ext)
		if _, err := os.Stat(candidate); os.IsNotExist(err) {
			return candidate
		}
	}
	return path + "_copy"
}

func BuildPreview(path string) string {
	if path == "" {
		return "No selection"
	}
	info, err := os.Stat(path)
	if err != nil {
		return fmt.Sprintf("preview error: %v", err)
	}
	if info.IsDir() {
		return "Directory selected"
	}
	data, err := os.ReadFile(path)
	if err != nil {
		return fmt.Sprintf("preview error: %v", err)
	}
	if isBinary(data) {
		head := data
		if len(head) > 16 {
			head = head[:16]
		}
		return fmt.Sprintf("Binary header (%d bytes): % X", len(head), head)
	}
	return firstLines(string(data), 10)
}

func isBinary(data []byte) bool {
	if len(data) == 0 {
		return false
	}
	if bytes.IndexByte(data, 0) != -1 {
		return true
	}
	nonPrintable := 0
	limit := len(data)
	if limit > 256 {
		limit = 256
	}
	for i := 0; i < limit; i++ {
		b := data[i]
		if b < 9 || (b > 13 && b < 32) {
			nonPrintable++
		}
	}
	return float64(nonPrintable)/float64(limit) > 0.2
}

func firstLines(s string, n int) string {
	lines := strings.Split(s, "\n")
	if len(lines) > n {
		lines = lines[:n]
	}
	return strings.Join(lines, "\n")
}
