# backend/tests/conftest.py
import os, sys
import io

import pytest

# find and import app.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import boto3

class DummyS3:
    def __init__(self):
        self.storage = {}

    def upload_fileobj(self, fileobj, Bucket, key):
        fileobj.seek(0)
        self.storage[key] = fileobj.read()

    def put_object(self, Bucket, Key, Body, ContentType=None):
        if hasattr(Body, 'read'):
            Body.seek(0)
            data = Body.read()
        else:
            data = Body
        self.storage[Key] = data
        return {'ResponseMetadata': {'HTTPStatusCode': 200}}

    def list_objects(self, Bucket, Prefix=''):
        keys = [k for k in self.storage if k.startswith(Prefix)]
        return {'Contents': [{'Key': k} for k in keys]}

    def get_object(self, Bucket, Key):
        import io
        data = self.storage.get(Key)
        if data is None:
            raise KeyError(f"{Key} not found in DummyS3")
        return {'Body': io.BytesIO(data)}

    def delete_object(self, Bucket, Key):
        self.storage.pop(Key, None)

_dummy_s3 = DummyS3()
boto3.client = lambda *args, **kwargs: _dummy_s3

from app import create_app

@pytest.fixture(scope='session', autouse=True)
def s3_bucket_env():
    os.environ['S3_BUCKET'] = 'test-bucket'
    yield
    del os.environ['S3_BUCKET']

@pytest.fixture
def app():
    return create_app(config_name='testing')
