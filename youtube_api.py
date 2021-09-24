from googleapiclient.discovery import build
import json
import os


def video_search(vid_name, release_year):
    with build('youtube','v3', developerKey=os.environ['Youtube_key']) as yt:
        request = yt.search().list(
            part = 'snippet',
            q = vid_name + " " + release_year + " trailer"
        )
        response = request.execute()
        # new_res = json.dumps(response, indent=4, sort_keys=True, ensure_ascii=False)
        # print(new_res)
        vid_id = response['items'][0]["id"]["videoId"]
        
        return vid_id