# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(B('Py',SPAN('Abs')),XML('&trade;&nbsp;'),
                  _class="navbar-brand",_href="http://pyabs.com/",
                  _id="pyabs-logo")
response.title = request.application.replace('_',' ').title()
response.subtitle = 'Antibody Management for Flow Cytometry (FACS)'

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Yi Liu <vievie@gmail.com>'
response.meta.description = 'Antibody Management for Flow Cytometry (FACS)'
response.meta.keywords = 'Antibody, Management, Flow Cytometry, FACS'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('Home'), False, URL('default', 'index'), [])
]

DEVELOPMENT_MENU = False

#########################################################################
## provide shortcuts for development. remove in production
#########################################################################

if DEVELOPMENT_MENU: _()

if "auth" in locals(): auth.wikimenu() 
