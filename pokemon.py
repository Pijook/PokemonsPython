import random
import copy

# Pokemon and Attacks types
PHYSICAL_TYPE = "Physical"
WATER_TYPE = "Water"
EARTH_TYPE = "Earth"
AIR_TYPE = "AIR"
FIRE_TYPE = "Fire"
ICE_TYPE = "Ice"
STEEL_TYPE = "Steel"

pokemonsInGame = []
enemies = []
player = None


class Stats:
    def __init__(self, health: int, damage: int, level: int, exp: int):
        self.health = health
        self.damage = damage
        self.level = level
        self.exp = exp

    def print_info(self):
        print("Health", self.health)
        print("Damage", self.damage)
        print("Level", self.level)
        print("Exp", self.exp)

    def increase_exp(self, amount: int):
        self.exp = self.exp + amount

    def increase_level(self, amount: int):
        self.level = self.level + amount

    def decrease_health(self, amount: int):
        self.health = self.health - amount


class Attack:
    def __init__(self, name: str, element: str, damage: int, accuracy: int):
        self.name = name
        self.element = element
        self.damage = damage
        self.accuracy = accuracy

    def print_into(self):
        print("Attack name", self.name)
        print("Element", self.element)
        print("Damage", self.damage)
        print("Accuracy", self.accuracy, "%")


class Pokemon:
    def __init__(self, name: str, element: str, stats: Stats, attacks: list):
        self.name = name
        self.element = element
        self.stats = stats
        self.attacks = attacks

    def status(self):
        print("Printing status of", self.name)
        print("Pokemon element", self.element)
        self.stats.print_info()
        print("Attacks:")
        for attack in self.attacks:
            attack.print_into()

    def attack(self, enemy_pokemon, ai: bool):
        if not ai:
            index = 1
            for attack in self.attacks:
                print(index, attack.name)
                index += 1

            attackIndex = -1

            while attackIndex < 0 or attackIndex >= len(self.attacks):
                int(input("Choose attack"))

            attack = self.attacks[attackIndex]
        else:
            attack = self.attacks[random.randint(0, len(self.attacks))]

        multiplier = get_attack_multiplier(attack.element, enemy_pokemon.element)
        crit = False
        if random.random() < 0.25:
            crit = True

        missed = False

        if random.randint(1, 100) > attack.accuracy:
            missed = True

        if missed:
            print(self.name, "used attack", attack.name, "but missed!")
        else:
            damage = (attack.damage + self.stats.damage) * multiplier
            if crit:
                damage = damage * 1.5

            enemy_pokemon.stats.decrease_health(damage)

            print(self.name, "used attack", attack.name, " at hit ", enemy_pokemon.name, "for", damage)
            if crit:
                print("It was critical strike!")
            if multiplier == 0.5:
                print("It wasn't very effective")
            elif multiplier == 1.5:
                print("It was very effective!")

    def ready_to_fight(self):
        return self.stats.health > 0


class Player:
    def __init__(self, name: str, pokemons: list):
        self.name = name
        self.selected_pokemon = 0
        self.pokemons = pokemons

    def has_pokemons_to_fight(self):
        for pokemon in self.pokemons:
            if pokemon.ready_to_fight():
                return True


def get_attack_multiplier(attack_type, enemy_type):
    normal_multiplier = 1.0
    weak_multiplier = 0.5
    effective_multiplier = 1.5

    if attack_type == PHYSICAL_TYPE:
        return normal_multiplier
    elif attack_type == WATER_TYPE:
        if enemy_type == EARTH_TYPE or enemy_type == FIRE_TYPE:
            return effective_multiplier
        elif enemy_type == WATER_TYPE:
            return weak_multiplier
    elif attack_type == EARTH_TYPE:
        if enemy_type == FIRE_TYPE or enemy_type == ICE_TYPE or enemy_type == STEEL_TYPE:
            return effective_multiplier
        elif enemy_type == AIR_TYPE:
            return weak_multiplier
    elif attack_type == AIR_TYPE:
        if enemy_type == ICE_TYPE:
            return effective_multiplier
        elif enemy_type == EARTH_TYPE or enemy_type == STEEL_TYPE:
            return weak_multiplier
    elif attack_type == FIRE_TYPE:
        if enemy_type == FIRE_TYPE or enemy_type == STEEL_TYPE:
            return effective_multiplier
        elif enemy_type == WATER_TYPE or enemy_type == EARTH_TYPE:
            return weak_multiplier
    elif attack_type == ICE_TYPE:
        if enemy_type == EARTH_TYPE:
            return effective_multiplier
        elif enemy_type == WATER_TYPE or enemy_type == FIRE_TYPE or enemy_type == ICE_TYPE:
            return weak_multiplier
    elif attack_type == STEEL_TYPE:
        if enemy_type == WATER_TYPE or enemy_type == AIR_TYPE:
            return effective_multiplier
        elif enemy_type == FIRE_TYPE or enemy_type == STEEL_TYPE:
            return weak_multiplier

    return normal_multiplier


