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
    self.actions = {}
    self.read_police()

    
  
  def read_police(self):
    police = open("police.txt","r")
    for line in police:
      if len(line.split()) > 1:
        if random.random() < 0.2:
          self.actions[line.split()[0]]=line.split()[1]
        else:
          self.actions[line.split()[0]]=random.choice(['0','1'])
      else:
        self.old_score = float(line)
    police.close()

  def reset_police(self):
    police = open("police.txt","w")
    for i in range(11):
      r = random.choice(range(2))
      police.write(str(i-5) + " " + str(r) + "\n")
    police.close()

  def replace_police(self):
    police = open("police.txt", "w")
    for i in range(11):
      police.write(str(i-5) + " " + self.actions[str(i-5)] + "\n")
    police.write(str(self.score))
    police.close()

  # Nome de seu agente deve ser colocado aqui  
  def get_name(self):
    return "Grupo/Apelido"

  # Um exemplo basico de algo proximo de tit-for-tat
  # apenas como demonstracao. Agente de aprendizagem
  # por reforco seria o objetivo
  def decision(self, amount, rounds_left, your_karma, his_karma):

    self.last_round = True if rounds_left == 0 else False
    
  
    if self.actions[str(his_karma)] == '0':
      return "steal"
    elif self.actions[str(his_karma)] == '1':
      return "split"
    else:
      raise RuntimeError("Unknown action")

  # Receba as acoes de cada agente e o reward obtido (vs total possivel)
  def result(self, your_action, his_action, total_possible, reward):
    if total_possible == reward:
      self.score += 2
    elif total_possible == reward*2:
      self.score += 1
    self.score_total += reward
    #if self.score >= self.old_score:
      #self.replace_police()
      #print(self.score)
    if self.last_round:
      self.last_opponent_action = None
    else:   
      self.last_opponent_action = his_action

