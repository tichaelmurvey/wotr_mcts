from dataclasses import dataclass
from typing import Dict, NamedTuple
from game_env.game_env_enums import Nation

@dataclass
class NationStatus:
    active: bool
    at_war: bool
    track_pos: int

STARTING_POLITICS : Dict[Nation, NationStatus] = {
    Nation.DWARVES: NationStatus(False, False, 0),
    Nation.NORTH : NationStatus(False, False, 0),
    Nation.ROHAN : NationStatus(False, False, 0),
    Nation.GONDOR : NationStatus(False, False, 1),
    Nation.ELVES: NationStatus(True, False, 0),
    Nation.MORDOR: NationStatus(True, False, 2),
    Nation.ISENGARD : NationStatus(True, False, 2),
    Nation.ELINGS : NationStatus(True, False, 1),
    
}

class Politics:
    nations : Dict[Nation, NationStatus]
    def __init__(self):
        self.nations = STARTING_POLITICS
    
    def advance_nation(self, nation : Nation):
        if self.nations[nation].track_pos == 2 and not self.nations[nation].active:
            raise Exception("Error: Tried to move inactive nation to war")
        
        self.nations[nation].track_pos  += 1
        if self.nations[nation].track_pos == 3:
            self.nations[nation].at_war = True

    def instant_war(self, nation):
        self.nations[nation] = NationStatus(True, True, 3)