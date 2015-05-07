import ent

class SpawnGroup:
    def __init__(self, enemType, amount ):
        self.enemType = enemType
        self.amount = amount
    
class SpawnCycle:
    def __init__(self, groups, time):
        self.groups = groups
        self.time = time
        self.timer = 0
        
    def spawn(self, entMgr):
        for group in self.groups:
            for i in range(group.amount):
                entMgr.createEnemy( group.enemType )
        self.timer = 0
                
    def tick(self, dt):
        self.timer += dt
        if self.timer > self.time:
            return True
        else:
            return False