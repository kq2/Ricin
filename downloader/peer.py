"""
Download Coursera peer-grading page.
"""
import util


def download(course, item):
    """
    Download peer-grading JSON.
    :param course: A Course object.
    :param item: This JSON item is directly written into saved file.
    :return: None.
    """
    path = '{}/peer_assessment/{}.json'
    path = path.format(course.get_folder(), item['item_id'])

    util.make_folder(path, True)
    util.write_json(path, item)

    content = util.read_file(path)
    content = util.remove_coursera_bad_formats(content)

    util.write_file(path, content)
