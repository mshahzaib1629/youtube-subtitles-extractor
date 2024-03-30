import json, os


def subtitle_extractor(file_path):
    # Provided JSON data
    json_data = {}

    with open(file_path, "r") as json_file:
        json_data = json.load(json_file)

    # Initialize an empty string to hold the concatenated subtitles
    subtitle_string = ""

    # Iterate through each event in the JSON data
    for event in json_data["events"]:
        # Iterate through each segment in the event
        for seg in event.get("segs", []):
            # Concatenate the utf8 content from each segment
            subtitle_string += seg.get("utf8", "")

    return subtitle_string


FILE_NAME = "Israel： Above the law？ ｜ Featured Documentary [ueXEXjqXNvk].en.json3"
file_path = os.path.join("subtitles", FILE_NAME)
print(subtitle_extractor(file_path))
