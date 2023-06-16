import random
import numpy as np
from itertools import combinations
import simple_opponents
import your_agent
import train_agent_5


mean = 100
variance = 10000  # Large variance

#Create Log file
log = open("Log.txt","w")


# Game settings
rounds_to_play = 10

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


    def render(self):
        #log.write(f"Rounds played: {self.rounds_played}/{self.total_rounds}\n\n")
        pass

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

    def render(self, x, y):
        #log.write(f"Name: {self.name}\n")
        #log.write(f"Amount: {self.total_amount:.2f}\n")
        pass

    
    def preround_render(self, x, y):
        #log.write(f"Karma: {self.karma}\n")
        
        #log.write(f"Name: {self.name}\n")
        
        #log.write((f"Amount: {self.total_amount:.2f}\n"))
        pass
        
    def render(self, x, y):
        #log.write(f"Karma: {self.karma}\n")
   
        #log.write(f"Name: {self.name}\n")
        pass


        # Draw decision
        #if self.last_decision == "split":
            #log.write("Split\n")
        #elif self.last_decision == "steal":
            #log.write("Steal\n")


    def decision(self, total_amount, rounds_played, your_karma, his_karma):
      self.last_decision = self.agent.decision(total_amount, rounds_played, your_karma, his_karma)
      return self.last_decision
      
    def result(self,  your_action, his_action, total_possible, reward):
      self.agent.result(your_action, his_action, total_possible, reward)


def play_round(game, agent1, agent2, remaining):
  log.write(f"{agent1.name} vs {agent2.name}\n")
  game.prepare_round()
  game.preround_render()
  agent1.preround_render(50, 50)
  agent2.preround_render(550, 50)        

  # Play a round
  game.play_round(agent1, agent2, remaining)

  # Render agents    
  agent1.render(50, 50)
  agent2.render(550, 50)
  game.render()

ntrains = 1
for i in range(ntrains):
  log.close()
  log = open("Log.txt","w")
  # Create agents
  agent1 = Player(simple_opponents.Splitter())
  agent2 = Player(simple_opponents.Stealer())
  agent3 = Player(simple_opponents.Randy())
  agent4 = Player(simple_opponents.Karmine())
  agent5 = Player(simple_opponents.Opportunist())
  agent6 = Player(simple_opponents.Pretender())
  agent_tittat = Player(your_agent.ReinforcementLearningAgent())

  # Allgame
  #agents = [agent1, agent2, agent3, agent4, agent5, agent6, ]

  # Simple
  #agents = [Player(simple_opponents.Karmine()),  Player(simple_opponents.Karmine()), Player(rl_agent.RLAgent()), agent_tittat]

  # Difficult 
  # agents = [Player(your_agent.ReinforcementLearningAgent()), Player(your_agent.ReinforcementLearningAgent()), Player(rl_agent.RLAgent()), Player(your_agent.ReinforcementLearningAgent())]

  # Very difficult
  # agents = [Player(simple_opponents.Pretender()), Player(simple_opponents.Pretender()), Player(rl_agent.RLAgent()), Player(simple_opponents.Karmine())]

  # Karma-aware
  # agents = [Player(simple_opponents.Karmine()), Player(simple_opponents.Karmine()), Player(rl_agent.RLAgent()), Player(simple_opponents.Stealer())]

  # Opportunists
  # agents = [Player(simple_opponents.Opportunist()),Player(simple_opponents.Opportunist()), Player(rl_agent.RLAgent()), agent_tittat]

  # 3 Karmines
  # agents = [Player(simple_opponents.Karmine()),  Player(simple_opponents.Karmine()), Player(rl_agent.RLAgent()), Player(simple_opponents.Karmine())]

  agents = [agent1, agent2, agent3, agent4, Player(your_agent.ReinforcementLearningAgent())]

  nrematches = 2 # Could very
  nfullrounds = 1 # How many full cycles
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

