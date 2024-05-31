import os
from flask import Blueprint, session, request, current_app, send_from_directory, render_template_string, redirect, url_for, flash
#from wtforms.validators import URL #InputRequired, Length
from mongoengine.errors import ValidationError, DoesNotExist, NotUniqueError
from mongoengine import URLField
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from bson.objectid import ObjectId
#from bson import ObjectId
from .users import Iscurrentuseradmin, errormessages, User, edit_create_view_id, details_dict_view
from .models import AllocatePapertoUserForm,DeallocatePapertoUserForm, PaperNewForm,PaperEditForm, PaperDeleteForm, PaperFileUplodedForm, PaperRefFileForm, PaperSelectForm, LinkDescForm
from .models import ResearchProblemForm, RPKeywordsForm, RPAplicationsForm, RPJournals_ConfForm, RPCode_LinksForm, RPDataSets_linksForm, RPPeoplesForm, RPArticalsForm, RPResouresForm, RPSocialmediaForm
from . import Paper, get_a_uuid, PaperPerson, ResearchProblem, FileUploded, LinkDesc,  PaperRefFile
from werkzeug.utils import secure_filename

papers = Blueprint('papers', __name__)


#############################################################   FileUploded   #################################################

def PaperFileUploded_filename(filename,ext):
    if not filename.strip():
        return None
    counter = 0
    fn = filename + '{}.' + ext
    while os.path.isfile(fn.format(counter)):
        counter += 1
    fn = fn.format(counter)
    return fn
    
# FileUploded at level 2 list
# paperid at level 0 /class property or attribute name(id1) at level 1 / attribute name at level 2 / value of arribute at level 2
PaperFileUplodedView = """
                {% from 'form_macros.html' import edit_create_view %}
                {% extends "base.html" %} {% block content %}
                (<button type="button" class="btn btn-info btn-sm" data-bs-toggle="modal" data-bs-target="#fileup">File Upload</button>)
                {{edit_create_view(form = form, fn_target = fn_target, kwargs = kwargs, backurl = backurl, id=id, id1=id1, id2=id2, id3=id3, id4=id4, id5=id5, enctypevalue = "multipart/form-data")}}
                <div class="modal fade" id="fileup" tabindex="-1" aria-labelledby="deletelabel" aria-hidden="true" role="dialog">
                    <div class="modal-dialog modal-dialog-centered">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" id="deletelabel">Alert</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                <form action="{{ url_for(fn_target, id = id, id1 = id1, id2 = id2, id3 = id3) }}" method="POST" enctype="multipart/form-data">
                                    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
                                    <input type="hidden" class="form-control col-sm-2 col-form-label ms-5" name="next" value={{backurl}} />
                                    <label for="fileupinput">File:</label>
                                    <input type="file" name="file" id="fileupinput"><br>
                                    <label for="fileupdescinput">File Desciption</label>
                                    <textarea name="desc" id="fileupdescinput" rows="4" cols="50"></textarea><br>
                                    <div class="form-group">
                                        <div>
                                            <button type="submit" class="btn btn-success">
                                                Upload
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
                {% endblock %}
                """
@papers.route('/paperfileuplodedl2/<id>/<id1>/<id2>/<id3>', methods=['GET', 'POST'])  
@login_required
def fileuplodedcreatel2(id,id1,id2,id3):
    if request.method == 'GET':
        uform = PaperFileUplodedForm()
        #return render_template_string(PaperFileUplodedView, form=pform)
        return render_template_string(PaperFileUplodedView, form=uform, fn_target='papers.fileuplodedcreatel2'
                                      , id=id, id1=id1, id2=id2, id3=id3, id4=None, id5=None
                                      , backurl = request.referrer
                                      , kwargs = {'class_':'form-control fw-bold'})
    if request.method == 'POST':
        #uform = UserContactsForm(request.form)
        uform = PaperFileUplodedForm(request.form)
        path = 'static/images/'
        mimetype = 'application/pdf'
        try:
            #check duplicate PaperRefFile
            #ad_duplicate = l1.filter(addtype = uform.contact.data['addtype'])
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file: #and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(path, filename))
                pap = Paper.objects(id=id).first()
                l1 = getattr(pap,str(id1)) # l1 = object at lavel 1 e.g. reffiles list ... etc
                l2 = l1.get(pk = id2) # PaperRefFile ... etc
                l3 = getattr(l2,str(id3))
                pfu = FileUploded(
                    pk = get_a_uuid()
                    ,filename = filename
                    ,path = path
                    ,ext = filename.rsplit('.', 1)[1].lower()
                    ,mimetype = mimetype
                    ,desc = request.form.get("desc")
                    )
                l3.append(pfu)
                pap.save()
                #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return redirect(request.form.get('next'))
                #return redirect(url_for('download_file', name=filename))
            # filename = secure_filename(uform.file.data.filename)
            # # if not filename.strip():
            # #     return None
            # # counter = 0
            # # fn = filename + '{}.' + ext
            # # while os.path.isfile(fn.format(counter)):
            # #     counter += 1
            # # fn = fn.format(counter)
            # pfu = FileUploded(
            #     pk = get_a_uuid()
            #     ,filename = filename
            #     ,path = '/'
            #     ,ext = uform.file.data.filename.rsplit('.', 1)[1].lower()
            #     ,mimetype = 'text/pdf'
            #     ,desc = 'First file'
            #     )
            # uform.file.data.save('/static/images',filename)
            # l3.append(pfu)
            # pap.save()
            # return redirect(request.form.get('next'))
            #return redirect('/')
        except DoesNotExist as e:
            flash(id1 + ' Doest Not Exist')
            return render_template_string(errormessages)
        except ValidationError as e:
            flash(e.message)
            flash(e.field_name)
            flash(e.errors)
            return render_template_string(errormessages)
        
@papers.route('/fileuplodededitl2/<id>/<id1>/<id2>/<id3>/<id4>', methods=['POST'])  
@login_required
def fileuplodededitl2(id,id1,id2,id3,id4):
    if request.method == 'POST':
        #uform = UserContactsForm(request.form)
        try:
            # id(level 0) for which user in document
            #pid = ObjectId(id)#session["target_id"]
            pap = Paper.objects(id=id).first() # Target user id
            
            # id1 for level 1 property(List) e.g. list of contacts/faculty ... etc
            # it will return List of property
            l1 = getattr(pap,str(id1)) # l1 = object at lavel 1 e.g. reffiles list ... etc
            
            l2 = l1.get(pk = id2) # PaperRefFile ... etc
            
            l3 = getattr(l2,str(id3)) # List of attribute id3 eg. PaperRefFile atribute office list id3='fileup'
            file_uploaded = l3.get(pk = id4) # find perticuler fileuploaded object in list
            file_uploaded.desc = request.form.get("desc")
            pap.save()
            return redirect(request.form.get('next'))
        except DoesNotExist as e:
            flash(id1 + ' Doest Not Exist')
            return render_template_string(errormessages)
        except ValidationError as e:
            flash(e.message)
            flash(e.field_name)
            flash(e.errors)
            return render_template_string(errormessages)

