"""
Download Coursera wiki page.
"""

import util


def download(course_obj, course_item):
    """
    Download wiki page HTML.
    :param course_obj: A Course object.
    :param course_item: {
        "uid": "coursepageEYJIs_YAEeKNdCIACugoiw",
        "section_id": "27",
        "order": "1",
        "item_type": "coursepage",
        "__type": "coursepage",
        "item_id": "EYJIs_YAEeKNdCIACugoiw",
        "id": "EYJIs_YAEeKNdCIACugoiw",
        "metadata": {
            "openTime": 1373785724930,
            "locked": true,
            "creator": 726142,
            "title": "Home",
            "modified": 1405321775510,
            "canonicalName": "home",
            "created": 1374849092873,
            "visible": true,
            "version": 11
        }
    }
    :return: None.
    """
    folder = util.make_folder(course_obj.get_folder() + 'wiki/')
    filename = course_item['metadata']['canonicalName']
    item_id = course_item['item_id']

    url = course_obj.get_url() + '/admin/api/pages/' + item_id + '?fields=content'
    path = folder + filename + '.html'
    util.download(url, path, course_obj.get_cookie_file())

    content = util.read_json(path)['content']
    content = util.remove_coursera_bad_formats(content)
    util.write_file(path, content)
