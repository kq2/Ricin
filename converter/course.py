"""
Convert a local Coursera course into Canvas course.
"""
from scraper import util


class Course:
    def __init__(self, path):
        self.path = path
        self.folder = util.make_folder('../%s-canvas/' % path)

    def get_path(self):
        return self.path

course = Course('interactivepython1-008')