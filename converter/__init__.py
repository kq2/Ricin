import course


def run(site, course_name, course_session):
    _course = course.Course(site, course_name, course_session)
    _course.convert_wiki_pages()

run('class.coursera.org', 'interactivepython', '005')
