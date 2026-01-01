# agent.py
import keras
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models, optimizers

class DQNAgent:
    ARMY_SIZE = 11

    def __init__(self, state_dim, action_dim, lr=0.001, gamma=0.95):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.gamma = gamma
        try:
            model = keras.models.load_model("rl_model")
        except Exception as e:
            model = self._build_model(lr)
        
        self.model = model
        
        self.episode_memory = []  # stores {"state", "action", "reward"}

    def _build_model(self, lr):
        model = models.Sequential([
            layers.Dense(64, activation='relu', input_shape=(self.state_dim,)),
            layers.Dense(64, activation='relu'),
            layers.Dense(self.action_dim, activation='linear')
        ])
        model.compile(optimizer=optimizers.Adam(learning_rate=lr),
                      loss='mse')
        return model

    def act(self, state, epsilon=0.0):
        """Choose action using epsilon-greedy. For imitation, set epsilon=0."""
        if np.random.rand() < epsilon:
            return np.random.randint(self.action_dim)
        q_values = self.model.predict(state[np.newaxis], verbose=0)
        return int(np.argmax(q_values[0]))

    def store_transition(self, state, action):
        """Store state and human action during the episode."""
        self.episode_memory.append({
            "state": state,
            "action": action,
            "reward": 0  # initial reward placeholder
        })

    def learn_from_episode(self, final_reward, bc_weight=1.0):
        """
        Hybrid learning: combine human imitation and Monte Carlo end-of-episode reward.
        bc_weight: weight for behavior cloning (human actions).
        """
        # Assign final reward to all transitions
        for transition in self.episode_memory:
            transition["reward"] = final_reward

        # Compute targets
        states = [t["state"] for t in self.episode_memory]
        targets = []
        G = final_reward

        # Iterate backwards to propagate discounted reward
        for transition in reversed(self.episode_memory):
            state = transition["state"]
            action = transition["action"]

            q_values = self.model.predict(state[np.newaxis], verbose=0)[0]

            # Combine behavior cloning (human action) with cumulative reward
            q_values[action] = bc_weight + G

            targets.insert(0, q_values)  # reverse order back to chronological
            G = self.gamma * G

        # Fit the model
        self.model.fit(np.array(states), np.array(targets), verbose=0)
        
        self.model.save("rl_model")
        self.episode_memory.clear()

    def decode_action(action_id, unit, enemies):
        # think about invalid states
        if action_id == 0:
            unit.movementState = IDLE

        elif action_id == 1:
            direction = action_id - 1
            unit.movementState = MOVING
            move_unit(unit, direction)

        elif 2 <= action_id <= 2+DQNAgent.ARMY_SIZE - 1:
            enemy_index = action_id - 2
            if enemy_index < len(enemies):
                unit.commandUnit = enemies[enemy_index].id
                unit.combactState = ATTACKING

        elif action_id == 2 + DQNAgent.ARMY_SIZE:
            unit.movementState = ESCAPING
