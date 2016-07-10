import course


def run(site, course_name, course_session):
    _course = course.Course(site, course_name, course_session)

    _course.convert_assets()
    _course.convert_wiki_pages()
    _course.convert_videos()
    _course.convert_quizzes()
    _course.convert_assignments()
    _course.convert_peer()
    _course.convert_rubrics()
    _course.convert_modules()

    _course.end_conversion()
    # _course.pack()

run('class.coursera.org', 'principlescomputing1', '005')
# run('class.coursera.org', 'principlescomputing2', '005')
# course1 = course.Course('class.coursera.org', 'principlescomputing1', '005')
# course2 = course.Course('class.coursera.org', 'principlescomputing2', '005')
# for name in course2.wiki_name_map:
#     if name not in course1.wiki_name_map:
#         print name, course2.wiki_name_map[name]
