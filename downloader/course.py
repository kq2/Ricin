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
import assets
import forum

DOWNLOADER = {
    'quiz': quiz.download,
    'coursepage': wiki.download,
    'assignment': assignment.download,
    'peergrading': peergrading.download,
    'announcement': announcement.download,
    'lecture': video.download,
    'subtitle': video.download_subtitles,
    'original': video.download_original_video,
    'compressed': video.download_compressed_video,
}


class Course:
    def __init__(self, url):
        pattern = r'\w+\.coursera\.org/(.*?)-([0-9]{3})'
        find = re.search(pattern, url)

        self.url = 'https://' + find.group(0)
        self.name = find.group(1)  # algebra
        self.session = find.group(2)  # 002
        self.id = self.name + '-' + self.session

        self.folder = util.make_folder('../' + self.id)
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
        url = '{}/admin/api/sections?COURSE_ID={}&full=1&drafts=1'
        url = url.format(self.url, self.id)
        util.download(url, self.section_file, self.cookie_file)

    def download(self, item_type=None):
        type_filter = item_type
        if item_type in ('subtitle', 'original', 'compressed'):
            type_filter = 'lecture'

        download_queue = []
        for section in util.read_json(self.section_file):
            for item in section['items']:
                if type_filter is None or type_filter == item['item_type']:
                    download_queue.append(item)

        num_download = len(download_queue)
        for idx, item in enumerate(download_queue):
            print "%d/%d" % (idx + 1, num_download)
            if type_filter is None:
                item_type = item['item_type']
            DOWNLOADER[item_type](self, item)

    def download_quizzes(self):
        self.download('quiz')

    def download_videos_info(self):
        self.download('lecture')

    def download_subtitles(self):
        self.download('subtitle')

    def download_original_videos(self):
        self.download('original')

    def download_compressed_video(self):
        self.download('compressed')

    def download_wiki_pages(self):
        self.download('coursepage')

    def download_assignments(self):
        self.download('assignment')

    def download_peergradings(self):
        self.download('peergrading')

    def download_announcements(self):
        self.download('announcement')

    def download_assets(self):
        assets.download(self)

    def download_forum(self):
        forum.download(self, '1942')
