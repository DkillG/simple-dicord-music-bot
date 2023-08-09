import requests

class robloxAPI:
    def get_game_info(self, id: str | int | None = None, name: str | None = None):
        if id:
            universe_id = requests.get(f"https://apis.roblox.com/universes/v1/places/{id}/universe").json()['universeId']

            game_info = requests.get(f"https://games.roblox.com/v1/games?universeIds={universe_id}").json()['data'][0]
            votes = requests.get(f"https://games.roblox.com/v1/games/votes?universeIds={universe_id}").json()['data'][0]
            thumbnails = requests.get(f"https://thumbnails.roblox.com/v1/games/multiget/thumbnails?universeIds={universe_id}&countPerUniverse=1&defaults=true&size=768x432&format=Png&isCircular=false").json()['data'][0]['thumbnails']

            return {
                'name': game_info['name'],
                'upvotes': votes['upVotes'],
                'playing': game_info['playing'],
                'downvotes': votes['downVotes'],
                'author': game_info['creator']['name'],
                'description': game_info['description'],
                'favorites': game_info['favoritedCount'],
                'thumbnail_url': thumbnails[0]['imageUrl'],
                'url': f"https://www.roblox.com/games/{game_info['id']}/",
                'author_url': f"https://www.roblox.com/users/{game_info['creator']['id']}/profile/",
            }

        elif name:
            game_tmp = requests.get(f"https://www.roblox.com/games/list-json?keyword={name}&startRows=0&maxRows=1").json()[0]
            game_info = requests.get(f"https://games.roblox.com/v1/games?universeIds={game_tmp['UniverseID']}").json()['data'][0]
            thumbnails = requests.get(f"https://thumbnails.roblox.com/v1/games/multiget/thumbnails?universeIds={game_tmp['UniverseID']}&countPerUniverse=1&defaults=true&size=768x432&format=Png&isCircular=false").json()['data'][0]['thumbnails']

            return {
                'name': game_tmp['Name'],
                'author': game_tmp['CreatorName'],
                'playing': game_tmp['PlayerCount'],
                'upvotes': game_tmp['TotalUpVotes'],
                'author_url': game_tmp['CreatorUrl'],
                'description': game_info['description'],
                'downvotes': game_tmp['TotalDownVotes'],
                'favorites': game_info['favoritedCount'],
                'url': game_tmp['GameDetailReferralUrl'],
                'thumbnail_url': thumbnails[0]['imageUrl'],
            }

        