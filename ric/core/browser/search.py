# -*- coding: utf-8 -*-

from plone import api
from zope.component import getMultiAdapter
from z3c.form import button, form, field
from plone.z3cform.layout import wrap_form
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from ric.core import RICMessageFactory as _
from ric.core.browser.interfaces import IRICSearch


class RICNoSearchFormView(BrowserView):
    """
    View displayed for anonymous user, asking them to connect
    """


class RICSearchForm(form.Form):

    fields = field.Fields(IRICSearch)
    label = _(u"Recherche dans l'annuaire du RIC")
    template = ViewPageTemplateFile('templates/search.pt')
    ignoreContext = True
    _data = None
    canSearch = False
    personsToComplete = []
    organizationsToComplete = []

    def update(self):
        self.personsToComplete = []
        self.organizationsToComplete = []

        if api.user.is_anonymous():
            self.request.response.redirect("%s/@@nosearch" % self.context.absolute_url())
            return ''
        user = api.user.get_current()
        if user.has_role('Manager') or api.user.has_permission('RIC: Administer website', user=user):
            self.canSearch = True
        else:
            persons = getMultiAdapter((self.context, self.request),
                                      name="get_persons_for_user")(userName=user.getUserName())
            # if user has a profile
            if persons:
                for person in persons:
                    isCompleted = getMultiAdapter((person, self.request),
                                                  name="is_profile_completed")()
                    if not isCompleted:
                        self.personsToComplete.append(person)

                organizations = getMultiAdapter((self.context, self.request),
                                                name="get_organizations_for_user")()
                for organization in organizations:
                    isCompleted = getMultiAdapter((organization, self.request),
                                                  name="is_profile_completed")()
                    if not isCompleted:
                        self.organizationsToComplete.append(organization)

                if not self.personsToComplete and not self.organizationsToComplete:
                    self.canSearch = True

        super(RICSearchForm, self).update()

    @button.buttonAndHandler(_(u'Rechercher'))
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            return False
        self._data = data

    def getResults(self):
        if self._data is None:
            return None
        form = self._data
        contentType = form.get('contentType')
        contentName = form.get('contentName')
        contentName = '*%s*' % contentName
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog.searchResults(portal_type=contentType,
                                       Title=contentName)[:20]
        return brains

RICSearchFormView = wrap_form(RICSearchForm)
