# -*- coding: utf-8 -*-

from Acquisition import aq_parent
from AccessControl.unauthorized import Unauthorized
from plone import api
from Products.Five.browser import BrowserView


class UtilsView(BrowserView):
    """
    Utils view
    """
    importantFields = []

    def isProfileCompleted(self):
        """
        Calculates profile completion depending on important fields
        and return True if content is more than 85% completed
        """
        context = self.context
        completedFields = 0
        for field in self.importantFields:
            if getattr(context, field, None) is not None:
                completedFields += 1
        completion = float(completedFields) / len(self.importantFields)
        return completion > 0.85

    def getPersonsForUser(self, userName=None):
        """
        Returns Person objects associated to logged in user (if any)
        """
        if userName is None:
            userName = api.user.get_current().getUserName()
        membrane = api.portal.get_tool('membrane_tool')
        membraneInfos = membrane.unrestrictedSearchResults(getUserId=userName)
        persons_final = []
        if membraneInfos:
            try:
                # Temporary fix because of insufficient rights on parent
                # organization
                persons = [mi.getObject() for mi in membraneInfos]
            except Unauthorized:
                return
            for person in persons:
                # Temporary check because of membrane returning organization
                if person.portal_type == 'person':
                    persons_final.append(person)
        return persons_final

    def getOrganizationsForUser(self):
        """
        Returns Organization objects associated to Persons of logged in user
        (if any)
        """
        persons = self.getPersonsForUser()
        if not persons:
            return []
        parents = [aq_parent(person) for person in persons]
        parents_final = []
        for parent in parents:
            if parent.portal_type == 'organization':
                parents_final.append(parent)
        return parents_final


class OrganizationView(UtilsView):
    """
    """
    importantFields = ['title',
                       'description',
                       'organization_type',
                       'phone',
                       #'cell_phone',
                       #'fax',
                       'email',
                       'website',
                       'number',
                       'street',
                       'zip_code',
                       'city',
                       'region',
                       'citizen',
                       #'servers',
                       #'softwares',
                       ]


class PersonView(UtilsView):
    """
    """
    importantFields = ['lastname',
                       'firstname',
                       'birthday',
                       'phone',
                       'cell_phone',
                       'fax',
                       'email',
                       'website',
                       'number',
                       'street',
                       'zip_code',
                       'city',
                       'region']
