import json
import requests
import logging
from typing import List


class CVATRunner:
    """
    Class for interaction with CVAT server
    """

    def __init__(
            self,
            url: str,
            username: str,
            password: str,
    ):
        self.url = url
        self.username = username
        self.password = password

        self._key = None

        self._authorize()

    def _authorize(self):
        response = requests.post(
            f'{self.url}/api/v1/auth/login',
            headers={
                'Content-Type': 'application/json'
            },
            data=json.dumps({'username': self.username, 'password': self.password})
        )
        if response.status_code != 200:
            raise ValueError('Authorization failed')
        self._key = response.json()['key']

    def get_projects(self):
        """

        :return: List of all projects
        """
        response = requests.get(
            f'{self.url}/api/v1/projects',
            headers={
                'Authorization': f'Token {self._key}',
            },
        )
        return response.json()['results']

    def create_task(self, name: str, project_id: int = None):
        """
        Creating new task
        :param name: name of the new task to create
        :param project_id: On which project assign created task.
        :return:
        """
        data = {
                'name': name,
            }
        if project_id is not None:
            data['project_id'] = project_id
        response = requests.post(
            f'{self.url}/api/v1/tasks',
            headers={
                'Authorization': f'Token {self._key}',
                'Content-Type': 'application/json'
            },
            data=json.dumps(data)
        )
        if response.status_code != 201:
            raise ValueError('Project creation failed')
        logging.info(f'Project {response.json()["id"]} created')

        return response.json()

    def upload_shared_data(self, task_id, file_paths: List[str]):
        """
        Uploads data from connected file share to given task creating a new job
        :param task_id: task id to upload ded
        :param files_paths: file paths from file share
        :return:
        """
        for i in range(len(file_paths)):
            if file_paths[i][0] != '/':
                # All files should have / on the beginning with path from shared folder
                file_paths[i] = '/' + file_paths[i]

        data = {f'server_files[{i}]': x for i, x in enumerate(file_paths)}
        data['image_quality'] = '70'
        data['use_zip_chunks'] = 'true'
        data['use_cache'] = 'true'
        response = requests.post(
            f'{self.url}/api/v1/tasks/{task_id}/data',
            headers={
                'Authorization': f'Token {self._key}',
            },
            data=data
        )
        return response.json()
