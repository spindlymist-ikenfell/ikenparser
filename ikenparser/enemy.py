class Enemy:
    def __init__(self):
        self.ClassName = None
        self.IsAbstract = None
        self.BaseClass = None
        self.NameID = None
        self.Name = None
        self.Categories = None
        self.HP = None
        self.Pow = None
        self.Def = None
        self.Spd = None
        self.Mov = None
        self.Exp = None
        self.Money = None
        self.Rewards = None
        self.Stealable = None
        self.GetExp = None
        self.GetMoney = None
        self.GetRewards = None
        self.GetSteal = None
        self.Sprite = None
        self.SpriteSet = None
        self.Notes = []
    
    def addNote(self, note):
        try:
            return self.Notes.index(note)
        except ValueError:
            self.Notes.append(note)
            return len(self.Notes) - 1
