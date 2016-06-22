"""
Resources module
"""

from downloader import util

MANIFEST = u'''<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="manifest" xmlns="http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1" xmlns:lomimscc="http://ltsc.ieee.org/xsd/imsccv1p1/LOM/manifest">
  <metadata>
    <schema>IMS Common Cartridge</schema>
    <schemaversion>1.1.0</schemaversion>
    <lomimscc:lom/>
  </metadata>
  <organizations>
    <organization identifier="org_1" structure="rooted-hierarchy">
      <item identifier="LearningModules"/>
    </organization>
  </organizations>
  <resources>
    <resource identifier="syllabus" type="associatedcontent/imscc_xmlv1p1/learning-application-resource" href="course_settings/syllabus.html" intendeduse="syllabus"/>
    <resource identifier="settings" type="associatedcontent/imscc_xmlv1p1/learning-application-resource" href="course_settings/canvas_export.txt"/>{}
  </resources>
</manifest>'''

TEMPLATE = u'''
    <resource identifier="{id}" type="{type}" href="{path}">
      <file href="{path}" />
    </resource>'''


def write_manifest(manifest_file, resources):
    util.write_file(manifest_file, MANIFEST.format(resources))
