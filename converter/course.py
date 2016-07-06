"""
Convert a local Coursera course into Canvas course.
"""
import wiki
import quiz
import peer
import video
import rubrics
import assignment
import announcement
import assets
import resource
import module
from downloader import util

CONVERTER = {
    'quiz': quiz.convert,
    'lecture': video.convert,
    'coursepage': wiki.convert,
    'assignment': assignment.convert,
    'peergrading': peer.convert,
    'announcement': announcement.convert
}


class Course:
    def __init__(self, course_site, course_name, course_session):
        self.site = course_site
        self.name = course_name
        self.session = course_session

        self.coursera_folder = '../../{}/{}/{}'.format(self.site, self.name, self.session)
        self.canvas_folder = '../../canvas/{}-{}'.format(self.name, self.session)

        self.section_file = (self.coursera_folder + '/session_info/section.json')
        self.sections = module.clean_sections(self.section_file)

        self.wiki_name_map = wiki.name_map(self.sections)
        self.ensemble_id_map = video.ensemble_id_map()
        self.resources = ''

    def get_coursera_folder(self):
        return self.coursera_folder

    def get_canvas_folder(self):
        return self.canvas_folder

    def get_wiki_file_name(self, coursera_name):
        return self.wiki_name_map[coursera_name]

    def get_ensemble_id(self, video_title):
        return self.ensemble_id_map[video_title]

    def convert(self, item_type=None):
        convert_queue = []
        for section in self.sections:
            for item in section['items']:
                if item_type is None or item_type == item['item_type']:
                    if item['published']:
                        convert_queue.append(item)

        total = len(convert_queue)
        for idx, item in enumerate(convert_queue):
            print "{}/{}".format(idx + 1, total), item['title']
            CONVERTER[item_type](self, item)

    def add_resources(self, args):
        self.resources += resource.TEMPLATE.format(**args)

    def end_conversion(self):
        resource.make_manifest(self, self.resources)
        assignment.make_groups(self)

    def pack(self):
        util.make_zip(self.canvas_folder)

    def convert_assets(self):
        assets.convert(self)

    def convert_wiki_pages(self):
        self.convert('coursepage')

    def convert_videos(self):
        self.convert('lecture')

    def convert_quizzes(self):
        self.convert('quiz')

    def convert_assignments(self):
        self.convert('assignment')

    def convert_peer(self):
        self.convert('peergrading')

    def convert_rubrics(self):
        peer_items = []
        for section in self.sections:
            for item in section['items']:
                if item['item_type'] == 'peergrading' and item['published']:
                    peer_items.append(item)
        rubrics.make_rubrics(self, peer_items)

    def convert_modules(self):
        published_sections = []

        # find all published sections (with at least one published item)
        for section in self.sections:
            items = [item for item in section['items'] if item['published']]
            if items:
                section['items'] = items
                published_sections.append(section)

        module.convert(self, published_sections)
