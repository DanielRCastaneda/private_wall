from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.message import Message
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/register_user', methods = ['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/')
    data ={
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.get_all(data)
    session['user_id'] = id  
    print(request.form)
    return redirect('/dashboard')

@app.route('/dashboard')
def dash():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {    
        'id':session['user_id']
    }
    user = User.get_by_id(data)
    messages = Message.get_user_messages(data)
    users = User.save()
    return render_template('dash.html', user = user , messages = messages, users = users)

@app.route('/login', methods = ['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash('Invaild email', 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Invaild Password', 'login')
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')