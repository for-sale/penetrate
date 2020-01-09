import json
from . import web
from app.models.content import Content
from app.models.base import db
from flask import current_app, Response, request
from .common import PRINTER_TYPE


@web.route('/proportion', methods=["POST"])
def proportion():
    current_app.logger.info("/api-v1/proportion")
    types_counts_dic = {}
    for p_type in PRINTER_TYPE:
        types_counts_dic[p_type] = {"printer_type": p_type, "counts": 0, "percent": 0}

    printer_types = db.session.query(Content.printer_type, db.func.count(Content.id)).group_by(
        Content.printer_type).all()
    total = 0.0
    for pt in printer_types:
        total += pt[1]
        if pt[0] == None or pt[0] == "":
            types_counts_dic["Unknown"]["counts"] += pt[1]
        elif "N1" in pt[0]:
            types_counts_dic["N1"]["counts"] += pt[1]
        elif "N2" in pt[0]:
            types_counts_dic["N2"]["counts"] += pt[1]
        elif pt[0] == "Pro2":
            types_counts_dic["Pro2"]["counts"] += pt[1]
        elif pt[0] == "Pro2 Plus":
            types_counts_dic["Pro2 Plus"]["counts"] += pt[1]

    for k, v in types_counts_dic.items():
        v["percent"] = float("%.2f" % (v["counts"] / total))

    res_dic = {}
    res_dic["data"] = list(types_counts_dic.values())
    return Response(json.dumps(res_dic), mimetype='application/json')
