"""
Convert a Coursera assignment
"""
import wiki
import peer
import resource
from downloader import util

ASSIGNMENT = u'''<?xml version="1.0" encoding="UTF-8"?>
<assignmentGroups>
  <assignmentGroup identifier="quiz">
    <title>Quiz</title>
    <position>1</position>
    <group_weight>20.0</group_weight>
  </assignmentGroup>
  <assignmentGroup identifier="peer">
    <title>Peer-review</title>
    <position>2</position>
    <group_weight>30.0</group_weight>
  </assignmentGroup>
  <assignmentGroup identifier="assignment">
    <title>Assignment</title>
    <position>2</position>
    <group_weight>50.0</group_weight>
  </assignmentGroup>
</assignmentGroups>'''

SETTINGS = u'''<?xml version="1.0" encoding="UTF-8"?>
<assignment identifier="{canvas_id}">
  <title><![CDATA[{title}]]></title>
  <due_at/>
  <lock_at/>
  <unlock_at/>
  <module_locked>false</module_locked>
  <all_day_date/>
  <peer_reviews_due_at/>
  <assignment_group_identifierref>assignment</assignment_group_identifierref>
  <workflow_state>unpublished</workflow_state>
  <rubric_identifierref/>
  <rubric_use_for_grading>false</rubric_use_for_grading>
  <rubric_hide_score_total>false</rubric_hide_score_total>
  <has_group_category>false</has_group_category>
  <points_possible>{points}</points_possible>
  <grading_type>points</grading_type>
  <all_day>true</all_day>
  <submission_types>{submit_type}</submission_types>
  <position>{position}</position>
  <peer_review_count>0</peer_review_count>
  <peer_reviews>false</peer_reviews>
  <automatic_peer_reviews>false</automatic_peer_reviews>
  <moderated_grading>false</moderated_grading>
  <anonymous_peer_reviews>false</anonymous_peer_reviews>
  <grade_group_students_individually>false</grade_group_students_individually>
  <muted>false</muted>
</assignment>'''


def convert(course, item):
    coursera_id = item['item_id']
    coursera_folder = course.get_coursera_folder()
    coursera_file = '{}/assignment/{}.html'.format(coursera_folder, coursera_id)

    canvas_id = item['canvas_id']
    canvas_folder = course.get_canvas_folder()

    title = item['title']
    assignment = util.read_file(coursera_file)
    assignment = wiki.convert_content(assignment, course)

    main_file = make_main_file(assignment, canvas_folder, canvas_id, title)
    settings_file = make_settings_file(course, canvas_folder, canvas_id, title)

    args = {
        'id': canvas_id,
        'type': 'associatedcontent/imscc_xmlv1p1/learning-application-resource',
        'path': main_file,
        'files': resource.FILE.format(main_file) + resource.FILE.format(settings_file)
    }
    course.add_resources(args)


def make_main_file(assignment, canvas_folder, canvas_id, title):
    file_name = wiki.get_canvas_wiki_filename(title)
    file_path = '{}/{}.html'.format(canvas_id, file_name)
    path = '{}/{}'.format(canvas_folder, file_path)
    args = {
        'title': title,
        'description': assignment
    }
    util.write_file(path, peer.ASSIGNMENT.format(**args))
    return file_path


def make_settings_file(course, canvas_folder, canvas_id, title):
    file_name = '{}/assignment_settings.xml'.format(canvas_id)
    path = '{}/{}'.format(canvas_folder, file_name)

    pos = course.get_assignment_pos()
    course.set_assignment_pos(pos + 1)

    args = {
        'canvas_id': canvas_id,
        'title': title,
        'points': 100,
        'submit_type': 'online_url',
        'position': pos,
    }
    util.write_file(path, SETTINGS.format(**args))
    return file_name


def make_groups(course):
    path = course.get_canvas_folder() + '/course_settings/assignment_groups.xml'
    util.write_file(path, ASSIGNMENT)
