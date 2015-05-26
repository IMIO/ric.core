# -*- coding: utf-8 -*-

from zope.interface import implements
from zope.component import adapts
from borg.localrole.interfaces import ILocalRoleProvider
from plone import api
from dexterity.membrane.behavior.membranegroup import IMembraneGroup


class MembraneGroupRoleProvider(object):
    """
    Set local roles for membrane group members
    """
    implements(ILocalRoleProvider)
    adapts(IMembraneGroup)

    _default_roles = ('Contributor',
                      'Reviewer',
                      'Reader',
                      'Editor',
                      'RICActualOrganizationMember')

    def __init__(self, context):
        self.context = context

    def getRoles(self, user_id):
        """
        """
        if user_id in [person.userid for person in self._getAllPersons()]:
            return self._default_roles
        else:
            return ()

    def getAllRoles(self):
        """Here we should apparently enumerate all users who should
        get an extra role.
        """
        persons = self._getAllPersons()
        for person in persons:
            yield person.userid, self._default_roles

    def _getAllPersons(self):
        catalog = api.portal.get_tool('portal_catalog')
        persons = catalog.searchResults(portal_type="person",
                                        path={'query': '/'.join(self.context.getPhysicalPath()),
                                              'depth': 1})
        return [person.getObject() for person in persons]
