# -*- coding: utf-8 -*-

from plone import api
from zope.component import getUtility
from zope.interface import alsoProvides
from plone.uuid.interfaces import IAttributeUUID, IMutableUUID, IUUIDGenerator


def addUUIDOnPortal(portal):
    if not IAttributeUUID.providedBy(portal):
        alsoProvides(portal, IAttributeUUID)
    uuid_adapter = IMutableUUID(portal)
    if uuid_adapter.get() is None:
        generator = getUtility(IUUIDGenerator)
        uuid = generator()
        uuid_adapter.set(uuid)


def changeSearchedTypes(site):
    """
        Change searched types
    """
    to_show = []
    to_hide = ['directory', 'held_position', 'organization', 'person', 'position']
    not_searched = list(site.portal_properties.site_properties.types_not_searched)
    for typ in to_show:
        if typ in not_searched:
            not_searched.remove(typ)
    for typ in to_hide:
        if typ not in not_searched:
            not_searched.append(typ)
    site.portal_properties.site_properties.manage_changeProperties(types_not_searched=not_searched)


def installCore(context):
    if context.readDataFile('ric.core-default.txt') is None:
        return

    membrane = api.portal.get_tool('membrane_tool')
    membrane.membrane_types = ['person']

    # Set all Authenticated Users as Member, because Membrane remove Member
    # role to Persons
    groupstool = api.portal.get_tool('portal_groups')
    groupstool.editGroup("AuthenticatedUsers", roles=["Member"], groups=())

    portal = context.getSite()
    addUUIDOnPortal(portal)
    changeSearchedTypes(portal)
