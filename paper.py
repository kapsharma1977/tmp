
#from app import get_db # #from flask import g
# #from flask import current_app as app
# #from . import db
# from mongoengine import DateTimeField, StringField, ReferenceField, ListField
# from datetime import datetime


#db = get_db()
# ###################################################################
# # Classes for Data Modleing

# class LinkDesc(db.EmbeddedDocument):
#     # Link and is's description
#     desc = db.StringField(max_length=500,default='')
#     link = db.URLField() #url

#     def __unicode__(self):
#         return self.desc 
#     def __repr__(self):
#         return self.desc 
#     def __str__(self):
#         return self.desc
#     def __dict__(self):
#         return {
#             'key_str':self.desc   # It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
#             ,'link':self.link
#         }

# class ResearchProblem(db.EmbeddedDocument):
#     statment = db.StringField(max_length=500,default='')  # "Research probleum statment"
#     date_created = db.DateTimeField(default=datetime.utcnow,
#                                         help_text='date the Research Problem was created')
#     keywords = db.EmbeddedDocumentListField(LinkDesc)
#     area = db.EmbeddedDocumentListField(LinkDesc)
#     applications = db.EmbeddedDocumentListField(LinkDesc)
#     journals_conf = db.EmbeddedDocumentListField(LinkDesc)
#     code_links =  db.EmbeddedDocumentListField(LinkDesc) #source Codes for 
#     datasets_links = db.EmbeddedDocumentListField(LinkDesc)
#     peoples = db.EmbeddedDocumentListField(LinkDesc)
#     articals = db.EmbeddedDocumentListField(LinkDesc)
#     resoures = db.EmbeddedDocumentListField(LinkDesc)
#     sm = db.EmbeddedDocumentListField(LinkDesc) # social media like youtube twiter 
#     desc = db.StringField(max_length=1000,default='')

#     def __unicode__(self):
#         return self.statment 
#     def __repr__(self):
#         return self.statment 
#     def __str__(self):
#         return self.statment
#     def __dict__(self):
#         #Keywords
#         ky = []
#         for i in self.keywords:
#             ky.append(i.__dict__())
#         #area
#         ar = []
#         for i in self.area:
#             ar.append(i.__dict__())
#         #applications
#         app = []
#         for i in self.applications:
#             app.append(i.__dict__())
#         #journals_conf
#         jc = []
#         for i in self.journals_conf:
#             jc.append(i.__dict__())
#         #code_links
#         cl = []
#         for i in self.code_links:
#             cl.append(i.__dict__())
#         #datasets_links
#         dsl = []
#         for i in self.datasets_links:
#             dsl.append(i.__dict__())
#         #peoples
#         pp = []
#         for i in self.peoples:
#             pp.append(i.__dict__())
#         #articals
#         art = []
#         for i in self.articals:
#             art.append(i.__dict__())
#         #resoures
#         res = []
#         for i in self.resoures:
#             res.append(i.__dict__())
#         #sm
#         s = []
#         for i in self.sm:
#             s.append(i.__dict__())
#         return {
#             'key_str':self.statment   # It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
#             ,'statment':self.statment
#             ,'date_created':self.date_created
#             ,'keywords':ky
#             ,'area':ar
#             ,'applications':app
#             ,'journals_conf':jc
#             ,'code_links':cl
#             ,'datasets_links':dsl
#             ,'peoples':pp
#             ,'articals':art
#             ,'resoures':res
#             ,'social_media':s
#         }

