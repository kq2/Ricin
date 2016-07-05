"""
Resources module
"""

from downloader import util

MANIFEST = u'''<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="manifest">
  <metadata>
    <schema>IMS Common Cartridge</schema>
    <schemaversion>1.1.0</schemaversion>
  </metadata>
  <resources>
    <resource identifier="syllabus" type="associatedcontent/imscc_xmlv1p1/learning-application-resource" href="course_settings/syllabus.html" intendeduse="syllabus"/>
    <resource identifier="settings" type="associatedcontent/imscc_xmlv1p1/learning-application-resource" href="course_settings/canvas_export.txt"/>
      <file href="course_settings/assignment_groups.xml"/>
      <file href="course_settings/module_meta.xml"/>
      <file href="course_settings/rubrics.xml"/>
    </resource>{}
  </resources>
</manifest>'''

TEMPLATE = u'''
    <resource identifier="{id}" type="{type}" href="{path}">{files}
    </resource>'''

FILE = u'''
      <file href="{}"/>'''


def make_manifest(course, resources):
    path = course.get_canvas_folder() + '/imsmanifest.xml'
    util.write_file(path, MANIFEST.format(resources))
