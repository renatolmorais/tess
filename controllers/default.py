# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------
import base64
import os
from hashlib import sha256
from time import sleep
import json
from tess import ocr,which

# ---- example index page ----
def index():
    #return dict(content = request.vars._filename)
    if request.vars.submit == "1":
        filename = request.vars._filename.filename
        extension = filename.split('.')[-1]
        filename = sha256(filename).hexdigest() + '.' + extension
        content = request.vars._filename.file.read()
        if not os.path.exists( request.folder + '/uploads/' + filename):
            with open(request.folder + '/uploads/' + filename,"wb") as fp:
                fp.write( content )
        content = 'couldn\'t read'
        if which('tesseract'):
            ret = os.popen2('tesseract "{0}" "{1}" > /dev/null 2>&1'.format(
                    request.folder + "/uploads/" + filename,
                    request.folder + "/static/" + filename
                    )
            )
            #content = base64.b64encode(content)#base64.b64encode(open(request.vars.filename,'rb').read())
            while not os.path.exists( request.folder + '/static/' + filename + '.txt' ): sleep(1)
            with open( request.folder + '/static/' + filename + '.txt' , 'r') as fp: content = fp.read()
            session.content = content
        redirect(URL('process'))
    return dict()

def process():
    return dict()

def process2():
    #return request.vars.arquivo.file.read()
    if not request.vars.token or request.vars.token != 'a1b2c3d4$': 
        return json.dumps(
            dict(
                status_code = 400,
                result = None,
            )
        )
    if request.vars.arquivo != None:
        if not which('tesseract'):
            return json.dumps(
                dict(
                    status_code = 200,
                    result = dict(
                        status = 1,
                        content = 'tesseract not present',
                    ),
                )
            )
        #filename = request.vars.arquivo.filename
        #extension = filename.split('.')[-1]
        #filename = sha256(filename).hexdigest() + '.' + extension
        content = request.vars.arquivo.file.read()
        #if not os.path.exists( request.folder + '/uploads/' + filename):
        #    with open(request.folder + '/uploads/' + filename,"wb") as fp:
        #        fp.write( content )
        #ret = os.popen2('tesseract "{0}" "{1}" > /dev/null 2>&1'.format(
        #        request.folder + "/uploads/" + filename,
        #        request.folder + "/static/" + filename
        #        )
        #)
        ret = ocr(content)
        #content = base64.b64encode(content)#base64.b64encode(open(request.vars.filename,'rb').read())
        content = 'couldn\'t read'
        #while not os.path.exists( request.folder + '/static/' + filename + '.txt' ): sleep(1)
        #with open( request.folder + '/static/' + filename + '.txt' , 'r') as fp: content = fp.read()
        return json.dumps(
            dict(
                status_code = 200,
                result = dict(
                    status = 0,
                    content = ret,
                )
            )
        )
    return json.dumps(
        dict(
            status_code = 400,
            result = None,
        )
    )

# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
