#from curses import mouseinterval
from hashlib import new
import os
from collections import namedtuple
from unicodedata import name
from flask import Blueprint, session, request, current_app, flash, render_template, redirect, url_for, render_template,  jsonify, render_template_string
# , login_manager, LoginManager, UserMixin, login_user, logout_user,
from flask_login import current_user, login_required
from bson.objectid import ObjectId
from mongoengine import URLField, StringField, EmailField
from mongoengine.errors import ValidationError, DoesNotExist, NotUniqueError
#from wtforms import BooleanField, StringField, PasswordField, validators, SubmitField, EmailField
#from flask_user import login_required, UserManager, UserMixin
from pymongo import ReturnDocument
import json
# from flask.ext.mongoengine.wtf import model_form

# from . import bcrypt # circular import
from . import Add, Faculty, Student, University, Department, SponsoredProjects, Patents, IndustryCollaboration # Address, Contact,
# mongoengine, bcrypt, app
from . import StartUp, Books, Awards, SocialImpact, TechnologyTransfer, db, bcrypt, csrf, User, LinkDesc, get_a_uuid
from .models import UserContactsForm, UserLoginForm, UserFacultyForm, UserStudentForm, UserTargetForm, UserUniversityForm, UserDepartmentForm, UserSponsoredProjectsForm
from .models import  UserPatentsForm, UserIndustryCollaborationForm, UserStartUpForm, UserBooksForm, UserAwardsForm, UserSocialImpactForm, UserTechnologyTransferForm, UserInformation, UserRoleForm, UserNewForm
from .models import UploadForm, AddressForm, SocialMediaAddressForm

from werkzeug.utils import secure_filename


users = Blueprint('users', __name__)

# change the comments
def Iscurrentuseradmin():
    return True
    # if current_user is None:
    #     return False
    #     # flash('You are not LogedIn')
    #     # return render_template_string(errormessages,messages='You are not LogedIn')
    # for role in current_user.roles:
    #     if role == current_app.config["ADMIN"]:
    #         return True
    # return False

###### /id/id1/id2/id3
#id = None id1 = None id2 = None id3 = None
# # editcreateview = """
# #     {% from 'form_macros.html' import edit_create_view %}
# #     {% extends "base.html" %} {% block content %}
# #         {{edit_create_view(form = form, fn_target = fn_target, kwargs = kwargs, backurl = backurl, id=id, id1=id1, id2=id2, id3=id3, id4=id4, id5=id5, enctypevalue = "application/x-www-form-urlencoded")}}
# #     {% endblock %}
# #     """
edit_create_view_id = """{% from 'form_macros.html' import render_field, render_checkbox_field, render_radio_field, render_submit_field, render_flashed_messages %}
                {% extends "base.html" %} {% block content %}
                {{render_flashed_messages()}}
                {% if id != None %}
                    {% if id1 != None %}
                        {% if id2 != None %}
                            {% if id3 != None %}
                                {% if id4 != None %}
                                    {% if id5 != None %}
                                        <form action="{{ url_for(fn_target, id = id, id1 = id1, id2 = id2, id3 = id3, id4 = id4, id5 = id5) }}" method="POST">
                                    {% else %}
                                        <form action="{{ url_for(fn_target, id = id, id1 = id1, id2 = id2, id3 = id3, id4 = id4) }}" method="POST">
                                    {% endif %}
                                {% else %}
                                    <form action="{{ url_for(fn_target, id = id, id1 = id1, id2 = id2, id3 = id3) }}" method="POST">
                                {% endif %}
                            {% else %}
                                <form action="{{ url_for(fn_target, id = id, id1 = id1, id2 = id2) }}" method="POST">
                            {% endif %}
                        {% else %}
                            <form action="{{ url_for(fn_target, id = id, id1 = id1) }}" method="POST">
                        {% endif %}
                    {% else %}
                        <form action="{{ url_for(fn_target, id = id) }}" method="POST">
                    {% endif %}
                {% else %}
                    <form action="{{ url_for(fn_target) }}" method="POST">
                {% endif %}
                {{ form.hidden_tag() }}
                {{ form.csrf_token }}
                <input type="hidden" class="form-control col-sm-2 col-form-label ms-5" name="next" value={{back}} />
                {% for field in form %}
                <div class="form-group row mb-1 {{ kwargs.get('bold_', '')}}">
                    {% if field.type == 'SubmitField' %}
                        {{render_submit_field(field)}}
                    {% else %}
                        {% if field.type == 'BooleanField' %}
                            {{render_checkbox_field(field, **kwargs)}}
                        {% else %}
                            {% if field.type != 'HiddenField' %}
                                {% if field.id != 'csrf_token' %}
                                    {{render_field(field, **kwargs)}}
                                {% endif %}
                            {% endif %}
                        {% endif %}
                    {% endif %}
                </div>
                {% endfor %}
                </form>
                {% endblock %}
                """
# dict to html table
details_dict_view = """"  
    {% extends "base.html" %} {% block content %}
    (<a href="{{url_for(fn_target, id = id)}}">Edit</a>)
    <table>
        <thead>
            <tr>
            <th>{{tablehead}}</th>
            <th>{{tableheadrvalue}} </th>
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
errormessages = """
                        {% extends "base.html" %} {% block content %}
                            {% with messages = get_flashed_messages() %}
                                {% if messages %}
                                    <ul class=flashes>
                                    {% for message in messages %}
                                    <li>{{ message }}</li>
                                    {% endfor %}
                                    </ul>
                                {% endif %}
                                {% endwith %}
                        {% endblock %}
                    """

@users.route('/userpapers', methods=['GET'])
@login_required
def userpapers():
    # Who can create user
    # A user having role Admin
    # Check role of Login User
    # print(current_app.config["STUDENT"])
    if Iscurrentuseradmin():
        if request.method == 'GET':
            tid = session["target_id"]  #user
            user = User.objects(id=tid).first()
            return render_template_string("""
                                {% extends "base.html" %} {% block content %}
                                    <a href="{{url_for('papers.assignpapertouser')}}">Assign Paper to User</a>
                                    {% for pid in papers %}
                                    <h4>Paper {{pid}} Assigned to User  </h4>
                                    {% endfor %}
                                {% endblock %}
                                """
                                ,papers=user.papers)


@users.route('/createuser', methods=['GET', 'POST'])
@login_required
def createuser():
    # Who can create user
    # A user having role Admin
    # Check role of Login User
    # print(current_app.config["STUDENT"])
    if Iscurrentuseradmin():
        if request.method == 'GET':
            uform = UserNewForm()
            return render_template_string(editcreateview, form=uform, fn_target='users.createuser'
                                      , id=None, id1=None, id2=None, id3=None, id4=None, id5=None
                                      , backurl = request.referrer
                                      , kwargs = {'class_':'form-control fw-bold'})
        
        if request.method == 'POST':
            uform = UserNewForm(request.form)
            if uform.validate_on_submit():
                username = uform.username.data #request.form.get("username")
                password = uform.password.data #request.form.get("password")
                passwd = uform.passwd.data #request.form.get("passwd")
                
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
                                <h3>User {{username}} already Exits  </h3>
                            {% endblock %}
                        """
                        ,username=username)
                    if userexistflag == False:
                        pw_hash = bcrypt.generate_password_hash(uform.password.data)
                        user = User(username=uform.username.data, password=pw_hash)
                        user.save()
                        # Find user
                        usr = User.objects(username=uform.username.data).first()
                        # ho_add = Address()
                        # ho_add.home = Add()
                        # ho_add.office = Add()
                        # cont = Contact()
                        # cont.address = ho_add
                        # usr.contact = cont
                        
                        # usr.faculty = Faculty()
                        # usr.student = Student()
                        # uni_vty = University()
                        # uni_vty.office = Add()
                        # usr.university = uni_vty
                        # dept = Department()
                        # dept.office = Add()
                        # usr.department = dept
                        usr.save()
                        return render_template_string("""
                            {% extends "base.html" %} {% block content %}
                                <a href="{{url_for('users.userrolescreate', id = id)}}">Add New Role to User</a>
                                <h3>User {{username}} is registerd. Fill other detiails </h3>
                            {% endblock %}
                        """
                        ,username=username, id = usr.id)
                else:
                    print("vsxjvajsvj")
                    print(passwd)
                    print(password)
            return redirect('/')
    else:
        return redirect(url_for('auth.logout'))

@users.route('/userdelete/<uname>', methods=['GET'])  # username
@login_required
def userdelete(uname):
    if Iscurrentuseradmin():
        user = User.objects(username=uname).first()
        if request.method == 'GET':
            if hasattr(user, 'objects') == True:
                ######### Check wether deleting user is Admin  ################
                flag_deletinguser_admin = False
                for role in user.roles:
                    if role == current_app.config["ADMIN"]:
                        flag_deletinguser_admin = True
                if flag_deletinguser_admin == False:
                    user.delete()
                #user.save()
            return redirect('/allusers')

@users.route('/allusers', methods=['GET'])
@login_required
def allusers(): ########### Check for role #### Admin Only
    if Iscurrentuseradmin():
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
    if Iscurrentuseradmin():
        if request.method == 'GET':
            userroleform = UserRoleForm()
            userroleform.role.data = role
            ######## userroles ##############
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

##############################################  User Target for Editing/Modification  ##################################################
usertarget_view = """
                {% extends "base.html" %} {% block content %}
                <a href="{{url_for('users.usertargetselect')}}">User Target for selection</a>
                
                <div class="container">
                    <div class="row mt-5">

                        
                        <div class="col-md-4">
                            <div class="card bg-dark text-center text-white">
                                <div class="card-header fw-bold fs-2">
                                    <h3>Current/LogedIn User</h3> 
                                </div>
                                <div class="card-body">
                                    <h4>{{current_user.username}}</h4>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="card bg-dark text-center text-white">
                                <div class="card-header fw-bold fs-2">
                                    <h3>User Target</h3> 
                                </div>
                                <div class="card-body">
                                    <h4>{{usertarget}}</h4>
                                </div>
                            </div>
                        </div>

                    </div>
			    </div>
                
                {% endblock %}
            """

@users.route('/usertarget', methods=['GET'])
@login_required
def usertarget():
    if Iscurrentuseradmin():
        user = User.objects(username=current_user.username).first()
        if request.method == 'GET':
            if hasattr(user, 'objects') == True:
                ######## userroles ##############
                tid = session["target_id"]
                user = User.objects(id=tid).first()
                return render_template_string(usertarget_view, usertarget=user.username)
            else:
                return redirect('/')

@users.route('/usertargetselect', methods=['GET', 'POST'])
@login_required
def usertargetselect():
    if Iscurrentuseradmin():
        tid = session["target_id"]
        user = User.objects(id=tid).first()
        if request.method == 'GET':
            if hasattr(user, 'objects') == True:
                uform = UserTargetForm()
                ######## usertarget ##############
                return render_template_string(editcreateview, form=uform, fn_target='users.usertargetselect'
                                      , id=None, id1=None, id2=None, id3=None, id4=None, id5=None
                                      , backurl = request.referrer
                                      , kwargs = {'class_':'form-control fw-bold'})
        if request.method == 'POST':
            uform = UserTargetForm(request.form)
            if uform.validate_on_submit():
                ######## usertarget #############
                user = User.objects(username=uform.usertarget.data).first()
                if hasattr(user, 'objects') == True:
                    session["target_id"] = user.id
                    session["target_username"] = user.username
                    return render_template_string(usertarget_view, usertarget=user.username)
                else:
                    return render_template_string(usertarget_view, usertarget='Target User Not Found')
        
##############################################  User and its Roles  ##################################################
userroles_view = """
                {% extends "base.html" %} {% block content %}
                <a href="{{url_for('users.userrolescreate', id = id)}}">Add New Role to User</a>
                
                <div class="container">
                    <div class="row mt-5">

                        {% for item in userroles %}
                            <div class="col-md-4">
                                <div class="card bg-dark text-center text-white">
                                    <div class="card-header fw-bold fs-2">
                                        <h3>{{item}}</h3> 
                                    </div>
                                    <div class="card-body">
                                        <a href="{{url_for('users.userrolesedit', id = id, id1 = item)}}" >Edit</a>
                                        <a href="{{url_for('users.userrolesdelete', id = id, id1 = item)}}" >Delete</a>
                                    </div>
                                </div>
                            </div>
                        {% endfor %}
                    
                    </div>
			    </div>
                
                {% endblock %}
            """

@users.route('/userroles', methods=['GET'])
#@login_required
def userroles():
    if Iscurrentuseradmin():
        #user = User.objects(username=current_user.username).first()
        tid = session["target_id"]
        user = User.objects(id=tid).first()
        if request.method == 'GET':
            if hasattr(user, 'objects') == True:
                ######## userroles ##############
                return render_template_string(userroles_view, userroles=user.roles, id = user.id)
            else:
                return redirect('/')
    else:
        flash('You are not Admin')
        return render_template_string("""
                        {% extends "base.html" %} {% block content %}
                            {% with messages = get_flashed_messages() %}
                                {% if messages %}
                                    <ul class=flashes>
                                    {% for message in messages %}
                                    <li>{{ message }}</li>
                                    {% endfor %}
                                    </ul>
                                {% endif %}
                                {% endwith %}
                        {% endblock %}
                    """
                    )
  
@users.route('/userrolescreate/<id>', methods=['GET', 'POST'])
@login_required
def userrolescreate(id):
    if Iscurrentuseradmin():
        #user = User.objects(username=current_user.username).first()
        #tid = session["target_id"]
        user = User.objects(id=id).first()
        if request.method == 'GET':
            if hasattr(user, 'objects') == True:
                uform = UserRoleForm()
                ######## userroles ##############
                return render_template_string(editcreateview, form=uform, fn_target='users.userrolescreate'
                                      , id=id, id1=None, id2=None, id3=None, id4=None, id5=None
                                      , backurl = request.referrer
                                      , kwargs = {'class_':'form-control fw-bold'})
        if request.method == 'POST':
            uform = UserRoleForm(request.form)
            if uform.validate_on_submit():
                ######## userroles #############
                if hasattr(user, 'objects') == True:
                    user.roles.append(uform.role.data)
                    user.save()
                    return redirect(request.form.get('next'))
    else:
        flash('You are not Admin')
        return render_template_string("""
                        {% extends "base.html" %} {% block content %}
                            {% with messages = get_flashed_messages() %}
                                {% if messages %}
                                    <ul class=flashes>
                                    {% for message in messages %}
                                    <li>{{ message }}</li>
                                    {% endfor %}
                                    </ul>
                                {% endif %}
                                {% endwith %}
                        {% endblock %}
                    """
                    )

@users.route('/userrolesedit/<id>/<id1>', methods=['GET', 'POST'])  # username
@login_required
def userrolesedit(id,id1):
    if Iscurrentuseradmin():
        #user = User.objects(username=current_user.username).first()
        #tid = session["target_id"]
        user = User.objects(id=id).first()
        if request.method == 'GET':
            uform = UserRoleForm()
            if hasattr(user, 'objects') == True:
                for r in user.roles:
                    if r == id1:
                        uform.role.data = id1
            return render_template_string(editcreateview, form=uform, fn_target='users.userrolesedit'
                                      , id=id, id1=id1, id2=None, id3=None, id4=None, id5=None
                                      , backurl = request.referrer
                                      , kwargs = {'class_':'form-control fw-bold'})
        if request.method == 'POST':
            uform = UserRoleForm(request.form)
            if uform.validate_on_submit():
                if hasattr(user, 'objects') == True:
                    for r in user.roles:
                        if r == id1:
                            i = user.roles.index(r)
                            user.roles[i] = uform.role.data
                            user.save()
                return redirect(request.form.get('next'))

@users.route('/userrolesdelete/<id>/<id1>', methods=['GET'])  # username
@login_required
def userrolesdelete(id,id1):
    if Iscurrentuseradmin(): 
        #user = User.objects(username=current_user.username).first()
        #tid = session["target_id"]
        user = User.objects(id=id).first()
        if request.method == 'GET':
            if hasattr(user, 'objects') == True:
                for r in user.roles:
                    if r == id1:
                        user.roles.remove(r)
                        user.save()
            return redirect(request.form.get('next'))

###########################################################  user details  ##########################################################################
@users.route('/userdetails', methods=['GET'])  # username
@login_required
def userdetails():
    #user = User.objects(username=current_user.username).first()
    tid = session["target_id"]
    user = User.objects(id=tid).first()
    if request.method == 'GET':
        if hasattr(user, 'objects') == True:
            print(user.personal_dict())
            return render_template_string(details_dict_view, fn_target='users.userdetailsedit', id = user.id
                                         ,userdict=user.personal_dict(),tablehead='Personal Details',tableheadrvalue='Information')

