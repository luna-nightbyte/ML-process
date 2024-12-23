# Golang scirpts
## Compile and Run
### Compile

To build, install Golang and run `go build` from within one of the script folders. 
Alternatevly, i have pre-compiled binaries for windows, linux and mac using `bash.sh`. These files are located in the `bin`folders.

### Run
#### Bin
Each program has a pre-compiled binary that can be used for Linux, Windows, and Mac.

#### Serve video folder
This script serves a folder of files. 
`server.py` is hardcoded to use only files with `.mp4`, `.jpg` and `.png` extentions. 
Files will be availavle on any local device on `http://IP_ADDRESS:PORT/VIDEO_NAME` and/or [localhost](http://localhost:8050/video_name)
#### Replace annotations
This script simply replaces a string within an annotatopn with a new one. 
It just reads the file and replaces old string with new. 


