#from curses import mouseinterval
from hashlib import new
from unicodedata import name
from flask import Blueprint, session, request, current_app, flash, render_template, redirect, url_for, render_template,  jsonify, render_template_string
# , login_manager, LoginManager, UserMixin, login_user, logout_user,
from flask_login import current_user, login_required
#from wtforms import BooleanField, StringField, PasswordField, validators, SubmitField, EmailField
#from flask_user import login_required, UserManager, UserMixin
from pymongo import ReturnDocument
import json
# from flask.ext.mongoengine.wtf import model_form

# from . import bcrypt # circular import
from . import Add, Address, Contact, Faculty, Student, University, Department, SponsoredProjects, Patents, IndustryCollaboration
# mongoengine, bcrypt, app
from . import StartUp, Books, Awards, SocialImpact, TechnologyTransfer, db, bcrypt, csrf, User
from .models import UserContactsForm, UserLoginForm, UserFacultyForm, UserStudentForm, UserUniversityForm, UserDepartmentForm, UserSponsoredProjectsForm
from .models import  UserPatentsForm, UserIndustryCollaborationForm, UserStartUpForm, UserBooksForm, UserAwardsForm, UserSocialImpactForm, UserTechnologyTransferForm, UserInformation, UserRoleForm, UserNewForm

users = Blueprint('users', __name__)


edit_create_view = """
                {% extends "base.html" %} {% block content %}
                
                {% if key_str != None %}
                    <form action="{{ url_for(fn_target, key_str = key_str) }}" method="POST">
                {% else %}
                    <form action="{{ url_for(fn_target) }}" method="POST">
                {% endif %}
                {{ form.hidden_tag() }}
                {{ form.csrf_token }}
                {% for field in form %}
                <div class="form-group row mb-3">
                    {% if field.type != 'SubmitField' %}
                        {% if field.id != 'csrf_token' %}
                            <label for="{{ field.id }}" class="control-label col-sm-2 col-form-label ms-5">{{ field.label.text|safe }}</label>
                            <div class="col-sm-10 mx-5">
                            {{ field(class_='form-control') }}
                            </div>
                        {% endif %}
                    {% else %}
                        <input type="submit" class="btn btn-primary mx-4 form-control" value="{{ field.label.text|safe }}" 
                        {% if tabindex %}
                            tabindex="{{ tabindex }}" 
                        {% endif %}
                    {% endif %}
                </div>
                {% endfor %}
                </form>
                {% endblock %}
            """


# @users.route('/createuser', methods=['GET', 'POST'])
# @login_required
# def createuser():
#     print('print Users creteuser')
#     userloginform = UserLoginForm()
#     if request.method == 'GET':
#         return render_template('/user/createuser.html', form=userloginform)
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
#         contact_twitter = request.form.get("contact_twiter")

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
#             address=address, web=contact_web, googlescholar=contact_googlescholar, linkedin=contact_linkedin, facebook=contact_facebook, youtube=contact_youtube, twitter=contact_twitter
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


###################################
# userdetails_view = """
#                 {% extends "base.html" %} {% block content %}
#                 <a href="{{url_for('users.sponsoredprojectscreate')}}">Add SponsoredProjects</a>
                
#                 <div class="container">
#                     <div class="row mt-5">

#                         {% for item in sponsoredprojects %}
#                             <div class="col-md-4">
#                                 <div class="card bg-dark text-center text-white">
#                                     <div class="card-header fw-bold fs-2">
#                                         <a href="{{item.url}}">{{item.title}}</a> 
#                                     </div>
#                                     <div class="card-body">
#                                         <h5 class="card-title fs-3">{{item.title}} <span class="text-success">/ 2022</span></h5>
#                                         <ul class="list-unstyled">
#                                             <li>{{item.countary}}</li>
#                                             <li>{{item.year}}</li>
#                                             <li>{{item.url}}</li>
#                                         </ul>
#                                         <a href="{{url_for('users.sponsoredprojectsedit', key_str = item.title)}}" >Edit</a>
#                                         <a href="{{url_for('users.sponsoredprojectsdelete', key_str = item.title)}}" >Delete</a>
#                                     </div>
#                                 </div>
#                             </div>
#                         {% endfor %}
                    
#                     </div>
# 			    </div>
                
#                 {% endblock %}
#             """
# edit_create_userdetails_view = """
#             {% extends "base.html" %} {% block content %}
                
#                 <form action="{{ url_for('users.userdetails') }}" method="POST">
#                     {{ form.hidden_tag() }}

#                     <div class="mb-3 mt-4">
#                         <label for="fname" class="form-label">First Name</label>
#                         <input type="text" class="form-control" id="fname" name="fname" />
#                     </div>
#                     <div class="mb-3">
#                         <label for="mname" class="form-label">Midle Name</label>
#                         <input type="text" class="form-control" id="mname" name="mname" />
#                     </div> 
#                     <div class="mb-3 mt-4">
#                         <label for="lname" class="form-label">Last Name</label>
#                         <input type="text" class="form-control" id="lname" name="lname" />
#                     </div>
#                     <div class="mb-3">
#                         <label for="directory" class="form-label">Directory</label>
#                         <input type="text" class="form-control" id="directory" name="directory" />
#                     </div> 
#                     <div class="mb-3 mt-4">
#                         <label for="photo" class="form-label">Path to Photo</label>
#                         <input type="text" class="form-control" id="photo" name="photo" />
#                     </div>
#                     <div class="mb-3">
#                         <label for="qualifications" class="form-label">Qualifications</label>
#                         <input type="text" class="form-control" id="qualifications" name="qualifications" />
#                     </div> 
#                     <div class="mb-3 mt-4">
#                         <label for="areas_of_interest" class="form-label">areas_of_interest</label>
#                         <input type="text" class="form-control" id="areas_of_interest" name="areas_of_interest" />
#                     </div>
#                     <div class="mb-3">
#                         <label for="bio" class="form-label">Bio</label>
#                         <input type="text" class="form-control" id="bio" name="bio" />
#                     </div> 
#                     <div class="mb-3">
#                         <label for="publications" class="form-label">Publications</label>
#                         <input type="text" class="form-control" id="publications" name="publications" />
#                     </div> 
#                     <div class="field is-grouped">
#                         <div class="control">
#                             <button class="button is-primary is-small">Save</button>
#                         </div>
#                     </div>
#                 </form>
#             {% endblock %}
#             """
# dict to html table
details_dict_view = """"  
    {% extends "base.html" %} {% block content %}
    <table>
        <thead>
            <tr>
            <th>{{tablehead}}</th>
            <th>{{tableheadrvalue}} (<a href="{{url_for(fn_target)}}">Edit</a>)</th>
            </tr>
        </thead>
        <tbody>
            {% for key, value in userdict.items() %}
                <tr>
                    <td> {{ key }} </td>
                    <td> {{ value }} </td>
                </tr>
            {% endfor %}
        </tbody>
</table>
{% endblock %}
    """

################################################################################################################
all_edit_create_view = """
                {% extends "base.html" %} {% block content %}

                <form action="{{ url_for(fn_target,uname=uname,role=role) }}" method="POST">
                    {{ form.hidden_tag() }} {{ form.csrf_token }}
                    {% for field in form %}
                        <div class="form-group row mb-3">
                            {% if field.type != 'SubmitField' %}
                                {% if field.id != 'csrf_token' %}
                                    <label for="{{ field.id }}" class="control-label col-sm-2 col-form-label ms-5">{{ field.label.text|safe }}</label>
                                    <div class="col-sm-10 mx-5">
                                        {{ field(class_='form-control') }}
                                    </div>
                                {% endif %}
                            {% else %}
                                <input type="submit" class="btn btn-primary mx-4 form-control" value="{{ field.label.text|safe }}">
                                {% if tabindex %}
                                    tabindex="{{ tabindex }}" 
                                {% endif %}
                            {% endif %}
                        </div>
                    {% endfor %}
                </form>
                {% endblock %}
            """
