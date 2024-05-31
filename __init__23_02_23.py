# This file contains an example Flask-User application.
# To keep the example simple, we are applying some unusual techniques:
# - Placing everything in one file
# - Using class-based configuration (instead of file-based configuration)
# - Using string-based templates (instead of file-based templates)

from email.policy import default
import imp
from pdb import post_mortem
from flask import Flask, g, render_template_string, request, redirect, session
from flask_mongoengine import MongoEngine
from mongoengine import Document
from mongoengine import DateTimeField, StringField, ReferenceField, ListField
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect

from flask_login import login_manager, LoginManager, UserMixin, login_user, login_required, logout_user, current_user # 
#from flask_user import UserManager
from flask_session import Session
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
#from .main import main as main_blueprint
#from .auth import auth as auth_blueprint
# from .models import db, User

# # def get_db():
# #     if 'db' not in g:
# #         g.db = MongoEngine()
# #     return g.db     

# # # Database However, using MongoEngine can come at an additional cost when misused
# # using the ORM in a for loop rather than batching up commands in PyMongo
#db = None # db.Document object has no attribute 'Document'
db = MongoEngine() #  # Database Name db is declared for scope not created
#db = get_db()
# # Password Encryption
bcrypt = Bcrypt() # Encryption Name db is declared for scope not created


# # Login Manager
login_manager = LoginManager() # Login Manager Name db is declared for scope not created

# # To enable CSRF protection globally for a Flask app. CSRF protection requires a secret key to securely sign the token. By default this will use the Flask app’s SECRET_KEY. If you’d like to use a separate token you can set WTF_CSRF_SECRET_KEY.
csrf = CSRFProtect()

# # The Application Factory. Any configuration, registration, and other setup the application needs will happen inside the function, then the application will be returned.
def create_app(test_config=None):
    # """Initialize the core application.""" ###########################
    #app = Flask(__name__)
    app = Flask(__name__, instance_relative_config=True,
                template_folder='template', instance_path=os.getcwd() + '/instance')
    app.config.from_object('config')
#     # app.config.from_pyfile('config.py')

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        # app.config.from_mapping(test_config) # for future options
        app.config.from_pyfile('config.py', silent=True)

    ########################### Debug Mode #################
    app.debug = True

    # # # # # Initialize Plugins  ######################################
    #########  All Plugins take cares of Application/Request contaxt
    try:
        # Setup Flask-MongoEngine
        # # # Database initialization
        db.init_app(app)
        
        # # Password Encryption initialization
        bcrypt.init_app(app)

        # user Manager
        #user_manager = UserManager(app, db, User)
        
        # # login_manager initialization
        login_manager.init_app(app)

        # # csrf initialization
        csrf.init_app(app)
        
        # blueprint for auth routes in our app
        from .auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)
        # blueprint for auth routes in our app
        from .main import main as main_blueprint
        app.register_blueprint(main_blueprint)
        # blueprint for users routes in our app
        from .users import users as users_blueprint
        app.register_blueprint(users_blueprint)
        # blueprint for papers routes in our app
        from .papers import papers as papers_blueprint
        app.register_blueprint(papers_blueprint)
        
        # session
        Session(app)
        #     # ensure the instance folder exists
        os.makedirs(app.instance_path)
    except OSError:
        pass
    ############# Application Context ########################
    with app.app_context():
        
        # from .models import User
        # Include our Routes
        # from . import routes
        # Set up models
        # Register Blueprints
        # The Home page is accessible to anyone
        @app.route('/')
        def home_page():
            # String-based templates
            return render_template_string("""
                {% extends "flask_user_layout.html" %}
                {% block content %}
                    <h2>Home page</h2>
                    <p><a href={{ url_for('user.register') }}>Register</a></p>
                    <p><a href={{ url_for('user.login') }}>Sign in</a></p>
                    <p><a href={{ url_for('home_page') }}>Home page</a> (accessible to anyone)</p>
                    <p><a href={{ url_for('member_page') }}>Member page</a> (login required)</p>
                    <p><a href={{ url_for('user.logout') }}>Sign out</a></p>
                {% endblock %}
                """)
        # https://medium.com/@dmitryrastorguev/basic-user-authentication-login-for-flask-using-mongoengine-and-wtforms-922e64ef87fe
        # @app.route('/login', methods=['POST'])
        # def login():
        #     if request.method == 'POST':
        #         mail_e = request.form.get("email")
        #         paswd = request.form.get("password")
        #         #usr = User.objects(username="kapil@ieee.org1").only("username").first()
        #         usr = User.objects(username=mail_e).first()
        #         if hasattr(usr, 'objects') != False:
        #             if app.bcrypt.check_password_hash(usr.password, paswd):
        #                 app.session["id"] = usr.id
        #                 login_user(usr)
        #                 return redirect('/')
        
        @app.route('/logout', methods = ['GET'])
        @login_required
        def logout():
            logout_user()
            app.session["id"] = None
            return redirect("/") #redirect(url_for('login'))
        # The Members page is only accessible to authenticated users via the @login_required decorator
        @app.route('/members')
        @login_required    # User must be authenticated
        def member_page():
            # String-based templates
            return render_template_string("""
                {% extends "flask_user_layout.html" %}
                {% block content %}
                    <h2>Members page</h2>
                    <p><a href={{ url_for('user.register') }}>Register</a></p>
                    <p><a href={{ url_for('user.login') }}>Sign in</a></p>
                    <p><a href={{ url_for('home_page') }}>Home page</a> (accessible to anyone)</p>
                    <p><a href={{ url_for('member_page') }}>Member page</a> (login required)</p>
                    <p><a href={{ url_for('user.logout') }}>Sign out</a></p>
                {% endblock %}
                """)
    
        @login_manager.user_loader
        def load_user(id):
            return User.objects(id=id).first()
    return app



