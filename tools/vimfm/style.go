package main

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"
)

func HumanSize(size int64) string {
	units := []string{"B", "KB", "MB", "GB", "TB"}
	val := float64(size)
	u := 0
	for val >= 1024 && u < len(units)-1 {
		val /= 1024
		u++
	}
	if u == 0 {
		return fmt.Sprintf("%d%s", size, units[u])
	}
	return fmt.Sprintf("%.1f%s", val, units[u])
}

func fileKind(path string, info os.FileInfo) string {
	if info.IsDir() {
		return "dir"
	}
	if info.Mode()&0111 != 0 {
		return "exec"
	}
	ext := strings.ToLower(filepath.Ext(path))
	if isImageExtension(ext) {
		return "image"
	}
	return "file"
}

func isImageExtension(ext string) bool {
	switch ext {
	case ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".svg":
		return true
	default:
		return false
	}
}

func colorizeName(path string, info os.FileInfo) string {
	name := filepath.Base(path)
	switch fileKind(path, info) {
	case "dir":
		return "\033[34m" + name + "\033[0m"
	case "exec":
		return "\033[32m" + name + "\033[0m"
	case "image":
		return "\033[35m" + name + "\033[0m"
	default:
		return name
	}
}
