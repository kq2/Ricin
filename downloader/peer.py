"""
Download Coursera peer-grading page.
"""
import re
import util


def download(course, item):
    """
    Download peer-grading JSON.
    :param course: A Course object.
    :param item: This JSON item is directly written into saved file.
    :return: None.
    """
    path = '{}/peer_assessment/{}.json'
    path = path.format(course.get_folder(), item['item_id'])

    util.make_folder(path, True)
    util.write_json(path, item)

    content = util.read_file(path)
    content = util.remove_coursera_bad_formats(content)

    util.write_file(path, content)


def download_assessment(course):
    _download_assesment(course, 'peer_assessment_bulk_download', 'submissions')
    _download_assesment(course, 'peer_assessment_grades', 'grades')


def _download_assesment(course, url, folder):
    url = '{}/data/export/{}'.format(course.get_url(), url)
    temp = 'temp.html'
    util.download(url, temp, course.get_cookie_file())

    page = util.read_file(temp)
    util.remove(temp)

    pattern = r'<tbody>.*?</tbody>'
    table = re.findall(pattern, page, re.DOTALL)[-1]

    pattern = r'<td colspan="2">(.*?)</td>.*?<a href="(.*?/export/(.*?)\?.*?)">Download</a>'
    for tr_match in re.finditer(r'<tr>.*?</tr>', table, re.DOTALL):
        for match in re.finditer(pattern, tr_match.group(0), re.DOTALL):
            name = match.group(1).replace('&quot;', '').replace(':', '')
            name = name.replace('&lt;em&gt;', '')
            name = name.replace('&lt;/em&gt;', '')
            url = match.group(2)
            file_name = util.unquote(match.group(3))

            path = u'{}/peer_assessment/{}/{} {}'.format(
                course.get_folder(), folder, name, file_name
            )
            util.download(url, path, course.get_cookie_file(), resume=True)
