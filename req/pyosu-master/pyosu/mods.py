# coding: utf-8

ids = {
    'NoFail': 1,
    'Easy': 2,
    'TouchDevice': 4,
    'Hidden': 8,
    'HardRock': 16,
    'SuddenDeath': 32,
    'DoubleTime': 64,
    'Relax': 128,
    'HalfTime': 256,
    'Nightcore': 512,  # Only set along with DoubleTime. i.e: NC only gives 576
    'Flashlight': 1024,
    'Autoplay': 2048,
    'SpunOut': 4096,
    'Relax2': 8192,  # Autopilot
    'Perfect': 16384,  # Only set along with SuddenDeath.i.e: PF only gives 16416
    'Key4': 32768,
    'Key5': 65536,
    'Key6': 131072,
    'Key7': 262144,
    'Key8': 524288,
    'FadeIn': 1048576,
    'Random': 2097152,
    'Cinema': 4194304,
    'Target': 8388608,
    'Key9': 16777216,
    'KeyCoop': 33554432,
    'Key1': 67108864,
    'Key3': 134217728,
    'Key2': 268435456,
    'ScoreV2': 536870912,
    'LastMod': 1073741824,
}


def decode_mods(key, raw=True):
    mods = set()

    for mod in list(ids)[::-1]:
        if key >= ids[mod]:
            key -= ids[mod]
            mods.add(mod)

    if not raw:
        if ('Nightcore' in mods) and ('DoubleTime' in mods):
            mods.remove('DoubleTime')

        if ('Perfect' in mods) and ('SuddenDeath' in mods):
            mods.remove('SuddenDeath')

    return mods


def encode_mods(mods):
    mods = list(mods)
    key = 0

    for mod in mods:
        key += ids[mod]

    return key
