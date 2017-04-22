##############################################################################
#
# Copyright (c) 2002 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

"""Subscriber function checking dependencies if a removal is performed
on an object having dependencies. It raises an exception if it's the
case.
"""


__docformat__ = 'restructuredtext'

from zope.i18nmessageid import Message
from zope.i18nmessageid import MessageFactory
from zope.location.interfaces import ILocationInfo

from zope.app.dependable.interfaces import IDependable, DependencyError

_ = MessageFactory('zope')

exception_msg = _("""
Removal of object (${object}) which has dependents (${dependents})
is not possible !

You must deactivate this object before trying to remove it.
""")

def CheckDependency(event):
    object = event.object
    dependency = IDependable(object, None)
    if dependency is not None:
        dependents = dependency.dependents()
        if dependents:
            mapping = {
                "object": ILocationInfo(object).getPath(),
                "dependents": ", ".join(dependents)
                }
            raise DependencyError(Message(exception_msg, mapping=mapping))
