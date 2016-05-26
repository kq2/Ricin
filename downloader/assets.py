"""
Download Coursera course assets.
"""
import os
import re
import util


def download(course):
    """
    Download course assets.
    :param course: A Coursera course object.
    :return: None
    """
    url = course.get_url() + '/admin/assets'
    folder = course.get_folder() + '/assets'

    cookie = course.get_cookie_file()
    files = _find_files(url, folder, cookie)

    num_file = len(files)
    for idx, (url, path) in enumerate(files):
        print '{}/{}'.format(idx + 1, num_file)
        util.download(url, path, cookie, resume=True)


def _find_files(url, folder, cookie):
    """
    Recursively find all files in current folder.
    :param url: A URL to given page.
    :param folder: A destination folder for this page.
    :param cookie: A cookie file used for downloading.
    :return: A list of files (url, path) in current folder.
    """
    files = []

    path = '{}/temp.html'.format(folder)
    util.download(url, path, cookie)

    page = util.read_file(path)
    os.remove(path)

    # recursively inspect all folders in this page
    pattern = r'<tr><td colspan="4"><a href="(.*?)">(.*?)</a>'
    for find in re.finditer(pattern, page, re.DOTALL):
        url = find.group(1)
        sub_folder = '{}/{}'.format(folder, find.group(2))
        files += _find_files(url, sub_folder, cookie)

    # find all files in this page
    pattern = r'<tr><td>(.*?)</td>.*?Embed.*?<a href="(.*?)\?.*?">Download</a>'
    for find in re.finditer(pattern, page, re.DOTALL):
        url = find.group(2)
        path = '{}/{}'.format(folder, find.group(1))
        files.append((url, path))

    return files