@users.route('/userdetailsedit/<id>', methods=['GET', 'POST'])  # username
@login_required
def userdetailsedit(id):
    #user = User.objects(username=current_user.username).first()
    #tid = session["target_id"]
    user = User.objects(id=id).first()
    if request.method == 'GET':
        if hasattr(user, 'objects') == True:
            uform = UserInformation()
            uform.fname.data=user.fname
            uform.mname.data=user.mname
            uform.lname.data=user.lname
            uform.title.data=user.title
            uform.directory.data=user.directory
            uform.photo.data=user.photo
            uform.qualifications.data=user.qualifications
            uform.areas_of_interest.data=user.areas_of_interest
            uform.bio.data=user.bio
            uform.publications.data=user.publications 
            # return render_template('/user/userdetails.html',usr = jsonify(user).get_json())
            # return render_template('/user/userdetails.html', fname=user.fname,mname=user.mname,lname=user.lname,directory=user.directory,photo=user.photo
            # ,qualifications=user.qualifications,areas_of_interest=user.areas_of_interest,bio=user.bio,publications=user.publications)
            return render_template_string(editcreateview, form=uform, fn_target='users.userdetailsedit'
                                      , id=id, id1=None, id2=None, id3=None, id4=None, id5=None
                                      , backurl = request.referrer
                                      , kwargs = {'class_':'form-control fw-bold'})

    if request.method == 'POST':
        if hasattr(user, 'objects') == True:
            uform = UserInformation(request.form)
            user.fname = uform.fname.data
            user.mname = uform.mname.data
            user.lname = uform.lname.data
            user.title = uform.title.data
            user.directory = uform.directory.data
            user.photo = uform.photo.data
            user.qualifications = uform.qualifications.data
            user.areas_of_interest = uform.areas_of_interest.data
            user.bio = uform.bio.data
            user.publications = uform.publications.data
            user.save()
            #print('Contact Saved')
            # print(jsonify(user).get_json())
        return redirect(request.form.get('next'))
        #return render_template_string(details_dict_view,userdict=user.personal_dict(),tablehead='Personal Details',tableheadrvalue='Information',fn_target='users.userdetailsedit')
        
################################# user Photo ##################################################
@users.route('/userphoto', methods=['GET', 'POST'])
@login_required
def userphoto():
    tid = session["target_id"]
    user = User.objects(id=tid).first()

    #if request.method == 'GET':
    if hasattr(user, 'objects') == True:
        uf = UploadForm()
        
        if uf.validate_on_submit():
            filename = secure_filename(uf.file.data.filename) # The function might return an empty filename. 
            #It's your responsibility to ensure that the filename is unique and that you abort or generate a random filename if the function returned an empty one.
            #print(filename)
            split_tup = os.path.splitext(filename) # fname = split_tup[0] filetype = split_tup[1]
            file_newname = ''.join(letter for letter in user.username if letter.isalnum())
            fn = file_newname +  split_tup[1]
            #print(fn)
            uf.file.data.save('static/images/' + fn)
            user.photo = fn
            user.save()
            return redirect(url_for('users.userdetails'))
        
        return render_template_string("""
            {% extends "base.html" %} {% block content %}
            
            <form method="post" enctype="multipart/form-data">
                {{ form.hidden_tag() }}
                {{ form.file }}
                <input type="submit">
            </form>
            {% endblock %}
        """, form=uf)

#############################################################   Add   #################################################

# id = target_id, id1 = contacts/university/dept etc , id2 = Add, id3 = sm 
# class property name / id pair eg (university/id) (contacts/id) (add/id)
# l1 url userid/'contacts'/addtype/desc
# Add at level 1 list 
@users.route('/addcreatel1/<id>/<id1>', methods=['GET', 'POST'])  
@login_required
def addcreatel1(id,id1):
    if request.method == 'GET':
        #print(request.referrer)
        
        # id(level 0) for which user in document 
        #usr = User.objects(id=id).first() # l0 = Target user object at lavel 0
        
        # id1 for level 1 property(List) e.g. list of contacts/faculty ... etc
        # it will return List of property
        #l1 = getattr(usr,str(id1)) # l1 = object at lavel 1 e.g. contacts/faculty/department ... etc
        # check l1 (object at level 1 is empty list  ################isinstance(l1, list):
        # if not l1:
        #     return render_template_string("""
        #                         {% extends "base.html" %} {% block content %}
        #                             <h3>Property {{addtype}} is not in user </h3>
        #                         {% endblock %}
        #                             """,addtype=str(id1))
        
        # id2 for specifice object with id2 in EmbeddedDocumentListField
        #l1 is list of address Add
        #ad = l1.get(addtype = id2)
        
        #ad = usr.contacts.get(addtype = str(id1))
        #print(ad.view__dict())
        #uform = UserContactsForm()
        # uform.contact.addtype.data = ad.addtype
        # uform.contact.add.data = ad.add
        # uform.contact.state.data = ad.state
        # uform.contact.pin.data = ad.pin
        # uform.contact.countary.data = ad.countary
        # uform.contact.phone.data = ad.phone
        # uform.contact.land.data = ad.land
        # uform.contact.email.data = ad.email
        uform = AddressForm()
        # uform.addtype.data = ad.addtype
        # uform.add.data = ad.add
        # uform.state.data = ad.state
        # uform.pin.data = ad.pin
        # uform.countary.data = ad.countary
        # uform.phone.data = ad.phone
        # uform.land.data = ad.land
        # uform.email.data = ad.email
        return render_template_string(edit_create_view_id, form=uform, fn_target='users.addcreatel1'
                                      , id=id, id1=id1, id2=None, id3=None, id4=None, id5=None
                                      , back = request.referrer
                                      , kwargs = {'class_':'form-control fw-bold'})
    if request.method == 'POST':
        #uform = UserContactsForm(request.form)
        uform = AddressForm(request.form)
        if uform.validate_on_submit():
            try:
                # id(level 0) for which user in document
                uid = ObjectId(id)#session["target_id"]
                usr = User.objects(id=uid).first() # Target user id
                
                # id1 for level 1 property(List) e.g. list of contacts/faculty ... etc
                # it will return List of property
                l1 = getattr(usr,str(id1)) # l1 = object at lavel 1 e.g. contacts ... etc
                
                #check duplicate Social Media Address
                #ad_duplicate = l1.filter(addtype = uform.contact.data['addtype'])
                ad_duplicate = l1.filter(addtype = uform.addtype.data)
                if ad_duplicate.count() > 0: # changed uform.addtype.data is already in in oyher addtype object
                    return render_template_string("""
                        {% extends "base.html" %} {% block content %}
                            <h3>addtype {{addtype}} is in list </h3>
                        {% endblock %}
                            """,addtype=uform.addtype.data)
                else:
                    # id2 for specifice object with id2 in EmbeddedDocumentListField
                    a_d = Add(#l1.get(addtype = id2)
                        addtype = uform.addtype.data
                        ,add = uform.add.data
                        ,state = uform.state.data
                        ,pin = uform.pin.data
                        ,countary = uform.countary.data
                        ,phone = uform.phone.data
                        ,land = uform.land.data
                        ,email = uform.email.data
                        )
                    #a_d = usr.contacts.get(addtype = id1)
                    # a_d.addtype = uform.contact.data['addtype']
                    # a_d.add = uform.contact.data['add']
                    # a_d.state = uform.contact.data['state']
                    # a_d.pin = uform.contact.data['pin']
                    # a_d.countary = uform.contact.data['countary']
                    # a_d.phone = uform.contact.data['phone']
                    # a_d.land = uform.contact.data['land']
                    # a_d.email = uform.contact.data['email']
                    l1.append(a_d)
                    usr.save()
                    return redirect(request.form.get('next'))
            except DoesNotExist as e:
                flash(id1 + ' Doest Not Exist')
                return render_template_string(errormessages,messages= id1 + ' Doest Not Exist')
            except ValidationError as e:
                flash(e.message)
                flash(e.field_name)
                flash(e.errors)
                return render_template_string(errormessages,messages=e.message)

# Add at level 2 list
# userid at level 0 /class property or attribute name(id1) at level 1 / attribute name at level 2 / value of arribute at level 2
@users.route('/addcreatel2/<id>/<id1>/<id2>/<id3>', methods=['GET', 'POST'])  
@login_required
def addcreatel2(id,id1,id2,id3):
    if request.method == 'GET':
        uform = AddressForm()
        return render_template_string(edit_create_view_id, form=uform, fn_target='users.addcreatel2'
                                      , id=id, id1=id1, id2=id2, id3=id3, id4=None, id5=None
                                      , back = request.referrer
                                      , kwargs = {'class_':'form-control fw-bold'})
    if request.method == 'POST':
        #uform = UserContactsForm(request.form)
        uform = AddressForm(request.form)
        if uform.validate_on_submit():
            try:
                # id(level 0) for which user in document
                uid = ObjectId(id)#session["target_id"]
                usr = User.objects(id=uid).first() # Target user id
                
                # id1 for level 1 property(List) e.g. list of contacts/faculty ... etc
                # it will return List of property
                l1 = getattr(usr,str(id1)) # l1 = object at lavel 1 e.g. contacts ... etc
                
                l2 = l1.get(pk = id2) # Dept/Uni ... etc
                
                l3 = getattr(l2,str(id3)) # List of attribute id3 eg. department atribute office list id3='office'
                #ad = l3.get(addtype = id5) # find perticuler address object in list 
                
                #check duplicate Social Media Address
                #ad_duplicate = l1.filter(addtype = uform.contact.data['addtype'])
                ad_duplicate = l3.filter(addtype = uform.addtype.data)
                if ad_duplicate.count() > 0: # changed uform.addtype.data is already in in oyher addtype object
                    return render_template_string("""
                        {% extends "base.html" %} {% block content %}
                            <h3>addtype {{addtype}} is in list </h3>
                        {% endblock %}
                            """,addtype=uform.addtype.data)
                else:
                    # id2 for specifice object with id2 in EmbeddedDocumentListField
                    a_d = Add(#l1.get(addtype = id2)
                        addtype = uform.addtype.data
                        ,add = uform.add.data
                        ,state = uform.state.data
                        ,pin = uform.pin.data
                        ,countary = uform.countary.data
                        ,phone = uform.phone.data
                        ,land = uform.land.data
                        ,email = uform.email.data
                        )
                    #a_d = usr.contacts.get(addtype = id1)
                    # a_d.addtype = uform.contact.data['addtype']
                    # a_d.add = uform.contact.data['add']
                    # a_d.state = uform.contact.data['state']
                    # a_d.pin = uform.contact.data['pin']
                    # a_d.countary = uform.contact.data['countary']
                    # a_d.phone = uform.contact.data['phone']
                    # a_d.land = uform.contact.data['land']
                    # a_d.email = uform.contact.data['email']
                    l3.append(a_d)
                    usr.save()
                    return redirect(request.form.get('next'))
            except DoesNotExist as e:
                flash(id1 + ' Doest Not Exist')
                return render_template_string(errormessages,messages= id1 + ' Doest Not Exist')
            except ValidationError as e:
                flash(e.message)
                flash(e.field_name)
                flash(e.errors)
                return render_template_string(errormessages,messages=e.message)

@users.route('/addeditl1/<id>/<id1>/<id2>', methods=['GET', 'POST'])  
@login_required
def addeditl1(id,id1,id2):
    if request.method == 'GET':
        #print(request.referrer)
        
        # id(level 0) for which user in document 
        usr = User.objects(id=id).first() # l0 = Target user object at lavel 0
        
        # id1 for level 1 property(List) e.g. list of contacts/faculty ... etc
        # it will return List of property
        l1 = getattr(usr,str(id1)) # l1 = object at lavel 1 e.g. contacts/faculty ... etc
        # check l1 (object at level 1 is empty list  ################isinstance(l1, list):
        if not l1:
            return render_template_string("""
                                {% extends "base.html" %} {% block content %}
                                    <h3>Property {{addtype}} is not in user </h3>
                                {% endblock %}
                                    """,addtype=str(id1))
        
        # id2 for specifice object with id2 in EmbeddedDocumentListField
        #l1 is list of address Add so addtype = id2
        # if list of Add is at level 1
        ad = l1.get(addtype = id2)
        
        
        uform = AddressForm()
        uform.addtype.data = ad.addtype
        uform.add.data = ad.add
        uform.state.data = ad.state
        uform.pin.data = ad.pin
        uform.countary.data = ad.countary
        uform.phone.data = ad.phone
        uform.land.data = ad.land
        uform.email.data = ad.email
        return render_template_string(edit_create_view_id, form=uform, fn_target='users.addeditl1'
                                      , id=id, id1=id1, id2=id2, id3=None, id4=None, id5=None
                                      , back = request.referrer
                                      , kwargs = {'class_':'form-control fw-bold'})
    if request.method == 'POST':
        #uform = UserContactsForm(request.form)
        uform = AddressForm(request.form)
        if uform.validate_on_submit():
            try:
                # id(level 0) for which user in document
                uid = ObjectId(id)#session["target_id"]
                usr = User.objects(id=uid).first() # Target user id
                
                # id1 for level 1 property(List) e.g. list of contacts/faculty ... etc
                # it will return List of property
                l1 = getattr(usr,str(id1)) # l1 = object at lavel 1 e.g. contacts/faculty ... etc
                
                #check duplicate Social Media Address
                #ad_duplicate = l1.filter(addtype = uform.contact.data['addtype'])
                # if list of Add is at level 1
                if uform.addtype.data != str(id2): #key addtype changed or not
                    ad_duplicate = l1.filter(addtype = uform.addtype.data)
                    if ad_duplicate.count() > 0: # changed uform.addtype.data is already in in other addtype object
                        return render_template_string("""
                            {% extends "base.html" %} {% block content %}
                                <h3>addtype {{addtype}} is in list </h3>
                            {% endblock %}
                                """,addtype=uform.addtype.data)
                    else:
                        a_d = l1.get(addtype = str(id2))
                        a_d.addtype = uform.addtype.data
                        a_d.add = uform.add.data
                        a_d.state = uform.state.data
                        a_d.pin = uform.pin.data
                        a_d.countary = uform.countary.data
                        a_d.phone = uform.phone.data
                        a_d.land = uform.land.data
                        a_d.email = uform.email.data
                        
                        usr.save()
                        return redirect(request.form.get('next'))
                else: #uform.addtype.data == str(id4)
                    # id2 for specifice object with id2 in EmbeddedDocumentListField
                    # if list of Add is at level 1
                    a_d = l1.get(addtype = str(id2)) 
                    ##a_d.addtype = uform.addtype.data
                    a_d.add = uform.add.data
                    a_d.state = uform.state.data
                    a_d.pin = uform.pin.data
                    a_d.countary = uform.countary.data
                    a_d.phone = uform.phone.data
                    a_d.land = uform.land.data
                    a_d.email = uform.email.data
                    
                    usr.save()
                    return redirect(request.form.get('next'))
            except DoesNotExist as e:
                flash(id1 + ' Doest Not Exist')
                return render_template_string(errormessages,messages= id1 + ' Doest Not Exist')
            except ValidationError as e:
                flash(e.message)
                flash(e.field_name)
                flash(e.errors)
                return render_template_string(errormessages,messages=e.message)

