"""
Coursera course class.
"""

import re
import util

import quiz
import wiki
import video
import assignment
import peergrading
import announcement
import forum

COURSE_ITEM = {
    'quiz': quiz,
    'lecture': video,
    'coursepage': wiki,
    'assignment': assignment,
    'peergrading': peergrading,
    'announcement': announcement
}
CLASS_URL = 'https://class.coursera.org/'
IIPP = 'interactivepython'
POC = 'principlescomputing'
ALG = 'algorithmicthink'


class Course:
    def __init__(self, url):
        pattern = r'\w+\.coursera\.org/(.*?)-([0-9]{3})'
        find = re.search(pattern, url)

        self.url = 'https://' + find.group(0)
        self.name = find.group(1)  # thinkpython
        self.session = find.group(2)  # 002
        self.id = self.name + '-' + self.session

        self.folder = util.make_folder('../' + self.id + '/')
        self.section_file = self.folder + 'section.json'
        self.cookie_file = 'cookie.txt'

    def get_url(self):
        return self.url

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_session(self):
        return self.session

    def get_folder(self):
        return self.folder

    def get_section_file(self):
        return self.section_file

    def get_cookie_file(self):
        return self.cookie_file

    def download_section_file(self):
        url = self.url + '/admin/api/sections?COURSE_ID=' + self.id + '&full=1&drafts=1'
        util.download(url, self.section_file, self.cookie_file)

    def download(self, course_item_type=None):
        download_queue = []

        course_sections = util.read_json(self.section_file)
        for course_section in course_sections:
            for course_item in course_section['items']:
                if course_item_type is None or course_item_type == course_item['item_type']:
                    download_queue.append(course_item)

        num_download = len(download_queue)
        for idx, course_item in enumerate(download_queue):
            print "%d/%d" % (idx+1, num_download),
            COURSE_ITEM[course_item['item_type']].download(self, course_item)

    def download_quizzes(self):
        self.download('quiz')

    def download_videos(self):
        self.download('lecture')

    def download_wiki_pages(self):
        self.download('coursepage')

    def download_assignments(self):
        self.download('assignment')

    def download_peergradings(self):
        self.download('peergrading')

    def download_announcements(self):
        self.download('announcement')

    def download_forum(self):
        forum.download(self, '1942')

course = Course(CLASS_URL + POC + '1-005')
# course.download_section_file()
course.download_videos()
