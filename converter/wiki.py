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
    wiki_id = item['id']
    wiki_title = item['metadata']['title']

    coursera_path = 'wiki/{}.html'.format(item['metadata']['canonicalName'])
    canvas_path = 'wiki_content/{}.html'.format(get_canvas_wiki_filename(wiki_title))

    coursera_wiki_file = course.get_coursera_folder() + '/' + coursera_path
    canvas_wiki_file = course.get_canvas_folder() + '/' + canvas_path

    convert_wiki_file(coursera_wiki_file, canvas_wiki_file, wiki_title, wiki_id)

    args = {'id': wiki_id, 'type': 'webcontent', 'path': canvas_path}
    return resource.TEMPLATE.format(**args)


def convert_wiki_file(coursera_wiki_file, canvas_wiki_file, wiki_title, wiki_id):
    coursera_wiki_content = util.read_file(coursera_wiki_file)
    canvas_wiki_content = get_canvas_wiki_content(coursera_wiki_content)
    canvas_wiki = TEMPLATE.format(wiki_title, wiki_id, canvas_wiki_content)
    util.write_file(canvas_wiki_file, canvas_wiki)


def get_canvas_wiki_filename(coursera_wiki_title):
    ans = coursera_wiki_title.lower()
    ans = ans.replace('*', 'star')
    ans = '-'.join(re.findall(r'[\w\d]+', ans))
    return ans


def get_canvas_wiki_content(coursera_wiki_content):
    ans = replace_wiki_links(coursera_wiki_content)
    ans = replace_assets_links(ans)
    return ans


def replace_wiki_links(coursera_wiki_content):
    coursera_link = r'href="(\w+)"'
    canvas_link = r'href="$WIKI_REFERENCE$/pages/\1"'
    return re.sub(coursera_link, canvas_link, coursera_wiki_content)


def replace_assets_links(coursera_wiki_content):
    coursera_link = r'src="\.\./\.\./\.\./.*?/assets/(.*?)"'
    canvas_link = r'src="$IMS-CC-FILEBASE$/\1"'
    return re.sub(coursera_link, canvas_link, coursera_wiki_content)
