#from flask_mongoengine import MongoEngine
# from mongoengine import Document
# from mongoengine import DateTimeField, StringField, ReferenceField, ListField, BooleanField
#from flask_login import UserMixin
from flask_wtf import Form, FlaskForm
from wtforms import FormField, BooleanField, StringField,TextAreaField, PasswordField, validators, SubmitField, EmailField, HiddenField, SelectField, IntegerField, DecimalField, DateTimeField
from wtforms.validators import DataRequired, Regexp, InputRequired, Length, NumberRange
from wtforms.widgets import URLInput, Input
from flask_wtf.file import FileField
# from flask_user import UserManager
# from .app import db #, app # from .app import app # from __init__ import db

# # # Database However, using MongoEngine can come at an additional cost when misused
# # using the ORM in a for loop rather than batching up commands in PyMongo
# db = MongoEngine()  # Database Name db is declared for scope not created


# # Classes for Data Modleing
# # def createModelsdb(MongoEngine db):


# # Define the User registration form
# # It augments the Flask-User RegisterForm with additional fields
# class MyRegisterForm(RegisterForm):
#     first_name = StringField('First name', validators=[
#         validators.DataRequired('First name is required')])
#     last_name = StringField('Last name', validators=[
#         validators.DataRequired('Last name is required')])

# name    = StringField('Full Name', [validators.required(), validators.length(max=10)])
# address = TextAreaField('Mailing Address', [validators.optional(), validators.length(max=200)])
# Define the User profile form
class UserLoginForm(FlaskForm):
    username = StringField('email', validators=[
                           InputRequired(), Length(min=8, max=100)])
    password = PasswordField('Re Type Password', validators=[
                             InputRequired(), Length(min=8, max=30)])
    # # ,validators.EqualTo('confirm', message='Passwords must match')
    # validators.DataRequired('Password name is required')])
    submit = SubmitField('LogIn')

class UserNewForm(FlaskForm):
    username = StringField('Email', validators=[
                           InputRequired(), Length(min=8, max=100)])
    passwd = StringField('Password', validators=[
                           InputRequired(), Length(min=8, max=30)])
    password = PasswordField('Re Type Password', validators=[
                             InputRequired(), Length(min=8, max=30)])
    # # ,validators.EqualTo('confirm', message='Passwords must match')
    # validators.DataRequired('Password name is required')])
    submit = SubmitField('Create User')

# Select Target User to Edit/Modify
class UserTargetForm(FlaskForm):
    usertarget = StringField('Target User Email', validators=[
                           InputRequired(), Length(min=8, max=100)])
    submit = SubmitField('Select Target User email')

# Define the User Role form
class UserRoleForm(FlaskForm):
    role = StringField('Role', validators=[
        InputRequired(), Length(min=3, max=25)])
    submit = SubmitField('Save')

# Define the User profile form
# User information


class UserInformation(FlaskForm):
    fname = StringField('First Name', validators=[
        validators.DataRequired('First Name is required')])
    mname = StringField('Middle name')
    lname = StringField('Last Name')
    title = StringField('Title', validators=[
        validators.DataRequired('Title is required')])
    directory = StringField('User Directory')
    photo = StringField('Path to photo file', validators=[
        validators.DataRequired('Path to photo file is required')])
    qualifications = StringField('Qualifications', validators=[
        validators.DataRequired('qualifications are required')])
    areas_of_interest = StringField('Areas of Interest', validators=[
        validators.DataRequired('Areas of Interest are required')])
    bio = StringField('Bio', validators=[
        validators.DataRequired('Biography is required')])
    publications = StringField('Publications', validators=[
        validators.DataRequired('Publications is required')])
    submit = SubmitField('Save')

class UploadForm(FlaskForm):
    file = FileField()
    submit = SubmitField('Upload')

