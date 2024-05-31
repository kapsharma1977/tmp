# This file contains an example Flask-User application.
# To keep the example simple, we are applying some unusual techniques:
# - Placing everything in one file
# - Using class-based configuration (instead of file-based configuration)
# - Using string-based templates (instead of file-based templates)

from email.policy import default
import base64,uuid,imp
from pdb import post_mortem
from flask import Flask, g, render_template_string, request, redirect, session, send_from_directory
from flask_mongoengine import MongoEngine
from mongoengine import Document
from mongoengine import DateTimeField, StringField, ObjectIdField ,ReferenceField, ListField, URLField
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
#from .paper import Paper
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
        
        # set db in global veriable g
        if 'db' not in g:
            g.db = db
        ################################
        #RuntimeError: Working outside of application context.
        #This typically means that you attempted to use functionality that needed
        #the current application. To solve this, set up an application context
        #with app.app_context(). See the documentation for more information.
        #######################
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
        @app.route('/download_file/<path>/<filename>', methods=['GET', 'POST'])
        @login_required
        def download_file(path, filename):
            #print(path.replace('-', '/'))
            return send_from_directory(path.replace('-', '/'), filename)
    return app


# get a UUID - URL safe, Base64
def get_a_uuid():
    r_uuid = base64.urlsafe_b64encode(uuid.uuid4().bytes)
    return r_uuid.decode('ascii').replace('=', '')
def get_new_filename(filename,ext):
    if not filename.strip():
        return None
    counter = 0
    fn = filename + '{}.' + ext
    while os.path.isfile(fn.format(counter)):
        counter += 1
    fn = fn.format(counter)
    return fn
#################################################################################################################
##########################################  Problem / Paper / Thesis / Project ##################################

class LinkDesc(db.EmbeddedDocument):
    # Link and is's description
    pk = db.StringField(max_length=100,default='') # pk
    desc = db.StringField(max_length=500,default='') # Unique PK
    link = db.StringField(max_length=500,default='')
    #link = db.URLField() #url

    def __unicode__(self):
        return self.desc 
    def __repr__(self):
        return self.desc 
    def __str__(self):
        return self.desc
    def __dict__(self):
        return {
            'pk':self.pk   # It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
            ,'desc':self.desc
            ,'link':self.link
        }

# def editlinkdesc(parentlist,childpropertylist,childpropertylistpk,linkdesc): # childpropertylist is of type LinkDesc
#     linkdesclist = getattr(parentlist,childpropertylist) # List of attribute id3 eg. PaperRefFile atribute office list id3='fileup'
#     ld = linkdesclist.get(pk = childpropertylistpk) # find perticuler LinkDesc object in list
#     ld.link = request.form.get("link")
#     ld.desc = request.form.get("desc")

class FileUploded(db.EmbeddedDocument):
    pk = db.StringField(max_length=100,default='') # pk 
    filename = db.StringField(max_length=100,default='') # It should be unique in file system diroctory
    path = db.StringField(max_length=100,default='') # full path to file
    ext = db.StringField(max_length=10,default='') #  file extenstion
    mimetype = db.StringField(max_length=50,default='') # text/plain,application/pdf, application/octet-stream meaning “download this file”
    uptime = db.DateTimeField(default=datetime.utcnow,
                                        help_text='date and time the file was uploaded')
    desc = db.StringField(max_length=500,default='')

    def __unicode__(self):
        return self.desc 
    def __repr__(self):
        return self.desc 
    def __str__(self):
        return self.desc
    def __dict__(self):
        return {
            'pk':self.pk   # It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
            ,'filename':self.filename
            ,'path':self.path
            ,'ext':self.ext
            ,'mimetype':self.mimetype
            ,'uptime':self.uptime
            ,'desc':self.desc
        }

class ResearchProblem(db.EmbeddedDocument):
    pk = db.StringField(max_length=100,default='') # pk 
    statment = db.StringField(max_length=500,default='')  # "Research problem statment"
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
            'pk':self.pk # It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
            ,'statment':self.statment   
            ,'statment':self.desc
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