###################################################################
# Classes for Data Modleing

class Add(db.EmbeddedDocument):
    add = db.StringField(max_length=100,default='')
    state = db.StringField(max_length=100,default='')
    pin = db.IntField(required=True, default=0)
    countary = db.StringField(max_length=25,default='')
    phone = db.StringField(max_length=25,default='')
    email = db.StringField(max_length=25,default='')
    

    def __unicode__(self):
        return self.add + ", " + self.state + ", " + self.pin + ", " + self.countary
    def __repr__(self):
        return self.add + ", " + self.state + ", " + self.pin + ", " + self.countary
    def __str__(self):
        return self.add + ", " + self.state + ", " + self.pin + ", " + self.countary
    def add_dict(self):
        return {
            'Flat No., Steet etc.':self.add
            ,'State':self.state
            ,'Pin Code':self.pin
            ,'Countary':self.countary
            ,'Mobile Phone':self.phone
            ,'Email':self.email
        }
    


class Address(db.EmbeddedDocument):
    home = db.EmbeddedDocumentField(Add)
    office = db.EmbeddedDocumentField(Add)

    def __unicode__(self):
        return self.home.__str__() + ", " + self.office.__str__()
    def __repr__(self):
        return self.home.__str__() + ", " + self.office.__str__()
    def __str__(self):
        return self.home.__str__() + ", " + self.office.__str__()
    def address_dict(self):
        return {
            'Home':self.home.add_dict()
            ,'Office':self.office.add_dict()
        }


class Contact(db.EmbeddedDocument):
    web = db.StringField(max_length=100,default='')
    googlescholar = db.StringField(max_length=200,default='')
    linkedin = db.StringField(max_length=200,default='')
    facebook = db.StringField(max_length=200,default='')
    youtube = db.StringField(max_length=200,default='')
    twitter = db.StringField(max_length=200,default='')
    # relations many to one
    address = db.EmbeddedDocumentField(Address)


    def __unicode__(self):
        return self.address.__str__() 
    def __repr__(self):
        return self.address.__str__() 
    def __str__(self):
        return self.address.__str__()
    def contact_dict(self):
        return {
            'Website/WebLink':self.web
            ,'Google Scholar':self.googlescholar
            ,'Linkedin':self.linkedin
            ,'Facebook':self.facebook
            ,'Youtube':self.youtube
            ,'twitter':self.twitter
            ,'Address':self.address.address_dict()

        }


class Faculty(db.EmbeddedDocument):
    position = db.StringField(max_length=25,default='')
    post = db.StringField(max_length=25,default='')
    empcode = db.StringField(max_length=9,default='')  # "8328"

    def __unicode__(self):
        return self.title + ", " + self.title + ", " + self.post + ", " + self.empcode
    def __repr__(self):
        return self.title + ", " + self.title + ", " + self.post + ", " + self.empcode
    def __str__(self):
        return self.title + ", " + self.title + ", " + self.post + ", " + self.empcode
    def faculty_dict(self):
        return {
            'Position':self.position
            ,'Post':self.post
            ,'Employee Code':self.empcode

        }


class Student(db.EmbeddedDocument):
    programe = db.StringField(max_length=50,default='')
    year = db.IntField(required=True, default=0)
    branch = db.StringField(max_length=50,default='')
    rollnumber = db.StringField(max_length=9,default='') #2K19/IT/10
    #roll = db.IntField(required=True, default=0)

    def __unicode__(self):
        return self.programe + ", " + self.year + ", " + self.branch + ", " + self.roll
    def __repr__(self):
        return self.programe + ", " + self.year + ", " + self.branch + ", " + self.roll
    def __str__(self):
        return self.programe + ", " + self.year + ", " + self.branch + ", " + self.roll
    def student_dict(self):
        return {
            'Programe':self.programe
            ,'year':self.year
            ,'Branch':self.branch
            ,'Roll Number':self.rollnumber
            #,'Roll Number':self.roll
        }

