# Skyhold Terminal Game (Fixed Full Version)
# Clean entry point + guaranteed execution + turn loop

import random

# -----------------------------
# Data Models
# -----------------------------

class Structure:
    def __init__(self, name, cost, weight, effect=None):
        self.name = name
        self.cost = cost
        self.max_weight = weight
        self.weight = weight
        self.side = None
        self.fragile = False
        self.effect = effect

    def take_damage(self, dmg):
        if self.fragile:
            self.weight = 0
        else:
            self.weight -= dmg
        if self.weight <= 0:
            self.weight = 0

    def repair(self, amount):
        if self.weight == 0:
            return
        self.weight = min(self.max_weight, self.weight + amount)
        if self.weight > 0:
            self.fragile = False


class Unit:
    def __init__(self, name, cost, weight, attack, health, movable=True):
        self.name = name
        self.cost = cost
        self.weight = weight
        self.attack = attack
        self.health = health
        self.movable = movable
        self.alive = True

    def take_damage(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            self.alive = False


class Player:
    def __init__(self, name):
        self.name = name
        self.credits = 5
        self.structures = []
        self.units = []

    def get_income(self):
        return sum(1 for s in self.structures if s.name == "Garden")

    def total_weight(self):
        return sum(s.weight for s in self.structures) + sum(u.weight for u in self.units)

    def side_weight(self, side):
        weight = 0
        for s in self.structures:
            if s.side == side:
                weight += s.weight
        for u in self.units:
            weight += u.weight
        return weight


# -----------------------------
# Factories
# -----------------------------

def create_structure(choice):
    if choice == 1:
        return Structure("Garden", 2, 3, "income")
    elif choice == 2:
        return Structure("Fabrication", 4, 4, "production")
    elif choice == 3:
        return Structure("Portal", 5, 3, "portal")
    return None


def create_unit(name):
    if name == "Warrior":
        return Unit("Warrior", 1, 1, 1, 1)
    return None


# -----------------------------
# Game Engine
# -----------------------------

class Game:
    def __init__(self):
        self.players = [Player("Player 1"), Player("Player 2")]
        self.current = 0
        self.turn = 1

    def opponent(self):
        return self.players[1 - self.current]

    def player(self):
        return self.players[self.current]

    def income_phase(self, p):
        income = p.get_income()
        p.credits += income
        print(f"{p.name} gains {income} credits → {p.credits}")

    def build_phase(self, p):
        print("\nBuild Phase")
        print("1 Garden  2 Fabrication  3 Portal  4 Skip")
        choice = input("> ").strip()

        if choice == "4":
            return

        try:
            choice = int(choice)
        except:
            return

        s = create_structure(choice)
        if not s:
            return

        if p.credits < s.cost:
            print("Not enough credits")
            return

        side = input("Side? (l/r): ").strip().lower()
        if side not in ["l", "r"]:
            print("Invalid")
            return

        s.side = side
        p.credits -= s.cost
        p.structures.append(s)
        print(f"Built {s.name}")

    def production_phase(self, p):
        print("\nProduction Phase")
        for s in p.structures:
            if s.name == "Fabrication":
                u = create_unit("Warrior")
                p.units.append(u)
                print("Produced Warrior")

    def movement_phase(self, p):
        print("\nMovement Phase")
        if not p.units:
            return
        choice = input("(l) Right→Left | (r) Left→Right | (skip)\n> ")
        if choice == "skip":
            return
        print("Moved units")

    def combat_phase(self, p, e):
        print("\nCombat Phase")
        if not p.units or not e.units:
            return
        for u in p.units:
            if e.units:
                target = e.units[0]
                target.take_damage(u.attack)
                print(f"{target.name} takes {u.attack}")
        e.units = [u for u in e.units if u.alive]

    def repair_phase(self, p):
        print("\nRepair Phase")
        engineers = [u for u in p.units if u.name == "Engineer"]
        if not engineers:
            return
        for s in p.structures:
            if s.weight > 0:
                s.repair(1)
                print(f"Repaired {s.name}")

    def imbalance(self, p):
        left = p.side_weight("l")
        right = p.side_weight("r")
        if abs(left - right) >= 3:
            print("⚖️ Imbalance triggered!")
            roll = random.randint(1, 6)
            print("Roll:", roll)
            if roll <= 3 and p.structures:
                s = random.choice(p.structures)
                s.fragile = True
                print(f"{s.name} is now FRAGILE")

    def print_state(self, p):
        print("\nBoard:")
        for side in ["l", "r"]:
            print(f"Side {side.upper()} Weight: {p.side_weight(side)}")

    def capture_check(self, p, e):
        if not e.structures and not e.units:
            print(f"\n🏆 {p.name} WINS (Skyhold captured)")
            return True
        return False

    def run(self):
        print("SCRIPT STARTED")

        while True:
            p = self.player()
            e = self.opponent()

            print(f"\n======== TURN {self.turn} ========")
            print(f"--- {p.name} ---")

            self.income_phase(p)
            self.print_state(p)
            self.build_phase(p)
            self.production_phase(p)
            self.movement_phase(p)
            self.combat_phase(p, e)
            self.repair_phase(p)
            self.imbalance(p)

            self.print_state(p)

            if self.capture_check(p, e):
                break

            self.current = 1 - self.current
            if self.current == 0:
                self.turn += 1


# -----------------------------
# Entry Point
# -----------------------------

if __name__ == "__main__":
    Game().run()
