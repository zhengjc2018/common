import os
import shutil
import zipfile
import argparse
import traceback


def do_sth(zip_path, old_context, new_context):
    '''
        this func used to rename the file which in the zip files
    '''
    for i in os.listdir(zip_path):
        if i.split('.')[-1] != 'zip':
            continue
        try:
            zip_name = os.path.join(zip_path, i)
            folder = zip_name.replace('.zip', '')

            if os.path.exists(folder):
                shutil.rmtree(folder)
            os.mkdir(folder)

            file = zipfile.ZipFile(zip_name, 'r')
            for i in file.namelist():
                file.extract(i, zip_path)

                old = os.path.join(zip_path, i)
                new = os.path.join(folder, i.replace(old_context, new_context))

                shutil.move(old, new)
            file.close()

            os.remove(zip_name)
            shutil.make_archive(folder, 'zip', folder)
            shutil.rmtree(folder)
        except Exception:
            print(f'rename zipfile err{traceback.format_exc()}')

    print(f'{zip_path} change finish')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="run", description="zipfile rename")
    parser.add_argument("zipfolder", help="the location of the folder where zipfiles in it")
    parser.add_argument("old_name", help="the name that you want to change")
    parser.add_argument("new_name", help="the name that you want to change to")
    args = parser.parse_args()

    zip_path = args.zipfolder
    old_name = args.old_name
    new_name = args.new_name
    do_sth(zip_path, old_name, new_name)