# class PaperPerson(db.EmbeddedDocument):
#     name = db.StringField(max_length=100,default='')
#     title = db.StringField(max_length=10,default='')# Mr. Ms. Miss
#     position = db.StringField(max_length=20,default='')# Dr. Prof
#     corresponding = db.BooleanField(required=True, default=False)
#     sequence = db.IntField(required=True, default=0)
#     gender = db.StringField(max_length=10,default='')
#     affiliation = db.EmbeddedDocumentField(LinkDesc)
#     ph = db.StringField(max_length=100,default='')
#     email = db.EmailField()
#     #user_id = db.StringField(max_length=100,default='') # ref to objectid of user document if any
#     #user_id = db.ObjectID()
#     webpage = db.EmbeddedDocumentField(LinkDesc)
#     sm = db.EmbeddedDocumentListField(LinkDesc) # social media like youtube twiter 

#     def __unicode__(self):
#         return self.name 
#     def __repr__(self):
#         return self.name 
#     def __str__(self):
#         return self.name
#     def __dict__(self):
#         #affiliation
#         aff = []
#         for i in self.affiliation:
#             aff.append(i.__dict__())
#         #webpage
#         wb = []
#         for i in self.webpage:
#             wb.append(i.__dict__())
#         #social_media
#         s = []
#         for i in self.sm:
#             s.append(i.__dict__())
#         return {
#             'key_str':self.name   # It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
#             ,'title':self.title
#             ,'position':self.position
#             ,'corresponding':self.corresponding
#             ,'sequence':self.sequence
#             ,'gender':self.gender
#             ,'affiliation':aff
#             ,'phone':self.ph
#             ,'email':self.email
#             ,'webpage':wb
#             ,'social_media':s
#         }

# class PaperRefFile(db.EmbeddedDocument): # file that has been uploaded and save in server file system
#     name = db.StringField(max_length=100,default='') # It should be unique in file system diroctory
#     articaltype = db.StringField(max_length=100,default='') # Journal / Conference / Book / Other
#     year = db.IntField(required=True, default=0)
#     path = db.StringField(max_length=100,default='') # full path to file
#     mimetype = db.StringField(max_length=50,default='') # text/plain,application/pdf, application/octet-stream meaning “download this file”
#     link = db.URLField() # url DOI etc
#     bibtext = db.StringField(max_length=1000,default='')
#     uptime = db.DateTimeField(default=datetime.utcnow,
#                                         help_text='date and time the file was uploaded')
#     desc = db.StringField(max_length=500,default='')

#     def __unicode__(self):
#         return self.name 
#     def __repr__(self):
#         return self.name 
#     def __str__(self):
#         return self.name
#     def __dict__(self):
#         return {
#             'key_str':self.name   # It is PK and index key in EmbeddedDocument IndustryCollaboration. It is used for edit update, delete opration.
#             ,'articaltype':self.articaltype
#             ,'year':self.year
#             ,'path':self.path
#             ,'mimetype':self.mimetype
#             ,'link':self.link
#             ,'bibtext':self.bibtext
#             ,'uptime':self.uptime
#             ,'desc':self.desc
#         }

# class PaperFile(db.EmbeddedDocument): # file that has been uploaded and save in server file system
#     name = db.StringField(max_length=100,default='') # It should be unique in file system diroctory
#     type = db.StringField(max_length=100,default='') # Manuscript / Figure /Dataset / Bibtext / Tables / Template /cover letter / proof / plagiarism report / comments /replay / camera ready / published
#     path = db.StringField(max_length=100,default='') # full path to file
#     mimetype = db.StringField(max_length=50,default='') # text/plain,application/pdf, application/octet-stream meaning “download this file”
#     link = db.URLField() # url if any in case of dataset from repository
#     uptime = db.DateTimeField(default=datetime.utcnow,
#                                         help_text='date and time the file was uploaded')
#     desc = db.StringField(max_length=1000,default='')

#     def __unicode__(self):
#         return self.name 
#     def __repr__(self):
#         return self.name 
#     def __str__(self):
#         return self.name
#     def __dict__(self):
#         return {
#             'key_str':self.name   # It is PK.
#             ,'type':self.type
#             ,'path':self.path
#             ,'mimetype':self.mimetype
#             ,'link':self.link
#             ,'uptime':self.uptime
#             ,'desc':self.desc
#         }

