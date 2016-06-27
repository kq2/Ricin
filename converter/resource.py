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
    </resource>{}
  </resources>
</manifest>'''

TEMPLATE = u'''
    <resource identifier="{id}" type="{type}" href="{path}">{files}
    </resource>'''

FILE = u'''
      <file href="{}"/>'''

DEPENDENCY = u'''
      <dependency identifierref="{}"/>'''


def write_manifest(manifest_file, resources):
    util.write_file(manifest_file, MANIFEST.format(resources))
