# -*- coding: utf-8 -*-

from collective.contact.core.content.organization import Organization
from collective.contact.core.content.person import Person
from collective.contact.core.vocabulary import get_vocabulary, get_directory


class RICOrganization(Organization):

    def Title(self):
        if self.organization_type:
            directory = get_directory(self)
            voc = get_vocabulary(directory.organization_types)
            return "%s %s" % (voc.getTerm(self.organization_type).title.encode('utf8'), self.title.encode('utf8'))
        else:
            return self.title.encode('utf8')


class RICPerson(Person):

    def Title(self):
        return "%s (%s)" % (self.get_title().encode('utf8'), self.__parent__.Title())
