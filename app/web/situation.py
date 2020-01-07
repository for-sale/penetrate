from . import web
from flask import request, jsonify
from sqlalchemy import and_
from app.models.content import Content
from app.web.common import str_2_timestamp, str_2_weeks, timestamp_to_str, week_2_day


@web.route('/situation', methods=["POST"])
def situation():
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

    if not printer_type or not issue_type:
        return jsonify({"status": "failed", "msg": "missing required parameters printer type or issue type"}), 200, \
               {'ContentType': 'application/json'}

    if report_time:
        data = report_data(report_time, printer_type, issue_type)
        return jsonify(data)

    if produce_time:
        data = produce_data(produce_time, printer_type, issue_type)
        return jsonify(data)

    if time_interval:
        data = interval_data(time_interval, printer_type, issue_type)
        return jsonify(data)
    # return 'this is a situation test ^_^'


def interval_data(time_interval, printer_type, issue_type):
    start_year, start_week = str_2_weeks(time_interval[0])
    end_year, end_week = str_2_weeks(time_interval[1])
    start_compare = start_year * 100 + start_week
    end_compare = end_year * 100 + end_week
    content = Content.query.filter(Content.issue_type_id.in_(issue_type),
                                   and_(Content.produce_year * 100 + Content.as_cycle) > start_compare,
                                   Content.produce_year * 100 + Content.as_cycle < end_compare).all()

    # 确定筛选的打印机类型
    printer_dict = dict()
    for printer in printer_type:
        printer_dict.update({printer: {}})

    for data in content:
        # 放到同类型下
        cur_type = data.printer_type
        as_cycle = data.as_cycle
        if cur_type in printer_dict.keys():
            if as_cycle:
                cur_date = str(data.produce_year * 100 + data.as_cycle)
                if cur_date in printer_dict[cur_type].keys():
                    printer_dict[cur_type][cur_date] += 1
                else:
                    printer_dict[cur_type][cur_date] = 1

        if cur_type is None and "Unknown" in printer_dict.keys():
            if as_cycle:
                cur_date = str(data.produce_year * 100 + data.as_cycle)
                if cur_date in printer_dict["Unknown"].keys():
                    printer_dict["Unknown"][cur_date] += 1
                else:
                    printer_dict["Unknown"][cur_date] = 1

    # 获取所有可能的键值
    effective_key = set()
    for key in printer_dict.keys():
        effective_key = effective_key | set(printer_dict[key].keys())
    print(effective_key)

    # 键值赋值
    new_printer_dict = printer_dict
    empty_printer_type = list()
    for cur_printer_type in printer_dict:
        cur_printer_data = printer_dict[cur_printer_type]
        if cur_printer_data:
            for date, value in cur_printer_data.items():
                new_printer_dict[cur_printer_type][date] = value
            # 不在的加进来
            for date in effective_key:
                if date not in new_printer_dict[cur_printer_type].keys():
                    new_printer_dict[cur_printer_type][date] = 0
        else:
            empty_printer_type.append(cur_printer_type)
    for empty_type in empty_printer_type:
        for date in effective_key:
            new_printer_dict[empty_type][date] = 0

    # 格式化数据
    data_list = []
    for cur_printer_type in new_printer_dict:
        if new_printer_dict[cur_printer_type]:
            for date, value in new_printer_dict[cur_printer_type].items():
                cur_dict = {"type": cur_printer_type, "date": date, "value": value}
                data_list.append(cur_dict)
    return data_list


def produce_data(produce_time, printer_type, issue_type):
    start_year, start_week = str_2_weeks(produce_time[0])
    end_year, end_week = str_2_weeks(produce_time[1])
    start_compare = start_year * 100 + start_week
    end_compare = end_year * 100 + end_week
    content = Content.query.filter(Content.issue_type_id.in_(issue_type),
                                   and_(Content.produce_year * 100 + Content.produce_week) > start_compare,
                                   Content.produce_year * 100 + Content.produce_week < end_compare).all()

    # 确定筛选的打印机类型
    printer_dict = dict()
    for printer in printer_type:
        printer_dict.update({printer: {}})

    for data in content:
        # 放到同类型下
        cur_type = data.printer_type
        serial_no = data.serial_no
        if cur_type in printer_dict.keys():
            if serial_no:
                cur_date = week_2_day(serial_no)
                if cur_date in printer_dict[cur_type].keys():
                    printer_dict[cur_type][cur_date] += 1
                else:
                    printer_dict[cur_type][cur_date] = 1

        if cur_type is None and "Unknown" in printer_dict.keys():
            if serial_no:
                cur_date = week_2_day(serial_no)
                if cur_date in printer_dict["Unknown"].keys():
                    printer_dict["Unknown"][cur_date] += 1
                else:
                    printer_dict["Unknown"][cur_date] = 1

    # 获取所有可能的键值
    effective_key = set()
    for key in printer_dict.keys():
        effective_key = effective_key | set(printer_dict[key].keys())
    print(effective_key)

    # 键值赋值
    new_printer_dict = printer_dict
    empty_printer_type = list()
    for cur_printer_type in printer_dict:
        cur_printer_data = printer_dict[cur_printer_type]
        if cur_printer_data:
            for date, value in cur_printer_data.items():
                new_printer_dict[cur_printer_type][date] = value
            # 不在的加进来
            for date in effective_key:
                if date not in new_printer_dict[cur_printer_type].keys():
                    new_printer_dict[cur_printer_type][date] = 0
        else:
            empty_printer_type.append(cur_printer_type)
    for empty_type in empty_printer_type:
        for date in effective_key:
            new_printer_dict[empty_type][date] = 0

    # 格式化数据
    data_list = []
    for cur_printer_type in new_printer_dict:
        if new_printer_dict[cur_printer_type]:
            for date, value in new_printer_dict[cur_printer_type].items():
                cur_dict = {"type": cur_printer_type, "date": date, "value": value}
                data_list.append(cur_dict)
    return data_list


