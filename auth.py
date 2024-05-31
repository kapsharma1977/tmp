from distutils.log import error
from hashlib import new
from flask import Blueprint, session, request, current_app, flash, render_template, redirect, url_for, render_template,  jsonify
#from flask_user import login_required, UserManager, UserMixin
from flask_login import login_manager, LoginManager, UserMixin, login_user, login_required, logout_user
from pymongo import ReturnDocument
# from flask.ext.mongoengine.wtf import model_form

# from . import bcrypt # circular import
from . import Add, Faculty, Student, University, Department, SponsoredProjects, Patents, IndustryCollaboration #Address, Contact,
# mongoengine, bcrypt, app
from . import StartUp, Books, Awards, SocialImpact, TechnologyTransfer, User, bcrypt #, db
from .models import UserLoginForm

auth = Blueprint('auth', __name__)


# @auth.route('/login', methods=['POST'])
# def login():
#     return 'Login'
# https://stackoverflow.com/questions/41854768/flask-bcrypt-attributeerror-module-object-has-no-attribute-ffi-deployed
# https://medium.com/@dmitryrastorguev/basic-user-authentication-login-for-flask-using-mongoengine-and-wtforms-922e64ef87fe
# https://flask-login.readthedocs.io/en/latest/#login-example
@auth.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    #session["id"] = None
    session["target_id"] = None # Target user id
    session["paper_id"] = None # Target paper id
    session["target_username"] = None
    #print("Logout")
    return redirect("/") #redirect(url_for('login'))

@ auth.route('/login', methods=['POST'])
def login():
    #print('login print')
    # and loginform.validate_on_submit():  # and form.validate_on_submit(): #form.validate():
    if request.method == 'POST':
        mail_e = request.form.get("email")
        paswd = request.form.get("password")
        #hashed = bcrypt.generate_password_hash(request.form.get("password")).decode('utf-8')
        # print(mail_e)
        #print(paswd)

        #usr = User.objects(username="kapil@ieee.org1").only("username").first()
        try:
            usr = User.objects(username=mail_e).first()
            if hasattr(usr, 'objects'):
                if bcrypt.check_password_hash(usr.password, paswd):
                    #session["id"] = usr.id
                    session["target_id"] = usr.id # Target user id
                    session["paper_id"] = None # Target paper id
                    # if len(usr.papers) > 0
                    #     session["paper_id"] = usr.papers[0] # Target paper id
                    session["target_username"] = mail_e
                    login_user(usr)
                    print(usr.home_dict())
                    #print("It Does Match :(")
                #else:
                    #print("It Does not Match :(")
        except:# OSError:
            print('error in login')
        flash('Thanks for Login')
    return redirect('/')

    


# @auth.route('/signup')
# def signup():
#     return 'Signup'


# @auth.route('/logout')
# def logout():
#     session["email"] = None
#     # return render_template('base.html')
#     return redirect('/')


@ auth.route('/resetpaswd', methods=['POST'])
#@login_required
def resetpaswd():
    if request.method == "POST":
        # recive data from form
        mail_e = request.form.get("email")
        oldpaswd = request.form.get("oldpassword")
        newpaswd = request.form.get("newpassword")

        hashed_newpaswd = bcrypt.generate_password_hash(
            newpaswd).decode('utf-8')
        try:
            # Retrive exsiting user
            usr = User.objects(username=mail_e).first()
            if hasattr(usr, 'objects') == True:
                if bcrypt.check_password_hash(usr.password, oldpaswd):
                    usr.password = hashed_newpaswd
                    usr.save()
                    logout()
                # usr.password = hashed_newpaswd
                # usr.save()
                # logout()
        except:
            flash("Error in update")
    return redirect('/')



# @auth.route('/createuser', methods=['GET', 'POST'])
# def CreateUser():
#     print('print auth creteuser')
#     userloginform = UserLoginForm()
#     if request.method == 'GET':
#         return render_template("createuser.html", form=userloginform)
#     if request.method == 'POST' and userloginform.validate_on_submit():
#         # username = request.form.get("username")
#         # password = request.form.get("password")

