from .models import User,Post
from flask import flash,render_template,request,redirect,url_for
from .forms import RegistrationForm,LoginForm
from app import app,db,bcrypt
from app import login_manager
from flask_login import login_user,current_user,logout_user

@app.route('/',methods=['POST','GET'])
def home():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}','success')
        return redirect(url_for('home'))
    return render_template('index4.html',form=form)





@app.route('/register',methods=['POST','GET'])
def register():
    title='Register'
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'{form.username.data}, Your Account has been Created, Login Here ','success')
        return redirect(url_for('login'))
    return render_template('register.html',form=form,title='Register')





@app.route('/login',methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            return redirect(url_for('home'))
            flash(f'Welcome {form.email.data}','success')
        else:
            flash('LOgin Unseccessful','danger')
        
    return render_template('login.html',form=form,title='Login')





@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

