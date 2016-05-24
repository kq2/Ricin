"""
Download Coursera quiz.
"""
import re
import util


def download(course_obj, course_item):
    """
    Download quiz XML.
    :param course_obj: A Course object.
    :param course_item: {
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
    folder = util.make_folder(course_obj.get_folder() + 'quiz/')
    item_id = course_item['item_id']
    
    url = course_obj.get_url() + '/admin/quiz/raw_edit?quiz_id=' + item_id
    path = folder + item_id + '.xml'
    util.download(url, path, course_obj.get_cookie_file())

    pattern = r'<textarea.*?>(.*)</textarea>'
    content = re.search(pattern, util.read_file(path), re.DOTALL).group(1)
    content = util.remove_coursera_bad_formats(content)
    content = '<?xml version="1.0" encoding="UTF-8"?>\n' + content
    util.write_file(path, content)
