from flask import json
from bson import json_util, ObjectId

def bson_to_json(data):
    return json.dumps(data, default=json_util.default)

def bson_obj_id(id):
    return ObjectId(id)

class AllowFile:
    IMG_EXTENSIONS = set(['jpg', 'png', 'jpeg', 'bmp'])

    @classmethod
    def is_img(cls, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1] in cls.IMG_EXTENSIONS

class TypeRender:

    _template = '''
        <tr class="center aligned" data-type="{type}">
          <td class="six wide">{name}</td>
          <td class="ten wide {attr_cls}">{attr}</td>
        </tr>
    '''

    _type = {
        'text': '{v}',
        'img': '<img src={v} width=200 height=150 />',
        'url': '<a href="{v}" target="_blank">{v}</a>',
        'num': '{v}',
        'star': '<div class="ui massive star rating">{v}</div>'
    }

    _star_tmp = '<i class="icon active"></i>'

    @classmethod
    def render_html(cls, attr_name, attr_value, attr_type):
        if attr_type == 'star':
            content = cls._type['star'].format(v=int(attr_value) * cls._star_tmp)
        elif attr_type == 'bool':
            if attr_value is True or attr_value == 1:
                return cls.render(attr_name, '是', attr_type, hightlight='positive')
            else:
                return cls.render(attr_name, '否', attr_type, hightlight='negative')
        else:
            content = cls._type[attr_type].format(v=attr_value)

        return cls.render(attr_name, content, attr_type)

    @classmethod
    def render(cls, name, attr, type, hightlight=''):
        return cls._template.format(name=name, attr=attr, type=type, attr_cls=hightlight)