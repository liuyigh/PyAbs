# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

## app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)


if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## choose a style for forms
response.formstyle = myconf.take('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.take('forms.separator')


## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)

auth.settings.extra_fields['auth_user']= [
  Field('piFirst'),
  Field('piLast'),
  Field('department'),
  Field('institution'),
  Field('zipcode')]

service = Service()
plugins = PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.take('smtp.server')
mail.settings.sender = myconf.take('smtp.sender')
mail.settings.login = myconf.take('smtp.login')

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

# db.define_table('auth_criteria',
#    Field('user_id', 'reference auth_user', readable=False, writable=False),
#    Field('salePrice', 'integer', widget=SQLFORM.widgets.radio.widget, requires = IS_IN_SET(salePrice)),
#    Field('tgPrice', 'integer', widget=SQLFORM.widgets.radio.widget, requires = IS_IN_SET(tgPrice)),
#    Field('aveRev', 'integer', requires = IS_IN_SET(aveRev)),
#    Field('percSave', 'integer', requires = IS_IN_SET(percSave)),
#    Field('toSend','integer', readable=False, writable=False))
# db.auth_criteria.user_id.requires = IS_IN_DB(db, db.auth_user.id)
# db.auth_criteria.id.readable=False 

storeTemp = {
    0: '4C',
    1: '-20C',
    2: '-80C'
}

fl = {
    1: 'FL1: FITC',
    2: 'FL2: PE',
    3: 'FL3: PE-Cy7',
    4: 'FL4: APC',
    5: 'FL5: PB/eF450',
    6: 'FL6: AmCyan',
    7: 'FL7: PerCP-Cy5.5',
    8: 'FL8: APC-Cy7',
    9: 'FL9: PE-TexasRed',
    10: 'FL10: Alexa-700',
    11: '',
    12: '',
    13: '',
    14: '',
}

db.define_table('box',
   Field('labId', 'reference auth_user', readable=False, writable=False),
   Field('temprature', 'integer', widget=SQLFORM.widgets.radio.widget, requires = IS_IN_SET(storeTemp)),
   Field('storeLoc','string')
   )

db.define_table('antibody',
   Field('antigen', 'string'),
   Field('fluorophore', 'string'),
   Field('fl', 'integer', requires = IS_IN_SET(fl)),
   Field('vendor','integer', requires = IS_IN_SET(fl)),
   Field('catNo','string'),
   Field('species','integer'),
   Field('reaction','integer'),
   Field('concentration','double'),
   Field('recomDose','double'),
   Field('pracDose','double')
   )

db.define_table('panel',
   Field('labId', 'reference auth_user', readable=False, writable=False),
   Field('description', 'string'),
   Field('instrument', 'string'),
   Field('dateDesign','date', writable=False),
   Field('gateExample', 'blob', readable=False, writable=False),
   Field('pubPriv', 'integer', readable=False, writable=False),
   Field('panelRef', readable=False, writable=False))

db.define_table('paAb',
   Field('panelId', 'reference panel', readable=False, writable=False),
   Field('abId', 'reference antibody', readable=False, writable=False)
   )

db.define_table('boAb',
   Field('boxId', 'reference box', readable=False, writable=False),
   Field('abId','reference antibody', readable=False, writable=False),
   Field('orderDate','date'),
   Field('orderPerson','string'),
   Field('expireDate','date'))

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
