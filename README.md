# CVAT toolbox

Tools for cvat tasks automatization. 

I got to create a lot of tasks during one project, so I created a couple of 
python scripts to make this process less boring. 

This repo allows you to automatically create tasks on CVAT server
and upload data into jobs  from connected file share.

## quick example: 
```python
from cvat_runner import CVATRunner
runner = CVATRunner(url='http://localhost:8080', username='', password='')
task_data = runner.create_task(name='task_2', project_id=1)
runner.upload_shared_data(task_id=task_data['id'], file_paths=file_paths)
```

More detailed information provided in `main.py` file
