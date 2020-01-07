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


@web.route("/solve_status", methods=["POST"])
def solve_status():
    n = request.form.get("length")
    if not n:
        n = 0
    if int(n):
        print(".......", n)
        start_time, end_time = last_few_days(int(n))
        status_data = db.session.query(Content.status_id, db.func.count(Content.id)).filter(
            Content.as_date.between(start_time, end_time)).group_by(Content.status_id).all()
    else:
        print("++++++", n)
        status_data = db.session.query(Content.status_id, db.func.count(Content.id)).group_by(Content.status_id).all()
    dic_status_data = {93: {"status_id": 93, "counts": 0, "percent": 0}}
    if status_data:
        total = 0
        for s_data in status_data:
            if s_data[0] == None:
                dic_status_data[93]["counts"] += s_data[1]
                total += s_data[1]
            else:
                dic_status_data[s_data[0]] = {"status_id": s_data[0], "counts": 0, "percent": 0}
                dic_status_data[s_data[0]]["counts"] += s_data[1]
                total += s_data[1]
        for k, v in dic_status_data.items():
            v["percent"] = float("%.2f" % (v["counts"] / total))
        res_dic = {}
        res_dic["data"] = list(dic_status_data.values())
    else:
        res_dic = {}
    return Response(json.dumps(res_dic), mimetype='application/json')