class PaperPerson(db.EmbeddedDocument): #author
    pk = db.StringField(max_length=100,default='') # pk
    email = db.StringField(max_length=100,default='') # logicalkey
    name = db.StringField(max_length=100,default='')
    user_id = db.ObjectIdField() # ref to objectid of user document if any
    title = db.StringField(max_length=10,default='')# Mr. Ms. Miss
    position = db.StringField(max_length=20,default='')# Dr. Prof
    corresponding = db.BooleanField(default=False)
    sequence = db.IntField(required=True, default=0) # zero means non author
    gender = db.StringField(max_length=25,default='')
    affiliation = db.EmbeddedDocumentListField(LinkDesc)
    ph = db.StringField(max_length=100,default='')
    #email = db.EmailField()
    
    webpage = db.EmbeddedDocumentListField(LinkDesc)
    sm = db.EmbeddedDocumentListField(LinkDesc) # social media like youtube twiter 

    def __unicode__(self):
        return self.name 
    def __repr__(self):
        return self.name 
    def __str__(self):
        return self.name
    def __dict__(self):
        # #affiliation
        # aff = []
        # for i in self.affiliation:
        #     aff.append(i.__dict__())
        #webpage
        # wb = []
        # for i in self.webpage:
        #     wb.append(i.__dict__())
        #social_media
        s = []
        for i in self.sm:
            s.append(i.__dict__())
        return {
            'pk':self.pk   # It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
            ,'title':self.title
            ,'position':self.position
            ,'corresponding':self.corresponding
            ,'sequence':str(self.sequence)
            ,'gender':self.gender
            ,'affiliation':self.affiliation.__dict__()
            ,'phone':self.ph
            ,'email':self.email
            ,'webpage':self.webpage.__dict__()
            ,'social_media':s
        }

class PaperRefFile(db.EmbeddedDocument): # file that has been uploaded and save in server file system
    pk = db.StringField(max_length=100,default='') # pk
    title = db.StringField(max_length=100,default='') # paper/book title
    articaltype = db.StringField(max_length=100,default='') # Journal / Conference / Book / Other
    year = db.IntField(required=True, default=0)
    #link = db.URLField() # url DOI etc
    links = db.EmbeddedDocumentListField(LinkDesc) #other then doi links  
    doi = db.StringField(max_length=300,default='') # url DOI if any
    bibtext = db.StringField(max_length=1000,default='')
    
    fileup = db.EmbeddedDocumentListField(FileUploded) # .pdf / .doc  etc for paper
    desc = db.StringField(max_length=500,default='')

    def __unicode__(self):
        return self.title 
    def __repr__(self):
        return self.title 
    def __str__(self):
        return self.title
    def __dict__(self):
        lks = []
        for i in self.links:
            lks.append(i.__dict__())
        fup = []
        for i in self.fileup:
            fup.append(i.__dict__())
        return {
            'pk':self.pk   # It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
            ,'title':self.title
            ,'articaltype':self.articaltype
            ,'year':str(self.year)
            ,'Links':lks
            ,'Digital Object Identifier':self.doi
            ,'Bibtex':self.bibtext
            ,'Download Files':fup
            ,'desc':self.desc
        }


class PaperSubmittedinJournalComment(db.EmbeddedDocument):
    pk = db.StringField(max_length=100,default='') # pk
    revisionno = db.IntField(required=True, default=0) # No 0 in first submission
    title = db.StringField(max_length=500,default='')  
    authors = db.EmbeddedDocumentListField(PaperPerson)
    comment = db.StringField(max_length=1000,default='') # No cooments in first submission
    uptime = db.DateTimeField(default=datetime.utcnow,
                                        help_text='submission date and time')
    reviewers = db.EmbeddedDocumentListField(PaperPerson)
    editors = db.EmbeddedDocumentListField(PaperPerson)
    submittedfiles = db.EmbeddedDocumentListField(FileUploded) 

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
            'pk':self.title   # It is PK.
            ,'authors':au
            ,'revisionno':str(self.revisionno)
            ,'comment':self.comment
            ,'uptime':self.uptime
            ,'reviewers':re
            ,'editors':ed
            ,'submittedfiles':sf
        }

class PaperSubmittedinJournal(db.EmbeddedDocument):
    pk = db.StringField(max_length=100,default='') # pk
    name = db.StringField(max_length=200,default='')
    mode = db.StringField(max_length=20,default='') # Open access / free / hybried / paied etc
    specialissue = db.EmbeddedDocumentListField(LinkDesc)#db.StringField(max_length=200,default='')
    #link = db.URLField() # url
    #link = db.StringField(max_length=300,default='')
    links = db.EmbeddedDocumentListField(LinkDesc) #other then doi links
    #submissionlink = db.StringField(max_length=100,default='')
    submissionlink = db.EmbeddedDocumentListField(LinkDesc)
    subtemplate = db.EmbeddedDocumentListField(FileUploded) # type : template
    publisher = db.StringField(max_length=200,default='')
    indexing = db.StringField(max_length=20,default='') # SCI / SCIE / ESCI / Scoups / Others
    score = db.DecimalField(precision=2,default=0)
    indexingproof = db.EmbeddedDocumentListField(FileUploded) # type : indexingprof
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
            'pk':self.name   # It is PK.
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
    submittedfiles = db.EmbeddedDocumentListField(FileUploded)  # cooments file and reply file with text in desc field

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
            'pk':self.title   # It is PK.
            ,'authors':au
            ,'revisionno':str(self.revisionno)
            ,'comment':self.comment
            ,'uptime':self.uptime
            ,'editors':me
            ,'submittedfiles':sf
        }

class PaperSubmittedinConference(db.EmbeddedDocument):
    pk = db.StringField(max_length=100,default='') # pk
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
    #link = db.URLField()
    #link = db.StringField(max_length=300,default='')
    links = db.EmbeddedDocumentListField(LinkDesc) #other then doi links
    #submissionlink = db.StringField(max_length=100,default='')
    submissionlink = db.EmbeddedDocumentListField(LinkDesc)
    subtemplate = db.EmbeddedDocumentListField(FileUploded) # type : template
    publisher = db.StringField(max_length=200,default='')
    indexing = db.StringField(max_length=20,default='') # SCI / SCIE / ESCI / Scoups / Others
    indexingproof = db.EmbeddedDocumentListField(FileUploded) # type : indexingprof
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
            'pk':self.name   # It is PK.
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
    #pk = db.StringField(max_length=100,default='') # pk
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
            'id':id
            ,'pk':self.name   # It is PK.
            ,'uptime':self.uptime
            ,'username':self.desc
        }
################################### paper class Document in Mongodb #########################
class Paper(db.Document):
    # pk(artificialkey) is id
    title = db.StringField(max_length=500,default='')  # PK
    rp = db.EmbeddedDocumentListField(ResearchProblem)
    status = db.StringField(max_length=50,default='') # Formulating / Simulation / Writing /Submitted / Comments Recived / Wating for reply / Accepted /Rejected
    date_created = db.DateTimeField(default=datetime.utcnow,
                                        help_text='date the Paper was created')
    authors = db.EmbeddedDocumentListField(PaperPerson)
    #bibfile = db.StringField(max_length=100,default='') # Biblography/references file
    reffiles = db.EmbeddedDocumentListField(PaperRefFile)
    discussionboard = db.EmbeddedDocumentListField(PaperDiscussionBoardComment) # NO CRUD operations
    ################################ paper writing / simulation #######################
    bibtext = db.EmbeddedDocumentListField(FileUploded)
    ownwork = db.EmbeddedDocumentListField(FileUploded) # idea / research contribution / incremental work / value addtion 
    litrature = db.EmbeddedDocumentListField(FileUploded)
    result = db.EmbeddedDocumentListField(FileUploded)
    futurescope = db.EmbeddedDocumentListField(FileUploded)
    intro = db.EmbeddedDocumentListField(FileUploded)
    abstract = db.EmbeddedDocumentListField(FileUploded)
    manuscript = db.EmbeddedDocumentListField(FileUploded)
    ############################ paper submission ##################################
    journals = db.EmbeddedDocumentListField(PaperSubmittedinJournal)
    conferences = db.EmbeddedDocumentListField(PaperSubmittedinConference)
    ######################### paper accepted  #########################
    acceptance = db.EmbeddedDocumentListField(FileUploded) # acceptance letter or email
    cameraready = db.EmbeddedDocumentListField(FileUploded)
    published = db.EmbeddedDocumentListField(FileUploded)
    #link = db.URLField()
    links = db.EmbeddedDocumentListField(LinkDesc) # final published external link (Level 1)

    def __unicode__(self):
        return self.title
    def __repr__(self):
        return self.title 
    def __str__(self):
        return self.title
    def __dict__(self):
        # ResearchProblem
        r = []
        for i in self.rp:
            r.append(i.__dict__())
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
        # acceptance
        acc = []
        for i in self.acceptance:
            acc.append(i.__dict__())
        # cameraready
        camrdy = []
        for i in self.cameraready:
            camrdy.append(i.__dict__())
        # published
        pubd = []
        for i in self.published:
            pubd.append(i.__dict__())
        return {
            'pk':self.title   # It is PK.
            ,'Problem Statment':r
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
            ,'acceptance':acc
            ,'cameraready':camrdy
            ,'published':pubd
            ,'link':self.link
        }
    def pap_dict(self):
        return {
        'pk':self.title   # It is PK.
        ,'status':self.status
        ,'link':self.link
        ,'date_created':self.date_created
        }
