# ！/usr/bin/env python
# -*-coding:utf-8 -*-

from . import admin
from app import db
from flask import render_template, flash, redirect, url_for
from app.models import Auth
from app.forms import AuthDataForm
from flask_login import login_required


@admin.route('/auth_add', methods=['GET', 'POST'])
@login_required
def auth_add():
    form = AuthDataForm()
    if form.validate_on_submit():
        name = form.name.data
        url = form.url.data

        auth = Auth(name=name,
                    url=url)

        db.session.add(auth)
        db.session.commit()
        flash('权限表数据添加成功!', 'ok')
        return redirect(url_for('admin.auth_add'))
    return render_template('add/auth_add.html', form=form)
