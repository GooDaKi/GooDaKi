# /usr/bin/env python

import pytest
from pymongo import MongoClient
from bson.objectid import ObjectId


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

    def __exit__(self, t, val, traceback):
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
