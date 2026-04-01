import random

# ----------------------------
# STRUCTURE
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
# UNIT
# ----------------------------

class Unit:
    def __init__(self, name, weight, hp, attack):
        self.name = name
        self.weight = weight
        self.hp = hp
        self.attack = attack

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
        total = 0
        for s in self.structures:
            total += s.weight
        for u in self.units:
            total += u.weight
        return total

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
            len(self.left.structures) == 0 and
            len(self.right.structures) == 0 and
            len(self.left.units) == 0 and
            len(self.right.units) == 0
        )

    def imbalance_check(self):
        left_weight = self.left.total_weight()
        right_weight = self.right.total_weight()
        diff = abs(left_weight - right_weight)

        if diff >= 3:
            print("⚖️ Imbalance triggered!")
            roll = random.randint(1, 6)
            print(f"Roll: {roll}")

            if roll <= 3:
                if left_weight > right_weight:
                    side = self.left
                else:
                    side = self.right

                if side.structures:
                    target = random.choice(side.structures)
                    target.fragile = True
                    print(f"{target.name} is now FRAGILE!")


# ----------------------------
# PLAYER
# ----------------------------

class Player:
    def __init__(self, name):
        self.name = name
        self.skyhold = Skyhold()
        self.credits = 5

        # STARTING STRUCTURE (prevents instant win)
        self.skyhold.left.structures.append(Structure("Wooden Deck", 1, 0))

    # ---------- PHASES ----------

    def income_phase(self):
        gardens = [s for s in self.all_structures() if s.name == "Garden"]
        gain = len(gardens)
        self.credits += gain
        print(f"{self.name} gains {gain} credits → {self.credits}")

    def build_phase(self):
        print("\nBuild Phase")
        print("1 Garden(2)  2 Fabrication(4)  3 Portal(5)  4 Skip")

        choice = input("> ").lower()

        if choice in ["4", "skip"]:
            return

        side = self.choose_side()

        if choice == "1" and self.credits >= 2:
            side.structures.append(Structure("Garden", 3, 2, income=1))
            self.credits -= 2
            print("Built Garden")

        elif choice == "2" and self.credits >= 4:
            side.structures.append(Structure("Fabrication", 4, 4, production=1))
            self.credits -= 4
            print("Built Fabrication")

        elif choice == "3" and self.credits >= 5:
            side.structures.append(Structure("Portal Gate", 3, 5, portal=True))
            self.credits -= 5
            print("Built Portal Gate")

        else:
            print("Invalid choice or not enough credits")

    def production_phase(self):
        print("\nProduction Phase")

        for s in self.all_structures():
            if s.production > 0:
                for _ in range(s.production):
                    unit = Unit("Warrior", 1, 1, 1)
                    self.skyhold.left.units.append(unit)
                    print("Produced Warrior")

    def movement_phase(self):
        print("\nMovement Phase")
        print("(l) Right→Left | (r) Left→Right | (skip)")

        choice = input("> ").lower()

        if choice == "l":
            self.skyhold.left.units += self.skyhold.right.units
            self.skyhold.right.units = []
            print("Moved units Right → Left")

        elif choice == "r":
            self.skyhold.right.units += self.skyhold.left.units
            self.skyhold.left.units = []
            print("Moved units Left → Right")

        elif choice == "skip":
            pass

    def combat_phase(self, enemy):
        print("\nCombat Phase")

        for side_name in ["left", "right"]:
            atk_side = getattr(self.skyhold, side_name)
            def_side = getattr(enemy.skyhold, side_name)

            total_attack = sum(u.attack for u in atk_side.units)

            if total_attack == 0:
                continue

            if def_side.units:
                target = random.choice(def_side.units)
                target.damage(total_attack)

            elif def_side.structures:
                target = random.choice(def_side.structures)
                target.damage(total_attack)

            def_side.cleanup()

    def repair_phase(self):
        print("\nRepair Phase")

        for s in self.all_structures():
            if self.credits > 0 and s.weight < s.max_weight:
                s.weight += 1
                self.credits -= 1
                print(f"Repaired {s.name} (+1)")

    # ---------- HELPERS ----------

    def choose_side(self):
        choice = input("Side? (l/r): ").lower()
        if choice == "r":
            return self.skyhold.right
        return self.skyhold.left

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

        for player, enemy in [(p1, p2), (p2, p1)]:
            print(f"\n--- {player.name} ---")

            player.income_phase()
            player.build_phase()
            player.production_phase()
            player.movement_phase()
            player.combat_phase(enemy)
            player.repair_phase()

            player.skyhold.imbalance_check()

            if enemy.skyhold.is_empty():
                print(f"\n🏆 {player.name} WINS (Skyhold captured)")
                return

        turn += 1