def report_data(report_time, printer_type, issue_type):
    start_time = str_2_timestamp(report_time[0])
    end_time = str_2_timestamp(report_time[1])
    content = Content.query.filter(Content.issue_type_id.in_(issue_type),
                                   Content.as_date > start_time,
                                   Content.as_date < end_time).all()

    # for data in content:
    #     print(data.printer_type)

    # 确定筛选的打印机类型
    printer_dict = dict()
    for printer in printer_type:
        printer_dict.update({printer: {}})

    # printer_dict_tmp = {
    #     "Pro2": {
    #         "20180101": 3,
    #         "20180102": 5,
    #         "20180103": 6
    #     },
    #     "N2": {
    #         "20180101": 3,
    #         "20180102": 5,
    #         "20180103": 6
    #     }
    #     }

    # {
    #     "type": "pro2", "date": "201802", "value": 3,
    #     "type": "pro2", "date": "201803", "value": 1,
    # }

    for data in content:
        # 放到同类型下
        cur_type = data.printer_type
        if cur_type in printer_dict.keys():
            if data.as_date:
                cur_date = timestamp_to_str(data.as_date)
                if cur_date in printer_dict[cur_type].keys():
                    printer_dict[cur_type][cur_date] += 1
                else:
                    printer_dict[cur_type][cur_date] = 1

        if cur_type is None and "Unknown" in printer_dict.keys():
            if data.as_date:
                cur_date = timestamp_to_str(data.as_date)
                if cur_date in printer_dict["Unknown"].keys():
                    printer_dict["Unknown"][cur_date] += 1
                else:
                    printer_dict["Unknown"][cur_date] = 1

    # 获取所有可能的键值
    effective_key = set()
    for key in printer_dict.keys():
        effective_key = effective_key | set(printer_dict[key].keys())
    print(effective_key)

    # 键值赋值
    new_printer_dict = printer_dict
    empty_printer_type = list()
    for cur_printer_type in printer_dict:
        cur_printer_data = printer_dict[cur_printer_type]
        if cur_printer_data:
            for date, value in cur_printer_data.items():
                new_printer_dict[cur_printer_type][date] = value
            # 不在的加进来
            for date in effective_key:
                if date not in new_printer_dict[cur_printer_type].keys():
                    new_printer_dict[cur_printer_type][date] = 0
        else:
            empty_printer_type.append(cur_printer_type)
    for empty_type in empty_printer_type:
        for date in effective_key:
            new_printer_dict[empty_type][date] = 0

    # 格式化数据
    data_list = []
    for cur_printer_type in new_printer_dict:
        if new_printer_dict[cur_printer_type]:
            for date, value in new_printer_dict[cur_printer_type].items():
                cur_dict = {"type": cur_printer_type, "date": date, "value": value}
                data_list.append(cur_dict)
    return data_list


# @web.route('/situation/detail', methods=["POST"])
# def situation_detail():
#
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

# @web.route('/situation')
# def situation():
#     # res = Issue.query.all()
#     # user = Issue.query.filter_by(id=2).first()
#     content = Content.query.filter_by(id=2).first()
#     #
#     # Content.query.join(followers, (followers.c.followed_id == Post.user_id))
#     print(content.as_date)
#     current_app.logger.info("this is log ...22222")
#
#     # 软硬件筛选
#     content = Content.query.filter(Content.printer_type.in_(["Pro2", "Pro2 Plus"])).all()
#     # Content.printer_type in )
#     print(content)
#
#     # logger.info("get user data success ...".format(content.as_date))
#     return 'this is a situation test ^_^'

    # if produce_time or time_interval:
    #     start_year, start_week = str_2_weeks(produce_time[0])
    #     end_year, end_week = str_2_weeks(produce_time[1])
    #     start_compare = start_year * 100 + start_week
    #     end_compare = end_year * 100 + end_week
    #     content = Content.query.filter(Content.printer_type.in_([""]),
    #                                    Content.issue_type_id.in_(issue_type),
    #                                    and_(Content.produce_year * 100 + Content.produce_week) > start_compare,
    #                                    Content.produce_year * 100 + Content.produce_week < end_compare).order_by(
    #                                    Content.as_date.asc()).all()
    #     for key in content:
    #         print(key.as_date)

    # if time_interval:
    #     start_year, start_week = str_2_weeks(produce_time[0])
    #     end_year, end_week = str_2_weeks(produce_time[1])
    #     content = Content.query.filter(Content.printer_type.in_(printer_type),
    #                                    Content.issue_type_id.in_(issue_type),
    #                                    and_(Content.produce_year * 1000))

    # content = Content.query.filter(Content.printer_type.in_(["Pro2", "Pro2 Plus"]),
    #                                Content.issue_type_id.in_([3, 4]),
    #                                Content.as_date > 1523376000000,
    #                                or_(and_(Content.produce_year > 2018, Content.produce_week > 10),
    #                                    Content.produce_year > 2019),
    #                                Content.as_cycle > 5).all()
    # print(content)

    # # 格式化数据
    # data_list = []
    # for cur_printer_type in printer_dict:
    #     if printer_dict[cur_printer_type]:
    #         for date, value in printer_dict[cur_printer_type].items():
    #             cur_dict = {"type": cur_printer_type, "date": date, "value": value}
    #             data_list.append(cur_dict)
    #     # else:
    #     #     cur_dict = {"type": cur_printer_type, "date": "", "value": 0}
    #     #     data_list.append(cur_dict)