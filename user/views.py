#!/usr/bin/env python
#coding: utf-8

from flask import Blueprint, render_template, request, flash, redirect, url_for 
from flask_login import current_user,login_user, logout_user

from .forms import LoginForm, SignupForm, ResetForm
from .models import User

from datetime import datetime

from db import db

bp = Blueprint('user', __name__)



@bp.route('/login', methods=['GET', 'POST'])
def login():
    ''' 管理员登录 '''
    if current_user is not None and current_user.is_authenticated():
        return redirect(url_for('term.index'))
        
    form = LoginForm(next=request.args.get('next', ''))
    if request.method == 'POST':
        print 'form.data:', form.data
        username = form.username.data
        password = form.password.data
        next = form.next.data
        user, authenticated = User.authenticate(username, password)
        if user and authenticated:
            if login_user(user, remember = form.remember.data):
                flash(u'登录成功', 'success')
                if next:
                    return redirect(next)
                return redirect(url_for('term.index'))
        elif not user:
            flash(u'用户不存在', 'error')
        else: 
            flash(u'密码错误', 'error')

        form.next.data = request.args.get('next', '')
        
    return render_template('user/login.html', form = form)
    
    
@bp.route('/signup', methods=['GET', 'POST'])    
def signup():
    form = SignupForm()
    if request.method == 'POST' and form.validate_on_submit():
        print 'form.data:', form.data
        if User.check_username(form.username.data) :
            flash(u"用户名已存在")
            return render_template("user/signup.html", form = form)
                      
        user = User()    
        user.login = form.username.data
        user.password = User.crypted_password(form.password.data)
        user.email = form.email.data
        db.session.add(user)
        db.session.commit()
        
        flash(u"注册成功")
        return redirect(url_for('user.login'))
              
    else:
        print form.errors
          
    return render_template("user/signup.html", form = form)    
  
  
@bp.route('/logout')
def logout():
    ''' 退出 '''
    logout_user()
    return redirect(url_for('user.login'))

    
@bp.route('/settings')
def settings():
    ''' 设置 '''
    return render_template('user/settings.html')


@bp.route('/account',  methods=['GET', 'POST'])    
def account():
    ''' 账户信息(修改密码) '''
    
    form = ResetForm()
    print form.validate(), form.is_submitted()
    if request.method == 'POST' and form.validate_on_submit():
        print 'form:', form.password.data, form.data
        user = User.query.get(current_user.id)    
        user.password = User.crypted_password(form.password.data)
        user.updated_at = datetime.now()
        db.session.commit()
        flash(u"修改成功")
    else:
        flash(u"修改密码")    
    return render_template('user/account.html', form = form)

    
@bp.route('/change-password')
def change_password():
    ''' 修改密码 '''
    return redirect('user.account')
    
    
@bp.route('/retrieve-password')
def retrieve_password():
    ''' 找回密码(通过邮箱) '''
    return render_template('user/retrieve-password.html')
        