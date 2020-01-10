import json
from . import web
from app.models.content import Content
from app.models.base import db
from flask import current_app, Response
from .common import PRINTER_TYPE
from .utils import type_sorted
from pandas import DataFrame


@web.route("/top_type", methods=["POST"])
def top_type():
    try:
        sorted_type_id = type_sorted()[0:3]
    except Exception as e:
        current_app.logger.error("top_type, select sorted_type_id data error")
        raise e

    top_type_dic = dict()
    for type_id in sorted_type_id:
        total = 0
        types_counts_dic = {}
        for p_type in PRINTER_TYPE:
            types_counts_dic.update({p_type: {"printer_type": p_type, "counts": 0, "percent": 0}})

        top_type_dic[type_id] = types_counts_dic
        try:
            issue_type = db.session.query(Content.printer_type, db.func.count(Content.id)).filter(
                Content.issue_type_id == type_id).group_by(Content.printer_type).all()
        except Exception as e:
            current_app.logger.error("select top_type data error, args: type_id:{}".format(type_id))
            raise e

        for res in issue_type:
            total += res[1]
            if res[0] is None or res[0] == "":
                top_type_dic[type_id]["Unknown"]["counts"] += res[1]
            elif "N1" in res[0]:
                top_type_dic[type_id]["N1"]["counts"] += res[1]
            elif "N2" in res[0]:
                top_type_dic[type_id]["N2"]["counts"] += res[1]
            elif res[0] == "Pro2":
                top_type_dic[type_id]["Pro2"]["counts"] += res[1]
            elif res[0] == "Pro2 Plus":
                top_type_dic[type_id]["Pro2 Plus"]["counts"] += res[1]
        for v in top_type_dic[type_id].values():
            v["percent"] = float("%.2f" % (v["counts"] / total))

    res_dic = {"data": []}
    index = 0
    for k, v in top_type_dic.items():
        t_dic = {"id": k, "index": index, "counts": list(v.values())}
        res_dic["data"].append(t_dic)
        index += 1
    return Response(json.dumps(res_dic), mimetype='application/json')


@web.route("/top_type_detail", methods=["POST"])
def top_type_data():
    try:
        sorted_type_id = type_sorted()[0:3]
    except Exception as e:
        current_app.logger.error("top_type_detail, select sorted_type_id data error")
        raise e

    top_type_dic = {}

    for type_id in sorted_type_id:
        total = 0
        top_type_dic.update({type_id: {"Unknown": 0}})
        try:
            issue_type = db.session.query(Content.printer_type, db.func.count(Content.id)).filter(
                Content.issue_type_id == type_id).group_by(Content.printer_type).all()
        except Exception as e:
            current_app.logger.error("select top_type_detail data error, args: type_id:{}".format(type_id))
            raise e
        for res in issue_type:
            total += res[1]
            if res[0] is None or res[0] == "":
                top_type_dic[type_id]["Unknown"] += res[1]
            else:
                top_type_dic[type_id][res[0]] = res[1]

    df = DataFrame(top_type_dic)
    df.loc['category_counts'] = df.apply(lambda x: x.sum())
    df.sort_values(by='category_counts', axis=1, inplace=True, ascending=False)
    c_l = df.columns.values.tolist()
    res_dic = {"data": [], "printerTypes": df.index.values.tolist()}
    for i_index, i_counts in enumerate(c_l):
        df[i_counts].fillna(0, inplace=True)
        l_dic = {"id": i_counts, "index": i_index, "counts": df[i_counts].tolist()}
        res_dic["data"].append(l_dic)
    return Response(json.dumps(res_dic), mimetype='application/json')


@web.route("/order_type_id", methods=["POST"])
def order_type_id():
    try:
        sorted_type_id = type_sorted()
    except Exception as e:
        current_app.logger.error("order_type_id, select sorted_type_id data error")
        raise e
    res_dic = dict()
    res_dic["data"] = sorted_type_id
    return Response(json.dumps(res_dic), mimetype='application/json')
