# ！/usr/bin/env python
# -*-coding:utf-8 -*-
from . import admin
from app import db
from flask import render_template, flash, redirect, url_for, request, session
from app.models import OrderTable, Project, User, Device
from app.forms import OrderDataForm
from flask_login import login_required


@admin.route('/orderlist/<int:page>', methods=["GET"])
@login_required
def orderlist(page):
    if page is None:
        page = 1
    page_data = OrderTable.query.join(
        User
    ).filter(
        User.id == OrderTable.user_id
    ).join(
        Device
    ).filter(
        Device.id == OrderTable.device_id
    ).join(
        Project
    ).filter(
        Project.id == OrderTable.project_id
    ).order_by(
        OrderTable.id.asc()
    ).paginate(page=page, per_page=5)

    # 保存管理员名字和角色id
    session_admin = session['admin']
    session_role_id = session['role']

    project_all = Project.query.all()
    order_all = OrderTable.query.all()


    return render_template('orderlist.html',
                           page_data=page_data,
                           project_all=project_all,
                           order_all=order_all,
                           session_admin=session_admin,
                           session_role_id=session_role_id
                           )


@admin.route('/order_add', methods=['GET', 'POST'])
@login_required
def order_add():
    form = OrderDataForm()

    if request.method == 'GET' or request.method == 'POST':
        form.user_id.choices = [(v.id, v.name) for v in User.query.all()]
        form.device.choices = [(v.id, v.name) for v in Device.query.all()]
        form.pay_method.choices = [(0, '微信'), (1, '支付宝'), (2, '现金'), (3, '银行卡')]
        form.stats.choices = [(0, '未支付'), (1, '已支付'), (2, '退款中'), (3, '完成退款')]

    if form.validate_on_submit():
        money = form.money.data
        number = form.number.data
        user_id = form.user_id.data
        device = form.device.data
        pay_method = form.pay_method.data
        stats = form.stats.data
        order = OrderTable(money=money,
                           number=number,
                           user_id=user_id,
                           device_id=device,
                           pay_method=pay_method,
                           stats=stats)

        db.session.add(order)
        db.session.commit()
        flash('订单表数据添加成功!', 'ok')
        return redirect(url_for('admin.order_add'))
    return render_template('add/order_add.html', form=form)
