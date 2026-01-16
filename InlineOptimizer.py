from numpy import float32 as f32
from BaseMothballSimulation import BasePlayer, MothballSequence
from Enums import OptimizeCellAxis
from PyQt5.QtCore import QThread
from AngleOptimizerCell import Worker
from typing import Callable
from math import degrees

class OptTick:
    def __init__(self, accel: float = 0.0, drag_x: float = 0.0, drag_z: float = 0.0):
        self.accel = float(accel)
        self.drag_x = float(drag_x)
        self.drag_z = float(drag_z)
        
class Restriction:
    def __init__(self, option: str, tick_1: int, tick_2: int, sign: str, value: float):
        self.option = option
        self.tick_1 = tick_1
        self.tick_2 = tick_2
        self.sign = sign
        self.value = value
    
    def to_list(self):
        return ['YES', '', self.option, str(self.tick_1), '-', str(self.tick_2), self.sign, str(self.value)]
        
class InlineOptimizer:
    def __init__(self):
        pass
    
    def optimize(self, init: float, angle: float, player: BasePlayer, sequence: MothballSequence, on_completion: Callable):
        data = [[], [], [], []]
        
        data[0].append(angle)
        
        if player.previous_slip is not None:
            data[1].append(float(f32(0.91) * player.previous_slip)) #TODO consider inertia probably
            data[2].append(float(f32(0.91) * player.previous_slip))
        else:
            data[1].append(float(f32(0.91) * self.current_slip))
            data[2].append(float(f32(0.91) * self.current_slip))
        
        data[3].append(init)
        
        player.simulate(sequence)

        for i in range(len(player.opthistory)):
            tick = player.opthistory[i]
            print(f'Accel: {tick.accel} Drag X: {tick.drag_x} Drag Z: {tick.drag_z}')
            
            data[0].append(f'F{i+1}')
            data[1].append(float(tick.drag_x))
            data[2].append(float(tick.drag_z))
            data[3].append(float(tick.accel))
            
        variables = {}
        variables['num_ticks'] = len(data[0])
        
        constraints = [res.to_list() for res in player.restrictions]
            
        worker = Worker(OptimizeCellAxis.X, 'min', variables, data, constraints)
        worker.finished.connect(on_completion)

        worker.run()
        
    def test(self, res, constraint_values, postprocess_dict):
        print("done")
        if isinstance(res, str):
            print(f"{res} {constraint_values}")
            return
        
        angles = [round(degrees(p),3) for p in res.x]
        for i, angle in enumerate(angles):
            # Range of angle is [-360, 360]
            if angle > 180:
                angles[i] = round(angle - 360,3)
            elif angle < -180:
                angles[i] = round(angle + 360,3)
                
            print(angles)
        