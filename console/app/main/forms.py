# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired
from wtforms import ValidationError
from ..models import User
from ..base import BaseForm

from ..read_config import ReadConfig
from flask_login import current_user


class CreateProductForm(FlaskForm, BaseForm):
    # config_name = SelectField('选择配置文件', coerce=str, validators=[DataRequired(message='文件名不能空')])
    name = StringField('产品名:')

    def __init__(self, *args, **kwards):
        super(CreateProductForm, self).__init__(*args, **kwards)

        # paths = ReadConfig().get_all_config()
        # self.config_name.choices = [(path['filename'], path['filename']) for path in paths] if paths else []


class StructureTreeForm(FlaskForm, BaseForm):
    company_name = StringField('公司名称:')
    project_location = StringField('工程位置:')
    consumer = StringField('客户名称:')
    name = StringField('项目:', validators=[DataRequired(message='服务器不能为空！')])
    submit = SubmitField('保存')

    def __init__(self, *args, **kwargs):
        super(StructureTreeForm, self).__init__(*args, **kwargs)
        self.required_form()
