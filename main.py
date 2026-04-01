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