# class PaperSubmittedinJournalComment(db.EmbeddedDocument):
#     title = db.StringField(max_length=500,default='')  
#     authors = db.EmbeddedDocumentListField(PaperPerson)
#     revisionno = db.IntField(required=True, default=0) # No 0 in first submission
#     comment = db.StringField(max_length=1000,default='') # No cooments in first submission
#     uptime = db.DateTimeField(default=datetime.utcnow,
#                                         help_text='submission date and time')
#     reviewers = db.EmbeddedDocumentListField(PaperPerson)
#     editors = db.EmbeddedDocumentListField(PaperPerson)
#     submittedfiles = db.EmbeddedDocumentListField(PaperFile) 

#     def __unicode__(self):
#         return self.title 
#     def __repr__(self):
#         return self.title 
#     def __str__(self):
#         return self.title
#     def __dict__(self):
#         #authors
#         au = []
#         for i in self.authors:
#             au.append(i.__dict__())
#         #reviewers
#         re = []
#         for i in self.reviewers:
#             re.append(i.__dict__())
#         #editors
#         ed = []
#         for i in self.editors:
#             ed.append(i.__dict__())
#         #submittedfiles
#         sf = []
#         for i in self.submittedfiles:
#             sf.append(i.__dict__())
#         return {
#             'key_str':self.title   # It is PK.
#             ,'authors':au
#             ,'revisionno':self.revisionno
#             ,'comment':self.comment
#             ,'uptime':self.uptime
#             ,'reviewers':re
#             ,'editors':ed
#             ,'submittedfiles':sf
#         }

# class PaperSubmittedinJournal(db.EmbeddedDocument):
#     name = db.StringField(max_length=200,default='')
#     mode = db.StringField(max_length=20,default='') # Open access / free / hybried / paied etc
#     specialissue = db.EmbeddedDocumentField(LinkDesc)#db.StringField(max_length=200,default='')
#     link = db.URLField() # url
#     submissionlink = db.StringField(max_length=100,default='')
#     subtemplate = db.EmbeddedDocumentField(PaperFile) # type : template
#     publisher = db.StringField(max_length=200,default='')
#     indexing = db.StringField(max_length=20,default='') # SCI / SCIE / ESCI / Scoups / Others
#     score = db.DecimalField(precision=2,default=0)
#     indexingproof = db.EmbeddedDocumentField(PaperFile) # type : indexingprof
#     username = db.StringField(max_length=50,default='')
#     papersubmittedinjournalcomments = db.EmbeddedDocumentListField(PaperSubmittedinJournalComment)

#     def __unicode__(self):
#         return self.name
#     def __repr__(self):
#         return self.name 
#     def __str__(self):
#         return self.name
#     def __dict__(self):
#         #papersubmittedinjournalcomments
#         psjc = []
#         for i in self.papersubmittedinjournalcomments:
#             psjc.append(i.__dict__())
#         return {
#             'key_str':self.name   # It is PK.
#             ,'mode':self.mode
#             ,'specialissue':self.specialissue.__dict__()
#             ,'link':self.link
#             ,'submissionlink':self.submissionlink
#             ,'subtemplate':self.subtemplate.__dict__()
#             ,'publisher':self.publisher
#             ,'indexing':self.indexing
#             ,'score':self.score
#             ,'indexingproof':self.indexingproof.__dict__()
#             ,'username':self.username
#             ,'papersubmittedinjournalcomments':psjc
#         }
    
# class PaperSubmittedinConferenceComment(db.EmbeddedDocument):
#     title = db.StringField(max_length=500,default='') 
#     authors = db.EmbeddedDocumentListField(PaperPerson)
#     revisionno = db.IntField(required=True, default=0) # No 0 in first submission
#     comment = db.StringField(max_length=1000,default='') # No cooments in first submission
#     uptime = db.DateTimeField(default=datetime.utcnow,
#                                         help_text='submission date and time')
#     members = db.EmbeddedDocumentListField(PaperPerson)
#     submittedfiles = db.EmbeddedDocumentListField(PaperFile)  # cooments file and reply file with text in desc field

