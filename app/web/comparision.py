from . import web
import json
from flask import request, Response, current_app
from app.models.content import Content
from app.web.common import id_2_type


@web.route('/comparision', methods=["POST"])
def comparision():
    data = request.json
    printer_type = data["printer_type"]  # str    single type
    issue_type = data["issue_type"]  # list   issue id
    # compare_week = data["compare_week"]  # [20180203  20180204]
    former_interval = data["former_interval"]
    after_interval = data["after_interval"]
    if not all([printer_type, issue_type, former_interval, after_interval]):
        current_app.logger.error("printer_type or issue_type error or compare_week error, return []")
        return Response(json.dumps([]), mimetype='application/json')

    data = comparision_data(printer_type, issue_type, former_interval, after_interval)
    return Response(json.dumps(data), mimetype='application/json')


def comparision_data(printer_type, issue_type, former_interval, after_interval):

    try:

        former_data, former_flag = get_comparision_data(printer_type, issue_type, former_interval)
        after_data, after_flag = get_comparision_data(printer_type, issue_type, after_interval)

        if not all([former_flag, after_flag]):
            return []

        final_list = list()
            # ""2018-01-2018-45","
        former = former_interval[0] + "weeks" + "~" + former_interval[1] + "weeks"
        after = after_interval[0] + "weeks" + "~" + after_interval[1] + "weeks"
        for issue_id in issue_type:
            final_list.append({"week": former, "id": int(issue_id), "value": former_data[int(issue_id)]})
            final_list.append({"week": after, "id": int(issue_id), "value": after_data[int(issue_id)]})

        return final_list
    except Exception as e:
        current_app.logger.error(e)
        return []


def get_comparision_data(printer_type, issue_type, time_interval):
    interval_f = time_interval[0]
    interval_a = time_interval[1]
    f_year, f_week = str_2_weeks(interval_f)
    a_year, a_week = str_2_weeks(interval_a)
    start_compare = f_year * 100 + f_week
    end_compare = a_year * 100 + a_week
    if start_compare == end_compare:
        start_compare -= 1
        end_compare += 1
    # content = None
    real_type = get_real_printer_type(printer_type)
    try:

        content = Content.query.filter(Content.issue_type_id.in_(issue_type),
                                       (Content.produce_year * 100 + Content.produce_week) > start_compare,
                                       (Content.produce_year * 100 + Content.produce_week) < end_compare).all()
    except Exception as e:
        current_app.logger.error("select comparision data error, args: printer_type:{}, "
                                 "issue_type:{}, compare  time_interval:{}".format(
                                    printer_type, issue_type, time_interval))
        raise e
    # {
    #     issue_type1_id : 3,
    #     issue_type2_id : 5
    # }
    res_dict = dict()
    for issue in issue_type:
        res_dict.update({int(issue): 0})

    flag = False
    if content:
        for data in content:
            # 放到同类型下面
            issue_type_id = data.issue_type_id
            if issue_type_id:
                if data.printer_type in real_type:
                    res_dict[issue_type_id] += 1
                    flag = True
    return res_dict, flag


def issue_to_str(issue_type):
    new_issue_list = list()
    for issue_id in issue_type:
        new_issue_list.append(id_2_type(issue_id))
    return new_issue_list


def check_args(data):
    if "printer_type" not in data:
        return False
    if "issue_type" not in data:
        return False
    if "compare_week" not in data:
        return False

    if not isinstance(data["printer_type"], str):
        return False
    if not isinstance(data["issue_type"], list):
        return False
    if not isinstance(data["compare_week"], list or len(data["compare_week"] != 2)):
        return False


def str_2_weeks(str_time):
    year = str_time[0:4]
    week = str_time[5:]
    return int(year), int(week)


def get_real_printer_type(printer_type):
    printer_list = list()
    for printer in printer_type:
        if printer == "N2":
            printer_list.extend(["N2S", "N2P(S)", "N2P(D)", "N2(S)", "N2(D)"])
        if printer == "N1":
            printer_list.extend(["N1(D)", "N1(S)"])
        if printer == "Unknown":
            printer_list.extend(["", None])
        if printer == "Pro2 Plus":
            printer_list.append(printer)
        if printer == "Pro2":
            printer_list.append(printer)
    return printer_list
