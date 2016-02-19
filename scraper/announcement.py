"""
Download Coursera announcement page.
"""
import re
import util


def download(course_obj, course_item):
    """
    Download announcement JSON.
    :param course_obj: A Course object.
    :param course_item: This JSON item is directly written into saved file.
    :return: None.
    """
    folder = util.make_folder(course_obj.get_folder() + 'announcement/')
    item_id = course_item['item_id']

    path = folder + item_id + '.json'
    util.write_json(path, course_item)

    content = util.read_file(path)
    content = util.remove_coursera_bad_formats(content)
    util.write_file(path, content)