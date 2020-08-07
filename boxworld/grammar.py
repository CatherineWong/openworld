class Meaning(object):
    def __init__(self, program):
        self.program = program
    
    def to_representation(self):
        return [str(primitive) for primitive in self.program]
        
    @staticmethod
    def empty_meaning():
        return Meaning(program=[])