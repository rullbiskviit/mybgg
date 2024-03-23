from decimal import Decimal
import html


class BoardGame:
    def __init__(self, game_data, image="", tags=[], numplays=0, expansions=[]):
        self.id = game_data["id"]
        self.name = game_data["name"]
        self.description = html.unescape(game_data["description"])
        self.categories = game_data["categories"]
        self.mechanics = game_data["mechanics"]
        self.players = self.calc_num_players(game_data, expansions)
        self.weight = self.calc_weight(game_data)
        self.weight_rating = float(game_data["weight"]) if game_data["weight"].strip() else -1
        self.playing_time = self.calc_playing_time(game_data)
        self.rank = self.calc_rank(game_data)
        self.usersrated = self.calc_usersrated(game_data)
        self.numowned = self.calc_numowned(game_data)
        self.rating = self.calc_rating(game_data)
        self.numplays = numplays
        self.image = image
        self.tags = tags
        self.expansions = expansions

    def calc_num_players(self, game_data, expansions):
        num_players = game_data["suggested_numplayers"].copy()

        for supported_num in range(game_data["min_players"], game_data["max_players"] + 1):
            if supported_num > 0 and str(supported_num) not in [num for num, _ in num_players]:
                num_players.append((str(supported_num), "supported"))

        # Add number of players from expansions
        for expansion in expansions:
            # First add all the recommended player counts from expansions, then look for additional counts that are just supported.
            for expansion_num, support in expansion.players:
                if expansion_num not in [num for num, _ in num_players]:
                    if support != "supported":
                        num_players.append((expansion_num, "expansion"))
            for expansion_num, support in expansion.players:
                if expansion_num not in [num for num, _ in num_players]:
                    if support == "supported":
                        num_players.append((expansion_num, "exp_supported"))
        
        num_players = sorted(num_players, key=lambda x: int(x[0].replace("+", "")))
        # Remove "+ player counts if they are not the last in the list
        # Also remove player counts >=11, except for the max player count (e.g. 1-100 suggested player counts will only list 1-10,100)
        num_players[:-1] = [player for player in num_players[:-1] if player[0][-1] != "+" and int(player[0]) < 11 ]
        return num_players

    def calc_playing_time(self, game_data):
        playing_time_mapping = {
            30: '<30min',
            60: '30min–1hr',
            120: '1–2hr',
            180: '2–3hr',
            240: '3–4hr',
        }
        for playing_time_max, playing_time in playing_time_mapping.items():
            if playing_time_max > int(game_data["playing_time"]):
                return playing_time

        return '>4hr'

    def calc_rank(self, game_data):
        if not game_data["rank"] or game_data["rank"] == "Not Ranked":
            return None

        return Decimal(game_data["rank"])

    def calc_usersrated(self, game_data):
        if not game_data["usersrated"]:
            return 0

        return Decimal(game_data["usersrated"])

    def calc_numowned(self, game_data):
        if not game_data["numowned"]:
            return 0

        return Decimal(game_data["numowned"])

    def calc_rating(self, game_data):
        if not game_data["rating"]:
            return None

        return Decimal(game_data["rating"])

    def calc_weight(self, game_data):
        weight_mapping = {
            0: "Light",
            1: "Light",
            2: "Medium Light",
            3: "Medium",
            4: "Medium Heavy",
            5: "Heavy",
        }
        return weight_mapping[round(Decimal(game_data["weight"] or 0))]
