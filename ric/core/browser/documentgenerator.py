# -*- coding: utf-8 -*-
from collective.documentgenerator import _ as _dg
from collective.documentgenerator.helper.archetypes import ATDocumentGenerationHelperView


# # # HELPERS # # #

class DocumentGenerationDirectoryHelper(ATDocumentGenerationHelperView):
    """
        Helper for collective.contact.core directory
    """

    def __init__(self, context, request):
        super(DocumentGenerationDirectoryHelper, self).__init__(context, request)
        self.uids = {}
        self.pers = {}
        self.directory_path = '/'.join(self.real_context.getPhysicalPath())
        self.dp_len = len(self.directory_path)
        self.pc = self.portal.portal_catalog

    def get_organizations(self):
        """
            Return a list of organizations, ordered by path, with parent id.
            [(id, parent_id, obj)]
        """
        lst = []
        id = 0
        paths = {}
        for brain in self.pc.unrestrictedSearchResults(portal_type='organization', path=self.directory_path,
                                                       sort_on='path'):
            id += 1
            self.uids[brain.UID] = id
            obj = brain._unrestrictedGetObject()
            path = brain.getPath()[self.dp_len:]
            parts = path.split('/')
            p_path = '/'.join(parts[:-1])
            paths[path] = id
            p_id = ''
            if p_path:
                p_id = paths[p_path]
            lst.append((id, p_id, obj))
        return lst

    def get_persons(self):
        """
            Return a list of persons.
            [(id, obj)]
        """
        lst = []
        id = 0
        for brain in self.pc.unrestrictedSearchResults(portal_type='person', path=self.directory_path,
                                                       sort_on='sortable_title'):
            id += 1
            self.uids[brain.UID] = id
            self.pers[brain.getPath()[self.dp_len:]] = id
            obj = brain._unrestrictedGetObject()
            lst.append((id, obj))
        return lst

    def get_held_positions(self):
        """
            Return a list of held positions tuples.
            [(id, person_id, org_id, obj)]
        """
        lst = []
        id = 0
        for brain in self.pc.unrestrictedSearchResults(portal_type='held_position', path=self.directory_path,
                                                       sort_on='path'):
            id += 1
            self.uids[brain.UID] = id
            obj = brain._unrestrictedGetObject()
            # pers id
            path = brain.getPath()[self.dp_len:]
            parts = path.split('/')
            p_path = '/'.join(parts[:-1])
            p_id = self.pers[p_path]
            # org id
            org = obj.get_organization()
            org_id = ''
            if org:
                org_id = self.uids[org.UID()]
            lst.append((id, p_id, org_id, obj))
        return lst


# # # GENERATION VIEW # # #

