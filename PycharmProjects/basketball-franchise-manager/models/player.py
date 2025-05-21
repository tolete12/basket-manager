import sqlite3
import random


class Player:
    # BIO
    player_id = 0
    name_id = 0
    surname_id = 0
    birth_date_id = 0
    team_id = 0
    height = 0
    weight = 0
    sport_id = 0

    # MENTAL
    intelligence = 0
    positioning = 0
    temperament = 0
    leadership = 0
    team_player = 0
    aggression = 0
    potential = 0
    mental_toughness = 0
    tactics = 0

    # PHYSICAL
    health = 0
    speed = 0
    acceleration = 0
    natural_fitness = 0
    stamina = 0
    jumping = 0
    strength = 0
    balance = 0
    side_scrolling = 0
    # Skills
    dribbling = 0

    def load_common_attributes_from_db(self, row: sqlite3.Row):

        for attribute in row.keys():
            setattr(self, attribute, row[attribute])
        #
        # self.player_id = row['IDJUGADORES']
        # self.name_id = row['IDNOMBRES']
        # self.surname_id = row['IDAPELLIDOS']
        # self.birth_date_id = row['birth_date_id']
        # self.team_id = row['INTEGER']
        # self.height = row['ALTURA']
        # self.weight = row['PESO']
        # self.sport_id = 0
        #
        # self.intelligence = row['INTELIGENCIA']
        # self.positioning = row['COLOCACION']
        # self.temperament = row['TEMPERAMENTO']
        # self.leadership = row['LIDEREAZGO']
        # self.team_player = row['TEAM_PLAYER']
        # self.aggression = row['AGRESIVIDAD']
        # self.potential = row['POTENCIAL']
        # self.mental_toughness = row['MENTAL_TOUGHNESS']
        # self.tactics = row['TACTICA']
        #
        # self.health = row['HEALTH']
        # self.speed = row['VELOCIDAD']
        # self.acceleration = row['ACELERACION']
        # self.natural_fitness = row['FORMA_NATURAL']
        # self.stamina = row['RESISTENCIA']
        # self.jumping = row['SALTO']
        # self.strength = row['FUERZA']
        # self.balance = row['EQUILIBRIO']
        # self.side_scrolling = row['DESPLAZAMIENTO_LATERAL']
        #
        # self.dribbling = row['DRIBBLING']

    def load_common_attributes_from_dict(self, attributes: dict):

        for key, value in attributes:
            setattr(self, key, value)

        # self.player_id = attributes['player_id']
        # self.name_id = attributes['name_id']
        # self.surname_id = attributes['surname_id']
        # self.birth_date_id = attributes['birth_date_id']
        # self.team_id = attributes['team_id']
        # self.height = attributes['height']
        # self.weight = attributes['weight']
        # self.sport_id = attributes['sport_id']
        #
        # self.intelligence = attributes['intelligence']
        # self.positioning = attributes['positioning']
        # self.temperament = attributes['temperament']
        # self.leadership = attributes['leadership']
        # self.team_player = attributes['team_player']
        # self.aggression = attributes['aggression']
        # self.potential = attributes['potential']
        # self.mental_toughness = attributes['mental_toughness']
        # self.tactics = attributes['tactics']
        #
        # self.health = attributes['health']
        # self.speed = attributes['speed']
        # self.acceleration = attributes['acceleration']
        # self.natural_fitness = attributes['natural_fitness']
        # self.stamina = attributes['stamina']
        # self.jumping = attributes['jumping']
        # self.strength = attributes['strength']
        # self.balance = attributes['balance']
        # self.side_scrolling = attributes['side_scrolling']
        #
        # self.dribbling = attributes['dribbling']

