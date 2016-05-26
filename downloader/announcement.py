"""
Download Coursera announcement page.
"""
import util


def download(course, item):
    """
    Download announcement JSON.
    :param course: A Course object.
    :param item: {
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
    item_id = item['item_id']

    path = '{}/announcement/{}.json'
    path = path.format(course.get_folder(), item_id)

    util.make_folder(path, True)
    util.write_json(path, item)

    content = util.read_file(path)
    content = util.remove_coursera_bad_formats(content)
    util.write_file(path, content)
