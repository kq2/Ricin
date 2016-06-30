"""
Coursera course class.
"""

import re
import util

import quiz
import wiki
import peer
import video
import assignment
import announcement
import assets
import grades
import forum

DOWNLOADER = {
    'quiz': quiz.download,
    'coursepage': wiki.download,
    'assignment': assignment.download,
    'peergrading': peer.download,
    'announcement': announcement.download,
    'lecture': video.download,
    'subtitle': video.download_subtitles,
    'original': video.download_original_video,
    'compressed': video.download_compressed_video
}


class Course:
    def __init__(self, url, name='', session=''):
        site = re.search(r'\w+\.coursera\.org', url).group(0)

        if name and session:
            self.url = url
            self.name = name
            self.session = session
        else:
            pattern = r'\w+\.coursera\.org/(.*?)-([\d]{3})'
            find = re.search(pattern, url)
            self.url = 'https://' + find.group(0)
            self.name = find.group(1)  # algebra
            self.session = find.group(2)  # 002

        self.id = self.name + '-' + self.session
        self.folder = '../../{}/{}/{}'.format(site, self.name, self.session)
        self.info_folder = self.folder + '/session_info'
        self.section_file = self.info_folder + '/section.json'
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

    def get_info_folder(self):
        return self.info_folder

    def get_section_file(self):
        return self.section_file

    def get_cookie_file(self):
        return self.cookie_file

    def download_section_file(self):
        url = '{}/admin/api/sections?course_id={}&full=1&drafts=1'
        url = url.format(self.url, self.id)
        path = self.section_file
        util.download(url, path, self.cookie_file)
        util.write_json(path, util.read_json(path))

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

    def download_grades(self):
        grades.download(self)

    def download_forum(self):
        forum.download(self)

    def download_stats(self):
        url = self.url + '/data/stats'
        path = self.info_folder + '/stats.html'
        util.download(url, path, self.cookie_file)

        content = util.read_file(path)
        pattern = r'<h1.*?</table>'
        content = re.search(pattern, content, re.DOTALL).group(0)
        util.write_file(path, content)

    def download_personal_info(self):
        url = self.url + '/data/export/pii_download'
        path = self.info_folder + '/pii.csv'
        util.download(url, path, self.cookie_file)

    def download_email_blacklist(self):
        url = self.url + '/data/export/pii'
        path = self.info_folder + '/temp.html'
        util.download(url, path, self.cookie_file)

        content = util.read_file(path)
        pattern = r'href="(https://coursera-reports.*?)"'
        url = re.search(pattern, content).group(1)

        util.remove(path)
        path = self.info_folder + '/email_blacklist.csv'
        util.download(url, path, self.cookie_file)

    def download_peer_assessment(self):
        peer.download_assessment(self)

    def upload(self):
        util.upload(self.folder)

        assets_folder = self.folder.rpartition('/')[0] + '/assets'
        util.upload(assets_folder)
