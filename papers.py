import os
from flask import Blueprint, session, request, current_app, send_from_directory, render_template_string, redirect, url_for, flash
#from wtforms.validators import URL #InputRequired, Length
from mongoengine.errors import ValidationError, DoesNotExist#, NotUniqueError, NameError, ValueError
from mongoengine import URLField
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from bson.objectid import ObjectId
#from bson import ObjectId
from .users import Iscurrentuseradmin, errormessages, User, edit_create_view_id, details_dict_view, details_dict_listview
from .models import AllocatePapertoUserForm,DeallocatePapertoUserForm, PaperNewForm,PaperEditForm, PaperDeleteForm, PaperFileUplodedForm, PaperRefFileForm, PaperSelectForm, LinkDescForm
from .models import ResearchProblemForm, RPKeywordsForm, PaperPersonForm,PaperPersonFormEdit, PaperDiscussionBoardCommentForm, PaperSubmittedinJournalForm, PaperSubmittedinConferenceForm, RPAplicationsForm, RPJournals_ConfForm, RPCode_LinksForm, RPDataSets_linksForm, RPPeoplesForm, RPArticalsForm, RPResouresForm, RPSocialmediaForm
from . import Paper, get_a_uuid, PaperPerson, ResearchProblem, FileUploded, LinkDesc,  PaperRefFile, PaperDiscussionBoardComment, PaperSubmittedinJournal, PaperSubmittedinConference
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

#############################################################  Route/controller at level 1 for (embeddeddocumentlistfield(FileUploded),View(render_paperfileuplodedl1(create,edit,delete)))
PaperFileUplodedView = """
                {% from 'form_macros.html' import edit_create_view %}
                {% extends "base.html" %} {% block content %}
                (<button type="button" class="btn btn-sm btn-link" data-bs-toggle="modal" data-bs-target="#fileup">File Upload</button>)
                {{edit_create_view(form = form, fn_target = fn_target, kwargs = kwargs, backurl = backurl, id=id, id1=id1, id2=id2, id3=id3, id4=id4, id5=id5, enctypevalue = "multipart/form-data")}}
                <div class="modal fade" id="fileup" tabindex="-1" aria-labelledby="deletelabel" aria-hidden="true" role="dialog">
                    <div class="modal-dialog modal-dialog-centered">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" id="deletelabel">Alert</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                <form action="{{ url_for(fn_target, id = id, id1 = id1, id2 = id2, id3 = id3) }}" method="POST" enctype="multipart/form-data" class="was-validated">
                                    <input type="hidden" class="form-control" name="csrf_token" value="{{ csrf_token() }}"/>
                                    <input type="hidden" class="form-control col-sm-2 col-form-label ms-5" name="next" value={{backurl}} />
                                    <div class="mb-3">
                                        <label for="fileupdescinput" class="form-label">File Desciption</label>
                                        <textarea name="desc" id="fileupdescinput" required class="form-control"></textarea>
                                        <div class="valid-feedback">Valid.</div>
                                        <div class="invalid-feedback">Please fill out this field.</div>
                                    </div>
                                    <div class="mb-3">
                                        <label for="fileupinput" class="form-label">File:</label>
                                        <input type="file" name="file" id="fileupinput" required class="form-control"><br>
                                        <div class="valid-feedback">Valid.</div>
                                        <div class="invalid-feedback">Please fill out this field.</div>
                                    </div>
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
### url/controller for view(render_paperfileuplodedl1 - > create)
### id -> paper_id, id1 -> property name (eg published) of list in Document paper of type FileUploded , id2 -> pk
@papers.route('/paperfileuplodedl1/<id>/<id1>', methods=['GET', 'POST'])  
@login_required
def fileuplodedcreatel1(id,id1):
    if request.method == 'GET':
        uform = PaperFileUplodedForm()
        return render_template_string(PaperFileUplodedView, form=uform, fn_target='papers.fileuplodedcreatel2'
                                      , id=id, id1=id1, id2=None, id3=None, id4=None, id5=None
                                      , backurl = request.referrer
                                      , kwargs = {'class_':'form-control fw-bold'})
    if request.method == 'POST':
        uform = PaperFileUplodedForm(request.form)
        path = 'static/images/'
        mimetype = 'application/pdf'
        try:
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
                l1_list = getattr(pap,str(id1)) # l1 = property name (published) of list in Document paper of type FileUploded ... etc
                pfu = FileUploded(
                    pk = get_a_uuid()
                    ,filename = filename
                    ,path = path
                    ,ext = filename.rsplit('.', 1)[1].lower()
                    ,mimetype = mimetype
                    ,desc = request.form.get("desc")
                    )
                l1_list.append(pfu)
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
        
@papers.route('/fileuplodededitl1/<id>/<id1>/<id2>', methods=['POST'])  
@login_required
def fileuplodededitl1(id,id1,id2):
    if request.method == 'POST':
        try:
            pap = Paper.objects(id=id).first() # Target user id
            
            l1_list = getattr(pap,str(id1)) # l1 = property name (published) of list in Document paper of type FileUploded ... etc
            
            l1_list_object = l1_list.get(pk = id2) # single object (of type FileUploded) in list of Document  ... etc
            
            l1_list_object.desc = request.form.get("desc")
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

@papers.route('/fileuplodeddeletel1/<id>/<id1>/<id2>', methods=['POST'])  
@login_required
def fileuplodeddeletel1(id,id1,id2):
    if request.method == 'POST':
        try:
            pap = Paper.objects(id=id).first() # Target user id
            
            l1_list = getattr(pap,str(id1)) # l1 = property name (published) of list in Document paper of type FileUploded ... etc
            
            l1_list_object = l1_list.get(pk = id2) # single object (of type FileUploded) in list of Document  ... etc
            
            file_to_remove = os.path.join(l1_list_object.path, l1_list_object.filename)
            l1_list.remove(l1_list_object)
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

#############################################################  Route/controller at level 1 for (embeddeddocumentlistfield(FileUploded),View(render_paperfileuplodedl1(create,edit,delete)))


#############################################################  Route/controller at level 2 for (embeddeddocumentlistfield(FileUploded),View(render_paperfileuplodedl2(create,edit,delete)))
### url/controller for view(render_paperfileuplodedl2 - > create)
# FileUploded at level 2 list
# paperid at level 0 /class property or attribute name(id1) at level 1 / attribute name at level 2 / value of arribute at level 2
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
        #uform = PaperFileUplodedForm(request.form)
        #print(uform.desc.data)
        path = 'static/images/'
        mimetype = 'application/pdf'
        try:
            #check duplicate PaperRefFile
            #ad_duplicate = l1.filter(addtype = uform.contact.data['addtype'])
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                print('No file part')
                return redirect(request.url)
            else:
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
                    print(f"l1={l1}")
                    l2 = l1.get(pk = id2) # PaperRefFile ... etc
                    print(f"l1={l2}")
                    l3 = getattr(l2,str(id3))
                    print(f"l1={l3}")
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
                (<button type="button" class="btn btn-link btn-sm" data-bs-toggle="modal" data-bs-target="#linkdesc">Link/Url</button>)
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

#############################################################  Route/controller at level 1 for (embeddeddocumentlistfield(LinkDesc),View(render_linkdescl1(create,edit,delete)))
### url/controller for view(render_linkdescl2 - > create)
@papers.route('/linkdesccreatel1/<id>/<id1>', methods=['POST'])  
@login_required
def linkdesccreatel1(id,id1):
     #id1 is name of property at L1 'links' # L1 LinkDesc
     #id2 is pk of list links
     if request.method == 'POST':
        uform = LinkDescForm(request.form)
        try:
            pap = Paper.objects(id=id).first()
            l1_list = getattr(pap,str(id1)) # l1 = property name of list in Document paper of type LinkDiesc ... etc
            #l2 = l1_list.get(pk = id2) # single object (of type LinkDesc) in list of Document  ... etc
            #check duplicate PaperRefFile
            if l1_list.filter(link = uform.link.data).count() > 0:
                return render_template_string("""
                        {% extends "base.html" %} {% block content %}
                            <h3>Link {{link}} is in list </h3>
                        {% endblock %}
                            """,link=uform.link.data)
            #ad_duplicate = l1.filter(addtype = uform.contact.data['addtype'])
            ld = LinkDesc(pk = get_a_uuid()
                    ,link = request.form.get("link") #uform.link.data
                    ,desc = request.form.get("desc") #uform.desc.data
                    )
            l1_list.append(ld)
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

@papers.route('/linkdesceditl1/<id>/<id1>/<id2>', methods=['POST'])  
@login_required
def linkdesceditl1(id,id1,id2):
     #id1 is name of property at L1 'links' # L1 LinkDesc
     #id2 is pk of list links
     if request.method == 'POST':
        #uform = UserContactsForm(request.form)
        try:
            pap = Paper.objects(id=id).first() # Target user id
            
            # id1 for level 1 property(List) e.g. list of contacts/faculty ... etc
            # it will return List of property
            l1_list = getattr(pap,str(id1)) # l1 = property name of list in Document paper of type LinkDiesc ... etc
            
            l1_list_object = l1_list.get(pk = id2) # single object (of type LinkDesc) in list of Document  ... etc
            
            l1_list_object.link = request.form.get("link")
            l1_list_object.desc = request.form.get("desc")
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
        
@papers.route('/linkdesccreatel1/<id>/<id1>/<id2>', methods=['POST'])  
@login_required
def linkdescdeletel1(id,id1,id2):
     #id1 is name of property at L1 'links' # L1 LinkDesc
     #id2 is pk of list links
     if request.method == 'POST':
        #uform = UserContactsForm(request.form)
        try:
            pap = Paper.objects(id=id).first() # Target user id
            
            l1_list = getattr(pap,str(id1)) # l1 = property name of list in Document paper of type LinkDiesc ... etc
            
            l1_list_object = l1_list.get(pk = id2) # PaperRefFile ... etc
            
            l1_list.remove(l1_list_object)
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
#############################################################  Route/controller at level 1 for (embeddeddocumentlistfield(LinkDesc),View(render_linkdescl1(create,edit,delete)))

#############################################################  Route/controller at level 2 for (embeddeddocumentlistfield(LinkDesc),View(render_linkdescl2(create,edit,delete)))
@papers.route('/linkdesccreatel2/<id>/<id1>/<id2>/<id3>', methods=['GET', 'POST'])  
@login_required
def linkdesccreatel2_old(id,id1,id2,id3):
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
                    ,link = request.form.get("link") #uform.link.data
                    ,desc = request.form.get("desc") #uform.desc.data
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

### url/controller for view(render_linkdescl2 - > create)
@papers.route('/linkdesccreatel2/<id>/<id1>/<id2>/<id3>', methods=['POST'])  
@login_required
def linkdesccreatel2(id,id1,id2,id3):
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
                    ,link = request.form.get("link") #uform.link.data
                    ,desc = request.form.get("desc") #uform.desc.data
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

### url/controller for view(render_linkdescl2 - > edit)
@papers.route('/linkdesceditl2/<id>/<id1>/<id2>/<id3>/<id4>', methods=['POST'])
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

### url/controller for view(render_linkdescl2 - > delete)
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

############################################################################ Route/controller at level 2 for (embeddeddocumentlistfield(LinkDesc),View(render_linkdescl2(create,edit,delete)))

#############################################################  Route/controller at level 3 for (embeddeddocumentlistfield(LinkDesc),View(render_linkdescl3(create,edit,delete)))

#############################################################  Route/controller at level 3 for (embeddeddocumentlistfield(LinkDesc),View(render_linkdescl3(create,edit,delete)))

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
                                    (<button type="button" class="btn btn-sm btn-link" data-bs-toggle="modal" data-bs-target="#delete{{value}}">Delete</button>) 
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

########################################################################################################
@papers.route('/paper', methods=['GET', 'POST'])
@login_required
def paper():
     if request.method == 'GET':
        if session['paper_id'] is None:
             return redirect(url_for('papers.paperselect'))
        #print(session["paper_id"])
        pid = session["paper_id"]
        pap = Paper.objects(id=pid).first()
        #print(pap.__dict__())
        return render_template_string("""{% from 'form_macros.html' import render_paperfileuplodedl1, render_flashed_messages %}
                        {% extends "base.html" %} {% block content %}
                        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
                            <a href="{{url_for('papers.editpaper', id = id)}}"><h1>Paper Title : {{paper.title}}  </h1></a>
                            <h2>Status : {{paper.status}}</h2><br/>
                            <a href="{{url_for('papers.rp', id = id)}}"><h5>Research Problem   </h5></a>
                            <a href="{{url_for('papers.addkeyword', pid = id)}}"><h5>Add keyword   </h5></a>
                            {% for kword in paper.rp.keywords %}
                                {% if kword.link == '' or kword.link == None%}
                                    <h4>{{kword.desc}} </h4> <a href="{{url_for('papers.editkeyword', pid = paper.id, pid1 = kword.desc)}}"> Edit </a>
                                {% else %}
                                    <a href={{kword.link}}><h4>{{kword.desc}}   </h4></a>
                                {% endif %}
                            {% endfor %}
                            {{render_paperfileuplodedl1(paper.bibtext, id, 'bibtext', '/paper', kwargs)}}
                            {{render_paperfileuplodedl1(paper.ownwork, id, 'ownwork', '/paper', kwargs)}}
                            {{render_paperfileuplodedl1(paper.litrature, id, 'litrature', '/paper', kwargs)}}
                            {{render_paperfileuplodedl1(paper.result, id, 'result', '/paper', kwargs)}}
                            {{render_paperfileuplodedl1(paper.futurescope, id, 'futurescope', '/paper', kwargs)}}
                            {{render_paperfileuplodedl1(paper.intro, id, 'intro', '/paper', kwargs)}}
                            {{render_paperfileuplodedl1(paper.abstract, id, 'abstract', '/paper', kwargs)}}
                            {{render_paperfileuplodedl1(paper.manuscript, id, 'manuscript', '/paper', kwargs)}}
                            {{render_paperfileuplodedl1(paper.acceptance, id, 'acceptance', '/paper', kwargs)}}
                            {{render_paperfileuplodedl1(paper.cameraready, id, 'cameraready', '/paper', kwargs)}}
                            {{render_paperfileuplodedl1(paper.published, id, 'published', '/paper', kwargs)}}
                        {% endblock %}
                    """               
                    ,backview = request.referrer
					,paper=pap, id = pap.id
					,kwargs = {'class_':'form-control row mb-1 col-sm-2 col-form-label ms-1'}
                    )
#########################################################################################################
################################  select target paper from user papers list (stpfupl) ###########################
@papers.route('/printpaper', methods=['GET', 'POST'])
@login_required
def printpaper():
    if request.method == 'GET':
        #print(session["paper_id"])
        pid = session["paper_id"]
        pap = Paper.objects(id=pid).first()
        #print(pap.__dict__())
        return render_template_string("""{% from 'form_macros.html' import render_paperfileuplodedl1, render_flashed_messages %}
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
    if len(user.papers) <= 0:
         return render_template_string("""{% extends "base.html" %} {% block content %}<h3>User doest have any Paper in his list </h3>{% endblock %}""")
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

