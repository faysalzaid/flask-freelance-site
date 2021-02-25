from flask_wtf  import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,SubmitField,BooleanField,TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from app.models import User
from flask_login import current_user
from flask_wtf.file import FileField,FileAllowed


class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=3,max=10)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Password',validators=[EqualTo('password')])
    submit = SubmitField('Sign Up')


    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This Username is already taken')


    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already taken')





class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remeber me')
    submit = SubmitField('Sign In') 
    
    def validate_email_login(self,email):
        emails = User.query.filter_by(email=email.data).first()
        if not emails:
            raise ValidationError('The Email is not recognized')



    

class UpdateProfileForm(FlaskForm):
        username = StringField('Username',validators=[DataRequired(),Length(min=3,max=10)])
        email = StringField('Email',validators=[DataRequired(),Email()])
        picture = FileField('Update Your Profile Pic',validators=[FileAllowed(['png','jpg'])])
        submit = SubmitField('Update')


        def validate_username(self,username):
            if username.data != current_user.username:
                user = User.query.filter_by(username=username.data).first()
                if user:
                    raise ValidationError('This Username is already taken')


        def validate_email(self,email):
            if email.data != current_user.email:
                user = User.query.filter_by(email=email.data).first()
                if user:
                    raise ValidationError('This email is already taken')





class PostForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired(),Length(max=100,min=5)])
    content = TextAreaField('Content',validators=[DataRequired()])
    picture = FileField('Choose Picture for Your Post',validators=[FileAllowed(['png','jpg'])])
    submit = SubmitField('Add')
