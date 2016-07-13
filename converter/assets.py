"""
Convert assets folder.
"""
import os
import shutil
import resource


def convert(course):
    coursera_assets_folder = course.get_coursera_folder().rpartition('/')[0] + '/assets'
    canvas_assets_folder = course.get_canvas_folder() + '/web_resources'

    # print "copy assets folder..."
    # copy_folder(coursera_assets_folder, canvas_assets_folder)

    add_resources(course, canvas_assets_folder)


def add_resources(course, assets_folder):
    for path in all_file_paths(assets_folder):
        pos = course.get_asset_pos()
        course.set_asset_pos(pos + 1)

        canvas_id = '{}_{}'.format('asset', pos)
        canvas_path = path.replace(assets_folder, 'web_resources')

        args = {
            'id': canvas_id,
            'type': 'webcontent',
            'path': canvas_path,
            'files': resource.FILE.format(canvas_path)
        }
        course.add_resources(args)


def copy_folder(src_folder, dst_folder):
    shutil.copytree(src_folder, dst_folder)


def all_file_paths(folder):
    ans = []
    for root, _, files in os.walk(folder):
        for filename in files:
            path = '{}/{}'.format(root, filename)
            ans.append(path)
    return ans
