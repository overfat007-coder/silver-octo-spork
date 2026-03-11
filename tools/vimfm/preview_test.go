package main

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestBuildPreviewTextAndBinary(t *testing.T) {
	tmp := t.TempDir()
	textPath := filepath.Join(tmp, "note.txt")
	text := strings.Repeat("line\n", 20)
	if err := os.WriteFile(textPath, []byte(text), 0o644); err != nil {
		t.Fatal(err)
	}
	pv := BuildPreview(textPath)
	if strings.Count(pv, "\n") > 9 {
		t.Fatalf("text preview should contain first 10 lines, got %d newlines", strings.Count(pv, "\n"))
	}

	binPath := filepath.Join(tmp, "blob.bin")
	if err := os.WriteFile(binPath, []byte{0, 1, 2, 3, 4, 5}, 0o644); err != nil {
		t.Fatal(err)
	}
	pv = BuildPreview(binPath)
	if !strings.Contains(pv, "Binary header") {
		t.Fatalf("expected binary header preview, got %q", pv)
	}
}

func TestMakeUniquePath(t *testing.T) {
	tmp := t.TempDir()
	base := filepath.Join(tmp, "file.txt")
	if err := os.WriteFile(base, []byte("x"), 0o644); err != nil {
		t.Fatal(err)
	}
	uniq := makeUniquePath(base)
	if uniq == base {
		t.Fatalf("expected unique path, got same")
	}
}
