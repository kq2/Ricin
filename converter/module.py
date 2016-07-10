"""
Convert sections.
"""

from downloader import util

MODULES = '''<?xml version="1.0" encoding="UTF-8"?>
<modules>{}
</modules>
'''
MODULE = '''
  <module identifier="module_{position}">
    <title><![CDATA[{title}]]></title>
    <workflow_state>unpublished</workflow_state>
    <position>{position}</position>
    <require_sequential_progress>false</require_sequential_progress>
    <items>{items}
    </items>
  </module>'''
ITEM = '''
      <item identifier="item_{canvas_id}">
        <content_type>{type}</content_type>
        <workflow_state>unpublished</workflow_state>
        <title><![CDATA[{title}]]></title>
        <identifierref>{canvas_id}</identifierref>
        <position>{position}</position>
        <new_tab>true</new_tab>
        <indent>0</indent>
      </item>'''
ITEM_TYPE = {
    'coursepage': 'WikiPage',
    'lecture': 'WikiPage',
    'quiz': 'Quizzes::Quiz',
    'peergrading': 'Assignment',
    'assignment': 'Assignment'
}


def convert(course, sections):
    modules = ''
    for section in sections:
        args = {
            'title': section['title'],
            'position': section['display_order'],
            'items': canvas_items(section['items'])
        }
        modules += MODULE.format(**args)

    path = course.get_canvas_folder() + '/course_settings/module_meta.xml'
    util.write_file(path, MODULES.format(modules))


def canvas_items(items):
    ans = ''
    for idx, item in enumerate(items):
        position = idx + 1
        ans += canvas_item(item, position)
    return ans


def canvas_item(item, position):
    item_type = item['item_type']
    if item_type in ITEM_TYPE:
        args = {
            'type': ITEM_TYPE[item_type],
            'title': item['title'],
            'canvas_id': item['canvas_id'],
            'position': position
        }
        return ITEM.format(**args)
    return ''


def clean_sections(section_file, part):
    sections = util.read_json(section_file)
    for section in sections:
        for item in section['items']:
            item_type = item['item_type']
            if item_type == 'coursepage':
                item['title'] = item['metadata']['title']
                item['item_id'] = item['metadata']['canonicalName']
                item['published'] = True
            elif '__published' in item:
                item['published'] = item['__published'] is 1
            elif 'published' in item:
                item['published'] = item['published'] is 1

            item['canvas_id'] = '{}_{}'.format(item_type, item['item_id'])
            if item_type != 'coursepage':
                item['canvas_id'] = '{}_{}'.format(part, item['canvas_id'])

    return sections
