"""
Download Coursera forum.
"""
import re
import util


def download(course):
    """
    Download a course's forum.
    """
    forums_folder = course.get_folder() + '/forum/forums'
    threads_folder = course.get_folder() + '/forum/threads'

    download_forums(course, forums_folder)
    download_threads(course, forums_folder, threads_folder)


def download_forums(course, folder):
    """
    Download info for forum and sub-forums.
    """
    forums = find_forums(course, folder)
    num_forum = len(forums)
    for idx, (forum_folder, forum_id) in enumerate(forums):
        print 'forum {}/{}'.format(idx + 1, num_forum)
        find_threads(course, forum_folder, forum_id)


def find_forums(course, forum_folder, forum_id=0):
    """
    Recursively find all sub-forums in current forum.
    Return a list of sub-forums and current forum.
    """
    print 'crawling forum', forum_id

    url = '{}/api/forum/forums/{}'.format(course.get_url(), forum_id)
    path = forum_folder + '/info.json'
    util.download(url, path, course.get_cookie_file())

    forum = util.read_json(path)
    util.write_json(path, forum)

    forums = [(forum_folder, forum_id)]
    for sub_forum in forum['subforums']:
        sub_folder = '{}/{}'.format(forum_folder, sub_forum['id'])

        # recursion
        forums += find_forums(course, sub_folder, sub_forum['id'])

    return forums


def find_threads(course, forum_folder, forum_id):
    """
    Find all threads in current forum.
    Note: forum 0 has every thread!
    """
    # download the 1st page of given forum
    query = 'sort=firstposted&page=1'
    url = '{}/api/forum/forums/{}/threads?{}'
    url = url.format(course.get_url(), forum_id, query)
    path = forum_folder + '/temp.json'
    util.download(url, path, course.get_cookie_file())

    # download a huge page with all threads
    forum = util.read_json(path)
    num_threads = forum['total_threads']
    url += '&page_size={}'.format(num_threads)
    util.download(url, path, course.get_cookie_file())

    # add each thread's id to forum info
    threads = util.read_json(path)['threads']
    util.remove(path)

    path = forum_folder + '/info.json'
    forum = util.read_json(path)

    forum_threads = []
    for thread in reversed(threads):
        forum_threads.append({'id': thread['id']})

    forum['num_threads'] = num_threads
    forum['threads'] = forum_threads

    util.write_json(path, forum)


def download_threads(course, forums_folder, threads_folder):
    """
    Download every thread (in forum 0).
    """
    forum = util.read_json(forums_folder + '/info.json')
    for idx, thread in enumerate(forum['threads']):
        print 'thread {}/{}'.format(idx + 1, forum['num_threads'])
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
    download_images(course, threads_folder, thread)

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


def download_images(course, threads_folder, thread):
    """
    Download images in given thread.
    The given thread object will be mutated.
    """
    posts = thread['posts']
    comments = thread['comments']

    thread_id = thread['id']
    thread_page = thread['start_page']

    images = []
    last_post_is_full = False
    for post in reversed(posts):
        if 'post_text' in post:
            text = post['post_text']
            text = find_images(text, images, thread_id, thread_page)
            post['post_text'] = text
            last_post_is_full = True
        elif last_post_is_full:
            break

    for comment in comments:
        text = comment['comment_text']
        text = find_images(text, images, thread_id, thread_page)
        comment['comment_text'] = text

    for url, path in images:
        path = '{}/{}'.format(threads_folder, path)
        util.download(url, path, course.get_cookie_file())


def find_images(text, images, thread_id, thread_page):
    """
    Append (image_url, image_path) to images.
    Return new text with URLs replaced.
    """
    pattern = r'"(https:\/\/coursera-forum-screenshots.*?)"'
    for url in re.findall(pattern, text, re.DOTALL):
        file_name = url.rpartition('/')[-1]
        num_image = len(images) + 1
        path = 'images/{}-{}-{}-{}'.format(thread_id, thread_page,
                                           num_image, file_name)
        images.append((url, path))
        text = text.replace(url, '../' + path)
    return text


def get_next_post_id(posts):
    """
    Return the first post's ID in next scroll.
    """
    post_id = 0
    for post in reversed(posts):
        if 'link' in post:
            return post_id
        post_id = post['id']