# def rep_dict(self):
#     #keywords
#     kwc = []
#     for i in self.rp.keywords:
#         i.append(i.__dict__())
#     return {
#     'pk':self.rp.statment
#     ,'Created On':self.rp.date_created
#     ,'desc':self.rp.desc
#     }

###################################################################
# Classes for Data Modleing

class Add(db.EmbeddedDocument):
    ## Address Type. It should be unique for each user eg. a user can not have two personal address
    addtype = db.StringField(max_length=100,default='') # pk Coressponding, Permanent, Office, Personal, Online, Professonal etc
    ## Postal mail Address
    add = db.StringField(max_length=100,default='')
    state = db.StringField(max_length=100,default='')
    pin = db.IntField(required=True, default=0)
    countary = db.StringField(max_length=50,default='')
    
    ## Celluler Adsress
    phone = db.StringField(max_length=25,default='') # Mobile
    land = db.StringField(max_length=25,default='') #landline
    
    ## Electronic Mail address
    #email = db.EmailField()
    email = db.StringField(max_length=100,default='')
    
    ## social media Address
    sm = db.EmbeddedDocumentListField(LinkDesc)
        # sm.append()
        # LinkDesc(desc='web',link='http://wwww.kapilsharma.in')
        # LinkDesc(desc='googlescholar',link='http://wwww.kapilsharma.in')
        # LinkDesc(desc='linkedin',link='http://wwww.kapilsharma.in')
        # LinkDesc(desc='facebook',link='http://wwww.kapilsharma.in')
        # LinkDesc(desc='youtube',link='http://wwww.kapilsharma.in')
        # LinkDesc(desc='twitter',link='http://wwww.kapilsharma.in')
        # LinkDesc(desc='whatsapp',link='http://wwww.kapilsharma.in')
        # LinkDesc(desc='signal',link='http://wwww.kapilsharma.in')
        # LinkDesc(desc='telegram',link='http://wwww.kapilsharma.in')
        # LinkDesc(desc='koo',link='http://wwww.kapilsharma.in')
        # LinkDesc(desc='orcid id',link='http://wwww.kapilsharma.in')
    ##QR code based address
    #qrcode
    ##Payment Address
    #paymentupi
    
    #completeadd = db.StringField(max_length=300,default='') # complete address in one shot 
    
    def __unicode__(self):
        return self.add + ", " + self.state + ", " + str(self.pin) + ", " + self.countary
    def __repr__(self):
        return self.add + ", " + self.state + ", " + str(self.pin) + ", " + self.countary
    def __str__(self):
        return self.add + ", " + self.state + ", " + str(self.pin) + ", " + self.countary
    def postaladd(self):
        return self.add + ',' + self.state + ',' + self.pin + ',' + self.countary
    def __dict__(self):
        s_m = []
        for s in self.sm:
            s_m.append(s.__dict__())
        return {
            'addtype':self.addtype
            ,'Flat No., Steet etc.':self.add
            ,'State':self.state
            ,'Pin Code':str(self.pin)
            ,'Countary':self.countary
            ,'Mobile Phone':self.phone
            ,'Land Line':self.land
            ,'Email':self.email
            ,'Social Media':s_m
        }
    
    def view__dict(self):
        return {
            'addtype':self.addtype
            ,'add':self.add
            ,'state':self.state
            ,'pin':self.pin
            ,'countary':self.countary
            ,'phone':self.phone
            ,'line':self.land
            ,'email':self.email
        }
    

