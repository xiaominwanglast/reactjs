#!/usr/bin/python
# -*- coding: UTF-8 -*-

from faker import Faker
from  datetime import datetime


class create_credit():
    def __init__(self, cardid='', name=''):
        self.f = Faker(locale='zh_CN')
        _now = datetime.now().strftime('%Y')
        cardid = cardid.replace(' ', '')
        if len(str(cardid)) == 18:
            self.cardId = cardid
        else:
            self.cardId = self.f.ssn(min_age=20, max_age=45)

        if name:
            self.name = name
        else:
            self.name = None

    def create_all(self):
        if self.name:
            name = self.name
        else:
            name = self.f.name()

        if int(str(self.cardId)[16]) % 2 == 0:
            gander = u"女"
        else:
            gander = u"男"

        birthday_y = str(self.cardId)[6:10]
        birthday_m = int(str(self.cardId)[10:12])
        birthday_d = int(str(self.cardId)[12:14])
        address = self.f.address()[:-7]

        if len(address) > 10:
            return name, gander, birthday_y, birthday_m, birthday_d, self.cardId, address[:9], address[9:]
        else:
            return name, gander, birthday_y, birthday_m, birthday_d, self.cardId, address
