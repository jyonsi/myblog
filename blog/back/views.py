import math

from flask import Blueprint, render_template, request, redirect, session, make_response, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from back.models import db, User, ArticleType, Article
from utils.functions import is_login, PageBean
blue = Blueprint('back',__name__,url_prefix='/back')


@blue.route('/login/',methods=["GET","POST"])
def login():
    if request.method=="GET":
        return render_template('back/login.html')
    if request.method=="POST":
        account = request.form.get("account")
        password = request.form.get('password')
        if account == '' or password == '':
            msg = '请输入密码和账号'
            return render_template('back/login.html',msg=msg)
        user = User.query.filter(User.account == account).first()
        if user == None:
            msg = '没有此用户'
            return render_template('back/login.html',msg=msg)
        elif not check_password_hash(user.password,password):
            msg = '密码输入错误'
            return render_template('back/login.html',msg=msg)
        session['user_id'] = user.id
        res = make_response(redirect(url_for('back.index')))
        res.set_cookie('token',str(user.id),max_age=10000)
        return  res


@blue.route('/regist/',methods=["POST","GET"])
def regist():
    if request.method == 'GET':
        return render_template('back/register.html')
    if request.method == 'POST':
        account = request.form.get('account')
        password1 = request.form.get('password01')
        password2 = request.form.get('password02')
        user = User.query.filter(User.account==account).first()
        print(user)
        if user:
            msg = '此用户已经存在'
            return render_template('back/register.html',msg=msg)
        print(password1,password2)
        if password1 != password2:
            msg = '密码不一致'
            return render_template('back/register.html',msg=msg)
        user = User()
        user.account = account
        user.password = generate_password_hash(password1)
        user.save()
    return redirect(url_for('back.login'))




@blue.route('/index/')
@is_login
def index():
    return render_template('/back/index.html')


@blue.route('/logout/')
def logout():
    del session['user_id']
    return redirect(url_for('back.login'))





@blue.route('/art_add/',methods=["POST","GET"])
@is_login
def art_add():
    if request.method == "GET":
        types = db.session.query(ArticleType).all()
        return render_template('/back/art_add.html',types=types)
    if request.method == "POST":
        artname = request.form.get('name')
        type = request.form.get('type')
        content = request.form.get('content')
        desc = request.form.get('desc')
        # print(artname,arttype,content,desc)
        #查出文章类型对象
        arttype = ArticleType.query.filter(ArticleType.type==type).first()

        art = Article()
        art.title = artname
        art.desc = desc
        art.content = content
        # 反向引用文章类型对象
        art.tp = arttype

        db.session.add(art)
        db.session.commit()
        return redirect(url_for('back.art_list'))




@blue.route('/art_delete/')
@is_login
def art_delete():

    id = request.args.get('id')
    print(id)
    delart = Article.query.get(id)
    print(delart)
    db.session.delete(delart)
    db.session.commit()
    arts = Article.query.all()
    return redirect(url_for('back.art_list',arts=arts))




@blue.route('/type_add/',methods=["POST","GET"])
@is_login
def type_add():
    if request.method == 'GET':
        return render_template('/back/type_add.html')
    if request.method == 'POST':
        typeName = request.form.get('type')
        print(typeName)
        newType = ArticleType()
        newType.type = typeName
        try:
            db.session.add(newType)
            db.session.commit()
        except:
            return redirect(url_for('back.type'))
        return redirect(url_for('back.type'))




# @blue.route('/art_list/',methods=["POST","GET"])
# @is_login
# def art_list():
#     arts = db.session.query(Article).all()
#
#     return render_template('/back/art_list.html',arts=arts)



@blue.route('/art_list/',methods=["POST","GET"])
@is_login
def art_list():
    if request.method=='GET':
        #查询所有数据
        arts = db.session.query(Article).all()
        # 获取当前页
        c = request.args.get('currentPage')
        print(c)
        if c:
            currentPage = int(c)
        pageBean = PageBean(arts,currentPage=1)

        return render_template('/back/art_list.html',pageBean=pageBean)



@blue.route('/type_category/')
@is_login
def type():
    if request.method == "GET":

        #查询所有数据
        types = db.session.query(ArticleType).all()
        # 获取当前页
        c = request.args.get('currentPage')
        print(c)
        if c:
            currentPage = int(c)
        pageBean = PageBean(types,currentPage=1)


        return render_template('/back/type_list.html',pageBean=pageBean)




@blue.route('/user_list/',methods=['POST',"GET"])
def user_list():
    if request.method == "GET":
        users = User.query.all()
        # 获取当前页
        c = request.args.get('currentPage')
        print(c)
        if c:
            currentPage = int(c)
        pageBean = PageBean(users,currentPage=1)

        return render_template('back/user_list.html',pageBean = pageBean)


    if request.method == 'POST':
        condition = request.form.get('condition')
        print(condition)
        users = User.query.filter(User.id==condition).all()
        # 获取当前页
        c = request.args.get('currentPage')
        print(c)
        if c:
            currentPage = int(c)
        pageBean = PageBean(users,currentPage=1)
        return render_template('back/user_list.html', pageBean=pageBean)