class University(db.EmbeddedDocument):
    name = db.StringField(max_length=200,default='')  # Delhi Technological University"
    url = db.StringField(max_length=100,default='')  # "http://www.dtu.ac.in"
    office = db.EmbeddedDocumentField(Add)

    def __unicode__(self):
        return self.name 
    def __repr__(self):
        return self.name 
    def __str__(self):
        return self.name
    def university_dict(self):
        return {
            'Name':self.name
            ,'Url':self.url
            ,'Office':self.office.add_dict()
        }

class Department(db.EmbeddedDocument):
    name = db.StringField(max_length=200,default='')  # "Information Technology",
    # "http://www.dtu.ac.in/Web/Departments/InformationTechnology/about/",
    url = db.StringField(max_length=100,default='')
    office = db.EmbeddedDocumentField(Add)

    def __unicode__(self):
        return self.name 
    def __repr__(self):
        return self.name 
    def __str__(self):
        return self.name 
    def department_dict(self):
        return {
            'Name':self.name
            ,'Url':self.url
            ,'Office':self.office.add_dict()
        }


class SponsoredProjects(db.EmbeddedDocument):
    title = db.StringField(max_length=200,default='')  # Title of Project
    name = db.StringField(max_length=200,default='')  # funding source name
    duration = db.StringField(max_length=20,default='')
    amount = db.StringField(max_length=20,default='')

    def __unicode__(self):
        return self.title 
    def __repr__(self):
        return self.title 
    def __str__(self): 
        return self.title 
    def __dict__(self):
        return {
            'key_str':self.title,   # It is PK and index key in EmbeddedDocument sponsoredprojects. It is used for edit update, delete opration.
            'Title':self.title
            ,'name':self.name
            ,'Duration':self.duration
            ,'Amount':self.amount
        }


class Patents(db.EmbeddedDocument):
    countary = db.StringField(max_length=200,default='')
    title = db.StringField(max_length=200,default='')
    year = db.IntField(required=True, default=0)
    url = db.StringField(max_length=200,default='')

    def __unicode__(self):
        return self.title 
    def __repr__(self): 
        return self.title 
    def __str__(self): 
        return self.title 
    def __dict__(self):
        return {
            'key_str':self.title   #  It is PK and index key in EmbeddedDocument patents. It is used for edit update, delete opration.
            ,'Title':self.title
            ,'url':self.url
            ,'Year':self.year
            ,'Countary':self.countary
        }


class IndustryCollaboration(db.EmbeddedDocument):
    name = db.StringField(max_length=200,default='')  # "Samsung India",
    url = db.StringField(max_length=200,default='')  # "https://www.samsung.com/in/home/",
    mou = db.StringField(max_length=200,default='')
    collaboration = db.StringField(max_length=200,default='')  # "M.Tech"
    title = db.StringField(max_length=200,default='')

    def __unicode__(self):
        return self.name 
    def __repr__(self):
        return self.name 
    def __str__(self):   
        return self.name
    def __dict__(self):
        return {
            'key_str':self.name   #  It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
            ,'Name':self.name
            ,'url':self.url
            ,'MoU':self.mou
            ,'Collaboration':self.collaboration
            ,'Title':self.title
        }


class StartUp(db.EmbeddedDocument):
    name = db.StringField(max_length=200,default='')  # "DezWebApp",
    url = db.StringField(max_length=200,default='')
    funding = db.StringField(max_length=200,default='')  # "Self"

    def __unicode__(self):
        return self.name 
    def __repr__(self):
        return self.name 
    def __str__(self):
        return self.name
    def __dict__(self):
        return {
            'key_str':self.name   #  It is PK and index key in EmbeddedDocument startup. It is used for edit update, delete opration.
            ,'Name':self.name
            ,'Url':self.url
            ,'Funding':self.funding
        }


class Books(db.EmbeddedDocument):
    # "Software Reliability Modeling and Selection",
    title = db.StringField(max_length=200,default='')
    # "Book describes selection of software reliability models",
    description = db.StringField(max_length=500,default='')
    year = db.IntField(required=True, default=0)  # 2012
    # "https://www.amazon.in/Software-Reliability-Modeling-Selection-Sharma/dp/3848481235",
    url = db.StringField(max_length=200,default='')
    publisher = db.StringField(max_length=200,default='')  # "Lambert"

    def __unicode__(self):
        return self.title 
    def __repr__(self):
        return self.title 
    def __str__(self): 
        return self.title 
    def __dict__(self):
        return {
            'key_str':self.title   # def __str__(self): return self.name  It is PK and index key in EmbeddedDocument books. It is used for edit update, delete opration.
            ,'Title':self.title
            ,'Url':self.url
            ,'Year':self.year
            ,'Description':self.description
            ,'Publisher':self.publisher
        }


