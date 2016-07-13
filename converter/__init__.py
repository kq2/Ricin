import course
import downloader


def convert(_course):
    if _course.get_part() == 1:
        _course.convert_assets()
    _course.convert_announcement()
    _course.convert_wiki_pages()
    _course.convert_videos()
    _course.convert_quizzes()
    _course.convert_assignments()
    _course.convert_peer()
    _course.convert_rubrics()
    _course.convert_modules()

    _course.end_conversion()
    # _course.pack()


def convert_all(courses):
    prev_course = None
    for _course in courses:
        if prev_course:
            _course.set_assignment_pos(prev_course.get_assignment_pos())
            _course.set_quiz_pos(prev_course.get_quiz_pos())
            _course.set_peer_pos(prev_course.get_peer_pos())
            _course.set_module_pos(prev_course.get_module_pos())
            _course.set_asset_pos(prev_course.get_asset_pos())
        convert(_course)
        prev_course = _course


def run():
    url = 'class.coursera.org'
    courses = [
        course.Course(url, downloader.IIPP + '1', '010', 1),
        # course.Course(url, downloader.IIPP + '2', '010', 2),
        # course.Course(url, downloader.POC + '1', '005', 1),
        # course.Course(url, downloader.POC + '2', '005', 2),
        # course.Course(url, downloader.ALG + '1', '004', 1),
        # course.Course(url, downloader.ALG + '2', '004', 2)
    ]
    convert_all(courses)


run()
