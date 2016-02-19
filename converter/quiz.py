"""
Convert a Coursera quiz into a Canvas quiz.
"""
from scraper import util
import template

# Coursera to Canvas question types
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
    quiz_type = 'survey' if course_item['quiz_type'] == 'survey' else 'assignment'

    coursera_folder = course_obj.get_coursera_folder() + '/quiz'
    canvas_folder = util.make_folder(course_obj.get_canvas_folder() + '/' + quiz_id)

    # This folder must exist for importing quizzes into Canvas.
    util.make_folder(course_obj.get_canvas_folder() + '/non_cc_assessments')

    coursera_file = coursera_folder + '/%s.xml' % item_id
    canvas_meta_file = canvas_folder + '/assessment_meta.xml'
    canvas_data_file = canvas_folder + '/%s.xml' % quiz_id

    root = util.xml_root(coursera_file)
    metadata = root.find('metadata')
    preamble = root.findtext('preamble')
    question_groups = root.find('data/question_groups')

    convert_meta(quiz_id, quiz_type, metadata, preamble, canvas_meta_file)
    convert_data(quiz_id, metadata, question_groups, canvas_data_file)


def convert_meta(quiz_id, quiz_type, metadata, preamble, canvas_meta_file):
    data = {
        'quiz_id': quiz_id,
        'quiz_type': quiz_type,
        'title': metadata.findtext('title'),
        'points': metadata.findtext('maximum_score'),
        'attempts': metadata.findtext('maximum_submissions'),
        'preamble': preamble,
        'shuffle': 'false' if quiz_type is 'survey' else 'true',
        'show_answer': 'false' if quiz_type is 'survey' else 'true'
    }
    util.write_file(canvas_meta_file, template.QUIZ_META.format(**data))


def convert_data(quiz_id, metadata, question_groups, canvas_data_file):
    data = {
        'quiz_id': quiz_id,
        'title': metadata.findtext('title'),
        'question_groups': convert_question_groups(quiz_id, question_groups)
    }
    util.write_file(canvas_data_file, template.QUIZ_DATA.format(**data))


def convert_question_groups(quiz_id, question_groups):
    canvas_question_groups = ''

    for idx, question_group in enumerate(question_groups):
        group_idx = idx + 1
        group_id = '%s_%s' % (quiz_id, group_idx)

        num_select = question_group.get('select')
        if num_select == 'all':
            num_select = len(question_group)

        data = {
            'group_id': group_id,
            'group_title': 'Group %s' % group_idx,
            'num_select': num_select,
            'questions': convert_questions(group_id, question_group, group_idx)
        }
        canvas_question_groups += template.QUESTION_GROUP.format(**data)

    return canvas_question_groups


def convert_questions(group_id, question_group, group_idx):
    canvas_questions = ''

    for idx, question in enumerate(question_group.findall('question')):
        data = {
            'question_id': '%s_%s' % (group_id, idx+1),
            'question_title': 'Question %s' % group_idx,
            'question_points': question.findtext('metadata/parameters/rescale_score'),
            'question_type': find_question_type(question),
            'question_text': question.findtext('data/text')
        }
        option_groups = question.find('data/option_groups')
        general_feedback = question.findtext('data/explanation')
        options, feedback = convert_options(option_groups,
                                            data['question_id'],
                                            data['question_type'],
                                            data['question_points'],
                                            general_feedback)
        data.update({'options': options, 'feedback': feedback})
        canvas_questions += template.QUESTION.format(**data)

    return canvas_questions


def find_question_type(question):
    question_type = question.find('metadata/parameters')[1].text
    return QUESTION_TYPE[question_type]


def convert_options(option_groups,
                    question_id,
                    question_type,
                    question_points,
                    general_feedback):
    options = ''
    processing_feedback = ''
    processing_answer = ''
    feedback = ''

    for idx, option in enumerate(option_groups.iter('option')):
        option_id = '%s_%s' % (question_id, idx+1)
        data = {
            'option_id': option_id,
            'option_text': option.findtext('text'),
            'option_feedback': option.findtext('explanation'),
            'option_selected_score': option.get('selected_score'),
            'option_unselected_score': option.get('unselected_score'),
            'condition': template.CONDITION_EQUAL.format(option_id)
        }

        options += template.OPTION.format(**data)
        processing_answer += convert_answer(question_type, question_points, data)
        if data['option_feedback']:
            processing_feedback += template.PROCESSING_FEEDBACK.format(**data)
            feedback += template.FEEDBACK.format(**data)

    options = wrap_options(question_type, options)
    if general_feedback:
        data = {
            'option_id': 'general',
            'option_feedback': general_feedback,
            'condition': template.CONDITION_OTHER
        }
        processing_feedback += template.PROCESSING_FEEDBACK.format(**data)
        feedback += template.FEEDBACK.format(**data)

    return options, processing_feedback + processing_answer + feedback


def convert_answer(question_type, question_points, data):
    option_points = data['option_selected_score']
    option_id = data['option_id']
    if question_type is 'multiple_choice_question':
        # if option is fully correct (it's possible that more than
        # one option are correct even it's single-answer type.)
        if question_points == option_points:
            return template.PROCESSING_ANSWER.format(
                condition=template.CONDITION_EQUAL.format(option_id)
            )
    return ''


def wrap_options(question_type, options):
    if question_type is 'numerical_question':
        return template.OPTIONS_NUMERICAL
    if question_type is 'short_answer_question':
        return template.OPTIONS_SHORT
    if question_type is 'multiple_choice_question':
        return template.OPTIONS_SINGLE.format(options=options)
    if question_type is 'multiple_answers_question':
        return template.OPTIONS_MULTIPLE.format(options=options)
