# coding: utf-8
from ..base import *
from sqlalchemy.orm import backref
from sqlalchemy.ext.declarative import declared_attr
from datetime import datetime


class ProductMixin:
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    config_name = db.Column(db.String(32))

    product_id = db.Column(db.String(12))

    company_name = db.Column(db.String(32))
    project_location = db.Column(db.String(68))
    consumer = db.Column(db.String(68))

    version = db.Column(db.String(68))
    name = db.Column(db.String(68), index=True)

    start_date = db.Column(db.DateTime)
    update_date = db.Column(db.DateTime)

    func_teams = db.Column(db.String(2000))
    fmea_id = db.Column(db.String(20))
    design_resp = db.Column(db.String(128))

    first_time = db.Column(db.DateTime, default=datetime.now)
    last_time = db.Column(db.DateTime, default=datetime.now)

    @declared_attr
    def user_id(cls):
        return db.Column(db.Integer, db.ForeignKey('users.id'))

    @declared_attr
    def user(cls):
        return db.relationship('User', foreign_keys=[cls.user_id], backref=backref("product", cascade="all,delete"))


class AnalysisMixin:
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    parent_id = db.Column(db.Integer, index=True)

    @declared_attr
    def product_id(cls):
        return db.Column(db.Integer, db.ForeignKey('product.id'))

    @declared_attr
    def product(cls):
        return db.relationship('Product', foreign_keys=[cls.product_id], backref=backref("child", cascade="all,delete"))


class Product(ProductMixin, db.Model):
    pass


class ProductChildRelation(AnalysisMixin, db.Model):
    pass
