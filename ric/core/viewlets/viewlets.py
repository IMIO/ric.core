from AccessControl import getSecurityManager
from plone import api
from zope.component import getMultiAdapter
from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class RICViewletBase(ViewletBase):

    def viewletsToShowTomanager(self):
        context = self.context
        if context.portal_type not in ['organization', 'person']:
            return None
        sm = getSecurityManager()
        if sm.checkPermission('RIC: Administer website', context):
            return context.portal_type
        return None


class CotisationViewlet(RICViewletBase):
    render = ViewPageTemplateFile('cotisation.pt')
    organizations = []
    isManager = False

    def available(self):
        self.organizations = []
        self.isManager = False
        catalog = api.portal.get_tool('portal_catalog')
        if self.viewletsToShowTomanager() == 'organization':
            self.isManager = True
            persons = catalog.searchResults(portal_type="person",
                                            path={'query': '/'.join(self.context.getPhysicalPath()),
                                                  'depth': 1})
            for person in persons:
                if 'contact_cotisation' in person.getObject().multimail:
                    return False
            self.organizations = [self.context]
            return True
        else:
            organizations = getMultiAdapter((self.context, self.request),
                                            name="get_organizations_for_user")()
            if not organizations:
                return False
            for organization in organizations:
                persons = catalog.searchResults(portal_type="person",
                                                path={'query': '/'.join(organization.getPhysicalPath()),
                                                      'depth': 1})
                contactCotisation = False
                for person in persons:
                    personObj = person.getObject()
                    if 'contact_cotisation' in personObj.multimail:
                        contactCotisation = True
                        break
                if not contactCotisation:
                    self.organizations.append(organization)
            return bool(self.organizations)


class ProfileViewlet(RICViewletBase):
    render = ViewPageTemplateFile('profile.pt')
    persons = []
    organizations = []
    isManager = False

    def available(self):
        self.persons = []
        self.organizations = []
        self.isManager = False
        if self.viewletsToShowTomanager() == 'organization':
            self.isManager = True
            isCompleted = getMultiAdapter((self.context, self.request),
                                          name="is_profile_completed")()
            if not isCompleted:
                self.organizations = [self.context]
                return True
            return False
        elif self.viewletsToShowTomanager() == 'person':
            self.isManager = True
            isCompleted = getMultiAdapter((self.context, self.request),
                                          name="is_profile_completed")()
            if not isCompleted:
                self.persons = [self.context]
                return True
            return False
        persons = getMultiAdapter((self.context, self.request),
                                  name="get_persons_for_user")()
        for person in persons:
            isCompleted = getMultiAdapter((person, self.request),
                                          name="is_profile_completed")()
            if not isCompleted:
                self.persons.append(person)
        organizations = getMultiAdapter((self.context, self.request),
                                        name="get_organizations_for_user")()
        for organization in organizations:
            isCompleted = getMultiAdapter((organization, self.request),
                                          name="is_profile_completed")()
            if not isCompleted:
                self.organizations.append(organization)
        return bool(self.persons or self.organizations)


class EmailViewlet(RICViewletBase):
    render = ViewPageTemplateFile('email.pt')
    persons = []

    def available(self):
        self.persons = []
        persons = getMultiAdapter((self.context, self.request),
                                  name="get_persons_for_user")()
        if not persons:
            return False
        for person in persons:
            if person.invalidmail:
                self.persons.append(person)
        return bool(self.persons)
