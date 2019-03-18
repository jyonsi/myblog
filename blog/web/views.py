import datetime
import random

from flask import Blueprint, redirect, request, render_template, url_for, make_response, Response, jsonify

from back.models import Article, Comment, db, ArticleType

web = Blueprint('web',__name__)


@web.route('/home/')
@web.route('/')
def index():
    arts = Article.query.all()
    len1 = len(arts)
    if len1 > 6:
        newArts = Article.query.offset(len1 - 6).limit(5).all()
    else:
        newArts = Article.query.all()

    ha = HotArticles()

    return render_template('web/home.html',arts = arts,newArts=newArts,hotArticles=ha)


@web.route('/detail/<int:id>',methods=["GET"])
def detail(id):
    if request.method == 'GET':

        art = Article.query.filter(Article.id==id).first()
        comments = art.comments
        art.views_count +=1
        db.session.commit()
        return render_template('web/detail.html',art= art,comments=comments,)

@web.route('/detail/<int:id>',methods=["POST"])
def comment(id):
    #comment_context = request.form.get('editorContent')
    #comment_context = request.args.get('editorContent')
    comment_context = request.values.get('editorContent')
    print(comment_context)
    create_time = datetime.datetime.now()

    comment = Comment()

    comment.content= comment_context
    comment.owner = 'jyonsi'
    comment.create_time = create_time

    art = Article.query.filter(Article.id==id).first()
    comment.com_art = art

    db.session.add(comment)
    db.session.commit()

    #res = make_response(redirect(url_for('web.detail',id=id)),)
    # resp = Response(response=res, status=200, content_type='text/html;charset=utf8')
    #return render_template('web/detail.html', art=art, comments=comments)
    # return res,200
    return jsonify({'result':'sccuess','status':'200'})
    #return res

@web.route('/articles/',methods=["GET"])
def articles():
    arts = Article.query.all()
    types = ArticleType.query.all()
    lookarts = lookAround()

    return render_template('web/article.html',arts=arts,types=types,lookarts=lookarts)


@web.route('/typenav/<type>')
def typenav(type):
    type = ArticleType.query.filter(ArticleType.type==type).first()

    arts = type.arts
    types = ArticleType.query.all()
    print(arts)
    return render_template('web/article.html',arts = arts,types=types)







def HotArticles():
    hotArticles = Article.query.order_by(-Article.views_count).limit(5).all()
    return hotArticles



def lookAround():
    arts = Article.query.all()
    len1 = len(arts)
    if len1>5:
        start = random.randint(0, len1 - 5)
    start = random.randint(0,len1)
    end = start+5
    return arts[start:end]


















@web.route('/test/')
def test():
    arts = lookAround()
    print(arts)
    return 'return'