class SocialMediaAddressForm(FlaskForm):
    desc = StringField('Social Media Platform Name(web/googlescholar/linkedin/facebook/youtube/twitter/whatsapp/signal/telegram/koo/orcid id/etc)', validators=[
        validators.DataRequired('Social Media Platform Name')])
    link = StringField('Social Media Platform Link/Handle/Address', validators=[
        validators.DataRequired('Social Media Platform Link/Handle/Address')])
    submit = SubmitField('Save Social Media Address')

class AddressForm(FlaskForm): #AddressForm(Form):
    addtype = StringField('Coressponding, Permanent, Office, Personal, Online, Professonal etc)', validators=[
        validators.DataRequired('Address Type')])
    add = StringField('Postal Address', validators=[
        validators.DataRequired('Postal Address')])
    state = StringField('State', validators=[
        validators.DataRequired('State')])
    pin = StringField('Pin', validators=[
        validators.DataRequired('Postal Pin Code ')])
    countary = StringField('Country', validators=[
        validators.DataRequired('Country')])
    phone = StringField('Mobile Phonr Number', validators=[
        validators.DataRequired('Mobile Phonr Number')])
    land = StringField('Land Line NUmber', validators=[
        validators.DataRequired('Land Line NUmber')])
    email = EmailField('Email Address', validators=[
        validators.DataRequired('email')])
    #completeadd = TextAreaField(u'Complete Address', [validators.optional(), validators.length(max=200)])
    submit = SubmitField('Save Address')

class UserContactsForm(FlaskForm):
    contact = FormField(AddressForm)
    submit = SubmitField('Save')

#################################  Faculty   #######################


class UserFacultyForm(FlaskForm):
    position = StringField('Position', validators=[
        validators.DataRequired('Position is required')])
    post = StringField('Post', validators=[
        validators.DataRequired('Post is required')])
    empcode = StringField('Employee Code', validators=[
        validators.DataRequired('Employee Code is required')])
    submit = SubmitField('Save')


class UserStudentForm(FlaskForm):
    programe = StringField('University Programe', validators=[
        validators.DataRequired('University Programe is required')])
    year = StringField('Admission Year', validators=[
        validators.DataRequired('Admission Year is required')])
    branch = StringField('Branch', validators=[
        validators.DataRequired('Branch is required')])
    # number = StringField('Class Roll Number', validators=[
    #     validators.DataRequired('Class Roll Number is required')])
    rollnumber = StringField('Student Roll Number', validators=[
        validators.DataRequired('Student Roll Number is required')])
    submit = SubmitField('Save')


class UserUniversityForm(FlaskForm):
    name = StringField('University Name', validators=[
        validators.DataRequired('University Name is required')])
    url = StringField('University url', validators=[
        validators.DataRequired('University url is required')])
    ######## office address #############
    #office = FormField(AddressForm)
    submit = SubmitField('Save')


class UserDepartmentForm(FlaskForm):
    name = StringField('Department Name', validators=[
        validators.DataRequired('Department Name is required')])
    url = StringField('Department url', validators=[
        validators.DataRequired('Department url is required')])
    ######## office address #############
    #office = FormField(AddressForm)
    submit = SubmitField('Save')


class UserSponsoredProjectsForm(FlaskForm):
    title = StringField('Sponsored Projects Title', validators=[
        validators.DataRequired('Sponsored Projects Title is required')])
    name = StringField('Sponsored Projects Name', validators=[
        validators.DataRequired('Department Name is required')])
    duration = StringField('Sponsored Projects Duration', validators=[
        validators.DataRequired('Department Name is required')])
    amount = StringField('Sponsored Projects Amount', validators=[
        validators.DataRequired('Department Name is required')])
    submit = SubmitField('Save')


class UserPatentsForm(FlaskForm):
    countary = StringField('Patent Countary', validators=[
        validators.DataRequired('Sponsored Projects Title is required')])
    title = StringField('Patent Title', validators=[
        validators.DataRequired('Sponsored Projects Title is required')])
    year = StringField('Patent Year', validators=[
        validators.DataRequired('Sponsored Projects Title is required')])
    url = StringField('Patent url', validators=[
        validators.DataRequired('Sponsored Projects Title is required')])
    submit = SubmitField('Save')


