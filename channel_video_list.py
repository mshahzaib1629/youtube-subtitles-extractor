# -*- coding: utf-8 -*-

# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
import argparse

import googleapiclient.discovery
from dotenv import load_dotenv
load_dotenv()

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


def get_videos_list(channel_id, max_results, pageToken=None):
    api_service_name = "youtube"
    api_version = "v3"
    api_key = os.getenv("GOOGLE_API_KEY")

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=api_key
    )

    request = youtube.activities().list(
        part="contentDetails",
        channelId=channel_id,
        maxResults=max_results,
        pageToken=pageToken
    )
    response = request.execute()
       
    for item in response["items"]:
        if "upload" in item["contentDetails"].keys():
            print(f"videoId (u): ", item["contentDetails"]["upload"]["videoId"])
        elif "playlistItem" in item["contentDetails"].keys():
            print(
                f"videoId (p): ",
                item["contentDetails"]["playlistItem"]["resourceId"]["videoId"],
            )

    print(f'page info: {response["pageInfo"]}')
    if "nextPageToken" in response.keys():
        nextPageToken = response["nextPageToken"]
        print(f'next page token: {nextPageToken}') 
        print('page break ------------------------')
        get_videos_list(channel_id, MAX_RESULTS, nextPageToken)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get video IDs from a YouTube channel')
    parser.add_argument('--channel_id', '-c', type=str, help='YouTube channel ID')
    parser.add_argument('--max_results', '-m', type=int, default=300, 
                        help='Maximum number of results per page (default: 300)')
    args = parser.parse_args()
    
    # If channel_id is not provided via argument, prompt the user
    channel_id = args.channel_id
    if not channel_id:
        channel_id = input("Enter the YouTube channel ID: ")
    
    MAX_RESULTS = args.max_results
    print(f"Fetching videos for channel ID: {channel_id}")
    get_videos_list(channel_id, MAX_RESULTS)
