import json
import time
from . import web
from app.models.issue import Issue
from app.models.content import Content
from app.models.setting import Setting
from app.models.base import db
from flask import current_app, Response, request, jsonify
from .common import PRINTER_TYPE, last_few_days
from .utils import type_sorted
from pandas import DataFrame


# status_data = db.session.query(Content.status_id, db.func.count(Content.id)).filter(
# Content.as_date.between(start_time, end_time)).group_by(Content.status_id).all()


@web.route("/solve_time", methods=["POST"])
def solve_time():
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")
    return "test"
