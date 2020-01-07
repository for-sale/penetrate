import json
import time
from . import web
from app.models.issue import Issue
from app.models.content import Content
from app.models.setting import Setting
from app.models.base import db
from flask import current_app, Response, request, jsonify
from .common import PRINTER_TYPE, last_few_days, get_year_week
from .utils import type_sorted
from pandas import DataFrame


# status_data = db.session.query(Content.status_id, db.func.count(Content.id)).filter(
# Content.as_date.between(start_time, end_time)).group_by(Content.status_id).all()


@web.route("/solve_time", methods=["POST"])
def solve_time():
    date_start = request.json.get("start_date")
    date_end = request.json.get("end_date")
    start_time, end_time = get_year_week(date_start, date_end)
    data = Content.query.filter(Content.id < 10).all()
    d_list = []
    d_dic = {}
    for d in data:
        # if d.serial_no and d.as_cycle:
            # print(d.issue_type_id, d.as_cycle)
        pass

    return "test"
