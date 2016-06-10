"""
Download Coursera assignment.
"""
import re
import util


def download(course, item):
    """
    Download assignment HTML.
    :param course: A Course object.
    :param item: {
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
    # path = '{}/assignment/info/{}.json'
    # path = path.format(course.get_folder(), item['item_id'])
    #
    # util.make_folder(path, True)
    # util.write_json(path, item)
    #
    url = '{}/admin/assignment?assignment_id={}'
    url = url.format(course.get_url(), item['item_id'])

    path = '{}/assignment/{}.html'
    path = path.format(course.get_folder(), item['item_id'])

    util.download(url, path, course.get_cookie_file())

    pattern = r'<textarea.*?>(.*)</textarea>'
    content = re.search(pattern, util.read_file(path), re.DOTALL).group(1)
    content = util.remove_coursera_bad_formats(content, course.get_name())

    util.write_file(path, content)
