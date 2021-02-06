import json
import requests
from tenacity import retry, retry_if_result, stop_after_attempt, wait_fixed


@retry(retry=retry_if_result(lambda x: x.status_code == 202), stop=stop_after_attempt(5), wait=wait_fixed(0.05))
def get_successful_request(request: requests.Request) -> requests.Response:
    """
    First cvat response sometimes is 202 without any actions
    So the best way to fix it is to send the same request again
    :param request:
    :return:
    """
    with requests.Session() as s:
        return s.send(request.prepare())


def get_annotation(url: str, token: str, task_id: int, format='COCO 1.0') -> dict:
    """
    Reads annotation file from server in given format
    :param url:
    :param token: authorization token
    :param task_id:
    :param format: annotation format. My favorite is coco :)
    :return:
    """
    request = requests.Request(
        method='GET',
        url=f'{url}/api/v1/tasks/{task_id}/annotations',
        headers={
            'Authorization': f'Token {token}',
            'accept': 'application/json'
        },
        params={
            'format': format,
            'action': 'download'
        }
    )
    response = get_successful_request(request)
    if response.status_code != 200:
        raise ValueError(f'Could not get annotation, status: {response.status_code}, message: {response.content}')
    return json.loads(response.content[64:-102])


def put_annotation(url: str, token: str, task_id: int, format='COCO 1.0', *, annotation: dict) -> requests.Response:
    """
    Upload given annotation to server, replacing existing.
    Warning: Be careful and backup existing annotations on server, there is no way to restore them.
    :param url:
    :param token:
    :param task_id:
    :param format:
    :param annotation:
    :return:
    """
    # I put data in raw format here because CVAT did not accepted data if it was passed in files key
    request = requests.Request(
        method='PUT',
        url=f'{url}/api/v1/tasks/{task_id}/annotations',
        headers={
            'Authorization': f'Token {token}',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryou0YKzTMZAuZ4RqF',
            'Connection': 'keep-alive',
        },
        params={
            'format': format,
        },
        data=f'------WebKitFormBoundaryou0YKzTMZAuZ4RqF\r\nContent-Disposition: form-data; '
             f'name="annotation_file"; filename="f.json"\r\nContent-Type: '
             f'application/json\r\n\r\n{json.dumps(annotation)}\r\n------WebKitFormBoundaryou0YKzTMZAuZ4RqF--\r\n'
    )
    response = get_successful_request(request)
    return response
