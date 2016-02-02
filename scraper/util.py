"""
Utility functions.
"""
import os
import json
from HTMLParser import HTMLParser

HTML_PARSER = HTMLParser()


def download(url, path='', cookie='', resume=False,
             follow_redirect=False, show_progress_bar=True):
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
    print "downloading %s" % url

    cmd = 'curl "%s"' % url
    cmd += ' -o "%s"' % path if path else ' -O'
    if cookie:
        cmd += ' --cookie "%s"' % cookie
    if resume:
        cmd += ' -C -'
    if follow_redirect:
        cmd += ' -L'
    if show_progress_bar:
        cmd += ' -#'
    os.system(cmd)


def make_folder(folder):
    """
    Try create a folder and return the folder name
    :param folder: The folder to create.
    :return: The folder name.
    """
    try:
        os.makedirs(folder)
    except OSError:
        pass
    return folder


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
    with open(json_file, 'r') as _file:
        return json.load(_file)


def unescape(text):
    """
    Un-escape all HTML escape characters.
    :param text: The text with HTML escaped characters.
    :return: The text with escaped characters replaced.
    """
    return HTML_PARSER.unescape(text)


def remove_coursera_bad_formats(text):
    """
    Remove Coursera bad formats.
    :param text: The Coursera content string.
    :return: The content string with bad formats removed.
    """
    text = unescape(text)
    text = text.strip(' \n')
    text = text.replace('view\?page=', '')
    return text
