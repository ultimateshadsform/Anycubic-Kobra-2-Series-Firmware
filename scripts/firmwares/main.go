package main

import (
	"fmt"
	"net/http"
	"os"
	"sync"
)

var (
	machine      = "K2Max"
	baseURL      = "https://cdn.cloud-universe.anycubic.com/ota/%s/AC104_%s_%d.%d.%d_%d.%d.%d_update.zip"
	maxThreads   = 1000
	successFile  = fmt.Sprintf("%s_success.txt", machine)
	waitGroup    sync.WaitGroup
	threadSem    = make(chan struct{}, maxThreads)
	successMutex sync.Mutex
)

func checkVersion(major1, minor1, patch1, major2, minor2, patch2 int) {
	defer waitGroup.Done()
	url := fmt.Sprintf(baseURL, machine, machine, major1, minor1, patch1, major2, minor2, patch2)

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
	for major1 := 0; major1 < 10; major1++ {
		for minor1 := 0; minor1 < 10; minor1++ {
			for patch1 := 0; patch1 < 10; patch1++ {
				for major2 := 0; major2 < 10; major2++ {
					for minor2 := 0; minor2 < 10; minor2++ {
						for patch2 := 0; patch2 < 10; patch2++ {
							waitGroup.Add(1)
							go checkVersion(major1, minor1, patch1, major2, minor2, patch2)
						}
					}
				}
			}
		}
	}

	// Wait for all threads to finish
	waitGroup.Wait()

	fmt.Printf("Successful URLs written to %s\n", successFile)
	fmt.Println("Done! RIP their servers.")
}
