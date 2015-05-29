# -*- coding: utf-8 -*-
from five import grok
from zope import schema
from zope.interface import alsoProvides
from plone.autoform.interfaces import IFormFieldProvider
from plone.autoform import directives as form
from plone.supermodel import model
from collective.z3cform.datagridfield import DataGridField, DictRow
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from z3c.form.browser.radio import RadioFieldWidget
from z3c.form.browser.select import SelectFieldWidget
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary

from ric.core import RICMessageFactory as _


class MultimailTypes(object):
    grok.implements(IContextSourceBinder)

    def __call__(self, context):
        registry = getUtility(IRegistry)

        terms = []

        if registry is not None:
            types = registry.get('ric.core.multimail', {})
            i = 0
            for type in types:
                terms.append(SimpleVocabulary.createTerm(type, i, types[type]))
                i += 1
        return SimpleVocabulary(terms)

    def getTermByToken(self, token):
        registry = getUtility(IRegistry)
        if registry is not None:
            types = registry.get('ric.core.multimail', {})
            return SimpleVocabulary.createTerm(types[token])


def FunctionsList(context):
    terms = []
    for brain in context.portal_catalog(portal_type='directory', id='annuaire'):
        for pos in brain.getObject().position_types:
            terms.append(SimpleVocabulary.createTerm(pos['token'], pos['token'], pos['name']))
    return SimpleVocabulary(terms)

alsoProvides(FunctionsList, IContextSourceBinder)


class IRICPerson(model.Schema):

    functions = schema.List(
        title=_(u"Fonctions"),
        description=_(u"Vous pouvez sélectionner plusieurs fonctions en appuyant sur la touche CTRL"),
        required=True,
        value_type=schema.Choice(source=FunctionsList),
    )
    form.widget('functions', SelectFieldWidget, multiple='multiple', size=3)

    invalidmail = schema.Bool(title=_(u"E-mail invalide"),
                              required=True)

    form.read_permission(invalidmail='RIC.ActualPersonOwner')
    form.write_permission(invalidmail='RIC.Administrator')
    form.widget('invalidmail', RadioFieldWidget)

    multimail = schema.List(title=_(u"Envoi mail"),
                            required=False,
                            value_type=schema.Choice(source=MultimailTypes()),
                            )
    form.widget('multimail', SelectFieldWidget, multiple='multiple', size=2)

    userid = schema.TextLine(title=_(u"Identifiant de l'utilisateur"),
                             required=False)

    form.read_permission(userid='RIC.Administrator')
    form.write_permission(userid='RIC.Administrator')


alsoProvides(IRICPerson, IFormFieldProvider)


class ICotisationRow(model.Schema):

    year = schema.Int(title=_(u"Année"),
                      required=True)

    payment = schema.Bool(title=_(u"Versement"),
                          required=True)


class IRICOrganization(model.Schema):

    citizen = schema.Int(
        title=_(u"Nombre d'habitants"),
        required=True,
        min=1
    )

    #servers = schema.TextLine(
    #    title=_(u"Serveurs"),
    #    required=True
    #)

    #softwares = schema.TextLine(
    #    title=_(u"Logiciels"),
    #    required=True
    #)

    subscriptions = schema.List(
        title=_(u"Cotisations"),
        value_type=DictRow(title=_(u"Cotisation"),
                           schema=ICotisationRow),
        required=False,
    )
    form.read_permission(subscriptions='RIC.ActualOrganizationMember')
    form.write_permission(subscriptions='RIC.Administrator')
    form.widget('subscriptions', DataGridField)

alsoProvides(IRICOrganization, IFormFieldProvider)
