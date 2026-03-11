package main

import (
	"os"
	"path/filepath"
	"testing"
)

func TestHumanSize(t *testing.T) {
	cases := []struct {
		size int64
		want string
	}{
		{999, "999B"},
		{1024, "1.0KB"},
		{5 * 1024 * 1024, "5.0MB"},
	}
	for _, tc := range cases {
		if got := HumanSize(tc.size); got != tc.want {
			t.Fatalf("HumanSize(%d) = %s, want %s", tc.size, got, tc.want)
		}
	}
}

func TestFileKind(t *testing.T) {
	tmp := t.TempDir()
	dirInfo, _ := os.Stat(tmp)
	if got := fileKind(tmp, dirInfo); got != "dir" {
		t.Fatalf("got %s", got)
	}

	execPath := filepath.Join(tmp, "run.sh")
	if err := os.WriteFile(execPath, []byte("#!/bin/sh\n"), 0o755); err != nil {
		t.Fatal(err)
	}
	execInfo, _ := os.Stat(execPath)
	if got := fileKind(execPath, execInfo); got != "exec" {
		t.Fatalf("got %s", got)
	}

	imgPath := filepath.Join(tmp, "a.png")
	if err := os.WriteFile(imgPath, []byte("x"), 0o644); err != nil {
		t.Fatal(err)
	}
	imgInfo, _ := os.Stat(imgPath)
	if got := fileKind(imgPath, imgInfo); got != "image" {
		t.Fatalf("got %s", got)
	}
}
