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
    coursera_title = item['title']
    canvas_id = item['canvas_id']

    coursera_file_name = item['item_id']
    canvas_file_name = course.get_wiki_file_name(coursera_file_name)

    coursera_path = 'wiki/{}.html'.format(coursera_file_name)
    canvas_path = 'wiki_content/{}.html'.format(canvas_file_name)

    coursera_wiki_file = course.get_coursera_folder() + '/' + coursera_path
    canvas_wiki_file = course.get_canvas_folder() + '/' + canvas_path

    wiki_content = util.read_file(coursera_wiki_file)
    make_canvas_wiki(wiki_content, coursera_title, canvas_wiki_file, canvas_id, course)

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
    ans = replace_video_links(ans, course)
    ans = replace_wiki_links(ans, course)
    ans = replace_assets_links(ans)
    ans = replace_quiz_links(ans)
    ans = remove_link_title(ans)
    return ans


def remove_extra_spaces(text):
    pattern = r'((href)|(title)|(target)|(src))[ \s]?=[ \s]?"'
    return re.sub(pattern, r'\1="', text)


def remove_link_title(coursera_content):
    return re.sub(r'title=".*?"', '', coursera_content)


def replace_wiki_links(coursera_content, course):
    coursera_link = r'href="(\.\./wiki/)?([\w\-\(\)]+)(#[\w-]+)?"'

    def canvas_link(match):
        page = course.get_wiki_file_name(match.group(2))
        pos = match.group(3)
        if pos:
            page += pos
        return 'href="$WIKI_REFERENCE$/pages/{}"'.format(page)

    return re.sub(coursera_link, canvas_link, coursera_content)


def replace_video_links(coursera_content, course):
    coursera_link = r'href="\.\./lecture/(\d+)"'
    canvas_link = 'href="$WIKI_REFERENCE$/pages/{}"'
    return re.sub(coursera_link,
                  lambda m: canvas_link.format(
                      course.get_wiki_file_name(m.group(1))),
                  coursera_content)


def replace_assets_links(coursera_content):
    coursera_link = r'="\.\./\.\./\.\./.*?/assets/(.*?)"'
    canvas_link = r'="$IMS-CC-FILEBASE$/\1"'
    return re.sub(coursera_link, canvas_link, coursera_content)


def replace_quiz_links(coursera_content):
    coursera_link = r'href="\.\./quiz/start\?quiz_id=(\d+)"'
    canvas_link = r'href="$CANVAS_OBJECT_REFERENCE$/quizzes/quiz_\1"'
    return re.sub(coursera_link, canvas_link, coursera_content)


def name_map(sections):
    ans = {}
    canvas_names = {}
    for section in sections:
        for item in section['items']:
            item_type = item['item_type']
            if item_type in ('coursepage', 'lecture'):
                coursera_name = item['item_id']

                # get an unique Canvas name
                canvas_name = get_canvas_wiki_filename(item['title'])
                if item_type is 'lecture':
                    canvas_name = '>-' + canvas_name
                if canvas_name in canvas_names:
                    canvas_names[canvas_name] += 1
                else:
                    canvas_names[canvas_name] = 1
                num = canvas_names[canvas_name]
                if num >= 2:
                    canvas_name = '{}-{}'.format(canvas_name, num)
                    canvas_title = '{} {}'.format(item['title'], num)
                    item['title'] = canvas_title

                ans[coursera_name] = canvas_name
    return ans