class Awards(db.EmbeddedDocument):
    name = db.StringField(max_length=200,default='')  # "DTU Research Awards",
    description = db.StringField(max_length=200,default='')  # "Annual",
    certificate = db.StringField(max_length=200,default='')  # "pathtofile"

    def __unicode__(self):
        return self.name 
    def __repr__(self):
        return self.name 
    def __str__(self): 
        return self.name
    def __dict__(self):
        return {
            'key_str':self.name   #  It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
            ,'Name':self.name
            ,'Description':self.description
            ,'Certificate':self.certificate
        }


class SocialImpact(db.EmbeddedDocument):
    # "App for election commission of india vote chandni chowk",
    name = db.StringField(max_length=200,default='')
    # "https://play.google.com/store/apps/details?id=in.gov.delhi.votechandnichowk&hl=en_IN&gl=US"
    url = db.StringField(max_length=200,default='')

    def __unicode__(self):
        return self.name 
    def __repr__(self):
        return self.name 
    def __str__(self):
        return self.name
    def __dict__(self):
        return {
            'key_str':self.name   #  It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
            ,'Name':self.name
            ,'Url':self.url
        }


class TechnologyTransfer(db.EmbeddedDocument):
    name = db.StringField(max_length=200,default='')  # "DezWebApp",
    technology = db.StringField(max_length=200,default='')  # "5G",
    url = db.StringField(max_length=200,default='')
    royalty = db.StringField(max_length=200,default='')

    def __unicode__(self):
        return self.name 
    def __repr__(self):
        return self.name 
    def __str__(self):
        return self.name
    def __dict__(self):
        return {
            'key_str':self.name   # It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
            ,'Name':self.name
            ,'Technology':self.technology
            ,'Url':self.url
            ,'Royalty':self.royalty
        }


# Define the User db.Document.
# NB: Make sure to add flask_user UserMixin !!!
class User(db.Document, UserMixin):
    active = db.BooleanField(default=True)
    #papers = db.EmbeddedDocumentListField(ReferenceField(Paper))

    # User authentication information
    username = db.StringField(default='')
    password = db.StringField(default='')

    # User information
    fname = db.StringField(default='')
    mname = db.StringField(default='')
    lname = db.StringField(default='')
    title = db.StringField(max_length=9,default='') # Mr Ms Dr.
    # dob = db.DateTimeField(null=True)
    # date_created = db.DateTimeField(default=datetime.utcnow,
    #                                     help_text='date the User was created')
    directory = db.StringField(default='')
    photo = db.StringField(default='')
    qualifications = db.StringField(default='')
    areas_of_interest = db.StringField(default='')
    bio = db.StringField(default='')
    publications = db.StringField(default='')

    contact = db.EmbeddedDocumentField(Contact)
    faculty = db.EmbeddedDocumentField(Faculty)
    student = db.EmbeddedDocumentField(Student)
    university = db.EmbeddedDocumentField(University)
    department = db.EmbeddedDocumentField(Department)

    sponsoredprojects = db.EmbeddedDocumentListField(SponsoredProjects)
    patents = db.EmbeddedDocumentListField(Patents)
    industrycollaboration = db.EmbeddedDocumentListField(IndustryCollaboration)
    startup = db.EmbeddedDocumentListField(StartUp)
    books = db.EmbeddedDocumentListField(Books)
    awards = db.EmbeddedDocumentListField(Awards)
    socialimpact = db.EmbeddedDocumentListField(SocialImpact)
    technologytransfer = db.EmbeddedDocumentListField(TechnologyTransfer)
    #####Relationships
    roles = db.ListField(StringField(), default=[])

    def personal_dict(self):
        return {
            'First Name':self.fname
            ,'Middle Name':self.mname
            ,'Last Name':self.lname
            ,'User Directory':self.directory
            ,'User Photo':self.photo
            ,'Qualifications':self.qualifications
            ,'Areas of Interest':self.areas_of_interest
            ,'Biography':self.bio
            ,'Publications':self.publications
        }
    def cred_dict(self):
        return {
            'User Name':self.username
            ,'Roles':self.roles
        }

    def home_dict(self):
        sp = []
        for i in self.sponsoredprojects:
            sp.append(i.__dict__())
            #print(i.__dict__())
        # patents
        pat = []
        for i in self.patents:
            pat.append(i.__dict__())
        #industrycollaboration
        ic = []
        for i in self.industrycollaboration:
            ic.append(i.__dict__())
        #startup
        stup = []
        for i in self.startup:
            stup.append(i.__dict__())
        #books
        bo = []
        for i in self.books:
            bo.append(i.__dict__())
        #awards
        aw = []
        for i in self.awards:
            aw.append(i.__dict__())
        #socialimpact
        si = []
        for i in self.socialimpact:
            si.append(i.__dict__())
        #technologytransfer
        tt = []
        for i in self.technologytransfer:
            tt.append(i.__dict__())
        return {
            'Name':self.fname + self.mname + self.lname
            ,'User Photo':self.photo
            ,'Dept':self.department.department_dict()
            ,'Qualifications':self.qualifications
            ,'Areas of Interest':self.areas_of_interest
            ,'Biography':self.bio
            ,'Publications':self.publications
            ,'Contact':self.contact.contact_dict()
            ,'Faculty':self.faculty.faculty_dict()
            ,'Student':self.student.student_dict()
            ,'University':self.university.university_dict()
            ,'Sponsored Projects':sp
            ,'Patents':pat
            ,'Industry Collaboration':ic
            ,'Startup':stup
            ,'Books':bo
            ,'Awards':aw
            ,'Social Impact':si
            ,'Technology Transfer':tt
        }


