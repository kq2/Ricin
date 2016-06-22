"""
Download Coursera wiki page.
"""

import re
import resource
import downloader.util

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
    coursera_title = item['metadata']['title']
    canvas_id = item['id']

    coursera_file_name = item['metadata']['canonicalName']
    canvas_file_name = course.get_wiki_file_name(coursera_file_name)

    coursera_path = 'wiki/{}.html'.format(coursera_file_name)
    canvas_path = 'wiki_content/{}.html'.format(canvas_file_name)

    coursera_wiki_file = course.get_coursera_folder() + '/' + coursera_path
    canvas_wiki_file = course.get_canvas_folder() + '/' + canvas_path

    convert_wiki_file(coursera_wiki_file, coursera_title,
                      canvas_wiki_file, canvas_id, course)

    args = {'id': canvas_id, 'type': 'webcontent', 'path': canvas_path}
    return resource.TEMPLATE.format(**args)


def convert_wiki_file(coursera_wiki_file, coursera_title,
                      canvas_wiki_file, canvas_id, course):
    coursera_wiki_content = downloader.util.read_file(coursera_wiki_file)
    canvas_wiki_content = convert_content(coursera_wiki_content, course)
    canvas_wiki = TEMPLATE.format(coursera_title, canvas_id, canvas_wiki_content)
    downloader.util.write_file(canvas_wiki_file, canvas_wiki)


def get_canvas_wiki_filename(coursera_wiki_title):
    ans = coursera_wiki_title.lower()
    ans = ans.replace('*', 'star')
    ans = '-'.join(re.findall(r'[\w\d]+', ans))
    return ans


def convert_content(coursera_content, course):
    ans = replace_wiki_links(coursera_content, course)
    ans = replace_assets_links(ans)
    return ans


def replace_wiki_links(coursera_content, course):
    coursera_link = r'href="(\w+)"'
    canvas_link = 'href="$WIKI_REFERENCE$/pages/{}"'
    return re.sub(coursera_link,
                  lambda m: canvas_link.format(course.get_wiki_file_name(m.group(1))),
                  coursera_content)


def replace_assets_links(coursera_content):
    coursera_link = r'src="\.\./\.\./\.\./.*?/assets/(.*?)"'
    canvas_link = r'src="$IMS-CC-FILEBASE$/\1"'
    return re.sub(coursera_link, canvas_link, coursera_content)
