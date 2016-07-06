"""
Convert a Coursera assignment
"""
import wiki
import resource
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
    coursera_id = item['item_id']
    coursera_folder = course.get_coursera_folder()
    coursera_file = '{}/assignment/{}.html'.format(coursera_folder, coursera_id)

    canvas_id = item['canvas_id']
    canvas_folder = course.get_canvas_folder()

    title = item['title']
    assignment = util.read_file(coursera_file)

    main_file = make_main_file(course, assignment, canvas_folder, canvas_id, title)
    settings_file = make_settings_file(assignment, canvas_folder, canvas_id, title)

    args = {
        'id': canvas_id,
        'type': 'associatedcontent/imscc_xmlv1p1/learning-application-resource',
        'path': main_file,
        'files': resource.FILE.format(main_file) + resource.FILE.format(settings_file)
    }
    course.add_resources(args)


def make_main_file(course, assignment, canvas_folder, canvas_id, title):
    file_name = wiki.get_canvas_wiki_filename(title)
    file_path = '{}/{}.html'.format(canvas_id, file_name)
    path = '{}/{}'.format(canvas_folder, file_path)
    return ''


def make_settings_file(assignment, canvas_folder, canvas_id, title):
    return ''


def make_groups(course):
    path = course.get_canvas_folder() + '/course_settings/assignment_groups.xml'
    util.write_file(path, ASSIGNMENT)
