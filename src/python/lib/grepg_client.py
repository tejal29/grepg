from __future__ import print_function

from util.utils import match, print_util, since_time_in_words
from lib.cheat_sheets_cache import CheatSheetsCache
from lib.grepg_api import GrepgAPI

from twitter.common import log


class CommandError(Exception):
  def __init__(self, mesg):
    super(CommandError, self).__init__(mesg)


class GrepgClient(object):
  def __init__(self, username, topic, search_term, colorize, force, ttl, match_op, base_url=None, access_token=None, ):
    self.user_name = username
    self.topic = topic
    self.search_term = search_term
    self.force = force
    self.colorize = colorize
    self.ttl =ttl
    self.match_op = match_op
    self.api = GrepgAPI.get_grepg_api(base_url, access_token)

  def _get_user_topics(self):
    with CheatSheetsCache(self.ttl) as cs:
      if self.force or not cs.has_valid_user_cheat_sheets(self.user_name):
        log.debug('Fetching user cheats from server')
        user_sheet = self.api.sheets(self.user_name)
        cs.add_or_update_user_sheet(self.user_name, user_sheet)
      return cs.get_user_topics(self.user_name)

  def get_user_topics(self, print_header=True):
    (since_timestamp, topic_map) = self._get_user_topics()
    if print_header:
      print_util("User: {0}, Last Fetched: {1} ago".format(self.user_name, since_time_in_words(since_timestamp)),
                 'green', self.colorize)
    print_util("Available Topics =>", 'green', self.colorize)
    topics = [topic.topic_name for topic in topic_map.values()]
    print_util('\t'.join(topics), 'blue', self.colorize)

  def _get_user_topic_cheats(self):
    (_, topics) = self._get_user_topics()
    for topic in topics.values():
      if topic.topic_name.lower() == self.topic.lower():
        with CheatSheetsCache(self.ttl) as cs:
          if self.force or topic.is_expired(self.ttl) or not topic.cheats:
            log.debug('Fetching user topic cheats from server')
            cs.add_or_update_user_topic_sheet(self.user_name,
                                              topic.topic_id,
                                              topic.topic_name,
                                              self.api.user_topic_cheats(self.user_name, topic.topic_id))
        return cs.get_user_topic_cheat(self.user_name, topic.topic_id)
    self.get_user_topics(False)
    raise CommandError('Topic {0} not found'.format(self.topic))

  def list_user_topic_cheats(self):
    (since_timestamp, topic_cheats) = self._get_user_topic_cheats()
    print_util('User: {0}, Topic: {1}, Last Fetched: {2} ago'.format(self.user_name, self.topic, since_time_in_words(since_timestamp)),
               'green', self.colorize)
    self.print_cheats(topic_cheats)

  def print_cheats(self, topic_cheats):
    for cheat in topic_cheats:
      print_util(cheat.description, 'blue', self.colorize)
      print(cheat.command, "\n")

  def search_user_topic_cheats(self):
    (since_timestamp, user_topic_cheats) = self._get_user_topic_cheats()
    print_util('User: {0}, Topic: {1}, Search-Term: {2}, Last fetched: {3} ago'
       .format(self.user_name, self.topic, self.search_term, since_time_in_words(since_timestamp)),
      'green', self.colorize)

    search_results = filter(lambda topic_cheat: match(self.search_term, topic_cheat.description, self.match_op), user_topic_cheats)
    if search_results:
      self.print_cheats(search_results)
    else:
      raise CommandError("No results for search-term '{0}' and Topic {1}".format(self.search_term, self.topic))
