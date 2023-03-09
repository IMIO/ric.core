# -*- coding: utf-8 -*-
from zope.i18nmessageid import MessageFactory

import logging
import permissions


permissions  # flake
logger = logging.getLogger('ric.core')
RICMessageFactory = MessageFactory('ric')
