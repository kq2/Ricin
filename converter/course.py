"""
Convert a local Coursera course into Canvas course.
"""
import wiki
import quiz
import peer
import video
import assignment
import announcement
import resource
import downloader.util

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
        self.manifest = self.canvas_folder + '/imsmanifest.xml'
        self.wiki_file_name = {}
        self.resources = ''
        self.count = {
            'quiz': 0,
            'lecture': 0,
            'coursepage': 0,
            'assignment': 0,
            'peergrading': 0,
            'announcement': 0
        }

    def get_coursera_folder(self):
        return self.coursera_folder

    def get_canvas_folder(self):
        return self.canvas_folder

    def convert(self, item_type=None):
        convert_queue = []
        for section in downloader.util.read_json(self.section_file):
            for item in section['items']:
                self.add_wiki_file_name(item)
                if item_type is None or item_type == item['item_type']:
                    convert_queue.append(item)

        total = len(convert_queue)
        for idx, item in enumerate(convert_queue):
            print "{}/{}".format(idx + 1, total)
            self.convert_item(item)

        self.pack()

    def add_wiki_file_name(self, item):
        if item['item_type'] == 'coursepage':
            coursera_title = item['metadata']['title']
            coursera_file_name = item['metadata']['canonicalName']
            canvas_file_name = wiki.get_canvas_wiki_filename(coursera_title)
            self.wiki_file_name[coursera_file_name] = canvas_file_name

    def get_wiki_file_name(self, coursera_name):
        return self.wiki_file_name[coursera_name]

    def convert_item(self, item):
        item_type = item['item_type']
        self.count[item_type] += 1
        item['id'] = '{}_{}'.format(item_type, self.count[item_type])
        self.resources += CONVERTER[item_type](self, item)

    def pack(self):
        resource.write_manifest(self.manifest, self.resources)
        downloader.util.make_zip(self.canvas_folder)

    def convert_wiki_pages(self):
        self.convert('coursepage')

    def convert_quizzes(self):
        self.convert('quiz')
