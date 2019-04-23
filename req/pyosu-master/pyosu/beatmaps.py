# coding: utf-8


class Map:
    def __init__(self, **kwargs):
        self.mapset_id = kwargs.get('mapset_id') or kwargs.get('beatmapset_id')
        self.map_id = kwargs.get('map_id') or kwargs.get('beatmap_id')
