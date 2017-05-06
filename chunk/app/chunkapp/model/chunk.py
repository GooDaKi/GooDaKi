#! /usr/bin/env python3

# ***     get     /api/chunk/{id}                 *ChunkControl::getChunkInfo(id)
# ***     get     /api/chunk/author/{id}          *ChunkControl::getChunkByAuthor(authorId)
# ***     post    /api/chunk                      *ChunkControl::createChunk(info)
# ***     put     /api/chunk                      *ChunkControl::editChunk(info)
# ***     post    /api/chunk/search               *ChunkControl::searchChunk(query)
# **      delete  /api/chunk/{id}                 *ChunkControl::deleteChunk(id)

class Chunk:
    :Chunk ## may subject to changes
{
    "chunkid": string,
    "chunkname": string,
    "authorid": string,
    "type": string,
    "video-link": string (url), # if it is a video
    "description": string,
    "text": string,   # the if the chunk is text-based or have text to show
    "created": DateTime,
    "updated": DateTime,
    "pretest" : test,
    "posttest" : test,
    "tags": [tags(string)]
}

    def __init__(self, options=None):
        if type(options) is dict:
            for key, val in db_row.items():
                setattr(self, key, val)
        else:
            self.id = None
            self.chunkname = None
            self.authorid = None
            self.type = None
            self.video_link = None
            self.description = None
            self.text = None
            self.created = None
            self.updated = None
            self.tags = None
        
    @staticmethod
    def load(chunk_id):
        chunk = g.db.chunk.find_one({'_id': chunk_id})
        return chunk
