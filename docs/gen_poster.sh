#!/bin/bash

# Poster generation script for videos
# Extracts the first frame from all videos in source/_static/videos/
# and saves them as poster images in source/_static/images/poster/

# Define directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="$SCRIPT_DIR/source/_static/videos"
TARGET_DIR="$SCRIPT_DIR/source/_static/images/poster"

# Supported video extensions
VIDEO_EXTENSIONS=("mp4" "avi" "mov" "mkv" "webm" "flv" "wmv")

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "Error: ffmpeg is not installed. Please install ffmpeg first."
    echo "On Ubuntu/Debian: sudo apt-get install ffmpeg"
    echo "On macOS: brew install ffmpeg"
    exit 1
fi


# Check if source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
    echo "Error: Source directory '$SOURCE_DIR' does not exist."
    exit 1
fi

# Create target directory if it doesn't exist
mkdir -p "$TARGET_DIR"
echo "Created target directory: $TARGET_DIR"

# Counter for processed files
processed=0
skipped=0
failed=0

# Process all video files
echo "Processing videos in: $SOURCE_DIR"
echo "------------------------------------------------"

for video_file in "$SOURCE_DIR"/*; do
    # Check if file exists and is a regular file (skip directories)
    [ -f "$video_file" ] || continue

    # Get file extension
    filename=$(basename "$video_file")
    extension="${filename##*.}"
    filename_noext="${filename%.*}"

    # Check if file has supported video extension
    if [[ " ${VIDEO_EXTENSIONS[*]} " =~ " ${extension,,} " ]]; then
        output_file="$TARGET_DIR/${filename_noext}.jpg"

        # Check if output file already exists and is valid
        if [ -f "$output_file" ]; then
            # Verify the existing poster is valid (not empty and is an image)
            if [ -s "$output_file" ]; then
                echo "✓  Skipping '$filename' (poster already exists)"
                ((skipped++))
                continue
            else
                echo "⚠  Removing invalid poster for '$filename'"
                rm -f "$output_file"
            fi
        fi

        echo "⏳ Processing '$filename'..."

        echo "Running: ffmpeg -i \"$video_file\" -vframes 1 -q:v 2 \"$output_file\" -y -loglevel error"
        if ffmpeg -i "$video_file" -vframes 1 -q:v 2 "$output_file" -y -loglevel error 2>&1; then
            ffmpeg_success=true
        else
            echo "ffmpeg command timed out or failed."
            ffmpeg_success=false
        fi
    

        # Add small delay to prevent system overload
        sleep 0.1

        if $ffmpeg_success; then
            # Verify the output file was created and is valid
            if [ -f "$output_file" ] && [ -s "$output_file" ]; then
                echo "✓ Created poster: ${filename_noext}.jpg"
                ((processed++))
            else
                echo "✗ Failed to create valid poster for '$filename'"
                rm -f "$output_file"  # Remove any partial output
                ((failed++))
            fi
        else
            # ffmpeg failed
            exit_code=$?
            if [ $exit_code -eq 124 ]; then
                echo "✗ Timeout processing '$filename' (after 30s)"
            else
                echo "✗ Failed to process '$filename' (exit code: $exit_code)"
            fi
            rm -f "$output_file"  # Remove any partial output
            ((failed++))
        fi
    else
        echo "⊘  Skipping '$filename' (not a supported video format)"
        ((skipped++))
    fi
done

echo "------------------------------------------------"
echo "Poster generation completed!"
echo "📊 Summary:"
echo "   ✓ Processed: $processed videos"
echo "   → Skipped: $skipped files"
if [ $failed -gt 0 ]; then
    echo "   ✗ Failed: $failed videos"
fi
echo "   Posters saved to: $TARGET_DIR"

if [ $processed -eq 0 ]; then
    if [ $failed -eq 0 ]; then
        echo "ℹ  No new posters were created."
    else
        echo "⚠  Some posters failed to generate. Please check the error messages above."
    fi
fi