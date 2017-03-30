# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy.orm.interfaces import MapperExtension
from web.basehandler import _Current_User

class DataUpdateExtension(MapperExtension):
    def before_update(self, mapper, connection, instance):
        if hasattr(instance,'UpdateTime'):
            instance.UpdateTime = datetime.now()
        if hasattr(instance,'UpdateId'):
            instance.UpdateId = _Current_User.Uid

    def before_insert(self, mapper, connection, instance):
        if hasattr(instance,'CreateTime'):
            instance.CreateTime = datetime.now()
            if hasattr(instance,'UpdateTime'):
                instance.UpdateTime = instance.CreateTime
        if hasattr(instance,'CreateId'):
            instance.CreateId = _Current_User.Uid
            if hasattr(instance,'UpdateId'):
                instance.UpdateId = instance.CreateId