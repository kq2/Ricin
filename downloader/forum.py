"""
Download Coursera quiz.
"""
import util


def download(course_obj, thread_id):
    """
    Download quiz XML.
    :param course_obj: A Course object.
    :param thread_id:
    :return: None.
    """
    folder = util.make_folder(course_obj.get_folder() + 'forum/')

    url = course_obj.get_url() + '/api/forum/threads/' + thread_id + '?sort=null'
    path = folder + thread_id + '.json'
    util.download(url, path, course_obj.get_cookie_file())

    content = util.pretty_json(util.read_json(path))
    util.write_file(path, content)
