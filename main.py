import random

class Structure:
    def __init__(self, name, health, protected_by=None):
        self.name = name
        self.max_health = health
        self.health = health
        self.protected_by = protected_by

    def is_destroyed(self):
        return self.health <= 0

    def take_damage(self, damage):
        if self.is_destroyed():
            return False
        
        self.health -= damage
        print(f"{self.name} takes {damage} damage! ({max(self.health,0)} HP left)")
        
        if self.health <= 0:
            print(f"🔥 {self.name} destroyed!")
            return True
        
        return False


class Skyhold:
    def __init__(self, owner):
        self.owner = owner
        self.structures = {
            "Shield Generator": Structure("Shield Generator", 60),
            "Engine": Structure("Engine", 50),
            "Core": Structure("Core", 100, protected_by="Shield Generator")
        }
        self.captured = False

    def get_active_structures(self):
        return [s for s in self.structures.values() if not s.is_destroyed()]

    def attack(self, damage):
        if self.captured:
            return

        core = self.structures["Core"]
        shield = self.structures["Shield Generator"]

        if not shield.is_destroyed():
            target = shield
        else:
            active = self.get_active_structures()
            target = random.choice(active)

        target.take_damage(damage)

        if core.is_destroyed():
            self.captured = True
            print(f"\n💀 {self.owner}'s Skyhold has fallen!\n")


class Player:
    def __init__(self, name):
        self.name = name
        self.skyhold = Skyhold(name)

    def is_alive(self):
        return not self.skyhold.captured


def game():
    p1 = Player("Player 1")
    p2 = Player("Player 2")

    turn = 1

    while p1.is_alive() and p2.is_alive():
        print(f"\n--- Turn {turn} ---")

        damage = random.randint(5, 20)
        print(f"{p1.name} attacks {p2.name} for {damage} damage")
        p2.skyhold.attack(damage)

        if not p2.is_alive():
            break

        damage = random.randint(5, 20)
        print(f"{p2.name} attacks {p1.name} for {damage} damage")
        p1.skyhold.attack(damage)

        turn += 1

    if p1.is_alive():
        print("\n🏆 Player 1 wins!")
    else:
        print("\n🏆 Player 2 wins!")


if __name__ == "__main__":
    print("SCRIPT STARTED")
    game()