@papers.route('/deletepaper/<id>', methods=['GET', 'POST'])
@login_required
def deletepaper(id):
    if Iscurrentuseradmin() != True:
        flash('You are not Admin')
        return render_template_string(errormessages,messages='You are not Admin')
    else:
        if request.method == 'GET':
            pform = PaperDeleteForm()
            #print('Paper created')
            return render_template_string(edit_create_view_paper, form=pform, fn_target='papers.deletepaper'
                                      , pid=id, pid1=None, pid2=None, pid3=None
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

@papers.route('/editpaper/<id>', methods=['GET', 'POST'])
@login_required
def editpaper(id): # PaperEditForm
    if Is_target_useris_author_of_sessionpaper() == False:
        return render_template_string("""
                        {% extends "base.html" %} {% block content %}
                            <h3>You are not author of this paper. Select another paper  </h3>
                        {% endblock %}
                    """)
    if request.method == 'GET':
        #print(request.referrer)
        pform = PaperEditForm()
        papid = ObjectId(id)#session["paper_id"]
        pap = Paper.objects(id=papid).first()
        pform.title.data = pap.title
        pform.status.data = pap.status
        return render_template_string(edit_create_view_paper, form=pform, fn_target='papers.editpaper'
                                      , pid=id, pid1=None, pid2=None, pid3=None
                                      , back = request.referrer
                                      , kwargs = {'class_':'form-control fw-bold'})
    if request.method == 'POST':
        pform = PaperEditForm(request.form)
        if pform.validate_on_submit():
            try:
                papid = ObjectId(id)#session["paper_id"]
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

#################################################################################### Module for discussionboard#############################################
#################################################################################### View HTML for discussionboard
discussionboard_jinja2 = """{% from 'form_macros.html' import render_linkdescl2, render_paperfileuplodedl2, render_flashed_messages %}

        	{% extends "base.html" %} {% block content %}
        	<input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
        	<input type="hidden" name="next" value={{backview}} />
        	{{render_flashed_messages()}}
            <div class="col-sm-4">discussionboard<button type="button" class="btn btn-sm btn-link" data-bs-toggle="modal" data-bs-target="#create_discussionboard">(New Paper Discussion Board Comment Form) </button>
        	{% for pdbcobj in pdbcobjlist %}
            		<div class="{{ kwargs.get('class_', '') }}">
            
		<div><h5>{{pdbcobj.desc}}</h5>
        		
        		</div>
		
            		</div>
            
		
        	{% endfor %}
            <div class="modal fade" id="create_discussionboard" tabindex="-1" aria-labelledby="createlabel" aria-hidden="true" role="dialog">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="createlabel">Alert</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <form action="{{ url_for('papers.discussionboardcommentcreate', id = id ) }}" method="POST" class="was-validated">
                            <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
                            <div class="mb-3">
                                <label for="discussionboardcomment" class="form-label">Post New Comment</label>
                                <textarea name="desc" id="discussionboardcomment" required class="form-control"></textarea>
                                <div class="valid-feedback">Valid.</div>
                                <div class="invalid-feedback">Please fill out this field.</div>
                            </div>
                            <div class="form-group">
                                <div>
                                    <button type="submit" class="btn btn-success">
                                        Post
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
#################################################################################### View Route for discussionboard
@papers.route('/discussionboard', methods=['GET'])
@papers.route('/discussionboard/<id>', methods=['GET'])
@login_required
def discussionboard(id = None):
	if session['paper_id'] is None:
		return redirect(url_for('papers.paperselect'))
	pap = Paper.objects(id=session['paper_id'] ).first()
	if request.method == 'GET':
		if hasattr(pap, 'objects') == True:
			return render_template_string(discussionboard_jinja2
						,backview = request.referrer
						,pdbcobjlist = pap.discussionboard, id = pap.id
						,kwargs = {'class_':'form-control row mb-1 col-sm-2 col-form-label ms-1'})
		else:
			return render_template_string("""{% extends "base.html" %} {% block content %}<h3>Paper Discussion Board Comments List is empty. </h3>{% endblock %}""")
#################################################################################### Create Route for discussionboard
@papers.route('/discussionboardcommentcreate/<id>', methods=['GET', 'POST'])
@login_required
def discussionboardcommentcreate(id):
	if (id):
		pap=Paper.objects(id=id).first()
	else:
		return render_template_string("""{% extends "base.html" %} {% block content %}<h3>Paper Discussion Board Comments id not found empty. </h3>{% endblock %}""")
	if request.method == 'GET':
		uform = PaperDiscussionBoardCommentForm()
		if hasattr(pap, 'objects') == True:
			return render_template_string(edit_create_view_id, form=uform, fn_target='papers.discussionboardcreate'
						, id=id, id1=None, id2=None, id3=None, id4=None, id5=None 
						, back = request.referrer
						, kwargs = {'class_':'form-control row mb-1 col-sm-2 col-form-label ms-1'})
	if request.method == 'POST':
		uform = PaperDiscussionBoardCommentForm(request.form)
		if uform.validate_on_submit():
			if hasattr(pap, 'objects') == True:
				try:
					discussionboard_tmp = PaperDiscussionBoardComment(name = 'Kapil', desc = uform.desc.data)
					pap.discussionboard.append(discussionboard_tmp)
					pap.discussionboard.save()
					return redirect('/discussionboard')
				except DoesNotExist as e:
					flash(id + ' Doest Not Exist')
					return render_template_string(errormessages)
				except ValidationError as e:
					flash(e.message)
					flash(e.field_name)
					flash(e.errors)
					return render_template_string(errormessages,messages=e.message)
#################################################################################### Module for discussionboard#############################################
#################################################################################### Module for discussionboard#############################################






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


#############################################################################################################
########################################################################################################

################################## /PaperRefFile   /keyword<pid>/rp/<kid>   ########################
# reffiles_view = """
#     {% from 'form_macros.html' import render_paperfileuplodedl2,render_linkdescl2 %}
#     {% extends "base.html" %} {% block content %}
#     <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
#     <input type="hidden" name="next" value={{backview}} />
#     <a href="{{url_for(fn_create, id = id )}}">(New Reference)</a>
#         {% for rf in reffiles %}
#             <div class="{{ kwargs.get('class_', '') }}">
#                 <a href={{rf.doi}}><h1>{{rf.title}}</h1></a>
#                 <a href="{{url_for(fn_edit, id = id, id1 = rf.pk )}}">(Edit)</a>
#                 (<button type="button" class="btn btn-link btn-sm" data-bs-toggle="modal" data-bs-target="#delete{{rf.pk}}">Delete</button>)
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
                





# # # # # #################################################################################### Module for rp#############################################
# # # # # #################################################################################### View HTML for rp
# # # # # rp_jinja2 = """{% from 'form_macros.html' import render_linkdescl2 %}
# # # # #         	{% extends "base.html" %} {% block content %}
# # # # #         	<input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
# # # # #         	<input type="hidden" name="next" value={{backview}} />
# # # # #         	<a href="{{url_for('papers.rpcreate', id = id )}}">(New Research Problem)</a>
# # # # #         	{% for item in itemlist %}
# # # # #         		<div class="{{ kwargs.get('class_', '') }}">
# # # # # 		<h1>{{item.statment}}</h1>
# # # # #         		<a href="{{url_for('papers.rpedit', id = id, id1 = item.pk)}}">(Edit)</a>
# # # # #         		(<button type="button" class="btn btn-sm btn-link" data-bs-toggle="modal" data-bs-target="#delete{{item.pk}}">Delete</button>)
# # # # # 		<a href="{{url_for('papers.linkdesccreatel2', id = id, id1 = 'rp', id2 = item.pk, id3 = 'keywords')}}">(Add Keywords)</a>
# # # # # 		<a href="{{url_for('papers.linkdesccreatel2', id = id, id1 = 'rp', id2 = item.pk, id3 = 'area')}}">(Add Area)</a>
# # # # # 		<a href="{{url_for('papers.linkdesccreatel2', id = id, id1 = 'rp', id2 = item.pk, id3 = 'applications')}}">(Add Applications)</a>
# # # # # 		<a href="{{url_for('papers.linkdesccreatel2', id = id, id1 = 'rp', id2 = item.pk, id3 = 'journals_conf')}}">(Add Journals/Conferences)</a>
# # # # # 		<a href="{{url_for('papers.linkdesccreatel2', id = id, id1 = 'rp', id2 = item.pk, id3 = 'code_links')}}">(Add Source Code)</a>
# # # # # 		<a href="{{url_for('papers.linkdesccreatel2', id = id, id1 = 'rp', id2 = item.pk, id3 = 'datasets_links')}}">(Add Datasets)</a>
# # # # # 		<a href="{{url_for('papers.linkdesccreatel2', id = id, id1 = 'rp', id2 = item.pk, id3 = 'peoples')}}">(Add Peoples)</a>
# # # # # 		<a href="{{url_for('papers.linkdesccreatel2', id = id, id1 = 'rp', id2 = item.pk, id3 = 'articals')}}">(Add Articals)</a>
# # # # # 		<a href="{{url_for('papers.linkdesccreatel2', id = id, id1 = 'rp', id2 = item.pk, id3 = 'resoures')}}">(Add Resoures)</a>
# # # # # 		<a href="{{url_for('papers.linkdesccreatel2', id = id, id1 = 'rp', id2 = item.pk, id3 = 'sm')}}">(Add Social Media Handels)</a>
# # # # # 		<h5>Description : {{item.desc}}</h5>
		
# # # # # 		{{render_linkdescl2(item.keywords, id, 'rp', item.pk, 'keywords','/rp', kwargs)}}
# # # # # 		{{render_linkdescl2(item.area, id, 'rp', item.pk, 'area','/rp', kwargs)}}
# # # # # 		{{render_linkdescl2(item.applications, id, 'rp', item.pk, 'applications','/rp', kwargs)}}
# # # # # 		{{render_linkdescl2(item.journals_conf, id, 'rp', item.pk, 'journals_conf','/rp', kwargs)}}
# # # # # 		{{render_linkdescl2(item.code_links, id, 'rp', item.pk, 'code_links','/rp', kwargs)}}
# # # # # 		{{render_linkdescl2(item.datasets_links, id, 'rp', item.pk, 'datasets_links','/rp', kwargs)}}
# # # # # 		{{render_linkdescl2(item.peoples, id, 'rp', item.pk, 'peoples','/rp', kwargs)}}
# # # # # 		{{render_linkdescl2(item.articals, id, 'rp', item.pk, 'articals','/rp', kwargs)}}
# # # # # 		{{render_linkdescl2(item.resoures, id, 'rp', item.pk, 'resoures','/rp', kwargs)}}
# # # # # 		{{render_linkdescl2(item.sm, id, 'rp', item.pk, 'sm','/rp', kwargs)}}
# # # # # 		</div>
# # # # #         	{% endfor %}
# # # # #                 {% for item in itemlist %}
# # # # #                     <div class="modal fade" id="delete{{item.pk}}" tabindex="-1" aria-labelledby="deletelabel" aria-hidden="true" role="dialog">
# # # # #                         <div class="modal-dialog modal-dialog-centered">
# # # # #                             <div class="modal-content">
# # # # #                                 <div class="modal-header">
# # # # #                                     <h5 class="modal-title" id="deletelabel">Alert</h5>
# # # # #                                     <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
# # # # #                                 </div>
# # # # #                                 <div class="modal-body">
# # # # #                                     <form action="{{ url_for('papers.rpdelete', id = id, id1 = item.pk) }}" method="POST">
# # # # #                                         <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
# # # # #                                         <div class="form-group">
# # # # #                                             <div>
# # # # #                                                 <button type="submit" class="btn btn-success">
# # # # #                                                     Delete
# # # # #                                                 </button>
# # # # #                                             </div>
# # # # #                                         </div>
# # # # #                                     </form>
# # # # #                                 </div>
# # # # #                                 <div class="mb-3">
# # # # #                                     <div class="modal-footer">
# # # # #                                         <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
# # # # #                                             Close
# # # # #                                         </button>
# # # # #                                     </div>
# # # # #                                 </div>
# # # # #                             </div>
# # # # #                         </div>
# # # # #                     </div>
# # # # #                 {% endfor %}
# # # # #             {% endblock %}
# # # # #             """
# # # # # #################################################################################### View Route for rp
# # # # # @papers.route('/rp', methods=['GET'])
# # # # # @login_required
# # # # # def rp():
# # # # # 	if session['paper_id'] is None:
# # # # # 		return redirect(url_for('papers.paperselect'))
# # # # # 	pap = Paper.objects(id=session['paper_id'] ).first()
# # # # # 	if request.method == 'GET':
# # # # # 		if hasattr(pap, 'objects') == True:
# # # # # 			return render_template_string(rp_jinja2
# # # # # 						,backview = request.referrer
# # # # # 						,itemlist = pap.rp, id = pap.id
# # # # # 						,kwargs = {'class_':'form-control fw-bold'})
# # # # # 		else:
# # # # # 			return render_template_string("""{% extends "base.html" %} {% block content %}<h3>Research Problem List is empty. </h3>{% endblock %}""")
# # # # # #################################################################################### View Dictonary  for rp
# # # # # @papers.route('/rp_dict', methods=['GET'])
# # # # # @login_required
# # # # # def rp_dict():
# # # # # 	if session['paper_id'] is None:
# # # # # 		return redirect(url_for('papers.paperselect'))
# # # # # 	pap = Paper.objects(id=session['paper_id'] ).first()
# # # # # 	details_dict_view_list = []
# # # # # 	for p in pap.rp:
# # # # # 		details_dict_view_list.append(p.__dict__())
# # # # # 	return render_template_string(details_dict_listview
# # # # # 		, fn_target_new = 'papers.rpcreate', fn_target_edit = 'papers.rpedit', fn_target_delete = 'papers.rpdelete'
# # # # # 		, back = request.referrer
# # # # # 		, id = pap.id, detailitemslist = details_dict_view_list, tablehead = 'Field', tableheadrvalue = 'Information'
# # # # # 		, kwargs = {'class_':'form-control fw-bold'})
# # # # # #################################################################################### Create Route for rp
# # # # # @papers.route('/rpcreate/<id>', methods=['GET', 'POST'])
# # # # # @login_required
# # # # # def rpcreate(id):
# # # # # 	pap=Paper.objects(id=id).first()
# # # # # 	if request.method == 'GET':
# # # # # 		uform = ResearchProblemForm()
# # # # # 		if hasattr(pap, 'objects') == True:
# # # # # 			return render_template_string(edit_create_view_id, form=uform, fn_target='papers.rpcreate'
# # # # # 						, id=id, id1=None, id2=None, id3=None, id4=None, id5=None 
# # # # # 						, back = request.referrer
# # # # # 						, kwargs = {'class_':'form-control fw-bold'})
# # # # # 	if request.method == 'POST':
# # # # # 		uform = ResearchProblemForm(request.form)
# # # # # 		if uform.validate_on_submit():
# # # # # 			if hasattr(pap, 'objects') == True:
# # # # # 				try:
# # # # # 					if pap.rp.filter(statment=uform.statment.data).count() > 0:
# # # # # 						return render_template_string("""{% extends "base.html" %} {% block content %}<h3>'Problem Statment' is in List </h3>{% endblock %}""")
# # # # # 					rp_tmp = ResearchProblem(pk= get_a_uuid(),statment = uform.statment.data,desc = uform.desc.data)
# # # # # 					pap.rp.append(rp_tmp)
# # # # # 					pap.rp.save()
# # # # # 					return redirect(request.form.get('next'))
# # # # # 				except DoesNotExist as e:
# # # # # 					flash(id + ' Doest Not Exist')
# # # # # 					return render_template_string(errormessages)
# # # # # 				except ValidationError as e:
# # # # # 					flash(e.message)
# # # # # 					flash(e.field_name)
# # # # # 					flash(e.errors)
# # # # # 					return render_template_string(errormessages,messages=e.message)
# # # # # #################################################################################### Edit Route for rp
# # # # # @papers.route('/rpedit/<id>/<id1>', methods=['GET', 'POST'])
# # # # # @login_required
# # # # # def rpedit(id,id1):
# # # # # 	pap=Paper.objects(id=id).first()
# # # # # 	if request.method == 'GET':
# # # # # 		uform = ResearchProblemForm()
# # # # # 		if hasattr(pap, 'objects') == True:
# # # # # 			rp_tmp = pap.rp.get(pk= id1)
# # # # # 			uform.statment.data = rp_tmp.statment
# # # # # 			uform.desc.data = rp_tmp.desc
# # # # # 			return render_template_string(edit_create_view_id, form=uform, fn_target='papers.rpedit', id=id, id1=id1, id2=None, id3=None, id4=None, id5=None, back = request.referrer, kwargs = {'class_':'form-control fw-bold'})
# # # # # 	if request.method == 'POST':
# # # # # 		uform = ResearchProblemForm(request.form)
# # # # # 		if uform.validate_on_submit():
# # # # # 			if hasattr(pap, 'objects') == True:
# # # # # 				try:
# # # # # 					if pap.rp.filter(statment=uform.statment.data).count() > 0:
# # # # # 						return render_template_string("""{% extends "base.html" %} {% block content %}<h3>'Problem Statment' is in List </h3>{% endblock %}""")
# # # # # 					rp_tmp = pap.rp.get(pk= id1)
# # # # # 					rp_tmp.statment = uform.statment.data
# # # # # 					rp_tmp.desc = uform.desc.data      
# # # # # 					pap.save()
# # # # # 					return redirect(request.form.get('next'))
# # # # # 				except DoesNotExist as e:
# # # # # 					flash(id + ' Doest Not Exist')
# # # # # 					return render_template_string(errormessages)
# # # # # 				except ValidationError as e:
# # # # # 					flash(e.message)
# # # # # 					flash(e.field_name)
# # # # # 					flash(e.errors)
# # # # # 					return render_template_string(errormessages)
# # # # # #################################################################################### Delete Route for rp
# # # # # @papers.route('/rpdelete/<id>/<id1>', methods=['POST'])
# # # # # @login_required
# # # # # def rpdelete(id,id1):
# # # # # 	pap=Paper.objects(id=id).first()
# # # # # 	if request.method == 'POST':
# # # # # 		if hasattr(pap, 'objects') == True:
# # # # # 			try:
# # # # # 				rp_tmp = pap.rp.get(pk= id1)
# # # # # 				pap.rp.remove(rp_tmp)
# # # # # 				pap.save()
# # # # # 				return redirect('/reffiles')
# # # # # 			except DoesNotExist as e:
# # # # # 				flash(id + ' Doest Not Exist')
# # # # # 				return render_template_string(errormessages)
# # # # # 			except ValidationError as e:
# # # # # 				flash(e.message)
# # # # # 				flash(e.field_name)
# # # # # 				flash(e.errors)
# # # # # 				return render_template_string(errormessages)
# # # # # #################################################################################### Module for rp#############################################
# # # # # #################################################################################### Module for rp#############################################












# #################################################################################### Module for rp#############################################
# #################################################################################### View HTML for rp
# rp_jinja2 = """{% from 'form_macros.html' import render_linkdescl2 %}
#         	{% extends "base.html" %} {% block content %}
#         	<input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
#         	<input type="hidden" name="next" value={{backview}} />
#         	<a href="{{url_for('papers.rpcreate', id = id )}}">(New Research Problem)</a>
#         	{% for item in itemlist %}
#             		<div class="{{ kwargs.get('class_', '') }}">
            
# 		<div><h1>{{item.statment}}</h1>
#         		<a href="{{url_for('papers.rpedit', id = id, id1 = item.pk)}}">Edit</a>
#         		<button type="button" class="btn btn-sm btn-link" data-bs-toggle="modal" data-bs-target="#delete_rp{{item.pk}}">Delete</button></div>
# 		<h5>Description : {{item.desc}}</h5>
		
#             		</div>
            
# 		{{render_linkdescl2(item.keywords, id, 'rp', item.pk, 'keywords','/rp', kwargs)}}
# 		{{render_linkdescl2(item.area, id, 'rp', item.pk, 'area','/rp', kwargs)}}
# 		{{render_linkdescl2(item.applications, id, 'rp', item.pk, 'applications','/rp', kwargs)}}
# 		{{render_linkdescl2(item.journals_conf, id, 'rp', item.pk, 'journals_conf','/rp', kwargs)}}
# 		{{render_linkdescl2(item.code_links, id, 'rp', item.pk, 'code_links','/rp', kwargs)}}
# 		{{render_linkdescl2(item.datasets_links, id, 'rp', item.pk, 'datasets_links','/rp', kwargs)}}
# 		{{render_linkdescl2(item.peoples, id, 'rp', item.pk, 'peoples','/rp', kwargs)}}
# 		{{render_linkdescl2(item.articals, id, 'rp', item.pk, 'articals','/rp', kwargs)}}
# 		{{render_linkdescl2(item.resoures, id, 'rp', item.pk, 'resoures','/rp', kwargs)}}
# 		{{render_linkdescl2(item.sm, id, 'rp', item.pk, 'sm','/rp', kwargs)}}
		
#         	{% endfor %}
#         	{% for item in itemlist %}
            		
#                     <div class="modal fade" id="delete_rp{{item.pk}}" tabindex="-1" aria-labelledby="deletelabel" aria-hidden="true" role="dialog">
#                         <div class="modal-dialog modal-dialog-centered">
#                             <div class="modal-content">
#                                 <div class="modal-header">
#                                     <h5 class="modal-title" id="deletelabel">Alert</h5>
#                                     <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
#                                 </div>
#                                 <div class="modal-body">
#                                     <form action="{{ url_for('papers.rpdelete', id = id, id1 = item.pk) }}" method="POST">
#                                         <input type="hidden" class="form-control" name="csrf_token" value="{{ csrf_token() }}"/>
#                                         <input type="hidden" class="form-control" name="next" value={{backview}} />
#                                         <div class="form-group">
#                                             <div>
#                                                 <button type="submit" class="btn btn-success">
#                                                     Delete
#                                                 </button>
#                                             </div>
#                                         </div>
#                                     </form>
#                                 </div>
#                                 <div class="mb-3">
#                                     <div class="modal-footer">
#                                         <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
#                                             Close
#                                         </button>
#                                     </div>
#                                 </div>
#                             </div>
#                         </div>
#                     </div>
#         	{% endfor %}
#         {% endblock %}
#             """
# #################################################################################### View Route for rp
# @papers.route('/rp/<id>', methods=['GET'])
# @login_required
# def rp(id):
# 	if session['paper_id'] is None:
# 		return redirect(url_for('papers.paperselect'))
# 	pap = Paper.objects(id=session['paper_id'] ).first()
# 	if request.method == 'GET':
# 		if hasattr(pap, 'objects') == True:
# 			return render_template_string(rp_jinja2
# 						,backview = request.referrer
# 						,itemlist = pap.rp, id = id #id = pap.id
# 						,kwargs = {'class_':'form-control fw-bold'})
# 		else:
# 			return render_template_string("""{% extends "base.html" %} {% block content %}<h3>Research Problem List is empty. </h3>{% endblock %}""")
# #################################################################################### View Dictonary  for rp
# @papers.route('/rp_dict', methods=['GET'])
# @login_required
# def rp_dict():
# 	if session['paper_id'] is None:
# 		return redirect(url_for('papers.paperselect'))
# 	pap = Paper.objects(id=session['paper_id'] ).first()
# 	details_dict_view_list = []
# 	for p in pap.rp:
# 		details_dict_view_list.append(p.__dict__())
# 	return render_template_string(details_dict_listview
# 		, fn_target_new = 'papers.rpcreate', fn_target_edit = 'papers.rpedit', fn_target_delete = 'papers.rpdelete'
# 		, back = request.referrer
# 		, id = pap.id, detailitemslist = details_dict_view_list, tablehead = 'Field', tableheadrvalue = 'Information'
# 		, kwargs = {'class_':'form-control fw-bold'})
# #################################################################################### Create Route for rp
# @papers.route('/rpcreate/<id>', methods=['GET', 'POST'])
# @login_required
# def rpcreate(id):
# 	pap=Paper.objects(id=id).first()
# 	if request.method == 'GET':
# 		uform = ResearchProblemForm()
# 		if hasattr(pap, 'objects') == True:
# 			return render_template_string(edit_create_view_id, form=uform, fn_target='papers.rpcreate'
# 						, id=id, id1=None, id2=None, id3=None, id4=None, id5=None 
# 						, back = request.referrer
# 						, kwargs = {'class_':'form-control fw-bold'})
# 	if request.method == 'POST':
# 		uform = ResearchProblemForm(request.form)
# 		if uform.validate_on_submit():
# 			if hasattr(pap, 'objects') == True:
# 				try:
# 					if pap.rp.filter(statment=uform.statment.data).count() > 0:
# 						return render_template_string("""{% extends "base.html" %} {% block content %}<h3>'Problem Statment' is in List </h3>{% endblock %}""")
# 					rp_tmp = ResearchProblem(pk= get_a_uuid(),statment = uform.statment.data,desc = uform.desc.data)
# 					pap.rp.append(rp_tmp)
# 					pap.rp.save()
# 					return redirect(request.form.get('next'))
# 				except DoesNotExist as e:
# 					flash(id + ' Doest Not Exist')
# 					return render_template_string(errormessages)
# 				except ValidationError as e:
# 					flash(e.message)
# 					flash(e.field_name)
# 					flash(e.errors)
# 					return render_template_string(errormessages,messages=e.message)
# #################################################################################### Edit Route for rp
# @papers.route('/rpedit/<id>/<id1>', methods=['GET', 'POST'])
# @login_required
# def rpedit(id,id1):
# 	pap=Paper.objects(id=id).first()
# 	if request.method == 'GET':
# 		uform = ResearchProblemForm()
# 		if hasattr(pap, 'objects') == True:
# 			rp_tmp = pap.rp.get(pk= id1)
# 			uform.statment.data = rp_tmp.statment
# 			uform.desc.data = rp_tmp.desc
# 			return render_template_string(edit_create_view_id, form=uform, fn_target='papers.rpedit', id=id, id1=id1, id2=None, id3=None, id4=None, id5=None, back = request.referrer, kwargs = {'class_':'form-control fw-bold'})
# 	if request.method == 'POST':
# 		uform = ResearchProblemForm(request.form)
# 		if uform.validate_on_submit():
# 			if hasattr(pap, 'objects') == True:
# 				try:
# 					if pap.rp.filter(statment=uform.statment.data).count() > 0:
# 						return render_template_string("""{% extends "base.html" %} {% block content %}<h3>'Problem Statment' is in List </h3>{% endblock %}""")
# 					rp_tmp = pap.rp.get(pk= id1)
# 					rp_tmp.statment = uform.statment.data
# 					rp_tmp.desc = uform.desc.data      
# 					pap.save()
# 					return redirect(request.form.get('next'))
# 				except DoesNotExist as e:
# 					flash(id + ' Doest Not Exist')
# 					return render_template_string(errormessages)
# 				except ValidationError as e:
# 					flash(e.message)
# 					flash(e.field_name)
# 					flash(e.errors)
# 					return render_template_string(errormessages)
# #################################################################################### Delete Route for rp
# @papers.route('/rpdelete/<id>/<id1>', methods=['POST'])
# @login_required
# def rpdelete(id,id1):
# 	pap=Paper.objects(id=id).first()
# 	if request.method == 'POST':
# 		if hasattr(pap, 'objects') == True:
# 			try:
# 				rp_tmp = pap.rp.get(pk= id1)
# 				pap.rp.remove(rp_tmp)
# 				pap.save()
# 				return redirect('/reffiles')
# 			except DoesNotExist as e:
# 				flash(id + ' Doest Not Exist')
# 				return render_template_string(errormessages)
# 			except ValidationError as e:
# 				flash(e.message)
# 				flash(e.field_name)
# 				flash(e.errors)
# 				return render_template_string(errormessages)
#################################################################################### Module for rp#############################################
#################################################################################### Module for rp#############################################


###############################################################################



#################################################################################### Module for authors#############################################
#################################################################################### View HTML for authors
authors_jinja2 = """{% from 'form_macros.html' import render_linkdescl2, render_flashed_messages %}
        	{% extends "base.html" %} {% block content %}
        	<input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
        	<input type="hidden" name="next" value={{backview}} />
             {{render_flashed_messages()}}
        	<a href="{{url_for('papers.authorscreate', id = id )}}">(New Paper Person)</a>
        	{% for ppobj in ppobjlist %}
            		<div class="{{ kwargs.get('class_', '') }}">
            
		<div><h1>{{ppobj.name}}</h1>
        		<a href="{{url_for('papers.authorsedit', id = id, id1 = ppobj.pk)}}">Edit</a>
        		<button type="button" class="btn btn-sm btn-link" data-bs-toggle="modal" data-bs-target="#delete_authors{{ppobj.pk}}">Delete</button></div>
		<h5>Email : {{ppobj.email}}</h5>
		<h5>Title : {{ppobj.title}}</h5>
		<h5>Position : {{ppobj.position}}</h5>
		<h5>Is Corresponding : {{ppobj.corresponding}}</h5>
		<h5>Sequence in Author(if any) : {{ppobj.sequence}}</h5>
		<h5>Gender : {{ppobj.gender}}</h5>
		<h5>Mobile Ph. : {{ppobj.ph}}</h5>
		
            		</div>
            
		{{render_linkdescl2(ppobj.affiliation, id, 'authors', ppobj.pk, 'affiliation','/authors', kwargs)}}
		
        	{% endfor %}
        	{% for ppobj in ppobjlist %}
            		
                    <div class="modal fade" id="delete_authors{{ppobj.pk}}" tabindex="-1" aria-labelledby="deletelabel" aria-hidden="true" role="dialog">
                        <div class="modal-dialog modal-dialog-centered">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title" id="deletelabel">Alert</h5>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                </div>
                                <div class="modal-body">
                                    <form action="{{ url_for('papers.authorsdelete', id = id, id1 = ppobj.pk) }}" method="POST">
                                        <input type="hidden" class="form-control" name="csrf_token" value="{{ csrf_token() }}"/>
                                        <input type="hidden" class="form-control" name="next" value={{backview}} />
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
        	{% endfor %}
        {% endblock %}
            """
#################################################################################### View Route for authors
@papers.route('/authors', methods=['GET'])
@papers.route('/authors/<id>', methods=['GET'])
@login_required
def authors(id = None):
	if session['paper_id'] is None:
		return redirect(url_for('papers.paperselect'))
	pap = Paper.objects(id=session['paper_id'] ).first()
	if request.method == 'GET':
		if hasattr(pap, 'objects') == True:
			return render_template_string(authors_jinja2
						,backview = request.referrer
						,ppobjlist = pap.authors, id = pap.id
						,kwargs = {'class_':'form-control row mb-1 col-sm-2 col-form-label ms-1'})
		else:
			return render_template_string("""{% extends "base.html" %} {% block content %}<h3>Person involved in Paper List is empty. </h3>{% endblock %}""")
#################################################################################### View Dictonary  for authors
@papers.route('/authors_dict', methods=['GET'])
@login_required
def authors_dict():
	if session['paper_id'] is None:
		return redirect(url_for('papers.paperselect'))
	pap = Paper.objects(id=session['paper_id'] ).first()
	details_dict_view_list = []
	for p in pap.authors:
		details_dict_view_list.append(p.__dict__())
	return render_template_string(details_dict_listview
		, fn_target_new = 'papers.authorscreate', fn_target_edit = 'papers.authorsedit', fn_target_delete = 'papers.authorsdelete'
		, back = request.referrer
		, id = pap.id, detailitemslist = details_dict_view_list, tablehead = 'Field', tableheadrvalue = 'Information'
		, kwargs = {'class_':'form-control row mb-1 col-sm-2 col-form-label ms-1'})
#################################################################################### Create Route for authors
@papers.route('/authorscreate/<id>', methods=['GET', 'POST'])
@login_required
def authorscreate(id):
	pap=Paper.objects(id=id).first()
	if request.method == 'GET':
		uform = PaperPersonForm()
		if hasattr(pap, 'objects') == True:
			return render_template_string(edit_create_view_id, form=uform, fn_target='papers.authorscreate'
						, id=id, id1=None, id2=None, id3=None, id4=None, id5=None 
						, back = request.referrer
						, kwargs = {'class_':'form-control row mb-1 col-sm-2 col-form-label ms-1'})
	if request.method == 'POST':
		uform = PaperPersonForm(request.form)
		if uform.validate_on_submit():
			if hasattr(pap, 'objects') == True:
				try:
					if pap.authors.filter(name=uform.name.data).count() > 0:
						return render_template_string("""{% extends "base.html" %} {% block content %}<h3>'Author' is in List </h3>{% endblock %}""")
					authors_tmp = PaperPerson(pk= get_a_uuid(),name = uform.name.data,email = uform.email.data,title = uform.title.data,position = uform.position.data,corresponding = uform.corresponding.data,sequence = uform.sequence.data,gender = uform.gender.data,ph = uform.ph.data)
					pap.authors.append(authors_tmp)
					pap.authors.save()
					return redirect(request.form.get('next'))
				except DoesNotExist as e:
					flash(id + ' Doest Not Exist')
					return render_template_string(errormessages)
				except ValidationError as e:
					flash(e.message)
					flash(e.field_name)
					flash(e.errors)
					return render_template_string(errormessages,messages=e.message)
#################################################################################### Edit Route for authors
@papers.route('/authorsedit/<id>/<id1>', methods=['GET', 'POST'])
@login_required
def authorsedit(id,id1):
	pap=Paper.objects(id=id).first()
	if request.method == 'GET':
		uform = PaperPersonFormEdit()
		if hasattr(pap, 'objects') == True:
			authors_tmp = pap.authors.get(pk= id1)
			uform.name.data = authors_tmp.name
			uform.email.data = authors_tmp.email
			uform.title.data = authors_tmp.title
			uform.position.data = authors_tmp.position
			uform.corresponding.data = authors_tmp.corresponding
			uform.sequence.data = authors_tmp.sequence
			uform.gender.data = authors_tmp.gender
			uform.ph.data = authors_tmp.ph
			return render_template_string(edit_create_view_id, form=uform, fn_target='papers.authorsedit', id=id, id1=id1, id2=None, id3=None, id4=None, id5=None, back = request.referrer, kwargs = {'class_':'form-control row mb-1 col-sm-2 col-form-label ms-1'})
	if request.method == 'POST':
		uform = PaperPersonFormEdit(request.form)
		if uform.validate_on_submit():
			if hasattr(pap, 'objects') == True:
				try:
					authors_tmp = pap.authors.get(pk= id1)
					authors_tmp.name = uform.name.data
					authors_tmp.email = uform.email.data
					authors_tmp.title = uform.title.data
					authors_tmp.position = uform.position.data
					authors_tmp.corresponding = uform.corresponding.data
					authors_tmp.sequence = uform.sequence.data
					authors_tmp.gender = uform.gender.data
					authors_tmp.ph = uform.ph.data      
					pap.save()
					return redirect(request.form.get('next'))
				except DoesNotExist as e:
					flash(id + ' Doest Not Exist')
					return render_template_string(errormessages)
				except ValidationError as e:
					flash(e.message)
					flash(e.field_name)
					flash(e.errors)
					return render_template_string(errormessages)
#################################################################################### Delete Route for authors
@papers.route('/authorsdelete/<id>/<id1>', methods=['POST'])
@login_required
def authorsdelete(id,id1):
	pap=Paper.objects(id=id).first()
	if request.method == 'POST':
		if hasattr(pap, 'objects') == True:
			try:
				authors_tmp = pap.authors.get(pk= id1)
				pap.authors.remove(authors_tmp)
				pap.save()
				return redirect('/reffiles')
			except DoesNotExist as e:
				flash(id + ' Doest Not Exist')
				return render_template_string(errormessages)
			except ValidationError as e:
				flash(e.message)
				flash(e.field_name)
				flash(e.errors)
				return render_template_string(errormessages)
#################################################################################### Module for authors#############################################
#################################################################################### Module for authors#############################################





#################################################################################### Module for rp#############################################
#################################################################################### View HTML for rp
rp_jinja2 = """{% from 'form_macros.html' import render_linkdescl2, render_flashed_messages %}
        	{% extends "base.html" %} {% block content %}
        	<input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
        	<input type="hidden" name="next" value={{backview}} />
        	{{render_flashed_messages()}}
            <a href="{{url_for('papers.rpcreate', id = id )}}">(New Research Problem)</a>
        	{% for rpobj in rpobjlist %}
            		<div class="{{ kwargs.get('class_', '') }}">
            
		<div><h1>{{rpobj.statment}}</h1>
        		<a href="{{url_for('papers.rpedit', id = id, id1 = rpobj.pk)}}">Edit</a>
        		<button type="button" class="btn btn-sm btn-link" data-bs-toggle="modal" data-bs-target="#delete_rp{{rpobj.pk}}">Delete</button></div>
		<h5>Description : {{rpobj.desc}}</h5>
		
            		</div>
            
		{{render_linkdescl2(rpobj.keywords, id, 'rp', rpobj.pk, 'keywords','/rp', kwargs)}}
		{{render_linkdescl2(rpobj.area, id, 'rp', rpobj.pk, 'area','/rp', kwargs)}}
		{{render_linkdescl2(rpobj.applications, id, 'rp', rpobj.pk, 'applications','/rp', kwargs)}}
		{{render_linkdescl2(rpobj.journals_conf, id, 'rp', rpobj.pk, 'journals_conf','/rp', kwargs)}}
		{{render_linkdescl2(rpobj.code_links, id, 'rp', rpobj.pk, 'code_links','/rp', kwargs)}}
		{{render_linkdescl2(rpobj.datasets_links, id, 'rp', rpobj.pk, 'datasets_links','/rp', kwargs)}}
		{{render_linkdescl2(rpobj.peoples, id, 'rp', rpobj.pk, 'peoples','/rp', kwargs)}}
		{{render_linkdescl2(rpobj.articals, id, 'rp', rpobj.pk, 'articals','/rp', kwargs)}}
		{{render_linkdescl2(rpobj.resoures, id, 'rp', rpobj.pk, 'resoures','/rp', kwargs)}}
		{{render_linkdescl2(rpobj.sm, id, 'rp', rpobj.pk, 'sm','/rp', kwargs)}}
		
        	{% endfor %}
        	{% for rpobj in rpobjlist %}
            		
                    <div class="modal fade" id="delete_rp{{rpobj.pk}}" tabindex="-1" aria-labelledby="deletelabel" aria-hidden="true" role="dialog">
                        <div class="modal-dialog modal-dialog-centered">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title" id="deletelabel">Alert</h5>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                </div>
                                <div class="modal-body">
                                    <form action="{{ url_for('papers.rpdelete', id = id, id1 = rpobj.pk) }}" method="POST">
                                        <input type="hidden" class="form-control" name="csrf_token" value="{{ csrf_token() }}"/>
                                        <input type="hidden" class="form-control" name="next" value={{backview}} />
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
        	{% endfor %}
        {% endblock %}
            """
#################################################################################### View Route for rp
@papers.route('/rp', methods=['GET'])
@papers.route('/rp/<id>', methods=['GET'])
@login_required
def rp(id = None):
	if session['paper_id'] is None:
		return redirect(url_for('papers.paperselect'))
	pap = Paper.objects(id=session['paper_id'] ).first()
	if request.method == 'GET':
		if hasattr(pap, 'objects') == True:
			return render_template_string(rp_jinja2
						,backview = request.referrer
						,rpobjlist = pap.rp, id = pap.id
						,kwargs = {'class_':'form-control row mb-1 col-sm-2 col-form-label ms-1'})
		else:
			return render_template_string("""{% extends "base.html" %} {% block content %}<h3>Research Problem List is empty. </h3>{% endblock %}""")
#################################################################################### View Dictonary  for rp
@papers.route('/rp_dict', methods=['GET'])
@login_required
def rp_dict():
	if session['paper_id'] is None:
		return redirect(url_for('papers.paperselect'))
	pap = Paper.objects(id=session['paper_id'] ).first()
	details_dict_view_list = []
	for p in pap.rp:
		details_dict_view_list.append(p.__dict__())
	return render_template_string(details_dict_listview
		, fn_target_new = 'papers.rpcreate', fn_target_edit = 'papers.rpedit', fn_target_delete = 'papers.rpdelete'
		, back = request.referrer
		, id = pap.id, detailitemslist = details_dict_view_list, tablehead = 'Field', tableheadrvalue = 'Information'
		, kwargs = {'class_':'form-control row mb-1 col-sm-2 col-form-label ms-1'})
#################################################################################### Create Route for rp
@papers.route('/rpcreate/<id>', methods=['GET', 'POST'])
@login_required
def rpcreate(id):
	pap=Paper.objects(id=id).first()
	if request.method == 'GET':
		uform = PaperPersonForm()
		if hasattr(pap, 'objects') == True:
			return render_template_string(edit_create_view_id, form=uform, fn_target='papers.rpcreate'
						, id=id, id1=None, id2=None, id3=None, id4=None, id5=None 
						, back = request.referrer
						, kwargs = {'class_':'form-control row mb-1 col-sm-2 col-form-label ms-1'})
	if request.method == 'POST':
		uform = PaperPersonForm(request.form)
		if uform.validate_on_submit():
			if hasattr(pap, 'objects') == True:
				try:
					if pap.rp.filter(statment=uform.statment.data).count() > 0:
						return render_template_string("""{% extends "base.html" %} {% block content %}<h3>'Problem Statment' is in List </h3>{% endblock %}""")
					rp_tmp = ResearchProblem(pk= get_a_uuid(),statment = uform.statment.data,desc = uform.desc.data)
					pap.rp.append(rp_tmp)
					pap.rp.save()
					return redirect(request.form.get('next'))
				except DoesNotExist as e:
					flash(id + ' Doest Not Exist')
					return render_template_string(errormessages)
				except ValidationError as e:
					flash(e.message)
					flash(e.field_name)
					flash(e.errors)
					return render_template_string(errormessages,messages=e.message)
#################################################################################### Edit Route for rp
@papers.route('/rpedit/<id>/<id1>', methods=['GET', 'POST'])
@login_required
def rpedit(id,id1):
	pap=Paper.objects(id=id).first()
	if request.method == 'GET':
		uform = PaperPersonFormEdit()
		if hasattr(pap, 'objects') == True:
			rp_tmp = pap.rp.get(pk= id1)
			uform.statment.data = rp_tmp.statment
			uform.desc.data = rp_tmp.desc
			return render_template_string(edit_create_view_id, form=uform, fn_target='papers.rpedit', id=id, id1=id1, id2=None, id3=None, id4=None, id5=None, back = request.referrer, kwargs = {'class_':'form-control row mb-1 col-sm-2 col-form-label ms-1'})
	if request.method == 'POST':
		uform = PaperPersonFormEdit(request.form)
		if uform.validate_on_submit():
			if hasattr(pap, 'objects') == True:
				try:
					rp_tmp = pap.rp.get(pk= id1)
					rp_tmp.statment = uform.statment.data
					rp_tmp.desc = uform.desc.data      
					pap.save()
					return redirect(request.form.get('next'))
				except DoesNotExist as e:
					flash(id + ' Doest Not Exist')
					return render_template_string(errormessages)
				except ValidationError as e:
					flash(e.message)
					flash(e.field_name)
					flash(e.errors)
					return render_template_string(errormessages)
#################################################################################### Delete Route for rp
@papers.route('/rpdelete/<id>/<id1>', methods=['POST'])
@login_required
def rpdelete(id,id1):
	pap=Paper.objects(id=id).first()
	if request.method == 'POST':
		if hasattr(pap, 'objects') == True:
			try:
				rp_tmp = pap.rp.get(pk= id1)
				pap.rp.remove(rp_tmp)
				pap.save()
				return redirect('/reffiles')
			except DoesNotExist as e:
				flash(id + ' Doest Not Exist')
				return render_template_string(errormessages)
			except ValidationError as e:
				flash(e.message)
				flash(e.field_name)
				flash(e.errors)
				return render_template_string(errormessages)
#################################################################################### Module for rp#############################################
#################################################################################### Module for rp#############################################






#################################################################################### Module for reffiles#############################################
#################################################################################### View HTML for reffiles
reffiles_jinja2 = """{% from 'form_macros.html' import render_linkdescl2, render_paperfileuplodedl2, render_flashed_messages %}
        	
            {% extends "base.html" %} {% block content %}
        	<input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
        	<input type="hidden" name="next" value={{backview}} />
            
            {{render_flashed_messages()}}
            <a href="{{url_for('papers.reffilescreate', id = id )}}">(New Paper Ref File Form)</a>
        	{% for probj in probjlist %}
            		<div class="{{ kwargs.get('class_', '') }}">
            
		<div><h1>{{probj.title}}</h1>
        		<a href="{{url_for('papers.reffilesedit', id = id, id1 = probj.pk)}}">Edit</a>
        		<button type="button" class="btn btn-sm btn-link" data-bs-toggle="modal" data-bs-target="#delete_reffiles{{probj.pk}}">Delete</button></div>
		<h5>Artical Type : {{probj.articaltype}}</h5>
		<h5>Year : {{probj.year}}</h5>
		<h5>DOI : {{probj.doi}}</h5>
		<h5>Bibtext : {{probj.bibtext}}</h5>
		<h5>Desc : {{probj.desc}}</h5>
		
            		</div>
            
		{{render_linkdescl2(probj.links, id, 'reffiles', probj.pk, 'links','/reffiles', kwargs)}}
		{{render_paperfileuplodedl2(probj.fileup, id, 'reffiles', probj.pk, 'fileup','/reffiles', kwargs)}}
		
        	{% endfor %}
        	{% for probj in probjlist %}
            		
                    <div class="modal fade" id="delete_reffiles{{probj.pk}}" tabindex="-1" aria-labelledby="deletelabel" aria-hidden="true" role="dialog">
                        <div class="modal-dialog modal-dialog-centered">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title" id="deletelabel">Alert</h5>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                </div>
                                <div class="modal-body">
                                    <form action="{{ url_for('papers.reffilesdelete', id = id, id1 = probj.pk) }}" method="POST">
                                        <input type="hidden" class="form-control" name="csrf_token" value="{{ csrf_token() }}"/>
                                        <input type="hidden" class="form-control" name="next" value={{backview}} />
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
        	{% endfor %}
        {% endblock %}
            """
#################################################################################### View Route for reffiles
@papers.route('/reffiles', methods=['GET'])
@papers.route('/reffiles/<id>', methods=['GET'])
@login_required
def reffiles(id = None):
	if session['paper_id'] is None:
		return redirect(url_for('papers.paperselect'))
	pap = Paper.objects(id=session['paper_id'] ).first()
	if request.method == 'GET':
		if hasattr(pap, 'objects') == True:
			return render_template_string(reffiles_jinja2
						,backview = request.referrer
						,probjlist = pap.reffiles, id = pap.id
						,kwargs = {'class_':'form-control row mb-1 col-sm-2 col-form-label ms-1'})
		else:
			return render_template_string("""{% extends "base.html" %} {% block content %}<h3>Refrence Paper List is empty. </h3>{% endblock %}""")
#################################################################################### View Dictonary  for reffiles
@papers.route('/reffiles_dict', methods=['GET'])
@login_required
def reffiles_dict():
	if session['paper_id'] is None:
		return redirect(url_for('papers.paperselect'))
	pap = Paper.objects(id=session['paper_id'] ).first()
	details_dict_view_list = []
	for p in pap.reffiles:
		details_dict_view_list.append(p.__dict__())
	return render_template_string(details_dict_listview
		, fn_target_new = 'papers.reffilescreate', fn_target_edit = 'papers.reffilesedit', fn_target_delete = 'papers.reffilesdelete'
		, back = request.referrer
		, id = pap.id, detailitemslist = details_dict_view_list, tablehead = 'Field', tableheadrvalue = 'Information'
		, kwargs = {'class_':'form-control row mb-1 col-sm-2 col-form-label ms-1'})
#################################################################################### Create Route for reffiles
@papers.route('/reffilescreate/<id>', methods=['GET', 'POST'])
@login_required
def reffilescreate(id):
	pap=Paper.objects(id=id).first()
	if request.method == 'GET':
		uform = PaperRefFileForm()
		if hasattr(pap, 'objects') == True:
			return render_template_string(edit_create_view_id, form=uform, fn_target='papers.reffilescreate'
						, id=id, id1=None, id2=None, id3=None, id4=None, id5=None 
						, back = request.referrer
						, kwargs = {'class_':'form-control row mb-1 col-sm-2 col-form-label ms-1'})
	if request.method == 'POST':
		uform = PaperRefFileForm(request.form)
		if uform.validate_on_submit():
			if hasattr(pap, 'objects') == True:
				try:
					if pap.reffiles.filter(title=uform.title.data).count() > 0:
						return render_template_string("""{% extends "base.html" %} {% block content %}<h3>'Title' is in List </h3>{% endblock %}""")
					reffiles_tmp = PaperRefFile(pk= get_a_uuid(),title = uform.title.data,articaltype = uform.articaltype.data,year = uform.year.data,doi = uform.doi.data,bibtext = uform.bibtext.data,desc = uform.desc.data)
					pap.reffiles.append(reffiles_tmp)
					pap.reffiles.save()
					return redirect(request.form.get('next'))
				except DoesNotExist as e:
					flash(id + ' Doest Not Exist')
					return render_template_string(errormessages)
				except ValidationError as e:
					flash(e.message)
					flash(e.field_name)
					flash(e.errors)
					return render_template_string(errormessages,messages=e.message)
#################################################################################### Edit Route for reffiles
@papers.route('/reffilesedit/<id>/<id1>', methods=['GET', 'POST'])
@login_required
def reffilesedit(id,id1):
	pap=Paper.objects(id=id).first()
	if request.method == 'GET':
		uform = PaperRefFileForm()
		if hasattr(pap, 'objects') == True:
			reffiles_tmp = pap.reffiles.get(pk= id1)
			uform.title.data = reffiles_tmp.title
			uform.articaltype.data = reffiles_tmp.articaltype
			uform.year.data = reffiles_tmp.year
			uform.doi.data = reffiles_tmp.doi
			uform.bibtext.data = reffiles_tmp.bibtext
			uform.desc.data = reffiles_tmp.desc
			return render_template_string(edit_create_view_id, form=uform, fn_target='papers.reffilesedit', id=id, id1=id1, id2=None, id3=None, id4=None, id5=None, back = request.referrer, kwargs = {'class_':'form-control row mb-1 col-sm-2 col-form-label ms-1'})
	if request.method == 'POST':
		uform = PaperRefFileForm(request.form)
		if uform.validate_on_submit():
			if hasattr(pap, 'objects') == True:
				try:
					reffiles_tmp = pap.reffiles.get(pk= id1)
					reffiles_tmp.title = uform.title.data
					reffiles_tmp.articaltype = uform.articaltype.data
					reffiles_tmp.year = uform.year.data
					reffiles_tmp.doi = uform.doi.data
					reffiles_tmp.bibtext = uform.bibtext.data
					reffiles_tmp.desc = uform.desc.data      
					pap.save()
					return redirect(request.form.get('next'))
				except DoesNotExist as e:
					flash(id + ' Doest Not Exist')
					return render_template_string(errormessages)
				except ValidationError as e:
					flash(e.message)
					flash(e.field_name)
					flash(e.errors)
					return render_template_string(errormessages)
#################################################################################### Delete Route for reffiles
@papers.route('/reffilesdelete/<id>/<id1>', methods=['POST'])
@login_required
def reffilesdelete(id,id1):
	pap=Paper.objects(id=id).first()
	if request.method == 'POST':
		if hasattr(pap, 'objects') == True:
			try:
				reffiles_tmp = pap.reffiles.get(pk= id1)
				pap.reffiles.remove(reffiles_tmp)
				pap.save()
				return redirect('/reffiles')
			except DoesNotExist as e:
				flash(id + ' Doest Not Exist')
				return render_template_string(errormessages)
			except ValidationError as e:
				flash(e.message)
				flash(e.field_name)
				flash(e.errors)
				return render_template_string(errormessages)
#################################################################################### Module for reffiles#############################################
#################################################################################### Module for reffiles#############################################











#################################################################################### Module for journals#############################################
#################################################################################### View HTML for journals
journals_jinja2 = """{% from 'form_macros.html' import render_linkdescl2, render_paperfileuplodedl2, render_flashed_messages %}
        	{% extends "base.html" %} {% block content %}
        	<input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
        	<input type="hidden" name="next" value={{backview}} />
        	{{render_flashed_messages()}}
        	<a href="{{url_for('papers.journalscreate', id = id )}}">(New Journal Form)</a>
        	{% for psjobj in psjobjlist %}
            		<div class="{{ kwargs.get('class_', '') }}">
            
		<div><h1>{{psjobj.name}}</h1>
        		<a href="{{url_for('papers.journalsedit', id = id, id1 = psjobj.pk)}}">Edit</a>
        		<button type="button" class="btn btn-sm btn-link" data-bs-toggle="modal" data-bs-target="#delete_journals{{psjobj.pk}}">Delete</button></div>
		<h5>Mode : {{psjobj.mode}}</h5>
		<h5>Publisher : {{psjobj.publisher}}</h5>
		<h5>Indexing : {{psjobj.indexing}}</h5>
		<h5>User Name : {{psjobj.username}}</h5>
		
            		</div>
            
		{{render_linkdescl2(psjobj.specialissue, id, 'journals', psjobj.pk, 'specialissue','/journals', kwargs)}}
		{{render_linkdescl2(psjobj.links, id, 'journals', psjobj.pk, 'links','/journals', kwargs)}}
		{{render_linkdescl2(psjobj.submissionlink, id, 'journals', psjobj.pk, 'submissionlink','/journals', kwargs)}}
		{{render_paperfileuplodedl2(psjobj.subtemplate, id, 'journals', psjobj.pk, 'subtemplate','/journals', kwargs)}}
		{{render_paperfileuplodedl2(psjobj.indexingproof, id, 'journals', psjobj.pk, 'indexingproof','/journals', kwargs)}}
		
        	{% endfor %}
        	{% for psjobj in psjobjlist %}
            		
                    <div class="modal fade" id="delete_journals{{psjobj.pk}}" tabindex="-1" aria-labelledby="deletelabel" aria-hidden="true" role="dialog">
                        <div class="modal-dialog modal-dialog-centered">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title" id="deletelabel">Alert</h5>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                </div>
                                <div class="modal-body">
                                    <form action="{{ url_for('papers.journalsdelete', id = id, id1 = psjobj.pk) }}" method="POST">
                                        <input type="hidden" class="form-control" name="csrf_token" value="{{ csrf_token() }}"/>
                                        <input type="hidden" class="form-control" name="next" value={{backview}} />
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
        	{% endfor %}
        {% endblock %}
            """
#################################################################################### View Route for journals
@papers.route('/journals', methods=['GET'])
@papers.route('/journals/<id>', methods=['GET'])
@login_required
def journals(id = None):
	if session['paper_id'] is None:
		return redirect(url_for('papers.paperselect'))
	pap = Paper.objects(id=session['paper_id'] ).first()
	if request.method == 'GET':
		if hasattr(pap, 'objects') == True:
			return render_template_string(journals_jinja2
						,backview = request.referrer
						,psjobjlist = pap.journals, id = pap.id
						,kwargs = {'class_':'form-control row mb-1 col-sm-2 col-form-label ms-1'})
		else:
			return render_template_string("""{% extends "base.html" %} {% block content %}<h3>Journals Comments List is empty. </h3>{% endblock %}""")
#################################################################################### View Dictonary  for journals
@papers.route('/journals_dict', methods=['GET'])
@login_required
def journals_dict():
	if session['paper_id'] is None:
		return redirect(url_for('papers.paperselect'))
	pap = Paper.objects(id=session['paper_id'] ).first()
	details_dict_view_list = []
	for p in pap.journals:
		details_dict_view_list.append(p.__dict__())
	return render_template_string(details_dict_listview
		, fn_target_new = 'papers.journalscreate', fn_target_edit = 'papers.journalsedit', fn_target_delete = 'papers.journalsdelete'
		, back = request.referrer
		, id = pap.id, detailitemslist = details_dict_view_list, tablehead = 'Field', tableheadrvalue = 'Information'
		, kwargs = {'class_':'form-control row mb-1 col-sm-2 col-form-label ms-1'})
#################################################################################### Create Route for journals
@papers.route('/journalscreate/<id>', methods=['GET', 'POST'])
@login_required
def journalscreate(id):
	pap=Paper.objects(id=id).first()
	if request.method == 'GET':
		uform = PaperSubmittedinJournalForm()
		if hasattr(pap, 'objects') == True:
			return render_template_string(edit_create_view_id, form=uform, fn_target='papers.journalscreate'
						, id=id, id1=None, id2=None, id3=None, id4=None, id5=None 
						, back = request.referrer
						, kwargs = {'class_':'form-control row mb-1 col-sm-2 col-form-label ms-1'})
	if request.method == 'POST':
		uform = PaperSubmittedinJournalForm(request.form)
		if uform.validate_on_submit():
			if hasattr(pap, 'objects') == True:
				try:
					if pap.journals.filter(name=uform.name.data).count() > 0:
						return render_template_string("""{% extends "base.html" %} {% block content %}<h3>'Name' is in List </h3>{% endblock %}""")
					journals_tmp = PaperSubmittedinJournal(pk= get_a_uuid(),name = uform.name.data,mode = uform.mode.data,publisher = uform.publisher.data,indexing = uform.indexing.data,score = uform.score.data,username = uform.username.data)
					pap.journals.append(journals_tmp)
					pap.journals.save()
					return redirect(request.form.get('next'))
				except DoesNotExist as e:
					flash(id + ' Doest Not Exist')
					return render_template_string(errormessages)
				except ValidationError as e:
					flash(e.message)
					flash(e.field_name)
					flash(e.errors)
					return render_template_string(errormessages,messages=e.message)
#################################################################################### Edit Route for journals
@papers.route('/journalsedit/<id>/<id1>', methods=['GET', 'POST'])
@login_required
def journalsedit(id,id1):
	pap=Paper.objects(id=id).first()
	if request.method == 'GET':
		uform = PaperSubmittedinJournalForm()
		if hasattr(pap, 'objects') == True:
			journals_tmp = pap.journals.get(pk= id1)
			uform.name.data = journals_tmp.name
			uform.mode.data = journals_tmp.mode
			uform.publisher.data = journals_tmp.publisher
			uform.indexing.data = journals_tmp.indexing
			uform.score.data = journals_tmp.score
			uform.username.data = journals_tmp.username
			return render_template_string(edit_create_view_id, form=uform, fn_target='papers.journalsedit', id=id, id1=id1, id2=None, id3=None, id4=None, id5=None, back = request.referrer, kwargs = {'class_':'form-control row mb-1 col-sm-2 col-form-label ms-1'})
	if request.method == 'POST':
		uform = PaperSubmittedinJournalForm(request.form)
		if uform.validate_on_submit():
			if hasattr(pap, 'objects') == True:
				try:
					journals_tmp = pap.journals.get(pk= id1)
					journals_tmp.name = uform.name.data
					journals_tmp.mode = uform.mode.data
					journals_tmp.publisher = uform.publisher.data
					journals_tmp.indexing = uform.indexing.data
					journals_tmp.score = uform.score.data
					journals_tmp.username = uform.username.data      
					pap.save()
					return redirect(request.form.get('next'))
				except DoesNotExist as e:
					flash(id + ' Doest Not Exist')
					return render_template_string(errormessages)
				except ValidationError as e:
					flash(e.message)
					flash(e.field_name)
					flash(e.errors)
					return render_template_string(errormessages)
#################################################################################### Delete Route for journals
@papers.route('/journalsdelete/<id>/<id1>', methods=['POST'])
@login_required
def journalsdelete(id,id1):
	pap=Paper.objects(id=id).first()
	if request.method == 'POST':
		if hasattr(pap, 'objects') == True:
			try:
				journals_tmp = pap.journals.get(pk= id1)
				pap.journals.remove(journals_tmp)
				pap.save()
				return redirect('/reffiles')
			except DoesNotExist as e:
				flash(id + ' Doest Not Exist')
				return render_template_string(errormessages)
			except ValidationError as e:
				flash(e.message)
				flash(e.field_name)
				flash(e.errors)
				return render_template_string(errormessages)
#################################################################################### Module for journals#############################################
#################################################################################### Module for journals#############################################






#################################################################################### Module for conferences#############################################
#################################################################################### View HTML for conferences
conferences_jinja2 = """{% from 'form_macros.html' import render_linkdescl2, render_paperfileuplodedl2, render_flashed_messages %}
        	{% extends "base.html" %} {% block content %}
        	<input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
        	<input type="hidden" name="next" value={{backview}} />
        	{{render_flashed_messages()}}
        	<a href="{{url_for('papers.conferencescreate', id = id )}}">(New Conference Form)</a>
        	{% for pscobj in pscobjlist %}
            		<div class="{{ kwargs.get('class_', '') }}">
            
		<div><h1>{{pscobj.name}}</h1>
        		<a href="{{url_for('papers.conferencesedit', id = id, id1 = pscobj.pk)}}">Edit</a>
        		<button type="button" class="btn btn-sm btn-link" data-bs-toggle="modal" data-bs-target="#delete_conferences{{pscobj.pk}}">Delete</button></div>
		<h5>Conference Number : {{pscobj.confnumber}}</h5>
		<h5>Submission Deadline : {{pscobj.deadline}}</h5>
		<h5>Start Date : {{pscobj.sdate}}</h5>
		<h5>End Date : {{pscobj.edate}}</h5>
		<h5>City : {{pscobj.city}}</h5>
		<h5>Address : {{pscobj.confadd}}</h5>
		<h5>Publisher : {{pscobj.publisher}}</h5>
		<h5>Indexing : {{pscobj.indexing}}</h5>
		<h5>User Name : {{pscobj.username}}</h5>
		
            		</div>
            
		{{render_linkdescl2(pscobj.links, id, 'conferences', pscobj.pk, 'links','/conferences', kwargs)}}
		{{render_linkdescl2(pscobj.submissionlink, id, 'conferences', pscobj.pk, 'submissionlink','/conferences', kwargs)}}
		{{render_paperfileuplodedl2(pscobj.subtemplate, id, 'conferences', pscobj.pk, 'subtemplate','/conferences', kwargs)}}
		{{render_paperfileuplodedl2(pscobj.indexingproof, id, 'conferences', pscobj.pk, 'indexingproof','/conferences', kwargs)}}
		
        	{% endfor %}
        	{% for pscobj in pscobjlist %}
            		
                    <div class="modal fade" id="delete_conferences{{pscobj.pk}}" tabindex="-1" aria-labelledby="deletelabel" aria-hidden="true" role="dialog">
                        <div class="modal-dialog modal-dialog-centered">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title" id="deletelabel">Alert</h5>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                </div>
                                <div class="modal-body">
                                    <form action="{{ url_for('papers.conferencesdelete', id = id, id1 = pscobj.pk) }}" method="POST">
                                        <input type="hidden" class="form-control" name="csrf_token" value="{{ csrf_token() }}"/>
                                        <input type="hidden" class="form-control" name="next" value={{backview}} />
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
        	{% endfor %}
        {% endblock %}
            """
#################################################################################### View Route for conferences
@papers.route('/conferences', methods=['GET'])
@papers.route('/conferences/<id>', methods=['GET'])
@login_required
def conferences(id = None):
	if session['paper_id'] is None:
		return redirect(url_for('papers.paperselect'))
	pap = Paper.objects(id=session['paper_id'] ).first()
	if request.method == 'GET':
		if hasattr(pap, 'objects') == True:
			return render_template_string(conferences_jinja2
						,backview = request.referrer
						,pscobjlist = pap.conferences, id = pap.id
						,kwargs = {'class_':'form-control row mb-1 col-sm-2 col-form-label ms-1'})
		else:
			return render_template_string("""{% extends "base.html" %} {% block content %}<h3>Conference Comments List is empty. </h3>{% endblock %}""")
#################################################################################### View Dictonary  for conferences
@papers.route('/conferences_dict', methods=['GET'])
@login_required
def conferences_dict():
	if session['paper_id'] is None:
		return redirect(url_for('papers.paperselect'))
	pap = Paper.objects(id=session['paper_id'] ).first()
	details_dict_view_list = []
	for p in pap.conferences:
		details_dict_view_list.append(p.__dict__())
	return render_template_string(details_dict_listview
		, fn_target_new = 'papers.conferencescreate', fn_target_edit = 'papers.conferencesedit', fn_target_delete = 'papers.conferencesdelete'
		, back = request.referrer
		, id = pap.id, detailitemslist = details_dict_view_list, tablehead = 'Field', tableheadrvalue = 'Information'
		, kwargs = {'class_':'form-control row mb-1 col-sm-2 col-form-label ms-1'})
#################################################################################### Create Route for conferences
@papers.route('/conferencescreate/<id>', methods=['GET', 'POST'])
@login_required
def conferencescreate(id):
	pap=Paper.objects(id=id).first()
	if request.method == 'GET':
		uform = PaperSubmittedinConferenceForm()
		if hasattr(pap, 'objects') == True:
			return render_template_string(edit_create_view_id, form=uform, fn_target='papers.conferencescreate'
						, id=id, id1=None, id2=None, id3=None, id4=None, id5=None 
						, back = request.referrer
						, kwargs = {'class_':'form-control row mb-1 col-sm-2 col-form-label ms-1'})
	if request.method == 'POST':
		uform = PaperSubmittedinConferenceForm(request.form)
		if uform.validate_on_submit():
			if hasattr(pap, 'objects') == True:
				try:
					if pap.conferences.filter(name=uform.name.data).count() > 0:
						return render_template_string("""{% extends "base.html" %} {% block content %}<h3>'Name' is in List </h3>{% endblock %}""")
					conferences_tmp = PaperSubmittedinConference(pk= get_a_uuid(),name = uform.name.data,confnumber = uform.confnumber.data,deadline = uform.deadline.data,sdate = uform.sdate.data,edate = uform.edate.data,city = uform.city.data,confadd = uform.confadd.data,publisher = uform.publisher.data,indexing = uform.indexing.data,username = uform.username.data)
					pap.conferences.append(conferences_tmp)
					pap.conferences.save()
					return redirect(request.form.get('next'))
				except DoesNotExist as e:
					flash(id + ' Doest Not Exist')
					return render_template_string(errormessages)
				except ValidationError as e:
					flash(e.message)
					flash(e.field_name)
					flash(e.errors)
					return render_template_string(errormessages,messages=e.message)
#################################################################################### Edit Route for conferences
@papers.route('/conferencesedit/<id>/<id1>', methods=['GET', 'POST'])
@login_required
def conferencesedit(id,id1):
	pap=Paper.objects(id=id).first()
	if request.method == 'GET':
		uform = PaperSubmittedinConferenceForm()
		if hasattr(pap, 'objects') == True:
			conferences_tmp = pap.conferences.get(pk= id1)
			uform.name.data = conferences_tmp.name
			uform.confnumber.data = conferences_tmp.confnumber
			uform.deadline.data = conferences_tmp.deadline
			uform.sdate.data = conferences_tmp.sdate
			uform.edate.data = conferences_tmp.edate
			uform.city.data = conferences_tmp.city
			uform.confadd.data = conferences_tmp.confadd
			uform.publisher.data = conferences_tmp.publisher
			uform.indexing.data = conferences_tmp.indexing
			uform.username.data = conferences_tmp.username
			return render_template_string(edit_create_view_id, form=uform, fn_target='papers.conferencesedit', id=id, id1=id1, id2=None, id3=None, id4=None, id5=None, back = request.referrer, kwargs = {'class_':'form-control row mb-1 col-sm-2 col-form-label ms-1'})
	if request.method == 'POST':
		uform = PaperSubmittedinConferenceForm(request.form)
		if uform.validate_on_submit():
			if hasattr(pap, 'objects') == True:
				try:
					conferences_tmp = pap.conferences.get(pk= id1)
					conferences_tmp.name = uform.name.data
					conferences_tmp.confnumber = uform.confnumber.data
					conferences_tmp.deadline = uform.deadline.data
					conferences_tmp.sdate = uform.sdate.data
					conferences_tmp.edate = uform.edate.data
					conferences_tmp.city = uform.city.data
					conferences_tmp.confadd = uform.confadd.data
					conferences_tmp.publisher = uform.publisher.data
					conferences_tmp.indexing = uform.indexing.data
					conferences_tmp.username = uform.username.data      
					pap.save()
					return redirect(request.form.get('next'))
				except DoesNotExist as e:
					flash(id + ' Doest Not Exist')
					return render_template_string(errormessages)
				except ValidationError as e:
					flash(e.message)
					flash(e.field_name)
					flash(e.errors)
					return render_template_string(errormessages)
#################################################################################### Delete Route for conferences
@papers.route('/conferencesdelete/<id>/<id1>', methods=['POST'])
@login_required
def conferencesdelete(id,id1):
	pap=Paper.objects(id=id).first()
	if request.method == 'POST':
		if hasattr(pap, 'objects') == True:
			try:
				conferences_tmp = pap.conferences.get(pk= id1)
				pap.conferences.remove(conferences_tmp)
				pap.save()
				return redirect('/reffiles')
			except DoesNotExist as e:
				flash(id + ' Doest Not Exist')
				return render_template_string(errormessages)
			except ValidationError as e:
				flash(e.message)
				flash(e.field_name)
				flash(e.errors)
				return render_template_string(errormessages)
#################################################################################### Module for conferences#############################################
#################################################################################### Module for conferences#############################################