@papers.route('/fileuplodeddeletel2/<id>/<id1>/<id2>/<id3>/<id4>', methods=['POST'])  
@login_required
def fileuplodeddeletel2(id,id1,id2,id3,id4):
    if request.method == 'POST':
        #uform = UserContactsForm(request.form)
        try:
            # id(level 0) for which user in document
            #pid = ObjectId(id)#session["target_id"]
            pap = Paper.objects(id=id).first() # Target user id
            
            # id1 for level 1 property(List) e.g. list of contacts/faculty ... etc
            # it will return List of property
            l1 = getattr(pap,str(id1)) # l1 = object at lavel 1 e.g. reffiles list ... etc
            
            l2 = l1.get(pk = id2) # PaperRefFile ... etc
            
            l3 = getattr(l2,str(id3)) # List of attribute id3 eg. PaperRefFile atribute office list id3='fileup'
            file_uploaded = l3.get(pk = id4) # find perticuler fileuploaded object in list 
            file_to_remove = os.path.join(file_uploaded.path, file_uploaded.filename)
            l3.remove(file_uploaded)
            pap.save()
            os.remove(file_to_remove)
            return redirect(request.form.get('next'))
        except OSError as e:
                # If it fails, inform the user.
                flash(e.filename)
                flash(e.strerror)
                return render_template_string(errormessages)
        except DoesNotExist as e:
            flash(id1 + ' Doest Not Exist')
            return render_template_string(errormessages)
        except ValidationError as e:
            flash(e.message)
            flash(e.field_name)
            flash(e.errors)
            return render_template_string(errormessages)

# @papers.route('/filedown/<id>/<id1>', methods=['GET', 'POST'])  
# @login_required
# def filedown(id,id1):
#     print('Hello')
#     return send_from_directory('static/images', id1)
@papers.route('/download_file/<path>/<filename>', methods=['GET', 'POST'])
@login_required
def download_file(path, filename):
    #print(path.replace('-', '/'))
    return send_from_directory(path.replace('-', '/'), filename)
    #return send_from_directory(app.config["UPLOAD_FOLDER"], name)

PaperLinkDescView = """
                {% from 'form_macros.html' import edit_create_view %}
                {% extends "base.html" %} {% block content %}
                (<button type="button" class="btn btn-info btn-sm" data-bs-toggle="modal" data-bs-target="#linkdesc">Link/Url</button>)
                {{edit_create_view(form = form, fn_target = fn_target, kwargs = kwargs, backurl = backurl, id=id, id1=id1, id2=id2, id3=id3, id4=id4, id5=id5, enctypevalue = "application/x-www-form-urlencoded")}}
                <div class="modal fade" id="linkdesc" tabindex="-1" aria-labelledby="deletelabel" aria-hidden="true" role="dialog">
                    <div class="modal-dialog modal-dialog-centered">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" id="deletelabel">Alert</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                <form action="{{ url_for(fn_target, id = id, id1 = id1, id2 = id2, id3 = id3) }}" method="POST" enctype = "application/x-www-form-urlencoded">
                                    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
                                    <input type="hidden" class="form-control col-sm-2 col-form-label ms-5" name="next" value={{backurl}} />
                                    <label for="linkinput">Url/Link:</label>
                                    <input type="text" name="link" id="linkinput"><br>
                                    <label for="descinput">Url Desciption</label>
                                    <textarea name="desc" id="descinput" rows="4" cols="50"></textarea><br>
                                    <div class="form-group">
                                        <div>
                                            <button type="submit" class="btn btn-success">
                                                Submit
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
                {% endblock %}
                """
@papers.route('/linkdesccreatel2/<id>/<id1>/<id2>/<id3>', methods=['GET', 'POST'])  
@login_required
def linkdesccreatel2(id,id1,id2,id3):
    if request.method == 'GET':
        uform = LinkDescForm()
        #return render_template_string(PaperFileUplodedView, form=pform)
        return render_template_string(PaperLinkDescView, form=uform, fn_target='papers.linkdesccreatel2'
                                      , id=id, id1=id1, id2=id2, id3=id3, id4=None, id5=None
                                      , backurl = request.referrer
                                      , kwargs = {'class_':'form-control fw-bold'})
    if request.method == 'POST':
        uform = LinkDescForm(request.form)
        try:
            pap = Paper.objects(id=id).first()
            l1 = getattr(pap,str(id1)) # l1 = object at lavel 1 e.g. reffiles list ... etc
            l2 = l1.get(pk = id2) # PaperRefFile ... etc
            l3 = getattr(l2,str(id3)) # list of links 
            #check duplicate PaperRefFile
            if l3.filter(link = uform.link.data).count() > 0:
                return render_template_string("""
                        {% extends "base.html" %} {% block content %}
                            <h3>Link {{link}} is in list </h3>
                        {% endblock %}
                            """,link=uform.link.data)
            #ad_duplicate = l1.filter(addtype = uform.contact.data['addtype'])
            ld = LinkDesc(pk = get_a_uuid()
                    ,link = uform.link.data
                    ,desc = uform.desc.data
                    )
            l3.append(ld)
            pap.save()
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(request.form.get('next'))
        except DoesNotExist as e:
            flash(id1 + ' Doest Not Exist')
            return render_template_string(errormessages)
        except ValidationError as e:
            flash(e.message)
            flash(e.field_name)
            flash(e.errors)
            return render_template_string(errormessages)

@papers.route('/linkdesceditl2/<id>/<id1>/<id2>/<id3>/<id4>', methods=['GET', 'POST'])
@login_required
def linkdesceditl2(id,id1,id2,id3,id4):
    if request.method == 'POST':
        #uform = UserContactsForm(request.form)
        try:
            # id(level 0) for which user in document
            #pid = ObjectId(id)#session["target_id"]
            pap = Paper.objects(id=id).first() # Target user id
            
            # id1 for level 1 property(List) e.g. list of contacts/faculty ... etc
            # it will return List of property
            l1 = getattr(pap,str(id1)) # l1 = object at lavel 1 e.g. reffiles list ... etc
            
            l2 = l1.get(pk = id2) # PaperRefFile ... etc
            
            l3 = getattr(l2,str(id3)) # List of attribute id3 eg. PaperRefFile atribute office list id3='fileup'
            ld = l3.get(pk = id4) # find perticuler LinkDesc object in list
            ld.link = request.form.get("link")
            ld.desc = request.form.get("desc")
            pap.save()
            return redirect(request.form.get('next'))
        except DoesNotExist as e:
            flash(id1 + ' Doest Not Exist')
            return render_template_string(errormessages)
        except ValidationError as e:
            flash(e.message)
            flash(e.field_name)
            flash(e.errors)
            return render_template_string(errormessages)

