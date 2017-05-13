#!/usr/bin/env python3

import flask_login
import requests
from flask import request, session, flash, redirect, url_for, render_template, jsonify, abort, g
from flask_login import login_required, current_user
from chunkapp import app
import chunkapp.model as model


# *** passed    get     /api/chunk/{id}                 *ChunkControl::getChunkInfo(id)
# *** passed    get     /api/chunk/author/{id}          *ChunkControl::getChunkByAuthor(authorId)
# *** passed    post    /api/chunk                      *ChunkControl::createChunk(info)
# ***     put     /api/chunk                      *ChunkControl::editChunk(info)
# *** passed    post    /api/chunk/search               *ChunkControl::searchChunk(query)
# **  passed    delete  /api/chunk/{id}                 *ChunkControl::deleteChunk(id)

def chunk_to_dict(chunk):
    ret = dict()
    for key, val in chunk.__dict__:
        if type(val) not in [int, str, list, dict, set, float]:
            val = str(val)
        ret[key] = val
    return ret


@app.route('/api/chunk/test')
def test():
    return 'testing chunk controller'


@app.route('/api/chunk/all')
def load_all():
    chunks = model.Chunk.get_all()
    if chunks is None:
        return jsonify(dict(error='error occurred')), 500
    return jsonify(list(map(lambda x: x.__dict__, chunks)))


@app.route('/api/chunk/any')
def load_any():
    chunk = model.Chunk.load_any()
    if chunk is None:
        return jsonify(dict(error='no chunk found')), 500
    return jsonify(chunk.__dict__)


@app.route('/api/chunk/createany/<name>')
def create_any(name='NAME'):
    chunk = model.Chunk()
    chunk.name = name
    chunk.save()
    return 'successfully create chunk name: {}'.format(name)


@app.route('/api/chunk/<chunk_id>')
def get_chunk_by_id(chunk_id):
    chunk = model.Chunk.load(chunk_id)
    if chunk is None:
        return jsonify(dict(error='chunk_id is not valid')), 400
    elif type(chunk) is bool and chunk is False:
        return jsonify(dict(error='chunk not found')), 500
    return jsonify(chunk.__dict__)


@app.route('/api/chunk/author/<author_id>')
def get_chunk_by_author_id(author_id):
    if type(author_id) is not str or not author_id.isdigit():
        return jsonify(dict(error='invalid author id')), 400
    chunks = model.Chunk.load_by_author(author_id)
    ret = list(map(lambda x: x.__dict__, chunks))
    return jsonify(ret)


@app.route('/api/chunk', methods=['POST'])
def create_chunk():
    options = request.get_json()
    options = dict(options)
    chunk = model.Chunk(options)
    new_id = chunk.save()
    if new_id is not None:
        return jsonify(dict(success=True, inserted_id=new_id))


@app.route('/api/chunk', methods=['PUT'])
def edit_chunk():
    # TODO change to correct chunk this is just a template
    options = request.get_json()
    ret = dict(options)
    ret['message'] = 'this is the receive message json'
    return jsonify(ret)


@app.route('/api/chunk/search', methods=['POST'])
def search_for_chunks():
    # TODO: make the search function more sophisticated
    options = request.get_json()
    ret = dict(options)
    chunks = model.Chunk.find(ret)
    return jsonify(list(map(lambda x: x.__dict__, chunks)))


@app.route('/api/chunk/<chunk_id>', methods=['DELETE'])
def delete_chunk(chunk_id):
    ret = model.Chunk.delete_by_id(chunk_id)
    if ret is None:
        return 'error occurred. Maybe the id is invalid', 400
    return 'deleted chunk with id: {}'.format(chunk_id)


@app.route('/api/chunk/deleteall', methods=['POST'])
def delete_all():
    msg = 'success'
    key = request.get_json()['key']
    if key == 'delete all':
        model.Chunk.delete_all()
    else:
        msg = 'error'
    return jsonify(dict(msg=msg))
