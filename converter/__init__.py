import course


def run(site, course_name, course_session, part):
    _course = course.Course(site, course_name, course_session, part)

    _course.convert_assets()
    _course.convert_wiki_pages()
    _course.convert_videos()
    _course.convert_quizzes()
    _course.convert_assignments()
    _course.convert_peer()
    _course.convert_rubrics()
    _course.convert_modules(30)

    _course.end_conversion()
    _course.pack()

# run('class.coursera.org', 'interactivepython1', '010', 1)
run('class.coursera.org', 'interactivepython2', '010', 2)
# run('class.coursera.org', 'principlescomputing1', '005', 1)
# run('class.coursera.org', 'principlescomputing2', '005', 2)
# run('class.coursera.org', 'algorithmicthink1', '004', 3)
# run('class.coursera.org', 'algorithmicthink2', '004', 4)
