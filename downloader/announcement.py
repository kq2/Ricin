"""
Download Coursera announcement page.
"""
import util


def download(course_obj, course_item):
    """
    Download announcement JSON.
    :param course_obj: A Course object.
    :param course_item: {
        "close_time": 2147483647,
        "user_id": 1069689,
        "open_time": 1411654451,
        "title": "Coursera",
        "deleted": 0,
        "email_announcements": "email_sent",
        "section_id": "14",
        "order": "6",
        "item_type": "announcement",
        "__type": "announcement",
        "published": 1,
        "item_id": "39",
        "message": "Hello, everyone.",
        "uid": "announcement39",
        "id": 39,
        "icon": ""
    }
    :return: None.
    """
    folder = util.make_folder(course_obj.get_folder() + 'announcement/')
    item_id = course_item['item_id']

    path = folder + item_id + '.json'
    util.write_json(path, course_item)

    content = util.read_file(path)
    content = util.remove_coursera_bad_formats(content)
    util.write_file(path, content)
