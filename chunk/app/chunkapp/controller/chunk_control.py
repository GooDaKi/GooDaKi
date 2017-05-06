#!/usr/bin/env python3

import flask_login
import requests
from flask import request, session, flash, redirect, url_for, render_template, jsonify, abort, g
from flask_login import login_required, current_user
from chunkapp import app


# ***     get     /api/chunk/{id}                 *ChunkControl::getChunkInfo(id)
# ***     get     /api/chunk/author/{id}          *ChunkControl::getChunkByAuthor(authorId)
# ***     post    /api/chunk                      *ChunkControl::createChunk(info)
# ***     put     /api/chunk                      *ChunkControl::editChunk(info)
# ***     post    /api/chunk/search               *ChunkControl::searchChunk(query)
# **      delete  /api/chunk/{id}                 *ChunkControl::deleteChunk(id)

@app.route('/api/chunk/test')
def test():
    return 'testing chunk controller'