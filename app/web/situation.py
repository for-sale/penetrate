from . import web
import time
from flask import current_app, request, jsonify
from sqlalchemy import or_, and_
from app.models.content import Content
from app.web.common import str_2_timestamp, str_2_weeks
from app.lib.issue_type import type_to_id


@web.route('/situation', methods=["POST"])
def situation():
    data = request.json
    # ware_type = data["ware_type"]   # str
    printer_type = data["printer_type"]   # list
    issue_type = data["issue_type"]   # list
    report_time = data["report_time"]   # ["开始", "结束"]  # 20180203  20180204
    produce_time = data["produce_time"]  # 20180203换算成周
    time_interval = data["time_interval"]   # 20180203  20180204

    if not printer_type or not issue_type:
        return jsonify({"status": "failed", "msg": "missing required parameters printer type or issue type"}), 200, \
               {'ContentType': 'application/json'}

    issue_id = type_to_id(issue_type)

    if report_time:
        start_time = str_2_timestamp(report_time[0])
        end_time = str_2_timestamp(report_time[1])
        content = Content.query.filter(Content.printer_type.in_(printer_type),
                                       Content.issue_type_id.in_(issue_id),
                                       Content.as_date > start_time,
                                       Content.as_date < end_time).all()

    if produce_time:
        start_year, start_week = str_2_weeks(produce_time[0])
        end_year, end_week = str_2_weeks(produce_time[1])
        content = Content.query.filter(Content.printer_type.in_(printer_type),
                                       Content.issue_type_id.in_(issue_id),
                                       or_(and_(Content.produce_year > 2018, Content.produce_week > 10),
                                           Content.produce_year > 2019),
                                       Content.as_cycle > 5).all()




    content = Content.query.filter(Content.printer_type.in_(["Pro2", "Pro2 Plus"]),
                                   Content.issue_type_id.in_([3, 4]),
                                   Content.as_date > 1523376000000,
                                   or_(and_(Content.produce_year > 2018, Content.produce_week > 10),
                                       Content.produce_year > 2019),
                                   Content.as_cycle > 5).all()
    print(content)
    return 'this is a situation test ^_^'




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
#     # res = db.session.query(Setting.title, db.func.count(Content.id)).join(Setting, (Content.status_id == Setting.id),
#     #                                                                       isouter=True).group_by(
#     #     Content.status_id).all()


def str_to_timestamp(time_str):
    # 2018-09-02
    time_stamp = time.mktime(time.strptime(time_str, '%Y-%m-%d'))

# def timestamp_2_str(time_str):


def hardware_or_software(data):
    # 软硬件筛选
    content = Content.query.filter((Content.printer_type._in == "Pro2", Content.printer_type == "Pro2 Plus")).all()
    # Content.printer_type in )
    print(content)


def issue_type(data):
    # 故障类型筛选
    pass


def machine_type(data):
    # 机器类型筛选
    pass


def report_time(data):
    # 上报时间
    pass


def product_time(data):
    # 生产时间
    pass


def time_interval(data):
    # 时间间隔
    pass


# def