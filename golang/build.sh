#!/bin/bash

# Set the names of your Go scripts and programs
SCRIPT_FOLDERS=("serve_folder" "replace_annotations")
PROGRAM_NAMES=("File_server" "Label_Replace")

INDEX=0
for script in "${SCRIPT_FOLDERS[@]}"
do
    PROGRAM_NAME=${PROGRAM_NAMES[INDEX]}
    ((INDEX++)) 
    cd $script

    OUTPUT_DIR="bin"

    mkdir -p $OUTPUT_DIR

    platforms=("windows/amd64" "linux/amd64" "darwin/amd64")

    # Loop through each platform and build the binary
    for platform in "${platforms[@]}"
    do
        IFS="/" read -r -a platform_split <<< "$platform"
        GOOS=${platform_split[0]}
        GOARCH=${platform_split[1]}

        output_name="$OUTPUT_DIR/$PROGRAM_NAME-$GOOS-$GOARCH"
        if [ "$GOOS" = "windows" ]; then
            output_name+='.exe'
        fi

        echo "Compiling $PROGRAM_NAME for $GOOS/$GOARCH..."
        env GOOS=$GOOS GOARCH=$GOARCH go build -o $output_name

        if [ $? -ne 0 ]; then
            echo "Failed to compile $PROGRAM_NAME for $GOOS/$GOARCH"
            exit 1
        fi
    done

    echo "Compilation of $PROGRAM_NAME finished!"
    cd ..
done

echo "All compilations finished!"
