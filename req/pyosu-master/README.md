# pyosu
This is a simple Python wrapper for osu! api.

### Usage
```python
import pyosu as osu

api = osu.Api('YOUR API KEY')
print(api.get_user(user=osu.User(name='Polkisss'))[0]['user_id'])
# outputs my ID. i.e. 11349334
```
You can see more examples at [examples page](https://github.com/Polkisss/pyosu/tree/master/example).
And [get your personal API key](https://osu.ppy.sh/p/api).

### Installation
1. Download it and unpack
1. Change your current directory to unpacked archive
1. Run following command: `python setup.py install`

Before you will install it, please, make sure you read [this official wiki](https://github.com/ppy/osu-api/wiki#mods).

