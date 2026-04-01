import random

# ----------------------------
# STRUCTURES
# ----------------------------

class Structure:
    def __init__(self, name, weight, cost, income=0, production=0, portal=False):
        self.name = name
        self.max_weight = weight
        self.weight = weight
        self.cost = cost
        self.income = income
        self.production = production
        self.portal = portal
        self.fragile = False

    def damage(self, dmg):
        if self.fragile or dmg >= self.weight:
            self.weight = 0
            print(f"🔥 {self.name} destroyed!")
        else:
            self.weight -= dmg
            print(f"{self.name} takes {dmg} → {self.weight}")

    def is_destroyed(self):
        return self.weight <= 0


# ----------------------------
# UNITS
# ----------------------------

class Unit:
    def __init__(self, name, weight, hp, attack, siege_bonus=0):
        self.name = name
        self.weight = weight
        self.hp = hp
        self.attack = attack
        self.siege_bonus = siege_bonus

    def damage(self, dmg):
        self.hp -= dmg
        print(f"{self.name} takes {dmg} → {self.hp}")

    def is_destroyed(self):
        return self.hp <= 0


# ----------------------------
# SIDE
# ----------------------------

class Side:
    def __init__(self):
        self.structures = []
        self.units = []

    def total_weight(self):
        return sum(s.weight for s in self.structures) + sum(u.weight for u in self.units)

    def cleanup(self):
        self.structures = [s for s in self.structures if not s.is_destroyed()]
        self.units = [u for u in self.units if not u.is_destroyed()]


# ----------------------------
# SKYHOLD
# ----------------------------

class Skyhold:
    def __init__(self):
        self.left = Side()
        self.right = Side()

    def is_empty(self):
        return (
            not self.left.structures and not self.right.structures and
            not self.left.units and not self.right.units
        )

    def has_portal(self):
        for s in self.left.structures + self.right.structures:
            if s.portal and not s.is_destroyed():
                return True
        return False

    def imbalance_check(self):
        diff = abs(self.left.total_weight() - self.right.total_weight())
        if diff >= 3:
            print("⚖️ Imbalance!")
            roll = random.randint(1, 6)
            print("Roll:", roll)
            if roll <= 3:
                side = self.left if self.left.total_weight() > self.right.total_weight() else self.right
                if side.structures:
                    target = random.choice(side.structures)
                    target.fragile = True
                    print(f"{target.name} becomes FRAGILE")


# ----------------------------
# PLAYER
# ----------------------------

class Player:
    def __init__(self, name):
        self.name = name
        self.skyhold = Skyhold()

# Starting structure so game doesn't instantly end
self.skyhold.left.structures.append(Structure("Wooden Deck", 1, 0))
        self.credits = 5

    # ---------- PHASES ----------

    def income(self):
        gardens = [s for s in self.all_structures() if s.name == "Garden"]
        gain = len(gardens)
        self.credits += gain
        print(f"{self.name} gains {gain} credits → {self.credits}")

    def build(self):
        print("\nBuild Phase")
        print("1 Garden(2)  2 Fabrication(4)  3 Portal(5)")
        choice = input("> ")

        side = self.choose_side()

        if choice == "1" and self.credits >= 2:
            side.structures.append(Structure("Garden", 3, 2, income=1))
            self.credits -= 2

        elif choice == "2" and self.credits >= 4:
            side.structures.append(Structure("Fabrication", 4, 4, production=1))
            self.credits -= 4

        elif choice == "3" and self.credits >= 5:
            side.structures.append(Structure("Portal Gate", 3, 5, portal=True))
            self.credits -= 5

        else:
            print("Invalid")

    def produce(self):
        print("\nProduction Phase")
        for s in self.all_structures():
            if s.production > 0:
                for _ in range(s.production):
                    unit = Unit("Warrior", 1, 1, 1)
                    self.skyhold.left.units.append(unit)
                    print("Produced Warrior")

    def move(self):
        print("\nMovement Phase")
        print("Move all units Left→Right or Right→Left? (l/r/skip)")
        choice = input("> ")

        if choice == "l":
            self.skyhold.left.units += self.skyhold.right.units
            self.skyhold.right.units = []
        elif choice == "r":
            self.skyhold.right.units += self.skyhold.left.units
            self.skyhold.left.units = []

    def combat(self, enemy):
        print("\nCombat Phase")

        for side_name in ["left", "right"]:
            atk_side = getattr(self.skyhold, side_name)
            def_side = getattr(enemy.skyhold, side_name)

            total_attack = sum(u.attack for u in atk_side.units)

            if def_side.units:
                target = random.choice(def_side.units)
                target.damage(total_attack)
            elif def_side.structures:
                target = random.choice(def_side.structures)
                target.damage(total_attack)

            def_side.cleanup()

    def repair(self):
        print("\nRepair Phase")
        for s in self.all_structures():
            if self.credits > 0 and s.weight < s.max_weight:
                s.weight += 1
                self.credits -= 1
                print(f"Repaired {s.name}")

    # ---------- HELPERS ----------

    def choose_side(self):
        side = input("Side? (l/r): ")
        return self.skyhold.left if side == "l" else self.skyhold.right

    def all_structures(self):
        return self.skyhold.left.structures + self.skyhold.right.structures


# ----------------------------
# GAME LOOP
# ----------------------------

def game():
    p1 = Player("Player 1")
    p2 = Player("Player 2")

    turn = 1

    while True:
        print(f"\n======== TURN {turn} ========")

        for p, enemy in [(p1, p2), (p2, p1)]:
            print(f"\n--- {p.name} ---")

            p.income()
            p.build()
            p.produce()
            p.move()
            p.combat(enemy)
            p.repair()

            p.skyhold.imbalance_check()

            if enemy.skyhold.is_empty():
                print(f"\n🏆 {p.name} WINS (Skyhold captured)")
                return

        turn += 1


if __name__ == "__main__":
    game()
