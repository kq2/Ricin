"""
Utility functions.
"""
import os
import re
import json
import codecs
import urllib
from HTMLParser import HTMLParser
from xml.etree import ElementTree

HTML_PARSER = HTMLParser()


def upload(course_folder):
    """
    Upload a course folder to Google Storage
    """
    if not exists(course_folder):
        print course_folder, 'does not exist!'
        return

    bucket = course_folder.replace('../', '')
    gs_bucket = 'gs://codeskulptor-archives/{}'.format(bucket)

    # exclude: original_videos folder, pii.csv, email_blacklist.csv, .DS_Store
    exclude = '.*original_videos/|.*pii\.csv$|.*email_blacklist\.csv$|.*\.DS_Store$'

    cmd = "gsutil -m rsync -r -x '{}' {} {}"
    cmd = cmd.format(exclude, course_folder, gs_bucket)

    os.system(cmd)


def download(url, path='', cookie='', resume=False,
             follow_redirect=True, show_progress_bar=True):
    """
    Use cURL to download an URL.
    """
    url = urllib.quote(url, safe="%/:=&?~#+!$,;'@()*[]")
    print "downloading {}".format(url)

    cmd = u'curl "{}"'.format(url.replace('"', '\\"'))

    if path:
        make_folder(path, True)
        cmd += u' -o "{}"'.format(path.replace('"', '\\"'))
    else:
        cmd += u' -O'

    if cookie:
        cmd += u' --cookie "{}"'.format(cookie)

    if resume:
        cmd += u' -C -'

    if follow_redirect:
        cmd += u' -L'

    if show_progress_bar:
        cmd += u' -#'

    cmd = cmd.encode('utf-8')
    os.system(cmd)


def make_folder(path, is_file=False):
    """
    Create a folder and return its name.
    """
    if is_file:
        path = path.rpartition('/')[0]
    try:
        os.makedirs(path)
    except OSError:
        pass
    return path


def copy_folder(from_folder, to_folder):
    """
    Copy a folder to another place.
    """
    make_folder(to_folder)
    cmd = 'cp -R {}/ {}/'.format(from_folder, to_folder)
    os.system(cmd)


def get_files(path):
    """
    Return a list of folders/files in given path.
    """
    return os.listdir(path)


def remove(path):
    """
    Remove a path.
    """
    try:
        os.remove(path)
    except OSError:
        print 'No such file! '


def exists(path):
    """
    Return True if path exist.
    """
    return os.path.exists(path)


def make_zip(path):
    """
    Make a zip file of given folder.
    """
    folder = path.rpartition('/')[2]
    zip_file = folder + '.zip'
    cmd = 'cd {0}; zip -r {1} .; mv {1} ..'.format(path, zip_file)
    os.system(cmd)


def read_file(path):
    """
    Return the content of file.
    """
    with open(path, 'r') as f:
        return f.read().decode('utf-8')


def write_file(path, text, append=False):
    """
    Re-write or append text to file.
    """
    make_folder(path, True)
    with open(path, 'a' if append else 'w') as f:
        f.write(text.encode('utf-8'))


def read_json(src, is_string=False):
    """
    Return the dictionary read from a JSON file.
    """
    if is_string:
        return json.loads(src)
    with open(src, 'r') as f:
        return json.load(f)


def write_json(json_file, json_obj):
    """
    Write pretty JSON to file.
    """
    with open(json_file, 'w') as f:
        f.write(pretty_json(json_obj))


def pretty_json(json_obj):
    """
    Pretty print JSON to console.
    """
    return json.dumps(json_obj, indent=4)


def read_xml(xml, is_string=False):
    """
    Return the root of an XML tree.
    """
    if is_string:
        return ElementTree.fromstring(xml.encode('utf-8'))
    else:
        return ElementTree.parse(xml).getroot()


def unescape(text):
    """
    Un-escape all HTML escape characters.
    """
    return HTML_PARSER.unescape(text)


def unicode_unescape(unicode_str):
    """
    Un-escape escaped characters (\" --> ").
    """
    return codecs.decode(unicode_str, "unicode_escape")


def unquote(url):
    """
    Unquote an URL.
    """
    return urllib.unquote(url)


def change_asset_url(text):
    """
    Change asset URL to relative URL
    https://d396qusza40orc.cloudfront.net/thinkpython/images/bfs.png ->
    ../../../thinkpython/assets/images/bfs.png
    """
    old_url = r'https://.*?\.cloudfront\.net/(\w+)/'
    new_url = r'../../../\1/assets/'
    return re.sub(old_url, new_url, text)


def remove_coursera_bad_formats(text):
    """
    Remove Coursera bad formats.
    """
    text = unescape(text)
    text = text.strip(' \n')
    text = re.sub(r'\w+\?page=', '', text)
    text = change_asset_url(text)
    return text


def make_coursera_new_formats(text):
    """
    Change the text to comply with Coursera's new system.
    """
    text = text.replace('h4>', 'h3>')
    text = re.sub(r'<code>(.*?)</code>', r'$$\\color{red}{\\verb|\1|}$$', text)
    return text


def write_log(text):
    write_file('log.txt', text + '\n', True)


def clear_log():
    write_file('log.txt', '')
