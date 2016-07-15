import filecmp
import course
import downloader


def convert(_course, include_assets):
    if include_assets:
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
        include_assets = True
        if prev_course:
            _course.set_assignment_pos(prev_course.get_assignment_pos())
            _course.set_quiz_pos(prev_course.get_quiz_pos())
            _course.set_peer_pos(prev_course.get_peer_pos())
            _course.set_module_pos(prev_course.get_module_pos())
            _course.set_asset_pos(prev_course.get_asset_pos())
            if _course.get_name() == prev_course.get_name():
                include_assets = False
        convert(_course, include_assets)
        prev_course = _course


def run():
    url = 'class.coursera.org'
    rice = 'rice.coursera.org'
    courses = [
        # course.Course(url, downloader.IIPP + '1', '010', 1),
        # course.Course(url, downloader.IIPP + '2', '010', 2),
        # course.Course(rice, downloader.COMP160, '005', 3),
        course.Course(url, downloader.POC + '1', '005', 1),
        course.Course(url, downloader.POC + '2', '005', 2),
        course.Course(url, downloader.ALG + '1', '004', 3),
        course.Course(url, downloader.ALG + '2', '004', 4)
    ]
    convert_all(courses)
    compare(courses[0], courses[1], 'web_resources', True)
    compare(courses[0], courses[1], 'wiki_content')
    compare(courses[2], courses[3], 'web_resources', True)
    compare(courses[2], courses[3], 'wiki_content')


def compare(prev_course, cur_course, folder, deep=False):
    dir1 = '{}/{}'.format(prev_course.get_canvas_folder(), folder)
    dir2 = '{}/{}'.format(cur_course.get_canvas_folder(), folder)
    if deep:
        filecmp.dircmp(dir1, dir2).report_full_closure()
    else:
        filecmp.dircmp(dir1, dir2).report()
    print "\n========================================\n"


run()