allusers_view = """
                {% extends "base.html" %} {% block content %}
                
                <div class="container">
                    <div class="row mt-5">
                        <h3><a href="{{url_for('users.createuser')}}">Create User</a></h3>
                        {% for au in allusers %}
                                <div class="col-md-4">
                                    <div class="card bg-dark text-center text-white">
                                        <div class="card-header fw-bold fs-2">
                                            <h3>{{au['User Name']}}</h3>
                                            <h5><a href="{{url_for('users.userdelete', uname = au['User Name'])}}" >Delete</a></h5> 
                                        </div>
                                        <div class="card-body">
                                            User Roles :
                                            {% for rol in au['Roles'] %}
                                                <a href="{{url_for('users.alluserrolesedit', uname = au['User Name'], role = rol)}}" >{{rol}}</a>
                                            {% endfor %}
                                        </div>
                                    </div>
                                </div>
                        {% endfor %}
                    
                    </div>
			    </div>
                
                <table>
                    <thead>
                        <tr>
                        <th>tablehead</th>
                        <th>tableheadrvalue </th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for key, value in currusrhome.items() %}
                            <tr>
                                <td> {{ key }} </td>
                                <td> {{ value }} </td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
                {% endblock %}
            """

@users.route('/createuser', methods=['GET', 'POST'])
@login_required
def createuser():
    #print('print Users creteuser')
    if request.method == 'GET':
        usernewform = UserNewForm()
        return render_template_string(edit_create_view, form=usernewform, fn_target='users.createuser', key_str=None)
    if request.method == 'POST':
        usernewform = UserNewForm(request.form)
        if usernewform.validate_on_submit():
            username = usernewform.username.data #request.form.get("username")
            password = usernewform.password.data #request.form.get("password")
            passwd = usernewform.passwd.data #request.form.get("passwd")
            
            if passwd == password:
                userexistflag = False
                u = None
                u = User.objects(username=username).first()
                if u != None: #if username == u.username:
                    userexistflag = True
                    print("User Already Exist")
                    return render_template_string("""
                        {% extends "base.html" %} {% block content %}
                            <a href="{{url_for('users.userrolescreate')}}">Add New Role to User</a>
                            <h3>User already Exits {username} </h3>
                        {% endblock %}
                    """
                    )
                if userexistflag == False:
                    user = User(username=usernewform.username.data, password=usernewform.password.data)
                    user.save()
                    return render_template_string("""
                        {% extends "base.html" %} {% block content %}
                            <a href="{{url_for('users.userrolescreate')}}">Add New Role to User</a>
                            <h3>User {username} is registerd. Fill other detiails </h3>
                        {% endblock %}
                    """
                    ,username=username)
            else:
                print("vsxjvajsvj")
                print(passwd)
                print(password)
        return redirect('/')

@users.route('/userdelete/<uname>', methods=['GET'])  # username
@login_required
def userdelete(uname):
    user = User.objects(username=uname).first()
    if request.method == 'GET':
        if hasattr(user, 'objects') == True:
            #for u in user:
            if user.username == uname:
                user.delete()
                #user.save()
        return redirect('/allusers')

@users.route('/allusers', methods=['GET'])
@login_required
def allusers():
    if request.method == 'GET':
        user = User.objects(username=current_user.username).first()
        ulist = []
        for u in User.objects:
            ulist.append(u.cred_dict())
        print(user.home_dict())
        return render_template_string(allusers_view, allusers=ulist,currusrhome=user.home_dict())
    else:
        return redirect('/')

@users.route('/alluserrolesedit/<uname>/<role>', methods=['GET', 'POST'])
@login_required # Admin Only
def alluserrolesedit(uname,role):
    if request.method == 'GET':
        userroleform = UserRoleForm()
        userroleform.role.data = role
        ######## userroles ##############
        # #########  <a href="{{url_for('users.indcolabedit', key_str = item.name)}}" >Edit</a> ; def __str__(self): return self.name  ;  It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
        return render_template_string(all_edit_create_view, form=userroleform, fn_target='users.alluserrolesedit',uname=uname,role=role)
    if request.method == 'POST':
        userroleform = UserRoleForm(request.form)
        user = User.objects(username=uname).first()
        if userroleform.validate_on_submit():
            if hasattr(user, 'objects') == True:
                for r in user.roles:
                    if r == role:
                        i = user.roles.index(r)
                        user.roles[i] = userroleform.role.data
                        user.save()
        return redirect('/allusers')
        #return render_template_string(userroles_view, userroles=user.roles)

##############################################  User and its Roles  ##################################################
userroles_view = """
                {% extends "base.html" %} {% block content %}
                <a href="{{url_for('users.userrolescreate')}}">Add New Role to User</a>
                
                <div class="container">
                    <div class="row mt-5">

                        {% for item in userroles %}
                            <div class="col-md-4">
                                <div class="card bg-dark text-center text-white">
                                    <div class="card-header fw-bold fs-2">
                                        <h3>{{item}}</h3> 
                                    </div>
                                    <div class="card-body">
                                        <a href="{{url_for('users.userrolesedit', key_str = item)}}" >Edit</a>
                                        <a href="{{url_for('users.userrolesdelete', key_str = item)}}" >Delete</a>
                                    </div>
                                </div>
                            </div>
                        {% endfor %}
                    
                    </div>
			    </div>
                
                {% endblock %}
            """

@users.route('/userroles', methods=['GET'])
@login_required
def userroles():
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        if hasattr(user, 'objects') == True:
            ######## userroles ##############
            # #########  <a href="{{url_for('users.indcolabedit', key_str = item.name)}}" >Edit</a> ; def __str__(self): return self.name  ;  It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
            return render_template_string(userroles_view, userroles=user.roles)
        else:
            return redirect('/')

@users.route('/userrolescreate', methods=['GET', 'POST'])
@login_required
def userrolescreate():
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        if hasattr(user, 'objects') == True:
            userroleform = UserRoleForm()
            ######## userroles ##############
            # #########  <a href="{{url_for('users.indcolabedit', key_str = item.name)}}" >Edit</a> ; def __str__(self): return self.name  ;  It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
            return render_template_string(edit_create_view, form=userroleform, fn_target='users.userrolescreate', key_str=None)
    if request.method == 'POST':
        userroleform = UserRoleForm(request.form)
        if userroleform.validate_on_submit():
            ######## userroles #############
            if hasattr(user, 'objects') == True:
                user.roles.append(userroleform.role.data)
                user.save()
        return render_template_string(userroles_view, userroles=user.roles)

@users.route('/userrolesedit/<key_str>', methods=['GET', 'POST'])  # username
@login_required
def userrolesedit(key_str):
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        userroleform = UserRoleForm()
        if hasattr(user, 'objects') == True:
            for r in user.roles:
                if r == key_str:
                    userroleform.role.data = key_str
        return render_template_string(edit_create_view, form=userroleform, fn_target='users.userrolesedit', key_str=key_str)
    if request.method == 'POST':
        userroleform = UserRoleForm(request.form)
        if userroleform.validate_on_submit():
            if hasattr(user, 'objects') == True:
                for r in user.roles:
                    if r == key_str:
                        i = user.roles.index(r)
                        user.roles[i] = userroleform.role.data
                        user.save()
        return render_template_string(userroles_view, userroles=user.roles)

@users.route('/userrolesdelete/<key_str>', methods=['GET'])  # username
@login_required
def userrolesdelete(key_str):
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        if hasattr(user, 'objects') == True:
            for r in user.roles:
                if r == key_str:
                    user.roles.remove(r)
                    user.save()
        return render_template_string(userroles_view, userroles=user.roles)




###########################################################  userdetails  ##########################################################################
@users.route('/userdetails', methods=['GET'])  # username
@login_required
def userdetails():
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        if hasattr(user, 'objects') == True:
            return render_template_string(details_dict_view,userdict=user.personal_dict(),tablehead='Personal Details',tableheadrvalue='Information',fn_target='users.userdetailsedit')



@users.route('/userdetailsedit', methods=['GET', 'POST'])  # username
@login_required
def userdetailsedit():
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        if hasattr(user, 'objects') == True:
            userinformation = UserInformation()
            userinformation.fname.data=user.fname
            userinformation.mname.data=user.mname
            userinformation.lname.data=user.lname
            userinformation.directory.data=user.directory
            userinformation.photo.data=user.photo
            userinformation.qualifications.data=user.qualifications
            userinformation.areas_of_interest.data=user.areas_of_interest
            userinformation.bio.data=user.bio
            userinformation.publications.data=user.publications 
            # return render_template('/user/userdetails.html',usr = jsonify(user).get_json())
            # return render_template('/user/userdetails.html', fname=user.fname,mname=user.mname,lname=user.lname,directory=user.directory,photo=user.photo
            # ,qualifications=user.qualifications,areas_of_interest=user.areas_of_interest,bio=user.bio,publications=user.publications)
            return render_template_string(edit_create_view,form=userinformation,fn_target='users.userdetailsedit')

    if request.method == 'POST':
        if hasattr(user, 'objects') == True:
            userinformation = UserInformation(request.form)
            user.fname = userinformation.fname.data
            user.mname = userinformation.mname.data
            user.lname = userinformation.lname.data
            user.directory = userinformation.directory.data
            user.photo = userinformation.photo.data
            user.qualifications = userinformation.qualifications.data
            user.areas_of_interest = userinformation.areas_of_interest.data
            user.bio = userinformation.bio.data
            user.publications = userinformation.publications.data
            user.save()
            print('Contact Saved')
            # print(jsonify(user).get_json())
        return render_template_string(edit_create_view,form=userinformation,fn_target='users.userdetailsedit')
    # for user in User.objects:
    #     print(user.username)
    # user = User.objects(username=usrnm)
    # print(jsonify(user).get_json())
    # return render_template('/user/userdetails.html',usr = jsonify(user).get_json())
