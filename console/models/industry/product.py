# coding: utf-8
from ..base import *
from sqlalchemy.orm import backref
from sqlalchemy.ext.declarative import declared_attr
from datetime import datetime
from enum import Enum


class ProductMixin:
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    # 名称 and 等级
    name = db.Column(db.String(68), index=True)
    level = db.Column(db.Integer, index=True, nullable=False, default=0)
    name_number = db.Column(db.String(32), default=0)  # 编号

    # 配置文件名称
    config_name = db.Column(db.String(32))

    first_time = db.Column(db.DateTime, default=datetime.now)
    last_time = db.Column(db.DateTime, default=datetime.now)

    @declared_attr
    def user_id(cls):
        return db.Column(db.Integer, db.ForeignKey('users.id'))

    @declared_attr
    def user(cls):
        return db.relationship('User', backref=backref("product", cascade="all,delete"))


class ProductRelationMixin:
    __tablename__ = 'product_relation'
    id = db.Column(db.Integer, primary_key=True)

    # 名称 and 等级
    name = db.Column(db.String(32))
    level = db.Column(db.Integer, index=True, nullable=False, default=1)
    number = db.Column(db.Integer, default=1)  # id
    name_number = db.Column(db.String(32), index=True)  # 编号

    # todo delete
    timestamp = db.Column(db.DateTime, default=datetime.now)

    parent_id = db.Column(db.Integer, index=True)

    relation_order = db.Column(db.Integer, default=0)

    @declared_attr
    def product_id(cls):
        return db.Column(db.Integer, db.ForeignKey('product.id'))

    @declared_attr
    def product(cls):
        return db.relationship('Product', backref=backref("product_relation", cascade="all, delete-orphan"))


class FuncRelationMixin:
    __tablename__ = 'func_relation'
    id = db.Column(db.Integer, primary_key=True)

    @declared_attr
    def product_relation_id(cls):
        return db.Column(db.Integer, db.ForeignKey('product_relation.id'))

    @declared_attr
    def product_id(cls):
        return db.Column(db.Integer, db.ForeignKey('product.id'))

    name = db.Column(db.String(64))
    number = db.Column(db.Integer, default=1)  # 插入顺序
    name_number = db.Column(db.String(32), index=True)  # 编号

    timestamp = db.Column(db.DateTime, default=datetime.now)

    type = db.Column(db.String(32), default='func')

    parent_id = db.Column(db.Integer)

    @declared_attr
    def product_relation(cls):
        return db.relationship('ProductRelation',
                               backref=db.backref('func_relation', lazy='dynamic', cascade='all, delete-orphan'))

    @declared_attr
    def product(cls):
        return db.relationship('Product', backref=backref("func_relation", cascade="all, delete-orphan"))


class AttrType(Enum):
    structure = '结构树'
    func = '功能树'
    failure = '失效树'


class AttrMixin:
    __tablename__ = 'attr'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(16))
    level = db.Column(db.Integer, default=-1)
    type = db.Column(db.Enum(AttrType))

    update_time = db.Column(db.DateTime, default=datetime.now)

    content = db.Column(db.Text)
    real_content = db.Column(db.Text)
    username = db.Column(db.String(12), default='系统')

    extra = db.Column(db.Boolean, default=False)
    name_number = db.Column(db.String(32))


class AttrOtherMixin:
    __tablename__ = 'attr_action'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(16))

    update_time = db.Column(db.DateTime, default=datetime.now)

    content = db.Column(db.Text)


class AttrContentMixin:
    __tablename__ = 'attr_content'
    id = db.Column(db.Integer, primary_key=True)

    real_content = db.Column(db.Text)

    # func | failuer | structure
    level = db.Column(db.Integer, default=-1)
    type = db.Column(db.Enum(AttrType))

    name_number = db.Column(db.String(32))

    @declared_attr
    def product_id(cls):
        return db.Column(db.Integer, db.ForeignKey('product.id'))

    @declared_attr
    def product(cls):
        return db.relationship('Product', backref=backref("attr_content", cascade="all, delete-orphan"))


class ProductAssessMixin:
    __tablename__ = 'product_assess'
    id = db.Column(db.Integer, primary_key=True)

    content = db.Column(db.Text)

    type = db.Column(db.String(32))  # current | optimize
    action_type = db.Column(db.String(32))  # preventive_action | probe_action

    @declared_attr
    def func_relation_id(cls):
        return db.Column(db.Integer, db.ForeignKey('func_relation.id'))

    @declared_attr
    def func_relation(cls):
        return db.relationship('FuncRelation', backref=backref("assess", cascade="all, delete-orphan"))

    @declared_attr
    def product_id(cls):
        return db.Column(db.Integer, db.ForeignKey('product.id'))

    @declared_attr
    def product(cls):
        return db.relationship('Product', backref=backref("assess", cascade="all, delete-orphan"))


class ProductTreeMixin:
    __tablename__ = 'product_tree_edit'
    id = db.Column(db.Integer, primary_key=True)

    @declared_attr
    def product_relation_id(cls):
        return db.Column(db.Integer, db.ForeignKey('product_relation.id'))

    content = db.Column(db.Text)
    type = db.Column(db.String(32))

    is_show = db.Column(db.Boolean, default=False)

    update_time = db.Column(db.DateTime, default=datetime.now)

    @declared_attr
    def func_id(cls):
        return db.Column(db.Integer, db.ForeignKey('func_relation.id'))

    @declared_attr
    def func(cls):
        return db.relationship('FuncRelation', backref=backref("product_tree_edit", cascade="all, delete-orphan"))

    @declared_attr
    def product_relation(cls):
        return db.relationship('ProductRelation',
                               backref=db.backref('edit_tree', lazy='dynamic', cascade='all, delete-orphan'))

    @declared_attr
    def product_id(cls):
        return db.Column(db.Integer, db.ForeignKey('product.id'))

    @declared_attr
    def product(cls):
        return db.relationship('Product', backref=backref("edit_tree", cascade="all, delete-orphan"))


class Product(ProductMixin, db.Model):
    pass


class ProductRelation(ProductRelationMixin, db.Model):
    pass


class FuncRelation(FuncRelationMixin, db.Model):
    pass


class Attr(AttrMixin, db.Model):
    pass


class AttrOther(AttrOtherMixin, db.Model):
    pass


class AttrContent(AttrContentMixin, db.Model):
    pass


class ProductAssess(ProductAssessMixin, db.Model):
    pass


class ProductTree(ProductTreeMixin, db.Model):
    pass
