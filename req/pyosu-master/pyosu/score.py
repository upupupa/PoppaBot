# coding: utf-8

from .beatmaps import Map


class Scores:
    def __init__(self, *, beatmap: Map):
        self.beatmap = beatmap
