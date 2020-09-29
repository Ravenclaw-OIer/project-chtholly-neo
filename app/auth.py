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