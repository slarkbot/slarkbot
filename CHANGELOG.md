
CHANGELOG


# Next [1.0.6]

# Env Vars
- `STEAM_API_KEY`: a steam API key, see https://steamcommunity.com/dev

# Bugfixes
- Fix markdown parsing in some responses
- Results in F and C conversion are now rounded

# Features
- A handcrafted list of hero aliases to match against when a command needs a hero name

# Commands
- /winrate <username> <hero name>: check winrate with a given hero. User must be registered. 
- /register can now convert between steamid32, steamid64, a full profile URL or the vanity part of the profile URL
- Inline query for full match details on /lastmatch
- Links to OpenDota and Dotabuff in /match

# Commands
- /changelog: alias for /changes
- /matches: alias for /recents
- /profile to get a link to your or someone else's steam profile
