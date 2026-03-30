import random

# ----------------------------
# STRUCTURE
# ----------------------------

class Structure:
    def __init__(self, name, health, protected_by=None):
        self.name = name
        self.max_health = health
        self.health = health
        self.protected_by = protected_by  # Name of structure that must fall first

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


# ----------------------------
# SKYHOLD
# ----------------------------

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

        # Core protected?
        core = self.structures["Core"]
        shield = self.structures["Shield Generator"]

        if not shield.is_destroyed():
            target = shield
        else:
            # Randomly hit remaining structure
            active = self.get_active_structures()
            target = random.choice(active)

        destroyed = target.take_damage(damage)

        # Check capture condition
        if core.is_destroyed():
            self.captured = True
            print(f"\n💀 {self.owner}'s Skyhold has fallen!\n")


# ----------------------------
# PLAYER
# ----------------------------

class Player:
    def __init__(self, name):
        self.name = name
        self.skyhold = Skyhold(name)

    def is_alive(self):
        return not self.skyhold.captured


# ----------------------------
# GAME LOOP
# ----------------------------

def game():
    p1 = Player("Player 1")
    p2 = Player("Player 2")

    turn = 1

    while p1.is_alive() and p2.is_alive():
        print(f"\n--- Turn {turn} ---")
