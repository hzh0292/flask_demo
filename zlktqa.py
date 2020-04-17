from flask import Flask, render_template, request, redirect, url_for, session, g
import config
from exts import db
from models import User, Question, Answer
from sqlalchemy import or_
from decorators import login_required

app = Flask(__name__)  # type:Flask
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    context = {
        'questions': Question.query.order_by(Question.id.desc()).all()
    }
    return render_template('index.html', **context)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter_by(telephone=telephone).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return "手机号码或密码错误，请重试！"


@app.route('/question/', methods=['GET', 'POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        user = g.user
        new_question = Question(title=title, content=content, author=user)
        db.session.add(new_question)
        db.session.commit()
        return '发布成功'


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(telephone=telephone).first()
        if user:
            return "该手机号码已经被注册，请更换手机号码！"
        else:
            if password1 != password2:
                return "两次密码输入不一致，请核对后再提交。"
            else:
                user = User(telephone=telephone, username=username, password=password1)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))


@app.route('/logout/')
def logout():
    session.pop('user_id')
    return redirect(url_for('login'))


@app.route('/detail/<question_id>/')
def detail(question_id):
    question_detail = Question.query.filter_by(id=question_id).first()
    return render_template('detail.html', question=question_detail)


@app.route('/add_answer', methods=['POST'])
def add_answer():
    answer_content = request.form.get('answer_content')
    question_id = request.form.get('question_id')
    answer = Answer(content=answer_content, author=g.user, question_id=question_id)
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail', question_id=question_id))


@app.route('/query')
def query():
    q = request.args.get('q')
    questions = Question.query.filter(or_(Question.title.contains(q), Question.content.contains(q))).all()
    return render_template('index.html', questions=questions)


@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter_by(id=user_id).first()
        if user:
            g.user = user


@app.context_processor
def my_context_processor():
    if hasattr(g, 'user'):
        return {'user': g.user}
    return {}


if __name__ == '__main__':
    app.run()
