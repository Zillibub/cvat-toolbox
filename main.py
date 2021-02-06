import os
from time import sleep
from cvat_runner import CVATRunner
import logging
from tqdm import tqdm


def main():
    # step 1: login
    runner = CVATRunner(
        url='http://localhost:8080',
        username='',  # username here
        password=''  # password  here
    )

    # Next you need to create task with original name
    # assuming you know the project id

    task_data = runner.create_task(name='task_2', project_id=1)

    # prepare folders that will be used for tasks
    share_folder = '../cvat-share'  # replace it with path to your share folder
    folders = os.listdir(share_folder)  # folders which will be used for jobs creation

    # now we want to add some data to the created task
    # here we add all data from folders in share root
    for folder in tqdm(folders):
        logging.info(f'starting folder ')
        # very important thing about file paths:
        # they should be going from the root of file share
        # for example if there is file in ../cvat-share/b1/file1.png
        # in file_paths array it should be as /b1/file1.png
        file_paths = [os.path.join(folder, x) for x in list(os.walk(os.path.join(share_folder, folder)))[0][2]]
        runner.upload_shared_data(task_id=task_data['id'], file_paths=file_paths)
        sleep(60)  # wait for one minute for files to upload


if __name__ == '__main__':
    main()
