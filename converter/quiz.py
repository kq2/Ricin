"""
Convert a Coursera quiz into a Canvas quiz.
"""
from scraper import util


def convert(course_obj, course_item):
    item_id = course_item['item_id']
    canvas_id = 'quiz' + item_id
    coursera_folder = course_obj.get_coursera_folder() + '/quiz'
    canvas_folder = util.make_folder(course_obj.get_canvas_folder() + '/' + canvas_id)

    # This folder must exist for importing quizzes into Canvas.
    util.make_folder(course_obj.get_canvas_folder() + '/non_cc_assessments')

    coursera_file = coursera_folder + '/%s.xml' % item_id
    canvas_meta_file = canvas_folder + '/assessment_meta.xml'
    canvas_data_file = canvas_folder + '/assessment_qti.xml'

    quiz_type = 'assignment'
    if course_item['quiz_type'] == 'survey':
        quiz_type = 'survey'

    root = util.xml_root(coursera_file)
    metadata = root[0]
    preamble = root[1]
    question_groups = root[2][0]

    convert_metadata(quiz_type, metadata, preamble, canvas_id, canvas_meta_file)

    # for child in question_groups:
    #     print child.tag

    # for question_group in root.iter('question_group'):
    #     print len(question_group)


def convert_metadata(quiz_type, metadata, preamble, canvas_id, canvas_meta_file):
    data = {
        'canvas_id': canvas_id,
        'quiz_type': quiz_type,
        'title': metadata.find('title').text,
        'points': metadata.find('maximum_score').text,
        'attempts': metadata.find('maximum_submissions').text,
        'preamble': preamble.text if preamble.text else '',
        'shuffle': 'false' if quiz_type == 'survey' else 'true',
        'show_answer': 'false' if quiz_type == 'survey' else 'true'
    }
    template = util.read_file('quiz_meta_template.xml')
    util.write_file(canvas_meta_file, template.format(**data))
