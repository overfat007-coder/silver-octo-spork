package main

import (
	"fmt"
	"os"
)

func main() {
	cwd, err := os.Getwd()
	if err != nil {
		fmt.Fprintf(os.Stderr, "failed to get cwd: %v\n", err)
		os.Exit(1)
	}

	app, err := NewApp(cwd)
	if err != nil {
		fmt.Fprintf(os.Stderr, "failed to initialize vimfm: %v\n", err)
		os.Exit(1)
	}

	if err := app.Run(); err != nil {
		fmt.Fprintf(os.Stderr, "vimfm error: %v\n", err)
		os.Exit(1)
	}
}
