from datetime import datetime
import psycopg2
from flask import Flask, render_template, url_for,flash , redirect,json,jsonify,request,make_response
#from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm, QuizSubmitForm
import configitems as ci

app = Flask(__name__)

app.config['SECRET_KEY'] = 'f06a98ac6c1ea22df69f4f4f031c1060'
'''app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db= SQLAlchemy(app)

class User(db.Model):
    id=db.Column(db.Integer , primary_key=True)
    username = db.Column(db.String(20),unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file =  db.Column(db.String(20), nullable=False,default='default.jpg')
    password = db.Column(db.String(60),nullable=False)
    posts = db.relationship('Post',backref= 'author' , lazy= True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}','{self.password}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    date_posted = db.Column(db.DateTime,nullable=False, default = datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer,db.Foreignkey('User.id'), nullable=False)


def __repr__(self):
    return f"Post('{self.title}','{self.date_posted}')"


posts = [
    {
        'author': 'corey schafer',
        'title': 'blog post1',
        'content': 'first post content',
        'date_posted': 'April 20,2018'
    },

    {
        'author': 'jane doe',
        'title': 'blog post2',
        'content': 'second post content',
        'date_posted': 'April 21,2018'
    }
]
'''

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='home')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET','POST'])
def register():
    form = RegistrationForm()
    username = form.username.data
    email = form.email.data
    password = form.password.data
    confirm_password =form.confirm_password.data
    if form.validate_on_submit():
        #d = {}
        '''
        d=[]
        d["username"] = username
        d["email"] = email
        d["password"] = password
        with open('data.json', 'a')as fp:
            jsonobj=json.dumps(d)
        '''
        conn = psycopg2.connect(database=ci.dbname, user=ci.dbuser, password=ci.dbpassword, host=ci.dbhost, port=ci.dbport)
        cur = conn.cursor()
        Userinsertqry=""" INSERT INTO user_login (username, email, password) VALUES (%s,%s,%s)"""
        UservaluestoInsert=(username,email,password)
        cur.execute(Userinsertqry, UservaluestoInsert)
        conn.commit()
        count = cur.rowcount
        if count>0:
            flash('Account created for {form.username.data}!', 'success')

        return redirect(url_for('home'))
    return render_template('register.html', form=form)


@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
         with open('data.json','r')as fp:
            data = json.load(fp)
            print(data)
         for d in data:
            if form.email.data == d['email'] and form.password.data == d['password']:
                flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
    else:
            flash('Login Unsuccessful. please check username and password','danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/submitform", methods=['GET','POST'])
def submitform():
    if request.method=='POST':
        form=QuizSubmitForm()
        question=form.question.data
        AOption=form.AOption.data
        BOption=form.BOption.data
        COption=form.COption.data
        DOption=form.DOption.data
        answer=form.Answer.data
        category=form.category.data
        conn = psycopg2.connect(database=ci.dbname, user=ci.dbuser, password=ci.dbpassword, host=ci.dbhost, port=ci.dbport)
        cur = conn.cursor()
        qid="1"
        hint="test"
        Question_insertqry = """ INSERT INTO question (question,choice4) VALUES (%s, %s)"""
        Question_valuestoInsert=(question,DOption)
        #Question_insertqry=""" INSERT INTO question (quest_id, question_description, choice1, choice2, choice3, choice4, correct_answer, category_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
        #Question_valuestoInsert=(qid,question,AOption,BOption,COption,DOption,answer,category)
        cur.execute(Question_insertqry, Question_valuestoInsert)
        conn.commit()
        count = cur.rowcount
        if count>0:
            flash('Question added', 'success')
        return redirect(url_for('submitform'))

    return render_template('submitform.html', title='submitQuiz')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
