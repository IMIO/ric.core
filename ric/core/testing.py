# -*- coding: utf-8 -*-

from datetime import datetime

from DateTime import DateTime

from Products.CMFCore.utils import getToolByName

from plone import api
from plone.testing import z2
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneWithPackageLayer
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import (login,
                               TEST_USER_NAME,
                               setRoles,
                               TEST_USER_ID)

from Products.membrane.tests.base import MembraneProfilesLayer
import ric.core


class RICCorePloneWithPackageLayer(PloneWithPackageLayer, MembraneProfilesLayer):
    """
    plone (portal root)
    |
    `-- 1: Annuaire        (directory)
        |-- 2: Affinitic   (organization)
        |   |-- 3: Tintin  (person)
        |   `-- 3: Haddock
        |
        `-- 2: Imio
            `-- 3: Dupont
    """

    products = ('collective.contact.membrane', 'Products.membrane')

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        self.loadZCML(package=ric.core,
                      name='testing.zcml')
        z2.installProduct(app, 'collective.indexing')
        z2.installProduct(app, 'Products.membrane')

    def setUpPloneSite(self, portal):
        catalog = getToolByName(portal, 'portal_catalog')
        applyProfile(portal, 'ric.core:testing')

        position_types = [{'name': u'Secretaire', 'token': 'secretaire'},
                          {'name': u'President', 'token': 'president'}]
        organization_types = [{'name': u'ASBL', 'token': 'asbl'},
                              {'name': u'PME', 'token': 'pme'}]
        organization_levels = [{'name': u'Info', 'token': 'info'},
                               {'name': u'Secretariat', 'token': 'secretariat'}]

        old_user_properties = {'last_login_time': DateTime(2000, 1, 1)}
        api.user.create(email='old_user@example.com',
                        username='old_user',
                        properties=old_user_properties)

        new_user_properties = {'last_login_time': DateTime()}
        api.user.create(email='new_user@example.com',
                        username='new_user',
                        properties=new_user_properties)

        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        annuaire = api.content.create(
            type='directory',
            title='Annuaire',
            position_types=position_types,
            organization_types=organization_types,
            organization_levels=organization_levels,
            id='annuaire',
            container=portal)

        affinitic = api.content.create(
            type='organization',
            title='Affinitic',
            id='affinitic',
            subscriptions=[
                {'year': 2014,
                 'payment': False},
                {'year': 2013,
                 'payment': True}],
            email='info@affinitic.be',
            citizen=100,
            servers='Linux',
            softwares='Firefox',
            description='Affinitic description',
            organization_type='asbl',
            phone='071123456',
            cell_phone='0488123456',
            fax='321123456',
            website='www.affinitic.be',
            number='3',
            street='random street',
            city='random city',
            region='random region',
            container=annuaire,
            use_parent_address=False)
        tintin = api.content.create(
            type='person',
            title='Tintin',
            id='tintin',
            email='tintin@affinitic.be',
            multimail=['contact_cotisation', 'formation'],
            invalidmail=True,
            userid='tintin',
            password='secret',
            confirm_password='secret',
            lastname='Tin',
            firstname='Tin',
            birthday=datetime(1987, 6, 25),
            phone='071123456',
            cell_phone='0488123456',
            fax='321123456',
            website='www.affinitic.be',
            number='26',
            street='rue du Labrador',
            additional_address_details='fictif',
            zip_code='1000',
            city='Bruxelles',
            region='Bruxelles',
            container=affinitic)
        haddock = api.content.create(
            type='person',
            title='Haddock',
            id='haddock',
            email='haddock@affinitic.be',
            multimail=[],
            invalidmail=False,
            userid='haddock',
            password='secret',
            confirm_password='secret',
            lastname='Haddock',
            container=affinitic)

        imio = api.content.create(
            type='organization',
            title='Imio',
            id='imio',
            subscriptions=[
                {'year': 2014,
                 'payment': False},
                {'year': 2013,
                 'payment': False}],
            email='info@imio.be',
            citizen=100,
            servers='Linux',
            softwares='Firefox',
            container=annuaire,
            use_parent_address=False)
        dupont = api.content.create(
            type='person',
            title='Dupont',
            id='dupont',
            email='dupont@imio.be',
            multimail=['formation'],
            invalidmail=False,
            userid='dupont',
            password='secret',
            confirm_password='secret',
            lastname='Dupont',
            birthday=datetime(1980, 1, 1),
            container=imio)

        catalog.reindexObject(annuaire)
        catalog.reindexObject(affinitic)
        catalog.reindexObject(tintin)
        catalog.reindexObject(haddock)
        catalog.reindexObject(imio)
        catalog.reindexObject(dupont)


RIC_CORE_FIXTURE = RICCorePloneWithPackageLayer(
    name="RIC_CORE_FIXTURE",
    zcml_filename="testing.zcml",
    zcml_package=ric.core,
    gs_profile_id="ric.core:testing")

RIC_CORE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(RIC_CORE_FIXTURE,),
    name="ric.core:Integration")

RIC_CORE_ROBOT_TESTING = FunctionalTesting(
    bases=(RIC_CORE_FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE,
           z2.ZSERVER_FIXTURE),
    name="ric.core:Robot")
