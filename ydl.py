# == To Install ===
# sudo curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp
# sudo chmod a+rx /usr/local/bin/yt-dlp  # Make executable
# =================

from yt_dlp import YoutubeDL

ydl_opts = {
    "skip_download": True,
    "writesubtitles": True,
    "writeautomaticsub": True,
    "subtitleslangs": ["en"],
    # Looks like formats available are vtt, ttml, srv3, srv2, srv1, json3
    "subtitlesformat": "json3",
    # You can skip the following option
    "sleep_interval_subtitles": 1,
    "paths": {
        "home": "./subtitles",
    },
}

VIDEO_IDS = ["f-tJ0_RFNvc"]

with YoutubeDL(ydl_opts) as ydl:
    ydl.download(VIDEO_IDS)