@users.route('/addeditl2/<id>/<id1>/<id2>/<id3>/<id4>', methods=['GET', 'POST'])  
@login_required
def addeditl2(id,id1,id2,id3,id4): # id5 stores old values addtype key
    if request.method == 'GET':
        
        try:
            # id(level 0) for which user in document 
            usr = User.objects(id=id).first() # l0 = Target user object at lavel 0
            
            # id1 for level 1 property(List) e.g. list of contacts/faculty ... etc
            # it will return List of property
            l1 = getattr(usr,str(id1)) # l1 = object at lavel 1 e.g. contacts/faculty ... etc
            # check l1 (object at level 1 is empty list  ################isinstance(l1, list):
            if not l1:
                return render_template_string("""
                                    {% extends "base.html" %} {% block content %}
                                        <h3>Property {{addtype}} is not in user </h3>
                                    {% endblock %}
                                        """,addtype=str(id1))
            l2 = l1.get(pk=id2) # Dept/Uni ... etc
            l3 = getattr(l2,str(id3)) # List of attribute id3 eg. department atribute office list id3='office'
            # id2 for specifice object with id2 in EmbeddedDocumentListField
            #l1 is list of address Add so addtype = id2
            # if list of Add is at level 1
            ad = l3.get(addtype = id4)
            
            uform = AddressForm()
            uform.addtype.data = ad.addtype
            uform.add.data = ad.add
            uform.state.data = ad.state
            uform.pin.data = ad.pin
            uform.countary.data = ad.countary
            uform.phone.data = ad.phone
            uform.land.data = ad.land
            uform.email.data = ad.email
            return render_template_string(edit_create_view_id, form=uform, fn_target='users.addeditl2'
                                        , id=id, id1=id1, id2=id2, id3=id3, id4 = id4, id5 = None
                                        , back = request.referrer
                                        , kwargs = {'class_':'form-control fw-bold'})
        except DoesNotExist as e:
            flash(id1 + ' Doest Not Exist')
            return render_template_string(errormessages,messages= id1 + ' Doest Not Exist')
        except ValidationError as e:
            flash(e.message)
            flash(e.field_name)
            flash(e.errors)
            return render_template_string(errormessages,messages=e.message) 
    if request.method == 'POST':
        #uform = UserContactsForm(request.form)
        uform = AddressForm(request.form)
        if uform.validate_on_submit():
            try:
                # id(level 0) for which user in document
                uid = ObjectId(id)#session["target_id"]
                usr = User.objects(id=uid).first() # Target user id
                
                # id1 for level 1 property(List) e.g. list of contacts/faculty ... etc
                # it will return List of property
                l1 = getattr(usr,str(id1)) # l1 = object at lavel 1 e.g. contacts/faculty ... etc
                l2 = l1.get(pk=id2) # Dept/Uni ... etc
                l3 = getattr(l2,str(id3)) # List of attribute id3 eg. department atribute office list id3='office'
                #check duplicate Social Media Address
                #ad_duplicate = l3.filter(addtype = uform.contact.data['addtype'])
                # if list of Add is at level 2
                
                if uform.addtype.data != str(id4): #key addtype changed or not
                    ad_duplicate = l3.filter(addtype = uform.addtype.data)
                    if ad_duplicate.count() > 0: # changed uform.addtype.data is already in in other addtype object
                        return render_template_string("""
                            {% extends "base.html" %} {% block content %}
                                <h3>addtype {{addtype}} is in list </h3>
                            {% endblock %}
                                """,addtype=uform.addtype.data)
                    else:
                        a_d = l3.get(addtype = str(id4))
                        a_d.addtype = uform.addtype.data
                        a_d.add = uform.add.data
                        a_d.state = uform.state.data
                        a_d.pin = uform.pin.data
                        a_d.countary = uform.countary.data
                        a_d.phone = uform.phone.data
                        a_d.land = uform.land.data
                        a_d.email = uform.email.data
                        
                        usr.save()
                        return redirect(request.form.get('next'))
                else: #uform.addtype.data == str(id4)
                    # id2 for specifice object with id2 in EmbeddedDocumentListField
                    # if list of Add is at level 1
                    a_d = l3.get(addtype = str(id4)) 
                    ##a_d.addtype = uform.addtype.data
                    a_d.add = uform.add.data
                    a_d.state = uform.state.data
                    a_d.pin = uform.pin.data
                    a_d.countary = uform.countary.data
                    a_d.phone = uform.phone.data
                    a_d.land = uform.land.data
                    a_d.email = uform.email.data
                    
                    usr.save()
                    return redirect(request.form.get('next'))
            except ValidationError as e:
                flash(e.message)
                flash(e.field_name)
                flash(e.errors)
                return render_template_string(errormessages,messages=e.message)

@users.route('/adddeletel1/<id>/<id1>/<id2>', methods=['GET', 'POST'])  
@login_required
def adddeletel1(id,id1,id2):
    if request.method == 'GET':
        try:
             #print(request.referrer)
        
            # id(level 0) for which user in document 
            usr = User.objects(id=id).first() # l0 = Target user object at lavel 0
            
            # id1 for level 1 property(List) e.g. list of contacts/faculty ... etc
            # it will return List of property
            l1 = getattr(usr,str(id1)) # l1 = object at lavel 1 e.g. contacts/faculty ... etc
            # check l1 (object at level 1 is empty list  ################isinstance(l1, list):
            if not l1:
                return render_template_string("""
                                    {% extends "base.html" %} {% block content %}
                                        <h3>Property {{addtype}} is not in user </h3>
                                    {% endblock %}
                                        """,addtype=str(id1))
            
            # id2 for specifice object with id2 in EmbeddedDocumentListField
            #l1 is list of address Add so addtype = id2
            # if list of Add is at level 1
            ad = l1.get(addtype = id2)
            l1.remove(ad)
            usr.save()
            return redirect(request.form.get('next'))
        except DoesNotExist as e:
            flash(id1 + ' Doest Not Exist')
            return render_template_string(errormessages,messages= id1 + ' Doest Not Exist')
        except ValidationError as e:
            flash(e.message)
            flash(e.field_name)
            flash(e.errors)
            return render_template_string(errormessages,messages=e.message)

@users.route('/adddeletel2/<id>/<id1>/<id2>/<id3>/<id4>', methods=['GET', 'POST'])  
@login_required
def adddeletel2(id,id1,id2,id3,id4): # id5 stores old values addtype key
    if request.method == 'GET':
        
        try:
            # id(level 0) for which user in document 
            usr = User.objects(id=id).first() # l0 = Target user object at lavel 0
            
            # id1 for level 1 property(List) e.g. list of contacts/faculty ... etc
            # it will return List of property
            l1 = getattr(usr,str(id1)) # l1 = object at lavel 1 e.g. contacts/faculty ... etc
            # check l1 (object at level 1 is empty list  ################isinstance(l1, list):
            if not l1:
                return render_template_string("""
                                    {% extends "base.html" %} {% block content %}
                                        <h3>Property {{addtype}} is not in user </h3>
                                    {% endblock %}
                                        """,addtype=str(id1))
            l2 = l1.get(pk=id2) # Dept/Uni ... etc
            l3 = getattr(l2,str(id3)) # List of attribute id3 eg. department atribute office list id3='office'
            # id2 for specifice object with id2 in EmbeddedDocumentListField
            #l1 is list of address Add so addtype = id2
            # if list of Add is at level 1
            ad = l3.get(addtype = id4)
            l3.remove(ad)
            usr.save()
            return redirect(request.form.get('next'))
        except DoesNotExist as e:
            flash(id1 + ' Doest Not Exist')
            return render_template_string(errormessages,messages= id1 + ' Doest Not Exist')
        except ValidationError as e:
            flash(e.message)
            flash(e.field_name)
            flash(e.errors)
            return render_template_string(errormessages,messages=e.message)

@users.route('/addsmcreatel1/<id>/<id1>/<id2>', methods=['GET', 'POST'])  
@login_required
def addsmcreatel1(id,id1,id2):
    if request.method == 'GET':
        
        uform = SocialMediaAddressForm()
        
        return render_template_string(edit_create_view_id, form=uform, fn_target='users.addsmcreatel1'
                                      , id=id, id1=id1, id2=id2, id3=None, id4=None, id5=None
                                      , back = request.referrer
                                      , kwargs = {'class_':'form-control fw-bold'})
    if request.method == 'POST':
        #uform = UserContactsForm(request.form)
        uform = SocialMediaAddressForm(request.form)
        if uform.validate_on_submit():
            try:
                # id(level 0) for which user in document
                uid = ObjectId(id)#session["target_id"]
                usr = User.objects(id=uid).first() # Target user id
                
                # id1 for level 1 property(List) e.g. list of contacts/faculty ... etc
                # it will return List of property
                l1 = getattr(usr,str(id1)) # l1 = object at lavel 1 e.g. contacts ... etc
                smlist = l1.get(addtype = id2).sm
                
                #check duplicate Social Media Address
                #ad_duplicate = l1.filter(addtype = uform.contact.data['addtype'])
                if smlist.filter(desc = uform.desc.data).count() > 0: # changed uform.addtype.data is already in in oyher addtype object
                    return render_template_string("""
                        {% extends "base.html" %} {% block content %}
                            <h3>Social Media {{desc}} is in list </h3>
                        {% endblock %}
                            """,desc=uform.desc.data)
                else:
                    smld = LinkDesc(pk = get_a_uuid()
                                    ,desc = uform.desc.data
                                    ,link = uform.link.data)
                    
                    smlist.append(smld)
                    usr.save()
                    return redirect(request.form.get('next'))
            except DoesNotExist as e:
                flash(id1 + ' Doest Not Exist')
                return render_template_string(errormessages,messages= id1 + ' Doest Not Exist')
            except ValidationError as e:
                flash(e.message)
                flash(e.field_name)
                flash(e.errors)
                return render_template_string(errormessages,messages=e.message)

@users.route('/addsmcreatel2/<id>/<id1>/<id2>/<id3>/<id4>', methods=['GET', 'POST'])  
@login_required
def addsmcreatel2(id,id1,id2,id3,id4):
    if request.method == 'GET':
        
        uform = SocialMediaAddressForm()
        
        return render_template_string(edit_create_view_id, form=uform, fn_target='users.addsmcreatel2'
                                      , id=id, id1=id1, id2=id2, id3=id3, id4=id4, id5=None
                                      , back = request.referrer
                                      , kwargs = {'class_':'form-control fw-bold'})
    if request.method == 'POST':
        #uform = UserContactsForm(request.form)
        uform = SocialMediaAddressForm(request.form)
        if uform.validate_on_submit():
            try:
                # id(level 0) for which user in document
                uid = ObjectId(id)#session["target_id"]
                usr = User.objects(id=uid).first() # Target user id
                
                # id1 for level 1 property(List) e.g. list of contacts/faculty ... etc
                # it will return List of property
                l1 = getattr(usr,str(id1)) # l1 = object at lavel 1 e.g. contacts ... etc
                l2 = l1.get(pk=id2) # Dept/Uni ... etc
                l3 = getattr(l2,str(id3)) # List of attribute id3 eg. department atribute office list id3='office'
            
                smlist = l3.get(addtype = id4).sm
                
                #check duplicate Social Media Address
                #ad_duplicate = l1.filter(addtype = uform.contact.data['addtype'])
                if smlist.filter(desc = uform.desc.data).count() > 0: # changed uform.addtype.data is already in in oyher addtype object
                    return render_template_string("""
                        {% extends "base.html" %} {% block content %}
                            <h3>Social Media {{desc}} is in list </h3>
                        {% endblock %}
                            """,desc=uform.desc.data)
                else:
                    smld = LinkDesc(pk = get_a_uuid()
                                    ,desc = uform.desc.data
                                    ,link = uform.link.data)
                    
                    smlist.append(smld)
                    usr.save()
                    return redirect(request.form.get('next'))
            except DoesNotExist as e:
                flash(id1 + ' Doest Not Exist')
                return render_template_string(errormessages,messages= id1 + ' Doest Not Exist')
            except ValidationError as e:
                flash(e.message)
                flash(e.field_name)
                flash(e.errors)
                return render_template_string(errormessages,messages=e.message)

@users.route('/addsmeditl1/<id>/<id1>/<id2>/<id3>', methods=['GET', 'POST'])  
@login_required
def addsmeditl1(id,id1,id2,id3):
    if request.method == 'GET':
        
        uform = SocialMediaAddressForm()
        uid = ObjectId(id)#session["target_id"]
        usr = User.objects(id=uid).first() # Target user id
        
        # id1 for level 1 property(List) e.g. list of contacts/faculty ... etc
        # it will return List of property
        l1 = getattr(usr,str(id1)) # l1 = object at lavel 1 e.g. contacts ... etc
        smlist = l1.get(addtype = id2).sm
        #dl = smlist.get(desc = id3) # LinkDesc
        dl = smlist.get(pk = id3) # LinkDesc
        uform.desc.data = dl.desc
        uform.link.data = dl.link
        
        return render_template_string(edit_create_view_id, form=uform, fn_target='users.addsmeditl1'
                                      , id=id, id1=id1, id2=id2, id3=id3, id4=None, id5=None
                                      , back = request.referrer
                                      , kwargs = {'class_':'form-control fw-bold'})
    if request.method == 'POST':
        #uform = UserContactsForm(request.form)
        uform = SocialMediaAddressForm(request.form)
        if uform.validate_on_submit():
            try:
                # id(level 0) for which user in document
                uid = ObjectId(id)#session["target_id"]
                usr = User.objects(id=uid).first() # Target user id
                
                # id1 for level 1 property(List) e.g. list of contacts/faculty ... etc
                # it will return List of property
                l1 = getattr(usr,str(id1)) # l1 = object at lavel 1 e.g. contacts ... etc
                smlist = l1.get(addtype = id2).sm
                #dl = smlist.get(desc = id3) # LinkDesc
                dl = smlist.get(pk = id3) # LinkDesc
                
                #check duplicate Social Media Address
                #ad_duplicate = l1.filter(addtype = uform.contact.data['addtype'])
                if smlist.filter(desc = uform.desc.data).count() > 0: # changed uform.addtype.data is already in in oyher addtype object
                    return render_template_string("""
                        {% extends "base.html" %} {% block content %}
                            <h3>Social Media {{desc}} is in list </h3>
                        {% endblock %}
                            """,desc=uform.desc.data)
                else:
                    dl.desc = uform.desc.data
                    dl.link = uform.link.data
                    
                    usr.save()
                    return redirect(request.form.get('next'))
                
            except DoesNotExist as e:
                flash(id1 + ' Doest Not Exist')
                return render_template_string(errormessages,messages= id1 + ' Doest Not Exist')
            except ValidationError as e:
                flash(e.message)
                flash(e.field_name)
                flash(e.errors)
                return render_template_string(errormessages,messages=e.message)

@users.route('/addsmeditl2/<id>/<id1>/<id2>/<id3>/<id4>/<id5>', methods=['GET', 'POST'])  
@login_required
def addsmeditl2(id,id1,id2,id3,id4,id5):
    if request.method == 'GET':
        
        uform = SocialMediaAddressForm()
        uid = ObjectId(id)#session["target_id"]
        usr = User.objects(id=uid).first() # Target user id
        
        # id1 for level 1 property(List) e.g. list of contacts/faculty ... etc
        # it will return List of property
        l1 = getattr(usr,str(id1)) # l1 = object at lavel 1 e.g. contacts ... etc
        l2 = l1.get(pk=id2) # Dept/Uni ... etc
        l3 = getattr(l2,str(id3)) # List of attribute id3 eg. department atribute office list id3='office'
    
        smlist = l3.get(addtype = id4).sm
        #dl = smlist.get(desc = id5)
        dl = smlist.get(pk = id5)
        uform.desc.data = dl.desc
        uform.link.data = dl.link
        
        return render_template_string(edit_create_view_id, form=uform, fn_target='users.addsmeditl2'
                                      , id=id, id1=id1, id2=id2, id3=id3, id4=id4, id5=id5
                                      , back = request.referrer
                                      , kwargs = {'class_':'form-control fw-bold'})
    if request.method == 'POST':
        #uform = UserContactsForm(request.form)
        uform = SocialMediaAddressForm(request.form)
        if uform.validate_on_submit():
            try:
                # id(level 0) for which user in document
                uid = ObjectId(id)#session["target_id"]
                usr = User.objects(id=uid).first() # Target user id
                
                # id1 for level 1 property(List) e.g. list of contacts/faculty ... etc
                # it will return List of property
                l1 = getattr(usr,str(id1)) # l1 = object at lavel 1 e.g. contacts ... etc
                l2 = l1.get(pk=id2) # Dept/Uni ... etc
                l3 = getattr(l2,str(id3)) # List of attribute id3 eg. department atribute office list id3='office'
            
                smlist = l3.get(addtype = id4).sm
                #dl = smlist.get(desc = id5)
                dl = smlist.get(pk = id5)
                #check duplicate Social Media Address
                #ad_duplicate = l1.filter(addtype = uform.contact.data['addtype'])
                if smlist.filter(desc = uform.desc.data).count() > 0: # changed uform.addtype.data is already in in oyher addtype object
                    return render_template_string("""
                        {% extends "base.html" %} {% block content %}
                            <h3>Social Media {{desc}} is in list </h3>
                        {% endblock %}
                            """,desc=uform.desc.data)
                else:
                    dl.desc = uform.desc.data
                    dl.link = uform.link.data
                    
                    usr.save()
                    return redirect(request.form.get('next'))
                
            except DoesNotExist as e:
                flash(id1 + ' Doest Not Exist')
                return render_template_string(errormessages,messages= id1 + ' Doest Not Exist')
            except ValidationError as e:
                flash(e.message)
                flash(e.field_name)
                flash(e.errors)
                return render_template_string(errormessages,messages=e.message)

@users.route('/addsmdeletel1/<id>/<id1>/<id2>/<id3>', methods=['GET', 'POST'])  
@login_required
def addsmdeletel1(id,id1,id2,id3):
    if request.method == 'GET':
        try:
            uid = ObjectId(id)#session["target_id"]
            usr = User.objects(id=uid).first() # Target user id
            
            # id1 for level 1 property(List) e.g. list of contacts/faculty ... etc
            # it will return List of property
            l1 = getattr(usr,str(id1)) # l1 = object at lavel 1 e.g. contacts ... etc
            smlist = l1.get(addtype = id2).sm
            #dl = smlist.get(desc = id3) # LinkDesc
            dl = smlist.get(pk = id3) # LinkDesc
            smlist.remove(dl)
            usr.save()
            return redirect(request.form.get('next'))
        except DoesNotExist as e:
                flash(id1 + ' Doest Not Exist')
                return render_template_string(errormessages,messages= id1 + ' Doest Not Exist')
        except ValidationError as e:
            flash(e.message)
            flash(e.field_name)
            flash(e.errors)
            return render_template_string(errormessages,messages=e.message)