class UserIndustryCollaborationForm(FlaskForm):
    name = StringField('Industry Collaboration Name', validators=[
        validators.DataRequired('Sponsored Projects Title is required')])
    url = StringField('Industry Collaboration url', validators=[
        validators.DataRequired('Sponsored Projects Title is required')])
    mou = StringField('Industry Collaboration MOU', validators=[
        validators.DataRequired('Sponsored Projects Title is required')])
    collaboration = StringField('Industry Collaboration Details', validators=[
        validators.DataRequired('Sponsored Projects Title is required')])
    title = StringField('Industry Collaboration Titlle', validators=[
        validators.DataRequired('Sponsored Projects Title is required')])
    submit = SubmitField('Save')


class UserStartUpForm(FlaskForm):
    name = StringField('StartUp Name', validators=[
        validators.DataRequired('Sponsored Projects Title is required')])
    url = StringField('StartUp url', validators=[
        validators.DataRequired('Sponsored Projects Title is required')])
    funding = StringField('StartUp Funding', validators=[
        validators.DataRequired('Sponsored Projects Title is required')])
    submit = SubmitField('Save')


class UserBooksForm(FlaskForm):
    title = StringField('Book Title', validators=[
        validators.DataRequired('Sponsored Projects Title is required')])
    description = StringField('Book Description', validators=[
        validators.DataRequired('Sponsored Projects Title is required')])
    year = StringField('Book Year', validators=[
        validators.DataRequired('Sponsored Projects Title is required')])
    url = StringField('Book url', validators=[
        validators.DataRequired('Sponsored Projects Title is required')])
    publisher = StringField('Book Publisher', validators=[
        validators.DataRequired('Sponsored Projects Title is required')])
    submit = SubmitField('Save')


class UserAwardsForm(FlaskForm):
    name = StringField('Award Name', validators=[
        validators.DataRequired('Sponsored Projects Title is required')])
    description = StringField('Award Description', validators=[
        validators.DataRequired('Sponsored Projects Title is required')])
    certificate = StringField('Award Certificate', validators=[
        validators.DataRequired('Sponsored Projects Title is required')])
    submit = SubmitField('Save')


class UserSocialImpactForm(FlaskForm):
    name = StringField('Social Impact Name', validators=[
        validators.DataRequired('Sponsored Projects Title is required')])
    url = StringField('Social Impact Name', validators=[
        validators.DataRequired('Sponsored Projects Title is required')])
    submit = SubmitField('Save')


class UserTechnologyTransferForm(FlaskForm):
    name = StringField('Technology Transfer Name', validators=[
        validators.DataRequired('Sponsored Projects Title is required')])
    technology = StringField('Technology Details', validators=[
        validators.DataRequired('Sponsored Projects Title is required')])
    url = StringField('Technology Transfer url', validators=[
        validators.DataRequired('Sponsored Projects Title is required')])
    royalty = StringField('Technology Transfer Royalty', validators=[
        validators.DataRequired('Sponsored Projects Title is required')])
    submit = SubmitField('Save')



#####################################################################################################################
###################################### Paper Models  ##############################################################
class PaperSelectForm(FlaskForm):
    paperseleted = SelectField('Select Paper', coerce=int, validators=[InputRequired('Select One Option')])
    submit = SubmitField('Select')

class PaperFileUplodedForm(FlaskForm):
    file = FileField('File name', validators=[
        validators.DataRequired('File Name used to store file in Cloud/Server')])
    desc = StringField('Description of file', validators=[
        validators.DataRequired('Any Importan details / Messages')])
    submit = SubmitField('Upload')

