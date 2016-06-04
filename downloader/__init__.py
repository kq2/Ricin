"""
Download a Coursera course.
"""
import course


CLASS_URL = 'https://class.coursera.org/'
IIPP = 'interactivepython'
POC = 'principlescomputing'
ALG = 'algorithmicthink'


def run(course_url):
    _course = course.Course(course_url)
    # _course.download_section_file()
    _course.download_forum()


run(CLASS_URL + IIPP + '-004')
