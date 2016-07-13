"""
Convert Coursera announcement.
"""

import wiki
import resource
from downloader import util

TOPIC = u'''<?xml version="1.0" encoding="UTF-8"?>
<topic>
  <title>{title}</title>
  <text texttype="text/html"><![CDATA[{content}]]></text>
</topic>'''

META = u'''<?xml version="1.0" encoding="UTF-8"?>
<topicMeta>
  <topic_id>{topic_id}</topic_id>
  <title>{title}</title>
  <posted_at>2016-07-13T03:10:53</posted_at>
  <position>{position}</position>
  <type>announcement</type>
  <discussion_type>side_comment</discussion_type>
  <has_group_category>false</has_group_category>
  <workflow_state>active</workflow_state>
  <module_locked>false</module_locked>
  <allow_rating>false</allow_rating>
  <only_graders_can_rate>false</only_graders_can_rate>
  <sort_by_rating>false</sort_by_rating>
</topicMeta>'''


def convert(course, item):
    canvas_folder = course.get_canvas_folder()

    data_canvas_id = item['canvas_id']
    meta_canvas_id = data_canvas_id + '_meta'

    data_file = '{}.xml'.format(data_canvas_id)
    meta_file = '{}.xml'.format(meta_canvas_id)

    data_path = '{}/{}'.format(canvas_folder, data_file)
    meta_path = '{}/{}'.format(canvas_folder, meta_file)

    pos = course.get_topic_pos()
    course.set_topic_pos(pos + 1)

    args = {
        'topic_id': item['canvas_id'],
        'title': item['title'],
        'position': pos,
        'content': wiki.convert_content(item['message'], course)
    }

    meta = META.format(**args)
    data = TOPIC.format(**args)

    util.write_file(data_path, data)
    util.write_file(meta_path, meta)

    data_args = {
        'id': data_canvas_id,
        'type': 'imsdt_xmlv1p1',
        'path': '',
        'files': resource.FILE.format(data_file) + resource.DEPENDENCY.format(meta_canvas_id)
    }
    meta_args = {
        'id': meta_canvas_id,
        'type': 'associatedcontent/imscc_xmlv1p1/learning-application-resource',
        'path': meta_file,
        'files': resource.FILE.format(meta_file)
    }
    course.add_resources(data_args)
    course.add_resources(meta_args)
