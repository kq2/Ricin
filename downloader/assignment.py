"""
Download Coursera assignment.
"""
import re
import util


def download(course_obj, course_item):
    """
    Download assignment HTML.
    :param course_obj: A Course object.
    :param course_item: {
        "maximum_submissions": 0,
        "open_time": 1409234400,
        "parent_id": 5,
        "soft_close_time": 1409965200,
        "title": "Module 1: Circles",
        "deleted": 0,
        "section_id": "6",
        "order": "9",
        "item_type": "assignment",
        "__type": "assignment",
        "hard_close_time": 1410138000,
        "item_id": "5",
        "last_updated": 1409236863,
        "__published": 1,
        "id": 6,
        "uid": "assignment6"
    }
    :return: None.
    """
    folder = util.make_folder(course_obj.get_folder() + 'assignment/')
    item_id = course_item['item_id']

    url = course_obj.get_url() + '/admin/assignment?assignment_id=' + item_id
    path = folder + item_id + '.html'
    util.download(url, path, course_obj.get_cookie_file())

    pattern = r'<textarea.*?>(.*)</textarea>'
    content = re.search(pattern, util.read_file(path), re.DOTALL).group(1)
    content = util.remove_coursera_bad_formats(content)
    util.write_file(path, content)
