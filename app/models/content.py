from sqlalchemy import Column, DateTime, ForeignKey, String, Text, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, LONGTEXT, TINYINT
from sqlalchemy.orm import relationship
from app.models.base import db
from app.models.issue import Issue
from app.models.setting import Setting


class Content(db.Model):
    __tablename__ = 'as_content'

    id = Column(INTEGER(11), primary_key=True, comment='序号id')
    produce_year = Column(INTEGER(5), comment='生产年')
    produce_week = Column(TINYINT(2), comment='生产周')
    produce_month = Column(TINYINT(2), comment='生产月')
    as_date = Column(BIGINT(20), comment='售后日期')
    as_week = Column(TINYINT(2), comment='售后周')
    as_cycle = Column(INTEGER(11), comment='售后周期')
    serial_no = Column(String(40), comment='序列号')
    partner_id = Column(ForeignKey('as_setting.id'), index=True, comment='第三方名称')
    case_no = Column(String(20))
    country = Column(String(100), comment='国家')
    issue_type_id = Column(ForeignKey('as_issue_type.id'), index=True, comment='问题类型id')
    issue_title = Column(String(2000), comment='问题名称')
    issue_content = Column(LONGTEXT, comment='问题具体内容')
    maintenance_id = Column(ForeignKey('as_setting.id'), index=True, comment='服务方式')
    printer_type = Column(String(100), comment='打印机类型')
    solution = Column(LONGTEXT, comment='解决内容')
    status_id = Column(ForeignKey('as_setting.id'), index=True, comment='售后状态id')
    completed = Column(TINYINT(1), nullable=False, server_default=text("'0'"), comment='是否完整')
    created = Column(DateTime, nullable=False, comment='创建时间')
    issue_content_imgs = Column(Text, comment='问题详情图片')
    solution_imgs = Column(Text, comment='解决详情图片')

    issue_type = relationship(Issue)
    maintenance = relationship(Setting, primaryjoin=(maintenance_id == Setting.id))
    partner = relationship(Setting, primaryjoin=(partner_id == Setting.id))
    status = relationship(Setting, primaryjoin=(status_id == Setting.id))

    def __init__(self, id, produce_year, produce_week, produce_month, as_date, as_week, as_cycle,
                 serial_no, partner_id, case_no, country, issue_type_id, issue_title, issue_content,
                 maintenance_id, printer_type, solution, status_id, completed, created, issue_content_imgs,
                 solution_imgs):
        self.id = id
        self.produce_year = produce_year
        self.produce_week = produce_week
        self.produce_month = produce_month
        self.as_date = as_date
        self.as_week = as_week
        self.as_cycle = as_cycle
        self.serial_no = serial_no
        self.partner_id = partner_id
        self.case_no = case_no
        self.country = country
        self.issue_type_id = issue_type_id
        self.issue_title = issue_title
        self.issue_content = issue_content
        self.maintenance_id = maintenance_id
        self.printer_type = printer_type
        self.solution = solution
        self.status_id = status_id
        self.completed = completed
        self.created = created
        self.issue_content_imgs = issue_content_imgs
        self.solution_imgs = solution_imgs

    # def __repr__(self):
# 	return "title".format(self.id)
