"""
Convert peer-assess assignment
"""

import wiki
import resource
from downloader import util

DESCRIPTION = u'''<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>{title}</title>
</head>

<body>
<p><strong>Instructions: </strong>Read/review the items below and implement the week's programming assignment.
When you have finished your implementation, copy and paste the CodeSkulptor URL for your cloud-saved program into
the URL submission field. Note that you may re-submit as many times as you wish before the deadline so feel free
to submit a partially working version early. Late submissions are not accepted. <strong>IMPORTANT</strong>:
Please use the "View the Original Page" link that appears in the upper right of the submission page to verify
that you submitted a working CodeSkulptor URL for the final version of your program.</p>

<ul>
    <li><a href="$WIKI_REFERENCE$/pages/" target="_blank">Mini-project Video</a></li>
    <li><a href="$WIKI_REFERENCE$/pages/{description}" target="_blank">Mini-project Description</a></li>
    <li><a href="$WIKI_REFERENCE$/pages/" target="_blank">Code Clinic Tips</a></li>
</ul>

<p><strong>Peer review: </strong> After you have submitted your program, Canvas will assign you five of your
peers' programs to grade after the assignment deadline. In return, five of your peers will grade your program.
Since you've worked hard on your program and would like your peers to do a good job of assessing your program,
please take your time and do a good job of assessing your peers' program in return.</p>

<p>For each item in the rubric, run your peers' program (in Chrome, Firefox or Safari) and observe its behavior.
If the program demonstrates the correct associated functionality, give it full credit for that item. If the
program demonstrates partial, inconsistent, or incorrect functionality, assign the program partial credit
based on your testing and our comments. <strong>When assigning partial or no credit, please add a short written
comment that describes the issues you observed.</strong> While this takes extra effort, please remember how
frustrating it would be to receive partial or no credit on part of your mini-project with no accompanying
explanation.</p>
</body>
</html>'''

SETTINGS = u'''<?xml version="1.0" encoding="UTF-8"?>
<assignment identifier="{canvas_id}">
  <title><![CDATA[{title}]]></title>
  <due_at/>
  <lock_at/>
  <unlock_at/>
  <module_locked>false</module_locked>
  <all_day_date/>
  <peer_reviews_due_at/>
  <assignment_group_identifierref>projects</assignment_group_identifierref>
  <workflow_state>unpublished</workflow_state>
  <rubric_identifierref>{rubric_id}</rubric_identifierref>
  <rubric_use_for_grading>true</rubric_use_for_grading>
  <rubric_hide_score_total>false</rubric_hide_score_total>
  <has_group_category>false</has_group_category>
  <points_possible>{points}</points_possible>
  <grading_type>points</grading_type>
  <all_day>true</all_day>
  <submission_types>{submit_type}</submission_types>
  <position>{position}</position>
  <peer_review_count>{num_peer}</peer_review_count>
  <peer_reviews>true</peer_reviews>
  <automatic_peer_reviews>true</automatic_peer_reviews>
  <moderated_grading>false</moderated_grading>
  <anonymous_peer_reviews>true</anonymous_peer_reviews>
  <grade_group_students_individually>false</grade_group_students_individually>
  <muted>false</muted>
</assignment>'''


def convert(course, item):
    coursera_id = item['item_id']
    coursera_folder = course.get_coursera_folder()
    coursera_file = '{}/peer_assessment/{}.json'.format(coursera_folder, coursera_id)

    canvas_id = item['canvas_id']
    canvas_folder = course.get_canvas_folder()

    title = item['title']
    assignment = util.read_json(coursera_file)

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
    make_description_page(course, assignment, canvas_id, title, file_name)

    file_path = '{}/{}.html'.format(canvas_id, file_name)
    path = '{}/{}'.format(canvas_folder, file_path)

    args = {
        'title': title,
        'description': file_name
    }
    util.write_file(path, DESCRIPTION.format(**args))
    return file_path


def make_settings_file(assignment, canvas_folder, canvas_id, title):
    file_name = '{}/assignment_settings.xml'.format(canvas_id)
    path = '{}/{}'.format(canvas_folder, file_name)

    args = {
        'canvas_id': canvas_id,
        'title': title,
        'rubric_id': '',
        'points': assignment['maxGrade'],
        'submit_type': 'online_url',
        'position': canvas_id.rpartition('_')[2],
        'num_peer': 5
    }
    util.write_file(path, SETTINGS.format(**args))
    return file_name


def make_description_page(course, assignment, canvas_id, title, file_name):
    content = assignment['form'][0]['children'][0]['html']
    canvas_id = 'coursepage_{}'.format(canvas_id)
    canvas_path = 'wiki_content/{}.html'.format(file_name)
    canvas_file = course.get_canvas_folder() + '/' + canvas_path

    wiki.make_canvas_wiki(content, title, canvas_file, canvas_id, course)

    args = {
        'id': canvas_id,
        'type': 'webcontent',
        'path': canvas_path,
        'files': resource.FILE.format(canvas_path)
    }
    course.add_resources(args)