#         # # User information
#         # fname = request.form.get("fname")
#         # mname = request.form.get("mname")
#         # lname = request.form.get("lname")
#         # directory = request.form.get("directory")
#         # photo = request.form.get("photo")
#         # qualifications = request.form.get("qualifications")
#         # areas_of_interest = request.form.get("areas_of_interest")
#         # bio = request.form.get("bio")
#         # publications = request.form.get("publications")

#         ################  contact  ####################################################################
#         contact_web = request.form.get("contact_web")
#         contact_googlescholar = request.form.get("contact_googlescholar")
#         contact_linkedin = request.form.get("contact_linkedin")
#         contact_facebook = request.form.get("contact_facebook")
#         contact_youtube = request.form.get("contact_youtube")
#         contact_twiter = request.form.get("contact_twiter")

#         # -----------------------------------------------------------
#         # contact_address_home_add = request.form.get("contact_address_home_add")
#         # contact_address_home_state = request.form.get(
#         #     "contact_address_home_state")
#         # contact_address_home_pin = request.form.get("contact_address_home_pin")
#         # contact_address_home_countary = request.form.get(
#         #     "contact_address_home_countary")
#         # contact_address_home_phone = request.form.get(
#         #     "contact_address_home_phone")
#         # contact_address_home_email = request.form.get(
#         #     "contact_address_home_email")
#         contact_home = Add(
#             add=request.form.get("contact_address_home_add"), state=request.form.get("contact_address_home_state"), pin=request.form.get("contact_address_home_pin"), phone=request.form.get("contact_address_home_phone"), email=request.form.get("contact_address_home_email")
#         )
#         # contact_home.add = contact_address_home_add
#         # contact_home.state = contact_address_home_state
#         # contact_home.pin = contact_address_home_pin
#         # contact_home.countary = contact_address_home_countary
#         # contact_home.phone = contact_address_home_phone
#         # contact_home.email = contact_address_home_email

#         # -----------------------------------------------------
#         # contact_address_office_add = request.form.get(
#         #     "contact_address_office_add")
#         # contact_address_office_state = request.form.get(
#         #     "contact_address_office_state")
#         # contact_address_office_pin = request.form.get(
#         #     "contact_address_office_pin")
#         # contact_address_office_countary = request.form.get(
#         #     "contact_address_office_countary")
#         # contact_address_office_phone = request.form.get(
#         #     "contact_address_office_phone")
#         # contact_address_office_email = request.form.get(
#         #     "contact_address_office_email")
#         contact_office = Add(
#             add=request.form.get("contact_address_office_add"), state=request.form.get("contact_address_office_state"), pin=request.form.get("contact_address_office_pin"), countary=request.form.get("contact_address_office_countary"), phone=request.form.get("contact_address_office_phone"), email=request.form.get("contact_address_office_email")
#         )
#         # contact_office.add = contact_address_office_add
#         # contact_office.state = contact_address_office_state
#         # contact_office.pin = contact_address_office_pin
#         # contact_office.countary = contact_address_office_countary
#         # contact_office.phone = contact_address_office_phone
#         # contact_office.email = contact_address_office_email
#         address = Address(
#             home=contact_home, office=contact_office
#         )
#         # address.home = contact_home
#         # address.office = contact_office

#         _contact = Contact(
#             address=address, web=contact_web, googlescholar=contact_googlescholar, linkedin=contact_linkedin, facebook=contact_facebook, youtube=contact_youtube, twiter=contact_twiter
#         )

#         ################  Faculty ##############
#         # faculty_position = request.form.get("faculty_position")
#         # faculty_title = request.form.get("faculty_title")
#         # faculty_post = request.form.get("faculty_post")
#         # faculty_empcode = request.form.get("faculty_empcode")

#         faculty = Faculty(
#             position=request.form.get("faculty_position"), title=request.form.get("faculty_title"), post=request.form.get("faculty_post"), empcode=request.form.get("faculty_empcode")
#         )

#         ################  Student ##############
#         # student_programe = request.form.get("student_programe")
#         # student_year = request.form.get("student_year")
#         # student_branch = request.form.get("student_branch")
#         # student_number = request.form.get("student_number")
#         # student_roll = request.form.get("student_roll")

