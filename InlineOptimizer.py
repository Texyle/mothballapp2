from numpy import float32 as f32
from BaseMothballSimulation import BasePlayer, MothballSequence
from math import sqrt

class OptTick:
    def __init__(self, accel: f32 = 0.0, drag_x: f32 = 0.0, drag_z: f32 = 0.0):
        self.accel = accel
        self.drag_x = drag_x
        self.drag_z = drag_z
        
class InlineOptimizer:
    def __init__(self):
        pass
    
    def optimize(self, player: BasePlayer, sequence: MothballSequence):
        accel = []
        
        #init
        print(self.state)
        accel.append(sqrt(player.vx**2 + player.vz**2))
        
        player.simulate(sequence)
        