#############################################################   usercontacts   ######################################################################################

@users.route('/usercontacts', methods=['GET'])  # username
@login_required
def usercontacts():
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        if hasattr(user, 'objects') == True:
            return render_template_string(details_dict_view,userdict=user.contact.contact_dict(),tablehead='Contact Details',tableheadrvalue='Information',fn_target='users.usercontactsedit')


@users.route('/usercontactsedit', methods=['GET', 'POST'])  # username
@login_required
def usercontactsedit():
    # print(current_user.get_id()) # not id of User in databse
    # print(current_user.username)
    user = User.objects(username=current_user.username).first()
    # print(jsonify(user).get_json())
    if request.method == 'GET':
        #usercontactsform = UserContactsForm(oldfield_id='',oldfield_lable='',oldfield_data='')
        usercontactsform = UserContactsForm()
        if hasattr(user, 'objects') == True:
            usercontactsform.web.data = user.contact.web
            usercontactsform.googlescholar.data = user.contact.googlescholar
            usercontactsform.linkedin.data = user.contact.linkedin
            usercontactsform.facebook.data = user.contact.facebook
            usercontactsform.youtube.data = user.contact.youtube
            usercontactsform.twitter.data = user.contact.twitter
            ######## Home address #############
            usercontactsform.home_add.data = user.contact.address.home.add
            usercontactsform.home_state.data = user.contact.address.home.state
            usercontactsform.home_pin.data = user.contact.address.home.pin
            usercontactsform.home_countary.data = user.contact.address.home.countary
            usercontactsform.home_phone.data = user.contact.address.home.phone
            usercontactsform.home_email.data = user.contact.address.home.email
            ######## office address #############
            usercontactsform.office_add.data = user.contact.address.office.add
            usercontactsform.office_state.data = user.contact.address.office.state
            usercontactsform.office_pin.data = user.contact.address.office.pin
            usercontactsform.office_countary.data = user.contact.address.office.countary
            usercontactsform.office_phone.data = user.contact.address.office.phone
            usercontactsform.office_email.data = user.contact.address.office.email
        #return render_template('/user/contacts.html', form=usercontactsform)
        return render_template_string(edit_create_view,form=usercontactsform,fn_target='users.usercontactsedit')
    if request.method == 'POST':
        usercontactsform = UserContactsForm(request.form)
        if usercontactsform.validate_on_submit():
            ######## Contacts #############
            if hasattr(user, 'objects') == True:
                ################  contact  ####################################################################
                user.contact.web = usercontactsform.web.data
                user.contact.googlescholar = usercontactsform.googlescholar.data
                user.contact.linkedin = usercontactsform.linkedin.data
                user.contact.facebook = usercontactsform.facebook.data
                user.contact.youtube = usercontactsform.youtube.data
                user.contact.twitter = usercontactsform.twitter.data
                ######## Home address #############
                user.contact.address.home.add = usercontactsform.home_add.data
                user.contact.address.home.state = usercontactsform.home_state.data
                user.contact.address.home.pin = usercontactsform.home_pin.data
                user.contact.address.home.countary = usercontactsform.home_countary.data
                user.contact.address.home.phone = usercontactsform.home_phone.data
                user.contact.address.home.email = usercontactsform.home_email.data
                ######## office address #############
                user.contact.address.office.add = usercontactsform.office_add.data
                user.contact.address.office.state = usercontactsform.office_state.data
                user.contact.address.office.pin = usercontactsform.office_pin.data
                user.contact.address.office.countary = usercontactsform.office_countary.data
                user.contact.address.office.phone = usercontactsform.office_phone.data
                user.contact.address.office.email = usercontactsform.office_email.data
                user.save()
                print('Contact Saved')
            # print(jsonify(user).get_json())
    #return render_template('/user/contacts.html', form=usercontactsform)
    return render_template_string(edit_create_view,form=usercontactsform,fn_target='users.usercontactsedit')


#####################################################################  faculty  #############################################################################
@users.route('/faculty', methods=['GET', 'POST'])  # username
@login_required
def faculty():
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        if hasattr(user, 'objects') == True:
            return render_template_string(details_dict_view,userdict=user.faculty.faculty_dict(),tablehead='Faculty Details',tableheadrvalue='Information',fn_target='users.facultyedit')


@users.route('/facultyedit', methods=['GET', 'POST'])  # username
@login_required
def facultyedit():
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        userfacultyform = UserFacultyForm()
        if hasattr(user, 'objects') == True:
            ######## Faculty ##############
            userfacultyform.position.data = user.faculty.position
            userfacultyform.title.data = user.faculty.title
            userfacultyform.post.data = user.faculty.post
            userfacultyform.empcode.data = user.faculty.empcode
        #return render_template('/user/faculty.html', form=userfacultyform)
        return render_template_string(edit_create_view,form=userfacultyform,fn_target='users.facultyedit')
    if request.method == 'POST':
        userfacultyform = UserFacultyForm(request.form)
        if userfacultyform.validate_on_submit():
            ######## Faculty #############
            if hasattr(user, 'objects') == True:
                user.faculty.position = userfacultyform.position.data
                user.faculty.title = userfacultyform.title.data
                user.faculty.post = userfacultyform.post.data
                user.faculty.empcode = userfacultyform.empcode.data
                user.save()
                print('Contact Saved')
            # print(jsonify(user).get_json())
        #return render_template('/user/faculty.html', form=userfacultyform)
        return render_template_string(edit_create_view,form=userfacultyform,fn_target='users.facultyedit')

#####################################################################  student  #############################################################################
@users.route('/student', methods=['GET', 'POST'])  # username
@login_required
def student():
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        if hasattr(user, 'objects') == True:
            return render_template_string(details_dict_view,userdict=user.student.student_dict(),tablehead='Stuent Details',tableheadrvalue='Information',fn_target='users.studentedit')


@users.route('/studentedit', methods=['GET', 'POST'])  # username
@login_required
def studentedit():
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        userstudentform = UserStudentForm()
        if hasattr(user, 'objects') == True:
            ######## student ##############
            userstudentform.programe.data = user.student.programe
            userstudentform.year.data = user.student.year
            userstudentform.branch.data = user.student.branch
            userstudentform.number.data = user.student.number
            userstudentform.roll.data = user.student.roll
        #return render_template('/user/student.html', form=userstudentform)
        return render_template_string(edit_create_view,form=userstudentform,fn_target='users.studentedit')
    if request.method == 'POST':
        userstudentform = UserStudentForm(request.form)
        if userstudentform.validate_on_submit():
            ######## Student #############
            if hasattr(user, 'objects') == True:
                user.student.programe = userstudentform.programe.data
                user.student.year = userstudentform.year.data
                user.student.branch = userstudentform.branch.data
                user.student.number = userstudentform.number.data
                user.student.roll = userstudentform.roll.data
                user.save()
                print('Contact Saved')
            # print(jsonify(user).get_json())
        #return render_template('/user/student.html', form=userstudentform)
        return render_template_string(edit_create_view,form=userstudentform,fn_target='users.studentedit')

#####################################################################  university  #############################################################################
@users.route('/university', methods=['GET', 'POST'])  # username
@login_required
def university():
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        if hasattr(user, 'objects') == True:
            return render_template_string(details_dict_view,userdict=user.university.university_dict(),tablehead='University Details',tableheadrvalue='Information',fn_target='users.universityedit')


