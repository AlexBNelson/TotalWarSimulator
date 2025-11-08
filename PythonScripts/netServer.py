# server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from neuralNet import DQNAgent
from armyModels import ArmyUnit

app = Flask(__name__)
# enable cors for all routes
CORS(app)

STATE_DIM = 4
ACTION_DIM = 2
agent = DQNAgent(STATE_DIM, ACTION_DIM)

# Storage for current episode
episode_memory = []

@app.route("/step", methods=["POST"])
def step():
    data = request.get_json()
    allies = np.array(data["allies"], dtype=ArmyUnit)
    enemies = np.array(data["enemies"], dtype=ArmyUnit)
    # Store experience (no training yet)
    episode_memory.append((allies, enemies))

    # Pick next action for Unity
    return {}

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"})

@app.route("/end_episode", methods=["POST"])
def end_episode():
    data = request.get_json()
    final_reward = float(data["final_reward"])

    # Train agent using final reward for all transitions
    
    agent.learn_from_episode(final_reward)

    # Clear memory
    episode_memory.clear()

    return jsonify({"status": "episode complete", "reward_used": final_reward})

@app.route("/")
def home():
    return "RL Server (episodic reward mode) running!"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
