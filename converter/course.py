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

        self.topic_pos = 1
        self.quiz_pos = 1
        self.peer_pos = 1
        self.assignment_pos = 1
        self.module_pos = 1
        self.asset_pos = 1

    def clean_sections(self):
        sections = util.read_json(self.section_file)
        for section in sections:
            for item in section['items']:
                item_type = item['item_type']

                # unify format for wiki pages
                if item_type == 'coursepage':
                    item['title'] = item['metadata']['title']
                    item['item_id'] = item['metadata']['canonicalName']

                # set coursera_id
                item['coursera_id'] = '{}_{}'.format(item_type, item['item_id'])

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
                coursera_id = item['coursera_id']
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
            if item_type == 'coursepage':
                return 'wiki_' + canvas_id
            else:
                return '>_' + canvas_id
        else:
            return '{}_{}'.format(item['coursera_id'], self.part)

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

    def get_name(self):
        return self.name[:-1]

    def get_topic_pos(self):
        return self.topic_pos

    def set_topic_pos(self, pos):
        self.topic_pos = pos

    def get_quiz_pos(self):
        return self.quiz_pos

    def set_quiz_pos(self, pos):
        self.quiz_pos = pos

    def get_peer_pos(self):
        return self.peer_pos

    def set_peer_pos(self, pos):
        self.peer_pos = pos

    def get_assignment_pos(self):
        return self.assignment_pos

    def set_assignment_pos(self, pos):
        self.assignment_pos = pos

    def get_module_pos(self):
        return self.module_pos

    def set_module_pos(self, pos):
        self.module_pos = pos

    def get_asset_pos(self):
        return self.asset_pos

    def set_asset_pos(self, pos):
        self.asset_pos = pos

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

    def convert_announcement(self):
        self.convert('announcement')

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
            items = [item for item in section['items']
                     if item['published'] and item['item_type'] != 'announcement']
            if items:
                section['items'] = items
                published_sections.append(section)

        module.convert(self, published_sections)
