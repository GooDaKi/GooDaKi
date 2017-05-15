# /usr/bin/env python

import pytest
import re
from pymongo import MongoClient
from bson.objectid import ObjectId


def is_objectid(e):
    objectid_validator = re.compile('^[0-9a-fA-F]{24}$')
    return re.match(objectid_validator, str(e))


class Dispose:
    def __init__(self):
        self.dispose_list = list()
        self.db = db()

    def __enter__(self):
        return self.dispose_list

    def __exit__(self, exc_type, exc_val, exc_tb):
        # print('dispose list contains {}'.format(self.dispose_list))
        dispose_ids = list(filter(is_objectid, self.dispose_list))
        for cid in dispose_ids:
            self.db.chunk.delete_one(dict(_id=ObjectId(cid)))
        dispose_objs = list(filter(lambda x: type(x) is dict, self.dispose_list))
        for obj in dispose_objs:
            self.db.chunk.delete_one(obj)


class TestEnv:
    def __init__(self):
        self.chunk_ids = list()
        self.db = db()

    def __enter__(self):
        chunk_objs = [
            {
                'name': 'chunk-1',
                'author_id': 2,
                'type': 'text',
                'description': 'test-chunk number #1',
                'tags': ['tag-1', 'tag-2']
            },
            {
                'name': 'chunk-2',
                'author_id': 2,
                'type': 'text',
                'description': 'test-chunk number #2',
                'tags': ['tag-1', 'tag-3']
            },
            {
                'name': 'chunk-3',
                'author_id': 3,
                'type': 'video',
                'video_link': 'http://some-video-link.com',
                'description': 'test-chunk number #3',
                'tags': ['tag-0', 'tag-2']
            }
        ]

        for i, obj in enumerate(chunk_objs):
            self.chunk_ids.append(str(self.db.chunk.insert(obj)))
            obj['id'] = str(obj.pop('_id'))

        return list(zip(self.chunk_ids, chunk_objs))

    def __exit__(self, exc_type, exc_val, exc_tb):
        for cid in self.chunk_ids:
            self.db.chunk.delete_one(dict(_id=ObjectId(cid)))


@pytest.fixture(scope='session')
def db():
    client = MongoClient('localhost', 28001)
    return client.goodaki


@pytest.fixture(scope='session')
def chunk_ids():
    env = TestEnv()
    with env as arr:
        yield arr


@pytest.fixture
def chunk_dispose_list():
    dispose_obj = Dispose()
    with dispose_obj as d:
        yield d
