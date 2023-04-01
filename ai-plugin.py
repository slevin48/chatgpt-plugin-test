#%%
import json
from urllib.request import urlopen

#%% 
# open local
jason = 'ai-plugin.json'

with open(jason) as f:
    ai = json.load(f)

print(ai["name_for_model"])

#%% 
# open from url 

url = 'https://seal-app-ulquy.ondigitalocean.app/.well-known/ai-plugin.json'

with urlopen(url) as response:
    data = response.read()
    ai = json.loads(data)

print(ai["api"]["url"])
