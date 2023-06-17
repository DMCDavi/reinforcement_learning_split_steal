import random

class ReinforcementLearningAgent:
  def __init__(self):
    self.score = 0
    self.score_total=0
    # Lembrando a ultima acao
    self.last_opponent_action = None
    
    # Flag indicando se essa seria a ultima rodada
    self.last_round = False

    #Reads the police
    self.police = "police_1.txt"
    self.actions = {}
    self.read_police()


  # Fix Vector into 4-matrix
  def fix_matrix(self, line):
    his_karma=line.split()[0]
    your_karma=line.split()[1]
    his_lastaction=line.split()[2]
    rounds_left=line.split()[3]
    if his_karma not in self.actions:
      self.actions[his_karma] = {}
    if your_karma not in self.actions[his_karma]:
      self.actions[his_karma][your_karma] = {}
    if his_lastaction not in self.actions[his_karma][your_karma]:
      self.actions[his_karma][your_karma][his_lastaction] = {}
    
  
  def read_police(self):
    file = open(self.police,"r")
    for line in file:
      if len(line.split()) > 1:
        self.fix_matrix(line)

        if random.random() < 0.7:
          self.actions[line.split()[0]][line.split()[1]][line.split()[2]][line.split()[3]]=line.split()[4]
        else:
          self.actions[line.split()[0]][line.split()[1]][line.split()[2]][line.split()[3]]=random.choice(['0','1'])
      else:
        self.old_score = float(line)
    file.close()

  def reset_police(self):
    police = open(self.police,"w")
    for his_karma in range(11):
        for your_karma in range(11):
            for his_lastaction in ["None","split","steal"]:
                for rounds_left in range (10):
                    r = random.choice([0,1])
                    police.write(str(his_karma-5) + " " + str(your_karma-5) + " " + his_lastaction + 
                                " " + str(rounds_left) + " " + str(r) + "\n")
    police.write("0")
    police.close()

  def replace_police(self):
    police = open(self.police, "w")
    for his_karma in range(11):
        for your_karma in range(11):
            for his_lastaction in ["None","split","steal"]:
                for rounds_left in range (10):
                    r = random.choice([0,1])
                    police.write(str(his_karma-5) + " " + str(your_karma-5) + " " + his_lastaction + " " + 
                                 str(rounds_left) + " " + self.actions[str(his_karma-5)][str(your_karma-5)]
                                 [str(his_lastaction)][str(rounds_left)] + "\n")
    police.write(str(self.score))
    police.close()

  # Nome de seu agente deve ser colocado aqui  
  def get_name(self):
    return "GP_agent"
  

  # Um exemplo basico de algo proximo de tit-for-tat
  # apenas como demonstracao. Agente de aprendizagem
  # por reforco seria o objetivo
  def decision(self, amount, rounds_left, your_karma, his_karma):

    self.last_round = True if rounds_left == 0 else False
    
    if rounds_left>=10:
      rounds_left=9
  
    if self.actions[str(his_karma)][str(your_karma)][str(self.last_opponent_action)][str(rounds_left)] == '0':
      return "steal"
    elif self.actions[str(his_karma)][str(your_karma)][str(self.last_opponent_action)][str(rounds_left)] == '1':
      return "split"
    else:
      raise RuntimeError("Unknown action")

  # Receba as acoes de cada agente e o reward obtido (vs total possivel)
  def result(self, your_action, his_action, total_possible, reward):
    if total_possible == reward:
      self.score += 2
    elif reward>0:
      self.score += 1
    elif your_action == "split":
      self.score -= 1
    self.score_total += reward
    #if self.score >= self.old_score:
      #self.replace_police()
      #print(self.score)
    if self.last_round:
      self.last_opponent_action = "None"
    else:   
      self.last_opponent_action = his_action