#################################################################################################################
##########################################  Problem / Paper / Thesis / Project ##################################

class LinkDesc(db.EmbeddedDocument):
    # Link and is's description
    desc = db.StringField(max_length=500,default='')
    link = db.StringField(max_length=200,default='')

    def __unicode__(self):
        return self.desc 
    def __repr__(self):
        return self.desc 
    def __str__(self):
        return self.desc
    def __dict__(self):
        return {
            'key_str':self.desc   # It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
            ,'link':self.link
        }

class ResearchProblem(db.EmbeddedDocument):
    statment = db.StringField(max_length=500,default='')  # "Research probleum statment"
    date_created = db.DateTimeField(default=datetime.utcnow,
                                        help_text='date the Research Problem was created')
    keywords = db.EmbeddedDocumentListField(LinkDesc)
    area = db.EmbeddedDocumentListField(LinkDesc)
    applications = db.EmbeddedDocumentListField(LinkDesc)
    journals_conf = db.EmbeddedDocumentListField(LinkDesc)
    code_links =  db.EmbeddedDocumentListField(LinkDesc) #source Codes for 
    datasets_links = db.EmbeddedDocumentListField(LinkDesc)
    peoples = db.EmbeddedDocumentListField(LinkDesc)
    articals = db.EmbeddedDocumentListField(LinkDesc)
    resoures = db.EmbeddedDocumentListField(LinkDesc)
    sm = db.EmbeddedDocumentListField(LinkDesc) # social media like youtube twiter 
    desc = db.StringField(max_length=1000,default='')

    def __unicode__(self):
        return self.statment 
    def __repr__(self):
        return self.statment 
    def __str__(self):
        return self.statment
    def __dict__(self):
        #Keywords
        ky = []
        for i in self.keywords:
            ky.append(i.__dict__())
        #area
        ar = []
        for i in self.area:
            ar.append(i.__dict__())
        #applications
        app = []
        for i in self.applications:
            app.append(i.__dict__())
        #journals_conf
        jc = []
        for i in self.journals_conf:
            jc.append(i.__dict__())
        #code_links
        cl = []
        for i in self.code_links:
            cl.append(i.__dict__())
        #datasets_links
        dsl = []
        for i in self.datasets_links:
            dsl.append(i.__dict__())
        #peoples
        pp = []
        for i in self.peoples:
            pp.append(i.__dict__())
        #articals
        art = []
        for i in self.articals:
            art.append(i.__dict__())
        #resoures
        res = []
        for i in self.resoures:
            res.append(i.__dict__())
        #sm
        s = []
        for i in self.sm:
            s.append(i.__dict__())
        return {
            'key_str':self.statment   # It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
            ,'statment':self.statment
            ,'date_created':self.date_created
            ,'keywords':ky
            ,'area':ar
            ,'applications':app
            ,'journals_conf':jc
            ,'code_links':cl
            ,'datasets_links':dsl
            ,'peoples':pp
            ,'articals':art
            ,'resoures':res
            ,'social_media':s
        }

