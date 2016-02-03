"""
Convert a Coursera quiz into a Canvas quiz.
"""
from scraper import util
import template

QUESTION_TYPE = {
    'numeric': 'numerical_question',
    'text': 'short_answer_question',
    'regexp': 'short_answer_question',
    'match_expr': 'short_answer_question',
    'radio': 'multiple_choice_question',
    'select': 'multiple_choice_question',
    'checkbox': 'multiple_answers_question'
}


def convert(course_obj, course_item):
    item_id = course_item['item_id']
    quiz_id = 'quiz' + item_id
    coursera_folder = course_obj.get_coursera_folder() + '/quiz'
    canvas_folder = util.make_folder(course_obj.get_canvas_folder() + '/' + quiz_id)

    # This folder must exist for importing quizzes into Canvas.
    util.make_folder(course_obj.get_canvas_folder() + '/non_cc_assessments')

    coursera_file = coursera_folder + '/%s.xml' % item_id
    canvas_meta_file = canvas_folder + '/assessment_meta.xml'
    canvas_data_file = canvas_folder + '/%s.xml' % quiz_id

    quiz_type = 'assignment'
    if course_item['quiz_type'] == 'survey':
        quiz_type = 'survey'

    root = util.xml_root(coursera_file)
    metadata = root[0]
    preamble = root[1]
    question_groups = root[2][0]

    convert_metadata(quiz_id, quiz_type, metadata, preamble, canvas_meta_file)
    convert_question_groups(quiz_id, question_groups)


def convert_metadata(quiz_id, quiz_type, metadata, preamble, canvas_meta_file):
    data = {
        'canvas_id': quiz_id,
        'quiz_type': quiz_type,
        'title': metadata.find('title').text,
        'points': metadata.find('maximum_score').text,
        'attempts': metadata.find('maximum_submissions').text,
        'preamble': preamble.text if preamble.text else '',
        'shuffle': 'false' if quiz_type == 'survey' else 'true',
        'show_answer': 'false' if quiz_type == 'survey' else 'true'
    }
    util.write_file(canvas_meta_file, template.QUIZ_META.format(**data))


def get_num_select(question_group):
    num_select = question_group.get('select')
    if num_select == 'all':
        num_select = len(question_group)
    return num_select


def convert_question_groups(quiz_id, question_groups):
    for idx, question_group in enumerate(question_groups):
        num = idx + 1
        data = {
            'group_id': '%s_%s' % (quiz_id, num),
            'group_title': 'Group %s' % num,
            'num_select': get_num_select(question_group)
        }
        convert_questions(data['group_id'], question_group, num)


def convert_questions(group_id, question_group, num):
    for idx, question in enumerate(question_group.findall('question')):
        data = {
            'question_id': '%s_%s' % (group_id, idx+1),
            'question_title': 'Question %s' % num,
            'question_points': question[0][0][0].text,
            'question_type': QUESTION_TYPE[question[0][0][1].text],
            'question_text': question[1].findtext('text'),
            'question_feedback': question[1].findtext('explanation')
        }
        convert_options(data['question_id'], question[1][2])


def convert_options(question_id, option_groups):
    for idx, option in enumerate(option_groups.iter('option')):
        data = {
            'option_id': '%s_%s' % (question_id, idx+1),
            'option_text': option.findtext('text'),
            'option_feedback': option.findtext('explanation'),
            'correct': 1 if float(option.get('selected_score')) > 0 else 0
        }
        print data['option_id'], data['correct']

