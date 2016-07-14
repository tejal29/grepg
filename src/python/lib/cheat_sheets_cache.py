import os
import pickle

from lib.cheat_sheets_model import *
from util.utils import user_dir


class CheatSheetsCache(object):
  def __init__(self, ttl, file=None, cheat_sheets={}):
    self.ttl = ttl
    self.file = file or os.path.join(user_dir(), ".sheets.pickle")
    self.cheat_sheets = cheat_sheets

  def __enter__(self):
    if os.path.exists(self.file):
      try:
        with open(self.file) as fp:
          self.cheat_sheets = pickle.load(fp)
      except Exception as e:
        self.cheat_sheets = self.cheat_sheets
    else:
      self.cheat_sheets = self.cheat_sheets
    return self

  def has_valid_user_cheat_sheets(self, user):
    return user in self.cheat_sheets and not self.cheat_sheets[user].is_expired(self.ttl)

  def get_user_topics(self, user):
    return (self.cheat_sheets[user].get_fetched_since_in_seconds(), self.cheat_sheets[user].topics)

  def add_or_update_user_sheet(self, user, json_user_sheet):
    user_id = None
    topics = {}
    for json_topic in json_user_sheet:
      user_id = json_topic['user_id']
      topics[json_topic['id']] = Topic(topic_id=json_topic['id'], topic_name=json_topic['name'])
    if user_id:
      self.cheat_sheets[user] = CheatSheet(user_id=user_id, user_name=user, topics=topics)

  def get_user_topic_cheat(self, user, topic_id):
    return (self.cheat_sheets[user].topics[topic_id].get_fetched_since_in_seconds(), self.cheat_sheets[user].topics[topic_id].cheats)

  def add_or_update_user_topic_sheet(self, user, topic_id, topic_name, json_user_topic_cheats):
    cheats = [Cheat(item['description'], item['command'], item['id']) for item in json_user_topic_cheats]
    self.cheat_sheets[user].topics[topic_id] = Topic(topic_id=topic_id, topic_name=topic_name, cheats=cheats)

  def __exit__(self, exc_type, exc_val, exc_tb):
    with open(self.file, "wb") as output:
      pickle.dump(self.cheat_sheets, output, pickle.HIGHEST_PROTOCOL)


