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

def select_agents(type):

  splitter = Player(simple_opponents.Splitter())
  stealer = Player(simple_opponents.Stealer())
  randy = Player(simple_opponents.Randy())
  karmine = Player(simple_opponents.Karmine())
  opportunist = Player(simple_opponents.Opportunist())
  pretender = Player(simple_opponents.Pretender())
  train = Player(gp_agent.ReinforcementLearningAgent(1))
  train_2 = Player(gp_agent.ReinforcementLearningAgent(2))
  train_3 = Player(gp_agent.ReinforcementLearningAgent(3))
  rl=Player(rl_agent.RLAgent())

  if type == "Allgame":
    return [splitter, stealer, randy, karmine, opportunist, pretender, train]

  if type == "Simple":
    return [karmine,  karmine, rl, train]

  if type == "Difficult":
    return [train_2, train_3, rl, train]

  if type == "Very_difficult":
    return [pretender, pretender, rl, karmine, train]

  if type == "Karma_aware":
    return [karmine, karmine, rl, stealer, train]

  if type == "Opportunists":
    return [opportunist,opportunist, rl, train]

  if type == "3_Karmines":
    return [karmine,  karmine, karmine, train]



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
  game.prepare_round()   
  # Play a round
  game.play_round(agent1, agent2, remaining)

ntrains = 500
log = open("Log.txt","w")

game_types = ["Allgame","Simple","Difficult","Very_difficult","Karma_aware","Opportunists","3_Karmines"]


df1 = open(f"score.txt", "w")
df1.write(f"i name total_amount reward type\n")
for type in game_types:

  for i in range(ntrains):
    log.close()
    log = open("Log.txt","a")

    # Create agents
    agents = select_agents(type)

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
        for remaining in reversed(range(0, nrematches)):
          play_round(game, player1, player2, remaining)

    max_score = -1
    best = None
    scores = []
    for a in agents:
      log.write(f"O agente '{a.name}' obteve {a.total_amount}\n")
      if a.total_amount > max_score:
        best = a
        max_score = a.total_amount
        
      df1.write(f"{i} {a.name} {a.total_amount} {a.agent.score} {type}\n")
      
      if "GP_agent" in a.name:
        if a.agent.score >= a.agent.old_score:
          a.agent.replace_police()
    log.write(f"Vencedor: {best.name}\n")
    log.write(f"Score: {max_score}\n\n\n")  
  
  for a in agents:
     if "GP_agent" in a.name:
        a.agent.save_police_backup(type)
        a.agent.reset_police()