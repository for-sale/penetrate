from . import web
from flask import request, jsonify
from sqlalchemy import and_
from app.models.content import Content
from app.web.common import str_2_timestamp, str_2_weeks, timestamp_to_str, \
    week_2_day, id_2_type


@web.route('/situation/detail', methods=["POST"])
def situation_detail():
    data = request.json
    # ware_type = data["ware_type"]   # str
    printer_type = data["printer_type"]  # list
    issue_type = data["issue_type"]  # list   issue id

    # ["开始", "结束"]  # 20180203  20180204 -> 时间戳
    report_time = data["report_time"] if "report_time" in data else []
    # 20180203换算成周
    produce_time = data["produce_time"] if "produce_time" in data else []
    # 20180203  20180204
    time_interval = data["time_interval"] if "time_interval" in data else []

    start = data["start"]
    length = data["length"]

    if not printer_type or not issue_type:
        return jsonify({"status": "failed", "msg": "missing required parameters printer type or issue type"}), 200, \
               {'ContentType': 'application/json'}

    if report_time:
        data = report_data(report_time, printer_type, issue_type, start, length)
        return jsonify(data)

    if produce_time:
        data = produce_data(produce_time, printer_type, issue_type, start, length)
        return jsonify(data)

    if time_interval:
        data = interval_data(time_interval, printer_type, issue_type, start, length)
        return jsonify(data)
    # return 'this is a situation test ^_^'

#     # 详情字段
#     detail_data = {
#                 "as_date": "",
#                 "serial_no": "",
#                 "issue": "",
#                 "issue_type": "",
#                 "printer_type": "",
#                 "time_internal": "",
#                 "produce_year": ""
#             }


def get_real_printer_type(printer_type):
    sub_printer_type = list()
    for key in printer_type:
        if key == "Unknown":
            sub_printer_type.append(None)
            continue
        if key == "N2":
            sub_printer_type.extend(["N2S", "N2P(S)", "N2P(D)", "N2(S)", "N2(D)"])
            continue
        if key == "N1":
            sub_printer_type.extend(["N1(D)", "N1(S)"])
            continue
        sub_printer_type.append(key)
    return sub_printer_type


def interval_data(time_interval, printer_type, issue_type, start, length):
    start_year, start_week = str_2_weeks(time_interval[0])
    end_year, end_week = str_2_weeks(time_interval[1])
    start_compare = start_year * 100 + start_week
    end_compare = end_year * 100 + end_week
    content = Content.query.filter(Content.issue_type_id.in_(issue_type),
                                   (Content.produce_year * 100 + Content.as_cycle) > start_compare,
                                   (Content.produce_year * 100 + Content.as_cycle) < end_compare).all()

    res_list = list()
    sub_printer_type = get_real_printer_type(printer_type)
    for data in content:
        if data.printer_type in sub_printer_type:
            sub_dict = {
                    "as_date": timestamp_to_str(data.as_date) if data.as_date else "",
                    "serial_no": data.serial_no if data.serial_no else "",
                    "issue": data.issue_content if data.issue_content else "",
                    "issue_type": id_2_type(data.issue_type_id) if data.issue_type_id else "",
                    "printer_type": data.printer_type if data.printer_type else "Unknown",
                    "time_internal": data.as_cycle if data.as_cycle and data.as_cycle > 0 else "",
                    "produce_year": data.produce_year if data.produce_year else ""
                }
            res_list.append(sub_dict)

    return {"data": res_list[start: start + length], "sum": len(res_list)}


def produce_data(produce_time, printer_type, issue_type, start, length):
    start_year, start_week = str_2_weeks(produce_time[0])
    end_year, end_week = str_2_weeks(produce_time[1])
    start_compare = start_year * 100 + start_week
    end_compare = end_year * 100 + end_week
    content = Content.query.filter(Content.issue_type_id.in_(issue_type),
                                   and_(Content.produce_year * 100 + Content.produce_week) > start_compare,
                                   Content.produce_year * 100 + Content.produce_week < end_compare).all()

    res_list = list()
    sub_printer_type = get_real_printer_type(printer_type)
    for data in content:
        if data.printer_type in sub_printer_type:
            sub_dict = {
                    "as_date": timestamp_to_str(data.as_date) if data.as_date else "",
                    "serial_no": data.serial_no if data.serial_no else "",
                    "issue": data.issue_content if data.issue_content else "",
                    "issue_type": id_2_type(data.issue_type_id) if data.issue_type_id else "",
                    "printer_type": data.printer_type if data.printer_type else "Unknown",
                    "time_internal": data.as_cycle if data.as_cycle else "",
                    "produce_year": data.produce_year if data.produce_year else ""
                }
            res_list.append(sub_dict)

    return {"data": res_list[start: start + length], "sum": len(res_list)}


def report_data(report_time, printer_type, issue_type, start, length):
    start_time = str_2_timestamp(report_time[0])
    end_time = str_2_timestamp(report_time[1])
    content = Content.query.filter(Content.issue_type_id.in_(issue_type),
                                   Content.as_date > start_time,
                                   Content.as_date < end_time).order_by(
                                   Content.as_date.asc()).all()
    res_list = list()
    sub_printer_type = get_real_printer_type(printer_type)
    for data in content:
        if data.printer_type in sub_printer_type:
            sub_dict = {
                    "as_date": timestamp_to_str(data.as_date) if data.as_date else "",
                    "serial_no": data.serial_no if data.serial_no else "",
                    "issue": data.issue_content if data.issue_content else "",
                    "issue_type": id_2_type(data.issue_type_id) if data.issue_type_id else "",
                    "printer_type": data.printer_type if data.printer_type else "Unknown",
                    "time_internal": data.as_cycle if data.as_cycle else "",
                    "produce_year": data.produce_year if data.produce_year else ""
                }
            res_list.append(sub_dict)

    return {"data": res_list[start: start + length], "sum": len(res_list)}