@users.route('/universityedit', methods=['GET', 'POST'])  # username
@login_required
def universityedit():
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        useruniversityform = UserUniversityForm()
        if hasattr(user, 'objects') == True:
            ######## university ##############
            useruniversityform.name.data = user.university.name
            useruniversityform.url.data = user.university.url
            ######## office address #############
            useruniversityform.office_add.data = user.university.office.add
            useruniversityform.office_state.data = user.university.office.state
            useruniversityform.office_pin.data = user.university.office.pin
            useruniversityform.office_countary.data = user.university.office.countary
            useruniversityform.office_phone.data = user.university.office.phone
            useruniversityform.office_email.data = user.university.office.email
        #return render_template('/user/university.html', form=useruniversityform)
        return render_template_string(edit_create_view,form=useruniversityform,fn_target='users.universityedit')
    if request.method == 'POST':
        useruniversityform = UserUniversityForm(request.form)
        if useruniversityform.validate_on_submit():
            ######## university #############
            if hasattr(user, 'objects') == True:
                user.university.name = useruniversityform.name.data
                user.university.url = useruniversityform.url.data
                user.university.office.add = useruniversityform.office_add.data
                user.university.office.state = useruniversityform.office_state.data
                user.university.office.pin = useruniversityform.office_pin.data
                user.university.office.countary = useruniversityform.office_countary.data
                user.university.office.phone = useruniversityform.office_phone.data
                user.university.office.email = useruniversityform.office_email.data
                user.save()
                print('Contact Saved')
            # print(jsonify(user).get_json())
        #return render_template('/user/university.html', form=useruniversityform)
        return render_template_string(edit_create_view,form=useruniversityform,fn_target='users.universityedit')

#####################################################################  department  #############################################################################
@users.route('/department', methods=['GET', 'POST'])  # username
@login_required
def department():
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        if hasattr(user, 'objects') == True:
            return render_template_string(details_dict_view,userdict=user.department.department_dict(),tablehead='Department Details',tableheadrvalue='Information',fn_target='users.departmentedit')

@users.route('/departmentedit', methods=['GET', 'POST'])  # username
@login_required
def departmentedit():
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        userdepartmentform = UserDepartmentForm()
        if hasattr(user, 'objects') == True:
            ######## department ##############
            userdepartmentform.name.data = user.department.name
            userdepartmentform.url.data = user.department.url
            ######## office address #############
            userdepartmentform.office_add.data = user.department.office.add
            userdepartmentform.office_state.data = user.department.office.state
            userdepartmentform.office_pin.data = user.department.office.pin
            userdepartmentform.office_countary.data = user.department.office.countary
            userdepartmentform.office_phone.data = user.department.office.phone
            userdepartmentform.office_email.data = user.department.office.email
        #return render_template('/user/department.html', form=userdepartmentform)
        return render_template_string(edit_create_view,form=userdepartmentform,fn_target='users.departmentedit')
    if request.method == 'POST':
        userdepartmentform = UserDepartmentForm(request.form)
        if userdepartmentform.validate_on_submit():
            ######## department #############
            if hasattr(user, 'objects') == True:
                ######## department ##############
                user.department.name = userdepartmentform.name.data
                user.department.url = userdepartmentform.url.data
                ######## office address #############
                user.department.office.add = userdepartmentform.office_add.data
                user.department.office.state = userdepartmentform.office_state.data
                user.department.office.pin = userdepartmentform.office_pin.data
                user.department.office.countary = userdepartmentform.office_countary.data
                user.department.office.phone = userdepartmentform.office_phone.data
                user.department.office.email = userdepartmentform.office_email.data
                user.save()
                print('Contact Saved')
            # print(jsonify(user).get_json())
        #return render_template('/user/department.html', form=userdepartmentform)
        return render_template_string(edit_create_view,form=userdepartmentform,fn_target='users.departmentedit')


####################################################################################################################
# def __str__(self): return self.name  It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.



###################################################################################################################
##############################################  sponsoredprojects  ##################################################
sponsoredprojects_view = """
                {% extends "base.html" %} {% block content %}
                <a href="{{url_for('users.sponsoredprojectscreate')}}">Add SponsoredProjects</a>
                
                <div class="container">
                    <div class="row mt-5">

                        {% for item in sponsoredprojects %}
                            <div class="col-md-4">
                                <div class="card bg-dark text-center text-white">
                                    <div class="card-header fw-bold fs-2">
                                        <a href="{{item.url}}">{{item.title}}</a> 
                                    </div>
                                    <div class="card-body">
                                        <h5 class="card-title fs-3">{{item.title}} <span class="text-success">/ 2022</span></h5>
                                        <ul class="list-unstyled">
                                            <li>{{item.countary}}</li>
                                            <li>{{item.year}}</li>
                                            <li>{{item.url}}</li>
                                        </ul>
                                        <a href="{{url_for('users.sponsoredprojectsedit', key_str = item.title)}}" >Edit</a>
                                        <a href="{{url_for('users.sponsoredprojectsdelete', key_str = item.title)}}" >Delete</a>
                                    </div>
                                </div>
                            </div>
                        {% endfor %}
                    
                    </div>
			    </div>
                
                {% endblock %}
            """


@users.route('/sponsoredprojects', methods=['GET'])
@login_required
def sponsoredprojects():
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        if hasattr(user, 'objects') == True:
            ######## IndustryCollaboration ##############
            # #########  <a href="{{url_for('users.indcolabedit', key_str = item.name)}}" >Edit</a> ; def __str__(self): return self.name  ;  It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
            return render_template_string(sponsoredprojects_view, sponsoredprojects=user.sponsoredprojects)
        else:
            return redirect('/')


# username
@users.route('/sponsoredprojectsedit/<key_str>', methods=['GET', 'POST'])
@login_required
def sponsoredprojectsedit(key_str):
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        usersponsoredprojectsform = UserSponsoredProjectsForm()
        if hasattr(user, 'objects') == True:
            ######## sponsoredprojects ##############
            for p in user.sponsoredprojects:
                # <a href="{{url_for('users.indcolabedit', key_str = item.name)}}" >Edit</a> ; def __str__(self): return self.name  ;  It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
                if str(p) == key_str:
                    usersponsoredprojectsform.title.data = p.title
                    usersponsoredprojectsform.name.data = p.name
                    usersponsoredprojectsform.duration.data = p.duration
                    usersponsoredprojectsform.amount.data = p.amount
        return render_template_string(edit_create_view, form=usersponsoredprojectsform, fn_target='users.sponsoredprojectsedit', key_str=key_str)
        # return render_template('/user/sponsoredprojects.html', form=usersponsoredprojectsform)
    if request.method == 'POST':
        usersponsoredprojectsform = UserSponsoredProjectsForm(request.form)
        if usersponsoredprojectsform.validate_on_submit():
            ######## sponsoredprojects #############
            if hasattr(user, 'objects') == True:
                for p in user.sponsoredprojects:
                    # <a href="{{url_for('users.indcolabedit', key_str = item.name)}}" >Edit</a> ; def __str__(self): return self.name  ;  It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
                    if str(p) == key_str:
                        p.title = usersponsoredprojectsform.title.data
                        p.name = usersponsoredprojectsform.name.data
                        p.duration = usersponsoredprojectsform.duration.data
                        p.amount = usersponsoredprojectsform.amount.data
                        user.save()
                        print('Contact Saved')
            # print(jsonify(user).get_json())
        return render_template_string(sponsoredprojects_view, sponsoredprojects=user.sponsoredprojects)
        # return render_template('/user/sponsoredprojects.html', form=usersponsoredprojectsform)


@users.route('/sponsoredprojectscreate', methods=['GET', 'POST'])  # create
@login_required
def sponsoredprojectscreate():
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        usersponsoredprojectsform = UserSponsoredProjectsForm()
        if hasattr(user, 'objects') == True:
            return render_template_string(edit_create_view, form=usersponsoredprojectsform, fn_target='users.sponsoredprojectscreate', key_str=None)
    if request.method == 'POST':
        usersponsoredprojectsform = UserSponsoredProjectsForm(request.form)
        if usersponsoredprojectsform.validate_on_submit():
            ######## industrycollaboration #############
            if hasattr(user, 'objects') == True:
                p = SponsoredProjects(name=usersponsoredprojectsform.name.data, duration=usersponsoredprojectsform.duration.data, amount=usersponsoredprojectsform.amount.data, title=usersponsoredprojectsform.title.data
                                      )
                user.sponsoredprojects.append(p)
                user.save()
        return render_template_string(sponsoredprojects_view, sponsoredprojects=user.sponsoredprojects)


@users.route('/sponsoredprojectsdelete/<key_str>', methods=['GET'])  # delete
@login_required
def sponsoredprojectsdelete(key_str):
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        if hasattr(user, 'objects') == True:
            for p in user.sponsoredprojects:
                # <a href="{{url_for('users.indcolabedit', key_str = item.name)}}" >Edit</a> ; def __str__(self): return self.name  ;  It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
                if str(p) == key_str:
                    user.sponsoredprojects.remove(p)
                    user.save()
        return render_template_string(sponsoredprojects_view, sponsoredprojects=user.sponsoredprojects)