@papers.route('/linkdescdeletel2/<id>/<id1>/<id2>/<id3>/<id4>', methods=['POST'])
@login_required
def linkdescdeletel2(id,id1,id2,id3,id4):
    if request.method == 'POST':
        #uform = UserContactsForm(request.form)
        try:
            # id(level 0) for which user in document
            #pid = ObjectId(id)#session["target_id"]
            pap = Paper.objects(id=id).first() # Target user id
            
            # id1 for level 1 property(List) e.g. list of contacts/faculty ... etc
            # it will return List of property
            l1 = getattr(pap,str(id1)) # l1 = object at lavel 1 e.g. reffiles list ... etc
            
            l2 = l1.get(pk = id2) # PaperRefFile ... etc
            
            l3 = getattr(l2,str(id3)) # List of attribute id3 eg. PaperRefFile atribute office list id3='fileup'
            ld = l3.get(pk = id4) # find perticuler LinkDesc object in list 
            l3.remove(ld)
            pap.save()
            return redirect(request.form.get('next'))
        except OSError as e:
                # If it fails, inform the user.
                flash(e.filename)
                flash(e.strerror)
                return render_template_string(errormessages)
        except DoesNotExist as e:
            flash(id1 + ' Doest Not Exist')
            return render_template_string(errormessages)
        except ValidationError as e:
            flash(e.message)
            flash(e.field_name)
            flash(e.errors)
            return render_template_string(errormessages)




