#   蓝图初始化操作
from flask import Blueprint, render_template

web = Blueprint('web', __name__, url_prefix="/api-v1")


# @web.app_errorhandler(404)
# def not_found(e):
#     return render_template('404.jinja')


from . import situation
