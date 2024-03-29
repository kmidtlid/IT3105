import random
import math
from copy import deepcopy
import numpy as np

class MCTS():

  def __init__(self, exploration_rate):
    self.c = exploration_rate

  def uct_search(self, tree, node, M):
    """
    The main MCTS algorithm. Runs M simulations to create the tree.
    Then selects the best child state for the given input state
    """
    board = deepcopy(node.board)
    for i in range(M):
      self.simulate(tree, node)

    node.board = board
    return self.select_best_child(node, 0)

  def simulate(self, tree, node):
    """
    The general simulation algorithm, tree traversal, rollout and backprop.
    """
    selected_node = self.sim_tree(tree, node)
    z = self.sim_default(selected_node.board)
    self.backup(selected_node, z)

  def sim_tree(self, tree, node):
    """
    Traversing the tree from the root to a leaf node by using the tree policy.
    """
    c = self.c
    board = deepcopy(node.board)
    board.verbose = False
    while (not board.is_terminal_state()):
      if not node in tree.nodes:
        self.new_node(tree, node)
        return node

      node = self.select_best_child(node, c)
      board.move(node.move)
    return node

  def new_node(self, tree, node):
    """
    Generating some or all child states of a parent state, and then connecting
    the tree node housing the parent state (a.k.a. parent node) to the nodes
    housing the child states (a.k.a. child nodes).
    """
    tree.nodes.append(node)
    node.Q = 0
    node.visits = 0
    for a in node.board.get_legal_moves():
      board = deepcopy(node.board)
      board.verbose = False
      board.move(a)
      child_node = tree.create_node(board, node, a)
      node.children.append(child_node)

  def sim_default(self, board):
    """
    Estimating the value of a leaf node in the tree by doing a rollout
    simulation using the default policy from the leaf node’s state to a
    final state.
    """
    def default_policy(board):
      moves = board.get_legal_moves()
      return random.choice(moves)
      
    game = deepcopy(board)
    game.verbose = False
    while (not game.is_terminal_state()):
      a = default_policy(game)
      game.move(a)
    return game.get_winner()

  def backup(self, selected_node, result):
    """
    Passing the evaluation of a final state back up the tree, updating
    relevant data (see course lecture notes) at all nodes and edges on
    the path from the final state to the tree root.
    """
    node = selected_node
    while node != None:
      node.visits += 1
      node.Q += (result - node.Q) / node.visits
      node = node.parent

  def select_best_child(self, node, c):
    """
    Selects the best child of a given state, based on the node visits
    and scores (Q-values).
    """
    board = node.board
    active_player = board.get_active_player()
    # True if player is 2 (2 - 1 = 1 = True), false if 1 (1-1=0=False)
    minimizing = active_player - 1 
    children = node.children
    child_scores = []
    for child in children:
      uct = c * math.sqrt(math.log(node.visits) / (child.visits + 1))
      score = child.Q - uct if minimizing else child.Q + uct
      child_scores.append(score)

    if (minimizing):
      best_child_index = np.argmin(child_scores)
    else:
      best_child_index = np.argmax(child_scores)
    
    return children[best_child_index]
