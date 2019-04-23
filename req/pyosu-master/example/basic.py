# coding: utf-8

import pyosu as osu

if __name__ == '__main__':
    api = osu.Api('api key')

    print(api.get_user(user=osu.User(name='Polkisss')))  # Search for User by ID or username
    print(api.get_beatmaps(beatmap=osu.Map(beatmap_id='577427')))  # Search for Mapset by ID, hash, etc
    print(api.get_beatmaps(beatmap=osu.Map(beatmapset_id='239788')))  # Search for Beatmap by ID
    print(api.get_scores(score=osu.Scores(beatmap=osu.Map(beatmap_id='577427')),
                         mods=576))  # Get score table with defined mods
    print(api.get_user_best(user=osu.User(name='Polkisss'), limit=1))
    print(api.get_user_recent(user=osu.User(name='Polkisss')))
    print(api.get_match(match_id='1936471'))
    print(api.get_replay(osu.User(name='Polkisss'), osu.Map(map_id='577427')))
