# -*- coding: utf-8 -*-
#utilities

from Products.CMFCore.utils import getToolByName
from plone import api


def sge_recent(self, count=10):
    """
        Recently modified search without some portal_types
    """
    catalog = getToolByName(self, 'portal_catalog')
    utils = getToolByName(self, 'plone_utils')
    friendly_types = utils.getUserFriendlyTypes()
    friendly_types.remove('PloneboardComment')
    friendly_types.remove('PloneboardForum')
    user = api.user.get_current()
    if user.has_role('Manager') or api.user.has_permission('RIC: Administer website', user=user):
        for typ in ['directory', 'held_position', 'organization', 'person', 'position']:
            friendly_types.append(typ)
    count = int(count)
    return catalog(portal_type=friendly_types,
                   sort_on='modified',
                   sort_order='reverse',
                   sort_limit=count)[:count]
