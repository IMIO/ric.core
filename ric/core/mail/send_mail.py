# -*- coding: utf-8 -*-
from datetime import datetime
from dateutil.relativedelta import relativedelta
from five import grok
from plone import api
from plone.api.portal import show_message
from plone.registry.interfaces import IRegistry
from ric.core import RICMessageFactory as _
from ric.core import logger
from ric.core.mail import events
from zope.component import getUtility
from zope.event import notify
from zope.interface import Interface


grok.templatedir('templates')
grok.context(Interface)


class SendMail(grok.View):
    grok.name('send_mail')
    grok.require('cmf.ManagePortal')
    grok.template('send_mail')

    def update(self):
        filter = self.request.get('filter') or None
        if not filter:
            return

        recipients = self.send_mail(filter)
        message = _(u"Email sent to")
        message = '%s: %s' % (message, ', '.join(recipients))
        show_message(message, self.request, type='info')

    def send_mail(self, filter):
        """
        Fire the event to send mails
        """
        if filter == "non_contributor":
            year = int(self.request.get('option'))
            recipients = self.get_non_contributor_organizations_members(year)
            event = events.SendNonContributor(self.context, recipients)

        elif filter == "organization_members":
            organization = self.request.get('option')
            recipients = self.get_organization_members(organization)
            event = events.SendOrganizationMembers(self.context, recipients)

        elif filter == "non_connected_members":
            days = int(self.request.get('option'))
            recipients = self.get_non_connected_members(days)
            event = events.SendNonConnectedMembers(self.context, recipients)

        elif filter == "send_mail_field":
            fields = self.request.get('option')
            recipients = self.get_person_by_fields(fields)
            event = events.SendMailField(self.context, recipients)

        self._notify(event)
        return recipients

    @staticmethod
    def _notify(event):
        """
        Notify event
        """
        try:
            notify(event)
        except:
            raise(Exception(_(u"A problem occured when sending the email")))

    def get_non_contributor_organizations_members(self, year):
        """
        Return organizations that are not contributor at a specific year
        """
        organizations = self.get_all_organizations()
        non_contributors = []

        for organization in organizations:
            for subscription in organization.subscriptions:
                if subscription.get('year') == year and subscription.get('payment') is False:
                    non_contributors.extend(self.get_organization_members(organization.id))

        return non_contributors

    def get_organization_members(self, organization):
        """
        Return all members of a specific organization
        """
        portal_catalog = api.portal.get_tool('portal_catalog')
        queryDict = {}
        queryDict['portal_type'] = 'organization'
        queryDict['sort_on'] = 'getObjPositionInParent'
        queryDict['id'] = organization
        organization = portal_catalog.searchResults(queryDict)[0].getObject()

        queryDict = {}
        queryDict['portal_type'] = 'person'
        queryDict['path'] = {'query': '/'.join(organization.getPhysicalPath()),
                             'depth': 1}
        results = portal_catalog.searchResults(queryDict)
        return [result.getObject().email for result in results if not result.getObject().invalidmail]

    def get_non_connected_members(self, days):
        """
        Return members not seen since days time
        """
        mt = api.portal.get_tool('portal_membership')
        members = mt.listMembers()

        non_connected_members = []
        for m in members:
            date_limit = datetime.now() - relativedelta(days=+days)
            last_login_time = convert_datetime(m.getProperty('last_login_time'))
            if last_login_time < date_limit:
                non_connected_members.append(m)

        return [member.getProperty('email') for member in non_connected_members]

    def get_person_by_fields(self, fields):
        """
        Return all persons by 'send mail' field selected
        """
        portal_catalog = api.portal.get_tool('portal_catalog')
        queryDict = {}
        queryDict['portal_type'] = 'person'
        queryDict['sort_on'] = 'getObjPositionInParent'
        results = portal_catalog.searchResults(queryDict)
        persons = [result.getObject() for result in results]

        persons_by_fields = []

        for field in fields:
            for person in persons:
                if person.invalidmail:
                    continue
                if not person.multimail or field in person.multimail:
                    persons_by_fields.append(person.email)
        return list(set(persons_by_fields))

    def get_multimail_fields(self):
        """
        Return vocabulary values for multimail field
        """
        registry = getUtility(IRegistry)
        multimail = registry.get('ric.core.multimail', {})
        return [(i, multimail[i]) for i in multimail]

    def get_all_organizations(self):
        """
        Return all organizations registered on the site
        """
        portal_catalog = api.portal.get_tool('portal_catalog')
        queryDict = {}
        queryDict['portal_type'] = 'organization'
        queryDict['sort_on'] = 'getObjPositionInParent'
        results = portal_catalog.searchResults(queryDict)
        return [result.getObject() for result in results]

    @staticmethod
    def get_current_year():
        return str(datetime.now().year)


def convert_datetime(plone_datetime):
    """
    Convert zope DateTime to python datetime
    """
    return datetime(year=plone_datetime.year(),
                    month=plone_datetime.month(),
                    day=plone_datetime.day(),
                    hour=plone_datetime.hour(),
                    minute=plone_datetime.minute(),
                    second=int(plone_datetime.second()))
