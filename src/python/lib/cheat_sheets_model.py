import time

class TTLCache(object):
  def __init__(self):
    self.timestamp = time.time()

  def update_timestamp(self):
    self.timestamp = time.time()

  def get_fetched_since_in_seconds(self):
    return time.time() - self.timestamp

  def is_expired(self, ttl):
    return self.get_fetched_since_in_seconds() > ttl

class CheatSheet(TTLCache):
  def __init__(self, user_id, user_name, topics={}):
    super(CheatSheet, self).__init__()
    self.user_id = user_id
    self.user_name = user_name
    self.topics = topics

  def __str__(self):
    return('CheatSheet({0}, {1})'.format(str(self.user_id), self.user_name))

class Topic(TTLCache):
  def __init__(self, topic_id, topic_name, cheats=[]):
    super(Topic, self).__init__()
    self.topic_id = topic_id
    self.topic_name = topic_name
    self.cheats = cheats

  def __str__(self):
    return('Topic({0}, {1})'.format(str(self.topic_id), self.topic_name))


class Cheat(TTLCache):
  def __init__(self, description, command, cheat_id):
    super(Cheat, self).__init__()
    self.description = description
    self.command = command
    self.cheat_id = cheat_id

  def __str__(self):
    return('Cheat({0}, {1})'.format(self.description, str(self.cheat_id)))