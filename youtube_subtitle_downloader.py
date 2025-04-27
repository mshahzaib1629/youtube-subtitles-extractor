import json
import os
import sys
import argparse
from yt_dlp import YoutubeDL

def list_available_languages(video_id):
    """
    List all available subtitle languages for a YouTube video
    """
    ydl_opts = {
        "skip_download": True,
        "listsubtitles": True,
    }
    
    print(f"Checking available subtitle languages for {video_id}...")
    
    with YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            # If we get here, the video exists, but we need to check if it has subtitles
            # The output is printed directly by yt-dlp
            return True
        except Exception as e:
            print(f"Error checking subtitles for {video_id}: {str(e)}")
            return False

def download_subtitles(video_ids, languages=None):
    """
    Download subtitles for the given list of YouTube video IDs in the specified languages.
    Returns a list of paths to the downloaded subtitle files.
    """
    # If no languages specified, default to English
    if not languages:
        languages = ["en"]
        
    ydl_opts = {
        "skip_download": True,
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": languages,
        "subtitlesformat": "json3",
        "sleep_interval_subtitles": 1,
        "paths": {
            "home": "./subtitles",
        },
    }
    
    print(f"Downloading subtitles for {len(video_ids)} video(s) in languages: {', '.join(languages)}...")
    
    with YoutubeDL(ydl_opts) as ydl:
        info_results = ydl.download(video_ids)
    
    # Get the files that were downloaded
    subtitle_files = []
    # Make sure the subtitles directory exists
    if not os.path.exists("subtitles"):
        return subtitle_files
    
    files = os.listdir("subtitles")
    for video_id in video_ids:
        # Find files matching this video ID and our languages
        for lang in languages:
            matching_files = [f for f in files if video_id in f and f.endswith(f".{lang}.json3")]
            if matching_files:
                subtitle_files.extend([os.path.join("subtitles", f) for f in matching_files])
    
    return subtitle_files

def extract_subtitle_text(file_path):
    """
    Extract subtitle text from the JSON3 subtitle file.
    Returns the extracted text as a string.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as json_file:
            json_data = json.load(json_file)
        
        subtitle_string = ""
        
        # Iterate through each event in the JSON data
        for event in json_data["events"]:
            # Iterate through each segment in the event
            for seg in event.get("segs", []):
                # Concatenate the utf8 content from each segment
                subtitle_string += seg.get("utf8", "")
        
        return subtitle_string
    except Exception as e:
        print(f"Error extracting subtitles from {file_path}: {str(e)}")
        return ""

def save_subtitle_text(subtitle_text, original_file_path):
    """
    Save the extracted subtitle text to a file in the outputs directory.
    """
    # Create outputs directory if it doesn't exist
    if not os.path.exists("outputs"):
        os.makedirs("outputs")
    
    # Get the base filename without extension
    base_name = os.path.basename(original_file_path)
    file_name = ".".join(base_name.split(".")[:-1])  # Remove the .json3 extension
    
    # Create the output file path
    output_file = os.path.join("outputs", f"{file_name}.txt")
    
    # Save the subtitle text to the output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(subtitle_text)
    
    print(f"Saved subtitle text to {output_file}")
    return output_file

def display_language_menu():
    """
    Display an interactive menu for language selection
    """
    common_languages = [
        ("en", "English"),
        ("es", "Spanish"),
        ("fr", "French"),
        ("de", "German"),
        ("ar", "Arabic"),
        ("ur", "Urdu"),
        ("hi", "Hindi"),
    ]
    
    print("\nSelect languages (comma-separated numbers, e.g., '1,3,5'):")
    for i, (code, name) in enumerate(common_languages, 1):
        print(f"{i}. {name} ({code})")
    print("14. Other (specify language code)")
    
    selection = input("\nEnter your selection: ")
    selected_languages = []
    
    if selection.strip():
        try:
            # Parse the comma-separated selection
            for num in selection.split(","):
                num = int(num.strip())
                if 1 <= num <= len(common_languages):
                    selected_languages.append(common_languages[num-1][0])
                elif num == 14:
                    # Custom language code entry
                    custom_code = input("Enter language code(s) separated by commas (e.g., vi,th,nl): ")
                    selected_languages.extend([code.strip() for code in custom_code.split(",") if code.strip()])
        except ValueError:
            print("Invalid selection, defaulting to English")
            selected_languages = ["en"]
    
    # If no valid languages were selected, default to English
    if not selected_languages:
        print("No languages selected, defaulting to English")
        selected_languages = ["en"]
    
    return selected_languages

def parse_arguments():
    """
    Parse command line arguments for the script
    """
    parser = argparse.ArgumentParser(description='Download and extract YouTube subtitles')
    parser.add_argument('video_ids', nargs='*', help='YouTube video IDs')
    parser.add_argument('-l', '--languages', help='Comma-separated language codes (e.g., en,fr,es)')
    parser.add_argument('-c', '--check', action='store_true', help='Check available subtitle languages for videos')
    
    args = parser.parse_args()
    
    # Process language codes if provided
    languages = []
    if args.languages:
        languages = [lang.strip() for lang in args.languages.split(',') if lang.strip()]
    
    return args.video_ids, languages, args.check

def main():
    # Parse command line arguments
    video_ids, languages, check_languages = parse_arguments()
    
    # If no video IDs provided via command line, prompt the user
    if not video_ids:
        video_input = input("Enter YouTube video IDs (separated by spaces): ")
        video_ids = video_input.split()
    
    if not video_ids:
        print("No video IDs provided. Exiting.")
        return
    
    # If check_languages flag is set, list available languages for each video
    if check_languages:
        for video_id in video_ids:
            list_available_languages(video_id)
        return
    
    # If no languages specified through command line, show language selection menu
    if not languages:
        languages = display_language_menu()
    
    print(f"Selected languages: {', '.join(languages)}")
    
    # Download subtitles
    subtitle_files = download_subtitles(video_ids, languages)
    
    if not subtitle_files:
        print("No subtitle files were downloaded.")
        return
    
    print(f"Downloaded {len(subtitle_files)} subtitle file(s).")
    
    # Extract and save subtitle text for each file
    for file_path in subtitle_files:
        print(f"Processing {file_path}...")
        subtitle_text = extract_subtitle_text(file_path)
        if subtitle_text:
            output_file = save_subtitle_text(subtitle_text, file_path)
        else:
            print(f"No subtitle text was extracted from {file_path}")

if __name__ == "__main__":
    main()