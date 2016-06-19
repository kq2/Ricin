"""
Ensemble module.
"""

import os
import util

COOKIE = 'ensemble_cookie.txt'


def get_data(api):
    response = 'temp.json'
    url = 'https://mediacosmos.rice.edu/api/' + api
    cmd = 'curl "{}" -o "{}" --cookie {}'.format(url, response, COOKIE)
    os.system(cmd)

    data = util.read_json(response)
    util.remove(response)
    return data


def get_library_list():
    api = 'libraries?PageSize=999'
    return get_data(api)['Data']


def get_video_list(library_id):
    api = 'content/{}?PageSize=9999'
    api = api.format(library_id)
    return get_data(api)['Data']


def get_upload_access(library_id):
    api = 'MediaWorkflows?FilterOn=LibraryID&FilterValue={}'
    api = api.format(library_id)
    return get_data(api)


def upload(video, title, upload_access):
    response = 'temp.txt'
    video = video.replace('"', '\\"')
    title = title.replace('"', '\\"')
    upload_id = upload_access['Data'][0]['ID']
    submit_url = upload_access['Settings']['SubmitUrl']

    # -o is used for showing upload progress meter
    cmd = 'curl -i -F FileData=@"{}" -F Title="{}" -F MediaWorkflowID={} {} -o {}'
    cmd = cmd.format(video, title, upload_id, submit_url, response)
    os.system(cmd)


def run(library_id):
    upload_access = get_upload_access(library_id)
    videos = util.read_json('videos.json')

    num_videos = len(videos)
    for idx, (path, title) in enumerate(videos.values()):
        print '{}/{}'.format(idx + 1, num_videos), path
        upload(path, title, upload_access)


# run('457006af-2dd9-4f5a-a310-8fcef3d02eeb')