class Faculty(db.EmbeddedDocument):
    pk = db.StringField(max_length=100,default='')
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
            'pk':self.pk   #  It is PK and index key in EmbeddedDocument department. It is used for edit update, delete opration.
            ,'Position':self.position
            ,'Post':self.post
            ,'Employee Code':self.empcode

        }


class Student(db.EmbeddedDocument):
    # primary key 'pk'
    pk = db.StringField(max_length=100,default='')
    programe = db.StringField(max_length=100,default='')
    year = db.IntField(required=True, default=0)
    branch = db.StringField(max_length=100,default='')
    rollnumber = db.StringField(max_length=25,default='') #2K19/IT/10
    #roll = db.IntField(required=True, default=0)

    def __unicode__(self):
        return self.programe + ", " + self.year + ", " + self.branch + ", " + self.roll
    def __repr__(self):
        return self.programe + ", " + self.year + ", " + self.branch + ", " + self.roll
    def __str__(self):
        return self.programe + ", " + self.year + ", " + self.branch + ", " + self.roll
    def student_dict(self):
        return {
            'pk':self.pk   #  It is PK and index key in EmbeddedDocument department. It is used for edit update, delete opration.
            ,'Programe':self.programe
            ,'year':str(self.year)
            ,'Branch':self.branch
            ,'Roll Number':self.rollnumber
            #,'Roll Number':self.roll
        }

class University(db.EmbeddedDocument):
    # primary key 'pk'
    pk = db.StringField(max_length=100,default='')
    name = db.StringField(max_length=200,default='')  # Delhi Technological University"
    #url = db.URLField()  # "http://www.dtu.ac.in"
    url = db.StringField(max_length=300,default='')
    #office = db.EmbeddedDocumentListField(Add) # Multiple offices like east campus
    office = db.EmbeddedDocumentListField(Add)

    def __unicode__(self):
        return self.name 
    def __repr__(self):
        return self.name 
    def __str__(self):
        return self.name
    def university_dict(self):
        ad = []
        for i in self.office:
            ad.append(i.__dict__())
        return {
            'pk':self.pk   #  It is PK and index key in EmbeddedDocument department. It is used for edit update, delete opration.
            ,'Name':self.name
            ,'Url':self.url
            ,'Office':ad
        }

class Department(db.EmbeddedDocument):
    # primary key 'pk'
    pk = db.StringField(max_length=100,default='')
    name = db.StringField(max_length=200,default='')  # "Information Technology",
    # "http://www.dtu.ac.in/Web/Departments/InformationTechnology/about/",
    #url = db.URLField()
    url = db.StringField(max_length=300,default='')
    office = db.EmbeddedDocumentListField(Add)

    def __unicode__(self):
        return self.name 
    def __repr__(self):
        return self.name 
    def __str__(self):
        return self.name 
    def department_dict(self):
        ad = []
        for i in self.office:
            ad.append(i.__dict__())
        return {
            'pk':self.pk   #  It is PK and index key in EmbeddedDocument department. It is used for edit update, delete opration.
            ,'Name':self.name
            ,'Url':self.url
            ,'Office':ad
        }


class SponsoredProjects(db.EmbeddedDocument):
    pk = db.StringField(max_length=100,default='')
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
            'pk':self.pk,   # It is PK and index key in EmbeddedDocument sponsoredprojects. It is used for edit update, delete opration.
            'Title':self.title
            ,'name':self.name
            ,'Duration':self.duration
            ,'Amount':self.amount
        }


