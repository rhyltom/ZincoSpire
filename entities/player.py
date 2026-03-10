class Player:

    def __init__(self):

        # Base stats
        self.max_hp = 50
        self.hp = 50
        self.block = 0
        self.attack = 5

        # Mana system (para magias mais tarde)
        self.max_mana = 3
        self.mana = 3

        # Gold (para loja)
        self.gold = 0

        # Status effects
        self.status = []

    
    def take_damage(self, dmg):

        dmg -= self.block

        if dmg < 0:
            dmg = 0

        self.block = 0
        self.hp -= dmg
        
        if self.hp < 0:
            self.hp = 0


    def heal(self, amount):

        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp