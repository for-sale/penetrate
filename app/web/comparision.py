from . import web
import json
from flask import request, Response, current_app
from app.models.content import Content
from app.web.common import str_2_weeks, id_2_type


@web.route('/comparision', methods=["POST"])
def comparision():
    data = request.json
    printer_type = data["printer_type"]  # str    single type
    issue_type = data["issue_type"]  # list   issue id
    compare_week = data["compare_week"]  # [20180203  20180204]
    if not printer_type or not issue_type or not compare_week:
        data = {"status": "failed", "msg": "missing required parameters printer type or issue type"}
        return Response(json.dumps(data), mimetype='application/json')

    data = comparision_data(printer_type, issue_type, compare_week)
    return Response(json.dumps(data), mimetype='application/json')


def comparision_data(printer_type, issue_type, compare_week):

    try:
        former_week = compare_week[0]
        after_week = compare_week[1]

        former_data = get_comparision_data(printer_type, issue_type, former_week)
        after_data = get_comparision_data(printer_type, issue_type, after_week)

        final_list = list()
        f_year, f_weeks = str_2_weeks(former_week)
        af_year, af_weeks = str_2_weeks(after_week)

        if f_weeks < 10:
            f_weeks = "0" + str(f_weeks)
        if af_weeks < 10:
            af_weeks = "0" + str(af_weeks)
        former = "{}-{}".format(f_year, f_weeks)
        after = "{}-{}".format(af_year, af_weeks)
        for issue_id in issue_type:
            final_list.append({"week": former, "id": int(issue_id), "value": former_data[int(issue_id)]})
            final_list.append({"week": after, "id": int(issue_id), "value": after_data[int(issue_id)]})

        return final_list
    except Exception as e:
        current_app.logger.error(e)
        return []


def get_comparision_data(printer_type, issue_type, compare_week):
    year, week = str_2_weeks(compare_week)
    content = None
    try:
        if printer_type in ["Pro2", "Pro2 Plus", "Unknown"]:
            if printer_type == "Unknown" or printer_type == "":
                sub_printer_type = None
            else:
                sub_printer_type = printer_type
            content = Content.query.filter(Content.printer_type == sub_printer_type,
                                           Content.issue_type_id.in_(issue_type),
                                           Content.produce_year == year,
                                           Content.produce_week == week).all()
        if printer_type in ["N2", "N1"]:
            if printer_type == "N2":
                sub_printer_type = ["N2S", "N2P(S)", "N2P(D)", "N2(S)", "N2(D)"]
            else:
                sub_printer_type = ["N1(D)", "N1(S)"]
            content = Content.query.filter(Content.printer_type.in_(sub_printer_type),
                                           Content.issue_type_id.in_(issue_type),
                                           Content.produce_year == year,
                                           Content.produce_week == week).all()
    except Exception as e:
        current_app.logger.error("select comparision data error, args: printer_type:{}, "
                                 "issue_type:{}, compare_week:{}".format(
                                    printer_type, issue_type, compare_week))
        raise e
    # {
    #     issue_type1_id : 3,
    #     issue_type2_id : 5
    # }
    res_dict = dict()
    for issue in issue_type:
        res_dict.update({int(issue): 0})

    if content:
        for data in content:
            # 放到同类型下面
            issue_type_id = data.issue_type_id
            if issue_type_id:
                res_dict[issue_type_id] += 1
    return res_dict


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
