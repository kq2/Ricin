from downloader import util

ASSIGNMENT = u'''<?xml version="1.0" encoding="UTF-8"?>
<assignmentGroups>
  <assignmentGroup identifier="quizzes">
    <title>Quizzes</title>
    <position>1</position>
    <group_weight>50.0</group_weight>
  </assignmentGroup>
  <assignmentGroup identifier="assignments">
    <title>Assignments</title>
    <position>2</position>
    <group_weight>50.0</group_weight>
  </assignmentGroup>
</assignmentGroups>'''


def convert(course, item):
    print course, item


def write_groups(assignment_groups_file):
    util.write_file(assignment_groups_file, ASSIGNMENT)
