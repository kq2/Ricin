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
    def __init__(self, course_site, course_name, course_session, part):
        self.site = course_site
        self.name = course_name
        self.session = course_session
        self.part = part

        self.coursera_folder = '../../{}/{}/{}'.format(self.site, self.name, self.session)
        self.canvas_folder = '../../canvas/{}-{}'.format(self.name, self.session)

        self.section_file = (self.coursera_folder + '/session_info/section.json')
        self.sections = self.clean_sections()

        self.id2id = {}
        self.set_canvas_id()

        self.ensemble_title2id = util.read_json('videos.json')
        self.resources = ''

    def clean_sections(self):
        sections = util.read_json(self.section_file)
        for section in sections:
            for item in section['items']:

                # unify format for wiki pages
                if item['item_type'] is 'coursepage':
                    item['title'] = item['metadata']['title']
                    item['item_id'] = item['metadata']['canonicalName']

                # unify format for published attribute
                if 'published' in item:
                    item['published'] = item['published'] == 1
                elif '__published' in item:
                    item['published'] = item['__published'] == 1
                else:
                    item['published'] = True

        return sections

    def set_canvas_id(self):
        canvas_id_alias = {}
        for section in self.sections:
            for item in section['items']:
                coursera_id = item['item_id']
                if coursera_id not in self.id2id:
                    canvas_id = self.make_canvas_id(item, canvas_id_alias)
                    item['canvas_id'] = canvas_id
                    self.id2id[coursera_id] = canvas_id

    def make_canvas_id(self, item, canvas_id_alias):
        item_type = item['item_type']
        if item_type in ('coursepage', 'lecture'):
            title = item['title']
            canvas_id = wiki.get_canvas_wiki_filename(title)

            # handle duplicates (same title)
            if canvas_id in canvas_id_alias:
                repeat = canvas_id_alias[canvas_id] + 1
                canvas_id_alias[canvas_id] = repeat
                canvas_id += '_{}'.format(repeat)
                if repeat == 2:
                    item['title'] = '{} {}'.format(title, 2)
                elif repeat > 2:
                    item['title'] = '{} {}'.format(title[:-2], repeat)
            else:
                canvas_id_alias[canvas_id] = 1

            # return the real canvas_id
            if item_type is 'coursepage':
                return 'wiki_' + canvas_id
            else:
                return '>_' + canvas_id
        else:
            return '{}_{}_{}'.format(item_type, item['item_id'], self.part)

    def get_coursera_folder(self):
        return self.coursera_folder

    def get_canvas_folder(self):
        return self.canvas_folder

    def get_canvas_id(self, coursera_id):
        return self.id2id[coursera_id]

    def get_ensemble_id(self, video_title):
        return self.ensemble_title2id[video_title]

    def get_part(self):
        return self.part

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
                if item['item_type'] is 'peergrading' and item['published']:
                    peer_items.append(item)
        rubrics.make_rubrics(self, peer_items)

    def convert_modules(self, start_position=1):
        published_sections = []

        # find all published sections (with at least one published item)
        for section in self.sections:
            items = [item for item in section['items'] if item['published']]
            if items:
                section['items'] = items
                published_sections.append(section)

        module.convert(self, published_sections, start_position)
