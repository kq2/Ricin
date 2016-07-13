"""
Convert a Coursera quiz into a Canvas quiz.
"""
import wiki
import resource
from downloader import util

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

METADATA = u'''<?xml version="1.0" encoding="UTF-8"?>
<quiz identifier="{quiz_id}">
  <title><![CDATA[{title}]]></title>
  <description><![CDATA[{preamble}]]></description>
  <shuffle_answers>{shuffle}</shuffle_answers>
  <scoring_policy>keep_highest</scoring_policy>
  <quiz_type>{quiz_type}</quiz_type>
  <points_possible>{points}</points_possible>
  <lockdown_browser_monitor_data/>
  <show_correct_answers>{show_answer}</show_correct_answers>
  <anonymous_submissions>false</anonymous_submissions>
  <allowed_attempts>{attempts}</allowed_attempts>
  <one_question_at_a_time>false</one_question_at_a_time>
  <cant_go_back>false</cant_go_back>
  <available>false</available>
  <one_time_results>false</one_time_results>
  <show_correct_answers_last_attempt>true</show_correct_answers_last_attempt>
  <module_locked>false</module_locked>
  <assignment identifier="{assignment_id}">
    <title><![CDATA[{title}]]></title>
    <module_locked>false</module_locked>
    <assignment_group_identifierref>quiz</assignment_group_identifierref>
    <workflow_state>unpublished</workflow_state>
    <quiz_identifierref>{quiz_id}</quiz_identifierref>
    <has_group_category>false</has_group_category>
    <points_possible>{points}</points_possible>
    <grading_type>points</grading_type>
    <all_day>false</all_day>
    <submission_types>online_quiz</submission_types>
    <position>{position}</position>
    <peer_review_count>0</peer_review_count>
    <peer_reviews>false</peer_reviews>
    <automatic_peer_reviews>false</automatic_peer_reviews>
    <muted>false</muted>
  </assignment>
</quiz>'''
DATA = u'''<?xml version="1.0" encoding="UTF-8"?>
<questestinterop>
  <assessment ident="{quiz_id}" title="{title}">
    <section ident="root_section">{question_groups}
    </section>
  </assessment>
</questestinterop>'''
QUESTION_GROUP = u'''
      <section ident="{group_id}" title="Group {group_title}">
        <selection_ordering>
          <selection>
            <selection_number>{num_select}</selection_number>
            <selection_extension>
              <points_per_item>{points}</points_per_item>
            </selection_extension>
          </selection>
        </selection_ordering>{questions}
      </section>'''
QUESTION = u'''
        <item ident="{question_id}" title="Question {question_title}">
          <itemmetadata>
            <qtimetadata>
              <qtimetadatafield>
                <fieldlabel>question_type</fieldlabel>
                <fieldentry>{question_type}</fieldentry>
              </qtimetadatafield>
              <qtimetadatafield>
                <fieldlabel>points_possible</fieldlabel>
                <fieldentry>{question_points}</fieldentry>
              </qtimetadatafield>
            </qtimetadata>
          </itemmetadata>{presentation}{processing}{feedback}
        </item>'''
PRESENTATION = u'''
          <presentation>
            <material>
              <mattext texttype="text/html"><![CDATA[{question}]]></mattext>
            </material>{options}
          </presentation>'''
SINGLE_OPTION = u'''
            <response_str ident="response" rcardinality="Single">
              <render_fib {fib_type}>
                <response_label ident="answer"/>
              </render_fib>
            </response_str>'''
MULTIPLE_OPTIONS = u'''
            <response_lid ident="response" rcardinality="Multiple">
              <render_choice>{options}
              </render_choice>
            </response_lid>'''
OPTIONS = {
    'numerical_question': SINGLE_OPTION,
    'short_answer_question': SINGLE_OPTION,
    'multiple_choice_question': MULTIPLE_OPTIONS,
    'multiple_answers_question': MULTIPLE_OPTIONS
}
OPTION = u'''
                <response_label ident="{option_id}">
                  <material>
                    <mattext texttype="text/html"><![CDATA[{option_text}]]></mattext>
                  </material>
                </response_label>'''
