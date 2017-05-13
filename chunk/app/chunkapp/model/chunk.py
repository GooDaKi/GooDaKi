#! /usr/bin/env python3

from flask import g
from time import strftime, gmtime
import re


# ***     get     /api/chunk/{id}                 *ChunkControl::getChunkInfo(id)
# ***     get     /api/chunk/author/{id}          *ChunkControl::getChunkByAuthor(authorId)
# ***     post    /api/chunk                      *ChunkControl::createChunk(info)
# ***     put     /api/chunk                      *ChunkControl::editChunk(info)
# ***     post    /api/chunk/search               *ChunkControl::searchChunk(query)
# **      delete  /api/chunk/{id}                 *ChunkControl::deleteChunk(id)

def transform_query(q):
    # TODO make it better not just str -> regex
    result = dict()
    for key, val in q.items():
        if type(val) is str:
            result[key] = re.compile(r'{}'.format(val))
    return result


class Chunk:
    #     :Chunk ## may subject to changes
    # {
    #     "id": string,
    #     "name": string,
    #     "author_id": string,
    #     "type": string,
    #     "video-link": string (url), # if it is a video
    #     "description": string,
    #     "text": string,   # the if the chunk is text-based or have text to show
    #     "created": DateTime,
    #     "updated": DateTime,
    #     "tags": [tags(string)]
    # }

    def __init__(self, options=None):
        if type(options) is dict:
            for key, val in options.items():
                setattr(self, key, val)
            if '_id' in options.keys():
                self.id = str(self._id)
                del self._id
        else:
            self.id = None
            self.name = None
            self.author_id = None
            self.type = None
            self.video_link = None
            self.description = None
            self.text = None
            self.created = strftime('%Y-%m-%d %H:%M:%S', gmtime())
            self.updated = strftime('%Y-%m-%d %H:%M:%S', gmtime())
            self.tags = None

    def edit(self, options):
        if type(options) is not dict:
            return None
        for key, val in options.items():
            setattr(self, key, val)
        self.updated = strftime('%Y-%m-%d %H:%M:%S', gmtime())

    def save(self):
        obj = {key: val for key, val in self.__dict__.items() if val is not None}
        if 'id' in obj:
            obj['_id'] = obj.pop('id', None)
        new_id = g.db.chunk.insert(obj)
        self.id = str(new_id)
        return str(new_id)

    @staticmethod
    def load(chunk_id):
        chunk_validator = re.compile('^[0-9a-fA-F]{24}$')
        if not re.match(chunk_validator, chunk_id):
            return None
        obj = g.db.chunk.find_one({'_id': g.ObjectId(chunk_id)})
        if obj is None:
            return False
        return Chunk(obj)

    @staticmethod
    def load_by_author(author_id):
        cursor = g.db.chunk.find(dict(author_id=int(author_id)))
        ret = list(map(Chunk, cursor))
        return ret

    @staticmethod
    def find(query):
        # TODO: validate query keys
        query = transform_query(query)
        # print(query)
        cursor = g.db.chunk.find(query)
        ret = list(map(Chunk, cursor))
        return ret

    @staticmethod
    def load_any():
        obj = g.db.chunk.find_one({})
        if obj is None:
            return None
        chunk = Chunk(obj)
        return chunk

    @staticmethod
    def get_all():
        cursor = g.db.chunk.find({})
        chunks = list(map(Chunk, cursor))
        return chunks

    @staticmethod
    def delete_by_id(chunk_id):
        result = g.db.chunk.delete_one(dict(_id=g.ObjectId(chunk_id)))
        if result.deleted_count <= 0:
            return None
        return True

    @staticmethod
    def delete_all():
        g.db.chunk.delete_many({})
        return True
