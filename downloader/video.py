"""
Download Coursera video.
"""
import os
import re
import util


def download(course_obj, course_item):
    """
    Download quiz XML.
    :param course_obj: A Course object.
    :param course_item: {
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
    folder = util.make_folder(course_obj.get_folder() + 'video/')
    item_id = course_item['item_id']

    path = folder + item_id + '.json'
    util.write_json(path, course_item)

    content = util.read_file(path)
    util.write_file(path, content)

    video = course_item['source_video']
    if video:
        download_subtitles(course_obj, folder, item_id)
        # download_in_video_quizzes(course_obj, course_item, folder, item_id)
        # download_original_video(course_obj, folder, video)
        # download_published_compressed_video(course_obj, course_item,
        #                                     folder, item_id, video)


def download_in_video_quizzes(course_obj, course_item, folder, item_id):
    """
    Download in-video quizzes.
    """
    folder = util.make_folder(folder + 'in_video_quiz/')

    if course_item['__in_video_quiz_v2']:
        download_new_quizzes(course_obj, course_item, folder, item_id)
    else:
        download_old_quizzes(course_obj, course_item, folder, item_id)


def download_old_quizzes(course_obj, course_item, folder, item_id):
    """
    Download old version in-video quizzes.
    """
    quiz_url = '{}/admin/quiz/quiz_load?quiz_id={}'
    quiz_id = course_item['quiz']['parent_id']
    url = quiz_url.format(course_obj.get_url(), quiz_id)

    path = folder + item_id + '.json'
    util.download(url, path, course_obj.get_cookie_file())
    util.write_json(path, util.read_json(path))


def download_new_quizzes(course_obj, course_item, folder, item_id):
    """
    Download new version in-video quizzes.
    """
    # Step 1, download a HTML that has quiz ID.
    quiz_url = '{}/lecture/view?quiz_v2_admin=1&lecture_id={}'
    quiz_id = course_item['parent_id']
    url = quiz_url.format(course_obj.get_url(), quiz_id)

    path = folder + item_id + '.json'
    util.download(url, path, course_obj.get_cookie_file())

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
    util.download(url, path, course_obj.get_cookie_file())

    # Step 3, download each question.
    quiz = util.read_json(path)
    questions = quiz['assessment']['definition']['questions']
    for question_id, question in questions.items():
        url = '{}/questions/{}'.format(class_url, question_id)
        util.download(url, path, course_obj.get_cookie_file())
        question_json = util.read_json(path)

        # add question content to quiz
        question['metadata'] = question_json['metadata']
        question['data'] = question_json['question']

    # write the whole quiz to file
    util.write_json(path, quiz)


def make_folder(path):
    """
    Make a new folder based on path.
    """
    folder = path.rpartition('/')[0]
    return util.make_folder(folder)


def download_original_video(course_obj, folder, video):
    """
    Download original (high-quality) video.
    """
    src_url = 'https://spark-public.s3.amazonaws.com/{}/source_videos/{}'
    url = src_url.format(course_obj.get_name(), video)

    path = folder + 'original/' + video
    make_folder(path)

    util.download(url, path, course_obj.get_cookie_file())


def download_published_compressed_video(course_obj, course_item,
                                        folder, item_id, video):
    """
    Download published compressed video.
    """
    if course_item['__published'] is 1:
        src_url = '{}/lecture/download.mp4?lecture_id={}'
        url = src_url.format(course_obj.get_url(), item_id)

        path = folder + 'compressed/' + video
        make_folder(path)

        util.download(url, path, course_obj.get_cookie_file(),
                      follow_redirect=True)


def download_subtitles(course_obj, folder, item_id):
    """
    Download all subtitles of this video.
    """
    url = '{}/admin/api/lectures/{}/subtitles'
    url = url.format(course_obj.get_url(), item_id)

    folder = util.make_folder(folder + 'subtitle')
    path = '{}/info/{}.json'.format(folder, item_id)
    make_folder(path)

    util.download(url, path, course_obj.get_cookie_file())

    subtitles = util.read_json(path)
    util.write_json(path, subtitles)

    for subtitle in subtitles:
        url = subtitle['srt_url']
        if url:
            path = '{}/{}.{}.srt'.format(folder, item_id, subtitle['language'])
            util.download(url, path, course_obj.get_cookie_file())