###### /pid/pid1/pid2/pid3
#pid = None pid1 = None pid2 = None pid3 = None
edit_create_view_paper = """
                {% extends "base.html" %} {% block content %}
                
                {% if pid != None %}
                    {% if pid1 != None %}
                        {% if pid2 != None %}
                            {% if pid3 != None %}
                                <form action="{{ url_for(fn_target, pid = pid, pid1 = pid1, pid2 = pid2, pid3 = pid3) }}" method="POST">
                            {% else %}
                                <form action="{{ url_for(fn_target, pid = pid, pid1 = pid1, pid2 = pid2) }}" method="POST">
                            {% endif %}
                        {% else %}
                            <form action="{{ url_for(fn_target, pid = pid, pid1 = pid1) }}" method="POST">
                        {% endif %}
                    {% else %}
                        <form action="{{ url_for(fn_target, pid = pid) }}" method="POST">
                    {% endif %}
                {% else %}
                    <form action="{{ url_for(fn_target) }}" method="POST">
                {% endif %}
                {{ form.hidden_tag() }}
                {{ form.csrf_token }}
                <input type="hidden" class="form-control col-sm-2 col-form-label ms-5" name="next" value={{back}} />
                {% for field in form %}
                <div class="form-group row mb-3">
                    {% if field.type != 'SubmitField' %}
                        {% if field.id != 'csrf_token' %}
                            <label for="{{ field.id }}" class="control-label col-sm-2 col-form-label ms-5">{{ field.label.text|safe }}</label>
                            <div class="col-sm-10 mx-5">
                            {{ field(**kwargs)|safe }}
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
# dict to html table
details_dict_view_paper = """"  
    {% extends "base.html" %} {% block content %}
    
    {% if pid != None %}
        {% if pid1 != None %}
            {% if pid2 != None %}
                {% if pid3 != None %}
                    <form action="{{ url_for(fn_target, pid = pid, pid1 = pid1, pid2 = pid2, pid3 = pid3) }}" method="POST">
                {% else %}
                    <form action="{{ url_for(fn_target, pid = pid, pid1 = pid1, pid2 = pid2) }}" method="POST">
                {% endif %}
            {% else %}
                <form action="{{ url_for(fn_target, pid = pid, pid1 = pid1) }}" method="POST">
            {% endif %}
        {% else %}
            <form action="{{ url_for(fn_target, pid = pid) }}" method="POST">
        {% endif %}
    {% else %}
        <form action="{{ url_for(fn_target) }}" method="POST">
    {% endif %}
    
    
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
####################################################################################################################
#def __dict__(self): 'pk':self.pk,  It is PK and index key in EmbeddedDocument. It is used for edit update, delete opration.
# dict to html table
details_dict_listview_paper = """"  
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


def Is_target_useris_author_of_sessionpaper():
    tid = session["target_id"]  #user
    user = User.objects(id=tid).first()
    for pid in user.papers:
        if session["paper_id"] == pid:
            return True
    return False
#########################################################################################################
################################  select target paper from user papers list (stpfupl) ###########################
@papers.route('/printpaper', methods=['GET', 'POST'])
@login_required
def printpaper():
    if request.method == 'GET':
        print(session["paper_id"])
        pid = session["paper_id"]
        pap = Paper.objects(id=pid).first()
        #print(pap.__dict__())
        return render_template_string("""
                        {% extends "base.html" %} {% block content %}
                        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
                            <a href="{{url_for('papers.editpaper', pid = paper.id)}}"><h1>Paper Title : {{paper.title}}  </h1></a>
                            <h2>Status : {{paper.status}}</h2><br/>
                            <a href="{{url_for('papers.addkeyword', pid = paper.id)}}"><h2>Add keyword   </h2></a>
                            {% for kword in paper.rp.keywords %}
                                {% if kword.link == '' or kword.link == None%}
                                    <h4>{{kword.desc}} </h4> <a href="{{url_for('papers.editkeyword', pid = paper.id, pid1 = kword.desc)}}"> Edit </a>
                                {% else %}
                                    <a href={{kword.link}}><h4>{{kword.desc}}   </h4></a>
                                {% endif %}
                            {% endfor %}
                        {% endblock %}
                    """               
                    ,paper=pap, fn_target='papers.printpaper')
        #return render_template_string(details_dict_view,userdict=pap.__dict__(),tablehead='Personal Details',tableheadrvalue='Information',fn_target='papers.printpaper')
        # for a in pap.authors:
        #     print(a.affiliation.__dict__()) # affiliation

@papers.route('/stpfupl', methods=['GET', 'POST'])
@login_required
def stpfupl():
    if request.method == 'GET':
        tid = session["target_id"]  #user
        user = User.objects(id=tid).first()
        utitles = []
        for pid in user.papers:
            utitles.append((Paper.objects(id=pid).first()).title)
        return render_template_string("""
                                {% extends "base.html" %} {% block content %}
                                    <a href="{{url_for('papers.allocatepapertouser')}}">Assign Paper to User</a>
                                    <form action="{{ url_for(fn_target) }}" method="POST">
                                        {{ form.hidden_tag() }}
                                        {{ form.csrf_token }}
                                        <table>
                                            <thead>
                                                <tr>
                                                <th>Select One Check Box</th>
                                                <th>Paper Title (<a href="{{url_for(fn_target)}}">Edit</a>)</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                {% for p in utitles %}
                                                    <div class="form-group row mb-3">
                                                        <tr>
                                                            <td> <input type="checkbox" id={{p}} name="title" value={{p}}> </td>
                                                            <td> <label for="title"> {{ p }}</label></td>
                                                        </tr>
                                                    </div>
                                                {% endfor %}
                                            </tbody>
                                        </table>
                                        <input type="submit" class="btn btn-primary mx-4 form-control" value="Submit">
                                    </form>
                                {% endblock %}
                                """,form=FlaskForm(), fn_target='papers.stpfupl', utitles=utitles)
    if request.method == 'POST':
        #request.form
        #if request.form. #validate_on_submit():
        title = request.form.get('title')
        pid = Paper.objects(title=title).first().id
        session["paper_id"] = pid
        return render_template_string("""
                            {% extends "base.html" %} {% block content %}
                                <a href="{{url_for('papers.allocatepapertouser')}}">Assign Paper to User</a>
                                <h3>Paper {{title}} is selected  </h3>
                            {% endblock %}
                            """
                            ,title=title)

############################################################################################################
################################  Allocate paper to user ###########################
@papers.route('/paperusers', methods=['GET'])
@login_required
def paperusers():
    if request.method == 'GET':
        pid = session["paper_id"]  #paper in session (selected)
        pap = Paper.objects(id=pid).first()
        authers = []
        for pp in pap.authors:
            authers.append(pp.name + ' ' + pp.email)
        return render_template_string("""
                                {% extends "base.html" %} {% block content %}
                                    <a href="{{url_for('papers.allocatepapertouser')}}">Assign Paper to User</a>
                                    <form action="{{ url_for(fn_target) }}" method="POST">
                                        {{ form.hidden_tag() }}
                                        {{ form.csrf_token }}
                                        <table>
                                            <thead>
                                                <tr>
                                                <th>Select One Check Box</th>
                                                <th>Paper Title (<a href="{{url_for(fn_target)}}">Edit</a>)</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                {% for p in utitles %}
                                                    <div class="form-group row mb-3">
                                                        <tr>
                                                            <td> <input type="checkbox" id={{p}} name="title" value={{p}}> </td>
                                                            <td> <label for="title"> {{ p }}</label></td>
                                                        </tr>
                                                    </div>
                                                {% endfor %}
                                            </tbody>
                                        </table>
                                        <input type="submit" class="btn btn-primary mx-4 form-control" value="Submit">
                                    </form>
                                {% endblock %}
                                """,form=FlaskForm(), fn_target='papers.paperusers', utitles=authers)

@papers.route('/allocatepapertouser', methods=['GET', 'POST'])
@login_required
def allocatepapertouser():
    if Iscurrentuseradmin() != True:
        flash('You are not Admin')
        return render_template_string(errormessages,messages='You are not Admin')
    else:
        if request.method == 'GET':
            pform = AllocatePapertoUserForm()
            #print('Paper created')
            return render_template_string(edit_create_view_paper, form=pform, fn_target='papers.allocatepapertouser', key_str=None, kwargs ={'class_':'form-control fw-bold'})
        if request.method == 'POST':
            pform = AllocatePapertoUserForm(request.form)
            if pform.validate_on_submit():
                try:
                    tid = session["target_id"]  #user
                    user = User.objects(id=tid).first()
                    pap = Paper.objects(title=pform.title.data).first()
                    session["paper_id"] = pap.id
                    # Check if paper is already in users papers list
                    for p in user.papers:
                        if p.title == pform.title.data:
                            return render_template_string("""
                                {% extends "base.html" %} {% block content %}
                                    <a href="{{url_for('papers.allocatepapertouser')}}">Assign Paper to User</a>
                                    <h3>Paper {{title}} already Assigned to User  </h3>
                                {% endblock %}
                                """
                                ,title=p.title)
                    user.papers.append(pap.id)
                    user.save()
                    return render_template_string("""
                                {% extends "base.html" %} {% block content %}
                                    <a href="{{url_for('papers.allocatepapertouser')}}">Assign Paper to User</a>
                                    {% for pid in papers %}
                                    <h4>Paper {{pid}} Assigned to User  </h4>
                                    {% endfor %}
                                {% endblock %}
                                """
                                ,papers=user.papers)
                except ValidationError as e:
                        flash(e.message)
                        flash(e.field_name)
                        flash(e.errors)
                        return render_template_string(errormessages)
                
@papers.route('/deallocatepapefromouser', methods=['GET', 'POST'])
@login_required
def deallocatepapefromouser():
    if Iscurrentuseradmin() != True:
        flash('You are not Admin')
        return render_template_string(errormessages,messages='You are not Admin')
    else:
        if request.method == 'GET':
            pform = DeallocatePapertoUserForm()
            #print('Paper created')
            return render_template_string(edit_create_view_paper, form=pform, fn_target='papers.deallocatepapefromouser', key_str=None, kwargs ={'class_':'form-control fw-bold'})
        if request.method == 'POST':
            pform = DeallocatePapertoUserForm(request.form)
            if pform.validate_on_submit():
                try:
                    tid = session["target_id"]  #user
                    user = User.objects(id=tid).first()
                    pap = Paper.objects(title=pform.title.data).first()
                    
                    # Check if paper is in users papers list
                    for p in user.papers:
                        if p.title == pform.title.data:
                            session["paper_id"] = None
                            user.papers.remove(pap.id)
                            user.save()
                            return render_template_string("""
                                {% extends "base.html" %} {% block content %}
                                    <a href="{{url_for('papers.allocatepapertouser')}}">DeAllocatepapefromouser Paper from User</a>
                                    <h3>Paper {{title}} already Assigned to User  </h3>
                                {% endblock %}
                                """
                                ,title=p.title)
                    
                    return render_template_string("""
                                {% extends "base.html" %} {% block content %}
                                    <a href="{{url_for('papers.allocatepapertouser')}}"> Paper is not in User papers List</a>
                                    {% for pid in papers %}
                                    <h4>Paper {{pid}} Assigned to User  </h4>
                                    {% endfor %}
                                {% endblock %}
                                """
                                ,papers=user.papers)
                except ValidationError as e:
                        flash(e.message)
                        flash(e.field_name)
                        flash(e.errors)
                        return render_template_string(errormessages)

# Select paper for diffrent operantion in session variable target_paper
@papers.route('/paperselect', methods=['GET', 'POST'])
@login_required
def paperselect():
    ##pid = session["paper_id"]  #paper in session (selected)
    id = session["target_id"]
    user = User.objects(id=id).first()
    pap_titles = []
    for pid in user.papers:
        pap_titles.append(Paper.objects(id=pid).first().title)
    
    if request.method == 'GET':
            uform = PaperSelectForm()
            uform.paperseleted.choices = [(count, value) for count, value in enumerate(pap_titles)] #uform.paperseleted.choices = [(count, value) for count, value in enumerate(pap_titles, start=1)]
            if request.referrer is None:
                #print(request.referrer)
                #print('back is none')
                return render_template_string(edit_create_view_paper, form=uform, fn_target='papers.paperselect'
                                      , pid=None, pid1=None, pid2=None, pid3=None
                                      , back = '/'
                                      , kwargs = {'class_':'form-control fw-bold'})
            
            return render_template_string(edit_create_view_paper, form=uform, fn_target='papers.paperselect'
                                      , pid=None, pid1=None, pid2=None, pid3=None
                                      , back = request.referrer
                                      , kwargs = {'class_':'form-control fw-bold'})
    if request.method == 'POST':
        uform = PaperSelectForm(request.form)
        uform.paperseleted.choices = [(count, value) for count, value in enumerate(pap_titles)] #uform.paperseleted.choices = [(count, value) for count, value in enumerate(pap_titles, start=1)]
        if uform.validate_on_submit():
            try:
                session["paper_id"] = Paper.objects(title=pap_titles[uform.paperseleted.data]).first().id
                #print(pap_titles[uform.paperseleted.data])
                #print(session["paper_id"])
                #return redirect('/reffiles')
                return redirect(request.form.get('next'))
            except ValidationError as e:
                flash(e.message)
                flash(e.field_name)
                flash(e.errors)
                return render_template_string(errormessages)
###############################################################################################################
############################################## paper CRUD #####################################################

@papers.route('/createpaper', methods=['GET', 'POST'])
@login_required
def createpaper():
    if Iscurrentuseradmin() != True:
        flash('You are not Admin')
        return render_template_string(errormessages,messages='You are not Admin')
    else:
        if request.method == 'GET':
            pform = PaperNewForm()
            #print('Paper created')
            return render_template_string(edit_create_view_paper, form=pform, fn_target='papers.createpaper'
                                      , pid=None, pid1=None, pid2=None, pid3=None
                                      , back = request.referrer
                                      , kwargs = {'class_':'form-control fw-bold'})
            #return render_template_string(edit_create_view, form=papernewform, fn_target='papers.createpaper', key_str=None, kwargs ={'class_':'form-control fw-bold'})
        if request.method == 'POST':
            pform = PaperNewForm(request.form)
            if pform.validate_on_submit():
                title = pform.title.data #request.form.get("username")
                status = pform.status.data #request.form.get("password")                
                u = Paper.objects(title=title).first()
                if u != None: 
                    return render_template_string("""
                        {% extends "base.html" %} {% block content %}
                            <a href="{{url_for('papers.createpaper')}}">Add New Paper </a>
                            <h3>Paper {{title}} already Exits  </h3>
                        {% endblock %}
                        """
                        ,title=title)
                else: # No paper with this title
                    pap = Paper(title=title,status=status) # Create new paper for target user
                    
                    paperperson = PaperPerson(user_id = session["target_id"])
                    #paperperson.user_id = session["target_id"] # target user  ####current_user.id
                    user = User.objects(id=paperperson.user_id).first()
                    try:
                        pap.authors.append(paperperson)
                        
                        
                        pap.save()
                        user.papers.append(pap.id) # target user
                        user.save()
                        session["paper_id"] = pap.id # new paper is assigned in session
                    except ValidationError as e:
                        flash(e.message)
                        flash(e.field_name)
                        flash(e.errors)
                        return render_template_string(errormessages)
                    
                    return render_template_string("""
                        {% extends "base.html" %} {% block content %}
                            <a href="{{url_for('papers.createpaper')}}">Add New Paper</a>
                            <h3>paper {{title}} {{id}}is Created. Fill other detiails </h3>
                        {% endblock %}
                        """
                        ,title=title,id=pap.id)

@papers.route('/deletepaper/<pid>', methods=['GET', 'POST'])
@login_required
def deletepaper(pid):
    if Iscurrentuseradmin() != True:
        flash('You are not Admin')
        return render_template_string(errormessages,messages='You are not Admin')
    else:
        if request.method == 'GET':
            pform = PaperDeleteForm()
            #print('Paper created')
            return render_template_string(edit_create_view_paper, form=pform, fn_target='papers.deletepaper'
                                      , pid=pid, pid1=None, pid2=None, pid3=None
                                      , back = request.referrer
                                      , kwargs = {'class_':'form-control fw-bold'})
        if request.method == 'POST':
            pform = PaperDeleteForm(request.form)
            if pform.validate_on_submit():
                title = pform.title.data #request.form.get("username")
                pap = Paper.objects(title=title).first()
                if pap == None: 
                    return render_template_string("""
                        {% extends "base.html" %} {% block content %}
                            <a href="{{url_for('papers.createpaper')}}">Add New Paper </a>
                            <h3>Paper {{title}} do not Exits  </h3>
                        {% endblock %}
                        """
                        ,title=title)
                else: # No paper with this title
                    usr = []
                    for auth in pap.authors:
                        usr.append(auth.user_id)
                    try:
                        for u in usr:
                            u_p = User.objects(id=u).first()
                            u_p.papers.remove(pap.id)
                            u_p.save()
                        pap.delete()
                        return redirect(request.form.get('next'))
                        # return render_template_string("""
                        # {% extends "base.html" %} {% block content %}
                        #     <a href="{{url_for('papers.createpaper')}}">Add New Paper </a>
                        #     <h3>Paper {{title}} Deleted  </h3>
                        #      <a href="{{url_for('papers.deletepaper')}}">Delete another Paper </a>
                        # {% endblock %}
                        # """
                        # ,title=title)
                    except ValidationError as e:
                        flash(e.message)
                        flash(e.field_name)
                        flash(e.errors)
                        return render_template_string(errormessages)