PROCESSING = u'''
          <resprocessing>
            <outcomes>
              <decvar maxvalue="100" minvalue="0" varname="SCORE" vartype="Decimal"/>
            </outcomes>{}
          </resprocessing>'''
RESPONSE = u'''
            <respcondition continue="{continue}">
              <conditionvar>{condition}
              </conditionvar>{action}
            </respcondition>'''
CONDITION_OTHER = u'''
                <other/>'''
CONDITION_EQUAL = u'''
                <varequal respident="response"><![CDATA[{}]]></varequal>'''
CONDITION_RANGE = u'''
                <vargte respident="response">{0}</vargte>
                <varlte respident="response">{1}</varlte>'''
OR = u'''
                <or>{}
                </or>'''
AND = u'''
                <and>{}
                </and>'''
EQUAL = u'''
                  <varequal respident="response"><![CDATA[{}]]></varequal>'''
RANGE = u'''
                  <vargte respident="response">{0}</vargte>
                  <varlte respident="response">{1}</varlte>'''
NOT = u'''
                  <not>
                    <varequal respident="response">{}</varequal>
                  </not>'''
ACTION_SCORE = u'''
              <setvar action="Set" varname="SCORE">100</setvar>'''
ACTION_FEEDBACK = u'''
              <displayfeedback feedbacktype="Response" linkrefid="{}_fb"/>'''
FEEDBACK = u'''
          <itemfeedback ident="{option_id}_fb">
            <flow_mat>
              <material>
                <mattext texttype="text/html"><![CDATA[{option_feedback}]]></mattext>
              </material>
            </flow_mat>
          </itemfeedback>'''


def convert(course, item):
    """
    Create a Canvas quiz from a Coursera quiz.
    """
    coursera_id = item['item_id']
    coursera_folder = course.get_coursera_folder()
    coursera_file = '{}/quiz/{}.xml'.format(coursera_folder, coursera_id)

    canvas_folder = course.get_canvas_folder()
    canvas_id = item['canvas_id']
    is_survey = item['quiz_type'] == 'survey'

    make_canvas_quiz(coursera_file, is_survey, canvas_id, canvas_folder, course)


def make_canvas_quiz(coursera_file, is_survey, canvas_id, canvas_folder, course):
    """
    Create a Canvas quiz (2 XML files).
    """
    xml = util.read_file(coursera_file)
    xml = wiki.convert_content(xml, course)
    quiz = util.read_xml(xml, is_string=True)

    metadata = quiz.find('metadata')
    preamble = quiz.findtext('preamble')
    data = quiz.find('data')

    metadata.set('canvas_id', canvas_id)
    metadata.set('is_survey', is_survey)

    metadata_file = make_canvas_metadata(course, metadata, preamble, canvas_folder)
    data_file = make_canvas_data(data, metadata, canvas_folder)

    args = {
        'id': canvas_id,
        'type': 'associatedcontent/imscc_xmlv1p1/learning-application-resource',
        'path': metadata_file,
        'files': resource.FILE.format(metadata_file) + resource.FILE.format(data_file)
    }
    course.add_resources(args)


def make_canvas_metadata(course, metadata, preamble, canvas_folder):
    """
    Create an XML file for metadata.
    """
    canvas_id = metadata.get('canvas_id')
    is_survey = metadata.get('is_survey')

    pos = course.get_quiz_pos()
    course.set_quiz_pos(pos + 1)

    args = {
        'title': metadata.findtext('title'),
        'points': metadata.findtext('maximum_score'),
        'attempts': metadata.findtext('maximum_submissions'),
        'quiz_type': 'survey' if is_survey else 'assignment',
        'show_answer': 'false' if is_survey else 'true',
        'shuffle': 'false' if is_survey else 'true',
        'preamble': preamble,
        'quiz_id': canvas_id,
        'assignment_id': 'a_' + canvas_id,
        'position': pos
    }
    content = METADATA.format(**args)
    file_name = '{}/assessment_meta.xml'.format(canvas_id)
    path = '{}/{}'.format(canvas_folder, file_name)
    util.write_file(path, content)
    return file_name


