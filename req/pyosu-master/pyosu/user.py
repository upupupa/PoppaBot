# coding: utf-8

from .errors import UserIDError


class User:
    def __init__(self, **kwargs):
        try:
            self.id = kwargs['userid']
            if self.id == '':
                raise UserIDError
            self.type = 'id'
            self.name = ''

        except (KeyError, UserIDError):
            self.name = str(kwargs.get('name'))
            self.type = 'string'
            self.id = ''

    @property
    def identificator(self):
        return self.type, self.id if self.type == 'id' else self.name
