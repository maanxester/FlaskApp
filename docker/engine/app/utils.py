
from flask import json
from werkzeug.exceptions import default_exceptions


def handle_any_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "message": e.description,
    })
    response.content_type = "application/json"
    return response


def register_error_handlers(app):
    for ex in default_exceptions:
        app.register_error_handler(ex, handle_any_exception)