class PaperPerson(db.EmbeddedDocument):
    name = db.StringField(max_length=100,default='')
    title = db.StringField(max_length=10,default='')# Mr. Ms. Miss
    position = db.StringField(max_length=20,default='')# Dr. Prof
    corresponding = db.BooleanField(required=True, default=False)
    sequence = db.IntField(required=True, default=0)
    gender = db.StringField(max_length=10,default='')
    affiliation = db.EmbeddedDocumentField(LinkDesc)
    ph = db.StringField(max_length=100,default='')
    email = db.EmailField(default='')
    user_id = db.StringField(max_length=100,default='') # ref to objectid of user document if any
    webpage = db.EmbeddedDocumentField(LinkDesc)
    sm = db.EmbeddedDocumentListField(LinkDesc) # social media like youtube twiter 

    def __unicode__(self):
        return self.name 
    def __repr__(self):
        return self.name 
    def __str__(self):
        return self.name
    def __dict__(self):
        #affiliation
        aff = []
        for i in self.affiliation:
            aff.append(i.__dict__())
        #webpage
        wb = []
        for i in self.webpage:
            wb.append(i.__dict__())
        #social_media
        s = []
        for i in self.sm:
            s.append(i.__dict__())
        return {
            'key_str':self.name   # It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
            ,'title':self.title
            ,'position':self.position
            ,'corresponding':self.corresponding
            ,'sequence':self.sequence
            ,'gender':self.gender
            ,'affiliation':aff
            ,'phone':self.ph
            ,'email':self.email
            ,'webpage':wb
            ,'social_media':s
        }

class PaperRefFile(db.EmbeddedDocument): # file that has been uploaded and save in server file system
    name = db.StringField(max_length=100,default='') # It should be unique in file system diroctory
    articaltype = db.StringField(max_length=100,default='') # Journal / Conference / Book / Other
    year = db.IntField(required=True, default=0)
    path = db.StringField(max_length=100,default='') # full path to file
    mimetype = db.StringField(max_length=50,default='') # text/plain,application/pdf, application/octet-stream meaning “download this file”
    link = db.StringField(max_length=100,default='') # DOI etc
    bibtext = db.StringField(max_length=1000,default='')
    uptime = db.DateTimeField(default=datetime.utcnow,
                                        help_text='date and time the file was uploaded')
    desc = db.StringField(max_length=500,default='')

    def __unicode__(self):
        return self.name 
    def __repr__(self):
        return self.name 
    def __str__(self):
        return self.name
    def __dict__(self):
        return {
            'key_str':self.name   # It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
            ,'articaltype':self.articaltype
            ,'year':self.year
            ,'path':self.path
            ,'mimetype':self.mimetype
            ,'link':self.link
            ,'bibtext':self.bibtext
            ,'uptime':self.uptime
            ,'desc':self.desc
        }

class PaperFile(db.EmbeddedDocument): # file that has been uploaded and save in server file system
    name = db.StringField(max_length=100,default='') # It should be unique in file system diroctory
    type = db.StringField(max_length=100,default='') # Manuscript / Figure /Dataset / Bibtext / Tables / Template /cover letter / proof / plagiarism report / comments /replay / camera ready / published
    path = db.StringField(max_length=100,default='') # full path to file
    mimetype = db.StringField(max_length=50,default='') # text/plain,application/pdf, application/octet-stream meaning “download this file”
    link = db.StringField(max_length=100,default='') # url if any in case of dataset from repository
    uptime = db.DateTimeField(default=datetime.utcnow,
                                        help_text='date and time the file was uploaded')
    desc = db.StringField(max_length=1000,default='')

    def __unicode__(self):
        return self.name 
    def __repr__(self):
        return self.name 
    def __str__(self):
        return self.name
    def __dict__(self):
        return {
            'key_str':self.name   # It is PK.
            ,'type':self.type
            ,'path':self.path
            ,'mimetype':self.mimetype
            ,'link':self.link
            ,'uptime':self.uptime
            ,'desc':self.desc
        }

class PaperSubmittedinJournalComment(db.EmbeddedDocument):
    title = db.StringField(max_length=500,default='')  
    authors = db.EmbeddedDocumentListField(PaperPerson)
    revisionno = db.IntField(required=True, default=0) # No 0 in first submission
    comment = db.StringField(max_length=1000,default='') # No cooments in first submission
    uptime = db.DateTimeField(default=datetime.utcnow,
                                        help_text='submission date and time')
    reviewers = db.EmbeddedDocumentListField(PaperPerson)
    editors = db.EmbeddedDocumentListField(PaperPerson)
    submittedfiles = db.EmbeddedDocumentListField(PaperFile) 

    def __unicode__(self):
        return self.title 
    def __repr__(self):
        return self.title 
    def __str__(self):
        return self.title
    def __dict__(self):
        #authors
        au = []
        for i in self.authors:
            au.append(i.__dict__())
        #reviewers
        re = []
        for i in self.reviewers:
            re.append(i.__dict__())
        #editors
        ed = []
        for i in self.editors:
            ed.append(i.__dict__())
        #submittedfiles
        sf = []
        for i in self.submittedfiles:
            sf.append(i.__dict__())
        return {
            'key_str':self.title   # It is PK.
            ,'authors':au
            ,'revisionno':self.revisionno
            ,'comment':self.comment
            ,'uptime':self.uptime
            ,'reviewers':re
            ,'editors':ed
            ,'submittedfiles':sf
        }

