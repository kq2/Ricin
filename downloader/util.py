"""
Utility functions.
"""
import os
import re
import json
import urllib
from HTMLParser import HTMLParser
from xml.etree import ElementTree

HTML_PARSER = HTMLParser()


def upload(course_folder):
    """
    Upload a course folder to Google Storage
    """
    bucket = course_folder.partition('/')[2]
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
    :param url: URL to download.
    :param path: Path to save downloaded file.
    :param cookie: Cookie for URL access.
    :param resume: Resume previous download progress or not.
    :param follow_redirect: Follow the redirect URL or not.
    :param show_progress_bar: Show downloading progress bar or not.
    :return: None.
    """
    if ' ' in url:
        write_log(path)

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
    :param path: A path of folder or file.
    :param is_file: True if path is a file.
    :return: The name of the created folder.
    """
    if is_file:
        path = path.rpartition('/')[0]
    try:
        os.makedirs(path)
    except OSError:
        pass
    return path


def get_files(path):
    """
    :param path: A given directory.
    :return: A list of files and folders in this directory.
    """
    return os.listdir(path)


def remove(path):
    """
    Remove a path.
    :param path:
    :return:
    """
    try:
        os.remove(path)
    except OSError:
        print 'No such file! '


def exists(path):
    """
    Return True if path exist.
    :param path:
    :return:
    """
    return os.path.exists(path)


def make_zip(folder):
    """
    Make a zip file of given folder in current directory.
    :param folder: A given folder in current directory.
    :return: None.
    """
    os.system('zip -r {0}.zip {0}'.format(folder))


def read_file(path):
    """
    Returns the content of file.
    :param path: The path to file.
    :return: The content of file.
    """
    with open(path, 'r') as f:
        return f.read().decode('utf-8')


def write_file(path, text, append=False):
    """
    Re-write or append text to file.
    :param path: The path to file.
    :param text: The text to write.
    :param append: Append the text to file content or not.
    :return: None.
    """
    with open(path, 'a' if append else 'w') as f:
        f.write(text.encode('utf-8'))


def read_json(json_file):
    """
    Return the dictionary read from a JSON file.
    :param json_file: The JSON file to read.
    :return: The dictionary of this JSON object.
    """
    with open(json_file, 'r') as f:
        return json.load(f)


def write_json(json_file, json_obj):
    """
    Write pretty JSON to file.
    :param json_file: The JSON file to write.
    :param json_obj: The JSON object.
    :return: None.
    """
    with open(json_file, 'w') as f:
        f.write(pretty_json(json_obj))


def pretty_json(json_obj):
    """
    Pretty print JSON to console.
    :param json_obj: A JSON object.
    :return: A pretty JSON string.
    """
    return json.dumps(json_obj, indent=4)


def xml_root(xml_file):
    """
    Returns the root of XML tree.
    :param xml_file: A given XML file.
    :return: The root of this XML tree.
    """
    tree = ElementTree.parse(xml_file)
    return tree.getroot()


def unescape(text):
    """
    Unescape all HTML escape characters.
    :param text: The text with HTML escaped characters.
    :return: The text with escaped characters replaced.
    """
    return HTML_PARSER.unescape(text)


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
    :param text: The Coursera content string.
    :return: The content string with bad formats removed.
    """
    text = unescape(text)
    text = unquote(text)
    text = text.strip(' \n')
    text = re.sub(r'\w+\?page=', '', text)
    text = change_asset_url(text)
    return text


def make_coursera_new_formats(text):
    """
    Change the text to comply with Coursera's new system.
    :param text: The content from old system.
    :return: The content with new format.
    """
    text = text.replace('h4>', 'h3>')
    text = re.sub(r'<code>(.*?)</code>', r'$$\\color{red}{\\verb|\1|}$$', text)
    return text


def write_log(text):
    write_file('log.txt', text+'\n', True)


def clear_log():
    write_file('log.txt', '')
