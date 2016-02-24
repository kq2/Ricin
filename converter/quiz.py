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
    canvas_folder = course_obj.get_canvas_folder()
    coursera_folder = course_obj.get_coursera_folder()

    item_id = course_item['item_id']
    canvas_quiz_id = 'quiz' + item_id
    coursera_quiz_xml = '{}/quiz/{}.xml'.format(coursera_folder, item_id)

    is_survey = course_item['quiz_type'] == 'survey'
    convert_quiz(coursera_quiz_xml, is_survey, canvas_quiz_id, canvas_folder)


def convert_quiz(coursera_quiz_xml, is_survey, canvas_quiz_id, canvas_folder):
    coursera_quiz = util.xml_root(coursera_quiz_xml)

    metadata = coursera_quiz.find('metadata')
    preamble = coursera_quiz.findtext('preamble')
    data = coursera_quiz.find('data')

    canvas_quiz_metadata = convert_quiz_metadata(
        metadata, preamble, is_survey, canvas_quiz_id)

    canvas_quiz_data = convert_quiz_data(
        data, metadata, canvas_quiz_id)

    # make a folder and save two converted XML files.
    quiz_folder = util.make_folder(canvas_folder + '/' + canvas_quiz_id)
    canvas_metadata_xml = quiz_folder + '/assessment_meta.xml'
    canvas_data_xml = quiz_folder + '/{}.xml'.format(canvas_quiz_id)
    util.write_file(canvas_metadata_xml, canvas_quiz_metadata)
    util.write_file(canvas_data_xml, canvas_quiz_data)


def convert_quiz_metadata(metadata, preamble, is_survey, canvas_quiz_id):
    args = {
        'title': metadata.findtext('title'),
        'points': metadata.findtext('maximum_score'),
        'attempts': metadata.findtext('maximum_submissions'),
        'preamble': preamble,
        'quiz_id': canvas_quiz_id,
        'quiz_type': 'survey' if is_survey else 'assignment',
        'shuffle': 'false' if is_survey else 'true',
        'show_answer': 'false' if is_survey else 'true'
    }
    return template.QUIZ_METADATA.format(**args)


def convert_quiz_data(data, metadata, canvas_quiz_id):
    question_groups = data.find('question_groups')
    args = {
        'quiz_id': canvas_quiz_id,
        'title': metadata.findtext('title'),
        'question_groups': convert_question_groups(question_groups, canvas_quiz_id)
    }
    return template.QUIZ_DATA.format(**args)


def convert_question_groups(question_groups, canvas_quiz_id):
    canvas_question_groups = ''
    for idx, question_group in enumerate(question_groups):
        canvas_question_groups += convert_question_group(
            question_group, canvas_quiz_id, idx+1)
    return canvas_question_groups


def convert_question_group(question_group, canvas_quiz_id, idx):
    questions = question_group.findall('question')
    group_id = '{}_{}'.format(canvas_quiz_id, idx)
    num_select = question_group.get('select')
    if num_select == 'all':
        num_select = len(question_group)

    args = {
        'group_id': group_id,
        'group_title': 'Group {}'.format(idx),
        'num_select': num_select,
        'questions': convert_questions(questions, group_id)
    }
    return template.QUESTION_GROUP.format(**args)


def convert_questions(questions, group_id):
    canvas_questions = ''
    for idx, question in enumerate(questions):
        canvas_questions += convert_question(question, group_id, idx+1)
    return canvas_questions


def convert_question(question, group_id, idx):
    # split_order = question.findtext('metadata/parameters/preserve_order')
    answer_split = question.findtext('metadata/parameters/split/limit')
    question_type = QUESTION_TYPE[question.find('metadata/parameters')[1].text]
    if answer_split:
        # Canvas does not support multiple-input answer, use short-answer
        # instead, so answer must match exact string in Canvas.
        question_type = 'short_answer_question'
    question_id = '{}_{}'.format(group_id, idx)

    args = {
        'question_id': question_id,
        'question_type': question_type,
        'question_title': 'Question ' + group_id[-1],
        'question_points': question.findtext('metadata/parameters/rescale_score'),
        'presentation': convert_presentation(question, question_type, question_id),
        'processing': convert_processing(question, question_type, question_id),
        'feedback': convert_feedback(question, question_id)
    }
    return template.QUESTION.format(**args)


def convert_presentation(question, question_type, question_id):
    options = question.find('data/option_groups')
    args = {
        'question_text': question.findtext('data/text'),
        'options_text': convert_options(options, question_type, question_id)
    }
    return template.PRESENTATION.format(**args)


