# YouSub

A Python toolset to fetch video IDs from YouTube channels and download their subtitles in multiple languages.

## Requirements

- Python Version: `3.12.2`
- Google API key (for the channel video list functionality)

## Installation

### 1. Clone the repository

```bash
git clone [repository-url]
cd youtube-subtitles-extractor
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Windows:
```bash
venv\Scripts\activate
```

macOS/Linux:
```bash
source venv/bin/activate
```

### 4. Install required packages

```bash
pip install -r requirements.txt
```

## Configuration

For the channel video list functionality, you need to set up a Google API key:

1. Generate a Google API key from the [Google Cloud Console](https://console.cloud.google.com/):
   - Create a new project or use an existing one
   - Navigate to "APIs & Services" > "Library"
   - Search for and enable the "YouTube Data API v3"
   - Navigate to "APIs & Services" > "Credentials"
   - Click "Create credentials" > "API key"
   - Copy your newly created API key

2. Create a `.env` file in the root directory
3. Add your Google API key to the file:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

### How to Find a YouTube Channel ID

To use the channel_video_list.py script, you need the channel ID of the YouTube channel you want to extract videos from. Here's how to find it:

1. Visit the YouTube channel in your browser
2. Click on the "About" tab or navigate to the channel's About page
3. Click the "Share Channel" button
4. Select "Copy channel ID" from the options

Alternatively, for newer YouTube interface:
1. Navigate to the YouTube channel
2. Click on the three dots "..." (More) button
3. Click "Share Channel"
4. Click "Copy channel ID"

The channel ID will typically look like: `UCNye-wNBqNL5ZzHSJj3l8Bg` (a string starting with UC followed by letters and numbers).

## Usage

### Getting Video IDs from a Channel

```bash
python channel_video_list.py
```

You can provide the channel ID directly as a command-line argument:

```bash
python channel_video_list.py --channel_id CHANNEL_ID
```

Or with the short option:

```bash
python channel_video_list.py -c CHANNEL_ID -m 30
```

You can also specify the maximum number of results per page:

```bash
python channel_video_list.py -c CHANNEL_ID --max_results 500
```

If you don't provide a channel ID, the script will prompt you to enter one.

### Downloading and Processing Subtitles

```bash
python youtube_subtitle_downloader.py [video_ids]
```

Options:
- Pass video IDs as arguments: `python youtube_subtitle_downloader.py dQw4w9WgXcQ xvFZjo5PgG0`
- Specify languages with `-l` or `--languages`: `python youtube_subtitle_downloader.py dQw4w9WgXcQ -l en,fr,es`
- Check available subtitle languages with `-c` or `--check`: `python youtube_subtitle_downloader.py dQw4w9WgXcQ -c`

If no video IDs are provided as arguments, the script will prompt you to enter them interactively.

## Output

- Downloaded subtitle files (JSON3 format) are saved in the `subtitles/` directory
- Extracted plaintext subtitles are saved in the `outputs/` directory

## File Structure

```
youtube-subtitles-extractor/
│
├── channel_video_list.py      # Script to fetch video IDs from a channel
├── youtube_subtitle_downloader.py  # Script to download and process subtitles
├── requirements.txt           # Required Python packages
├── .env                       # Environment variables (not tracked by git)
│
├── subtitles/                 # Downloaded subtitle files in JSON3 format
└── outputs/                   # Extracted plaintext subtitle files
```

## Examples

1. Get all video IDs from a channel:
   ```bash
   python channel_video_list.py -c UCNye-wNBqNL5ZzHSJj3l8Bg
   ```

2. Download English subtitles for a video:
   ```bash
   python youtube_subtitle_downloader.py dQw4w9WgXcQ -l en
   ```

3. Check available languages for a video:
   ```bash
   python youtube_subtitle_downloader.py dQw4w9WgXcQ -c
   ```

4. Download multiple language subtitles for multiple videos:
   ```bash
   python youtube_subtitle_downloader.py dQw4w9WgXcQ xvFZjo5PgG0 -l en,fr,es
   ```

