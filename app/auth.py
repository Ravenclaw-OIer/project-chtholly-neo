import functools
from flask import (
  Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')
def check_password_strength(pwd):
  # Comment the next line in production
  return "OK"
  # Comment the prev line in production
  has_letter = False
  has_number = False
  for c in pwd:
    if 'a' <= c and c <= 'z':
      has_letter = True
    elif 'A'  <= c and c <= 'Z':
      has_letter = True
    elif '0' <= c <= '9':
      has_number = True
  
  if len(pwd) < 6:
    return '密码长度至少应该为 6''
  elif not has_letter:
    return '密码中必须包含至少一个字母'
  elif not has_number:
    return '密码中必须包含至少一个数字''
  else:
    return 'OK'

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
    elif check_password_strength(password) != 'OK':
      error = check_password_strength(password)
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