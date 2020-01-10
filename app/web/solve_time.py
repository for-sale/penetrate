from . import web
from app.models.content import Content
from app.models.base import db
from flask import current_app, request
from .common import get_year_week
from .utils import jsonify, type_sorted
import time


@web.route("/solve_time", methods=["POST"])
def solve_time():
    current_app.logger.info("/api-v1/solve_time")
    date_start = request.json.get("date_start", "2018-01")
    end_default = time.strftime('%Y-%W', time.localtime(time.time()))
    date_end = request.json.get("date_end", end_default)
    bool_res = all([date_start, date_end])
    if not bool_res:
        return jsonify({"status": "failed", "msg": "missing required parameters issue type"}), 200, {
            'ContentType': 'application/json'}
    issue_type_ids = request.json.get("issue_type_ids", None)
    if not issue_type_ids:
        issue_type_ids = type_sorted[0:10]
    start_year, start_week = get_year_week(date_start)
    end_year, end_week = get_year_week(date_end)
    start_compare = start_year * 100 + start_week
    end_compare = end_year * 100 + end_week

    content_data = Content.query.filter(Content.issue_type_id.in_(issue_type_ids),
                                        Content.produce_year * 100 + Content.produce_week > start_compare,
                                        Content.produce_year * 100 + Content.produce_week < end_compare).all()

    type_cycle_dic = {}
    for t_id in issue_type_ids:
        type_cycle_dic.update({t_id: []})
    for data in content_data:
        type_id = data.issue_type_id
        as_cycle = data.as_cycle
        if as_cycle > 0:
            type_cycle_dic[type_id].append(as_cycle)
            type_cycle_dic[type_id].sort()

    res_dic = {"data": []}
    for k, v in type_cycle_dic.items():
        if v:
            total = len(v)
            low_node = v[round(total * 0.2)]
            high_node = v[round(total * 0.8)]
            average = round(sum(v) / total)
            low_cycle = v[0]
            high_cycle = v[-1]
            box_data = {
                "x_type_id": k,
                "low_cycle": low_cycle,
                "low_node": low_node,
                "average": average,
                "high_node": high_node,
                "high_cycle": high_cycle,
            }
            res_dic["data"].append(box_data)
    return jsonify(res_dic), 200, {'ContentType': 'application/json'}
