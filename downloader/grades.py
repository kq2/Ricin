"""
Download student grades.
"""
import os
import re
import util


def download(course):
    """
    Download grade book.
    :param course: A Coursera course object.
    :return: None.
    """
    path = course.get_folder() + '/grades/temp.html'
    url = course.get_url() + '/admin/course_grade/export_grades'
    util.download(url, path, course.get_cookie_file())

    pattern = r'graded. <a href="(.*?)">'
    url = re.search(pattern, util.read_file(path), re.DOTALL).group(1)

    os.remove(path)
    path = course.get_folder() + '/grades/grades.csv'

    util.download(url, path, course.get_cookie_file())