@papers.route('/editpaper/<pid>', methods=['GET', 'POST'])
@login_required
def editpaper(pid): # PaperEditForm
    if Is_target_useris_author_of_sessionpaper() == False:
        return render_template_string("""
                        {% extends "base.html" %} {% block content %}
                            <h3>You are not author of this paper. Select another paper  </h3>
                        {% endblock %}
                    """)
    if request.method == 'GET':
        #print(request.referrer)
        pform = PaperEditForm()
        papid = ObjectId(pid)#session["paper_id"]
        pap = Paper.objects(id=papid).first()
        pform.title.data = pap.title
        pform.status.data = pap.status
        return render_template_string(edit_create_view_paper, form=pform, fn_target='papers.editpaper'
                                      , pid=pid, pid1=None, pid2=None, pid3=None
                                      , back = request.referrer
                                      , kwargs = {'class_':'form-control fw-bold'})
    if request.method == 'POST':
        pform = PaperEditForm(request.form)
        if pform.validate_on_submit():
            try:
                papid = ObjectId(pid)#session["paper_id"]
                pap = Paper.objects(id=papid).first()
                pap.title = pform.title.data
                pap.status = pform.status.data
                pap.save()
                return redirect(request.form.get('next'))
            except ValidationError as e:
                flash(e.message)
                flash(e.field_name)
                flash(e.errors)
                return render_template_string(errormessages)
            #print('hi')
            #print(request.form.get('next'))
            #return redirect(request.form.get('next'))
            #return render_template_string(details_dict_view,userdict=pap.__dict__(),tablehead='Paper Details',tableheadrvalue='Information',fn_target='papers.editpaper')


# @papers.route('/paper', methods=['GET', 'POST'])
# @login_required
# def paper(): ####### read /  display paper