@users.route('/addsmdeletel2/<id>/<id1>/<id2>/<id3>/<id4>/<id5>', methods=['GET', 'POST'])  
@login_required
def addsmdeletel2(id,id1,id2,id3,id4,id5):
    if request.method == 'GET':
        try:
            uid = ObjectId(id)#session["target_id"]
            usr = User.objects(id=uid).first() # Target user id
            
            # id1 for level 1 property(List) e.g. list of contacts/faculty ... etc
            # it will return List of property
            l1 = getattr(usr,str(id1)) # l1 = object at lavel 1 e.g. contacts ... etc
            l2 = l1.get(pk=id2) # Dept/Uni ... etc
            l3 = getattr(l2,str(id3)) # List of attribute id3 eg. department atribute office list id3='office'
        
            smlist = l3.get(addtype = id4).sm
            #dl = smlist.get(desc = id5)
            dl = smlist.get(pk = id5)
            smlist.remove(dl)
            usr.save()
            return redirect(request.form.get('next'))
        except DoesNotExist as e:
                flash(id1 + ' Doest Not Exist')
                return render_template_string(errormessages,messages= id1 + ' Doest Not Exist')
        except ValidationError as e:
            flash(e.message)
            flash(e.field_name)
            flash(e.errors)
            return render_template_string(errormessages,messages=e.message)
########################################################        ##############################################################

#############################################################  Contacts Add   ######################################################################################   
contacts_view = """
    {% from 'form_macros.html' import render_addl1 %}
    {% extends "base.html" %} {% block content %}
        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
        <input type="hidden" name="next" value={{back}} />
        <a href="{{url_for(fn_targetaddcreate, id = usrid, id1 = 'contacts' )}}">(New Address)</a></br>
        {{render_addl1(contacts, usrid, 'contacts',kwargs)}}
    {% endblock %}
    """  
      
@users.route('/contactsadd', methods=['GET'])  # username
@login_required
def contactsadd():
    if request.method == 'GET':
        uid = session["target_id"] # Target user id
        user = User.objects(id=uid).first()
        #print(pap.__dict__())
        return render_template_string(contacts_view #, fn_target='users.department' ## uform=FlaskForm()
                                      #,fn_create = 'users.facultycreate', fn_edit = 'users.facultyedit' , fn_delete = 'users.facultydelete'
                                      ,fn_targetaddcreate = 'users.addcreatel1', fn_targetaddedit = 'users.addeditl1' , fn_targetadddelete = 'users.adddeletel1'
                                      ,fn_targetsmcreate = 'users.addsmcreatel1',fn_targetsmedit = 'users.addsmeditl1', fn_targetsmdelete = 'users.addsmdeletel1'
                                      ,back = request.referrer
                                      ,contacts = user.contacts, usrid = user.id
                                      ,kwargs = {'class_':'form-control fw-bold'})
        

#############################################################      ######################################################################################



#####################################################################  faculty  #############################################################################
fac_view = """
    {% extends "base.html" %} {% block content %}
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
    <input type="hidden" name="next" value={{back}} />
    <a href="{{url_for(fn_create, id = usrid )}}">(New Faculty Roll)</a>
        {% for lst in faculty %}
            <div class="{{ kwargs.pop('class_', '') }}">
                <a href="{{url_for(fn_edit, id = usrid, id1 = lst.pk )}}">(Edit)</a>
                <a href="{{url_for(fn_delete, id = usrid, id1 = lst.pk )}}">(Delete)</a>
                <h3>Position : {{lst.position}}</h3>
                <h3>Post : {{lst.post}}</h3>
                <h3>Employee Code : {{lst.empcode}}</h3>
            </div>
        {% endfor %}
    {% endblock %}
    """
@users.route('/faculty', methods=['GET', 'POST'])  # username
@login_required
def faculty():
    #user = User.objects(username=current_user.username).first()
    tid = session["target_id"]
    user = User.objects(id=tid).first()
    if request.method == 'GET':
        if hasattr(user, 'objects') == True:
            return render_template_string(fac_view #, fn_target='users.department' ## uform=FlaskForm()
                                      ,fn_create = 'users.facultycreate', fn_edit = 'users.facultyedit' , fn_delete = 'users.facultydelete'
                                      #,fn_targetaddcreate = 'users.addcreatel2', fn_targetaddedit = 'users.addeditl2' , fn_targetadddelete = 'users.adddeletel2'
                                      #,fn_targetsmcreate = 'users.addsmcreatel2',fn_targetsmedit = 'users.addsmeditl2', fn_targetsmdelete = 'users.addsmdeletel2'
                                      ,back = request.referrer
                                      ,faculty = user.faculty, usrid = user.id
                                      ,kwargs = {'class_':'form-control fw-bold'})
            #return render_template_string(details_dict_view,userdict=user.faculty.faculty_dict(),tablehead='Faculty Details',tableheadrvalue='Information',fn_target='users.facultyedit')

@users.route('/facultycreate/<id>', methods=['GET', 'POST'])  # username
@login_required
def facultycreate(id):
    #id = session["target_id"]
    user = User.objects(id=id).first()
    if request.method == 'GET':
        uform = UserFacultyForm()
        if hasattr(user, 'objects') == True:
             return render_template_string(edit_create_view_id, form=uform, fn_target='users.facultycreate'
                                      , id=id, id1=None, id2=None, id3=None
                                      , back = request.referrer
                                      , kwargs = {'class_':'form-control fw-bold'})
    if request.method == 'POST':
        uform = UserFacultyForm(request.form)
        if uform.validate_on_submit():
            ######## industrycollaboration #############
            if hasattr(user, 'objects') == True:
                try:
                    # check for duplicate department entart
                    #print(user.university.filter(name = uform.name.data).count())
                    if user.faculty.filter(position = uform.position.data
                                ,post = uform.post.data
                                ,empcode = uform.empcode.data).count() > 0:
                        return render_template_string("""
                                    {% extends "base.html" %} {% block content %}
                                        <h3>faculty {{fac}} is in studet List </h3>
                                    {% endblock %}
                                        """,fac= uform.position.data + uform.post.data + uform.empcode.data )
                    
                    p = Faculty( pk = get_a_uuid()
                                , position = uform.position.data
                                ,post = uform.post.data
                                ,empcode = uform.empcode.data
                                )
                    user.faculty.append(p)
                    user.save()
                    return redirect(request.form.get('next'))
                except ValidationError as e:
                    flash(e.message)
                    flash(e.field_name)
                    flash(e.errors)
                    return render_template_string(errormessages,messages=e.message)

@users.route('/facultyedit/<id>/<id1>', methods=['GET', 'POST'])  # username
@login_required
def facultyedit(id,id1):
    #user = User.objects(username=current_user.username).first()
    #id = session["target_id"]
    user = User.objects(id=id).first()
    if request.method == 'GET':
        uform = UserFacultyForm()
        if hasattr(user, 'objects') == True:
            ######## faculty ##############
            fac = user.faculty.get(pk = id1)
            uform.position.data = fac.position
            uform.post.data = fac.post
            uform.empcode.data = fac.empcode
            
            return render_template_string(edit_create_view_id, form=uform, fn_target='users.facultyedit'
                                      , id=id, id1=id1, id2=None, id3=None
                                      , back = request.referrer
                                      , kwargs = {'class_':'form-control fw-bold'})
        #return render_template('/user/department.html', form=userdepartmentform)
    if request.method == 'POST':
        uform = UserFacultyForm(request.form)
        if uform.validate_on_submit():
            if hasattr(user, 'objects') == True:
                try:
                    ######## faculty ##############
                    fac = user.faculty.get(pk = id1)
                    fac.position = uform.position.data
                    fac.post = uform.post.data
                    fac.empcode = uform.empcode.data
                    
                    user.save()
                    return redirect(request.form.get('next'))
                except DoesNotExist as e:
                    flash(id1 + ' Doest Not Exist')
                    return render_template_string(errormessages,messages= id1 + ' Doest Not Exist')
                except ValidationError as e:
                    flash(e.message)
                    flash(e.field_name)
                    flash(e.errors)
                    return render_template_string(errormessages,messages=e.message)

@users.route('/facultydelete/<id>/<id1>', methods=['GET'])  # username
@login_required
def facultydelete(id,id1):
    user = User.objects(id=id).first()
    if request.method == 'GET':
        try:
            dep = user.faculty.get(pk=id1)
            user.faculty.remove(dep)
            user.save()
            return redirect('/faculty')
            #return redirect(request.form.get('next'))
        except DoesNotExist as e:
            flash(id1 + ' Doest Not Exist')
            return render_template_string(errormessages,messages= id1 + ' Doest Not Exist')
        except ValidationError as e:
            flash(e.message)
            flash(e.field_name)
            flash(e.errors)
            return render_template_string(errormessages,messages=e.message)     



#####################################################################  student  #############################################################################
stu_view = """
    {% extends "base.html" %} {% block content %}
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
    <input type="hidden" name="next" value={{back}} />
    <a href="{{url_for(fn_create, id = usrid )}}">(New Roll Number)</a>
        {% for lst in student %}
            <div class="{{ kwargs.pop('class_', '') }}">
                <a href="{{url_for(fn_edit, id = usrid, id1 = lst.pk )}}">(Edit)</a>
                <a href="{{url_for(fn_delete, id = usrid, id1 = lst.pk )}}">(Delete)</a>
                <h3>Student Roll Number : {{lst.rollnumber}}</h3>
                <h3>University Programe: {{lst.programe}}</h3>
                <h3>Admission Year : {{lst.year}}</h3>
                <h3>Branch : {{lst.branch}}</h3>
            </div>
        {% endfor %}
    {% endblock %}
    """

@users.route('/student', methods=['GET', 'POST'])  # username
@login_required
def student():
    #user = User.objects(username=current_user.username).first()
    tid = session["target_id"]
    user = User.objects(id=tid).first()
    if request.method == 'GET':
        if hasattr(user, 'objects') == True:
            return render_template_string(stu_view #, fn_target='users.department' ## uform=FlaskForm()
                                      ,fn_create = 'users.studentcreate', fn_edit = 'users.studentedit' , fn_delete = 'users.studentdelete'
                                      #,fn_targetaddcreate = 'users.addcreatel2', fn_targetaddedit = 'users.addeditl2' , fn_targetadddelete = 'users.adddeletel2'
                                      #,fn_targetsmcreate = 'users.addsmcreatel2',fn_targetsmedit = 'users.addsmeditl2', fn_targetsmdelete = 'users.addsmdeletel2'
                                      ,back = request.referrer
                                      ,student = user.student, usrid = user.id
                                      ,kwargs = {'class_':'form-control fw-bold'})
            #return render_template_string(details_dict_view,userdict=user.student.student_dict(),tablehead='Stuent Details',tableheadrvalue='Information',fn_target='users.studentedit')

@users.route('/studentcreate/<id>', methods=['GET', 'POST'])  # username
@login_required
def studentcreate(id):
    #id = session["target_id"]
    user = User.objects(id=id).first()
    if request.method == 'GET':
        uform = UserStudentForm()
        if hasattr(user, 'objects') == True:
             return render_template_string(edit_create_view_id, form=uform, fn_target='users.studentcreate'
                                      , id=id, id1=None, id2=None, id3=None
                                      , back = request.referrer
                                      , kwargs = {'class_':'form-control fw-bold'})
    if request.method == 'POST':
        uform = UserStudentForm(request.form)
        if uform.validate_on_submit():
            ######## industrycollaboration #############
            if hasattr(user, 'objects') == True:
                try:
                    # check for duplicate department entart
                    #print(user.university.filter(name = uform.name.data).count())
                    if user.student.filter(programe = uform.programe.data
                                           ,year = uform.year.data
                                           ,branch = uform.branch.data
                                           ,rollnumber = uform.rollnumber.data).count() > 0:
                        return render_template_string("""
                                    {% extends "base.html" %} {% block content %}
                                        <h3>Stdent {{roll}} is in studet List </h3>
                                    {% endblock %}
                                        """,roll= uform.programe.data + uform.year.data + uform.branch.data + uform.rollnumber.data)
                    
                    p = Student( pk = get_a_uuid()
                                ,programe = uform.programe.data
                                ,year = uform.year.data
                                ,branch = uform.branch.data
                                ,rollnumber = uform.rollnumber.data
                                )
                    user.student.append(p)
                    user.save()
                    return redirect(request.form.get('next'))
                except ValidationError as e:
                    flash(e.message)
                    flash(e.field_name)
                    flash(e.errors)
                    return render_template_string(errormessages,messages=e.message)

@users.route('/studentedit/<id>/<id1>', methods=['GET', 'POST'])  # username
@login_required
def studentedit(id,id1):
    #user = User.objects(username=current_user.username).first()
    #id = session["target_id"]
    user = User.objects(id=id).first()
    if request.method == 'GET':
        uform = UserStudentForm()
        if hasattr(user, 'objects') == True:
            ######## student ##############
            stu = user.student.get(pk = id1)
            uform.programe.data = stu.programe
            uform.year.data = stu.year
            uform.branch.data = stu.branch
            uform.rollnumber.data = stu.rollnumber
            
            return render_template_string(edit_create_view_id, form=uform, fn_target='users.studentedit'
                                      , id=id, id1=id1, id2=None, id3=None
                                      , back = request.referrer
                                      , kwargs = {'class_':'form-control fw-bold'})
        #return render_template('/user/department.html', form=userdepartmentform)
    if request.method == 'POST':
        uform = UserStudentForm(request.form)
        if uform.validate_on_submit():
            if hasattr(user, 'objects') == True:
                try:
                    ######## student ##############
                    stu = user.student.get(pk = id1)
                    stu.programe = uform.programe.data
                    stu.year = uform.year.data
                    stu.branch = uform.branch.data
                    stu.rollnumber = uform.rollnumber.data
                    
                    user.save()
                    return redirect(request.form.get('next'))
                except DoesNotExist as e:
                    flash(id1 + ' Doest Not Exist')
                    return render_template_string(errormessages,messages= id1 + ' Doest Not Exist')
                except ValidationError as e:
                    flash(e.message)
                    flash(e.field_name)
                    flash(e.errors)
                    return render_template_string(errormessages,messages=e.message)

@users.route('/studentdelete/<id>/<id1>', methods=['GET'])  # username
@login_required
def studentdelete(id,id1):
    user = User.objects(id=id).first()
    if request.method == 'GET':
        try:
            dep = user.student.get(pk=id1)
            user.student.remove(dep)
            user.save()
            return redirect('/student')
            #return redirect(request.form.get('next'))
        except DoesNotExist as e:
            flash(id1 + ' Doest Not Exist')
            return render_template_string(errormessages,messages= id1 + ' Doest Not Exist')
        except ValidationError as e:
            flash(e.message)
            flash(e.field_name)
            flash(e.errors)
            return render_template_string(errormessages,messages=e.message)     
###################################################################################################################
#####################################################################  university  #############################################################################
uni_view = """
    {% from 'form_macros.html' import render_addl2 %}
    {% extends "base.html" %} {% block content %}
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
    <input type="hidden" name="next" value={{back}} />
    <a href={{university.url}}><h1>{{university.name}}</h1></a>
    <a href="{{url_for(fn_create, id = usrid )}}">(New University)</a></br>
        {% for lst in university %}
            <a href={{lst.url}}><h1>{{lst.name}}</h1></a>
            <a href="{{url_for(fn_edit, id = usrid, id1 = lst.pk )}}">(Edit)</a>
            <a href="{{url_for(fn_delete, id = usrid, id1 = lst.pk )}}">(Delete)</a>
            <a href="{{url_for(fn_targetaddcreate, id = usrid, id1 = 'university', id2 = lst.pk, id3 = 'office' )}}">(create new University Address)</a></br>
            {{render_addl2(lst.office, usrid, 'university', lst.pk, 'office', kwargs)}}
        {% endfor %}
    {% endblock %}
    """

