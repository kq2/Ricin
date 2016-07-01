from downloader import util

ASSIGNMENT = u'''<?xml version="1.0" encoding="UTF-8"?>
<assignmentGroups>
  <assignmentGroup identifier="quizzes">
    <title>Quizzes</title>
    <position>1</position>
    <group_weight>50.0</group_weight>
  </assignmentGroup>
  <assignmentGroup identifier="projects">
    <title>Mini-projects</title>
    <position>2</position>
    <group_weight>50.0</group_weight>
  </assignmentGroup>
</assignmentGroups>'''


def convert(course, item):
    return ''


def make_groups(course):
    path = course.get_canvas_folder() + '/course_settings/assignment_groups.xml'
    util.write_file(path, ASSIGNMENT)
