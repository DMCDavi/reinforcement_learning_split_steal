import random
import numpy as np
from itertools import combinations
import simple_opponents
import gp_agent
import rl_agent


mean = 100
variance = 10000  # Large variance

#Create Log file
log = open("Log.txt","w")

def create_agents(game_type):
  train = Player(gp_agent.ReinforcementLearningAgent())

  if game_type == "Allgame":
    return [Player(simple_opponents.Splitter()), Player(simple_opponents.Stealer()), Player(simple_opponents.Randy()), Player(simple_opponents.Karmine()), Player(simple_opponents.Opportunist()), Player(simple_opponents.Pretender()), train]

  if game_type == "Simple":
    return [Player(simple_opponents.Karmine()),  Player(simple_opponents.Karmine()), Player(rl_agent.RLAgent()), train]

  if game_type == "Difficult":
    return [Player(gp_agent.ReinforcementLearningAgent(2)), Player(gp_agent.ReinforcementLearningAgent(3)), Player(rl_agent.RLAgent()), train]

  if game_type == "Very_difficult":
    return [Player(simple_opponents.Pretender()), Player(simple_opponents.Pretender()), Player(rl_agent.RLAgent()), Player(simple_opponents.Karmine()), train]

  if game_type == "Karma_aware":
    return [Player(simple_opponents.Karmine()), Player(simple_opponents.Karmine()), Player(rl_agent.RLAgent()), Player(simple_opponents.Stealer()), train]

  if game_type == "Opportunists":
    return [Player(simple_opponents.Opportunist()),Player(simple_opponents.Opportunist()), Player(rl_agent.RLAgent()), train]

  if game_type == "3_Karmines":
    return [Player(simple_opponents.Karmine()),  Player(simple_opponents.Karmine()), Player(simple_opponents.Karmine()), train]

class Game:
    def __init__ (self, total_rounds):
        self.rounds_played = 0
        self.total_rounds = total_rounds 
        self.current_amount = 0
        
        
    def isOver(self):
        return self.rounds_played >= self.total_rounds
        
    def prepare_round(self):
        # Generate random values for total amount and rounds played
        self.current_amount = max(mean, np.random.normal(mean, np.sqrt(variance)))    
         
    
    def play_round(self, left_agent, right_agent, remaining):  
        self.rounds_played += 1


        # Call the callback function with the generated values
        left_decision = left_agent.decision(self.current_amount, remaining, left_agent.karma, right_agent.karma)
        assert left_decision in ["split", "steal"]
        right_decision = right_agent.decision(self.current_amount, remaining, right_agent.karma, left_agent.karma)
        assert right_decision in ["steal", "split"]        
        decisions = np.array([left_decision, right_decision])
        log.write(f"Agent {left_agent.name}={left_decision}"
              f" vs Agent {right_agent.name}={right_decision}\n")
            
        if all(decisions == "steal"):
            left_reward = 0
            right_reward = 0
        elif all(decisions == "split"):
            left_reward = self.current_amount / 2
            right_reward = self.current_amount / 2            
        elif left_decision == 'steal':
            left_reward = self.current_amount   
            right_reward = 0   
        elif right_decision == 'steal':
            right_reward = self.current_amount 
            left_reward = 0
            
        log.write(f"Agent {left_agent.name} won {left_reward:.2f}"
              f" vs Agent {right_agent.name} won {right_reward:.2f}\n")   
            
        left_agent.total_amount += left_reward
        right_agent.total_amount += right_reward
        
        left_agent.result(
            left_decision, 
            right_decision, 
            self.current_amount, 
            left_reward)
            
        right_agent.result(
            right_decision, 
            left_decision, 
            self.current_amount, 
            right_reward)  

        if left_decision == "steal":
          left_agent.add_karma(-1)
        else:
          left_agent.add_karma(+1)
          
        if right_decision == "steal":
          right_agent.add_karma(-1)
        else:
          right_agent.add_karma(+1)            
                      

    def preround_render(self):
        
        log.write(f"\nRounds played: {self.rounds_played}/{self.total_rounds}\n")
        log.write(f"Current Amount: ${self.current_amount: .2f}\n")

class Player:
    def __init__(self, agent):
        self.name = agent.get_name()
        self.agent = agent
        self.total_amount = 0
        self.last_decision = "none"
        self.karma = 0
        
    def add_karma(self, value):
      self.karma = min(max(self.karma + value, -5), 5)

    def reset_karma(self):
      self.karma = 0

    def decision(self, total_amount, rounds_played, your_karma, his_karma):
      self.last_decision = self.agent.decision(total_amount, rounds_played, your_karma, his_karma)
      return self.last_decision
      
    def result(self,  your_action, his_action, total_possible, reward):
      self.agent.result(your_action, his_action, total_possible, reward)


def play_round(game, agent1, agent2, remaining):
  log.write(f"{agent1.name} vs {agent2.name}\n")
  game.prepare_round()
  game.preround_render()  

  # Play a round
  game.play_round(agent1, agent2, remaining)

ntrains = 1
for i in range(ntrains):
  log.close()
  log = open("Log.txt","w")

  agents = create_agents("Very_difficult")

  nrematches = 10 # Could very
  nfullrounds = 50 # How many full cycles
  total_rounds = int(len(agents)*(len(agents) - 1) * nfullrounds * nrematches / 2)
  game = Game(total_rounds)

  from collections import defaultdict
  matches_played = defaultdict(lambda: 0)
  # Play rounds
  while not game.isOver():
    random.shuffle(agents)
    for a in agents:
      a.reset_karma()
    
    for player1, player2 in combinations(agents, 2):
      matches_played[player1.name] += 1
      matches_played[player2.name] += 1
      log.write("==========\n")
      for remaining in reversed(range(0, nrematches)): 
        play_round(game, player1, player2, remaining)

  # print(matches_played)

max_score = -1
best = None
scores = []
log.write("\n\n==========\n")
for a in agents:
  log.write(f"O agente '{a.name}' obteve {a.total_amount}\n")
  if a.total_amount > max_score:
    best = a
    max_score = a.total_amount
log.write(f"Vencedor: {best.name}\n")
log.write(f"Score: {max_score}\n")

