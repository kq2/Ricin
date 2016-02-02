"""
Convert a local Coursera course into Canvas course.
"""
from scraper import util


class Course:
    def __init__(self, coursera_folder):
        self.coursera_folder = coursera_folder
        self.canvas_folder = util.make_folder('../%s-canvas/' % coursera_folder)

    def get_coursera_folder(self):
        return self.coursera_folder

    def get_canvas_folder(self):
        return self.canvas_folder

    def convert_quizzes(self):
        pass

course = Course('interactivepython1-008')