class Patents(db.EmbeddedDocument):
    pk = db.StringField(max_length=100,default='')
    countary = db.StringField(max_length=200,default='')
    title = db.StringField(max_length=200,default='')
    year = db.IntField(required=True, default=0)
    #url = db.URLField()
    url = db.StringField(max_length=300,default='')

    def __unicode__(self):
        return self.title 
    def __repr__(self): 
        return self.title 
    def __str__(self): 
        return self.title 
    def __dict__(self):
        return {
            'pk':self.pk   #  It is PK and index key in EmbeddedDocument patents. It is used for edit update, delete opration.
            ,'Title':self.title
            ,'url':self.url
            ,'Year':str(self.year)
            ,'Countary':self.countary
        }


class IndustryCollaboration(db.EmbeddedDocument):
    pk = db.StringField(max_length=100,default='')
    name = db.StringField(max_length=200,default='')  # "Samsung India",
    #url = db.URLField()  # "https://www.samsung.com/in/home/",
    url = db.StringField(max_length=300,default='')
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
            'pk':self.pk   #  It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
            ,'Name':self.name
            ,'url':self.url
            ,'MoU':self.mou
            ,'Collaboration':self.collaboration
            ,'Title':self.title
        }


class StartUp(db.EmbeddedDocument):
    pk = db.StringField(max_length=100,default='')
    name = db.StringField(max_length=200,default='')  # "DezWebApp",
    #url = db.URLField()
    url = db.StringField(max_length=300,default='')
    funding = db.StringField(max_length=200,default='')  # "Self"

    def __unicode__(self):
        return self.name 
    def __repr__(self):
        return self.name 
    def __str__(self):
        return self.name
    def __dict__(self):
        return {
            'pk':self.pk   #  It is PK and index key in EmbeddedDocument startup. It is used for edit update, delete opration.
            ,'Name':self.name
            ,'Url':self.url
            ,'Funding':self.funding
        }


class Books(db.EmbeddedDocument):
    pk = db.StringField(max_length=100,default='')
    # "Software Reliability Modeling and Selection",
    title = db.StringField(max_length=200,default='')
    # "Book describes selection of software reliability models",
    description = db.StringField(max_length=500,default='')
    year = db.IntField(required=True, default=0)  # 2012
    # "https://www.amazon.in/Software-Reliability-Modeling-Selection-Sharma/dp/3848481235",
    #url = db.URLField()
    url = db.StringField(max_length=300,default='')
    publisher = db.StringField(max_length=200,default='')  # "Lambert"

    def __unicode__(self):
        return self.title 
    def __repr__(self):
        return self.title 
    def __str__(self): 
        return self.title 
    def __dict__(self):
        return {
            'pk':self.pk   # def __str__(self): return self.name  It is PK and index key in EmbeddedDocument books. It is used for edit update, delete opration.
            ,'Title':self.title
            ,'Url':self.url
            ,'Year':str(self.year)
            ,'Description':self.description
            ,'Publisher':self.publisher
        }


class Awards(db.EmbeddedDocument):
    pk = db.StringField(max_length=100,default='')
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
            'pk':self.pk   #  It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
            ,'Name':self.name
            ,'Description':self.description
            ,'Certificate':self.certificate
        }


class SocialImpact(db.EmbeddedDocument):
    pk = db.StringField(max_length=100,default='')
    # "App for election commission of india vote chandni chowk",
    name = db.StringField(max_length=200,default='')
    # "https://play.google.com/store/apps/details?id=in.gov.delhi.votechandnichowk&hl=en_IN&gl=US"
    #url = db.URLField()
    url = db.StringField(max_length=300,default='')

    def __unicode__(self):
        return self.name 
    def __repr__(self):
        return self.name 
    def __str__(self):
        return self.name
    def __dict__(self):
        return {
            'pk':self.pk   #  It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
            ,'Name':self.name
            ,'Url':self.url
        }


class TechnologyTransfer(db.EmbeddedDocument):
    pk = db.StringField(max_length=100,default='')
    name = db.StringField(max_length=200,default='')  # "DezWebApp",
    technology = db.StringField(max_length=200,default='')  # "5G",
    #url = db.URLField()
    url = db.StringField(max_length=300,default='')
    royalty = db.StringField(max_length=200,default='')

    def __unicode__(self):
        return self.name 
    def __repr__(self):
        return self.name 
    def __str__(self):
        return self.name
    def __dict__(self):
        return {
            'pk':self.pk   # It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
            ,'Name':self.name
            ,'Technology':self.technology
            ,'Url':self.url
            ,'Royalty':self.royalty
        }