#     def __unicode__(self):
#         return self.title 
#     def __repr__(self):
#         return self.title 
#     def __str__(self):
#         return self.title
#     def __dict__(self):
#         #authors
#         au = []
#         for i in self.authors:
#             au.append(i.__dict__())
#         #editors
#         me = []
#         for i in self.members:
#             me.append(i.__dict__())
#         #submittedfiles
#         sf = []
#         for i in self.submittedfiles:
#             sf.append(i.__dict__())
#         return {
#             'key_str':self.title   # It is PK.
#             ,'authors':au
#             ,'revisionno':self.revisionno
#             ,'comment':self.comment
#             ,'uptime':self.uptime
#             ,'editors':me
#             ,'submittedfiles':sf
#         }

# class PaperSubmittedinConference(db.EmbeddedDocument):
#     name = db.StringField(max_length=200,default='')
#     confnumber = db.StringField(max_length=200,default='') # eg IEEE confrence ID
#     deadline = db.DateTimeField(default=datetime.utcnow,
#                                         help_text='submission Deadline date and time')
#     sdate = db.DateTimeField(default=datetime.utcnow,
#                                         help_text='conference is scheduled on date and time')
#     edate = db.DateTimeField(default=datetime.utcnow,
#                                         help_text='conference is closed on date and time')
#     city = db.StringField(max_length=50,default='')
#     confadd = db.StringField(max_length=200,default='')
#     link = db.URLField()
#     submissionlink = db.StringField(max_length=100,default='')
#     subtemplate = db.EmbeddedDocumentField(PaperFile) # type : template
#     publisher = db.StringField(max_length=200,default='')
#     indexing = db.StringField(max_length=20,default='') # SCI / SCIE / ESCI / Scoups / Others
#     indexingproof = db.EmbeddedDocumentField(PaperFile) # type : indexingprof
#     username = db.StringField(max_length=50,default='')
#     papersubmittedinconferencecomments = db.EmbeddedDocumentListField(PaperSubmittedinConferenceComment)

#     def __unicode__(self):
#         return self.name
#     def __repr__(self):
#         return self.name 
#     def __str__(self):
#         return self.name
#     def __dict__(self):
#         #papersubmittedinconferencecomments
#         pscc = []
#         for i in self.papersubmittedinconferencecomments:
#             pscc.append(i.__dict__())
#         return {
#             'key_str':self.name   # It is PK.
#             ,'confnumber':self.confnumber
#             ,'deadline':self.deadline
#             ,'sdate':self.sdate
#             ,'edate':self.edate
#             ,'city':self.city
#             ,'confadd':self.confadd
#             ,'link':self.link
#             ,'submissionlink':self.submissionlink
#             ,'subtemplate':self.subtemplate.__dict__()
#             ,'publisher':self.publisher
#             ,'indexing':self.indexing
#             ,'indexingproof':self.indexingproof.__dict__()
#             ,'username':self.username
#             ,'papersubmittedinjournalcomments':pscc
#         }
      

# class PaperDiscussionBoardComment(db.EmbeddedDocument):
#     name = db.StringField(max_length=50,default='') # Who post it
#     uptime = db.DateTimeField(default=datetime.utcnow,
#                                         help_text='comment date and time')
#     desc = db.StringField(max_length=1000,default='')

