from termcolor import colored, cprint

class Grepg(object):
  def __init__(self, username, topic, search_term, colorize, verbose):
    self.user_name = username
    self.topic = topic
    self.search_term = search_term
    self.verbose = verbose
    self.colorize = colorize

  def get_user_cheats(self):
    cprint(self.user_name, 'green')
    print("get_user_cheats NYI")

  def search(self):
    print("search NYI")