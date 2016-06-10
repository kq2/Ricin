"""
Download Coursera video.
"""
import os
import re
import util


def download(course, item):
    """
    Download video info and quizzes.
    :param course: A Course object.
    :param item: {
        u'last_updated': 1406213737,
        u'uid': u'lecture3',
        u'maximum_submissions': 100,
        u'soft_close_time': None,
        u'__published': 1,
        u'__type': u'lecture',
        u'id': 4,
        u'open_time': 1409090400,
        u'title': u'CodeSkulptor (11:22)',
        u'quiz': {
            u'authentication_required': 1,
            u'last_updated': 1377442183,
            u'open_time': 1377442183,
            u'maximum_submissions': 0,
            u'soft_close_time': 1375330022,
            u'proctoring_requirement': u'none',
            u'title': u'CodeSkulptor (11:22)',
            u'deleted': 0,
            u'hard_close_time': 1376539622,
            u'__published': 1,
            u'parent_id': 65,
            u'__type': u'quiz',
            u'quiz_type': u'video',
            u'duration': 0,
            u'id': 66,
            u'uid': u'quiz66'},
        u'parent_id': 3,
        u'quiz_id': 66,
        u'final': 0,
        u'video_id_v2': None,
        u'deleted': 0,
        u'section_id': u'4',
        u'item_id': u'3',
        u'__in_video_quiz_v2': False,
        u'video_id': u'933b363eb7103f4f0148945596c61d40',
        u'hard_close_time': None,
        u'item_type': u'lecture',
        u'source_video': u'codeskulptor.mp4',
        u'video_length': None,
        u'order': u'1'
    }
    :return: None.
    """
    # path = '{}/video/info/{}.json'
    # path = path.format(course.get_folder(), item['item_id'])
    #
    # util.make_folder(path, True)
    # util.write_json(path, item)
    #
    if item['source_video']:
        _download_in_video_quizzes(course, item)


def _download_in_video_quizzes(course, item):
    """
    Download in-video quizzes.
    """
    if item['__in_video_quiz_v2']:
        _download_new_quizzes(course, item)
    else:
        _download_old_quizzes(course, item)


def _download_old_quizzes(course, item):
    """
    Download old version in-video quizzes.
    """
    url = '{}/admin/quiz/quiz_load?quiz_id={}'
    url = url.format(course.get_url(), item['quiz']['parent_id'])

    path = '{}/video/quizzes/{}.json'
    path = path.format(course.get_folder(), item['item_id'])

    util.download(url, path, course.get_cookie_file())
    util.write_json(path, util.read_json(path))


def _download_new_quizzes(course, item):
    """
    Download new version in-video quizzes.
    """
    # Step 1, download a HTML that has quiz ID.
    url = '{}/lecture/view?quiz_v2_admin=1&lecture_id={}'
    url = url.format(course.get_url(), item['parent_id'])

    path = '{}/video/quizzes/{}.json'
    path = path.format(course.get_folder(), item['item_id'])

    util.download(url, path, course.get_cookie_file())

    pattern = r'v2-classId="(.*?)".*?v2-id="(.*?)".*?v2-lecture-id="(.*?)"'
    find = re.search(pattern, util.read_file(path), re.DOTALL)
    class_id, v2_id, lecture_id = find.group(1, 2, 3)

    # if no quiz in this video, delete the file
    if not v2_id:
        os.remove(path)
        return

    # Step 2, download a JSON that has question ID.
    class_url = 'https://class.coursera.org/api/assess/v1/inVideo/class/' + class_id
    url = '{}/lecture/{}/{}'.format(class_url, lecture_id, v2_id)
    util.download(url, path, course.get_cookie_file())

    # Step 3, download each question.
    quiz = util.read_json(path)
    questions = quiz['assessment']['definition']['questions']
    for question_id, question in questions.items():
        url = '{}/questions/{}'.format(class_url, question_id)
        util.download(url, path, course.get_cookie_file())
        question_json = util.read_json(path)

        # add question content to quiz
        question['metadata'] = question_json['metadata']
        question['data'] = question_json['question']

    # write the whole quiz to file
    util.write_json(path, quiz)


def download_original_video(course, item):
    """
    Download original (high-quality) video.
    """
    if item['source_video']:
        url = 'https://spark-public.s3.amazonaws.com/{}/source_videos/{}'
        url = url.format(course.get_name(), item['source_video'])

        path = '{}/video/original/{}'
        path = path.format(course.get_folder(), item['source_video'])

        util.download(url, path, course.get_cookie_file(), resume=True)


def download_compressed_video(course, item):
    """
    Download compressed video.
    """
    if item['source_video']:
        url = '{}/lecture/view?lecture_id={}&preview=1'
        url = url.format(course.get_url(), item['item_id'])

        path = '{}/video/compressed/{}.txt'
        path = path.format(course.get_folder(), item['source_video'])

        util.download(url, path, course.get_cookie_file())

        pattern = r'type="video/mp4" src="(.*?)"'
        url = re.search(pattern, util.read_file(path), re.DOTALL).group(1)

        os.remove(path)
        path = '{}/video/compressed/{}'
        path = path.format(course.get_folder(), item['source_video'])

        util.download(url, path, course.get_cookie_file(), resume=True)


def download_subtitles(course, item):
    """
    Download all subtitles of this video.
    """
    url = '{}/admin/api/lectures/{}/subtitles'
    url = url.format(course.get_url(), item['item_id'])

    path = course.get_folder() + '/video/subtitles/temp.json'
    util.download(url, path, course.get_cookie_file())

    subtitles = util.read_json(path)
    os.remove(path)

    for subtitle in subtitles:
        url = subtitle['srt_url']
        if url:
            path = '{}/video/subtitles/{}.{}.srt'
            path = path.format(course.get_folder(), item['item_id'],
                               subtitle['language'])
            util.download(url, path, course.get_cookie_file())
