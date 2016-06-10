"""
Download Coursera quiz.
"""
import re
import util


def download(course, item):
    """
    Download quiz XML.
    :param course: A Course object.
    :param item: {
        "last_updated": 1409275771,
        "authentication_required": 1,
        "proctoring_requirement": "none",
        "open_time": 1409263200,
        "parent_id": 87,
        "soft_close_time": 1409752800,
        "duration": 0,
        "maximum_submissions": 1,
        "deleted": 0,
        "section_id": "6",
        "__type": "quiz",
        "order": "8",
        "item_type": "quiz",
        "quiz_type": "survey",
        "hard_close_time": 1409925600,
        "item_id": "87",
        "title": "Welcome Survey",
        "__published": 1,
        "id": 88,
        "uid": "quiz88"
    }
    :return: None.
    """
    # path = '{}/quiz/info/{}.json'
    # path = path.format(course.get_folder(), item['item_id'])
    #
    # util.make_folder(path, True)
    # util.write_json(path, item)
    #
    url = '{}/admin/quiz/raw_edit?quiz_id={}'
    url = url.format(course.get_url(), item['item_id'])

    path = '{}/quiz/{}.xml'
    path = path.format(course.get_folder(), item['item_id'])

    util.download(url, path, course.get_cookie_file())

    pattern = r'<textarea.*?>(.*)</textarea>'
    xml = re.search(pattern, util.read_file(path), re.DOTALL).group(1)
    xml = util.remove_coursera_bad_formats(xml, course.get_name())
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n' + xml

    util.write_file(path, xml)
