# coding: utf-8

import requests

from .beatmaps import Map
from .errors import *
from .mods import *
from .score import Scores
from .user import User


class Api:
    def __init__(self, apikey: str):
        self.key = apikey

    def _get(self, params: str, target: str):
        link = 'https://osu.ppy.sh/api/' + target + '?k=' + self.key + params
        data = requests.get(link).json()

        try:
            raise APIError(data['error'])
        except (TypeError, KeyError):
            return data

    @staticmethod
    def _make_params(args):
        line = ''
        for i in args:
            if args[i] != '':
                line += '&{}={}'.format(i, args[i])

        return line

    @staticmethod
    def _num_mode(mode: str):
        modes = ['osu', 'taiko', 'ctb', 'mania']

        try:
            mode = modes.index(mode)
        except ValueError:
            mode = '0'  # osu

        return mode

    def get_user(self, user: User, **kwargs):

        if user.type == 'id':
            u = user.id
        else:
            u = user.name

        args = {
            'u': u,
            'm': self._num_mode(kwargs.get('mode')),
            'type': user.type,
            'event_days': kwargs.get('event_days') or ''
        }

        params = self._make_params(args)

        return self._get(params, 'get_user')

    def get_beatmaps(self, *, beatmap: Map, **kwargs):

        user = User(
            userid=kwargs.get('userid') or '',
            name=kwargs.get('username') or '',
        )

        args = {
            'since': kwargs.get('since') or '',
            's': beatmap.mapset_id or '',
            'b': beatmap.map_id or '',
            'u': user.identificator[1] or '',
            'type': user.identificator[0] or '',
            'm': self._num_mode(kwargs.get('mode')),
            'a': 1 if str(kwargs.get('include_converted')) == 'True' else 0,
            'h': kwargs.get('hash') or '',
            'limit': kwargs.get('limit') or ''
        }

        params = self._make_params(args)

        return self._get(params, 'get_beatmaps')

    def get_scores(self, score: Scores, **kwargs):

        user = User(
            userid=kwargs.get('userid') or '',
            name=kwargs.get('username') or '',
        )

        m = kwargs.get('mods')

        args = {
            'b': score.beatmap.map_id,
            'u': user.identificator[1] or '',
            'm': self._num_mode(kwargs.get('mode')),
            'mods': encode_mods(m) if type(m).__name__ in ('list', 'tuple', 'set') else m or '',
            'type': user.identificator[0] or '',
            'limit': kwargs.get('limit') or ''
        }

        params = self._make_params(args)

        return self._get(params, 'get_scores')

    def get_user_best(self, user: User, **kwargs):

        args = {
            'u': user.identificator[1],
            'm': self._num_mode(kwargs.get('mode')),
            'limit': kwargs.get('limit') or '',
            'type': user.identificator[0],
        }

        params = self._make_params(args)

        return self._get(params, 'get_user_best')

    def get_user_recent(self, user: User, **kwargs):

        args = {
            'u': user.identificator[1],
            'm': self._num_mode(kwargs.get('mode')),
            'limit': kwargs.get('limit') or '',
            'type': user.identificator[0]
        }

        params = self._make_params(args)

        return self._get(params, 'get_user_recent')

    def get_match(self, match_id):

        args = {
            'mp': match_id
        }

        params = self._make_params(args)

        return self._get(params, 'get_match')

    def get_replay(self, user: User, beatmap: Map, mode='osu'):

        args = {
            'u': user.identificator[1],
            'm': self._num_mode(mode),
            'type': user.identificator[0],
            'b': beatmap.map_id
        }

        params = self._make_params(args)

        return self._get(params, 'get_replay').get('content')