@users.route('/university', methods=['GET', 'POST'])  # username
@login_required
def university():
    #user = User.objects(username=current_user.username).first()
    tid = session["target_id"]
    user = User.objects(id=tid).first()
    if request.method == 'GET':
        if hasattr(user, 'objects') == True:
            return render_template_string(uni_view #, fn_target='users.department' ## uform=FlaskForm()
                                      ,fn_create = 'users.universitycreate', fn_edit = 'users.universityedit' , fn_delete = 'users.universitydelete'
                                      ,fn_targetaddcreate = 'users.addcreatel2', fn_targetaddedit = 'users.addeditl2' , fn_targetadddelete = 'users.adddeletel2'
                                      ,fn_targetsmcreate = 'users.addsmcreatel2',fn_targetsmedit = 'users.addsmeditl2', fn_targetsmdelete = 'users.addsmdeletel2'
                                      ,back = request.referrer
                                      ,university = user.university, usrid = user.id
                                      ,kwargs = {'class_':'form-control fw-bold'})
            # return render_template_string(uni_view #, fn_target='users.contactsadd' ## uform=FlaskForm()
            #                           ,fn_targetaddedit = 'users.universityedit'#,fn_targetaddcreate = 'users.contactsaddcreate', fn_targetadddelete = 'users.contactsadddelete'
            #                           ,fn_targetsmedit = 'users.universityaddsmedit',fn_targetsmcreate = 'users.universityaddsmcreate', fn_targetsmdelete = 'users.universityaddsmdelate'
            #                           ,back = request.referrer
            #                           ,university = user.university, usrid = user.id)

@users.route('/universitycreate/<id>', methods=['GET', 'POST'])  # username
@login_required
def universitycreate(id):
    #id = session["target_id"]
    user = User.objects(id=id).first()
    if request.method == 'GET':
        uform = UserUniversityForm()
        if hasattr(user, 'objects') == True:
             return render_template_string(edit_create_view_id, form=uform, fn_target='users.universitycreate'
                                      , id=id, id1=None, id2=None, id3=None
                                      , back = request.referrer
                                      , kwargs = {'class_':'form-control fw-bold'})
    if request.method == 'POST':
        uform = UserUniversityForm(request.form)
        if uform.validate_on_submit():
            ########  #############
            if hasattr(user, 'objects') == True:
                try:
                    # check for duplicate department entart
                    #print(user.university.filter(name = uform.name.data).count())
                    if user.university.filter(name = uform.name.data).count() > 0:
                        return render_template_string("""
                                    {% extends "base.html" %} {% block content %}
                                        <h3>University {{name}} is in university List </h3>
                                    {% endblock %}
                                        """,name=uform.name.data)
                    
                    p = University( pk = get_a_uuid()
                                ,name=uform.name.data
                                ,url=uform.url.data
                                        )
                    user.university.append(p)
                    user.save()
                    return redirect(request.form.get('next'))
                except ValidationError as e:
                    flash(e.message)
                    flash(e.field_name)
                    flash(e.errors)
                    return render_template_string(errormessages,messages=e.message)

@users.route('/universityedit/<id>/<id1>', methods=['GET', 'POST'])  # username
@login_required
def universityedit(id,id1):
    #user = User.objects(username=current_user.username).first()
    #id = session["target_id"]
    user = User.objects(id=id).first()
    if request.method == 'GET':
        uform = UserUniversityForm()
        if hasattr(user, 'objects') == True:
            ######## department ##############
            uni = user.university.get(pk = id1)
            uform.name.data = uni.name
            uform.url.data = uni.url
            
            return render_template_string(edit_create_view_id, form=uform, fn_target='users.universityedit'
                                      , id=id, id1=id1, id2=None, id3=None
                                      , back = request.referrer
                                      , kwargs = {'class_':'form-control fw-bold'})
        #return render_template('/user/department.html', form=userdepartmentform)
    if request.method == 'POST':
        uform = UserUniversityForm(request.form)
        if uform.validate_on_submit():
            ######## department #############
            if hasattr(user, 'objects') == True:
                try:
                    ######## department ##############
                    uni = user.university.get(pk = id1)
                    uni.name = uform.name.data
                    uni.url = uform.url.data
                    ######## office address #############
                    # user.department.office.addtype = uform.office.data['addtype']
                    # user.department.office.add = uform.office.data['add']
                    # user.department.office.state = uform.office.data['state']
                    # user.department.office.pin = uform.office.data['pin']
                    # user.department.office.countary = uform.office.data['countary']
                    # user.department.office.phone = uform.office.data['phone']
                    # user.department.office.land = uform.office.data['land']
                    # user.department.office.email = uform.office.data['email']
                    user.save()
                    return redirect(request.form.get('next'))
                except DoesNotExist as e:
                    flash(id1 + ' Doest Not Exist')
                    return render_template_string(errormessages,messages= id1 + ' Doest Not Exist')
                except ValidationError as e:
                    flash(e.message)
                    flash(e.field_name)
                    flash(e.errors)
                    return render_template_string(errormessages,messages=e.message)

@users.route('/universitydelete/<id>/<id1>', methods=['GET'])  # username
@login_required
def universitydelete(id,id1):
    user = User.objects(id=id).first()
    if request.method == 'GET':
        try:
            dep = user.university.get(pk=id1)
            user.university.remove(dep)
            user.save()
            return redirect('/university')
            #return redirect(request.form.get('next'))
        except DoesNotExist as e:
            flash(id1 + ' Doest Not Exist')
            return render_template_string(errormessages,messages= id1 + ' Doest Not Exist')
        except ValidationError as e:
            flash(e.message)
            flash(e.field_name)
            flash(e.errors)
            return render_template_string(errormessages,messages=e.message)     

#################### University Social Media Address
# @users.route('/universityaddsmedit/<id>/<id1>', methods=['GET', 'POST'])  # target_id/addtype/smdesc
# @login_required
# def universityaddsmedit(id,id1):
#     if request.method == 'GET':
#         #print(request.referrer)
#         uform = SocialMediaAddressForm()
#         usr = User.objects(id=id).first() # Target user id
#         uni = getattr(usr,'university')
#         #print(uni.office.email)
#         dl = usr.university.office.sm.get(desc = str(id1))
#         uform.desc.data = dl.desc
#         uform.link.data = dl.link
#         return render_template_string(edit_create_view_id, form=uform, fn_target='users.universityaddsmedit'
#                                       , id=id, id1=id1, id2=None, id3=None
#                                       , back = request.referrer
#                                       , kwargs = {'class_':'form-control fw-bold'})
#     if request.method == 'POST':
#         uform = SocialMediaAddressForm(request.form)
#         if uform.validate_on_submit():
#             try:
#                 uid = ObjectId(id)#session["target_id"]
#                 usr = User.objects(id=uid).first() # Target user id
                
#                 #check duplicate Social Media Address
#                 if str(id1) != uform.desc.data:
#                     ad = usr.university.office
#                     for s in ad.sm:
#                         if s.desc == uform.desc.data:
#                             return render_template_string("""
#                                 {% extends "base.html" %} {% block content %}
#                                     <h3>University Social Media Addres {{keyword}} is in list </h3>
#                                 {% endblock %}
#                                     """,keyword=uform.desc.data)
#                 else:
#                     usr.university.office.sm.get(desc = id1).desc = uform.desc.data
#                     usr.university.office.sm.get(desc = id1).link = uform.link.data
#                     usr.save()
#                     return redirect(request.form.get('next'))
#             except ValidationError as e:
#                 flash(e.message)
#                 flash(e.field_name)
#                 flash(e.errors)
#                 return render_template_string(errormessages,messages=e.message)


# @users.route('/universityaddsmdelete/<id>/<id1>', methods=['GET', 'POST'])  # target_id/addtype
# @login_required
# def universityaddsmdelate(id,id1):
#     if request.method == 'GET':
#         try:
#             #print(request.referrer)
#             #uform = SocialMediaAddressForm()
#             usr = User.objects(id=id).first() # Target user id
#             ad = usr.university.office
#             for s in ad.sm:
#                 if s.desc == str(id1):
#                     ad.sm.remove(s)
#             usr.save()
#             return redirect(request.form.get('next'))
#         except ValidationError as e:
#             flash(e.message)
#             flash(e.field_name)
#             flash(e.errors)
#             return render_template_string(errormessages,messages=e.message)


# @users.route('/universityaddsmcreate/<id>', methods=['GET', 'POST'])  # target_id/addtype
# @login_required
# def universityaddsmcreate(id):
    if request.method == 'GET':
        #print(request.referrer)
        uform = SocialMediaAddressForm()
        #usr = User.objects(id=id).first() # Target user id
        #ad = usr.contacts.get(addtype = id1)
        
        return render_template_string(edit_create_view_id, form=uform, fn_target='users.universityaddsmcreate'
                                      , id=id, id1=None, id2=None, id3=None
                                      , back = request.referrer
                                      , kwargs = {'class_':'form-control fw-bold'})
    if request.method == 'POST':
        uform = SocialMediaAddressForm(request.form)
        if uform.validate_on_submit():
            try:
                uid = ObjectId(id)#session["target_id"]
                usr = User.objects(id=uid).first() # Target user id
                ad = usr.university.office
                #check duplicate Social Media Address
                for s in ad.sm:
                    if s.desc == uform.desc.data:
                        return render_template_string("""
                            {% extends "base.html" %} {% block content %}
                                <h3>University Social Media Addres {{keyword}} is in list </h3>
                            {% endblock %}
                                """,keyword=uform.desc.data)
                ad.sm.append(LinkDesc(desc=uform.desc.data,link=uform.link.data))
                usr.save()
                return redirect(request.form.get('next'))
            except ValidationError as e:
                flash(e.message)
                flash(e.field_name)
                flash(e.errors)
                return render_template_string(errormessages,messages=e.message)



#########################################################################################################
#####################################################################  department  ########################
dep_view = """
    {% from 'form_macros.html' import render_addl2 %}
    {% extends "base.html" %} {% block content %}
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
    <input type="hidden" name="next" value={{back}} />
    <a href="{{url_for(fn_create, id = usrid )}}">(New Department)</a>
        {% for dept in department %}
            <a href={{dept.url}}><h1>{{dept.name}}</h1></a>
            <a href="{{url_for(fn_edit, id = usrid, id1 = dept.pk )}}">(Edit)</a>
            <a href="{{url_for(fn_delete, id = usrid, id1 = dept.pk )}}">(Delete)</a>
            <a href="{{url_for(fn_targetaddcreate, id = usrid, id1 = 'department', id2 = dept.pk, id3 = 'office' )}}">(create new Department Address)</a></br>
            {{render_addl2(dept.office, usrid, 'department', dept.pk, 'office', kwargs)}}
        {% endfor %}
    {% endblock %}
    """
@users.route('/department', methods=['GET', 'POST'])  # username
@login_required
def department():
    #user = User.objects(username=current_user.username).first()
    tid = session["target_id"]
    user = User.objects(id=tid).first()
    if request.method == 'GET':
        if hasattr(user, 'objects') == True:
            # return render_template('department.html' #, fn_target='users.department' ## uform=FlaskForm()
            #                           ,fn_create = 'users.departmentcreate', fn_edit = 'users.departmentedit' , fn_delete = 'users.departmentdelete'
            #                           ,fn_targetaddcreate = 'users.addcreatel2', fn_targetaddedit = 'users.addeditl2' , fn_targetadddelete = 'users.adddeletel2'
            #                           ,fn_targetsmcreate = 'users.addsmcreatel2',fn_targetsmedit = 'users.addsmeditl2', fn_targetsmdelete = 'users.addsmdeletel2'
            #                           ,back = request.referrer
            #                           ,department = user.department, usrid = user.id)
            return render_template_string(dep_view #, fn_target='users.department' ## uform=FlaskForm()
                                      ,fn_create = 'users.departmentcreate', fn_edit = 'users.departmentedit' , fn_delete = 'users.departmentdelete'
                                      ,fn_targetaddcreate = 'users.addcreatel2', fn_targetaddedit = 'users.addeditl2' , fn_targetadddelete = 'users.adddeletel2'
                                      ,fn_targetsmcreate = 'users.addsmcreatel2',fn_targetsmedit = 'users.addsmeditl2', fn_targetsmdelete = 'users.addsmdeletel2'
                                      ,back = request.referrer
                                      ,department = user.department, usrid = user.id
                                      ,kwargs = {'class_':'form-control fw-bold'})
            #return render_template_string(details_dict_view,userdict=user.department.department_dict(),tablehead='Department Details',tableheadrvalue='Information',fn_target='users.departmentedit')

@users.route('/departmentcreate/<id>', methods=['GET', 'POST'])  # username
@login_required
def departmentcreate(id):
    #id = session["target_id"]
    user = User.objects(id=id).first()
    if request.method == 'GET':
        uform = UserDepartmentForm()
        if hasattr(user, 'objects') == True:
             return render_template_string(edit_create_view_id, form=uform, fn_target='users.departmentcreate'
                                      , id=id, id1=None, id2=None, id3=None, id4=None, id5=None
                                      , back = request.referrer
                                      , kwargs = {'class_':'form-control fw-bold'})
    if request.method == 'POST':
        uform = UserDepartmentForm(request.form)
        if uform.validate_on_submit():
            ######## industrycollaboration #############
            if hasattr(user, 'objects') == True:
                try:
                    # check for duplicate department entart
                    #print(user.department.filter(name = uform.name.data).count())
                    if user.department.filter(name = uform.name.data).count() > 0:
                        return render_template_string("""
                                    {% extends "base.html" %} {% block content %}
                                        <h3>Department {{name}} is in Department List </h3>
                                    {% endblock %}
                                        """,name=uform.name.data)
                    # off = Add(
                    #     addtype = uform.office.data['addtype']
                    #     ,add = uform.office.data['add']
                    #     ,state = uform.office.data['state']
                    #     ,pin = uform.office.data['pin']
                    #     ,countary = uform.office.data['countary']
                    #     ,phone = uform.office.data['phone']
                    #     ,land = uform.office.data['land']
                    #     ,email = uform.office.data['email']
                    # )
                    p = Department( pk = get_a_uuid()
                                ,name=uform.name.data
                                ,url=uform.url.data
                                        )
                    user.department.append(p)
                    user.save()
                    return redirect(request.form.get('next'))
                except ValidationError as e:
                    flash(e.message)
                    flash(e.field_name)
                    flash(e.errors)
                    return render_template_string(errormessages,messages=e.message)
                

@users.route('/departmentedit/<id>/<id1>', methods=['GET', 'POST'])  # username
@login_required
def departmentedit(id,id1):
    #user = User.objects(username=current_user.username).first()
    #id = session["target_id"]
    user = User.objects(id=id).first()
    if request.method == 'GET':
        uform = UserDepartmentForm()
        if hasattr(user, 'objects') == True:
            ######## department ##############
            dept = user.department.get(pk = id1)
            uform.name.data = dept.name
            uform.url.data = dept.url
            
            return render_template_string(edit_create_view_id, form=uform, fn_target='users.departmentedit'
                                      , id=id, id1=id1, id2=None, id3=None, id4=None, id5=None
                                      , back = request.referrer
                                      , kwargs = {'class_':'form-control fw-bold'})
        #return render_template('/user/department.html', form=userdepartmentform)
    if request.method == 'POST':
        uform = UserDepartmentForm(request.form)
        if uform.validate_on_submit():
            ######## department #############
            if hasattr(user, 'objects') == True:
                try:
                    ######## department ##############
                    dept = user.department.get(pk = id1)
                    dept.name = uform.name.data
                    dept.url = uform.url.data
                    ######## office address #############
                    # user.department.office.addtype = uform.office.data['addtype']
                    # user.department.office.add = uform.office.data['add']
                    # user.department.office.state = uform.office.data['state']
                    # user.department.office.pin = uform.office.data['pin']
                    # user.department.office.countary = uform.office.data['countary']
                    # user.department.office.phone = uform.office.data['phone']
                    # user.department.office.land = uform.office.data['land']
                    # user.department.office.email = uform.office.data['email']
                    user.save()
                    return redirect(request.form.get('next'))
                except DoesNotExist as e:
                    flash(id1 + ' Doest Not Exist')
                    return render_template_string(errormessages,messages= id1 + ' Doest Not Exist')
                except ValidationError as e:
                    flash(e.message)
                    flash(e.field_name)
                    flash(e.errors)
                    return render_template_string(errormessages,messages=e.message)
            # print(jsonify(user).get_json())
        #return render_template('/user/department.html', form=userdepartmentform)
        #return render_template_string(details_dict_view,userdict=user.department.department_dict(),tablehead='Department Details',tableheadrvalue='Information',fn_target='users.departmentedit')
        #return render_template_string(edit_create_view_key_str,form=userdepartmentform,fn_target='users.departmentedit')

@users.route('/departmentdelete/<id>/<id1>', methods=['GET'])  # username
@login_required
def departmentdelete(id,id1):
    user = User.objects(id=id).first()
    if request.method == 'GET':
        try:
            dep = user.department.get(pk=id1)
            user.department.remove(dep)
            user.save()
            return redirect('/department')
            #return redirect(request.form.get('next'))
        except DoesNotExist as e:
            flash(id1 + ' Doest Not Exist')
            return render_template_string(errormessages,messages= id1 + ' Doest Not Exist')
        except ValidationError as e:
            flash(e.message)
            flash(e.field_name)
            flash(e.errors)
            return render_template_string(errormessages,messages=e.message)
        
