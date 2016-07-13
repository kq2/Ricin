"""
Download Coursera wiki page.
"""

import re
import resource
from downloader import util

TEMPLATE = u'''<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>{}</title>
<meta name="identifier" content="{}"/>
<meta name="editing_roles" content="teachers"/>
<meta name="workflow_state" content="unpublished"/>
</head>
<body>
{}
</body>
</html>'''


def convert(course, item):
    title = item['title']
    coursera_id = item['item_id']
    canvas_id = item['canvas_id']

    coursera_path = 'wiki/{}.html'.format(coursera_id)
    canvas_path = 'wiki_content/{}.html'.format(canvas_id.replace('wiki_', '', 1))

    coursera_wiki_file = course.get_coursera_folder() + '/' + coursera_path
    canvas_wiki_file = course.get_canvas_folder() + '/' + canvas_path

    wiki_content = util.read_file(coursera_wiki_file)
    make_canvas_wiki(wiki_content, title, canvas_wiki_file, canvas_id, course)

    args = {
        'id': canvas_id,
        'type': 'webcontent',
        'path': canvas_path,
        'files': resource.FILE.format(canvas_path)
    }
    course.add_resources(args)


def make_canvas_wiki(wiki_content, wiki_title, canvas_file, canvas_id, course):
    wiki_content = convert_content(wiki_content, course)
    canvas_wiki = TEMPLATE.format(wiki_title, canvas_id, wiki_content)
    util.write_file(canvas_file, canvas_wiki)


# helper functions
def get_canvas_wiki_filename(coursera_wiki_title):
    ans = coursera_wiki_title.lower()
    ans = ans.replace('#', 'number')
    ans = ans.replace('*', 'star')
    ans = ans.replace('.', ' dot')
    ans = '-'.join(re.findall(r'[\w\d]+', ans))
    return ans


def convert_content(coursera_content, course):
    ans = remove_extra_spaces(coursera_content)
    ans = remove_bad_formats(ans)
    ans = remove_link_title(ans)
    ans = replace_assets_links(ans)
    ans = replace_quiz_links(ans, course)
    ans = replace_peer_links(ans, course)
    ans = replace_wiki_links(ans, course)
    ans = replace_video_links(ans, course)
    ans = replace_assignment_links(ans, course)
    return ans


def remove_extra_spaces(text):
    pattern = r'((href)|(title)|(target)|(src))[ \s]?=[ \s]?"'
    return re.sub(pattern, r'\1="', text)


def remove_link_title(coursera_content):
    return re.sub(r' title=".*?"', '', coursera_content)


def remove_bad_formats(coursera_content):
    return coursera_content.replace('quiz?quiz_type=homework', 'quiz')


def replace_assets_links(coursera_content):
    coursera_link = r'="\.\./\.\./\.\./.*?/assets/(.*?)"'
    canvas_link = r'="$IMS-CC-FILEBASE$/\1"'
    return re.sub(coursera_link, canvas_link, coursera_content)


def replace_wiki_links(coursera_content, course):
    coursera_link = r'href="(\.\./wiki/)?([\w\-\(\)]+)(#[\w-]+)?"'

    def _canvas_link(match):
        coursera_id = 'coursepage_' + match.group(2)
        canvas_id = course.get_canvas_id(coursera_id).replace('wiki_', '', 1)
        anchor = match.group(3)
        if anchor:
            canvas_id += anchor
        return 'href="$WIKI_REFERENCE$/pages/{}"'.format(canvas_id)

    return re.sub(coursera_link, _canvas_link, coursera_content)


def replace_video_links(coursera_content, course):
    coursera_link = r'href="\.\./lecture(/(\d+))?"'

    def _canvas_link(match):
        if match.group(2):
            coursera_id = 'lecture_' + match.group(2)
            canvas_id = course.get_canvas_id(coursera_id)
            return 'href="$WIKI_REFERENCE$/pages/{}"'.format(canvas_id)
        return 'href="$WIKI_REFERENCE$/pages/"'

    return re.sub(coursera_link, _canvas_link, coursera_content)


def replace_quiz_links(coursera_content, course):
    coursera_link = r'href="\.\./quiz(/\w+\?quiz_id=(\d+))?"'

    def _canvas_link(match):
        if match.group(2):
            coursera_id = 'quiz_' + match.group(2)
            canvas_id = course.get_canvas_id(coursera_id)
            return 'href="$CANVAS_OBJECT_REFERENCE$/quizzes/{}"'.format(canvas_id)
        return 'href="$CANVAS_COURSE_REFERENCE$/quizzes"'

    return re.sub(coursera_link, _canvas_link, coursera_content)


def replace_peer_links(coursera_content, course):
    coursera_link = r'href="\.\./human_grading(/view\?assessment_id=(\d+))?"'

    def _canvas_link(match):
        if match.group(2):
            coursera_id = 'peergrading_' + match.group(2)
            canvas_id = course.get_canvas_id(coursera_id)
            return 'href="$CANVAS_OBJECT_REFERENCE$/assignments/{}"'.format(canvas_id)
        return 'href="$CANVAS_COURSE_REFERENCE$/assignments"'

    return re.sub(coursera_link, _canvas_link, coursera_content)


def replace_assignment_links(coursera_content, course):
    coursera_link = r'href="\.\./assignment(/start\?assignment_id=(\d+))?"'

    def _canvas_link(match):
        if match.group(2):
            coursera_id = 'assignment_' + match.group(2)
            canvas_id = course.get_canvas_id(coursera_id)
            return 'href="$CANVAS_OBJECT_REFERENCE$/assignments/{}"'.format(canvas_id)
        return 'href="$CANVAS_COURSE_REFERENCE$/assignments"'

    return re.sub(coursera_link, _canvas_link, coursera_content)
