from flask import Flask, request, jsonify
import numpy as np
from agent import DQNAgent  # your existing agent.py

app = Flask(__name__)

# Example dims - change to your actual dims
STATE_DIM = 8   # example: position + movement states etc.
ACTION_DIM = 5  # example: idle, move N, move S, attack, retreat

# Create global agent instance
agent = DQNAgent(state_dim=STATE_DIM, action_dim=ACTION_DIM)

@app.route("/store", methods=["POST"])
def store_transition():
    """
    Receive a state and human action during episode.
    Expected JSON:
    {
      "state": [...],   # list of floats/ints length = STATE_DIM
      "action": int     # human chosen action index
    }
    """
    data = request.get_json()

    state = np.array(data["state"], dtype=np.float32)
    action = int(data["action"])

    agent.store_transition(state, action)

    return jsonify({"status": "stored"})


@app.route("/act", methods=["POST"])
def act():
    """
    Given state, return action from agent.
    Expected JSON:
    {
      "state": [...]
    }
    Returns:
    {
      "action": int
    }
    """
    data = request.get_json()
    state = np.array(data["state"], dtype=np.float32)

    # For inference, use epsilon=0 to avoid random actions
    action = agent.act(state, epsilon=0.0)

    return jsonify({"action": action})


@app.route("/end_episode", methods=["POST"])
def end_episode():
    """
    Called at episode end to provide final reward and trigger training.
    Expected JSON:
    {
      "final_reward": float,
      "bc_weight": float (optional, default 1.0)
    }
    """
    data = request.get_json()

    final_reward = float(data["final_reward"])
    bc_weight = float(data.get("bc_weight", 1.0))

    agent.learn_from_episode(final_reward, bc_weight)

    return jsonify({"status": "trained"})

if __name__ == "__main__":
    # Run on localhost:5000 by default
    app.run(host="0.0.0.0", port=5000)