#################### Department Social Media Address
# @users.route('/departmentaddsmedit/<id>/<id1>', methods=['GET', 'POST'])  # target_id/addtype/smdesc
# @login_required
# def departmentaddsmedit(id,id1):
#     if request.method == 'GET':
#         #print(request.referrer)
#         uform = SocialMediaAddressForm()
#         usr = User.objects(id=id).first() # Target user id
#         # dep = getattr(usr,'department')
#         # print(dep)
#         dl = usr.university.office.sm.get(desc = str(id1))
#         uform.desc.data = dl.desc
#         uform.link.data = dl.link
#         return render_template_string(edit_create_view_id, form=uform, fn_target='users.universityaddsmedit'
#                                       , id=id, id1=id1, id2=None, id3=None
#                                       , back = request.referrer
#                                       , kwargs = {'class_':'form-control fw-bold'})
#     if request.method == 'POST':
#         uform = SocialMediaAddressForm(request.form)
#         if uform.validate_on_submit():
#             try:
#                 uid = ObjectId(id)#session["target_id"]
#                 usr = User.objects(id=uid).first() # Target user id
                
#                 #check duplicate Social Media Address
#                 if str(id1) != uform.desc.data:
#                     ad = usr.university.office
#                     for s in ad.sm:
#                         if s.desc == uform.desc.data:
#                             return render_template_string("""
#                                 {% extends "base.html" %} {% block content %}
#                                     <h3>University Social Media Addres {{keyword}} is in list </h3>
#                                 {% endblock %}
#                                     """,keyword=uform.desc.data)
#                 else:
#                     usr.university.office.sm.get(desc = id1).desc = uform.desc.data
#                     usr.university.office.sm.get(desc = id1).link = uform.link.data
#                     usr.save()
#                     return redirect(request.form.get('next'))
#             except ValidationError as e:
#                 flash(e.message)
#                 flash(e.field_name)
#                 flash(e.errors)
#                 return render_template_string(errormessages,messages=e.message)


# @users.route('/departmentaddsmdelete/<id>/<id1>', methods=['GET', 'POST'])  # target_id/addtype
# @login_required
# def departmentaddsmdelate(id,id1):
#     if request.method == 'GET':
#         try:
#             #print(request.referrer)
#             #uform = SocialMediaAddressForm()
#             usr = User.objects(id=id).first() # Target user id
#             ad = usr.university.office
#             for s in ad.sm:
#                 if s.desc == str(id1):
#                     ad.sm.remove(s)
#             usr.save()
#             return redirect(request.form.get('next'))
#         except ValidationError as e:
#             flash(e.message)
#             flash(e.field_name)
#             flash(e.errors)
#             return render_template_string(errormessages,messages=e.message)


# @users.route('/departmentaddsmcreate/<id>', methods=['GET', 'POST'])  # target_id/addtype
# @login_required
# def departmentaddsmcreate(id):
    if request.method == 'GET':
        #print(request.referrer)
        uform = SocialMediaAddressForm()
        #usr = User.objects(id=id).first() # Target user id
        #ad = usr.contacts.get(addtype = id1)
        
        return render_template_string(edit_create_view_id, form=uform, fn_target='users.universityaddsmcreate'
                                      , id=id, id1=None, id2=None, id3=None
                                      , back = request.referrer
                                      , kwargs = {'class_':'form-control fw-bold'})
    if request.method == 'POST':
        uform = SocialMediaAddressForm(request.form)
        if uform.validate_on_submit():
            try:
                uid = ObjectId(id)#session["target_id"]
                usr = User.objects(id=uid).first() # Target user id
                ad = usr.university.office
                #check duplicate Social Media Address
                for s in ad.sm:
                    if s.desc == uform.desc.data:
                        return render_template_string("""
                            {% extends "base.html" %} {% block content %}
                                <h3>University Social Media Addres {{keyword}} is in list </h3>
                            {% endblock %}
                                """,keyword=uform.desc.data)
                ad.sm.append(LinkDesc(desc=uform.desc.data,link=uform.link.data))
                usr.save()
                return redirect(request.form.get('next'))
            except ValidationError as e:
                flash(e.message)
                flash(e.field_name)
                flash(e.errors)
                return render_template_string(errormessages,messages=e.message)



####################################################################################################################
# dict to html table
details_dict_listview = """"  
    {% extends "base.html" %} {% block content %}
        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
        <input type="hidden" name="next" value={{back}} />
        <table>
            <thead>
                <tr>
                <th>{{tablehead}}</th>
                <th>{{tableheadrvalue}} (<a href="{{url_for(fn_target_new, id = id)}}">New</a>) </th>
                </tr>
            </thead>
            <tbody>
                {% set ns = namespace(i=0) %}
                {% for dict_item in detailitemslist  %}
                    {% set ns.i = ns.i + 1 %}
                    {% for key, value in dict_item.items() %}
                        {% if key == 'pk' %}
                            <tr>
                                <td> {{ ns.i }} </td>
                                <td> (<a href="{{url_for(fn_target_edit, id = id, id1 = value)}}">Edit</a>)
                                    (<button type="button" class="btn btn-info btn-sm" data-bs-toggle="modal" data-bs-target="#delete{{value}}">Delete</button>) 
                                </td>
                            </tr>
                        {% else %}
                            <tr>
                                <td> {{ key }} </td>
                                <td> {{ value }} </td>
                            </tr>
                        {% endif %}
                    {% endfor %}
                {% endfor %}
            </tbody>
        </table>
        {% for dict_item in detailitemslist  %}
            {% for key, value in dict_item.items() %}
                {% if key == 'pk' %}
                    <div class="modal fade" id="delete{{value}}" tabindex="-1" aria-labelledby="deletelabel" aria-hidden="true" role="dialog">
                        <div class="modal-dialog modal-dialog-centered">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title" id="deletelabel">Alert</h5>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                </div>
                                <div class="modal-body">
                                    <form action="{{ url_for(fn_target_delete, id = id, id1 = value) }}" method="POST">
                                        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
                                        <div class="form-group">
                                            <div>
                                                <button type="submit" class="btn btn-success">
                                                    Delete
                                                </button>
                                            </div>
                                        </div>
                                    </form>
                                </div>
                                <div class="mb-3">
                                    <div class="modal-footer">
                                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                                            Close
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                {% endif %}
            {% endfor %}
        {% endfor %}
    {% endblock %}
"""
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
                                        <a href="{{url_for('users.sponsoredprojectsedit', pk = item.title)}}" >Edit</a>
                                        <a href="{{url_for('users.sponsoredprojectsdelete', pk = item.title)}}" >Delete</a>
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
    #user = User.objects(username=current_user.username).first()
    id = session["target_id"]
    user = User.objects(id=id).first()
    if request.method == 'GET':
        if hasattr(user, 'objects') == True:
            ######## IndustryCollaboration ##############
            details_dict_view_list = []
            for p in user.sponsoredprojects:
                details_dict_view_list.append(p.__dict__())
            #print(details_dict_view_list)
            return render_template_string(details_dict_listview
                                          , fn_target_new = 'users.sponsoredprojectscreate', fn_target_edit = 'users.sponsoredprojectsedit', fn_target_delete = 'users.sponsoredprojectsdelete' 
                                          , back = request.referrer
                                          , id = user.id, detailitemslist = details_dict_view_list, tablehead = 'Sponsored Project', tableheadrvalue = 'Information'
                                          , kwargs = {'class_':'form-control fw-bold'})

@users.route('/sponsoredprojectscreate/<id>', methods=['GET', 'POST'])  # create
@login_required
def sponsoredprojectscreate(id):
    #user = User.objects(username=current_user.username).first()
    #id = session["target_id"]
    user = User.objects(id=id).first()
    if request.method == 'GET':
        uform = UserSponsoredProjectsForm()
        if hasattr(user, 'objects') == True:
            return render_template_string(edit_create_view_id, form=uform, fn_target='users.sponsoredprojectscreate'
                                          , id=id, id1=None, id2=None, id3=None, id4=None, id5=None 
                                          , back = request.referrer
                                          , kwargs = {'class_':'form-control fw-bold'})
    if request.method == 'POST':
        uform = UserSponsoredProjectsForm(request.form)
        if uform.validate_on_submit():
            ######## sponsoredproject #############
            if hasattr(user, 'objects') == True:
                try:
                    if user.sponsoredprojects.filter(name=uform.name.data
                                        , duration=uform.duration.data
                                        , title=uform.title.data
                                        ).count() > 0:
                        return render_template_string("""
                                    {% extends "base.html" %} {% block content %}
                                        <h3>SponsoredProject {{name}} is in SponsoredProject List </h3>
                                    {% endblock %}
                                        """,name=uform.name.data)
                    p = SponsoredProjects(pk = get_a_uuid()
                                        , name=uform.name.data
                                        , duration=uform.duration.data
                                        , amount=uform.amount.data
                                        , title=uform.title.data
                                        )
                    user.sponsoredprojects.append(p)
                    user.save()
                    return redirect(request.form.get('next'))
                except DoesNotExist as e:
                    flash(id + ' Doest Not Exist')
                    return render_template_string(errormessages,messages= id + ' Doest Not Exist')
                except ValidationError as e:
                    flash(e.message)
                    flash(e.field_name)
                    flash(e.errors)
                    return render_template_string(errormessages,messages=e.message)
                
@users.route('/sponsoredprojectsedit/<id>/<id1>', methods=['GET', 'POST'])
@login_required
def sponsoredprojectsedit(id,id1):
    #user = User.objects(username=current_user.username).first()
    #tid = session["target_id"]
    user = User.objects(id=id).first()
    if request.method == 'GET':
        uform = UserSponsoredProjectsForm()
        if hasattr(user, 'objects') == True:
            ######## sponsoredprojects ##############
            p = user.sponsoredprojects.get(pk = id1)
            uform.title.data = p.title
            uform.name.data = p.name
            uform.duration.data = p.duration
            uform.amount.data = p.amount
        return render_template_string(edit_create_view_id, form=uform, fn_target='users.sponsoredprojectsedit'
                                    , id=id, id1=id1, id2=None, id3=None, id4=None, id5=None 
                                    , back = request.referrer
                                    , kwargs = {'class_':'form-control fw-bold'})
        # return render_template('/user/sponsoredprojects.html', form=usersponsoredprojectsform)
    if request.method == 'POST':
        uform = UserSponsoredProjectsForm(request.form)
        if uform.validate_on_submit():
            ######## sponsoredprojects #############
            if hasattr(user, 'objects') == True:
                try:
                    if user.sponsoredprojects.filter(name=uform.name.data
                                        , duration=uform.duration.data
                                        , title=uform.title.data
                                        ).count() > 0:
                        return render_template_string("""
                                    {% extends "base.html" %} {% block content %}
                                        <h3>SponsoredProject {{name}} is in SponsoredProject List </h3>
                                    {% endblock %}
                                        """,name=uform.name.data)
                    
                    p = user.sponsoredprojects.get(pk = id1)
                    p.title = uform.title.data
                    p.name = uform.name.data
                    p.duration = uform.duration.data
                    p.amount = uform.amount.data
                    user.save()
                    return redirect(request.form.get('next'))
                except DoesNotExist as e:
                    flash(id + ' Doest Not Exist')
                    return render_template_string(errormessages)
                except ValidationError as e:
                    flash(e.message)
                    flash(e.field_name)
                    flash(e.errors)
                    return render_template_string(errormessages)
                        #print('Contact Saved')
                # print(jsonify(user).get_json())
                
                
@users.route('/sponsoredprojectsdelete/<id>/<id1>', methods=['POST'])  # delete
@login_required
def sponsoredprojectsdelete(id,id1):
    #user = User.objects(username=current_user.username).first()
    #tid = session["target_id"]
    
    if request.method == 'POST':
        user = User.objects(id=id).first()
        if hasattr(user, 'objects') == True:
            try:
                    p = user.sponsoredprojects.get(pk = id1) 
                    user.sponsoredprojects.remove(p)
                    user.save()
                    return redirect('/sponsoredprojects')

            except DoesNotExist as e:
                flash(id + ' Doest Not Exist')
                return render_template_string(errormessages,messages= id + ' Doest Not Exist')
            except ValidationError as e:
                flash(e.message)
                flash(e.field_name)
                flash(e.errors)
                return render_template_string(errormessages,messages=e.message)
                

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
                                        <a href="{{url_for('users.patentsedit', pk = item.title)}}" >Edit</a>
                                        <a href="{{url_for('users.patentsdelete', pk = item.title)}}" >Delete</a>
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
    #user = User.objects(username=current_user.username).first()
    tid = session["target_id"]
    user = User.objects(id=tid).first()
    if request.method == 'GET':
        if hasattr(user, 'objects') == True:
            ######## IndustryCollaboration ##############
            details_dict_view_list = []
            for p in user.patents:
                details_dict_view_list.append(p.__dict__())
            #print(details_dict_view_list)
            return render_template_string(details_dict_listview, fn_target_new = 'users.patentscreate', fn_target_edit = 'users.patentsedit', fn_target_delete = 'users.patentsdelete'
                                          , back = request.referrer
                                          , id = user.id, detailitemslist=details_dict_view_list, tablehead = 'Patents', tableheadrvalue = 'Information'
                                          , kwargs = {'class_':'form-control fw-bold'})
            #return render_template_string(patents_view, patents=user.patents)

@users.route('/patentscreate/<id>', methods=['GET', 'POST'])  # create
@login_required
def patentscreate(id):
    #user = User.objects(username=current_user.username).first()
    #tid = session["target_id"]
    user = User.objects(id=id).first()
    if request.method == 'GET':
        uform = UserPatentsForm()
        if hasattr(user, 'objects') == True:
            return render_template_string(edit_create_view_id, form=uform, fn_target='users.patentscreate'
                                          , id=id, id1=None, id2=None, id3=None, id4=None, id5=None 
                                          , back = request.referrer
                                          , kwargs = {'class_':'form-control fw-bold'})
    if request.method == 'POST':
        uform = UserPatentsForm(request.form)
        if uform.validate_on_submit():
            ######## patents #############
            if hasattr(user, 'objects') == True:
                try:
                    if user.patents.filter(countary=uform.countary.data
                                , url=uform.url.data
                                , year=uform.year.data
                                , title=uform.title.data
                                        ).count() > 0:
                        return render_template_string("""
                                    {% extends "base.html" %} {% block content %}
                                        <h3>Patents {{name}} is in Patents List </h3>
                                    {% endblock %}
                                        """,name=uform.title.data)
                    pt = Patents(pk = get_a_uuid()
                                , countary=uform.countary.data
                                , url=uform.url.data
                                , year=uform.year.data
                                , title=uform.title.data
                                )
                    user.patents.append(pt)
                    user.save()
                    return redirect(request.form.get('next'))
                except DoesNotExist as e:
                    flash(id + ' Doest Not Exist')
                    return render_template_string(errormessages,messages= id + ' Doest Not Exist')
                except ValidationError as e:
                    flash(e.message)
                    flash(e.field_name)
                    flash(e.errors)
                    return render_template_string(errormessages,messages=e.message)

@users.route('/patents/<id>/<id1>', methods=['GET', 'POST'])  # username
@login_required
def patentsedit(id,id1):
    #user = User.objects(username=current_user.username).first()
    #tid = session["target_id"]
    user = User.objects(id=id).first()
    if request.method == 'GET':
        uform = UserPatentsForm()
        if hasattr(user, 'objects') == True:
            ######## patents ##############
            p = user.patents.get(pk = id1)
            uform.countary.data = p.countary
            uform.title.data = p.title
            uform.year.data = p.year
            uform.url.data = p.url
        return render_template_string(edit_create_view_id, form=uform, fn_target='users.patentsedit'
                                    , id=id, id1=id1, id2=None, id3=None, id4=None, id5=None 
                                    , back = request.referrer
                                    , kwargs = {'class_':'form-control fw-bold'})
        # return render_template('/user/patents.html', form=userpatentsform)
    if request.method == 'POST':
        uform = UserPatentsForm(request.form)
        if uform.validate_on_submit():
            ######## patents #############
            if hasattr(user, 'objects') == True:
                try:
                    if user.patents.filter(countary=uform.countary.data
                                , url=uform.url.data
                                , year=uform.year.data
                                , title=uform.title.data
                                        ).count() > 0:
                        return render_template_string("""
                                    {% extends "base.html" %} {% block content %}
                                        <h3>Patents {{name}} is in Patents List </h3>
                                    {% endblock %}
                                        """,name=uform.title.data)
                    p = user.patents.get(pk = id1)
                    p.countary = uform.countary.data
                    p.title = uform.title.data
                    p.year = uform.year.data
                    p.url = uform.url.data
                    user.save()
                    #print('Contact Saved')
                    # print(jsonify(user).get_json())
                    return redirect(request.form.get('next'))
                except DoesNotExist as e:
                    flash(id + ' Doest Not Exist')
                    return render_template_string(errormessages,messages= id + ' Doest Not Exist')
                except ValidationError as e:
                    flash(e.message)
                    flash(e.field_name)
                    flash(e.errors)
                    return render_template_string(errormessages,messages=e.message)
                

