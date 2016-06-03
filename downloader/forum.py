"""
Download Coursera forum.
"""
import util


def download(course):
    """
    Download a course's forum.
    """
    forums_folder = course.get_folder() + '/forum/forums'
    threads_folder = course.get_folder() + '/forum/threads'

    forums = find_forums(course, forums_folder, 0)
    download_forums(course, forums)

    forum_threads_folder = forums_folder + '/threads'
    download_threads(course, forum_threads_folder, threads_folder)


def find_forums(course, forum_folder, forum_id):
    """
    Recursively find all sub-forums in current forum.
    Return a list of sub-forums and current forum.
    """
    forums = [(forum_folder, forum_id)]
    print 'crawling forum', forum_id

    url = '{}/api/forum/forums/{}'.format(course.get_url(), forum_id)
    path = forum_folder + '/info.json'
    util.download(url, path, course.get_cookie_file())

    forum = util.read_json(path)
    util.write_json(path, forum)

    for sub_forum in forum['subforums']:
        sub_folder = '{}/{}'.format(forum_folder, forum['id'])
        forums += find_forums(course, sub_folder, sub_forum['id'])

    return forums


def download_forums(course, forums):
    """
    Download every forum in forum list.
    """
    num_forum = len(forums)
    for idx, (forum_folder, forum_id) in enumerate(forums):
        print 'forum {}/{}'.format(idx + 1, num_forum)
        download_forum(course, forum_folder, forum_id)


def download_forum(course, forum_folder, forum_id, page=1):
    """
    Download all threads in current forum.
    Note: forum 0 has every thread!
    """
    # download 1st page
    query = 'sort=firstposted&page={}&page_size=100'.format(page)
    url = '{}/api/forum/forums/{}/threads?{}'.format(course.get_url(), forum_id, query)

    path = '{}/threads/{}.json'.format(forum_folder, page)
    util.download(url, path, course.get_cookie_file())

    threads = util.read_json(path)
    util.write_json(path, threads)

    # download rest pages
    max_page = threads['max_pages']
    if page < max_page:
        page += 1
        print 'forum page {}/{}'.format(page, max_page)
        download_forum(course, forum_folder, forum_id, page)


def download_threads(course, forum_threads_folder, threads_folder):
    """
    Download every thread (in forum 0).
    """
    thread_count = 0
    for page_file in util.get_files(forum_threads_folder):
        path = '{}/{}'.format(forum_threads_folder, page_file)
        page = util.read_json(path)

        num_thread = page['total_threads']
        for thread in page['threads']:
            thread_count += 1
            print 'thread {}/{}'.format(thread_count, num_thread)

            download_thread(course, threads_folder, thread['id'])


def download_thread(course, threads_folder, thread_id, page=1, post_id=None):
    """
    Download a thread.
    """
    # Download 1st page
    url = '{}/api/forum/threads/{}'.format(course.get_url(), thread_id)
    if post_id:
        url = '{}?post_id={}&position=after'.format(url, post_id)

    path = '{}/{}/{}.json'.format(threads_folder, thread_id, page)
    util.download(url, path, course.get_cookie_file())

    thread = util.read_json(path)
    util.write_json(path, thread)

    # Download rest pages
    page = thread['start_page']
    num_page = thread['num_pages']

    if page < num_page:
        page += 1
        print 'thread page {}/{}'.format(page, num_page)

        post_id = get_next_post_id(thread['posts'])
        if post_id:
            download_thread(course, threads_folder, thread_id, page, post_id)


def get_next_post_id(posts):
    """
    Return the first post's ID in next scroll.
    """
    post_id = 0
    for post in reversed(posts):
        if 'link' in post:
            return post_id
        post_id = post['id']
