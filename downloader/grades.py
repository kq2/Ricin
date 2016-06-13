"""
Download student grades.
"""
import re
import util


def download(course):
    """
    Download grade book.
    :param course: A Coursera course object.
    :return: None.
    """
    path = course.get_info_folder() + '/temp.html'
    url = course.get_url() + '/admin/course_grade/export_grades'
    util.download(url, path, course.get_cookie_file())

    pattern = r'graded. <a href="(.*?)">'
    find = re.search(pattern, util.read_file(path), re.DOTALL)
    util.remove(path)

    if find:
        url = find.group(1)
        path = course.get_info_folder() + '/grades.csv'
        util.download(url, path, course.get_cookie_file())