def play():
    fight_round = 1
    for enemy in enemies:
        print("Round number", fight_round)
        result = fight(player, enemy)

        if result:
            print("You won!")
            print("Do you want to continue?")

            player_decision = input("Yes or No ")
            if player_decision == "Yes":
                print("Starting next fight...")
            else:
                print("Disabling...")
                break
        else:
            print(enemy.name, "won! You lost...")
            break

        fight_round += 1


def generate_player():
    print("Starting game")

    username = input("Enter your nickname ")
    print("Welcome", username)
    print("Time to choose your pokemons!")

    player_pokemons = []
    pokemons_taken = {-1}

    for i in range(6):
        validDecision = False
        while not validDecision:
            index = 0
            for pokemon in pokemonsInGame:
                if index not in pokemons_taken:
                    print((index+1), pokemon.name)
                index += 1

            player_choice = int(input("Choose your pokemon ")) - 1

            if 0 <= player_choice < len(pokemonsInGame) and player_choice not in pokemons_taken:
                chosenPokemon = copy.deepcopy(pokemonsInGame[player_choice])
                print(chosenPokemon.name, "joins your squad!")
                player_pokemons.append(chosenPokemon)
                pokemons_taken.add(player_choice)
                validDecision = True

    global player
    player = Player(username, player_pokemons)


def generate_pokemons():
    print("Generating pokemons")
    # Physical attacks
    slashAttack = Attack("Slash", PHYSICAL_TYPE, 25, 95)
    biteAttack = Attack("Bite", PHYSICAL_TYPE, 30, 90)
    scratchAttack = Attack("Scratch", PHYSICAL_TYPE, 15, 100)

    # Fire attacks
    fireBreathAttack = Attack("Fire Breath", FIRE_TYPE, 50, 75)
    fireBallAttack = Attack("Fire Ball", FIRE_TYPE, 60, 75)
    fireWaveAttack = Attack("Fire Wave", FIRE_TYPE, 100, 65)

    # Water attacks
    tsunamiAttack = Attack("Tsunami", WATER_TYPE, 100, 75)
    plumAttack = Attack("Plum", WATER_TYPE, 5, 100)
    waterTornadoAttack = Attack("Water tornado", WATER_TYPE, 150, 50)

    # Air attacks
    airSlashAttack = Attack("Air Slash", AIR_TYPE, 25, 75)
    tornadoAttack = Attack("Tornado", AIR_TYPE, 30, 75)
    wingSlashAttack = Attack("Wing slash", AIR_TYPE, 100, 100)

    # Earth attacks
    smashAttack = Attack("Smash", EARTH_TYPE, 30, 85)
    rockThrowAttack = Attack("Rock Throw", EARTH_TYPE, 50, 50)
    earthquakeAttack = Attack("Earthquake", EARTH_TYPE, 150, 95)

    # Steel attacks
    katanaCutAttack = Attack("Katana Cut", STEEL_TYPE, 100, 100)
    steelBeam = Attack("Steel Beam", STEEL_TYPE, 50, 75)
    steelFistAttack = Attack("Steel Fist", STEEL_TYPE, 25, 100)

    # Ice attacks
    iceBoltAttack = Attack("Ice Bolt", ICE_TYPE, 25, 100)
    iceTornadoAttack = Attack("Ice Tornado", ICE_TYPE, 100, 65)
    iceBeamAttack = Attack("Ice Beam", ICE_TYPE, 50, 75)

    charmandur = Pokemon(
        "Charmandur",
        FIRE_TYPE,
        Stats(50, 15, 1, 0),
        [scratchAttack, biteAttack, fireBallAttack, fireBreathAttack]
    )
    pokemonsInGame.append(charmandur)

    amogus = Pokemon(
        "Amogus",
        PHYSICAL_TYPE,
        Stats(100, 50, 1, 0),
        [scratchAttack, biteAttack, slashAttack, rockThrowAttack]
    )
    pokemonsInGame.append(amogus)

    wingu = Pokemon(
        "Wingu",
        AIR_TYPE,
        Stats(15, 150, 1, 0),
        [slashAttack, scratchAttack, wingSlashAttack, airSlashAttack]
    )
    pokemonsInGame.append(wingu)

    yeti = Pokemon(
        "Yeti",
        ICE_TYPE,
        Stats(200, 5, 1, 0),
        [biteAttack, iceTornadoAttack, iceBoltAttack, iceBeamAttack]
    )
    pokemonsInGame.append(yeti)

    magifish = Pokemon(
        "Magifish",
        WATER_TYPE,
        Stats(9000, 9001, 1, 0),
        [biteAttack, tsunamiAttack, plumAttack, waterTornadoAttack]
    )
    pokemonsInGame.append(magifish)

    plop = Pokemon(
        "Plop",
        WATER_TYPE,
        Stats(1, 1, 1, 0),
        [plumAttack, plumAttack, plumAttack, plumAttack]
    )
    pokemonsInGame.append(plop)

    steluWindu = Pokemon(
        "SteeluWinduu",
        STEEL_TYPE,
        Stats(160, 15, 1, 0),
        [steelBeam, steelFistAttack, airSlashAttack, katanaCutAttack]
    )
    pokemonsInGame.append(steluWindu)


