"""
Ensemble module.
"""

import os
import util

COOKIE = 'ensemble_cookie.txt'


def get_data(api):
    response = 'temp.json'
    url = 'https://mediacosmos.rice.edu/api/' + api
    cmd = 'curl {} -o {} --cookie {}'.format(url, response, COOKIE)
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


def upload(video, upload_access):
    response = 'temp.txt'
    upload_id = upload_access['Data'][0]['ID']
    submit_url = upload_access['Settings']['SubmitUrl']

    # -o is used for showing upload progress meter
    cmd = 'curl -i -F FileData=@{} -F MediaWorkflowID={} {} -o {}'
    cmd = cmd.format(video, upload_id, submit_url, response)
    os.system(cmd)

    util.remove(response)
