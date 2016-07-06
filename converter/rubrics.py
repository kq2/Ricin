"""
Convert a Coursera peer-assessment rubrics in Canvas format.
"""

from downloader import util

RUBRICS = u'''<?xml version="1.0" encoding="UTF-8"?>
<rubrics>{}
</rubrics>'''

RUBRIC = u'''
  <rubric identifier="{canvas_id}_rubric">
    <read_only>false</read_only>
    <title><![CDATA[{title}]]></title>
    <reusable>false</reusable>
    <public>false</public>
    <points_possible>{points}</points_possible>
    <hide_score_total>false</hide_score_total>
    <free_form_criterion_comments>false</free_form_criterion_comments>
    <criteria>{criteria}
    </criteria>
  </rubric>'''

CRITERION = u'''
      <criterion>
        <criterion_id>{criterion_id}</criterion_id>
        <points>{points}</points>
        <description><![CDATA[{description}]]></description>
        <ratings>{ratings}
        </ratings>
      </criterion>'''

RATING = u'''
          <rating>
            <description><![CDATA[{description}]]></description>
            <points>{points}</points>
            <criterion_id>{criterion_id}</criterion_id>
            <id>{rating_id}</id>
          </rating>'''


def make_rubrics(course, peer_items):

    coursera_folder = course.get_coursera_folder()
    canvas_folder = course.get_canvas_folder()

    rubrics = ''
    for item in peer_items:
        coursera_id = item['item_id']
        coursera_file = '{}/peer_assessment/{}.json'.format(coursera_folder, coursera_id)
        canvas_id = item['canvas_id']
        rubrics += make_rubric(coursera_file, canvas_id)

    canvas_file = '{}/course_settings/rubrics.xml'.format(canvas_folder)
    util.write_file(canvas_file, RUBRICS.format(rubrics))


def make_rubric(coursera_file, canvas_id):
    peer_assessment = util.read_json(coursera_file)
    args = {
        'canvas_id': canvas_id,
        'title': peer_assessment['title'],
        'points': peer_assessment['maxGrade'],
        'criteria': make_criteria(peer_assessment['form'][1])
    }
    return RUBRIC.format(**args)


def make_criteria(rubric):
    # footer = rubric['evaluation']['children'][0]
    # header = rubric['children'][0]
    items = rubric['children'][0]['evaluation']['children']
    ans = ''
    for item in items:
        ans += make_criterion(item)
    return ans


def make_criterion(criterion):
    criterion_id = criterion['id']
    op_type = criterion['children'][0]['type']
    options = criterion['children'][0]['parameters']['options']

    if op_type == 'gradingNumber':
        ratings, points = make_ratings(options, criterion_id)
        args = {
            'criterion_id': criterion_id,
            'points': points,
            'description': criterion['html'],
            'ratings': ratings
        }
        return CRITERION.format(**args)

    return ''


def make_ratings(options, criterion_id):
    ans = ''
    max_points = 0

    for option in options:
        rating, points = make_rating(option, criterion_id)
        ans += rating
        if points > max_points:
            max_points = points

    return ans, max_points


def make_rating(option, criterion_id):
    points = option['value']
    args = {
        'description': option['label'],
        'points': points,
        'criterion_id': criterion_id,
        'rating_id': option['id']
    }
    return RATING.format(**args), points
