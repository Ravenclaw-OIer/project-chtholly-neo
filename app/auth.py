import functools
from flask import (
  Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')
@bp.route('/register', methods = ('GET', 'POST'))
def register():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    db = get_db()
    error = None

    if not username:
      error = '用户名不能为空'
    elif not password:
      error = '密码不能为空'
    elif db.execute(
      'SELECT id FROM user WHERE username = ?', 
      (username, )
    ).fetchone() is not None:
      error = '用户名 {} 已经注册'.format(username)

    if error is None:
      db.execute(
        'INSERT INTO user (username, password) VALUE (?, ?)',
        (username, generate_password_hash(password))
      )
      db.commit()
      return redirect(url_for('auth.login'))
    
    flash(error)
  return render_template('auth/register.html')

@bp.route('/login', methods = ('GET', 'POST')):
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    db = get_db()
    error = None

    if not username:
      error = '用户名不能为空'
    elif not password:
      error = '密码不能为空'
    else:
      user = db.execute('SELECT id FROM user WHERE username = ?', (username, )).fetchone()
    
    if user is None:
      error = '用户尚未注册'
    elif not check_password_hash(user['password'], password):
      error = '密码错误'

    if error is None:
      session.clear()
      session['user_id'] = user['id']
      return redirect(url_for('index'))
    
    flash(error)
  return render_template('auth/register.html')

@bp.route('/logout')
def logout():
  session.clear()
  return redirect(url_for('index'))

def login_required(view):
  @functools.wraps(view)
  def wrapped_view(**kwargs):
    if g.user is None:
      return redirect(url_for('auth.login'))
    
    return view(**kwargs)

@bp.before_app_request
def load_user():
  uid = session.get('user_id')
  if uid is None:
    g.user = None
  else:
    g.user = get_db().execute('SELECT * FROM user WHERE id = ?', (username, )).fetchone()
    