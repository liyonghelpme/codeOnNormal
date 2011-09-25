
from tg import expose, flash, require, url, request, redirect,response
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from pylons import response
from tgext.admin.tgadminconfig import TGAdminConfig
from tgext.admin.controller import AdminController
from repoze.what import predicates
from sqlalchemy.exceptions import InvalidRequestError
from sqlalchemy.exceptions import IntegrityError
from stchong.lib.base import BaseController
from stchong.model import mc,DBSession,wartaskbonus, taskbonus,metadata,operationalData,businessWrite,businessRead,warMap,Map,visitFriend,Ally,Victories,Gift,Occupation,Battle,News,Friend,Datesurprise,Datevisit,FriendRequest,Card,Caebuy,Papayafriend,Rank,logfile
from stchong import model
from stchong.controllers.secure import SecureController
from datetime import datetime
from stchong.controllers.error import ErrorController
import time
import sys
import random
import logging
import StringIO
import hashlib
import copy
import httplib
import json
__all__ = ['WarController']
