# coding: utf-8
from .. import db
from models.industry.product import AttrContentMixin
import json
from sqlalchemy import or_


class AttrContent(AttrContentMixin, db.Model):
    def __init__(self, *args, **kwargs):
        super(AttrContent, self).__init__(*args, **kwargs)

    def get_insert_data(self, data, product_id):
        if not data:
            return
        level = data.get('level')
        type_name = data.get('type_name')
        name_number = data.get('name_number')
        try:
            del data['level']
            del data['name_number']
            del data['type_name']
        except:
            pass
        d = {
            'level': level,
            'product_id': product_id,
            'real_content': json.dumps(data),
            'type': 'structure' if not type_name else type_name,
            'name_number': name_number,
        }
        return d

    @classmethod
    def create_edit(cls, data, product_id, name_number):
        is_have_content = cls.query.filter(cls.product_id == product_id, cls.name_number == name_number).first()

        data = cls().get_insert_data(data, product_id)
        if not is_have_content:
            content = cls(**data)
            db.session.add(content)
            return

        cls.update_model(is_have_content, data)
        return
