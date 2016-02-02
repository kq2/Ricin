"""
Convert a local Coursera course into Canvas course.
"""
from scraper import util
import quiz
import wiki
import video
import assignment
import peergrading
import announcement

COURSE_ITEM = {
    'quiz': quiz,
    'lecture': video,
    'coursepage': wiki,
    'assignment': assignment,
    'peergrading': peergrading,
    'announcement': announcement
}


class Course:
    def __init__(self, course_id):
        self.id = course_id
        self.coursera_folder = '../' + self.id
        self.section_file = self.coursera_folder + '/section.json'
        self.canvas_folder = util.make_folder(self.coursera_folder + '-canvas')

    def get_coursera_folder(self):
        return self.coursera_folder

    def get_canvas_folder(self):
        return self.canvas_folder

    def convert(self, course_item_type=None):
        course_sections = util.read_json(self.section_file)
        for course_section in course_sections:
            for course_item in course_section['items']:
                if course_item_type is None or course_item_type == course_item['item_type']:
                    COURSE_ITEM[course_item['item_type']].convert(self, course_item)

    def convert_quizzes(self):
        self.convert('quiz')

course = Course('interactivepython1-008')
course.convert_quizzes()