# Define the User db.Document.
# NB: Make sure to add flask_user UserMixin !!!
class User(db.Document, UserMixin):
    active = db.BooleanField(default=True)
     #####Relationships
    #roles = db.EmbeddedDocumentListField(StringField(), default=[])
    roles = db.ListField(StringField(), default=[])
    #papers = db.EmbeddedDocumentListField(ObjectIdField())
    #####papers = db.ListField(ReferenceField(Paper))
    papers = db.ListField(ObjectIdField(), default=[])
    ######pep = db.ReferenceField(Paper)
    
    # User authentication information
    username = db.StringField(max_length=50,default='') # app.config["MAXNUNAME"]
    password = db.StringField(max_length=100,default='') # due to hash pasword length is grater then actual password

    # User information
    fname = db.StringField(max_length=25,default='')
    mname = db.StringField(max_length=25,default='')
    lname = db.StringField(max_length=25,default='')
    title = db.StringField(max_length=9,default='') # Mr Ms Dr.
    gender = db.StringField(max_length=25,default='')
    aadhar = db.StringField(max_length=12,default='')
    # dob = db.DateTimeField(null=True)
    # date_created = db.DateTimeField(default=datetime.utcnow,
    #                                     help_text='date the User was created')
    directory = db.StringField(max_length=100,default='')
    photo = db.StringField(max_length=25,default='')
    qualifications = db.StringField(max_length=100,default='')
    areas_of_interest = db.StringField(max_length=300,default='')
    bio = db.StringField(max_length=500,default='')
    publications = db.StringField(max_length=500,default='')
    
    ############ List property of user object at level 1
    contacts = db.EmbeddedDocumentListField(Add)  # office/home/parmanent/old campus/ east campus etc
    
    ############ List property of user object at level 2 with primary key 'pk'
    # user(level 0)
    # -> (level 1) user attribute list given below (faculty to technologytransfer)  
    # -> (level 2) list of Models Faculty to TechnologyTransfer with primary key pk
    faculty = db.EmbeddedDocumentListField(Faculty) # pk = email
    student = db.EmbeddedDocumentListField(Student) # pk = roll
    university = db.EmbeddedDocumentListField(University) # pk = university name
    department = db.EmbeddedDocumentListField(Department) # pk = dept name

    sponsoredprojects = db.EmbeddedDocumentListField(SponsoredProjects) # pk = project name
    patents = db.EmbeddedDocumentListField(Patents) # pk = patent number
    industrycollaboration = db.EmbeddedDocumentListField(IndustryCollaboration) # pk = collab name
    startup = db.EmbeddedDocumentListField(StartUp) # pk = startup name
    books = db.EmbeddedDocumentListField(Books) # pk = book title
    awards = db.EmbeddedDocumentListField(Awards) # pk = award name + year
    socialimpact = db.EmbeddedDocumentListField(SocialImpact) # pk = social work + year
    technologytransfer = db.EmbeddedDocumentListField(TechnologyTransfer) # pk = tech name
    ############ List property of user object with primary key 'pk'

    def personal_dict(self):
        return {
            'First Name':self.fname
            ,'Middle Name':self.mname
            ,'Last Name':self.lname
            ,'title':self.title
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
        cont = []
        for i in self.contacts:
            cont.append(i.__dict__())
        dep = []
        for i in self.department:
            dep.append(i.__dict__())
        flt = []
        for i in self.faculty:
            flt.append(i.__dict__())
        stu = []
        for i in self.student:
            stu.append(i.__dict__())
        uni = []
        for i in self.university:
            uni.append(i.__dict__())
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
            ,'Dept':dep
            ,'Qualifications':self.qualifications
            ,'Areas of Interest':self.areas_of_interest
            ,'Biography':self.bio
            ,'Publications':self.publications
            ,'Faculty':flt
            ,'Student':stu
            ,'University':uni
            ,'Contacts':cont
            ,'Sponsored Projects':sp
            ,'Patents':pat
            ,'Industry Collaboration':ic
            ,'Startup':stup
            ,'Books':bo
            ,'Awards':aw
            ,'Social Impact':si
            ,'Technology Transfer':tt
        }