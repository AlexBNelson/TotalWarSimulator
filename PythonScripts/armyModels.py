import math
from dataclasses import dataclass, field
from typing import Dict, Optional


# --- Unity-like stubs ---
@dataclass
class Vector3:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __mul__(self, scalar: float):
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    @staticmethod
    def clamp_magnitude(v, max_length: float):
        mag = v.magnitude()
        if mag > max_length:
            return v * (max_length / mag)
        return v
    
    
class ArmyUnit:
    
    id: int
    # ID of enemy unit commanded against
    commandUnit: int
    # ID of enemy unit currently fighting against
    fightingTarget: int
    pathSpeed: float
    numCols: int
    # Maps from UnitMovementState enum
    movementState: int
    # From UnitState enum
    state: int
    # From UnitCombactState enum
    combactState: int
    position: Vector3




