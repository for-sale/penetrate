import time
import json
from . import web
from app.models.content import Content
from flask import current_app, request, Response
from .common import get_year_week
from .utils import type_sorted


@web.route("/solve_time", methods=["POST"])
def solve_time():
    try:
        date_start = request.json.get("date_start", "2018-01")
        end_default = time.strftime('%Y-%W', time.localtime(time.time()))
        date_end = request.json.get("date_end", end_default)
        issue_type_ids = request.json.get("issue_type_ids", None)
    except Exception as e:
        current_app.logger.error("select solve_time data error: {}".format(str(e)))
        raise e

    bool_res = all([date_start, date_end])
    if not bool_res:
        res_dic = {"status": "failed", "msg": "missing required parameters date_start or date_end"}
        return Response(json.dumps(res_dic), mimetype='application/json')

    if not issue_type_ids:
        try:
            issue_type_ids = type_sorted()[0:10]
        except Exception as e:
            current_app.logger.error("solve_time, select sorted_type_id data error")
            raise e

    res_dic = get_mysql_data(date_start, date_end, issue_type_ids)
    return Response(json.dumps(res_dic), mimetype='application/json')


def get_mysql_data(date_start, date_end, issue_type_ids):
    try:
        start_year, start_week = get_year_week(date_start)
        end_year, end_week = get_year_week(date_end)
        start_compare = start_year * 100 + start_week
        end_compare = end_year * 100 + end_week

        content_data = Content.query.filter(Content.issue_type_id.in_(issue_type_ids),
                                            Content.produce_year * 100 + Content.produce_week > start_compare,
                                            Content.produce_year * 100 + Content.produce_week < end_compare).all()
    except Exception as e:
        current_app.logger.error("select solve_time data error, args: issue_type_ids:{}, "
                                 "date_start:{}, date_end:{}".format(issue_type_ids, date_start, date_end))
        raise e
    res_dic = get_res_dic(issue_type_ids, content_data)
    return res_dic


def get_res_dic(issue_type_ids, content_data):
    type_cycle_dic = dict()
    for t_id in issue_type_ids:
        type_cycle_dic.update({t_id: []})
    try:
        for data in content_data:
            type_id = data.issue_type_id
            as_cycle = data.as_cycle
            if as_cycle > 0:
                type_cycle_dic[type_id].append(as_cycle)
                type_cycle_dic[type_id].sort()

        res_dic = {"data": []}
    except Exception as e:
        current_app.logger.error(e)
        return []
    max_counts = 0
    for k, v in type_cycle_dic.items():
        if v:
            total = len(v)
            low_node = v[round(total * 0.2)]
            high_node = v[round(total * 0.8)]
            average = round(sum(v) / total)
            low_cycle = v[0]
            high_cycle = v[-1]
            max_counts = high_cycle if high_cycle > max_counts else max_counts
            box_data = {
                "x_type_id": k,
                "low_cycle": low_cycle,
                "low_node": low_node,
                "average": average,
                "high_node": high_node,
                "high_cycle": high_cycle,
            }
            res_dic["data"].append(box_data)
    res_dic["max_counts"] = max_counts

    return res_dic