############################################## Patents  #############################################################
patents_view = """
                {% extends "base.html" %} {% block content %}
                <a href="{{url_for('users.patentscreate')}}">Add Patents</a>
                
                <div class="container">
                    <div class="row mt-5">

                        {% for item in patents %}
                            <div class="col-md-4">
                                <div class="card bg-dark text-center text-white">
                                    <div class="card-header fw-bold fs-2">
                                        <a href="{{item.url}}">{{item.title}}</a> 
                                    </div>
                                    <div class="card-body">
                                        <h5 class="card-title fs-3">{{item.title}} <span class="text-success">/ 2022</span></h5>
                                        <ul class="list-unstyled">
                                            <li>{{item.countary}}</li>
                                            <li>{{item.year}}</li>
                                            <li>{{item.url}}</li>
                                        </ul>
                                        <a href="{{url_for('users.patentsedit', key_str = item.title)}}" >Edit</a>
                                        <a href="{{url_for('users.patentsdelete', key_str = item.title)}}" >Delete</a>
                                    </div>
                                </div>
                            </div>
                        {% endfor %}
                    
                    </div>
			    </div>
                
                {% endblock %}
            """


@users.route('/patents', methods=['GET'])
@login_required
def patents():
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        if hasattr(user, 'objects') == True:
            ######## IndustryCollaboration ##############
            # #########  <a href="{{url_for('users.indcolabedit', key_str = item.name)}}" >Edit</a> ; def __str__(self): return self.name  ;  It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
            return render_template_string(patents_view, patents=user.patents)
        else:
            return redirect('/')


@users.route('/patents/<key_str>', methods=['GET', 'POST'])  # username
@login_required
def patentsedit(key_str):
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        userpatentsform = UserPatentsForm()
        if hasattr(user, 'objects') == True:
            ######## patents ##############
            for p in user.patents:
                # <a href="{{url_for('users.indcolabedit', key_str = item.name)}}" >Edit</a> ; def __str__(self): return self.name  ;  It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
                if str(p) == key_str:
                    userpatentsform.countary.data = p.countary
                    userpatentsform.title.data = p.title
                    userpatentsform.year.data = p.year
                    userpatentsform.url.data = p.url
        return render_template_string(edit_create_view, form=userpatentsform, fn_target='users.patentsedit', key_str=key_str)
        # return render_template('/user/patents.html', form=userpatentsform)
    if request.method == 'POST':
        userpatentsform = UserPatentsForm(request.form)
        if userpatentsform.validate_on_submit():
            ######## patents #############
            if hasattr(user, 'objects') == True:
                for p in user.patents:
                    # <a href="{{url_for('users.indcolabedit', key_str = item.name)}}" >Edit</a> ; def __str__(self): return self.name  ;  It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
                    if str(p) == key_str:
                        p.countary = userpatentsform.countary.data
                        p.title = userpatentsform.title.data
                        p.year = userpatentsform.year.data
                        p.url = userpatentsform.url.data
                        user.save()
                        print('Contact Saved')
            # print(jsonify(user).get_json())
        # return render_template('/user/patents.html', form=userpatentsform)
        return render_template_string(patents_view, patents=user.patents)


@users.route('/patentscreate', methods=['GET', 'POST'])  # create
@login_required
def patentscreate():
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        userpatentsform = UserPatentsForm()
        if hasattr(user, 'objects') == True:
            return render_template_string(edit_create_view, form=userpatentsform, fn_target='users.patentscreate', key_str=None)
    if request.method == 'POST':
        userpatentsform = UserPatentsForm(request.form)
        if userpatentsform.validate_on_submit():
            ######## industrycollaboration #############
            if hasattr(user, 'objects') == True:
                p = Patents(countary=userpatentsform.countary.data, url=userpatentsform.url.data, year=userpatentsform.year.data, title=userpatentsform.title.data
                            )
                user.patents.append(p)
                user.save()
        return render_template_string(patents_view, patents=user.patents)


@users.route('/patentsdelete/<key_str>', methods=['GET'])  # delete
@login_required
def patentsdelete(key_str):
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        if hasattr(user, 'objects') == True:
            for p in user.patents:
                # <a href="{{url_for('users.indcolabedit', key_str = item.name)}}" >Edit</a> ; def __str__(self): return self.name  ;  It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
                if str(p) == key_str:
                    user.patents.remove(p)
                    user.save()
        return render_template_string(patents_view, patents=user.patents)


############################################## industrycollaboration #############################################
indcolab_view = """
                {% extends "base.html" %} {% block content %}
                <a href="{{url_for('users.indcolabcreate')}}">Create IndustryCollaboration</a>
                
                <div class="container">
                    <div class="row mt-5">

                        {% for item in industrycollaborations %}
                            <div class="col-md-4">
                                <div class="card bg-dark text-center text-white">
                                    <div class="card-header fw-bold fs-2">
                                        <a href="{{item.url}}">{{item.name}}</a> 
                                    </div>
                                    <div class="card-body">
                                        <h5 class="card-title fs-3">{{item.title}} <span class="text-success">/ 2022</span></h5>
                                        <ul class="list-unstyled">
                                            <li>{{item.title}}</li>
                                            <li>{{item.collaboration}}</li>
                                            <li>{{item.mou}}</li>
                                        </ul>
                                        <a href="{{url_for('users.indcolabedit', key_str = item.name)}}" >Edit</a>
                                        <a href="{{url_for('users.indcolabdelete', key_str = item.name)}}" >Delete</a>
                                    </div>
                                </div>
                            </div>
                        {% endfor %}
                    
                    </div>
			    </div>
                
                {% endblock %}
            """


@users.route('/indcolab', methods=['GET'])
@login_required
def indcolab():
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        if hasattr(user, 'objects') == True:
            ######## IndustryCollaboration ##############
            # #########  <a href="{{url_for('users.indcolabedit', key_str = item.name)}}" >Edit</a> ; def __str__(self): return self.name  ;  It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
            return render_template_string(indcolab_view, industrycollaborations=user.industrycollaboration)
        else:
            return redirect('/')


@users.route('/indcolabedit/<key_str>', methods=['GET', 'POST'])  # edit
@login_required
def indcolabedit(key_str):
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        userindustrycollaborationform = UserIndustryCollaborationForm()
        if hasattr(user, 'objects') == True:
            ######## industrycollaboration ##############
            for ic in user.industrycollaboration:
                # <a href="{{url_for('users.indcolabedit', key_str = item.name)}}" >Edit</a> ; def __str__(self): return self.name  ;  It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
                if str(ic) == key_str:
                    userindustrycollaborationform.name.data = ic.name
                    userindustrycollaborationform.url.data = ic.url
                    userindustrycollaborationform.mou.data = ic.mou
                    userindustrycollaborationform.collaboration.data = ic.collaboration
                    userindustrycollaborationform.title.data = ic.title
        return render_template_string(edit_create_view, form=userindustrycollaborationform, fn_target='users.indcolabedit', key_str=key_str)
        # return render_template('/user/industrycollaboration.html', form=userindustrycollaborationform,fn_target='users.indcolabedit',key_str=title)
    if request.method == 'POST':
        userindustrycollaborationform = UserIndustryCollaborationForm(
            request.form)
        if userindustrycollaborationform.validate_on_submit():
            ######## industrycollaboration #############
            if hasattr(user, 'objects') == True:
                for ic in user.industrycollaboration:
                    # <a href="{{url_for('users.indcolabedit', key_str = item.name)}}" >Edit</a> ; def __str__(self): return self.name  ;  It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
                    if str(ic) == key_str:
                        ic.name = userindustrycollaborationform.name.data
                        ic.url = userindustrycollaborationform.url.data
                        ic.mou = userindustrycollaborationform.mou.data
                        ic.collaboration = userindustrycollaborationform.collaboration.data
                        ic.title = userindustrycollaborationform.title.data
                        user.save()
                        print('Contact Saved')
            # print(jsonify(user).get_json())
        return render_template_string(indcolab_view, industrycollaborations=user.industrycollaboration)
        # return render_template('/user/industrycollaboration.html', form=userindustrycollaborationform)


