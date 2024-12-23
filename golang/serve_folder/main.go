package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
)

const helpText = `
Usage: go run main.go [INPUT_DIR] [IP_ADDRESS] [PORT]

Serves video files from the specified directory on a local web server.

Arguments:
  INPUT_DIR   The directory containing the video files to serve.
  IP_ADDRESS  The IP address where the server will be accessible.
  PORT        The port number on which the server will listen.

Example:
  go run main.go ./videos 127.0.0.1 8080

The files will be available at: http://127.0.0.1:8080/FILENAME
`

func main() {
	args := os.Args

	if len(args) < 2 || args[1] == "-h" || args[1] == "--help" {
		fmt.Println(helpText)
		return
	}

	if len(args) != 4 {
		fmt.Println("Error: Incorrect number of arguments.")
		fmt.Println(helpText)
		return
	}

	inputDir := args[1]
	ip := args[2]
	port := args[3]

	fs := http.FileServer(http.Dir(inputDir))
	http.Handle("/", fs)

	log.Printf("Serving files on http://%s:%s\n", ip, port)
	err := http.ListenAndServe(fmt.Sprintf("%s:%s", ip, port), nil)
	if err != nil {
		log.Fatal(err)
	}
}
