
from .models import User,Post
from flask import flash,render_template,request,redirect,url_for,abort
from .forms import RegistrationForm,LoginForm,UpdateProfileForm,PostForm
from app import app,db,bcrypt
from app import login_manager
from flask_login import login_user,current_user,logout_user,login_required
import os,secrets
from PIL import Image


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
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
            flash(f'Welcome {form.email.data}','success')
        else:
            flash('Email Or Password Incorrect','danger')
        
    return render_template('login.html',form=form,title='Login')





@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))



def save_pic(form_picture):
    rando_hex = secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = rando_hex + f_ext
    picture_path = os.path.join(app.root_path,'static/profile_pic',picture_fn)
    form_picture.save(picture_path)
    return picture_fn

def save_post_pic(form_post_pic):
    rando_hex = secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_post_pic.filename)
    picture_fn = rando_hex + f_ext
    picture_path = os.path.join(app.root_path,'static/posts',picture_fn)

    output_size = (834,340)
    i = Image.open(form_post_pic)
    i.thumbnail(output_size)
    i.save(picture_path)
    # form_post_pic.save(picture_path)
    return picture_fn




@app.route('/account',methods=['POST','GET'])
@login_required 
def account():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file= save_pic(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your Account has been updated successfully ','success')
        return redirect(url_for('account'))

    elif request.method=='GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',filename='profile_pic/'+current_user.image_file)
    return render_template('candidates_profile.html',title='Account',image_file=image_file,form=form)





@app.route('/add_post',methods=['POST','GET'])
@login_required
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_post_pic(form.picture.data)
        title = form.title.data
        content = form.content.data
        author = current_user

        post = Post(title=title,content=content,author=author,image_file=picture_file)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created",'success')
        return redirect(url_for('posts'))
    return render_template('add_post.html',form=form,legend='Add Post')



@app.route('/posts',methods=['POST','GET'])
def posts():
    posts = Post.query.all()
    return render_template('blog_list.html',posts=posts)


@app.route("/post/<post_id>")
def post_detail(post_id):
    post = Post.query.get(post_id)
    return render_template('blog_single.html',title=post.title,post=post)




@app.route("/post/<post_id>/update",methods=['POST','GET'])
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:     
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file= save_post_pic(form.picture.data)
            post.image_file  = picture_file        
        post.title=form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('You blog has been updated successfully....')
        return redirect(url_for('post_detail',post_id=post.id))
    elif request.method =='GET':
        form.title.data = post.title
        form.content.data = post.content
        form.picture.data = post.image_file
    return render_template('add_post.html',title="Update Post",post=post,form=form,legend='Update Post')

