# -*- coding: utf-8 -*-
#utilities

from Products.CMFCore.utils import getToolByName
from Products.CPUtils.Extensions.utils import check_zope_admin
from imio.helpers.security import generate_password


def import_organization(self, dochange=''):
    """
        Recently modified search without some portal_types
    """
    if not check_zope_admin():
        return "You must be a zope manager to run this script"
    out = []
    if not dochange:
        out.append("To really import, call the script with param:")
        out.append("-> dochange=1")
        out.append("by example ...?dochange=1\n")
    real = False
    if dochange not in ('', '0', 'False', 'false'):
        real = True

    portal = getToolByName(self, "portal_url").getPortalObject()
    if 'organization_list' not in portal.objectIds():
        return "You must create a DTMLDocument containing the list of organizations to create"
    annuaire = portal.annuaire
    lines = portal.organization_list.raw.splitlines()
    for line in lines:
        line = line.strip(' \n')
        if not line:
            continue
        (orga, prov, pop) = line.split(';')
        for typ in (u'ac', u'cpas'):
            gen_id = generate_password(length=20, upper=0, special=0, readable=False)
            out.append("Will create orga: '%s %s' with id '%s'" % (typ, orga.decode('utf8'), gen_id))
            if real:
                annuaire.invokeFactory('organization', id=gen_id, title=orga.decode('utf8'),
                                       province=prov.decode('utf8'), citizen=int(pop), organization_type=typ,
                                       use_parent_address=False)
                obj = annuaire[gen_id]
                obj.reindexObject()
    return '\n'.join(out)
