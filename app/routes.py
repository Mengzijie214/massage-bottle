# 路由处理
import os

from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models import User, Bottle, Reply
from app.extensions import mysql
from passlib.hash import sha256_crypt
from functools import wraps
from app import create_app

main_bp = Blueprint('main', __name__)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'loggedin' not in session:
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function


@main_bp.route('/')
def index():
    return render_template('index.html')


@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        User.create(username, password)
        return redirect(url_for('main.login'))
    return render_template('register.html')


@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute('''
            SELECT id, username, password
            FROM users
            WHERE username = %s
            ''', (username,))

        account = cursor.fetchone()

        if account and sha256_crypt.verify(password, account['password']):
            session['loggedin'] = True
            session['user_id'] = account['id']
            return redirect(url_for('main.dashboard'))
    return render_template('login.html')


@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@main_bp.route('/send_bottle', methods=['POST'])
@login_required
def send_bottle():
    content = request.form['content']
    Bottle.create(session['user_id'], content)
    return redirect(url_for('main.dashboard'))


@main_bp.route('/get_bottle')
@login_required
def get_bottle():
    cursor = mysql.connection.cursor()
    cursor.execute('''
        SELECT * FROM bottles
        WHERE user_id != %s
        ORDER BY RAND() LIMIT 1
    ''', (session['user_id'],))
    bottle = cursor.fetchone()
    return render_template('view_bottle.html', bottle=bottle)


@main_bp.route('/reply/<int:bottle_id>', methods=['POST'])
@login_required
def reply(bottle_id):
    content = request.form['content']
    Reply.create(bottle_id, session['user_id'], content)
    return redirect(url_for('main.dashboard'))


@main_bp.route('/my_bottles')
@login_required
def my_bottles():
    cursor = mysql.connection.cursor()
    cursor.execute('''
        SELECT
            b.id AS bottle_id,
            b.content AS bottle_content,
            DATE_FORMAT(b.create_time, '%%Y-%%m-%%d %%H:%%i') AS bottle_time,
            r.content AS reply_content,
            DATE_FORMAT(r.create_time, '%%Y-%%m-%%d %%H:%%i') AS reply_time
        FROM bottles b
        LEFT JOIN replies r ON b.id = r.bottle_id
        WHERE b.user_id = %s
        ORDER BY b.create_time DESC
    ''', (session['user_id'],))
    bottles = cursor.fetchall()
    return render_template('my_bottles.html', bottles=bottles)


@main_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

# 测试数据库链接
# app = create_app(os.getenv())
# with app.app_context():
#     try:
#         conn = mysql.connection
#         cursor = conn.cursor()
#         cursor.execute("SELECT 1")
#         print("数据库链接成功！")
#     except Exception as e:
#         print(f'数据库链接失败:{e}')

# from flask import Blueprint, render_template, request, redirect, url_for, session
# from app.models import User, Bottle, Reply
# from app.extensions import mysql
# from passlib.hash import sha256_crypt
# from functools import wraps
#
# main_bp = Blueprint('main', __name__)
#
#
# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if 'loggedin' not in session:
#             return redirect(url_for('main.login'))
#         return f(*args, **kwargs)
#
#     return decorated_function
#
#
# @main_bp.route('/')
# def index():
#     return render_template('index.html')
#
#
# @main_bp.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         User.create(username, password)
#         return redirect(url_for('main.login'))
#     return render_template('register.html')
#
#
# @main_bp.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#
#         cursor = mysql.connection.cursor()
#         cursor.execute('''
#             SELECT id, username, password
#             FROM users
#             WHERE username = %s
#             ''', (username,))
#
#         account = cursor.fetchone()
#
#         if account and sha256_crypt.verify(password, account[2]):
#             session['loggedin'] = True
#             session['user_id'] = account[0]
#             return redirect(url_for('main.dashboard'))
#     return render_template('login.html')
#
#
# @main_bp.route('/dashboard')
# @login_required
# def dashboard():
#     return render_template('dashboard.html')
#
#
# @main_bp.route('/send_bottle', methods=['POST'])
# @login_required
# def send_bottle():
#     content = request.form['content']
#     Bottle.create(session['user_id'], content)
#     return redirect(url_for('main.dashboard'))
#
#
# @main_bp.route('/get_bottle')
# @login_required
# def get_bottle():
#     cursor = mysql.connection.cursor()
#     cursor.execute('''
#         SELECT * FROM bottles
#         WHERE user_id != %s
#         ORDER BY RAND() LIMIT 1
#     ''', (session['user_id'],))
#     bottle = cursor.fetchone()
#     return render_template('view_bottle.html', bottle=bottle)
#
#
# @main_bp.route('/reply/<int:bottle_id>', methods=['POST'])
# @login_required
# def reply(bottle_id):
#     content = request.form['content']
#     Reply.create(bottle_id, session['user_id'], content)
#     return redirect(url_for('main.dashboard'))
#
#
# @main_bp.route('/my_bottles')
# @login_required
# def my_bottles():
#     cursor = mysql.connection.cursor()
#     cursor.execute('''
#         SELECT b.*, r.content as reply_content, r.create_time as reply_time
#         FROM bottles b
#         LEFT JOIN replies r ON b.id = r.bottle_id
#         WHERE b.user_id = %s
#         ORDER BY b.create_time DESC
#     ''', (session['user_id'],))
#     bottles = cursor.fetchall()
#     return render_template('my_bottles.html', bottles=bottles)
#
#
# @main_bp.route('/logout')
# def logout():
#     session.clear()
#     return redirect(url_for('main.index'))