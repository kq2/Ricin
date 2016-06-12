"""
Download a Coursera course.
"""
import course


CLASS_URL = 'https://class.coursera.org/'
IIPP = 'interactivepython'
POC = 'principlescomputing'
ALG = 'algorithmicthink'
FOC = 'foccapstone'
TA = 'interactivepythontas'

RICE_URL = 'https://rice.coursera.org/'
COMP160 = 'rice-interactivepython'
COMP140 = 'thinkpython'
COMP182 = 'algorithmicthinking'

COURSES = {
    IIPP: [
        '-002', '-003', '-004', '-005',
        '1-002', '1-003', '1-007',
        '1-008', '1-009', '1-010',
        '2-002', '2-003', '2-007',
        '2-008', '2-009', '2-010'
    ],
    POC: [
        '-001',
        '1-002', '1-003', '1-004', '1-005',
        '2-002', '2-003', '2-004', '2-005'
    ],
    ALG: [
        '-001',
        '1-002', '1-003', '1-004',
        '2-002', '2-003', '2-004'
    ],
    FOC: [
        '-001', '2-002', '2-003'
    ],
    'analyticalchem': ['-001'],
    'eefun': ['-001', '-002'],
    'eefunlab': ['-001'],
    'foreigneyes': ['-001'],
    'genchem1': ['-001'],
    'genchem2': ['-001'],
    'inquirytechniques': ['-001'],
    'nanotech': ['-001'],
    'scicontentsurvey': ['-001'],
    'sciframework': ['-001'],
    'scileadership': ['-001'],
    'scistudentinquiry': ['-001'],
    'teachinghist': ['-001']
}


def run(course_url):
    _course = course.Course(course_url)

    # _course.download_section_file()
    _course.download()
    # _course.download_grades()
    # _course.download_stats()
    # _course.download_subtitles()

    # _course.download_forum()
    # _course.download_personal_info()
    # _course.download_compressed_video()

    # _course.download_assets()
    # _course.download_original_videos()


def get_all():
    for course_name, sessions in COURSES.items():
        for session in sessions:
            url = CLASS_URL + course_name + session
            run(url)


# run(CLASS_URL + TA + '-001')
# run(RICE_URL + COMP140 + '-002')
get_all()