def make_canvas_data(data, metadata, canvas_folder):
    """
    Create an XML file for data.
    """
    canvas_id = metadata.get('canvas_id')
    question_groups = data.find('question_groups')
    args = {
        'quiz_id': canvas_id,
        'title': metadata.findtext('title'),
        'question_groups': canvas_question_groups(question_groups, canvas_id)
    }
    content = DATA.format(**args)
    file_name = 'non_cc_assessments/{}.xml.qti'.format(canvas_id)
    path = '{}/{}'.format(canvas_folder, file_name)
    util.write_file(path, content)
    return file_name


def canvas_question_groups(question_groups, canvas_id):
    """
    Return a string of Canvas question groups.
    """
    ans = ''
    num_group = len(question_groups)
    for idx, question_group in enumerate(question_groups):
        group_id = '{}_{}'.format(canvas_id, idx + 1)
        group_title = '{}/{}'.format(idx + 1, num_group)
        question_group.set('id', group_id)
        question_group.set('title', group_title)
        ans += canvas_question_group(question_group)
    return ans


def canvas_question_group(question_group):
    """
    Return a string of a Canvas question group.
    """
    questions = question_group.findall('question')
    num_select = question_group.get('select')
    if num_select == 'all':
        num_select = len(questions)

    args = {
        'group_id': question_group.get('id'),
        'group_title': question_group.get('title'),
        'num_select': num_select,
        'points': question_points(questions[0]),
        'questions': canvas_questions(question_group, questions)
    }

    return QUESTION_GROUP.format(**args)


def canvas_questions(question_group, questions):
    """
    Return a string of Canvas questions.
    """
    ans = ''
    for idx, question in enumerate(questions):
        group_id = question_group.get('id')
        question_id = '{}_{}'.format(group_id, idx + 1)
        question.set('id', question_id)

        question_type = canvas_question_type(question)
        question.set('type', question_type)

        question_title = question_group.get('title')
        question.set('title', question_title)

        ans += canvas_question(question)
    return ans


def canvas_question(question):
    """
    Return a string of a Canvas question.
    """
    options = canvas_options(question)
    args = {
        'question_id': question.get('id'),
        'question_type': question.get('type'),
        'question_title': question.get('title'),
        'question_points': question_points(question),
        'presentation': canvas_presentation(question, options),
        'processing': canvas_processing(question, options),
        'feedback': canvas_feedback(question, options)
    }
    return QUESTION.format(**args)


def canvas_presentation(question, options):
    """
    Return a string of a Canvas presentation.
    """
    args = {
        'question': question.findtext('data/text'),
        'options': canvas_present_options(question, options)
    }
    return PRESENTATION.format(**args)


def canvas_present_options(question, options):
    """
    Return a string of Canvas options.
    """
    fib_type = ''
    present_options = ''

    question_type = question.get('type')
    if question_type is 'numerical_question':
        fib_type = 'fibtype="Decimal"'
    elif question_type in ('multiple_choice_question', 'multiple_answers_question'):
        for option in options:
            present_options += canvas_present_option(option)

    args = {
        'fib_type': fib_type,
        'options': present_options
    }
    return OPTIONS[question_type].format(**args)


def canvas_present_option(option):
    """
    Return a string of a Canvas option.
    """
    args = {
        'option_id': option.get('id'),
        'option_text': option.findtext('text')
    }
    return OPTION.format(**args)


def canvas_processing(question, options):
    """
    Return a string of a Canvas processing.
    """
    process_feedback = canvas_process_feedback(question, options)
    process_answer = canvas_process_answer(question, options)
    response = process_feedback + process_answer
    return PROCESSING.format(response)


def canvas_process_feedback(question, options):
    """
    Return a string of a Canvas processing feedback.
    """
    ans = ''

    general_feedback = question.findtext('data/explanation')
    if general_feedback:
        args = {
            'continue': 'Yes',
            'condition': CONDITION_OTHER,
            'action': ACTION_FEEDBACK.format('general')
        }
        ans += RESPONSE.format(**args)

    for option in options:
        option_feedback = option.findtext('explanation')
        if option_feedback:
            args = {
                'continue': 'Yes',
                'condition': feedback_condition(question, option),
                'action': ACTION_FEEDBACK.format(option.get('id'))
            }
            ans += RESPONSE.format(**args)

    return ans