#######################################################################################################################
###################################### researchproblem CRUD  ##############################################################   
@papers.route('/createresearchproblem/<pid>', methods=['GET', 'POST'])
@login_required
def createresearchproblem(pid):
    if Is_target_useris_author_of_sessionpaper() == False:
        return render_template_string("""
                        {% extends "base.html" %} {% block content %}
                            <h3>You are not author of this paper. Select another paper  </h3>
                        {% endblock %}
                    """)
    if request.method == 'GET':
        pform = ResearchProblemForm()
        #print('Paper created')
        return render_template_string(edit_create_view_paper, form=pform, fn_target='papers.createresearchproblem'
                                      , pid=pid, pid1=None, pid2=None, pid3=None
                                      , back = request.referrer
                                      , kwargs = {'class_':'form-control fw-bold'})
        #return render_template_string(edit_create_view_paper, form=pform, fn_target='papers.createresearchproblem', pid=pid, pid1=None, pid2=None, pid3=None, kwargs ={'class_':'form-control fw-bold'})
    if request.method == 'POST':
        pform = ResearchProblemForm(request.form)
        if pform.validate_on_submit():
            papid = ObjectId(pid)#session["paper_id"]
            pap = Paper.objects(id=papid).first()
            statment = pform.statment.data #request.form.get("username")
            # did problum stsatment already exists
        try:
            if pap.rp.statment == statment:
            #print('Research problem exist')
                return render_template_string("""
                        {% extends "base.html" %} {% block content %}
                            <a href="{{url_for('papers.editresearchproblem', pid = pid)}}">Edit Problem Statment</a>
                            <h3>Problem Statment {{statment}} already Exits  </h3>
                        {% endblock %}
                    """
                    ,statment=statment, pidr=pid)
            pap.rp.statment = statment
            pap.rp.desc = pform.desc.data
            pap.save()
            return redirect(request.form.get('next'))
        except ValidationError as e:
            flash(e.message)
            flash(e.field_name)
            flash(e.errors)
            return render_template_string(errormessages)
        # # return render_template_string("""
        # #     {% extends "base.html" %} {% block content %}
        # #         <a href="{{url_for('papers.editresearchproblem', pid = pid)}}">Edit Problem Statment</a>
        # #         <h3>Problem Statment {{statment}} is Created. Fill other detiails </h3>
        # #     {% endblock %}
        # #     """
        # #     ,statment=statment, pid_str=pid)

        
@papers.route('/editresearchproblem/<pid>', methods=['GET', 'POST'])
@login_required
def editresearchproblem(pid):
    if Is_target_useris_author_of_sessionpaper() == False:
        return render_template_string("""
                        {% extends "base.html" %} {% block content %}
                            <h3>You are not author of this paper. Select another paper  </h3>
                        {% endblock %}
                    """)
    if request.method == 'GET':
        pform = ResearchProblemForm()
        papid = ObjectId(pid) #session["paper_id"]
        pap = Paper.objects(_id=papid).first()
        pform.statment.data = pap.rp.statment
        pform.desc.data = pap.rp.desc
        return render_template_string(edit_create_view_paper, form=pform, fn_target='papers.editresearchproblem'
                                      , pid=pid, pid1=None, pid2=None, pid3=None
                                      , back = request.referrer
                                      , kwargs = {'class_':'form-control fw-bold'})
        #return render_template_string(edit_create_view_paper, form=pform, fn_target='papers.editresearchproblem', pid=pid,pid1=None,pid2=None,pid3=None, kwargs ={'class_':'form-control fw-bold'})
    if request.method == 'POST':
        pform = ResearchProblemForm(request.form)
        if pform.validate_on_submit():
            papid = ObjectId(pid)#session["paper_id"]
            pap = Paper.objects(_id=papid).first()
            try:
                pap.rp.statment = pform.statment.data
                pap.rp.desc = pform.desc.data
                pap.save()
            except ValidationError as e:
                flash(e.message)
                flash(e.field_name)
                flash(e.errors)
                return render_template_string(errormessages)
            return render_template_string(details_dict_view,userdict=pap.rp.__dict__(),tablehead='Paper Details',tableheadrvalue='Information',fn_target='papers.editresearchproblem')
        

# # # @papers.route('/deleteresearchproblem', methods=['GET', 'POST'])
# # # @login_required
# # # def deleteresearchproblem():

# @papers.route('/researchproblem', methods=['GET', 'POST'])
# @login_required
# def researchproblem():

################################## /keyword in rp   /keyword<pid>/rp/<kid>   ########################
@papers.route('/keyword/<pid>/rp', methods=['GET', 'POST'])
@login_required
def addkeyword(pid):
    if Is_target_useris_author_of_sessionpaper() == False:
        return render_template_string("""
                        {% extends "base.html" %} {% block content %}
                            <h3>You are not author of this paper. Select another paper  </h3>
                        {% endblock %}
                    """)
    if request.method == 'GET':
        #print(request.referrer)
        pform = RPKeywordsForm()
        # papid = ObjectId(pid)#session["paper_id"]
        # pap = Paper.objects(id=papid).first()
        # pform.title.data = pap.title
        # pform.status.data = pap.status
        return render_template_string(edit_create_view_paper, form=pform, fn_target='papers.addkeyword'
                                      , pid=pid, pid1=None, pid2=None, pid3=None
                                      , back = request.referrer
                                      , kwargs = {'class_':'form-control fw-bold'})
    if request.method == 'POST':
        pform = RPKeywordsForm(request.form)
        if pform.validate_on_submit():
            try:
                papid = ObjectId(pid)#session["paper_id"]
                pap = Paper.objects(id=papid).first()
                # Max limit of keywords
                if pap.rp.keywords.count() > current_app.config["MAXKEYWORDS"]:
                    return render_template_string("""
                        {% extends "base.html" %} {% block content %}
                            <h3>You can not add more keyword max limit has reached {{current_app.config["MAXKEYWORDS"]}}  </h3>
                        {% endblock %}
                    """)
                #check duplicate keywords
                for k in pap.rp.keywords:
                    if k.desc == pform.desc.data:
                        return render_template_string("""
                            {% extends "base.html" %} {% block content %}
                                <h3>Keyworld {{keyword}} is in list </h3>
                            {% endblock %}
                                """,keyword=pform.desc.data)
                if pform.link.data == '' or pform.link.data == None:
                    pap.rp.keywords.append(LinkDesc(pk = get_a_uuid()
                                                    ,desc=pform.desc.data))
                else:
                    pap.rp.keywords.append(LinkDesc(pk = get_a_uuid()
                                                    ,desc=pform.desc.data
                                                    ,link=pform.link.data))
                pap.save()
                #print('saved')
                return redirect(request.form.get('next'))
            except ValidationError as e:
                flash(e.message)
                flash(e.field_name)
                flash(e.errors)
                return render_template_string(errormessages)

