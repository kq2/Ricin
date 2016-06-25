"""
Convert assets folder.
"""
import os
import shutil
import resource


def convert(course):
    coursera_assets_folder = course.get_coursera_folder().rpartition('/')[0] + '/assets'
    canvas_assets_folder = course.get_canvas_folder() + '/web_resources'
    copy_folder(coursera_assets_folder, canvas_assets_folder)
    return add_resources(coursera_assets_folder)


def add_resources(assets_folder):
    ans = ''
    for idx, path in enumerate(all_files(assets_folder)):
        canvas_id = '{}_{}'.format('asset', idx + 1)
        canvas_path = 'web_resources/' + path
        args = {
            'id': canvas_id,
            'type': 'webcontent',
            'path': canvas_path,
            'files': resource.FILE.format(canvas_path)
        }
        ans += resource.TEMPLATE.format(**args)
    return ans


def copy_folder(src_folder, dst_folder):
    shutil.copytree(src_folder, dst_folder)


def all_files(folder, rel_path=True):
    ans = []
    for root, _, files in os.walk(folder):
        for filename in files:
            path = root
            if rel_path:
                path = os.path.relpath(root, folder)
            ans.append(os.path.join(path, filename))
    return ans