def generate_enemies():
    print("Generating enemies")

    names = ["Yi", "Goku", "Vegeta", "Kame", "Zen", "Yoink", "Hex", "Fade", "Fez", "Pijok"]
    namesTaken = {-1}

    for i in range(6):
        nameIndex = -1
        while nameIndex in namesTaken:
            nameIndex = random.randint(0, len(names) - 1)

        namesTaken.add(nameIndex)
        enemy_name = names[nameIndex]

        enemy_pokemons = []
        pokemons_taken = {-1}

        for x in range(6):
            pokemonIndex = -1
            while pokemonIndex in pokemons_taken:
                pokemonIndex = random.randint(0, len(pokemonsInGame) - 1)

            pokemons_taken.add(pokemonIndex)
            enemy_pokemons.append(copy.deepcopy(pokemonsInGame[pokemonIndex]))

        enemies.append(Player(enemy_name, enemy_pokemons))


def fight(player: Player, enemy: Player):
    while player.has_pokemons_to_fight() and enemy.has_pokemons_to_fight():
        global turn
        turn = 0
        if turn == 0:
            turn_completed = False
            print(player.name, "turn")
            while not turn_completed:
                print("What do you want to do?")
                print("1. Attack")
                print("2. Change pokemon")
                print("3. Evolve pokemon")

                player_choice = -1

                while player_choice < 1 or player_choice > 3:
                    player_choice = int(input("Choose option (1-3): "))

                # Attack enemy pokemon
                if player_choice == 1:
                    player.pokemons[player.selected_pokemon].attack(enemy.pokemons[enemy.selected_pokemon])
                    turn_completed = True
                # Change currently used pokemon
                elif player_choice == 2:
                    print("Available pokemons")
                    index = 1
                    for pokemon in player.pokemons:
                        if pokemon.ready_to_fight():
                            print(index, pokemon.name)
                        index += 1
                    print("0. Back")

                    pokemonChoice = int(input("Choose new pokemon: "))

                    pokemonChoice -= 1

                    if pokemonChoice == -1:
                        print("")
                    elif 0 <= pokemonChoice <= len(player.pokemons) - 1:
                        if player.pokemons[pokemonChoice].ready_to_fight():
                            player.selected_pokemon = player_choice
                        else:
                            print("Chose wrong pokemon!")
                    else:
                        print("Wrong number!")

                # Evolve pokemon
                # elif player_choice == 3:

            turn = 1
        elif turn == 1:
            print(enemy.name, "turn")

            player_pokemon: Pokemon = player.pokemons[player.selected_pokemon]
            current_pokemon: Pokemon = enemy.pokemons[enemy.selected_pokemon]
            current_pokemon.attack(player_pokemon, True)

            if not player_pokemon.ready_to_fight():
                print(player_pokemon.name, "fainted!")
                if player.has_pokemons_to_fight():
                    index: int = 1
                    for pokemon in player.pokemons:
                        if pokemon.ready_to_fight:
                            print(index, pokemon.name)
                        index += 1

                new_pokemon_index = int(input("Choose your next pokemon")) - 1

                if 0 <= new_pokemon_index < len(player.pokemons) and player.pokemons[new_pokemon_index].ready_to_fight():
                    print(player.name, "chooses", player.pokemons[new_pokemon_index].name)
                    player.selected_pokemon = new_pokemon_index

            turn = 0

    if player.has_pokemons_to_fight():
        return True
    else:
        return False



