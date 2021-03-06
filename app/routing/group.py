from . import admin
from app import db
from flask import render_template, flash, redirect, url_for, request, session
from app.models import DeviceGroup, Device
from app.forms import DeviceGroupDataForm
from flask_login import login_required


@admin.route('/group/<int:page>', methods=["GET"])
@login_required
def group(page):
    if page is None:
        page = 1
    page_data = DeviceGroup.query.order_by(
        DeviceGroup.id.asc()
    ).paginate(page=page, per_page=5)

    # 保存管理员名字和角色id
    session_admin = session['admin']
    session_role_id = session['role']

    device_all = Device.query.all()
    device_count = Device.query.count()
    device_online = Device.query.filter_by(_online=1).count()
    device_active = Device.query.filter_by(_active=1).count()

    return render_template('group.html',
                           page_data=page_data,
                           device_count=device_count,
                           device_all=device_all,
                           device_online=device_online,
                           device_active=device_active,
                           session_admin=session_admin,
                           session_role_id=session_role_id
                           )


@admin.route('/group_edit', methods=['GET', 'POST'])
@login_required
def group_edit():
    id = request.args.get('id')
    group = DeviceGroup.query.get_or_404(id)
    form = DeviceGroupDataForm()
    if form.validate_on_submit():
        data = form.data
        group.name = data['name']
        db.session.add(group)
        db.session.commit()
        flash("项目组表数据修改成功", "ok")
    return render_template('edit/group_edit.html', form=form, group=group)


@admin.route('/group_add', methods=['GET', 'POST'])
@login_required
def group_add():
    form = DeviceGroupDataForm()
    if form.validate_on_submit():
        name = form.name.data

        device_group = DeviceGroup(name=name)

        db.session.add(device_group)
        db.session.commit()
        flash('设备组表数据添加成功!', 'ok')
        return redirect(url_for('admin.group_add'))
    return render_template('add/group_add.html', form=form)


@admin.route('/group_delete', methods=['GET', 'POST'])
@login_required
def group_delete():
    id = request.args.get('id')
    page = request.args.get('page')
    group = DeviceGroup.query.get_or_404(id)
    group.id = id
    db.session.delete(group)
    db.session.commit()
    flash("项目组表数据删除成功", "ok")
    return redirect(url_for('admin.group', page=page))
