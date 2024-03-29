from game.simWorld import Environment
from agent.actor import Actor
from agent.critic import Critic
from config import *
from agent.agent_config import *
from main_plots import plot_remaining_pegs

# Initialize actor and critic
critic = Critic()
actor = Actor()

# Keep track of pegs left on board for each episode (for plotting)
remaining_pegs = []

# Local variable for the epsilon greedy strategy
epsilon = epsilon_greedy_value

# Run for num_of_episodes
for episode in range(num_of_episodes):
  env = Environment(viz=(episode == num_of_episodes-1))

  # Reset eligibilites in actor and critic
  critic.reset_eligibilities()
  actor.reset_eligibilities()

  # Get initial state
  state, legal_moves, reward, done = env.get_current_state()

  if critic_type == "table":
    critic.add_state(state)
    
  # Get initial action
  action = actor.choose_action(state, legal_moves, epsilon)

  saps = [(state, action, reward)] # Will contain all state-action pairs for this episode

  while done == 0: # If done is -1 the game is lost, if done is 1 the game is won
    # Do action
    new_state, legal_moves, reward, done = env.move(action)

    if critic_type == "table":
      critic.add_state(new_state)

    # Choose new action
    new_action = actor.choose_action(new_state, legal_moves, epsilon)

    actor.update_eligibility(state, action, 1)

    if critic_type == "table":
      critic.update_delta(reward, new_state, state)
      critic.update_eligibility(state, 1)

    # Add new state, action and reward to the state-action pairs for this episode
    saps.append((new_state, new_action, reward))

    if critic_type == "table":
      for sap in saps:
        s, a, r = sap # No need for reward r, but need to unpack it
        critic.update_eval(s)
        critic.update_eligibility(s)
        actor.update_policy(s, a, critic.delta)
        actor.update_eligibility(s, a)
    else:
      # Evaluate all states and get their corresponding td error
      td_errors = critic.nn_update_eval(saps)
      for i in range(len(saps)-1):
        s, a, r = saps[i]
        actor.update_policy(s, a, td_errors[i])
        actor.update_eligibility(s, a)

    action = new_action
    state = new_state

    # Decay epsilon for the epsilon greedy strategy
    epsilon = epsilon * epsilon_decay_rate

  print("Episode:", episode + 1)

  if (env.get_remaining_pegs() == 1):
    print("Solved!")

  remaining_pegs.append(env.get_remaining_pegs()) # For plotting

  if episode == num_of_episodes-1: # Visualize the last episode
    env.show()

plot_remaining_pegs(remaining_pegs)

if critic_type == "neural_net":
  critic.value_func.summary()