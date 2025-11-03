import io
import json

payload = {
        "projectName": "Test Project Task",
        "taskNumber": 1,
        "tasks": [
            {
                "taskIndex": 1,
                "taskTitle": "Test task 1",
                "taskInstructions": "test",
                "taskUpload": "test",
                "timeguide": 1,
                "urlForInstructions": "www.test.com",
                "iconForThisStep": 1,
                "componenttype": "test",
                "taskTip": "test"
            }
        ]
    }

# Test for: /api/projectTask/upload
def test_upload_projectTask_1(client):
    data = {
        'file': (
            io.BytesIO(json.dumps(payload).encode('utf-8')),
            'projectTask.json'
        )
    }
    resp = client.post(
        '/api/projectTask/upload',
        data=data,
        content_type='multipart/form-data'
    )
    assert resp.status_code == 200
    assert b'Successfully' in resp.data

# Test for: /api/projectTask/get_projectTask_list
def test_list_projectTask_1(client):
    client.post(
        '/api/projectTask/upload',
        data={'file': (io.BytesIO(json.dumps(payload).encode()), 'projectTask')},
        content_type='multipart/form-data'
    )
    resp = client.get('/api/projectTask/get_projectTask_list')
    assert resp.status_code == 200
    lst = resp.get_json()
    assert isinstance(lst, list)
    assert any(item['filename']=='projectTask.json' for item in lst)
    assert any(item['name']=='Test Project Task' for item in lst)

# Test for: /api/projectTask/get_projectTask
def test_get_projectTask_1(client):
    client.post(
        '/api/projectTask/upload',
        data={'file': (io.BytesIO(json.dumps(payload).encode()), 'projectTask')},
        content_type='multipart/form-data'
    )
    resp = client.get('/api/projectTask/get_projectTask', query_string={'file': 'projectTask'})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['projectName'] == 'Test Project Task'
    assert data['taskNumber'] == 1
    assert isinstance(data['tasks'], list) and len(data['tasks']) == 1
    task = data['tasks'][0]
    assert task['taskIndex'] == 1
    assert task['taskTitle'] == 'Test task 1'
    assert task['timeguide'] == 1
    assert task['urlForInstructions'] == 'www.test.com'
    assert task['iconForThisStep'] == 1
    assert task['componenttype'] == 'test'
    assert task['taskTip'] == 'test'

    resp2 = client.get('/api/projectTask/get_projectTask')
    assert resp2.status_code == 400

# Test for: /api/update/projectTask/update
def test_update_projectTask_1(client):
    client.post(
        '/api/projectTask/upload',
        data={'file': (io.BytesIO(json.dumps(payload).encode()), 'projectTask')},
        content_type='multipart/form-data'
    )
    resp = client.get('/api/projectTask/get_projectTask', query_string={'file': 'projectTask'})
    data = resp.get_json()
    assert data['projectName'] == 'Test Project Task'

    updated = {
        "projectName": "Updated project name",
        "taskNumber": 2,
        "tasks": [
            {
                "taskIndex": 1,
                "taskTitle": "Updated task 1",
                "taskInstructions": "Updated",
                "taskUpload": "Updated",
                "timeguide": 1,
                "urlForInstructions": "www.updated.com",
                "iconForThisStep": 1,
                "componenttype": "Updated",
                "taskTip": "Updated"
            },
            {
                "taskIndex": 2,
                "taskTitle": "Test task 2",
                "taskInstructions": "test",
                "taskUpload": "test",
                "timeguide": 1,
                "urlForInstructions": "www.test.com",
                "iconForThisStep": 1,
                "componenttype": "test",
                "taskTip": "test"
            }
        ]
    }
    resp = client.put(
        '/api/projectTask/update',
        data={'file': (io.BytesIO(json.dumps(updated).encode()), 'projectTask')},
        content_type='multipart/form-data'
    )
    assert resp.status_code == 200

    resp = client.get('/api/projectTask/get_projectTask', query_string={'file': 'projectTask'})
    data = resp.get_json()
    assert data['projectName'] == 'Updated project name'
    assert data['taskNumber'] == 2
    assert isinstance(data['tasks'], list) and len(data['tasks']) == 2

# Test for: /api/projectTask/delete
def test_delete_projectTask_1(client):
    client.post(
        '/api/projectTask/upload',
        data={'file': (io.BytesIO(json.dumps(payload).encode()), 'projectTask')},
        content_type='multipart/form-data'
    )
    resp = client.get('/api/projectTask/get_projectTask', query_string={'file': 'projectTask'})
    assert resp.status_code == 200

    resp2 = client.delete('/api/projectTask/delete', query_string={'file': 'projectTask'})
    assert resp2.status_code == 204

    resp3 = client.get('/api/projectTask/get_projectTask', query_string={'file': 'projectTask'})
    assert resp3.status_code == 500

############################################################################

# Test for: /api/recording/upload
def test_upload_recording_1(client):
    form = {
        'projectName': 'P',
        'firstName': 'Alice',
        'lastName': 'Wu',
        'email': 'a@b.com',
        'uuid': 'u123',
        'taskTile': 'TaskOne'
    }
    files = {
        'recordedScreen': (io.BytesIO(b'screen-data'), 's.webm'),
        'recordedCamera': (io.BytesIO(b'cam-data'), 'c.webm'),
        'recordedAudio': (io.BytesIO(b'audio-data'), 'a.webm'),
    }

    resp = client.post(
        '/api/recording/upload',
        data={**form, **files},
        content_type='multipart/form-data'
    )
    assert resp.status_code == 200
    result = resp.get_json()
    assert result['status'] == 'success'
    keys = result['keys']
    assert 'recordedScreen' in keys
    assert 'recordedCamera' in keys
    assert 'recordedAudio' in keys
    assert 'metadata' in keys

    assert isinstance(keys['metadata'], str)

############################################################################

# Test for: /api/visualization/get_project_list


# Test for: /api/visualization/get_heatmap_list/<project_name>