@users.route('/patentsdelete/<id>/<id1>', methods=['POST'])  # delete
@login_required
def patentsdelete(id,id1):
    #user = User.objects(username=current_user.username).first()
    #tid = session["target_id"]
    user = User.objects(id=id).first()
    if request.method == 'POST':
        if hasattr(user, 'objects') == True:
            try:
                p = user.patents.get(pk = id1)
                user.patents.remove(p)
                user.save()
                #print('Contact Saved')
                # print(jsonify(user).get_json())
                return redirect('/patents')
            except DoesNotExist as e:
                flash(id + ' Doest Not Exist')
                return render_template_string(errormessages,messages= id + ' Doest Not Exist')
            except ValidationError as e:
                flash(e.message)
                flash(e.field_name)
                flash(e.errors)
                return render_template_string(errormessages,messages=e.message)


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
                                        <a href="{{url_for('users.indcolabedit', pk = item.name)}}" >Edit</a>
                                        <a href="{{url_for('users.indcolabdelete', pk = item.name)}}" >Delete</a>
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
    #user = User.objects(username=current_user.username).first()
    tid = session["target_id"]
    user = User.objects(id=tid).first()
    if request.method == 'GET':
        if hasattr(user, 'objects') == True:
            ######## IndustryCollaboration ##############
            details_dict_view_list = []
            for p in user.industrycollaboration:
                details_dict_view_list.append(p.__dict__())
            return render_template_string(details_dict_listview, fn_target_new = 'users.indcolabcreate', fn_target_edit = 'users.indcolabedit', fn_target_delete = 'users.indcolabdelete'
                                          , back = request.referrer
                                          , id = user.id, detailitemslist=details_dict_view_list, tablehead = 'Industry Collaboration', tableheadrvalue = 'Information'
                                          , kwargs = {'class_':'form-control fw-bold'})
            #return render_template_string(indcolab_view, industrycollaborations=user.industrycollaboration)
        


@users.route('/indcolabcreate/<id>', methods=['GET', 'POST'])  # create
@login_required
def indcolabcreate(id):
    #user = User.objects(username=current_user.username).first()
    #tid = session["target_id"]
    user = User.objects(id=id).first()
    if request.method == 'GET':
        uform = UserIndustryCollaborationForm()
        if hasattr(user, 'objects') == True:
            return render_template_string(edit_create_view_id, form=uform, fn_target='users.indcolabcreate'
                                          , id=id, id1=None, id2=None, id3=None, id4=None, id5=None 
                                          , back = request.referrer
                                          , kwargs = {'class_':'form-control fw-bold'})
    if request.method == 'POST':
        uform = UserIndustryCollaborationForm(request.form)
        #print('form collected')
        if uform.validate_on_submit():
            ######## industrycollaboration #############
            #print('form validate_on_submit')
            if hasattr(user, 'objects') == True:
                try:
                    if user.industrycollaboration.filter( name=uform.name.data
                                , title=uform.title.data
                                        ).count() > 0:
                        return render_template_string("""
                                    {% extends "base.html" %} {% block content %}
                                        <h3>IndustryCollaboration {{name}} is in IndustryCollaboration List </h3>
                                    {% endblock %}
                                        """,name=uform.title.data)
                    ic = IndustryCollaboration(pk = get_a_uuid()
                                            , name=uform.name.data
                                            , url=uform.url.data
                                            , mou=uform.mou.data
                                            , collaboration=uform.collaboration.data
                                            , title=uform.title.data
                                            )
                    user.industrycollaboration.append(ic)
                    user.save()
                    return redirect(request.form.get('next'))
                except DoesNotExist as e:
                    flash(id + ' Doest Not Exist')
                    return render_template_string(errormessages,messages= id + ' Doest Not Exist')
                except ValidationError as e:
                    flash(e.message)
                    flash(e.field_name)
                    flash(e.errors)
                    return render_template_string(errormessages,messages=e.message)
                

@users.route('/indcolabedit/<id>/<id1>', methods=['GET', 'POST'])  # edit
@login_required
def indcolabedit(id,id1):
    #user = User.objects(username=current_user.username).first()
    #tid = session["target_id"]
    user = User.objects(id=id).first()
    if request.method == 'GET':
        uform = UserIndustryCollaborationForm()
        if hasattr(user, 'objects') == True:
            ######## industrycollaboration ##############
            ic = user.industrycollaboration.get(pk = id1)
            uform.name.data = ic.name
            uform.url.data = ic.url
            uform.mou.data = ic.mou
            uform.collaboration.data = ic.collaboration
            uform.title.data = ic.title
            return render_template_string(edit_create_view_id, form=uform, fn_target='users.indcolabedit'
                                    , id=id, id1=id1, id2=None, id3=None, id4=None, id5=None 
                                    , back = request.referrer
                                    , kwargs = {'class_':'form-control fw-bold'})
    if request.method == 'POST':
        uform = UserIndustryCollaborationForm(request.form)
        if uform.validate_on_submit():
            ######## industrycollaboration #############
            if hasattr(user, 'objects') == True:
                try:
                    if user.industrycollaboration.filter( name=uform.name.data
                                , title=uform.title.data
                                        ).count() > 0:
                        return render_template_string("""
                                    {% extends "base.html" %} {% block content %}
                                        <h3>IndustryCollaboration {{name}} is in IndustryCollaboration List </h3>
                                    {% endblock %}
                                        """,name=uform.title.data)
                    ic = user.industrycollaboration.get(pk = id1)
                    ic.name = uform.name.data
                    ic.url = uform.url.data
                    ic.mou = uform.mou.data
                    ic.collaboration = uform.collaboration.data
                    ic.title = uform.title.data
                    user.save()
                    return redirect(request.form.get('next'))
                except DoesNotExist as e:
                    flash(id + ' Doest Not Exist')
                    return render_template_string(errormessages,messages= id + ' Doest Not Exist')
                except ValidationError as e:
                    flash(e.message)
                    flash(e.field_name)
                    flash(e.errors)
                    return render_template_string(errormessages,messages=e.message)
                        

@users.route('/indcolabdelete/<id>/<id1>', methods=['POST'])  # delete
@login_required
def indcolabdelete(id,id1):
    #user = User.objects(username=current_user.username).first()
    #tid = session["target_id"]
    user = User.objects(id=id).first()
    if request.method == 'POST':
        if hasattr(user, 'objects') == True:
            try:
                ic = user.industrycollaboration.get(pk = id1)
                user.industrycollaboration.remove(ic)
                user.save()
                return redirect('/indcolab')
            except DoesNotExist as e:
                flash(id + ' Doest Not Exist')
                return render_template_string(errormessages,messages= id + ' Doest Not Exist')
            except ValidationError as e:
                flash(e.message)
                flash(e.field_name)
                flash(e.errors)
                return render_template_string(errormessages,messages=e.message)

######################################### Startup   ####################################################


@users.route('/startup', methods=['GET'])
@login_required
def startup():
    #user = User.objects(username=current_user.username).first()
    tid = session["target_id"]
    user = User.objects(id=tid).first()
    if request.method == 'GET':
        #userstartupform = UserStartUpForm()
        if hasattr(user, 'objects') == True:
            ######## startup ##############
            details_dict_view_list = []
            for p in user.startup:
                details_dict_view_list.append(p.__dict__())
            return render_template_string(details_dict_listview, fn_target_new = 'users.startupcreate', fn_target_edit = 'users.startupedit', fn_target_delete = 'users.startupdelete'
                                          , back = request.referrer
                                          , id = user.id, detailitemslist=details_dict_view_list, tablehead = 'Startup', tableheadrvalue = 'Information'
                                          , kwargs = {'class_':'form-control fw-bold'})
        else:
            return redirect('/')

@users.route('/startupcreate/<id>', methods=['GET', 'POST'])
@login_required
def startupcreate(id):
    #user = User.objects(username=current_user.username).first()
    #tid = session["target_id"]
    user = User.objects(id=id).first()
    if request.method == 'GET':
        uform = UserStartUpForm()
        if hasattr(user, 'objects') == True:
            ######## startup ##############
            return render_template_string(edit_create_view_id, form=uform, fn_target='users.startupcreate'
                                          , id=id, id1=None, id2=None, id3=None, id4=None, id5=None 
                                          , back = request.referrer
                                          , kwargs = {'class_':'form-control fw-bold'})
    if request.method == 'POST':
        uform = UserStartUpForm(request.form)
        if uform.validate_on_submit():
            #         ######## startup #############
            if hasattr(user, 'objects') == True:
                try:
                    if user.startup.filter( name=uform.name.data
                                        ).count() > 0:
                        return render_template_string("""
                                    {% extends "base.html" %} {% block content %}
                                        <h3>startup {{name}} is in startup List </h3>
                                    {% endblock %}
                                        """,name=uform.name.data)
                    stup = StartUp(pk = get_a_uuid()
                                   , name=uform.name.data
                                   , url=uform.url.data
                                   , funding=uform.funding.data)
                    user.startup.append(stup)
                    user.save()
                    return redirect(request.form.get('next'))
                except DoesNotExist as e:
                    flash(id + ' Doest Not Exist')
                    return render_template_string(errormessages,messages= id + ' Doest Not Exist')
                except ValidationError as e:
                    flash(e.message)
                    flash(e.field_name)
                    flash(e.errors)
                    return render_template_string(errormessages,messages=e.message)
                        
@users.route('/startupedit/<id>/<id1>', methods=['GET', 'POST'])
@login_required
def startupedit(id,id1):
    #user = User.objects(username=current_user.username).first()
    #tid = session["target_id"]
    user = User.objects(id=id).first()
    if request.method == 'GET':
        uform = UserStartUpForm()
        if hasattr(user, 'objects') == True:
            ######## startup ##############
            stup = user.startup.get(pk = id1)
            uform.name.data = stup.name
            uform.url.data = stup.url
            uform.funding.data = stup.funding
            return render_template_string(edit_create_view_id, form=uform, fn_target='users.startupedit'
                                          , id=id, id1=id1, id2=None, id3=None, id4=None, id5=None 
                                          , back = request.referrer, kwargs = {'class_':'form-control fw-bold'})
            # return render_template('/user/startup.html', form=userstartupform)
    if request.method == 'POST':
        uform = UserStartUpForm(request.form)
        if uform.validate_on_submit():
            #         ######## startup #############
            if hasattr(user, 'objects') == True:
                try:
                    if user.startup.filter( name=uform.name.data
                                        ).count() > 0:
                        return render_template_string("""
                                    {% extends "base.html" %} {% block content %}
                                        <h3>startup {{name}} is in startup List </h3>
                                    {% endblock %}
                                        """,name=uform.name.data)
                    stup = user.startup.get(pk = id1)
                    stup.name = uform.name.data
                    stup.url = uform.url.data
                    stup.funding = uform.funding.data
                    user.save()
                    return redirect(request.form.get('next'))
                except DoesNotExist as e:
                    flash(id + ' Doest Not Exist')
                    return render_template_string(errormessages,messages= id + ' Doest Not Exist')
                except ValidationError as e:
                    flash(e.message)
                    flash(e.field_name)
                    flash(e.errors)
                    return render_template_string(errormessages,messages=e.message)
                

@users.route('/startupdelete/<id>/<id1>', methods=['POST'])
@login_required
def startupdelete(id,id1):
    #user = User.objects(username=current_user.username).first()
    #tid = session["target_id"]
    user = User.objects(id=id).first()
    if request.method == 'POST':
        if hasattr(user, 'objects') == True:
            try:
                ic = user.startup.get(pk = id1)
                user.startup.remove(ic)
                user.save()
                return redirect('/startup')
            except DoesNotExist as e:
                flash(id + ' Doest Not Exist')
                return render_template_string(errormessages,messages= id + ' Doest Not Exist')
            except ValidationError as e:
                flash(e.message)
                flash(e.field_name)
                flash(e.errors)
                return render_template_string(errormessages,messages=e.message)

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
                                        <a href="{{url_for('users.booksedit', pk = item.title)}}" >Edit</a>
                                        <a href="{{url_for('users.booksdelete', pk = item.title)}}" >Delete</a>
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
    #user = User.objects(username=current_user.username).first()
    tid = session["target_id"]
    user = User.objects(id=tid).first()
    if request.method == 'GET':
        if hasattr(user, 'objects') == True:
            ######## IndustryCollaboration ##############
            details_dict_view_list = []
            for p in user.books:
                details_dict_view_list.append(p.__dict__())
            return render_template_string(details_dict_listview, fn_target_new = 'users.bookscreate', fn_target_edit = 'users.booksedit', fn_target_delete = 'users.booksdelete'
                                          , back = request.referrer
                                          , id = user.id, detailitemslist=details_dict_view_list, tablehead = 'Books', tableheadrvalue = 'Information'
                                          , kwargs = {'class_':'form-control fw-bold'})

@users.route('/bookscreate/<id>', methods=['GET', 'POST'])  # create
@login_required
def bookscreate(id):
    #user = User.objects(username=current_user.username).first()
    #tid = session["target_id"]
    user = User.objects(id=id).first()
    if request.method == 'GET':
        uform = UserBooksForm()
        if hasattr(user, 'objects') == True:
            return render_template_string(edit_create_view_id, form=uform, fn_target='users.bookscreate'
                                          , id=id, id1=None, id2=None, id3=None, id4=None, id5=None 
                                          , back = request.referrer
                                          , kwargs = {'class_':'form-control fw-bold'})
    if request.method == 'POST':
        uform = UserBooksForm(request.form)
        if uform.validate_on_submit():
            ######## industrycollaboration #############
            if hasattr(user, 'objects') == True:
                try:
                    if user.books.filter( name=uform.title.data
                                        ).count() > 0:
                        return render_template_string("""
                                    {% extends "base.html" %} {% block content %}
                                        <h3>books {{title}} is in books List </h3>
                                    {% endblock %}
                                        """,name=uform.title.data)
                    p = Books(pk = get_a_uuid()
                              ,title=uform.title.data
                              , description=uform.description.data
                              , year=uform.year.data
                              , url=uform.url.data
                              , publisher=uform.publisher.data
                            )
                    user.books.append(p)
                    user.save()
                    return redirect(request.form.get('next'))
                except DoesNotExist as e:
                    flash(id + ' Doest Not Exist')
                    return render_template_string(errormessages,messages= id + ' Doest Not Exist')
                except ValidationError as e:
                    flash(e.message)
                    flash(e.field_name)
                    flash(e.errors)
                    return render_template_string(errormessages,messages=e.message)
                

@users.route('/booksedit//<id>/<id1>', methods=['GET', 'POST'])
@login_required
def booksedit(id,id1):
    #user = User.objects(username=current_user.username).first()
    #tid = session["target_id"]
    user = User.objects(id=id).first()
    if request.method == 'GET':
        uform = UserBooksForm()
        if hasattr(user, 'objects') == True:
            ######## Books ##############
            p = user.books.get(pk = id1)
            uform.title.data = p.title
            uform.description.data = p.description
            uform.year.data = p.year
            uform.url.data = p.url
            uform.publisher.data = p.publisher
        return render_template_string(edit_create_view_id, form=uform, fn_target='users.booksedit'
                                      , id=id, id1=id1, id2=None, id3=None, id4=None, id5=None 
                                      , back = request.referrer, kwargs = {'class_':'form-control fw-bold'})
        # return render_template('/user/books.html', form=userbooksform)
    if request.method == 'POST':
        uform = UserBooksForm(request.form)
        if uform.validate_on_submit():
            ######## Faculty #############
            if hasattr(user, 'objects') == True:
                try:
                    if user.books.filter( name=uform.title.data
                                    ).count() > 0:
                        return render_template_string("""
                                {% extends "base.html" %} {% block content %}
                                    <h3>books {{title}} is in books List </h3>
                                {% endblock %}
                                    """,name=uform.title.data)
                    p = user.books.get(pk = id1)
                    p.title = uform.title.data
                    p.description = uform.description.data
                    p.year = uform.year.data
                    p.url = uform.url.data
                    p.publisher = uform.publisher.data
                    user.save()
                    return redirect(request.form.get('next'))
                except DoesNotExist as e:
                    flash(id + ' Doest Not Exist')
                    return render_template_string(errormessages,messages= id + ' Doest Not Exist')
                except ValidationError as e:
                    flash(e.message)
                    flash(e.field_name)
                    flash(e.errors)
                    return render_template_string(errormessages,messages=e.message)
                    #print('Contact Saved')
                    # print(jsonify(user).get_json())
                

