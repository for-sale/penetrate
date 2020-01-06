from app.models.base import db
from sqlalchemy import Column, String, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT


class Setting(db.Model):
    __tablename__ = 'as_setting'

    id = Column(INTEGER(11), primary_key=True, comment='主键id')
    title = Column(String(100), nullable=False, comment='第三方')
    sort_num = Column(INTEGER(11), nullable=False, comment='排序号')
    type = Column(TINYINT(1), nullable=False, server_default=text("'1'"),
                  comment='1Partner、2Maintenance Method、3Status')
    state = Column(TINYINT(1), nullable=False, server_default=text("'1'"), comment='0停用、1启用')