class LinkDescForm(FlaskForm):
    link = StringField('Refrance Paper Link', validators=[
        validators.DataRequired('Refrance Paper Link is required')])
    desc = StringField('Link Description', validators=[
        validators.DataRequired('Refrance Paper Link Description')])
    submit = SubmitField('Save')

##########################   rp = db.EmbeddedDocumentListField(ResearchProblem)
class ResearchProblemForm(FlaskForm):
    statment =  StringField('Problem Statment of New Paper', validators=[
        validators.DataRequired('New Paper Problem Statment is required')])
    desc = StringField('Discription of Problem Statment of New Paper', validators=[
        validators.DataRequired('Discription of Problem Statment of New Paper')])
    submit = SubmitField('Save')

###########################   authors = db.EmbeddedDocumentListField(PaperPerson)
# email = db.StringField(max_length=100,default='') # logicalkey
#     name = db.StringField(max_length=100,default='')
#     user_id = db.ObjectIdField() # ref to objectid of user document if any
#     title = db.StringField(max_length=10,default='')# Mr. Ms. Miss
#     position = db.StringField(max_length=20,default='')# Dr. Prof
#     corresponding = db.BooleanField(required=True, default=False)
#     sequence = db.IntField(required=True, default=0)
#     gender = db.StringField(max_length=25,default='')
#     affiliation = db.EmbeddedDocumentListField(LinkDesc)
#     ph 
class PaperPersonForm(FlaskForm):
    email = StringField('Email', validators=[
        validators.DataRequired('Email of Author/paper person')])
    name = StringField('Full Name', validators=[
        validators.DataRequired('Full Name of Author/paper person')])
    user_id = StringField('User id of Person', validators=[
        validators.DataRequired('User id of Author from User Document in Mongodb if any otherwise None')])
    title = StringField('Author\'s Title', validators=[
        validators.DataRequired('Auther\'s Title eg. Prof. Dr. Mrs. Mr.')])
    position = StringField('Administrative Position', validators=[
        validators.DataRequired('Position in Administration eg. VC, Dean, Hod')])
    corresponding = BooleanField(label='Corresponding', validators=[
        validators.optional()],false_values=(False, "false", ""))#,default="checked"
    sequence = IntegerField('Author\'s Sequence', validators=[
        validators.NumberRange(min=0, max=10), validators.DataRequired('Refrance Paper Year of Publication')])
    gender = StringField('Gender', validators=[
        validators.DataRequired('Gender')])
    # affiliation = StringField('Affiliation', validators=[
    #     validators.DataRequired('Affiliation')])
    ph = StringField('Phone Number', validators=[
        validators.DataRequired('Phone Number')])
    submit = SubmitField('Save')
class PaperPersonFormEdit(FlaskForm):
    email = StringField('Email', validators=[
        validators.DataRequired('Email of Author/paper person')])
    name = StringField('Full Name', validators=[
        validators.DataRequired('Full Name of Author/paper person')])
    title = StringField('Author\'s Title', validators=[
        validators.DataRequired('Auther\'s Title eg. Prof. Dr. Mrs. Mr.')])
    position = StringField('Administrative Position', validators=[
        validators.DataRequired('Position in Administration eg. VC, Dean, Hod')])
    corresponding = BooleanField(label='Corresponding', validators=[
        validators.optional()],false_values=(False, "false", "")) #,default="checked"
    # corresponding = StringField('Corresponding', validators=[
    #     validators.DataRequired('True or False')]) 
    sequence = IntegerField('Author\'s Sequence', validators=[
        validators.NumberRange(min=0, max=10), validators.DataRequired('Refrance Paper Year of Publication')])
    gender = StringField('Gender', validators=[
        validators.DataRequired('Gender')])
    # affiliation = StringField('Affiliation', validators=[
    #     validators.DataRequired('Affiliation')])
    ph = StringField('Phone Number', validators=[
        validators.DataRequired('Phone Number')])
    submit = SubmitField('Save')