#         student = Student(
#             programe=request.form.get("student_programe"), year=request.form.get("student_year"), branch=request.form.get("student_branch"), number=request.form.get("student_number"), roll=request.form.get("student_roll")
#         )
#         ################  University ##############
#         # university_name = request.form.get("university_name")
#         # university_url = request.form.get("university_url")
#         # university_add = request.form.get("university_add")
#         # university_state = request.form.get("university_state")
#         # university_pin = request.form.get("university_pin")
#         # university_countary = request.form.get("university_countary")
#         # university_phone = request.form.get("university_phone")
#         # university_email = request.form.get("university_email")

#         # university = University()
#         # university.name = request.form.get("university_name")
#         # university.url = request.form.get("university_url")
#         # university_add = Add()
#         # university_add.add = request.form.get("university_add")
#         # university_add.state = request.form.get("university_state")
#         # university_add.pin = request.form.get("university_pin")
#         # university_add.countary = request.form.get("university_countary")
#         # university_add.phone = request.form.get("university_phone")
#         # university_add.email = request.form.get("university_email")

#         university_add = Add(
#             add=request.form.get("university_add"), state=request.form.get("university_state"), pin=request.form.get("university_pin"), countary=request.form.get("university_countary"), phone=request.form.get("university_phone"), email=request.form.get("university_email")
#         )

#         university = University(
#             name=request.form.get("university_name"), url=request.form.get("university_url"), office=university_add
#         )
#         ################  Department ##############
#         # department = Department()
#         # department.name = request.form.get("department_name")
#         # department.url = request.form.get("department_url")
#         # department_add = Add()
#         # department_add.add = request.form.get("department_add")
#         # department_add.state = request.form.get("department_state")
#         # department_add.pin = request.form.get("department_pin")
#         # department_add.countary = request.form.get("department_countary")
#         # department_add.phone = request.form.get("department_phone")
#         # department_add.email = request.form.get("department_email")
#         # department.office = department_add

#         department_add = Add(
#             add=request.form.get("department_add"), state=request.form.get("department_state"), pin=request.form.get("department_pin"), countary=request.form.get("department_countary"), phone=request.form.get("department_phone"), email=request.form.get("department_email")
#         )

#         department = Department(
#             name=request.form.get("department_name"), url=request.form.get("department_url"), office=department_add
#         )
#         ################  SponsoredProjects ##############
#         # sponsoredproject = SponsoredProjects()
#         # sponsoredproject.title = request.form.get("sponsoredprojects_title")
#         # sponsoredproject.name = request.form.get("sponsoredprojects_name")
#         # sponsoredproject.duration = request.form.get(
#         #     "sponsoredprojects_duration")
#         # sponsoredproject.amount = request.form.get("sponsoredprojects_amount")
#         # ################ Patents ##############
#         # patents = Patents()
#         # patents.countary = request.form.get("patents_countary")
#         # patents.title = request.form.get("patents_title")
#         # patents.year = request.form.get("patents_year")
#         # patents.url = request.form.get("patents_url")
#         # ################ IndustryCollaboration ##############
#         # industrycollaboration = IndustryCollaboration()
#         # industrycollaboration.name = request.form.get(
#         #     "industrycollaboration_name")
#         # industrycollaboration.url = request.form.get(
#         #     "industrycollaboration_url")
#         # industrycollaboration.mou = request.form.get(
#         #     "industrycollaboration_mou")
#         # industrycollaboration.collaboration = request.form.get(
#         #     "industrycollaboration_collaboration")
#         # industrycollaboration.title = request.form.get(
#         #     "industrycollaboration_title")
#         # ################ StartUp ##############
#         # startup = StartUp()
#         # startup.name = request.form.get("startup_name")
#         # startup.url = request.form.get("startup_url")
#         # startup.funding = request.form.get("startup_funding")
#         # ################ Books ##############
#         # book = Books()
#         # book.title = request.form.get("book_title")
#         # book.description = request.form.get("book_description")
#         # book.year = request.form.get("book_year")
#         # book.url = request.form.get("book_url")
#         # book.publisher = request.form.get("book_publisher")
#         # ################ Awards ##############
#         # awards = Awards()
#         # awards.name = request.form.get("awards_name")
#         # awards.description = request.form.get("awards_description")
#         # awards.certificate = request.form.get("awards_certificate")
#         # ################ SocialImpact ##############
#         # socialimpact = SocialImpact()
#         # socialimpact.name = request.form.get("socialimpact_name")
#         # socialimpact.url = request.form.get("socialimpact_url")
#         # ################ TechnologyTransfer ##############
#         # technologytransfer = TechnologyTransfer()
#         # technologytransfer.name = request.form.get("technologytransfer_name")
#         # technologytransfer.technology = request.form.get(
#         #     "technologytransfer_technology")
#         # technologytransfer.url = request.form.get("technologytransfer_url")
#         # technologytransfer.royalty = request.form.get(
#         #     "technologytransfer_royalty")

