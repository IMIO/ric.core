# -*- coding: utf-8 -*-

from zope.component import adapts
from zope.interface import implements
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from z3c.form.interfaces import IEditForm, IAddForm, IForm
from AccessControl import getSecurityManager
from plone.z3cform.fieldsets import extensible
from plone.z3cform.fieldsets.interfaces import IFormExtender


class ContactFormExtender(extensible.FormExtender):
    implements(IFormExtender)
    adapts(Interface, IDefaultBrowserLayer, IForm)

    def __init__(self, context, request, form):
        self.context = context
        self.request = request
        self.form = form

    def update(self):
        isForm = IEditForm.providedBy(self.form) or IAddForm.providedBy(self.form)
        if not isForm:
            return

        if not hasattr(self.form, 'portal_type'):
            return

        if self.form.portal_type == 'organization':
            self.remove('logo')
            self.remove('activity')
            self.remove('IContactDetails.im_handle')
            self.remove('IContactDetails.country')
            self.remove('IContactDetails.cell_phone')
            self.remove('IContactDetails.fax')
            self.remove('IContactDetails.region')
            sm = getSecurityManager()
            if not sm.checkPermission('RIC: Administer website', self.context):
                self.form.fields['IBasic.title'].mode = 'display'
            contactFields = self.form.groups[0].fields
            #contactFields['IContactDetails.email'].field.required = True

        elif self.form.portal_type == 'person':
            self.remove('gender')
            self.remove('person_title')
            self.remove('photo')
            self.remove('IContactDetails.im_handle')
            self.remove('IContactDetails.fax')
            self.remove('IContactDetails.country')
            self.remove('IContactDetails.region')
            self.remove('IContactDetails.website')
            self.form.fields['firstname'].field.required = True
            contactFields = self.form.groups[0].fields
            contactFields['IContactDetails.email'].field.required = True