#     def __unicode__(self):
#         return self.name
#     def __repr__(self):
#         return self.name 
#     def __str__(self):
#         return self.name
#     def __dict__(self):
#         return {
#             'key_str':self.name   # It is PK.
#             ,'uptime':self.uptime
#             ,'username':self.desc
#         }
# ################################### paper class Document in Mongodb #########################
# class Paper(db.Document):
#     title = db.StringField(max_length=500,default='')  # PK
#     rp = db.EmbeddedDocumentField(ResearchProblem)
#     status = db.StringField(max_length=50,default='') # Formulating / Simulation / Writing /Submitted / Comments Recived / Wating for reply / Accepted /Rejected
#     date_created = db.DateTimeField(default=datetime.utcnow,
#                                         help_text='date the Paper was created')
#     authors = db.EmbeddedDocumentListField(PaperPerson)
#     #bibfile = db.StringField(max_length=100,default='') # Biblography/references file
#     reffiles = db.EmbeddedDocumentListField(PaperRefFile)
#     discussionboard = db.EmbeddedDocumentListField(PaperDiscussionBoardComment)
#     ################################ paper writing / simulation #######################
#     bibtext = db.EmbeddedDocumentListField(PaperFile)
#     ownwork = db.EmbeddedDocumentListField(PaperFile)
#     litrature = db.EmbeddedDocumentListField(PaperFile)
#     result = db.EmbeddedDocumentListField(PaperFile)
#     futurescope = db.EmbeddedDocumentListField(PaperFile)
#     intro = db.EmbeddedDocumentListField(PaperFile)
#     abstract = db.EmbeddedDocumentListField(PaperFile)
#     ############################ paper submission ##################################
#     journals = db.EmbeddedDocumentListField(PaperSubmittedinJournal)
#     conferences = db.EmbeddedDocumentListField(PaperSubmittedinConference)
#     ######################### paper accepted  #########################
#     acceptance = db.EmbeddedDocumentField(PaperFile) # acceptance letter or email
#     cameraready = db.EmbeddedDocumentField(PaperFile)
#     published = db.EmbeddedDocumentField(PaperFile)
#     link = db.URLField()

#     def __unicode__(self):
#         return self.title
#     def __repr__(self):
#         return self.title 
#     def __str__(self):
#         return self.title
#     def __dict__(self):
#         #papersubmittedinconferencecomments
#         au = []
#         for i in self.authors:
#             au.append(i.__dict__())
#         #reffiles
#         rf = []
#         for i in self.reffiles:
#             rf.append(i.__dict__())
#         #discussionboard
#         disb = []
#         for i in self.discussionboard:
#             disb.append(i.__dict__())
#         #bibtext
#         bt = []
#         for i in self.bibtext:
#             bt.append(i.__dict__())
#         #ownwork
#         ow = []
#         for i in self.ownwork:
#             ow.append(i.__dict__())
#         #litrature
#         lt = []
#         for i in self.litrature:
#             lt.append(i.__dict__())
#         #result
#         r = []
#         for i in self.result:
#             r.append(i.__dict__())
#         #futurescope
#         fs = []
#         for i in self.futurescope:
#             fs.append(i.__dict__())
#         #intro
#         io = []
#         for i in self.intro:
#             io.append(i.__dict__())
#         #abstract
#         ab = []
#         for i in self.abstract:
#             ab.append(i.__dict__())
#         #journals
#         j = []
#         for i in self.journals:
#             j.append(i.__dict__())
#         #conferences
#         c = []
#         for i in self.conferences:
#             c.append(i.__dict__())
#         return {
#             'key_str':self.title   # It is PK.
#             ,'confnumber':self.rp.__dict__()
#             ,'status':self.status
#             ,'date_created':self.date_created
#             ,'authors':au
#             ,'reffiles':rf
#             ,'discussionboard':disb
#             ,'bibtext':bt
#             ,'ownwork':ow
#             ,'litrature':lt
#             ,'result':r
#             ,'futurescope':fs
#             ,'intro':io
#             ,'abstract':ab
#             ,'journals':j
#             ,'conferences':c
#             ,'acceptance':self.acceptance.__dict__()
#             ,'cameraready':self.cameraready.__dict__()
#             ,'published':self.published.__dict__()
#             ,'link':self.link
#         }