def convert_options(options, question_type, question_id):
    canvas_options = ''
    for idx, option in enumerate(options.iter('option')):
        args = {
            'option_id': '{}_{}'.format(question_id, idx+1),
            'option_text': option.findtext('text')
        }
        canvas_options += template.OPTION.format(**args)

    if question_type is 'numerical_question':
        return template.OPTIONS_NUMERICAL
    if question_type is 'short_answer_question':
        return template.OPTIONS_SHORT
    if question_type is 'multiple_choice_question':
        return template.OPTIONS_SINGLE.format(options=canvas_options)
    if question_type is 'multiple_answers_question':
        return template.OPTIONS_MULTIPLE.format(options=canvas_options)


def convert_processing(question, question_type, question_id):
    return template.PROCESSING.format(
        feedback=processing_feedback(question, question_type, question_id),
        answer=processing_answer(question, question_type, question_id))


def processing_feedback(question, question_type, question_id):
    feedback = ''

    general_feedback = question.findtext('data/explanation')
    if general_feedback:
        feedback += template.PROCESSING_FEEDBACK.format(
            condition=template.CONDITION_OTHER,
            option_id='general')

    options = question.find('data/option_groups')
    for idx, option in enumerate(options.iter('option')):
        option_id = '{}_{}'.format(question_id, idx+1)
        option_feedback = option.findtext('explanation')
        if option_feedback and question_type in ('multiple_choice_question',
                                                 'multiple_answers_question'):
            # The other two types have processing_feedback in processing_answer,
            # because their equal condition is the answer text instead of option_id.
            feedback += template.PROCESSING_FEEDBACK.format(
                condition=template.CONDITION_EQUAL.format(option_id),
                option_id=option_id)

    return feedback


def processing_answer(question, question_type, question_id):
    answer = ''

    split_answer = []
    multi_condition = ''
    question_points = question.findtext('metadata/parameters/rescale_score')

    options = question.find('data/option_groups')
    for idx, option in enumerate(options.iter('option')):
        option_id = '{}_{}'.format(question_id, idx+1)
        option_text = option.findtext('text')
        option_points = option.get('selected_score')

        fully_correct = option_points == question_points
        correct = float(option_points) > 0

        if question_type is 'short_answer_question':
            if fully_correct:
                answer += template.PROCESSING_ANSWER_TEXT.format(
                    condition=template.CONDITION_EQUAL.format(option_text),
                    option_id=option_id)
            elif correct:
                split_answer.append(option_text)

        if question_type is 'numerical_question':
            if fully_correct:
                # '1' --> ['1']
                # '[1,3]' --> ['1', '3']
                option_answer = option_text.strip('[]\n').split(',')

                if len(option_answer) == 1:
                    condition = template.CONDITION_EXACT  # exact number answer
                else:
                    condition = template.CONDITION_RANGE  # range number answer

                answer += template.PROCESSING_ANSWER_TEXT.format(
                    condition=condition.format(*option_answer),
                    option_id=option_id)

        if question_type is 'multiple_choice_question':
            if fully_correct:
                answer += template.PROCESSING_ANSWER.format(
                    condition=template.CONDITION_EQUAL.format(option_id))

        if question_type is 'multiple_answers_question':
            if correct:
                multi_condition += template.CONDITION_MULTIPLE_CORRECT.format(option_id)
            else:
                multi_condition += template.CONDITION_MULTIPLE_INCORRECT.format(option_id)

    if multi_condition:
        answer += template.PROCESSING_ANSWER.format(
            condition=template.CONDITION_MULTIPLE.format(multi_condition))

    if split_answer:
        answer += template.PROCESSING_ANSWER.format(
            condition=template.CONDITION_EQUAL.format(' '.join(split_answer)))

    return answer


def convert_feedback(question, question_id):
    canvas_feedback = ''

    general_feedback = question.findtext('data/explanation')
    if general_feedback:
        canvas_feedback += template.FEEDBACK.format(
            option_id='general', option_feedback=general_feedback)

    options = question.find('data/option_groups')
    for idx, option in enumerate(options.iter('option')):
        option_feedback = option.findtext('explanation')
        if option_feedback:
            args = {
                'option_id': '{}_{}'.format(question_id, idx+1),
                'option_feedback': option_feedback
            }
            canvas_feedback += template.FEEDBACK.format(**args)

    return canvas_feedback
