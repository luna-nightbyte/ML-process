package main

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"
)

const helpText = `
Usage: go run main.go [INPUT_DIR] [OLD_LABEL] [NEW_LABEL]

This script replaces specified labels in XML annotation files within a directory.

Arguments:
  INPUT_DIR   The directory containing the XML files to process.
  OLD_LABEL   The label to be replaced in the XML files.
  NEW_LABEL   The new label to replace the old label.

Example:
  go run main.go ./annotations cat dog

This will replace all occurrences of the label "cat" with "dog" in the XML files within the ./annotations directory.
`

func main() {
	args := os.Args

	// Display help text if required
	if len(args) < 2 || args[1] == "-h" || args[1] == "--help" {
		fmt.Println(helpText)
		return
	}

	// Argument validation
	if len(args) != 4 {
		fmt.Println("Error: Incorrect number of arguments.")
		fmt.Println(helpText)
		return
	}

	// Set input variables based on arguments
	inputDir := args[1]
	labelsToReplace := []string{args[2]}
	newLabel := args[3]

	// Read the directory
	files, err := os.ReadDir(inputDir)
	if err != nil {
		panic(err)
	}

	// Process each file in the directory
	for _, file := range files {
		if !file.IsDir() && strings.HasSuffix(file.Name(), ".xml") {
			labelFilePath := filepath.Join(inputDir, file.Name())
			fileContent, err := os.ReadFile(labelFilePath)
			if err != nil {
				fmt.Printf("Error reading file %s: %v\n", file.Name(), err)
				continue
			}

			// Replace labels in the file content
			newContent := string(fileContent)
			for _, replaceLabel := range labelsToReplace {
				if strings.Contains(newContent, replaceLabel) {
					newContent = strings.ReplaceAll(newContent, replaceLabel, newLabel)
				}
			}

			// Write the modified content back to the file
			if newContent != string(fileContent) {
				err = os.WriteFile(labelFilePath, []byte(newContent), 0644)
				if err != nil {
					fmt.Printf("Error writing to file %s: %v\n", file.Name(), err)
				} else {
					fmt.Printf("Updated file: %s\n", file.Name())
				}
			}
		}
	}
}
