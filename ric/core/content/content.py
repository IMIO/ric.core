# -*- coding: utf-8 -*-

from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from collective.contact.core.content.organization import Organization
from collective.contact.core.vocabulary import get_vocabulary, get_directory


class RICOrganization(Organization):

    def Title(self):
        if self.organization_type:
            directory = get_directory(self)
            voc = get_vocabulary(directory.organization_types)
            return "%s %s" % (voc.getTerm(self.organization_type).title, self.title)
        else:
            return self.title
