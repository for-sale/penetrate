import time
from app.models.content import Content
from app.models.base import db
from .common import SOFTWARE_ID
from . import web
from flask import current_app
import json


# @web.before_request
@web.before_app_first_request
def type_sorted():
    printer_types = db.session.query(Content.issue_type_id).group_by(Content.issue_type_id).order_by(
        db.desc(db.func.count(Content.id))).all()
    sorted_type_id = []
    for p_type in printer_types:
        sorted_type_id.append(p_type[0])
    print(sorted_type_id)
    return sorted_type_id


# @web.errorhandler(400)
# def error(msg):
#     current_app.logger.error(msg)

#     return '400'


def jsonify(*args, **kwargs):
    indent = None
    separators = (',', ':')

    if current_app.config['JSONIFY_PRETTYPRINT_REGULAR'] or current_app.debug:
        indent = 2
        separators = (', ', ': ')

    if args and kwargs:
        raise TypeError('jsonify() behavior undefined when passed both args and kwargs')
    elif len(args) == 1:  # single args are passed directly to dumps()
        data = args[0]
    else:
        data = args or kwargs

    return current_app.response_class(
        json.dumps(data, indent=indent, separators=separators, sort_keys=False) + '\n',
        mimetype=current_app.config['JSONIFY_MIMETYPE']
    )

