from sqlalchemy import Column, String, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from app.models.base import db


class Issue(db.Model):
	__tablename__ = 'as_issue_type'

	id = Column(INTEGER(11), primary_key=True)
	title = Column(String(200), nullable=False, comment='问题类型')
	sort_num = Column(INTEGER(11), nullable=False, comment='排序号')
	type_no = Column(String(100), nullable=False, comment='问题类型编号')
	state = Column(TINYINT(1), nullable=False, server_default=text("'1'"), comment='0停用、1启用')

	def __init__(self, id, title, sort_num, type_no, state):
		self.id = id
		self.title = title
		self.sort_num = sort_num
		self.type_no = type_no
		self.state = state

	# def __repr__(self):
	# 	return "title".format(self.title)
