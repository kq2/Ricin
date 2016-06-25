"""
Convert Coursera lectures
"""
import re
import wiki
import resource
from downloader import util

EMBED = u'''
<p>
  <iframe src="https://mediacosmos.rice.edu/app/plugin/embed.aspx?ID={}&amp;displayTitle=false"
    width="640" height="380"
    allowfullscreen="allowfullscreen"
    webkitallowfullscreen="webkitallowfullscreen"
    mozallowfullscreen="mozallowfullscreen">
  </iframe>
</p>
{}
'''
LINK = u'''
<p><a href="{0}">{0}</a></p>'''


def convert(course, item):
    if item['__published'] is 1:
        coursera_title = item['title']
        canvas_title = u'\u25B6 ' + coursera_title

        coursera_id = item['item_id']
        canvas_id = item['canvas_id']

        ensemble_id = course.get_ensemble_id(coursera_title)
        canvas_file_name = course.get_wiki_file_name(coursera_id)

        coursera_path = 'video/quizzes/{}.json'.format(coursera_id)
        canvas_path = 'wiki_content/{}.html'.format(canvas_file_name)

        coursera_file = course.get_coursera_folder() + '/' + coursera_path
        canvas_file = course.get_canvas_folder() + '/' + canvas_path

        make_canvas_video_page(course, coursera_file, canvas_file,
                               canvas_title, canvas_id, ensemble_id)

        args = {
            'id': canvas_id,
            'type': 'webcontent',
            'path': canvas_path,
            'files': resource.FILE.format(canvas_path)
        }
        return resource.TEMPLATE.format(**args)

    return ''


def make_canvas_video_page(course, coursera_file, canvas_file,
                           canvas_title, canvas_id, ensemble_id):
    content = EMBED.format(ensemble_id,
                           get_in_video_links(coursera_file, course))
    content = wiki.TEMPLATE.format(canvas_title, canvas_id, content)
    util.write_file(canvas_file, content)


def get_in_video_links(in_video_quiz_file, course):
    ans = ''
    quiz = util.read_json(in_video_quiz_file)
    for group in quiz['questionGroups']:
        for question in group['questions']:
            for link in find_links(question['text'], course):
                ans += LINK.format(link)
    if ans:
        return u'<h4>References</h4>' + ans

    return ''


def find_links(text, course):
    ans = []
    text = wiki.convert_content(text, course)
    for match in re.finditer(r'href="(.*?)"', text):
        ans.append(match.group(1))
    return ans


def ensemble_id_map():
    ans = {}
    videos = util.read_json('ensemble.json')['Data']
    for video in videos:
        title = util.unescape(video['Title'])
        ensemble_id = video['ID']
        ans[title] = ensemble_id
    return ans
