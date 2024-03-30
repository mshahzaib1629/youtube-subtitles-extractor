# -*- coding: utf-8 -*-

# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os

import googleapiclient.discovery
import googleapiclient.errors
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


CHANNEL_ID = "UCNye-wNBqNL5ZzHSJj3l8Bg"
MAX_RESULTS = 300
get_videos_list(CHANNEL_ID, MAX_RESULTS)