@users.route('/indcolabcreate', methods=['GET', 'POST'])  # create
@login_required
def indcolabcreate():
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        userindustrycollaborationform = UserIndustryCollaborationForm()
        if hasattr(user, 'objects') == True:
            return render_template_string(edit_create_view, form=userindustrycollaborationform, fn_target='users.indcolabcreate', key_str=None)
    if request.method == 'POST':
        userindustrycollaborationform = UserIndustryCollaborationForm(
            request.form)
        print('form collected')
        if userindustrycollaborationform.validate_on_submit():
            ######## industrycollaboration #############
            print('form validate_on_submit')
            if hasattr(user, 'objects') == True:
                ic = IndustryCollaboration(name=userindustrycollaborationform.name.data, url=userindustrycollaborationform.url.data, mou=userindustrycollaborationform.mou.data, collaboration=userindustrycollaborationform.collaboration.data, title=userindustrycollaborationform.title.data
                                           )
                user.industrycollaboration.append(ic)
                user.save()
        return render_template_string(indcolab_view, industrycollaborations=user.industrycollaboration)


@users.route('/indcolabdelete/<key_str>', methods=['GET'])  # delete
@login_required
def indcolabdelete(key_str):
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        if hasattr(user, 'objects') == True:
            for ic in user.industrycollaboration:
                # <a href="{{url_for('users.indcolabedit', key_str = item.name)}}" >Edit</a> ; def __str__(self): return self.name  ;  It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
                if str(ic) == key_str:
                    user.industrycollaboration.remove(ic)
                    user.save()
        return render_template_string(indcolab_view, industrycollaborations=user.industrycollaboration)

######################################### Startup   ####################################################


@users.route('/startup', methods=['GET'])
@login_required
def startup():
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        #userstartupform = UserStartUpForm()
        if hasattr(user, 'objects') == True:
            ######## startup ##############
            # return render_template('/user/startup.html', startups=user.startup)
            return render_template_string("""
                {% extends "base.html" %} {% block content %}
                <a href="{{url_for('users.startupcreate')}}">Create New StartUp</a>
                {% for startup in startups %}
                <ul>
                <li>
                    <a href="{{startup.url}}">{{startup.name}} ({{startup.funding}})</a> 
                    <a href="{{url_for('users.startupedit', startupname = startup.name)}}">edit</a>
                    <a href="{{url_for('users.startupdelete', startupname = startup.name)}}">Delete</a>
                </li>
                </ul>
                {% endfor %}
                {% endblock %}
            """, startups=user.startup)
        else:
            return redirect('/')


@users.route('/startupedit/<startupname>', methods=['GET', 'POST'])
@login_required
def startupedit(startupname):
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        userstartupform = UserStartUpForm()
        if hasattr(user, 'objects') == True:
            ######## startup ##############
            for stup in user.startup:
                if stup.name == startupname:
                    userstartupform.name.data = stup.name
                    userstartupform.url.data = stup.url
                    userstartupform.funding.data = stup.funding
        # return render_template('/user/startup.html', form=userstartupform)
        return render_template_string("""
                {% extends "base.html" %} {% block content %}
                <form action="{{ url_for('users.startupedit', startupname = startupname) }}" method="POST">
                {{ form.hidden_tag() }}
                {% for field in form %}
                <div class="form-group row mb-3">
                    {% if field.type != 'SubmitField' %}
                    <label for="{{ field.id }}" class="control-label col-sm-2 col-form-label ms-5">{{ field.label.text|safe }}</label>
                    <div class="col-sm-10 mx-5">
                    {{ field(class_='form-control') }}
                    </div>
                    {% else %}
                    <input type="submit" class="btn btn-primary mx-4 form-control" value="{{ field.label.text|safe }}" {% if tabindex
                    %}tabindex="{{ tabindex }}" {% endif %}>
                    {% endif %}
                </div>
                {% endfor %}
                </form>
                {% endblock %}
            """, form=userstartupform, startupname=startupname)
    if request.method == 'POST':
        userstartupform = UserStartUpForm(request.form)
        if userstartupform.validate_on_submit():
            #         ######## startup #############
            if hasattr(user, 'objects') == True:
                for stup in user.startup:
                    if stup.name == startupname:
                        stup.name = userstartupform.name.data
                        stup.url = userstartupform.url.data
                        stup.funding = userstartupform.funding.data
                        user.save()
        return render_template_string("""
                {% extends "base.html" %} {% block content %}
                <a href="{{url_for('users.startupcreate')}}">Create New StartUp</a>
                {% for startup in startups %}
                <ul>
                <li>
                    <a href="{{startup.url}}">{{startup.name}} ({{startup.funding}})</a> 
                    <a href="{{url_for('users.startupedit', startupname = startup.name)}}">edit</a>
                    <a href="{{url_for('users.startupdelete', startupname = startup.name)}}">Delete</a>
                </li>
                </ul>
                {% endfor %}
                {% endblock %}
            """, startups=user.startup)


@users.route('/startupcreate', methods=['GET', 'POST'])
@login_required
def startupcreate():
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        userstartupform = UserStartUpForm()
        if hasattr(user, 'objects') == True:
            ######## startup ##############
            return render_template_string("""
                {% extends "base.html" %} {% block content %}
                <form action="{{ url_for('users.startupcreate') }}" method="POST">
                {{ form.hidden_tag() }}
                {% for field in form %}
                <div class="form-group row mb-3">
                    {% if field.type != 'SubmitField' %}
                    <label for="{{ field.id }}" class="control-label col-sm-2 col-form-label ms-5">{{ field.label.text|safe }}</label>
                    <div class="col-sm-10 mx-5">
                    {{ field(class_='form-control') }}
                    </div>
                    {% else %}
                    <input type="submit" class="btn btn-primary mx-4 form-control" value="{{ field.label.text|safe }}" {% if tabindex
                    %}tabindex="{{ tabindex }}" {% endif %}>
                    {% endif %}
                </div>
                {% endfor %}
                </form>
                {% endblock %}
            """, form=userstartupform)
    if request.method == 'POST':
        userstartupform = UserStartUpForm(request.form)
        if userstartupform.validate_on_submit():
            #         ######## startup #############
            if hasattr(user, 'objects') == True:
                stup = StartUp(name=userstartupform.name.data,
                               url=userstartupform.url.data, funding=userstartupform.funding.data)
                user.startup.append(stup)
                user.save()
        return render_template_string("""
                {% extends "base.html" %} {% block content %}
                <a href="{{url_for('users.startupcreate')}}">Create New StartUp</a>
                {% for startup in startups %}
                <ul>
                <li>
                    <a href="{{startup.url}}">{{startup.name}} ({{startup.funding}})</a> 
                    <a href="{{url_for('users.startupedit', startupname = startup.name)}}">edit</a>
                    <a href="{{url_for('users.startupdelete', startupname = startup.name)}}">Delete</a>
                </li>
                </ul>
                {% endfor %}
                {% endblock %}
            """, startups=user.startup)


@users.route('/startupdelete/<startupname>', methods=['GET'])
@login_required
def startupdelete(startupname):
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        if hasattr(user, 'objects') == True:
            for stup in user.startup:
                if stup.name == startupname:
                    user.startup.remove(stup)
                    user.save()
        return render_template_string("""
                {% extends "base.html" %} {% block content %}
                <a href="{{url_for('users.startupcreate')}}">Create New StartUp</a>
                {% for startup in startups %}
                <ul>
                <li>
                    <a href="{{startup.url}}">{{startup.name}} ({{startup.funding}})</a> 
                    <a href="{{url_for('users.startupedit', startupname = startup.name)}}">edit</a>
                    <a href="{{url_for('users.startupdelete', startupname = startup.name)}}">Delete</a>
                </li>
                </ul>
                {% endfor %}
                {% endblock %}
            """, startups=user.startup)


######################################### Books   ####################################################
books_view = """
                {% extends "base.html" %} {% block content %}
                <a href="{{url_for('users.bookscreate')}}">Add Books</a>
                
                <div class="container">
                    <div class="row mt-5">

                        {% for item in books %}
                            <div class="col-md-4">
                                <div class="card bg-dark text-center text-white">
                                    <div class="card-header fw-bold fs-2">
                                        <a href="{{item.url}}">{{item.title}}</a> 
                                    </div>
                                    <div class="card-body">
                                        <h5 class="card-title fs-3">{{item.title}} <span class="text-success">/ 2022</span></h5>
                                        <ul class="list-unstyled">
                                            <li>{{item.title}}</li>
                                            <li>{{item.year}}</li>
                                            <li>{{item.description}}</li>
                                            <li>{{item.publisher}}</li>
                                        </ul>
                                        <a href="{{url_for('users.booksedit', key_str = item.title)}}" >Edit</a>
                                        <a href="{{url_for('users.booksdelete', key_str = item.title)}}" >Delete</a>
                                    </div>
                                </div>
                            </div>
                        {% endfor %}
                    
                    </div>
			    </div>
                
                {% endblock %}
            """


