"""
Download Coursera wiki page.
"""

import util


def download(course, item):
    """
    Download a wiki page.
    :param course: A Course object.
    :param item: {
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
    # path = '{}/wiki/info/{}.json'
    # path = path.format(course.get_folder(), item['metadata']['canonicalName'])
    #
    # util.make_folder(path, True)
    # util.write_json(path, item)
    #
    url = '{}/admin/api/pages/{}?fields=content'
    url = url.format(course.get_url(), item['item_id'])

    path = '{}/wiki/{}.html'
    path = path.format(course.get_folder(), item['metadata']['canonicalName'])

    util.download(url, path, course.get_cookie_file())

    wiki = util.read_json(path)
    content = wiki['content']
    content = util.remove_coursera_bad_formats(content)

    util.write_file(path, content)
