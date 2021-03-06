from sqlalchemy import Column, VARCHAR, Integer, ForeignKey, DateTime, Integer
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship, backref

from ext import db


class Role(db.Model):
    __tablename__ = "role"
    id = Column(Integer(), autoincrement=True, primary_key=True)
    name = Column(VARCHAR(32), nullable=False)


class Permission(db.Model):
    __tablename__ = "permission"
    id = Column(Integer(), autoincrement=True, primary_key=True)
    name = Column(VARCHAR(32), comment="名称")
    url = Column(VARCHAR(62), comment="前端路由")
    action = Column(VARCHAR(32), comment="增删盖茶")
    description = Column(VARCHAR(32), comment="描述")
    order_field = Column(Integer(), default=1)
    parent_id = db.Column(Integer(), ForeignKey("permission.id", ondelete="CASCADE"))

    child_permissions = relationship("Permission", back_populates="parent_permission", lazy="dynamic")
    parent_permission = relationship("Permission", back_populates="child_permissions", remote_side=[id], lazy="dynamic", uselist=True)


class RolePermission(db.Model):
    __tablename__ = "role_permission"
    id = Column(Integer(), autoincrement=True, primary_key=True)
    role_id = db.Column(Integer(), db.ForeignKey("role.id"))
    permission_id = db.Column(Integer(), db.ForeignKey("permission.id"))

    role = relationship("Role", backref=backref("role_permission", lazy="dynamic"), uselist=False)
    permission = relationship("Permission", backref=backref("role_permission", lazy="dynamic"))


class UserRole(db.Model):
    __tablename__ = "user_role"
    id = Column(Integer(), autoincrement=True, primary_key=True)
    user_id = db.Column(Integer(), db.ForeignKey("user.id"))
    role_id = db.Column(Integer(), db.ForeignKey("role.id"))

    # user = relationship("User", backref=backref("user_role"))
    role = relationship("Role", backref=backref("user_role"))


