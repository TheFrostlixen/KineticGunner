import command

class UnitAI:

    def __init__(self, ent):
        self.ent = ent
        self.commands = []
        
    def tick(self, dtime):
        if self.commands != []:
            if self.commands[0].tick(dtime):
                self.commands.pop(0)
                    
    def addCommand(self, newCommand):
        self.commands.append( newCommand )

    def clearCommands(self):
        self.commands = []

    def setCommand(self, newCommand):
        self.clearCommands()
        self.addCommand( newCommand )
