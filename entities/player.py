class Player:

    def __init__(self, vocation="warrior"):

        self.vocation = vocation

        # ========================
        # BASE STATS
        # ========================

        self.max_hp = 50
        self.hp = 50

        self.max_mana = 3
        self.mana = 3

        self.attack = 5
        self.str = 1
        self.mgc = 1

        self.block = 0
        self.evade = False

        self.crit_chance = 0.1
        self.crit_multiplier = 2

        # ========================
        # CLASSES
        # ========================

        if vocation == "warrior":

            self.max_hp = 80
            self.hp = 80

            self.max_mana = 2
            self.mana = 2

            self.attack = 6
            self.str = 3
            self.mgc = 0

            self.crit_chance = 0.10


        elif vocation == "hunter":

            self.max_hp = 60
            self.hp = 60

            self.max_mana = 3
            self.mana = 3

            self.attack = 5
            self.str = 2
            self.mgc = 0

            self.crit_chance = 0.20


        elif vocation == "mage":

            self.max_hp = 40
            self.hp = 40

            self.max_mana = 10
            self.mana = 10

            self.attack = 3
            self.str = 0
            self.mgc = 4

            self.crit_chance = 0.15


        # ========================
        # INVENTORY
        # ========================

        self.items = []
        self.gold = 0
        self.status = []


    # ========================
    # DAMAGE SYSTEM
    # ========================

    def take_damage(self, dmg):

        blocked = min(self.block, dmg)

        dmg -= blocked

        if dmg < 0:
            dmg = 0

        self.block = 0

        self.hp -= dmg

        if self.hp < 0:
            self.hp = 0


    # ========================
    # HEALING
    # ========================

    def heal(self, amount):

        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp


    # ========================
    # MANA SYSTEM
    # ========================

    def use_mana(self, amount):

        if self.mana >= amount:
            self.mana -= amount
            return True

        return False


    def restore_mana(self, amount):

        self.mana += amount

        if self.mana > self.max_mana:
            self.mana = self.max_mana