@users.route('/booksdelete//<id>/<id1>', methods=['POST'])  # delete
@login_required
def booksdelete(id,id1):
    #user = User.objects(username=current_user.username).first()
    #tid = session["target_id"]
    user = User.objects(id=id).first()
    if request.method == 'POST':
        if hasattr(user, 'objects') == True:
            try:
                ic = user.books.get(pk = id1)
                user.books.remove(ic)
                user.save()
                return redirect('/books')
            except DoesNotExist as e:
                flash(id + ' Doest Not Exist')
                return render_template_string(errormessages,messages= id + ' Doest Not Exist')
            except ValidationError as e:
                flash(e.message)
                flash(e.field_name)
                flash(e.errors)
                return render_template_string(errormessages,messages=e.message)


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
                                        <a href="{{url_for('users.awardsedit', pk = item.name)}}" >Edit</a>
                                        <a href="{{url_for('users.awardsdelete', pk = item.name)}}" >Delete</a>
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
    #user = User.objects(username=current_user.username).first()
    tid = session["target_id"]
    user = User.objects(id=tid).first()
    if request.method == 'GET':
        if hasattr(user, 'objects') == True:
            ######## IndustryCollaboration ##############
            #return render_template_string(awards_view, awards=user.awards)
            details_dict_view_list = []
            for p in user.awards:
                details_dict_view_list.append(p.__dict__())
            return render_template_string(details_dict_listview, fn_target_new = 'users.awardscreate', fn_target_edit = 'users.awardsedit', fn_target_delete = 'users.awardsdelete'
                                          , back = request.referrer
                                          , id = user.id, detailitemslist=details_dict_view_list, tablehead = 'Awards', tableheadrvalue = 'Information'
                                          , kwargs = {'class_':'form-control fw-bold'})
        

@users.route('/awardscreate/<id>', methods=['GET', 'POST'])  # create
@login_required
def awardscreate(id):
    #user = User.objects(username=current_user.username).first()
    #tid = session["target_id"]
    user = User.objects(id=id).first()
    if request.method == 'GET':
        uform = UserAwardsForm()
        if hasattr(user, 'objects') == True:
            return render_template_string(edit_create_view_id, form=uform, fn_target='users.awardscreate'
                                          , id=id, id1=None, id2=None, id3=None, id4=None, id5=None 
                                          , back = request.referrer
                                          , kwargs = {'class_':'form-control fw-bold'})
    if request.method == 'POST':
        uform = UserAwardsForm(request.form)
        if uform.validate_on_submit():
            ######## awards #############
            if hasattr(user, 'objects') == True:
                try:
                    if user.awards.filter( name=uform.name.data
                                        ).count() > 0:
                        return render_template_string("""
                                    {% extends "base.html" %} {% block content %}
                                        <h3>awards {{title}} is in awards List </h3>
                                    {% endblock %}
                                        """,name=uform.name.data)
                    p = Awards(pk = get_a_uuid()
                               ,name=uform.name.data
                               , description=uform.description.data
                               , certificate=uform.certificate.data
                            )
                    user.awards.append(p)
                    user.save()
                    return redirect(request.form.get('next'))
                except DoesNotExist as e:
                    flash(id + ' Doest Not Exist')
                    return render_template_string(errormessages,messages= id + ' Doest Not Exist')
                except ValidationError as e:
                    flash(e.message)
                    flash(e.field_name)
                    flash(e.errors)
                    return render_template_string(errormessages,messages=e.message)
                

@users.route('/awardsedit//<id>/<id1>', methods=['GET', 'POST'])
@login_required
def awardsedit(id,id1):
    #user = User.objects(username=current_user.username).first()
    #tid = session["target_id"]
    user = User.objects(id=id).first()
    if request.method == 'GET':
        uform = UserAwardsForm()
        if hasattr(user, 'objects') == True:
            ######## awards ##############
            p = user.awards.get(pk = id1)
            uform.name.data = p.name
            uform.description.data = p.description
            uform.certificate.data = p.description
        return render_template_string(edit_create_view_id, form=uform, fn_target='users.awardsedit'
                                      , id=id, id1=id1, id2=None, id3=None, id4=None, id5=None 
                                      , back = request.referrer, kwargs = {'class_':'form-control fw-bold'})
        # return render_template('/user/awards.html', form=userawardsform)
    if request.method == 'POST':
        uform = UserAwardsForm(request.form)
        if uform.validate_on_submit():
            ######## Faculty #############
            if hasattr(user, 'objects') == True:
                try:
                    if user.awards.filter( name=uform.name.data
                                        ).count() > 0:
                        return render_template_string("""
                                    {% extends "base.html" %} {% block content %}
                                        <h3>awards {{name}} is in awards List </h3>
                                    {% endblock %}
                                        """,name=uform.name.data)
                    p = user.awards.get(pk = id1)
                    p.name = uform.name.data
                    p.description = uform.description.data
                    p.description = uform.certificate.data
                    user.save()
                    return redirect(request.form.get('next'))
                except DoesNotExist as e:
                    flash(id + ' Doest Not Exist')
                    return render_template_string(errormessages,messages= id + ' Doest Not Exist')
                except ValidationError as e:
                    flash(e.message)
                    flash(e.field_name)
                    flash(e.errors)
                    return render_template_string(errormessages,messages=e.message)


@users.route('/awardsdelete/<id>/<id1>', methods=['POST'])  # delete
@login_required
def awardsdelete(id,id1):
    #user = User.objects(username=current_user.username).first()
    #tid = session["target_id"]
    user = User.objects(id=id).first()
    if request.method == 'POST':
        if hasattr(user, 'objects') == True:
            try:
                ic = user.awards.get(pk = id1)
                user.awards.remove(ic)
                user.save()
                return redirect('/awards')
            except DoesNotExist as e:
                flash(id + ' Doest Not Exist')
                return render_template_string(errormessages,messages= id + ' Doest Not Exist')
            except ValidationError as e:
                flash(e.message)
                flash(e.field_name)
                flash(e.errors)
                return render_template_string(errormessages,messages=e.message)
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
                                        <a href="{{url_for('users.socialimpactedit', pk = item.name)}}" >Edit</a>
                                        <a href="{{url_for('users.socialimpactdelete', pk = item.name)}}" >Delete</a>
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
    #user = User.objects(username=current_user.username).first()
    tid = session["target_id"]
    user = User.objects(id=tid).first()
    if request.method == 'GET':
        if hasattr(user, 'objects') == True:
            ######## IndustryCollaboration ##############
            #return render_template_string(socialimpact_view, socialimpact=user.socialimpact)
            details_dict_view_list = []
            for p in user.socialimpact:
                details_dict_view_list.append(p.__dict__())
            return render_template_string(details_dict_listview, fn_target_new = 'users.socialimpactcreate', fn_target_edit = 'users.socialimpactedit', fn_target_delete = 'users.socialimpactdelete'
                                          , back = request.referrer
                                          , id = user.id, detailitemslist=details_dict_view_list, tablehead = 'Social Impact', tableheadrvalue = 'Information'
                                          , kwargs = {'class_':'form-control fw-bold'})
        else:
            return redirect('/')

@users.route('/socialimpactcreate/<id>', methods=['GET', 'POST'])  # create
@login_required
def socialimpactcreate(id):
    #user = User.objects(username=current_user.username).first()
    #tid = session["target_id"]
    user = User.objects(id=id).first()
    if request.method == 'GET':
        uform = UserSocialImpactForm()
        if hasattr(user, 'objects') == True:
            return render_template_string(edit_create_view_id, form=uform, fn_target='users.socialimpactcreate'
                                          , id=id, id1=None, id2=None, id3=None, id4=None, id5=None 
                                          , back = request.referrer
                                          , kwargs = {'class_':'form-control fw-bold'})
    if request.method == 'POST':
        uform = UserSocialImpactForm(request.form)
        if uform.validate_on_submit():
            ######## industrycollaboration #############
            if hasattr(user, 'objects') == True:
                try:
                    if user.socialimpact.filter( name=uform.name.data
                                        ).count() > 0:
                        return render_template_string("""
                                    {% extends "base.html" %} {% block content %}
                                        <h3>socialimpact {{name}} is in socialimpact List </h3>
                                    {% endblock %}
                                        """,name=uform.name.data)
                    p = SocialImpact(pk = get_a_uuid()
                                     , name=uform.name.data
                                     , url=uform.url.data
                                    )
                    user.socialimpact.append(p)
                    user.save()
                    return redirect(request.form.get('next'))
                except DoesNotExist as e:
                    flash(id + ' Doest Not Exist')
                    return render_template_string(errormessages,messages= id + ' Doest Not Exist')
                except ValidationError as e:
                    flash(e.message)
                    flash(e.field_name)
                    flash(e.errors)
                    return render_template_string(errormessages,messages=e.message)

@users.route('/socialimpactedit/<id>/<id1>', methods=['GET', 'POST'])
@login_required
def socialimpactedit(id,id1):
    #user = User.objects(username=current_user.username).first()
    #tid = session["target_id"]
    user = User.objects(id=id).first()
    if request.method == 'GET':
        uform = UserSocialImpactForm()
        if hasattr(user, 'objects') == True:
            ######## socialimpact ##############
            p = user.socialimpact.get(pk = id1)
            uform.name.data = p.name
            uform.url.data = p.url
        return render_template_string(edit_create_view_id, form=uform, fn_target='users.socialimpactedit'
                                      , id=id, id1=id1, id2=None, id3=None, id4=None, id5=None 
                                      , back = request.referrer, kwargs = {'class_':'form-control fw-bold'})
    if request.method == 'POST':
        uform = UserSocialImpactForm(request.form)
        if uform.validate_on_submit():
            ######## Faculty #############
            if hasattr(user, 'objects') == True:
                try:
                    if user.socialimpact.filter( name=uform.name.data
                                        ).count() > 0:
                        return render_template_string("""
                                    {% extends "base.html" %} {% block content %}
                                        <h3>socialimpact {{name}} is in socialimpact List </h3>
                                    {% endblock %}
                                        """,name=uform.name.data)
                    p = user.socialimpact.get(pk = id1)
                    p.name = uform.name.data
                    p.url = uform.url.data
                    user.save()
                    return redirect(request.form.get('next'))
                except DoesNotExist as e:
                    flash(id + ' Doest Not Exist')
                    return render_template_string(errormessages,messages= id + ' Doest Not Exist')
                except ValidationError as e:
                    flash(e.message)
                    flash(e.field_name)
                    flash(e.errors)
                    return render_template_string(errormessages,messages=e.message)


@users.route('/socialimpactdelete/<id>/<id1>', methods=['POST'])  # delete
@login_required
def socialimpactdelete(id,id1):
    #user = User.objects(username=current_user.username).first()
    #tid = session["target_id"]
    user = User.objects(id=id).first()
    if request.method == 'POST':
        if hasattr(user, 'objects') == True:
            try:
                ic = user.socialimpact.get(pk = id1)
                user.socialimpact.remove(ic)
                user.save()
                return redirect('/socialimpact')
            except DoesNotExist as e:
                flash(id + ' Doest Not Exist')
                return render_template_string(errormessages,messages= id + ' Doest Not Exist')
            except ValidationError as e:
                flash(e.message)
                flash(e.field_name)
                flash(e.errors)
                return render_template_string(errormessages,messages=e.message)


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
                                            <a href="{{url_for('users.technologytransferedit', pk = item.name)}}" >Edit</a>
                                            <a href="{{url_for('users.technologytransferdelete', pk = item.name)}}" >Delete</a>
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
    #user = User.objects(username=current_user.username).first()
    tid = session["target_id"]
    user = User.objects(id=tid).first()
    if request.method == 'GET':
        if hasattr(user, 'objects') == True:
            ######## IndustryCollaboration ##############
            details_dict_view_list = []
            for p in user.technologytransfer:
                details_dict_view_list.append(p.__dict__())
            return render_template_string(details_dict_listview, fn_target_new = 'users.technologytransfercreate', fn_target_edit = 'users.technologytransferedit', fn_target_delete = 'users.technologytransferdelete'
                                          , back = request.referrer
                                          , id = user.id, detailitemslist=details_dict_view_list, tablehead = 'Technology Transfer', tableheadrvalue = 'Information'
                                          , kwargs = {'class_':'form-control fw-bold'})

@users.route('/technologytransfercreate/<id>', methods=['GET', 'POST'])  # create
@login_required
def technologytransfercreate(id):
    #user = User.objects(username=current_user.username).first()
    #tid = session["target_id"]
    user = User.objects(id=id).first()
    if request.method == 'GET':
        uform = UserTechnologyTransferForm()
        if hasattr(user, 'objects') == True:
            return render_template_string(edit_create_view_id, form=uform, fn_target='users.technologytransfercreate'
                                          , id=id, id1=None, id2=None, id3=None, id4=None, id5=None 
                                          , back = request.referrer
                                          , kwargs = {'class_':'form-control fw-bold'})
    if request.method == 'POST':
        uform = UserTechnologyTransferForm(request.form)
        if uform.validate_on_submit():
            ######## industrycollaboration #############
            if hasattr(user, 'objects') == True:
                try:
                    if user.technologytransfer.filter( name=uform.name.data
                                        ).count() > 0:
                        return render_template_string("""
                                    {% extends "base.html" %} {% block content %}
                                        <h3>TechnologyTransfer {{name}} is in technologytransfer List </h3>
                                    {% endblock %}
                                        """,name=uform.name.data)
                    p = TechnologyTransfer(pk = get_a_uuid()
                                           ,name=uform.name.data
                                           , technology=uform.technology.data
                                           , url=uform.url.data
                                           , royalty=uform.royalty.data
                                       )
                    user.technologytransfer.append(p)
                    user.save()
                    return redirect(request.form.get('next'))
                except DoesNotExist as e:
                    flash(id + ' Doest Not Exist')
                    return render_template_string(errormessages,messages= id + ' Doest Not Exist')
                except ValidationError as e:
                    flash(e.message)
                    flash(e.field_name)
                    flash(e.errors)
                    return render_template_string(errormessages,messages=e.message)

@users.route('/technologytransferedit/<id>/<id1>', methods=['GET', 'POST'])
@login_required
def technologytransferedit(id,id1):
    #user = User.objects(username=current_user.username).first()
    #tid = session["target_id"]
    user = User.objects(id=id).first()
    if request.method == 'GET':
        uform = UserTechnologyTransferForm()
        if hasattr(user, 'objects') == True:
            ######## technologytransfer ##############
            p = user.technologytransfer.get(pk = id1)
            uform.name.data = p.name
            uform.technology.data = p.technology
            uform.url.data = p.url
            uform.royalty.data = p.royalty
        return render_template_string(edit_create_view_id, form=uform, fn_target='users.technologytransferedit'
                                      , id=id, id1=id1, id2=None, id3=None, id4=None, id5=None 
                                      , back = request.referrer, kwargs = {'class_':'form-control fw-bold'})
    if request.method == 'POST':
        uform = UserTechnologyTransferForm(request.form)
        if uform.validate_on_submit():
            ######## Faculty #############
            if hasattr(user, 'objects') == True:
                try:
                    if user.technologytransfer.filter( name=uform.name.data
                                        ).count() > 0:
                        return render_template_string("""
                                    {% extends "base.html" %} {% block content %}
                                        <h3>TechnologyTransfer {{name}} is in technologytransfer List </h3>
                                    {% endblock %}
                                        """,name=uform.name.data)
                    p = user.technologytransfer.get(pk = id1)
                    p.name = uform.name.data
                    p.technology = uform.technology.data
                    p.url = uform.url.data
                    p.royalty = uform.royalty.data
                    user.save()
                    #print('Contact Saved')
                    # print(jsonify(user).get_json())
                    return redirect(request.form.get('next'))
                except DoesNotExist as e:
                    flash(id + ' Doest Not Exist')
                    return render_template_string(errormessages,messages= id + ' Doest Not Exist')
                except ValidationError as e:
                    flash(e.message)
                    flash(e.field_name)
                    flash(e.errors)
                    return render_template_string(errormessages,messages=e.message)

@users.route('/technologytransferdelete/<id>/<id1>', methods=['POST'])  # delete
@login_required
def technologytransferdelete(id,id1):
    #user = User.objects(username=current_user.username).first()
    #tid = session["target_id"]
    user = User.objects(id=id).first()
    if request.method == 'POST':
        if hasattr(user, 'objects') == True:
            try:
                ic = user.technologytransfer.get(pk = id1)
                user.technologytransfer.remove(ic)
                user.save()
                return redirect('/technologytransfer')
            except DoesNotExist as e:
                flash(id + ' Doest Not Exist')
                return render_template_string(errormessages,messages= id + ' Doest Not Exist')
            except ValidationError as e:
                flash(e.message)
                flash(e.field_name)
                flash(e.errors)
                return render_template_string(errormessages,messages=e.message)