def canvas_process_answer(question, options):
    """
    Return a string of a Canvas processing answer.
    """
    args = {
        'continue': 'No',
        'condition': answer_condition(question, options),
        'action': ACTION_SCORE
    }
    return RESPONSE.format(**args)


def canvas_feedback(question, options):
    """
    Return a string of Canvas feedback.
    """
    ans = ''

    general_feedback = question.findtext('data/explanation')
    if general_feedback:
        args = {
            'option_id': 'general',
            'option_feedback': general_feedback
        }
        ans += FEEDBACK.format(**args)

    for option in options:
        option_feedback = option.findtext('explanation')
        if option_feedback:
            args = {
                'option_id': option.get('id'),
                'option_feedback': option_feedback
            }
            ans += FEEDBACK.format(**args)

    return ans


# helper functions
def question_points(question):
    return question.findtext('metadata/parameters/rescale_score')


def canvas_question_type(question):
    """
    Return a Canvas question type from a Coursera type.
    """
    ans = question.find('metadata/parameters')[1].text
    ans = QUESTION_TYPE[ans]

    # Canvas does not support answer split, use short answer instead
    if answer_split(question):
        ans = 'short_answer_question'

    return ans


def canvas_options(question):
    """
    Since Canvas does no support option group, this function
    returns a list of all option nodes in all groups.
    """
    ans = []
    question_id = question.get('id')
    option_groups = question.find('data/option_groups')
    for idx, option in enumerate(option_groups.iter('option')):
        option_id = '{}_{}'.format(question_id, idx + 1)
        option.set('id', option_id)
        ans.append(option)
    return ans


def answer_split(question):
    """
    Return '' if no answer split.
    """
    return question.findtext('metadata/parameters/split/limit')


def option_correct(option, question, fully=False):
    """
    Return True if option is correct.
    """
    option_points = option.get('selected_score')
    if fully:
        return option_points == question_points(question)
    return float(option_points) > 0


def text_condition(question, option):
    """
    Return the match condition of a text option.
    """
    question_type = question.get('type')
    option_text = option.findtext('text')

    if question_type is 'short_answer_question':
        return CONDITION_EQUAL.format(option_text)

    if question_type is 'numerical_question':
        answers = option_text.strip('[]\n').split(',')

        # exact match
        if len(answers) == 1:
            return CONDITION_EQUAL.format(*answers)
        # range match
        else:
            return CONDITION_RANGE.format(*answers)

    return ''


def feedback_condition(question, option):
    """
    Return the match condition of a feedback.
    """
    question_type = question.get('type')
    if question_type in ('multiple_choice_question', 'multiple_answers_question'):
        return CONDITION_EQUAL.format(option.get('id'))
    elif answer_split(question):
        return ''  # Canvas does not support feedback for split answer
    else:
        return text_condition(question, option)


def answer_condition(question, options):
    """
    Return the match condition of a question's answer.
    """
    if answer_split(question):
        ans = []
        for option in options:
            if option_correct(option, question):
                ans.append(option.findtext('text'))
        return CONDITION_EQUAL.format(' '.join(ans))

    question_type = question.get('type')
    ans = ''

    if question_type is 'short_answer_question':
        for option in options:
            if option_correct(option, question, True):
                option_text = option.findtext('text')
                ans += EQUAL.format(option_text)
        return OR.format(ans)

    if question_type is 'numerical_question':
        for option in options:
            if option_correct(option, question, True):
                option_text = option.findtext('text')
                answers = option_text.strip('[]\n').split(',')
                if len(answers) == 1:
                    ans += EQUAL.format(*answers)
                else:
                    ans += RANGE.format(*answers)
        return OR.format(ans)

    if question_type is 'multiple_choice_question':
        for option in options:
            if option_correct(option, question, True):
                option_id = option.get('id')
                ans += EQUAL.format(option_id)
        return OR.format(ans)

    if question_type is 'multiple_answers_question':
        for option in options:
            option_id = option.get('id')
            if option_correct(option, question):
                ans += EQUAL.format(option_id)
            else:
                ans += NOT.format(option_id)
        return AND.format(ans)

    return ans
