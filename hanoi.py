import math

class Hanoi():
    def __init__(self, pegs=3, disks=5, state=None, parent=None, last_action=None):
        self.pegs = pegs
        self.disks = disks
        self.state = self.initial_state(state)
        self.parent = parent
        self.last_action = last_action
        
    def initial_state(self, state):
        if state is not None:
            return state
        first_peg = [list(range(self.disks, 0, -1))]
        other_pegs = [[] for _ in range(self.pegs-1)]
        return first_peg + other_pegs
    
    def next_state(self, from_peg, to_peg):
        if not self.disk_mouvement_is_valid(from_peg, to_peg):
            raise ValueError("Disk mouvement is invalid")
        self.state[to_peg].append(self.state[from_peg].pop())
        return Hanoi(pegs=self.pegs, disks=self.disks, state=self.state, parent=self, last_action=(from_peg, to_peg))
    
    def peg_is_empty(self, peg):
        return len(self.state[peg]) == 0
    
    def disk_mouvement_is_valid(self, from_peg, to_peg):
        if from_peg == to_peg:
            return False
        if self.peg_is_empty(from_peg):
            return False
        if self.peg_is_empty(to_peg):
            return True
        return self.state[from_peg][-1] <= self.state[to_peg][-1]
        
    def get_possible_actions(self):
        actions = []
        for from_peg in range(self.pegs):
            for to_peg in range(self.pegs):
                if self.disk_mouvement_is_valid(from_peg, to_peg):
                    actions.append((from_peg, to_peg))
        return actions
        
    def is_goal_state(self):
        return len(self.state[-1]) == self.disks
    
    def __str__(self):
        height = self.disks
        width = math.floor(math.log10(self.disks)) + 2
        out = ""
        for row in range(height-1, -1, -1):
            for peg in range(0, self.pegs):
                if len(self.state[peg]) > row:
                    out += f"{self.state[peg][row]:{width}}"
                else:
                    out += " " * (width-1) + "|"
            out += "\n"
        return out

    def __repr__(self):
        return str(self.state)

    def __eq__(self, other):
        return self.state == other.state
    
    
hanoi = Hanoi(pegs=3, disks=5)
print(hanoi)
print(hanoi.get_possible_actions())
hanoi = hanoi.next_state(0, 1)
print(hanoi)
print(hanoi.get_possible_actions())
hanoi = hanoi.next_state(0, 2)
print(hanoi)
