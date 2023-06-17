import random

class ReinforcementLearningAgent:
  def __init__(self):
    # Chance percentual do agente tomar a ação descrita na política
    self.epsilon = 0.9
    # Recompensa do agente
    self.score = 0
    # Quantidade total de dinheiro que o agente ganhou
    self.total_amount = 0
    # Lembrando a ultima acao
    self.last_opponent_action = None
    # Flag indicando se essa seria a ultima rodada
    self.last_round = False
    # Nome do arquivo da política do agente
    self.police = "police_7.txt"
    # Dicionário com a política do agente
    self.actions = {}
    # Recompensa da última melhor política
    self.old_score = 0

    try:
      self.read_police()
    except FileNotFoundError:
      self.reset_police()
      self.read_police()


  # Cria a estrutura do dicionário que armazenará a política do agente
  def create_actions_dictionary_structure(self, line):
    his_karma=line.split()[0]
    your_karma=line.split()[1]
    his_lastaction=line.split()[2]
    if his_karma not in self.actions:
      self.actions[his_karma] = {}
    if your_karma not in self.actions[his_karma]:
      self.actions[his_karma][your_karma] = {}
    if his_lastaction not in self.actions[his_karma][your_karma]:
      self.actions[his_karma][your_karma][his_lastaction] = {}
    
  # Lê o arquivo da política do agente
  def read_police(self):
    file = open(self.police,"r")
    for line in file:
      # Verifica se a linha é uma política ou se é a pontuação
      if len(line.split()) > 1:
        self.create_actions_dictionary_structure(line)

        if random.random() < self.epsilon:
          self.actions[line.split()[0]][line.split()[1]][line.split()[2]][line.split()[3]]=line.split()[4]
        else:
          self.actions[line.split()[0]][line.split()[1]][line.split()[2]][line.split()[3]]=random.choice(['0','1'])
      else:
        self.old_score = float(line)
    file.close()

  # Cria o arquivo da política completamente aleatório
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

  # Substitui o arquivo pela política atual
  def replace_police(self):
    police = open(self.police, "w")
    for his_karma in range(11):
        for your_karma in range(11):
            for his_lastaction in ["None","split","steal"]:
                for rounds_left in range (10):
                    police.write(str(his_karma-5) + " " + str(your_karma-5) + " " + his_lastaction + " " + 
                                 str(rounds_left) + " " + self.actions[str(his_karma-5)][str(your_karma-5)]
                                 [str(his_lastaction)][str(rounds_left)] + "\n")
    # Escreve a pontuação dessa política
    police.write(str(self.score))
    police.close()

  # Retona o nome do agente
  def get_name(self):
    return "GP_Agent"
  
  # Função que escolhe qual ação será tomada
  def decision(self, amount, rounds_left, your_karma, his_karma):

    # Verifica se é a última rodada
    self.last_round = True if rounds_left == 0 else False
    
    # Para diminuir o tamanho da política, o rounds_left tem um limite de 9
    if rounds_left>=10:
      rounds_left=9
  
    # Toma as ações baseadas na política, em que 0 representa dividir e 1 roubar
    if self.actions[str(his_karma)][str(your_karma)][str(self.last_opponent_action)][str(rounds_left)] == '0':
      return "steal"
    elif self.actions[str(his_karma)][str(your_karma)][str(self.last_opponent_action)][str(rounds_left)] == '1':
      return "split"
    else:
      raise RuntimeError("Unknown action")

  # Finaliza a rodada, calcula a recompensa do agente e verifica se a política será substituída 
  def result(self, your_action, his_action, total_possible, reward):
    if total_possible == reward:
      self.score += 2
    elif reward>0:
      self.score += 1
    elif your_action == "split":
      self.score -= 1
    self.total_amount += reward

    if self.score >= self.old_score:
      self.replace_police()
      print(self.score)

    if self.last_round:
      self.last_opponent_action = "None"
    else:   
      self.last_opponent_action = his_action

