import random
import shutil
import numpy as np

class ReinforcementLearningAgent:
  def __init__(self, id=1):
    # Identificador do agente
    self.id = id
    # Chance percentual do agente tomar a ação descrita na política
    self.epsilon = 1
    # Recompensa do agente
    self.score = 0
    # Quantidade total de dinheiro que o agente ganhou
    self.total_amount = 0
    # Lembrando a ultima acao
    self.last_opponent_action = None
    # Flag indicando se essa seria a ultima rodada
    self.last_round = False
    # Nome do arquivo da política do agente
    self.police = f"gp_police_{id}.txt"
    # Dicionário com a política do agente
    self.actions = {}
    # Recompensa da última melhor política
    self.old_score = 0
    # Variáveis da decisão
    self.rounds_left = 0
    self.his_karma = 0
    self.your_karma = 0
    # Learn Rate
    self.lr = 0
    # Future Importance
    self.fi = 0.9
    # Quantidade de decisões que o agente tomou
    self.ndecisions = 0

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
    rounds_left=line.split()[3]
    if his_karma not in self.actions:
      self.actions[his_karma] = {}
    if your_karma not in self.actions[his_karma]:
      self.actions[his_karma][your_karma] = {}
    if his_lastaction not in self.actions[his_karma][your_karma]:
      self.actions[his_karma][your_karma][his_lastaction] = {}
    if rounds_left not in self.actions[his_karma][your_karma][his_lastaction]:
      self.actions[his_karma][your_karma][his_lastaction][rounds_left] = {}
    
  # Lê o arquivo da política do agente
  def read_police(self):
    file = open(self.police,"r")
    for line in file:
      # Verifica se a linha é uma política ou se é a pontuação
      if len(line.split()) > 1:
        self.create_actions_dictionary_structure(line)

        self.actions[line.split()[0]][line.split()[1]][line.split()[2]][line.split()[3]][line.split()[4]]=float(line.split()[5])
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
                    for decision in ["split","steal"]:
                      police.write(str(his_karma-5) + " " + str(your_karma-5) + " " + his_lastaction + 
                                  " " + str(rounds_left) + " " + decision + " 0\n")
    police.write("0")
    police.close()

  # Substitui o arquivo pela política atual
  def replace_police(self):
    police = open(self.police, "w")
    for his_karma in range(11):
        for your_karma in range(11):
            for his_lastaction in ["None","split","steal"]:
                for rounds_left in range (10):
                    for decision in ["split","steal"]:
                      police.write(str(his_karma-5) + " " + str(your_karma-5) + " " + his_lastaction + " " + 
                                  str(rounds_left) + " " + decision + " " +str(self.actions[str(his_karma-5)][str(your_karma-5)]
                                  [str(his_lastaction)][str(rounds_left)][decision]) + "\n")
    police.write(str(self.score))
    police.close()

  # Salva a cópia da última política para o tipo de jogo
  def save_police_backup(self, game_type):
    shutil.copy2(self.police, f"trained_{game_type}_{self.police}")

  # Retona o nome do agente
  def get_name(self):
    return f"GP_agent_{self.id}"
  
  # Função que escolhe qual ação será tomada
  def decision(self, amount, rounds_left, your_karma, his_karma):
    
    # Verifica se é a última rodada
    self.last_round = True if rounds_left == 0 else False
    
    # Para diminuir o tamanho da política, o rounds_left tem um limite de 9
    if rounds_left>=10:
      rounds_left=9

    # Salva os dados da decisão
    self.rounds_left = rounds_left
    self.his_karma = his_karma
    self.your_karma = your_karma

    # Escolhe se vai seguir a política (exploit) ou não (explore) com base no valor de epsilon
    if random.random() < self.epsilon:
      r_split = float(self.actions[str(his_karma)][str(your_karma)][str(self.last_opponent_action)][str(rounds_left)]["split"])
      r_steal = float(self.actions[str(his_karma)][str(your_karma)][str(self.last_opponent_action)][str(rounds_left)]["steal"])
      # Escolhe a ação que tem a maior pontuação
      if r_split>r_steal:
        return "split"
      else:
        return "steal"
    else:
      return random.choice(["split","steal"])

  # Calcula e seta a média do score de acordo a quantidade de decisões
  def set_mean_decisions_score(self, score):
    self.score *= self.ndecisions
    self.score += score
    self.ndecisions += 1
    self.score /= self.ndecisions

  # Calcula o score da ação tomada com base em estados futuros
  def calculate_action_score(self, your_action, his_action, score):
    # Calcula o karma do agente com base na ação
    if your_action == "split":
      future_your_karma = self.your_karma+1 if self.your_karma < 5 else 5
    else:
      future_your_karma = self.your_karma-1 if self.your_karma > -5 else -5

    # Calcula o karma do oponente com base na ação dele
    if his_action == "split":
      future_his_karma = self.his_karma+1 if self.his_karma < 5 else 5
    else:
      future_his_karma = self.his_karma-1 if self.his_karma > -5 else -5

    # Diminui em 1 a quantidade de rodadas faltantes para a ação futura 
    future_rounds_left = self.rounds_left-1
    # Verifica qual o score da ação que será tomada na próxima rodada
    if future_rounds_left >=0:
      f_split = self.actions[str(future_his_karma)][str(future_your_karma)][str(his_action)][str(future_rounds_left)]["split"]
      f_steal = self.actions[str(future_his_karma)][str(future_your_karma)][str(his_action)][str(future_rounds_left)]["steal"]
      future = f_split if f_split > f_steal else f_steal
    else:
      future=0

    action_score = self.actions[str(self.his_karma)][str(self.your_karma)][str(self.last_opponent_action)][str(self.rounds_left)][your_action]
    # Calcula a recompensa com base no futuro e taxas de aprendizado
    return self.lr*(score+self.fi*future)+(1-self.lr)*action_score

  # Finaliza a rodada e calcula a recompensa do agente
  def result(self, your_action, his_action, total_possible, reward):
    if total_possible == reward:
      score = 2
    elif reward>0:
      score = 1
    elif your_action == "split":
      score = -1
    else:
      score = 0

    self.total_amount += reward

    self.set_mean_decisions_score(score)

    action_score = self.calculate_action_score(your_action, his_action, score)

    self.actions[str(self.his_karma)][str(self.your_karma)][str(self.last_opponent_action)][str(self.rounds_left)][your_action]=action_score
    
    # Salva a última ação do oponente
    if self.last_round:
      self.last_opponent_action = "None"
    else:   
      self.last_opponent_action = his_action