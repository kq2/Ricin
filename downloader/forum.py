"""
Download Coursera forum.
"""
import util


def download(course):
    """
    Download forum.
    :param course: A Course object.
    :return: None.
    """
    forum_id = 0
    folder = course.get_folder() + '/forum/forum'

    forums = []
    download_forum(forums, forum_id, folder, course)

    total = len(forums)
    for idx, (forum_id, folder) in enumerate(forums):
        print 'forum {}/{}'.format(idx + 1, total)

        # Notice: forum 0 has every thread!
        download_pages(forum_id, folder, course)


def download_forum(forums, forum_id, folder, course):
    """
    Recursively download all sub-forums in current forum.
    :param forums:
    :param forum_id:
    :param folder:
    :param course:
    :return:
    """
    print 'crawling forum', forum_id
    forums.append((forum_id, folder))

    url = '{}/api/forum/forums/{}'
    url = url.format(course.get_url(), forum_id)

    path = folder + '/info.json'
    util.download(url, path, course.get_cookie_file())

    info = util.read_json(path)
    util.write_json(path, info)

    for forum in info['subforums']:
        sub_folder = '{}/{}'.format(folder, forum['id'])
        download_forum(forums, forum['id'], sub_folder, course)


def download_pages(forum_id, folder, course, page=1):
    """
    Download all threads in current forum.
    :param forum_id:
    :param folder:
    :param course:
    :param page:
    :return:
    """
    # download 1st page
    _url = '{}/api/forum/forums/{}/threads?sort=firstposted&page={}&page_size=100'
    url = _url.format(course.get_url(), forum_id, page)

    _path = folder + '/page/{}.json'
    path = _path.format(page)

    util.download(url, path, course.get_cookie_file())

    info = util.read_json(path)
    util.write_json(path, info)

    # download rest pages
    max_page = info['max_pages']
    while page < max_page:
        page += 1
        print 'forum page {}/{}'.format(page, max_page)

        url = _url.format(course.get_url(), forum_id, page)
        path = _path.format(page)

        util.download(url, path, course.get_cookie_file())
        util.write_json(path, util.read_json(path))
