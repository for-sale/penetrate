from app.models.content import Content
from app.models.base import db
from .common import SOFTWARE_ID


# @web.before_request
# @web.before_app_first_request
def type_sorted():
    printer_types = db.session.query(Content.issue_type_id).group_by(Content.issue_type_id).order_by(
        db.desc(db.func.count(Content.id))).all()
    # printer_types = db.session.query(Content.issue_type_id).filter(Content.issue_type_id.notin_(SOFTWARE_ID)).group_by(Content.issue_type_id).order_by(db.desc(db.func.count(Content.id))).all()
    sorted_type_id = []
    for p_type in printer_types:
        sorted_type_id.append(p_type[0])
    return sorted_type_id

# @web.errorhandler(400)
# def error(msg):
#     current_app.logger.error(msg)
#     return '400'
