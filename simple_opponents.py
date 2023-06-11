import random

def always_split_callback(total_amount, rounds_left, your_karma, his_karma):
    return 'split'

def always_steal_callback(total_amount, rounds_left, your_karma, his_karma):
    return 'steal'

def always_random_callback(total_amount, rounds_left, your_karma, his_karma):
    return random.choice(['steal', 'split'])

def always_his_karma_callback(total_amount, rounds_left, your_karma, his_karma):
    return "split" if his_karma >= 0 else "steal" 



class StaticAgent:

  def __init__(self, name, decision_callback):
    self.decision_callback = decision_callback
    self.name = name
    
  def get_name(self):
    return self.name

  def decision(self, total_amount, rounds_left, your_karma, his_karma):
    return self.decision_callback(total_amount, rounds_left, your_karma, his_karma)

  def result(self, your_action, his_action, total_possible, reward):
    pass

class Splitter(StaticAgent):
  def __init__(self):
    StaticAgent.__init__(self, "Splitter", always_split_callback)
    
class Randy(StaticAgent):
  def __init__(self):
    StaticAgent.__init__(self, "Randy", always_random_callback)    

    
class Stealer(StaticAgent):
  def __init__(self):
    StaticAgent.__init__(self, "Stealer", always_steal_callback)    

class Karmine(StaticAgent):
  def __init__(self):
    StaticAgent.__init__(self, "Karmine", always_his_karma_callback)    