#########################  
class PaperRefFileForm(FlaskForm):
    title = StringField('Refrance Paper Title', validators=[
        validators.DataRequired('Refrance Paper Title is required')])
    articaltype = StringField('Artical type', validators=[
        validators.DataRequired('Refrance Paper Type (Journal Paper/book/confrence)')])
    year = IntegerField('Year', validators=[
        validators.NumberRange(min=1900, max=2050), validators.DataRequired('Refrance Paper Year of Publication')])
    # year = StringField('Year', validators=[
    #     validators.DataRequired('Refrance Paper Year of Publication')])
    doi = StringField('Digital Object Identifier', validators=[
        validators.DataRequired('Digital Object Identifier')])
    bibtext = StringField('bibtex', validators=[
        validators.DataRequired('bibtex')])
    desc = StringField('Discription', validators=[
        validators.DataRequired('Discription')])
    submit = SubmitField('Save')

class PaperDiscussionBoardCommentForm(FlaskForm):
    desc = StringField('Discription', validators=[
        validators.DataRequired('Discription')])

class PaperSubmittedinJournalForm(FlaskForm):
    name = StringField('Name of Journal', validators=[
        validators.DataRequired('Name of Journal')])
    mode = StringField('Open access / free / hybried / paied etc', validators=[
        validators.DataRequired('Open access / free / hybried / paied etc')])
    publisher = StringField('Publisher of Journal', validators=[
        validators.DataRequired('Publisher of Journal')])
    indexing = StringField('SCI / SCIE / ESCI / Scoups / Others', validators=[
        validators.DataRequired('SCI / SCIE / ESCI / Scoups / Others')])
    score = DecimalField('Journal Score', validators=[
        validators.DataRequired('Journal Score')])
    username = StringField('Journal Login Username', validators=[
        validators.DataRequired('Journal Login Username')])

class PaperSubmittedinConferenceForm(FlaskForm):
    name = StringField('Name of Conference', validators=[
        validators.DataRequired('Name of Conference')])
    confnumber = StringField('Conference Number if any', validators=[
        ])
    deadline  = DateTimeField('Submission Deadline Date and Time', validators=[
        validators.DataRequired('submission Deadline date and time')])
    sdate  = DateTimeField('Conference is scheduled on date and time', validators=[
        validators.DataRequired('Conference is scheduled on date and time')])
    edate  = DateTimeField('Conference is closed on date and time', validators=[
        validators.DataRequired('Conference is closed on date and time')])
    city = StringField('City Name', validators=[
        validators.DataRequired('City Name')])
    confadd = StringField('Conference Address', validators=[
        validators.DataRequired('Conference Address')])
    publisher = StringField('Publisher of Journal', validators=[
        validators.DataRequired('Publisher of Journal')])
    indexing = StringField('SCI / SCIE / ESCI / Scoups / Others', validators=[
        validators.DataRequired('SCI / SCIE / ESCI / Scoups / Others')])
    score = DecimalField('Journal Score', validators=[
        validators.DataRequired('Journal Score')])
    username = StringField('Journal Login Username', validators=[
        validators.DataRequired('Journal Login Username')])

class AllocatePapertoUserForm(FlaskForm):
    title = StringField('Title of the Paper to be Assigned to User', validators=[
        validators.DataRequired('Title of the Paper to be Assigned to User')])
    submit = SubmitField('Assign')

class DeallocatePapertoUserForm(FlaskForm):
    title = StringField('Title of the Paper to be DeAllocate from User papers list', validators=[
        validators.DataRequired('Title of the Paper to be DeAllocate from User papers list')])
    submit = SubmitField('DeAllocate')

class PaperNewForm(FlaskForm):
    title = StringField('Title of New Paper', validators=[
        validators.DataRequired('New Paper Title is required')])
    status = StringField('Paper Status : Formulating / Simulation / Writing /Submitted / Comments Recived / Wating for reply / Accepted /Rejected', validators=[
        validators.DataRequired('New paper Status is required')])
    submit = SubmitField('Save')