@users.route('/books', methods=['GET'])
@login_required
def books():
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        if hasattr(user, 'objects') == True:
            ######## IndustryCollaboration ##############
            # #########  <a href="{{url_for('users.indcolabedit', key_str = item.name)}}" >Edit</a> ; def __str__(self): return self.name  ;  It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
            return render_template_string(books_view, books=user.books)
        else:
            return redirect('/')


@users.route('/booksedit/<key_str>', methods=['GET', 'POST'])
@login_required
def booksedit(key_str):
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        userbooksform = UserBooksForm()
        if hasattr(user, 'objects') == True:
            ######## Books ##############
            for p in user.books:
                # <a href="{{url_for('users.indcolabedit', key_str = item.name)}}" >Edit</a> ; def __str__(self): return self.name  ;  It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
                if str(p) == key_str:
                    userbooksform.title.data = p.title
                    userbooksform.description.data = p.description
                    userbooksform.year.data = p.year
                    userbooksform.url.data = p.url
                    userbooksform.publisher.data = p.publisher
        return render_template_string(edit_create_view, form=userbooksform, fn_target='users.booksedit', key_str=key_str)
        # return render_template('/user/books.html', form=userbooksform)
    if request.method == 'POST':
        userbooksform = UserBooksForm(request.form)
        if userbooksform.validate_on_submit():
            ######## Faculty #############
            if hasattr(user, 'objects') == True:
                for p in user.books:
                    # <a href="{{url_for('users.indcolabedit', key_str = item.name)}}" >Edit</a> ; def __str__(self): return self.name  ;  It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
                    if str(p) == key_str:
                        p.title = userbooksform.title.data
                        p.description = userbooksform.description.data
                        p.year = userbooksform.year.data
                        p.url = userbooksform.url.data
                        p.publisher = userbooksform.publisher.data
                        user.save()
                        print('Contact Saved')
            # print(jsonify(user).get_json())
        return render_template_string(books_view, books=user.books)
        # return render_template('/user/books.html', form=userbooksform)


@users.route('/bookscreate', methods=['GET', 'POST'])  # create
@login_required
def bookscreate():
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        userbooksform = UserBooksForm()
        if hasattr(user, 'objects') == True:
            return render_template_string(edit_create_view, form=userbooksform, fn_target='users.bookscreate', key_str=None)
    if request.method == 'POST':
        userbooksform = UserBooksForm(request.form)
        if userbooksform.validate_on_submit():
            ######## industrycollaboration #############
            if hasattr(user, 'objects') == True:
                p = Books(title=userbooksform.title.data, description=userbooksform.description.data, year=userbooksform.year.data, url=userbooksform.url.data, publisher=userbooksform.publisher.data
                          )
                user.books.append(p)
                user.save()
        return render_template_string(books_view, books=user.books)


@users.route('/booksdelete/<key_str>', methods=['GET'])  # delete
@login_required
def booksdelete(key_str):
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        if hasattr(user, 'objects') == True:
            for p in user.books:
                # <a href="{{url_for('users.indcolabedit', key_str = item.name)}}" >Edit</a> ; def __str__(self): return self.name  ;  It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
                if str(p) == key_str:
                    user.books.remove(p)
                    user.save()
        return render_template_string(books_view, books=user.books)


######################################### awards  #####################################################
awards_view = """
                {% extends "base.html" %} {% block content %}
                <a href="{{url_for('users.awardscreate')}}">Add Awards</a>
                
                <div class="container">
                    <div class="row mt-5">

                        {% for item in awards %}
                            <div class="col-md-4">
                                <div class="card bg-dark text-center text-white">
                                    <div class="card-header fw-bold fs-2">
                                        <a href="{{item.url}}">{{item.name}}</a> 
                                    </div>
                                    <div class="card-body">
                                        <h5 class="card-title fs-3">{{item.name}} <span class="text-success">/ 2022</span></h5>
                                        <ul class="list-unstyled">
                                            <li>{{item.name}}</li>
                                            <li>{{item.certificate}}</li>
                                            <li>{{item.description}}</li>
                                        </ul>
                                        <a href="{{url_for('users.awardsedit', key_str = item.name)}}" >Edit</a>
                                        <a href="{{url_for('users.awardsdelete', key_str = item.name)}}" >Delete</a>
                                    </div>
                                </div>
                            </div>
                        {% endfor %}
                    
                    </div>
			    </div>
                
                {% endblock %}
            """


@users.route('/awards', methods=['GET'])
@login_required
def awards():
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        if hasattr(user, 'objects') == True:
            ######## IndustryCollaboration ##############
            # #########  <a href="{{url_for('users.indcolabedit', key_str = item.name)}}" >Edit</a> ; def __str__(self): return self.name  ;  It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
            return render_template_string(awards_view, awards=user.awards)
        else:
            return redirect('/')


@users.route('/awardsedit/<key_str>', methods=['GET', 'POST'])
@login_required
def awardsedit(key_str):
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        userawardsform = UserAwardsForm()
        if hasattr(user, 'objects') == True:
            ######## awards ##############
            for p in user.awards:
                # <a href="{{url_for('users.indcolabedit', key_str = item.name)}}" >Edit</a> ; def __str__(self): return self.name  ;  It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
                if str(p) == key_str:
                    userawardsform.name.data = p.name
                    userawardsform.description.data = p.description
                    userawardsform.certificate.data = p.description
        return render_template_string(edit_create_view, form=userawardsform, fn_target='users.awardsedit', key_str=key_str)
        # return render_template('/user/awards.html', form=userawardsform)
    if request.method == 'POST':
        userawardsform = UserAwardsForm(request.form)
        if userawardsform.validate_on_submit():
            ######## Faculty #############
            if hasattr(user, 'objects') == True:
                for p in user.awards:
                    # <a href="{{url_for('users.indcolabedit', key_str = item.name)}}" >Edit</a> ; def __str__(self): return self.name  ;  It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
                    if str(p) == key_str:
                        p.name = userawardsform.name.data
                        p.description = userawardsform.description.data
                        p.description = userawardsform.certificate.data
                        user.save()
                        print('Contact Saved')
            # print(jsonify(user).get_json())
        return render_template_string(awards_view, awards=user.awards)
        # return render_template('/user/awards.html', form=userawardsform)


@users.route('/awardscreate', methods=['GET', 'POST'])  # create
@login_required
def awardscreate():
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        userawardsform = UserAwardsForm()
        if hasattr(user, 'objects') == True:
            return render_template_string(edit_create_view, form=userawardsform, fn_target='users.awardscreate', key_str=None)
    if request.method == 'POST':
        userawardsform = UserAwardsForm(request.form)
        if userawardsform.validate_on_submit():
            ######## industrycollaboration #############
            if hasattr(user, 'objects') == True:
                p = Awards(name=userawardsform.name.data, description=userawardsform.description.data, certificate=userawardsform.certificate.data
                           )
                user.awards.append(p)
                user.save()
        return render_template_string(awards_view, awards=user.awards)


@users.route('/awardsdelete/<key_str>', methods=['GET'])  # delete
@login_required
def awardsdelete(key_str):
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        if hasattr(user, 'objects') == True:
            for p in user.awards:
                # <a href="{{url_for('users.indcolabedit', key_str = item.name)}}" >Edit</a> ; def __str__(self): return self.name  ;  It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
                if str(p) == key_str:
                    user.awards.remove(p)
                    user.save()
        return render_template_string(awards_view, awards=user.awards)


#######################################  socialimpact  ##############################################
socialimpact_view = """
                {% extends "base.html" %} {% block content %}
                <a href="{{url_for('users.socialimpactcreate')}}">Add SocialImpact</a>
                
                <div class="container">
                    <div class="row mt-5">

                        {% for item in socialimpact %}
                            <div class="col-md-4">
                                <div class="card bg-dark text-center text-white">
                                    <div class="card-header fw-bold fs-2">
                                        <a href="{{item.url}}">{{item.name}}</a> 
                                    </div>
                                    <div class="card-body">
                                        <h5 class="card-title fs-3">{{item.name}} <span class="text-success">/ 2022</span></h5>
                                        <ul class="list-unstyled">
                                            <li>{{item.name}}</li>
                                            <li>{{item.url}}</li>
                                        </ul>
                                        <a href="{{url_for('users.socialimpactedit', key_str = item.name)}}" >Edit</a>
                                        <a href="{{url_for('users.socialimpactdelete', key_str = item.name)}}" >Delete</a>
                                    </div>
                                </div>
                            </div>
                        {% endfor %}
                    
                    </div>
			    </div>
                
                {% endblock %}
            """


