<<<<<<< HEAD
#!/usr/bin/env python3

from mainapp.controller import user_control

from mainapp import app


@app.errorhandler(403)
def forbidden(e):
    return '403: forbidden', 403


@app.error_handler(404)
def page_not_found(e):
    return '404: page not found', 404
=======
from mainapp.controller import user_control,career_stub,course_stub,chunk_stub,search_stub

>>>>>>> origin/orakanya_course_and_subject_service
