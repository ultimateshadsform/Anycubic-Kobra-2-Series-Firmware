package main

import (
	"fmt"
	"net/http"
	"os"
	"sync"
)

var (
	machine      = "K2Max"
	extensions   = []string{"bin", "zip", "swu"}
	baseURL      = "https://cdn.cloud-universe.anycubic.com/ota/%s/AC104_%s_1.1.0_%d.%d.%d_update.%s"
	maxThreads   = 1000
	successFile  = fmt.Sprintf("%s_success.txt", machine)
	waitGroup    sync.WaitGroup
	threadSem    = make(chan struct{}, maxThreads)
	successMutex sync.Mutex
)

func checkVersion(major, minor, patch int, ext string) {
	defer waitGroup.Done()
	url := fmt.Sprintf(baseURL, machine, machine, major, minor, patch, ext)

	threadSem <- struct{}{}        // acquire semaphore
	defer func() { <-threadSem }() // release semaphore

	resp, err := http.Head(url)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}

	if resp.StatusCode == http.StatusOK {
		successMessage := fmt.Sprintf("Success: %s\n", url)
		fmt.Print(successMessage)

		successMutex.Lock()
		defer successMutex.Unlock()

		// Write successful URLs to the file
		file, err := os.OpenFile(successFile, os.O_APPEND|os.O_WRONLY|os.O_CREATE, 0644)
		if err != nil {
			fmt.Printf("Error opening file: %v\n", err)
			return
		}
		defer file.Close()

		if _, err := file.WriteString(successMessage); err != nil {
			fmt.Printf("Error writing to file: %v\n", err)
		}
	} else {
		fmt.Printf("Failed: %s\n", url)
	}
}

func main() {
	// Create threads
	for major := 0; major <= 9; major++ {
		for minor := 0; minor <= 9; minor++ {
			for patch := 0; patch <= 9; patch++ {
				for _, ext := range extensions {
					waitGroup.Add(1)
					go checkVersion(major, minor, patch, ext)
				}
			}
		}
	}

	// Wait for all threads to finish
	waitGroup.Wait()

	fmt.Printf("Successful URLs written to %s\n", successFile)
	fmt.Println("Done! RIP their servers.")
}
