from . import web
import json
from flask import request, Response, current_app


@web.route('/tag', methods=["POST"])
def add_tag():
    data = request.json
    tag_time = data["tag_time"]  # str    single type
    tag_name = data["tag_name"]  # list   issue id
    if not all([tag_name, tag_time]):
        return Response(json.dumps({"status": "failed"}), mimetype='application/json')

    # tag 写入文件
    tag_path = current_app.config.get("TAG_PATH")

    # 判断是否已经存在
    tag_list = get_tag_data()
    for data in tag_list:
        if data["tag_time"] == tag_time:
            return Response(json.dumps({"status": "tag time exists"}), mimetype='application/json')

    tag = {"tag_time": tag_time, "tag_name": tag_name}
    try:
        with open(tag_path, "a+") as f:
            f.write(json.dumps(tag))
            f.write("\n")
    except ValueError as e:
        current_app.logger.error("write file value error")
        pass

    except IOError as e:
        current_app.logger.error("write file io error")
        pass

    return Response(json.dumps({"status": "success"}), mimetype='application/json')


def get_tag_data():
    tag_path = current_app.config.get("TAG_PATH")
    res_dict = list()
    try:
        with open(tag_path, "r") as f:
            lines = f.readlines()
            for line in lines:
                tag = line.strip("\n")
                res_dict.append(json.loads(tag))
        return res_dict
    except ValueError as e:
        current_app.logger.error("write file value error")
        return []

    except IOError as e:
        current_app.logger.error("write file io error")
        return []


@web.route('/tag', methods=["GET"])
def get_tag():
    tag = get_tag_data()
    return Response(json.dumps({"data": tag}), mimetype='application/json')


@web.route('/tag', methods=["DELETE"])
def delete_tag():
    data = request.json
    tag_time = data["tag_time"]  # str    single type
    if not tag_time:
        return Response(json.dumps({"status": "failed"}), mimetype='application/json')

    tag_path = current_app.config.get("TAG_PATH")
    # list
    new_tag_list = []
    tag = get_tag_data()
    if tag:
        for data in tag:
            #   data = {"tag_time": "20200113", "tag_name": "first"}
            if data["tag_time"] == tag_time:
                continue
            else:
                new_tag_list.append(data)

    try:
        with open(tag_path, "w") as f:
            for line in new_tag_list:
                f.write(json.dumps(line))
                f.write("\n")
    except ValueError as e:
        current_app.logger.error("write file value error")
        raise e

    except IOError as e:
        current_app.logger.error("write file io error")
        raise e
    return Response(json.dumps({"status": "success"}), mimetype='application/json')
