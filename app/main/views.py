from app import mongo
from app.forms import PkForm, LoginForm, BaseEntryForm
from datetime import datetime
from flask import render_template, request, flash, url_for, current_app, abort, redirect, jsonify
from flask.ext.login import current_user
from util import TypeRender

from . import main

@main.route('/')
def index():
    pk_form = PkForm()
    lg_form = LoginForm()
    return render_template('index.html', pk_form=pk_form, lg_form=lg_form)


@main.route('/pk', methods=['GET', 'POST'])
def pk():
    pk_form = PkForm(request.form)
    if pk_form.validate_on_submit():
        pk1_name = request.form.get('pk1').strip()
        pk2_name = request.form.get('pk2').strip()
        pk1_data = mongo.db['items'].find({'title': pk1_name})
        pk2_data = mongo.db['items'].find({'title': pk2_name})
        flash('查询成功', 'SUCCESS')
        return render_template('pk.html', pk1=pk1_name, pk2=pk2_name)
    flash('非法请求', 'WARNING')
    return render_template('pk.html')

@main.route('/item/<title>')
def item(title):
    data = mongo.db['items'].find_one({'title': title})
    if not data:
        abort(404)
    mongo.db['items'].update({'title': title}, {"$inc": {"view": 1}})
    return render_template('item.html', data=data, TypeRender=TypeRender)

@main.route('/item/add_attr', methods=['POST'])
def add_attr():
    if request.method == 'POST':
        title = request.json['title'].strip()
        attr_name = request.json['attr_name']
        attr_type = request.json['attr_type']
        attr_value = request.json['attr_value']
        if attr_value is None:
            return jsonify(status=False, reason="属性值不能为空")
        if mongo.db['items'].find_one({'title': title, 'attributes.attr_name': attr_name}):
            return jsonify(status=False, reason="属性已存在")
        mongo.db['items'].update(
            {'title': title},
            {
                '$inc': {'attr_count': 1},
                '$push':
                    {
                        'attributes':
                            {
                                'attr_name': attr_name,
                                'attr_value': attr_value,
                                'attr_type': attr_type
                            }
                    }
            }
        )
        html = TypeRender.render_html(attr_name, attr_value, attr_type)
        return jsonify(status=True, reason="添加属性成功", html=html)

@main.route('/create_entry', methods=['GET', 'POST'])
def create_entry():
    entry_form = BaseEntryForm()
    if entry_form.validate_on_submit():
        title = request.form['title']
        type = request.form['type']
        mongo.db.items.insert({
            'title': title,
            'type': type,
            'attributes':[],
            'attr_count': 1,
            'view': 0,
            'created_at': datetime.now(),
            'created_by': current_user.id
        })
        return redirect(url_for('.item', title=title))
    return render_template('create.html', entry_form=entry_form)
