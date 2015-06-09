# -*- coding: utf-8 -*-
#utilities

from slugify import slugify, Slugify
from Products.CMFPlone.utils import safe_unicode
from Products.CMFCore.utils import getToolByName
from Products.CPUtils.Extensions.utils import check_zope_admin
from imio.helpers.security import generate_password


def import_organization(self, dochange=''):
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


def import_person(self, dochange=''):
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
    subs = {}

    portal = getToolByName(self, "portal_url").getPortalObject()
    if 'person_list' not in portal.objectIds():
        return "You must create a DTMLDocument containing the list of persons to create"
    pc = portal.portal_catalog
    slug = Slugify(to_lower=True, safe_chars="()-'", separator=' ')
    lines = portal.person_list.raw.splitlines()
    for line in lines:
        line = line.strip(' \n')
        if not line:
            continue
        (userid, email, nom, prenom, typ, orga, groupe) = line.split(';')
        sortable_title = slug('%s %s' % (typ, orga))
        brains = pc(portal_type='organization', sortable_title=sortable_title)
        if not brains:
            out.append("Cannot find organization '%s %s' with '%s'" % (typ, orga, sortable_title))
            continue
        elif len(brains) > 1:
            out.append("Find multiple organization '%s'" % ', '.join([brain.Title for brain in brains]))
            continue
        orga = brains[0].getObject()
        gen_id = slugify('%s %s' % (nom, prenom), to_lower=True)
        out.append("Will create person: '%s %s' with id '%s'" % (nom, prenom, gen_id.encode('utf8')))
        if real:
            orga.invokeFactory('person', id=gen_id, firstname=prenom.decode('utf8'), lastname=nom.decode('utf8'),
                               email=email, userid=userid, invalidmail=False)
            obj = orga[gen_id]
            obj.reindexObject()
        if orga.id not in subs:
            subs[orga.id] = {}
        groups = eval(groupe)
        if 'cotisants2012-2013' in groups:
            subs[orga.id][2012] = True
        if 'cotisants2013-2014' in groups:
            subs[orga.id][2013] = True
        if 'cotisants2014-2015' in groups:
            subs[orga.id][2014] = True

    tots = {2012: 0, 2013: 0, 2014: 0}
    for gen_id in subs:
        brains = pc(portal_type='organization', id=gen_id)
        if len(brains) != 1:
            out.append('Cannot find organization with id %s' % gen_id.encode('utf8'))
            continue
        brain = brains[0]
        res = []
        for year in sorted(subs[gen_id].keys()):
            res.append({'payment': True, 'year': year})
            tots[year] += 1
        if not res: continue
        out.append("For orga %s, subscriptions=%s" % (brain.Title.encode('utf8'), res))
        if real:
            brain.getObject().subscriptions = res
    out.append('')
    for year in sorted(tots.keys()):
        out.append("Year %d: %d subscriptions" % (year, tots[year]))
    return '\n'.join(out)
