"""
Download a Coursera course.
"""
import course


CLASS_URL = 'https://class.coursera.org/'
IIPP = 'interactivepython'
POC = 'principlescomputing'
ALG = 'algorithmicthink'

RICE_URL = 'https://rice.coursera.org/'
COMP160 = 'rice-interactivepython'
COMP140 = 'thinkpython'


def run(course_url):
    _course = course.Course(course_url)
    _course.download_section_file()
    # _course.download()
    # _course.download_assets()
    # _course.download_grades()
    # _course.download_stats()
    # _course.download_subtitles()
    # _course.download_forum()
    # _course.download_compressed_video()
    _course.download_personal_info()


run(CLASS_URL + IIPP + '1-005')
# run(RICE_URL + COMP140 + '-002')