@users.route('/socialimpact', methods=['GET'])
@login_required
def socialimpact():
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        if hasattr(user, 'objects') == True:
            ######## IndustryCollaboration ##############
            # #########  <a href="{{url_for('users.indcolabedit', key_str = item.name)}}" >Edit</a> ; def __str__(self): return self.name  ;  It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
            return render_template_string(socialimpact_view, socialimpact=user.socialimpact)
        else:
            return redirect('/')


@users.route('/socialimpactedit/<key_str>', methods=['GET', 'POST'])
@login_required
def socialimpactedit(key_str):
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        usersocialimpactform = UserSocialImpactForm()
        if hasattr(user, 'objects') == True:
            ######## socialimpact ##############
            for p in user.socialimpact:
                # <a href="{{url_for('users.indcolabedit', key_str = item.name)}}" >Edit</a> ; def __str__(self): return self.name  ;  It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
                if str(p) == key_str:
                    usersocialimpactform.name.data = p.name
                    usersocialimpactform.url.data = p.url
        return render_template_string(edit_create_view, form=usersocialimpactform, fn_target='users.socialimpactedit', key_str=key_str)
    if request.method == 'POST':
        usersocialimpactform = UserSocialImpactForm(request.form)
        if usersocialimpactform.validate_on_submit():
            ######## Faculty #############
            if hasattr(user, 'objects') == True:
                for p in user.socialimpact:
                    # <a href="{{url_for('users.indcolabedit', key_str = item.name)}}" >Edit</a> ; def __str__(self): return self.name  ;  It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
                    if str(p) == key_str:
                        p.name = usersocialimpactform.name.data
                        p.url = usersocialimpactform.url.data
                        user.save()
                        print('Contact Saved')
            # print(jsonify(user).get_json())
        return render_template_string(socialimpact_view, socialimpact=user.socialimpact)


@users.route('/socialimpactcreate', methods=['GET', 'POST'])  # create
@login_required
def socialimpactcreate():
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        usersocialimpactform = UserSocialImpactForm()
        if hasattr(user, 'objects') == True:
            return render_template_string(edit_create_view, form=usersocialimpactform, fn_target='users.socialimpactcreate', key_str=None)
    if request.method == 'POST':
        usersocialimpactform = UserSocialImpactForm(request.form)
        if usersocialimpactform.validate_on_submit():
            ######## industrycollaboration #############
            if hasattr(user, 'objects') == True:
                p = SocialImpact(name=usersocialimpactform.name.data, url=usersocialimpactform.url.data
                                 )
                user.socialimpact.append(p)
                user.save()
        return render_template_string(socialimpact_view, socialimpact=user.socialimpact)


@users.route('/socialimpactdelete/<key_str>', methods=['GET'])  # delete
@login_required
def socialimpactdelete(key_str):
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        if hasattr(user, 'objects') == True:
            for p in user.socialimpact:
                # <a href="{{url_for('users.indcolabedit', key_str = item.name)}}" >Edit</a> ; def __str__(self): return self.name  ;  It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
                if str(p) == key_str:
                    user.socialimpact.remove(p)
                    user.save()
        return render_template_string(socialimpact_view, socialimpact=user.socialimpact)


#######################################  technologytransfer  ######################################
technologytransfer_view = """
                {% extends "base.html" %} {% block content %}
                <a href="{{url_for('users.technologytransfercreate')}}">Add TechnologyTransfer</a>
                
                <div class="container">
                    <div class="row mt-5">

                        {% for item in technologytransfer %}
                            {% if item.name != None %}
                                <div class="col-md-4">
                                    <div class="card bg-dark text-center text-white">
                                        <div class="card-header fw-bold fs-2">
                                            <a href="{{item.url}}">{{item.name}}</a> 
                                        </div>
                                        <div class="card-body">
                                            <h5 class="card-title fs-3">{{item.name}} <span class="text-success">/ 2022</span></h5>
                                            <ul class="list-unstyled">
                                                <li>{{item.name}}</li>
                                                <li>{{item.url}}</li>
                                                <li>{{item.technology}}</li>
                                                <li>{{item.royalty}}</li>
                                            </ul>
                                            <a href="{{url_for('users.technologytransferedit', key_str = item.name)}}" >Edit</a>
                                            <a href="{{url_for('users.technologytransferdelete', key_str = item.name)}}" >Delete</a>
                                        </div>
                                    </div>
                                </div>
                            {% endif %}
                        {% endfor %}
                    
                    </div>
			    </div>
                
                {% endblock %}
            """


@users.route('/technologytransfer', methods=['GET'])
@login_required
def technologytransfer():
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        if hasattr(user, 'objects') == True:
            ######## IndustryCollaboration ##############
            # #########  <a href="{{url_for('users.indcolabedit', key_str = item.name)}}" >Edit</a> ; def __str__(self): return self.name  ;  It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
            return render_template_string(technologytransfer_view, technologytransfer=user.technologytransfer)
        else:
            return redirect('/')


@users.route('/technologytransferedit/<key_str>', methods=['GET', 'POST'])
@login_required
def technologytransferedit(key_str):
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        usertechnologytransferform = UserTechnologyTransferForm()
        if hasattr(user, 'objects') == True:
            ######## technologytransfer ##############
            for p in user.technologytransfer:
                # <a href="{{url_for('users.indcolabedit', key_str = item.name)}}" >Edit</a> ; def __str__(self): return self.name  ;  It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
                if str(p) == key_str:
                    usertechnologytransferform.name.data = p.name
                    usertechnologytransferform.technology.data = p.technology
                    usertechnologytransferform.url.data = p.url
                    usertechnologytransferform.royalty.data = p.royalty
        return render_template_string(edit_create_view, form=usertechnologytransferform, fn_target='users.technologytransferedit', key_str=key_str)
        # return render_template('/user/technologytransfer.html', form=usertechnologytransferform)
    if request.method == 'POST':
        usertechnologytransferform = UserTechnologyTransferForm(request.form)
        if usertechnologytransferform.validate_on_submit():
            ######## Faculty #############
            if hasattr(user, 'objects') == True:
                for p in user.technologytransfer:
                    # <a href="{{url_for('users.indcolabedit', key_str = item.name)}}" >Edit</a> ; def __str__(self): return self.name  ;  It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
                    if str(p) == key_str:
                        p.name = usertechnologytransferform.name.data
                        p.technology = usertechnologytransferform.technology.data
                        p.url = usertechnologytransferform.url.data
                        p.royalty = usertechnologytransferform.royalty.data
                        user.save()
                        print('Contact Saved')
            # print(jsonify(user).get_json())
        return render_template_string(technologytransfer_view, technologytransfer=user.technologytransfer)
        # return render_template('/user/technologytransfer.html', form=usertechnologytransferform)


@users.route('/technologytransfercreate', methods=['GET', 'POST'])  # create
@login_required
def technologytransfercreate():
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        usertechnologytransferform = UserTechnologyTransferForm()
        if hasattr(user, 'objects') == True:
            return render_template_string(edit_create_view, form=usertechnologytransferform, fn_target='users.technologytransfercreate', key_str=None)
    if request.method == 'POST':
        usertechnologytransferform = UserTechnologyTransferForm(request.form)
        if usertechnologytransferform.validate_on_submit():
            ######## industrycollaboration #############
            if hasattr(user, 'objects') == True:
                p = TechnologyTransfer(name=usertechnologytransferform.name.data, technology=usertechnologytransferform.technology.data, url=usertechnologytransferform.url.data, royalty=usertechnologytransferform.royalty.data
                                       )
                user.technologytransfer.append(p)
                user.save()
        return render_template_string(technologytransfer_view, technologytransfer=user.technologytransfer)


@users.route('/technologytransferdelete/<key_str>', methods=['GET'])  # delete
@login_required
def technologytransferdelete(key_str):
    user = User.objects(username=current_user.username).first()
    if request.method == 'GET':
        if hasattr(user, 'objects') == True:
            for p in user.technologytransfer:
                # <a href="{{url_for('users.indcolabedit', key_str = item.name)}}" >Edit</a> ; def __str__(self): return self.name  ;  It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
                if str(p) == key_str:
                    user.technologytransfer.remove(p)
                    user.save()
        return render_template_string(technologytransfer_view, technologytransfer=user.technologytransfer)
