#!/usr/bin/env python3

from mainapp.controller import user_control,temporary_stub

from mainapp import app


@app.errorhandler(403)
def forbidden(e):
    return '403: forbidden', 403


@app.errorhandler(404)
def page_not_found(e):
    return '404: page not found', 404