class PaperSubmittedinJournal(db.EmbeddedDocument):
    name = db.StringField(max_length=200,default='')
    mode = db.StringField(max_length=20,default='') # Open access / free / hybried / paied etc
    specialissue = db.EmbeddedDocumentField(LinkDesc)#db.StringField(max_length=200,default='')
    link = db.StringField(max_length=100,default='')
    submissionlink = db.StringField(max_length=100,default='')
    subtemplate = db.EmbeddedDocumentField(PaperFile) # type : template
    publisher = db.StringField(max_length=200,default='')
    indexing = db.StringField(max_length=20,default='') # SCI / SCIE / ESCI / Scoups / Others
    score = db.DecimalField(precision=2,default=0)
    indexingproof = db.EmbeddedDocumentField(PaperFile) # type : indexingprof
    username = db.StringField(max_length=50,default='')
    papersubmittedinjournalcomments = db.EmbeddedDocumentListField(PaperSubmittedinJournalComment)

    def __unicode__(self):
        return self.name
    def __repr__(self):
        return self.name 
    def __str__(self):
        return self.name
    def __dict__(self):
        #papersubmittedinjournalcomments
        psjc = []
        for i in self.papersubmittedinjournalcomments:
            psjc.append(i.__dict__())
        return {
            'key_str':self.name   # It is PK.
            ,'mode':self.mode
            ,'specialissue':self.specialissue.__dict__()
            ,'link':self.link
            ,'submissionlink':self.submissionlink
            ,'subtemplate':self.subtemplate.__dict__()
            ,'publisher':self.publisher
            ,'indexing':self.indexing
            ,'score':self.score
            ,'indexingproof':self.indexingproof.__dict__()
            ,'username':self.username
            ,'papersubmittedinjournalcomments':psjc
        }
    
class PaperSubmittedinConferenceComment(db.EmbeddedDocument):
    title = db.StringField(max_length=500,default='') 
    authors = db.EmbeddedDocumentListField(PaperPerson)
    revisionno = db.IntField(required=True, default=0) # No 0 in first submission
    comment = db.StringField(max_length=1000,default='') # No cooments in first submission
    uptime = db.DateTimeField(default=datetime.utcnow,
                                        help_text='submission date and time')
    members = db.EmbeddedDocumentListField(PaperPerson)
    submittedfiles = db.EmbeddedDocumentListField(PaperFile)  # cooments file and reply file with text in desc field

    def __unicode__(self):
        return self.title 
    def __repr__(self):
        return self.title 
    def __str__(self):
        return self.title
    def __dict__(self):
        #authors
        au = []
        for i in self.authors:
            au.append(i.__dict__())
        #editors
        me = []
        for i in self.members:
            me.append(i.__dict__())
        #submittedfiles
        sf = []
        for i in self.submittedfiles:
            sf.append(i.__dict__())
        return {
            'key_str':self.title   # It is PK.
            ,'authors':au
            ,'revisionno':self.revisionno
            ,'comment':self.comment
            ,'uptime':self.uptime
            ,'editors':me
            ,'submittedfiles':sf
        }

class PaperSubmittedinConference(db.EmbeddedDocument):
    name = db.StringField(max_length=200,default='')
    confnumber = db.StringField(max_length=200,default='') # eg IEEE confrence ID
    deadline = db.DateTimeField(default=datetime.utcnow,
                                        help_text='submission Deadline date and time')
    sdate = db.DateTimeField(default=datetime.utcnow,
                                        help_text='conference is scheduled on date and time')
    edate = db.DateTimeField(default=datetime.utcnow,
                                        help_text='conference is closed on date and time')
    city = db.StringField(max_length=50,default='')
    confadd = db.StringField(max_length=200,default='')
    link = db.StringField(max_length=100,default='')
    submissionlink = db.StringField(max_length=100,default='')
    subtemplate = db.EmbeddedDocumentField(PaperFile) # type : template
    publisher = db.StringField(max_length=200,default='')
    indexing = db.StringField(max_length=20,default='') # SCI / SCIE / ESCI / Scoups / Others
    indexingproof = db.EmbeddedDocumentField(PaperFile) # type : indexingprof
    username = db.StringField(max_length=50,default='')
    papersubmittedinconferencecomments = db.EmbeddedDocumentListField(PaperSubmittedinConferenceComment)

    def __unicode__(self):
        return self.name
    def __repr__(self):
        return self.name 
    def __str__(self):
        return self.name
    def __dict__(self):
        #papersubmittedinconferencecomments
        pscc = []
        for i in self.papersubmittedinconferencecomments:
            pscc.append(i.__dict__())
        return {
            'key_str':self.name   # It is PK.
            ,'confnumber':self.confnumber
            ,'deadline':self.deadline
            ,'sdate':self.sdate
            ,'edate':self.edate
            ,'city':self.city
            ,'confadd':self.confadd
            ,'link':self.link
            ,'submissionlink':self.submissionlink
            ,'subtemplate':self.subtemplate.__dict__()
            ,'publisher':self.publisher
            ,'indexing':self.indexing
            ,'indexingproof':self.indexingproof.__dict__()
            ,'username':self.username
            ,'papersubmittedinjournalcomments':pscc
        }
      

