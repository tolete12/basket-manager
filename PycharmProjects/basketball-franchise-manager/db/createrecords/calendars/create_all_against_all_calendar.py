import random


class CreateAllAgainstAllCalendar:
    @staticmethod
    def first_round(num_teams: int, pivot_team_id: int, list_tuples: list):
        dict_matches = {}
        for i in range(1, num_teams):
            if not i == 1:
                if i % 2 == 0:
                    # Par
                    list_tuples = CreateAllAgainstAllCalendar.even_matches(list_tuples, pivot_team_id)
                else:
                    # Impar
                    list_tuples = CreateAllAgainstAllCalendar.odd_matches(list_tuples, pivot_team_id)
            dict_matches = CreateAllAgainstAllCalendar.add_matches(dict_matches, i, list_tuples)
        return dict_matches

    @staticmethod
    def second_round(dict_matches: dict, num_teams: int):
        for i in range(num_teams, num_teams * 2 - 1):
            if i not in dict_matches:
                dict_matches[i] = []

            for match in dict_matches[i - num_teams + 1]:
                dict_matches[i].append(tuple((match[1], match[0])))
        return dict_matches

    @staticmethod
    def generate_matches(teams: list):
        if not len(teams) % 2 == 0:
            teams.append(0)
        random.shuffle(teams)
        teams_1 = teams[0: int(len(teams) / 2)]
        teams_2 = teams[int(len(teams) / 2):]
        list_tuples = list(zip(teams_1, teams_2))
        pivot_team_id = list_tuples[0][1]
        dict_matches = CreateAllAgainstAllCalendar.first_round(len(teams), pivot_team_id, list_tuples)
        return CreateAllAgainstAllCalendar.second_round(dict_matches, len(teams))

    @staticmethod
    def odd_matches(list_tuples: list, pivot_team_id: int):
        list_tuples_temp = []
        pivot_team_id_1 = list_tuples[0][0]
        pivot_team_id_2 = list_tuples[len(list_tuples) - 1][1]
        i = 1
        for _ in list_tuples:
            if i == 1:
                list_tuples_temp.append(tuple((pivot_team_id_1, pivot_team_id)))
            else:
                if i == len(list_tuples):
                    list_tuples_temp.append(tuple((list_tuples[i - 2][1], pivot_team_id_2)))
                else:
                    list_tuples_temp.append(tuple((list_tuples[i - 2][1], list_tuples[i - 1][0])))

            i += 1
        return list_tuples_temp

    @staticmethod
    def even_matches(list_tuples: list, pivot_team_id: int):
        list_tuples_temp = []
        i = 1
        for match in list_tuples:
            if i == len(list_tuples):
                list_tuples_temp.append(tuple((pivot_team_id, match[0])))
            else:
                list_tuples_temp.append(tuple((list_tuples[i][1], match[0])))
            i += 1
        return list_tuples_temp

    @staticmethod
    def add_matches(dict_matches: dict, num: int, list_tuples: list):
        dict_matches[num] = []
        for match in list_tuples:
            dict_matches[num].append(match)
        return dict_matches


if __name__ == "__main__":
    calendar = CreateAllAgainstAllCalendar.generate_matches([1,2,3,4])
    print(calendar)