class PaperDeleteForm(FlaskForm):
    title = StringField('Title of Paper to be Deleted', validators=[
        validators.DataRequired('Paper Title is required')])
    submit = SubmitField('Delete Paper')

class PaperEditForm(FlaskForm):
    title = StringField('Edit Paper Title', validators=[
        validators.DataRequired('Paper Title is required')])
    status = StringField('Change Paper Status : Formulating / Simulation / Writing /Submitted / Comments Recived / Wating for reply / Accepted /Rejected', validators=[
        validators.DataRequired('Change paper Status is required')])
    submit = SubmitField('Save')



class RPKeywordsForm(FlaskForm):
    desc = StringField('Keyword for Problem Statment of New Paper', validators=[
        validators.DataRequired('Keyword for Problem Statment for Problem Statment of New Paper is Required')])
    #link = URLInput('Web Link for Keyword if any otherwise leave empty')
    link = StringField('Web Link for Keyword if any otherwise leave empty')
                       #,validators=[validators.DataRequired('url is required'),Regexp('^(http|https):\/\/[\w.\-]+(\.[\w.\-]+)+.*$', 0,'URL must be a valid link')])
    submit = SubmitField('Save')
    
class RPAplicationsForm(FlaskForm):
    desc = StringField('Application Area for Problem Statment of New Paper', validators=[
        validators.DataRequired('Application Area for Problem Statment of New Paper is Required')])
    link = StringField('Web Link for Application Area if any otherwise leave empty')
    submit = SubmitField('Save')

class RPJournals_ConfForm(FlaskForm):
    desc = StringField('Target Journal/Conference for Problem Statment of New Paper', validators=[
        validators.DataRequired('Target Journal/Conference for Problem Statment of New Paper is Required')])
    link = StringField('Web Link for Target Journal/Conference if any otherwise leave empty')
    submit = SubmitField('Save')

class RPCode_LinksForm(FlaskForm):
    desc = StringField('Code/software for Problem Statment of New Paper', validators=[
        validators.DataRequired('Code/software for Problem Statment of New Paper is Required')])
    link = StringField('Web Link for Code/software if any otherwise leave empty')
    submit = SubmitField('Save')

class RPDataSets_linksForm(FlaskForm):
    desc = StringField('Data Set for Problem Statment of New Paper', validators=[
        validators.DataRequired('Data Set for Problem Statment of New Paper is Required')])
    link = StringField('Web Link for Data Set if any otherwise leave empty')
    submit = SubmitField('Save')

class RPPeoplesForm(FlaskForm):
    desc = StringField('Person/Peoples in the Area for Problem Statment', validators=[
        validators.DataRequired('Person/Peoples for Problem Statment of New Paper is Required')])
    link = StringField('Web Link for Person/Peoples if any otherwise leave empty')
    submit = SubmitField('Save')

class RPArticalsForm(FlaskForm):
    desc = StringField('Artical like white papers, magazine artical, blogs etc', validators=[
        validators.DataRequired('Artical for Problem Statment of New Paper is Required')])
    link = StringField('Web Link for Artical if any otherwise leave empty')
    submit = SubmitField('Save')

class RPResouresForm(FlaskForm):
    desc = StringField('Online Resources like professor,s page lab for Problem Statment of New Paper', validators=[
        validators.DataRequired('Online Resources for Problem Statment of New Paper is Required')])
    link = StringField('Web Link for Application Area if any otherwise leave empty')
    submit = SubmitField('Save')

class RPSocialmediaForm(FlaskForm):
    desc = StringField('Social Media Link for Problem Statment of New Paper', validators=[
        validators.DataRequired('Social Media Link for Problem Statment of New Paper is Required')])
    link = StringField('Social Media Link if any otherwise leave empty')
    submit = SubmitField('Save')