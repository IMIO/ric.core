# -*- coding: utf-8 -*-

from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from collective.contact.core.content.organization import Organization


class RICOrganization(Organization):

    def Title(self):
        if self.organization_type:
            factory = getUtility(IVocabularyFactory, 'OrganizationTypesOrLevels')
            voc = factory(self)
            return "%s %s" % (voc.getTerm(self.organization_type).title, self.title)
        else:
            return self.title
