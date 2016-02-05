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

    convert_meta(quiz_id, quiz_type, metadata, preamble, canvas_meta_file)
    convert_data(quiz_id, metadata, question_groups, canvas_data_file)


def convert_meta(quiz_id, quiz_type, metadata, preamble, canvas_meta_file):
    data = {
        'quiz_id': quiz_id,
        'quiz_type': quiz_type,
        'title': metadata.find('title').text,
        'points': metadata.find('maximum_score').text,
        'attempts': metadata.find('maximum_submissions').text,
        'preamble': preamble.text if preamble.text else '',
        'shuffle': 'false' if quiz_type == 'survey' else 'true',
        'show_answer': 'false' if quiz_type == 'survey' else 'true'
    }
    util.write_file(canvas_meta_file, template.QUIZ_META.format(**data))


def convert_data(quiz_id, metadata, question_groups, canvas_data_file):
    data = {
        'quiz_id': quiz_id,
        'title': metadata.find('title').text,
        'question_groups': convert_question_groups(quiz_id, question_groups)
    }
    util.write_file(canvas_data_file, template.QUIZ_DATA.format(**data))


def convert_question_groups(quiz_id, question_groups):
    canvas_question_groups = ''
    for idx, question_group in enumerate(question_groups):
        num = idx + 1
        group_id = '%s_%s' % (quiz_id, num)
        data = {
            'group_id': group_id,
            'group_title': 'Group %s' % num,
            'num_select': get_num_select(question_group),
            'questions': convert_questions(group_id, question_group, num)
        }
        canvas_question_groups += template.QUESTION_GROUP.format(**data)
    return canvas_question_groups


def get_num_select(question_group):
    num_select = question_group.get('select')
    if num_select == 'all':
        num_select = len(question_group)
    return num_select


def convert_questions(group_id, question_group, num):
    canvas_questions = ''
    for idx, question in enumerate(question_group.findall('question')):
        question_id = '%s_%s' % (group_id, idx+1)
        question_type = QUESTION_TYPE[question[0][0][1].text]
        option_groups = question[1].find('option_groups')
        general_feedback = question[1].findtext('explanation')
        options, feedback = convert_options(question_id, question_type,
                                            option_groups, general_feedback)
        data = {
            'question_id': question_id,
            'question_title': 'Question %s' % num,
            'question_points': question[0][0][0].text,
            'question_type': question_type,
            'question_text': question[1].findtext('text'),
            'options': options,
            'feedback': feedback
        }
        canvas_questions += template.QUESTION.format(**data)
    return canvas_questions


def convert_options(question_id, question_type, option_groups, general_feedback):
    options = ''
    feedback = ''
    for idx, option in enumerate(option_groups.iter('option')):
        option_id = '%s_%s' % (question_id, idx+1)
        option_text = option.findtext('text')
        option_feedback = option.findtext('explanation')
        option_correct = 1 if float(option.get('selected_score')) > 0 else 0
        if option_text:
            options += template.OPTION.format(option_id=option_id,
                                              option_text=option_text)
        if option_feedback:
            feedback += template.FEEDBACK.format(option_id=option_id,
                                                 option_feedback=option_feedback)
    if general_feedback:
        feedback += template.FEEDBACK.format(option_id='general',
                                             option_feedback=general_feedback)

    if question_type == 'numerical_question':
        options = template.OPTION_GROUP_TEXT.format(fibtype='fibtype="Decimal"')
    elif question_type == 'short_answer_question':
        options = template.OPTION_GROUP_TEXT.format(fibtype='')
    elif question_type == 'multiple_choice_question':
        options = template.OPTION_GROUP_CHOICE.format(single='Single', options=options)
    elif question_type == 'multiple_answers_question':
        options = template.OPTION_GROUP_CHOICE.format(single='Multiple', options=options)
    else:
        print "Unknown question type! "

    return options, feedback