@papers.route('/keyword/<pid>/rp/<pid1>', methods=['GET', 'POST']) # desc is pid1
@login_required
def editkeyword(pid,pid1):
    if Is_target_useris_author_of_sessionpaper() == False:
        return render_template_string("""
                        {% extends "base.html" %} {% block content %}
                            <h3>You are not author of this paper. Select another paper  </h3>
                        {% endblock %}
                    """)
    if request.method == 'GET':
        #print(request.referrer)
        pform = RPKeywordsForm()
        papid = ObjectId(pid)#session["paper_id"]
        pap = Paper.objects(id=papid).first()
        kwrd = pap.rp.keywords.get(desc=pid1)
        pform.desc.data = kwrd.desc
        pform.link.data = kwrd.link
        return render_template_string(edit_create_view_paper, form=pform, fn_target='papers.editkeyword'
                                      , pid=pid, pid1=pid1, pid2=None, pid3=None
                                      , back = request.referrer
                                      , kwargs = {'class_':'form-control fw-bold'})
    if request.method == 'POST':
        pform = RPKeywordsForm(request.form)
        if pform.validate_on_submit():
            try:
                papid = ObjectId(pid)#session["paper_id"]
                pap = Paper.objects(id=papid).first()
                # no change in keyword
                if pid1 == pform.desc.data: 
                    if pform.link.data == None:
                        return redirect(request.form.get('next'))
                    if pform.link.data == '':
                        return redirect(request.form.get('next'))
                    dl = pap.rp.keywords.get(desc=pid1).link
                    if hasattr(dl, 'link'):
                        pap.rp.keywords.filter(desc=pid1).update(link=pform.link.data)
                        print(dl.link)
                        print(pid1)
                    else:
                        pap.rp.keywords.filter(desc=pid1).delete()
                        pap.rp.keywords.append(LinkDesc(pk = get_a_uuid()
                                                        , desc=pform.desc.data
                                                        , link='http://www.dtu.ac.in'))
                        print("saved delete")
                        pap.save()
                    
                    return redirect(request.form.get('next'))

                #check duplicate keywords due to update with exsiting keyword
                for k in pap.rp.keywords:
                    if k.desc == pform.desc.data:
                        return render_template_string("""
                            {% extends "base.html" %} {% block content %}
                                <h3>Keyworld {{keyword}} is in list </h3>
                            {% endblock %}
                                """,keyword=pform.desc.data)
                if pform.link.data == '' or pform.link.data == None:
                    pap.rp.keywords.filter(desc=pid1).update(desc=pform.desc.data,link=None)
                    #pap.rp.keywords.get(desc=pid1).update(desc=pform.desc.data)
                else:
                    pap.rp.keywords.filter(desc=pid1).update(desc=pform.desc.data,link=pform.link.data)
                    #pap.rp.keywords.get(desc=pid1).update(desc=pform.desc.data,link=pform.link.data)
                
                pap.save()
                return redirect(request.form.get('next'))
            except ValidationError as e:
                flash(e.message)
                flash(e.field_name)
                flash(e.errors)
                return render_template_string(errormessages)

# @papers.route('/keyword/<pid>/rp', methods=['GET', 'POST'])
# @login_required
# def deletekeyword(pid):


# #############################################################################################################
# ########################################################################################################

# ################################## /PaperRefFile   /keyword<pid>/rp/<kid>   ########################
# reffiles_view = """
#     {% from 'form_macros.html' import render_paperfileuplodedl2,render_linkdescl2 %}
#     {% extends "base.html" %} {% block content %}
#     <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
#     <input type="hidden" name="next" value={{backview}} />
#     <a href="{{url_for(fn_create, id = id )}}">(New Reference)</a>
#         {% for rf in reffiles %}
#             <div class="{{ kwargs.pop('class_', '') }}">
#                 <a href={{rf.doi}}><h1>{{rf.title}}</h1></a>
#                 <a href="{{url_for(fn_edit, id = id, id1 = rf.pk )}}">(Edit)</a>
#                 (<button type="button" class="btn btn-info btn-sm" data-bs-toggle="modal" data-bs-target="#delete{{rf.pk}}">Delete</button>)
#                 <a href="{{url_for(fn_paperfileuplodedcreate, id = id, id1 = 'reffiles', id2 = rf.pk, id3 = 'fileup' )}}">(Upload New File)</a>
#                 <a href="{{url_for(fn_linkdesccreate, id = id, id1 = 'reffiles', id2 = rf.pk, id3 = 'links' )}}">(Online Links for reference)</a></br>
#                 <h5>Artical Type :  {{rf.articaltype}}</h5>
#                 <h5>Year :  {{rf.year}}</h5>
#                 <h5>Digital Object Identifie :  {{rf.doi}}</h5>
#                 <h5>Bibtex :  {{rf.bibtex}}</h5>
#                 <h5>Description :  {{rf.desc}}</h5>
#                 {{render_paperfileuplodedl2(rf.fileup, id, 'reffiles', rf.pk, 'fileup','/reffiles', kwargs)}}
#                 {{render_linkdescl2(rf.links, id, 'reffiles', rf.pk, 'links', '/reffiles', kwargs)}}
#             </div>
#         {% endfor %}
#         {% for rf in reffiles %}
#             <div class="modal fade" id="delete{{rf.pk}}" tabindex="-1" aria-labelledby="deletelabel" aria-hidden="true" role="dialog">
#                 <div class="modal-dialog modal-dialog-centered">
#                     <div class="modal-content">
#                         <div class="modal-header">
#                             <h5 class="modal-title" id="deletelabel">Alert</h5>
#                             <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
#                         </div>
#                         <div class="modal-body">
#                             <form action="{{ url_for(fn_delete, id = id, id1 = rf.pk) }}" method="POST">
#                                 <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
#                                 <div class="form-group">
#                                     <div>
#                                         <button type="submit" class="btn btn-success">
#                                             Delete
#                                         </button>
#                                     </div>
#                                 </div>
#                             </form>
#                         </div>
#                         <div class="mb-3">
#                             <div class="modal-footer">
#                                 <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
#                                     Close
#                                 </button>
#                             </div>
#                         </div>
#                     </div>
#                 </div>
#             </div>
#         {% endfor %}
#     {% endblock %}
#     """
# @papers.route('/reffiles', methods=['GET', 'POST'])
# @login_required
# def reffiles():
#     #user = User.objects(username=current_user.username).first()
#     #tid = session["target_id"]
#     #user = User.objects(id=tid).first()
#     #for pid in user.papers
#     if session["paper_id"] is None:
#         return redirect(url_for('papers.paperselect'))
#     pid = session["paper_id"]  #paper in session (selected)
#     #pid = '642e69405945f32375891bfe'
#     pap = Paper.objects(id=pid).first()
#     if request.method == 'GET':
#         if hasattr(pap, 'objects') == True:
#             ######## IndustryCollaboration ##############
#             # #########  <a href="{{url_for('users.indcolabedit', key_str = item.name)}}" >Edit</a> ; def __str__(self): return self.name  ;  It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
#             return render_template_string(reffiles_view #, fn_target='users.department' ## uform=FlaskForm()
#                                       ,fn_create = 'papers.reffilescreate', fn_edit = 'papers.reffilesedit' , fn_delete = 'papers.reffilesdelete'
#                                       ,fn_paperfileuplodedcreate = 'papers.fileuplodedcreatel2', fn_paperfileuplodededit = 'users.fileuplodededitl2' , fn_paperfileuplodeddelete = 'users.fileuplodeddeletel2'
#                                       ,fn_linkdesccreate = 'papers.linkdesccreatel2', fn_linkdescedit = 'papers.linkdesceditl2' , fn_linkdescdelete = 'papers.linkdescdeletel2'
#                                       ,backview = request.referrer
#                                       ,reffiles = pap.reffiles, id = pap.id
#                                       ,kwargs = {'class_':'form-control fw-bold'})