#         ######################### User Object #########################

#         user = User(username=request.form.get("username"), password=request.form.get("password"), fname=request.form.get("fname"), mname=request.form.get("mname"), lname=request.form.get("lname"), directory=request.form.get("directory"), photo=request.form.get("photo"), qualifications=request.form.get("qualifications"), areas_of_interest=request.form.get("areas_of_interest"), bio=request.form.get("bio"), publications=request.form.get("publications"), contact=_contact, faculty=faculty, student=student, university=university, department=department
#                     )
#         sponsoredproject_dic = {"title": request.form.get("sponsoredprojects_title"), "name": request.form.get(
#             "sponsoredprojects_name"), "duration": request.form.get("sponsoredprojects_duration"), "amount": request.form.get("sponsoredprojects_amount")}
#         user.sponsoredprojects.create(**sponsoredproject_dic)
#         patents_dic = {"countary": request.form.get("patents_countary"), "title": request.form.get(
#             "patents_title"), "year": request.form.get("patents_year"), "url": request.form.get("patents_url")}
#         user.patents.create(**patents_dic)
#         industrycollaboration_dic = {"name": request.form.get("industrycollaboration_name"), "url": request.form.get("industrycollaboration_url"), "mou": request.form.get(
#             "industrycollaboration_mou"), "collaboration": request.form.get("industrycollaboration_collaboration"), "title": request.form.get("industrycollaboration_title")}
#         user.industrycollaboration.create(**industrycollaboration_dic)
#         startup_dic = {"name": request.form.get("startup_name"), "url": request.form.get(
#             "startup_url"), "funding": request.form.get("startup_funding")}
#         user.startup.create(**startup_dic)
#         book_dic = {"title": request.form.get("book_title"), "description": request.form.get("book_description"), "year": request.form.get(
#             "book_year"), "url": request.form.get("book_url"), "publisher": request.form.get("book_publisher")}
#         user.books.create(**book_dic)
#         award_dic = {"name": request.form.get("awards_name"), "description": request.form.get(
#             "awards_description"), "certificate": request.form.get("awards_certificate")}
#         user.awards.create(**award_dic)
#         socialimpact_dic = {"name": request.form.get(
#             "socialimpact_name"), "url": request.form.get("socialimpact_url")}
#         user.socialimpact.create(**socialimpact_dic)
#         technologytransfer_dic = {"name": request.form.get("technologytransfer_name"), "technology": request.form.get(
#             "technologytransfer_technology"), "url": request.form.get("technologytransfer_url"), "royalty": request.form.get("technologytransfer_royalty")}
#         user.technologytransfer.create(**technologytransfer_dic)
#         # user.username = request.form.get("username")
#         # user.password = request.form.get("password")
#         # user.fname = request.form.get("fname")
#         # user.mname = request.form.get("mname")
#         # user.lname = request.form.get("lname")
#         # user.directory = request.form.get("directory")
#         # user.photo = request.form.get("photo")
#         # user.qualifications = request.form.get("qualifications")
#         # user.areas_of_interest = request.form.get("areas_of_interest")
#         # user.bio = request.form.get("bio")
#         # user.publications = request.form.get("publications")

#         # user.contact = contact
#         # user.faculty = faculty
#         # user.student = student
#         # user.university = university
#         # user.department = department

#         # user.sponsoredsrojects = sponsoredproject
#         # user.patents = [patents]
#         # user.industrycollaboration = [industrycollaboration]
#         # user.startup = [startup]
#         # user.books = [book]
#         # user.awards = [awards]
#         # user.socialimpact = [socialimpact]
#         # user.technologytransfer = [technologytransfer]

#         user.save()
#         flash('Thanks for Login')
#         return redirect('/')