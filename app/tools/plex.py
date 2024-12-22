# %%
import json
import yaml
from plexapi.myplex import MyPlexAccount

# Get plex token by
# 1. https://app.plex.tv/desktop/#!/
# 2. On any movie poster, click the three dots
# 3. Get info > View XML
# 4. Look for "X-Plex-Token" in the URL

from plexapi.server import PlexServer

from app.helpers.env_vars import PLEX_TOKEN, PLEX_SERVER_URL

with open("config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

BASE_URL = PLEX_SERVER_URL
plex = PlexServer(BASE_URL, PLEX_TOKEN)


def get_plex_clients():
    plex = PlexServer(BASE_URL, PLEX_TOKEN)
    # Example 3: List all clients connected to the Server.
    return [client.title for client in plex.clients()]


# %%
def get_plex_playlists():
    plex = PlexServer(BASE_URL, PLEX_TOKEN)
    return [
        f"{playlist.title} ({len(playlist.items)})" for playlist in plex.playlists()
    ]


# %%
