using UnityEngine;
namespace Restart.Models
{
    public class Step
    {
        public UnitStep[] allies;
        public UnitStep[] enemies;
    }

    public class UnitStep
    {
        // Probably needs ID
        public int id;
        // ID of enemy unit commanded against
        public int commandedTarget;
        // ID of enemy unit currently fighting against
        public int fightingTarget;
        public int numCols;
        // Maps from UnitMovementState enum
        public int movementState;
        // From UnitState enum
        public int state;
        // From UnitCombactState enum
        public int combactState;
        public Vector3 position;
    }
}