# @papers.route('/reffiles_dict', methods=['GET', 'POST'])
# @login_required
# def reffiles_dict():
#     #user = User.objects(username=current_user.username).first()
#     #tid = session["target_id"]
#     #user = User.objects(id=tid).first()
#     #for pid in user.papers
#     pid = session["paper_id"]  #paper in session (selected)
#     #pid = '642e69405945f32375891bfe'
#     pap = Paper.objects(id=pid).first()
#     if request.method == 'GET':
#         if hasattr(pap, 'objects') == True:
#             ######## IndustryCollaboration ##############
#             # #########  <a href="{{url_for('users.indcolabedit', key_str = item.name)}}" >Edit</a> ; def __str__(self): return self.name  ;  It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
#             details_dict_view_list = []
#             for p in pap.reffiles:
#                 details_dict_view_list.append(p.__dict__())
#             #print(details_dict_view_list)
#             return render_template_string(details_dict_listview_paper
#                                           , fn_target_new = 'papers.reffilescreate', fn_target_edit = 'papers.reffilesedit', fn_target_delete = 'papers.reffilesdelete' 
#                                           , back = request.referrer
#                                           , id = pap.id, detailitemslist = details_dict_view_list, tablehead = 'Paper Ref File', tableheadrvalue = 'Information'
#                                           , kwargs = {'class_':'form-control fw-bold'})

# @papers.route('/reffilescreate/<id>', methods=['GET', 'POST'])  # create
# @login_required
# def reffilescreate(id):
#     #user = User.objects(username=current_user.username).first()
#     #id = session["target_id"]
#     pap = Paper.objects(id=id).first()
#     if request.method == 'GET':
#         uform = PaperRefFileForm()
#         if hasattr(pap, 'objects') == True:
#             return render_template_string(edit_create_view_id, form=uform, fn_target='papers.reffilescreate'
#                                           , id=id, id1=None, id2=None, id3=None, id4=None, id5=None #key_str=None
#                                           , back = request.referrer
#                                           , kwargs = {'class_':'form-control fw-bold'})
#     if request.method == 'POST':
#         uform = PaperRefFileForm(request.form)
#         if uform.validate_on_submit():
#             ######## PaperRefFile #############
#             if hasattr(pap, 'objects') == True: 
#                 try:
#                     if pap.reffiles.filter(title=uform.title.data
#                                         ).count() > 0:
#                         return render_template_string("""
#                                     {% extends "base.html" %} {% block content %}
#                                         <h3>PaperRefFile {{name}} is in PaperRefFile List </h3>
#                                     {% endblock %}
#                                         """,name=uform.title.data)
#                     p = PaperRefFile(pk = get_a_uuid()
#                                         , title=uform.title.data
#                                         , articaltype=uform.articaltype.data
#                                         , year=uform.year.data
#                                         , doi=uform.doi.data
#                                         , bibtext=uform.bibtext.data
#                                         , desc=uform.desc.data
#                                         )
#                     pap.reffiles.append(p)
#                     pap.save()
#                     return redirect(request.form.get('next'))
#                 except DoesNotExist as e:
#                     flash(id + ' Doest Not Exist')
#                     return render_template_string(errormessages)
#                 except ValidationError as e:
#                     flash(e.message)
#                     flash(e.field_name)
#                     flash(e.errors)
#                     return render_template_string(errormessages)
                
# @papers.route('/reffilesedit/<id>/<id1>', methods=['GET', 'POST'])
# @login_required
# def reffilesedit(id,id1):
#     #user = User.objects(username=current_user.username).first()
#     #tid = session["target_id"]
#     pap = Paper.objects(id=id).first()
#     print(pap.id)
#     if request.method == 'GET':
#         uform = PaperRefFileForm()
#         if hasattr(pap, 'objects') == True:
#             ######## sponsoredprojects ##############
#             p = pap.reffiles.get(pk = id1)
#             #print(p.__dict__())
#             uform.title.data=p.title
#             uform.articaltype.data=p.articaltype
#             uform.year.data=p.year
#             uform.doi.data=p.doi
#             uform.bibtext.data=p.bibtext
#             uform.desc.data=p.desc
#         return render_template_string(edit_create_view_id, form=uform, fn_target='papers.reffilesedit'
#                                     , id=id, id1=id1, id2=None, id3=None, id4=None, id5=None #key_str=key_str
#                                     , back = request.referrer
#                                     , kwargs = {'class_':'form-control fw-bold'})
#         # return render_template('/user/sponsoredprojects.html', form=usersponsoredprojectsform)
#     if request.method == 'POST':
#         uform = PaperRefFileForm(request.form)
#         if uform.validate_on_submit():
#             ######## sponsoredprojects #############
#             if hasattr(pap, 'objects') == True:
#                 try:
#                     if pap.reffiles.filter(title=uform.title.data
#                                         ).count() > 0:
#                         return render_template_string("""
#                                     {% extends "base.html" %} {% block content %}
#                                         <h3>PaperRefFile {{name}} is in PaperRefFile List </h3>
#                                     {% endblock %}
#                                         """,name=uform.title.data)
                    
#                     p = pap.reffiles.get(pk = id1)
#                     p.title=uform.title.data
#                     p.articaltype=uform.articaltype.data
#                     p.year=uform.year.data
#                     p.doi=uform.doi.data
#                     p.bibtext=uform.bibtext.data
#                     p.desc=uform.desc.data
#                     pap.save()
#                     return redirect(request.form.get('next'))
#                 except DoesNotExist as e:
#                     flash(id + ' Doest Not Exist')
#                     return render_template_string(errormessages)
#                 except ValidationError as e:
#                     flash(e.message)
#                     flash(e.field_name)
#                     flash(e.errors)
#                     return render_template_string(errormessages)
#                         #print('Contact Saved')
#                 # print(jsonify(user).get_json())
                
#                 #return render_template_string(details_dict_listview, fn_target_edit = 'users.sponsoredprojectsedit', fn_target_delete = 'users.sponsoredprojectsdelete', fn_target_new = 'users.sponsoredprojectscreate', detailitemslist=details_dict_view_list, tablehead = 'Sponsored Project', tableheadrvalue = 'Information')
                
# @papers.route('/reffilesdelete/<id>/<id1>', methods=['POST'])  # delete
# @login_required
# def reffilesdelete(id,id1):
#     #user = User.objects(username=current_user.username).first()
#     #tid = session["target_id"]
#     if request.method == 'POST':
#         pap = Paper.objects(id=id).first()
#         if hasattr(pap, 'objects') == True:
#             try:
#                 p = pap.reffiles.get(pk = id1)
#                 pap.reffiles.remove(p)
#                 pap.save()
#                 return redirect('/reffiles')

#             except DoesNotExist as e:
#                 flash(id + ' Doest Not Exist')
#                 return render_template_string(errormessages)
#             except ValidationError as e:
#                 flash(e.message)
#                 flash(e.field_name)
#                 flash(e.errors)
#                 return render_template_string(errormessages)
                