class PaperDiscussionBoardComment(db.EmbeddedDocument):
    name = db.StringField(max_length=50,default='') # Who post it
    uptime = db.DateTimeField(default=datetime.utcnow,
                                        help_text='comment date and time')
    desc = db.StringField(max_length=1000,default='')

    def __unicode__(self):
        return self.name
    def __repr__(self):
        return self.name 
    def __str__(self):
        return self.name
    def __dict__(self):
        return {
            'key_str':self.name   # It is PK.
            ,'uptime':self.uptime
            ,'username':self.desc
        }
################################### paper class Document in Mongodb #########################
class Paper(db.Document):
    title = db.StringField(max_length=500,default='')  # PK
    rp = db.EmbeddedDocumentField(ResearchProblem)
    status = db.StringField(max_length=50,default='') # Formulating / Simulation / Writing /Submitted / Comments Recived / Wating for reply / Accepted /Rejected
    date_created = db.DateTimeField(default=datetime.utcnow,
                                        help_text='date the Paper was created')
    authors = db.EmbeddedDocumentListField(PaperPerson)
    #bibfile = db.StringField(max_length=100,default='') # Biblography/references file
    reffiles = db.EmbeddedDocumentListField(PaperRefFile)
    discussionboard = db.EmbeddedDocumentListField(PaperDiscussionBoardComment)
    ################################ paper writing / simulation #######################
    bibtext = db.EmbeddedDocumentListField(PaperFile)
    ownwork = db.EmbeddedDocumentListField(PaperFile)
    litrature = db.EmbeddedDocumentListField(PaperFile)
    result = db.EmbeddedDocumentListField(PaperFile)
    futurescope = db.EmbeddedDocumentListField(PaperFile)
    intro = db.EmbeddedDocumentListField(PaperFile)
    abstract = db.EmbeddedDocumentListField(PaperFile)
    ############################ paper submission ##################################
    journals = db.EmbeddedDocumentListField(PaperSubmittedinJournal)
    conferences = db.EmbeddedDocumentListField(PaperSubmittedinConference)
    ######################### paper accepted  #########################
    acceptance = db.EmbeddedDocumentField(PaperFile) # acceptance letter or email
    cameraready = db.EmbeddedDocumentField(PaperFile)
    published = db.EmbeddedDocumentField(PaperFile)
    link = db.StringField(max_length=100,default='')

    def __unicode__(self):
        return self.title
    def __repr__(self):
        return self.title 
    def __str__(self):
        return self.title
    def __dict__(self):
        #papersubmittedinconferencecomments
        au = []
        for i in self.authors:
            au.append(i.__dict__())
        #reffiles
        rf = []
        for i in self.reffiles:
            rf.append(i.__dict__())
        #discussionboard
        disb = []
        for i in self.discussionboard:
            disb.append(i.__dict__())
        #bibtext
        bt = []
        for i in self.bibtext:
            bt.append(i.__dict__())
        #ownwork
        ow = []
        for i in self.ownwork:
            ow.append(i.__dict__())
        #litrature
        lt = []
        for i in self.litrature:
            lt.append(i.__dict__())
        #result
        r = []
        for i in self.result:
            r.append(i.__dict__())
        #futurescope
        fs = []
        for i in self.futurescope:
            fs.append(i.__dict__())
        #intro
        io = []
        for i in self.intro:
            io.append(i.__dict__())
        #abstract
        ab = []
        for i in self.abstract:
            ab.append(i.__dict__())
        #journals
        j = []
        for i in self.journals:
            j.append(i.__dict__())
        #conferences
        c = []
        for i in self.conferences:
            c.append(i.__dict__())
        return {
            'key_str':self.title   # It is PK.
            ,'confnumber':self.rp.__dict__()
            ,'status':self.status
            ,'date_created':self.date_created
            ,'authors':au
            ,'reffiles':rf
            ,'discussionboard':disb
            ,'bibtext':bt
            ,'ownwork':ow
            ,'litrature':lt
            ,'result':r
            ,'futurescope':fs
            ,'intro':io
            ,'abstract':ab
            ,'journals':j
            ,'conferences':c
            ,'acceptance':self.acceptance.__dict__()
            ,'cameraready':self.cameraready.__dict__()
            ,'published':self.published.__dict__()
            ,'link':self.link
        }

