import random


class CreatePlayers:

    @staticmethod
    def get_random_value(start_value, end_value) -> int:
        return random.randint(start_value, end_value)

    @staticmethod
    def get_random_from_dict(names_dict: dict) -> int:
        values = sum(names_dict.values())
        rand_num = random.randint(1, values)
        amount_odds = 0
        for name, odd in names_dict.items():
            if amount_odds + odd > rand_num:
                splits = name.split('-')
                return splits[0], splits[1]
            amount_odds += odd

