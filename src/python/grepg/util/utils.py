from __future__ import print_function

from datetime import datetime, timedelta
import os
import yaml

from termcolor import cprint

from twitter.common.dirutil import safe_open

def user_dir():
  return os.path.expanduser("~")


def get_user_name(user_opt):
 user_name = user_opt if user_opt else get_config('user')
 if user_name:
   return user_name
 else:
   raise Exception('Either username should be specified as --user on command line or in the {0}/.grepg.yml'.format(user_dir()))

def get_config(key_name, default=None):
  home = user_dir()
  user_settings_file = os.path.join(home, '.grepg.yml')
  if os.path.exists(user_settings_file):
    with open(user_settings_file) as user_config_file:
      try:
        yaml_dict = yaml.load(user_config_file)
        if key_name in yaml_dict:
          return yaml_dict[key_name]
      except Exception as e:
        raise e
  return default


def print_util(string, color, colorize):
  if colorize:
    cprint(string, color)
  else:
    print(string)


def since_time_in_words(time_in_seconds):
  detla = datetime(1,1,1) + timedelta(seconds=int(time_in_seconds))
  if detla.day-1:
    return '{0} day(s)'.format(detla.day-1)
  elif detla.hour:
    return '{0} hour(s)'.format(detla.hour)
  elif detla.minute:
    return '{0} minute(s)'.format(detla.minute)
  else:
    return '{0} second(s)'.format(detla.second)


def match(query_str, string, match_op="or"):
  query_terms = set([word.lower() for word in query_str.split()])
  document_words =  set([word.lower() for word in string.split()])
  if match_op == "or":
    for query_term in query_terms:
      for word in document_words:
        if query_term in word:
          return True
    return False
  else:
    for query_term in query_terms:
      found = False
      for word in document_words:
        if query_term in word:
          found = True
      if not found:
        return found
    return True

def log_query(dir, user, topic, search_str, count):
  if not dir:
    return
  current_date_iso = datetime.utcnow().isoformat() + 'Z'
  with safe_open(os.path.join(dir, 'grepg.log'), 'a') as fp:
    fp.write("{0}\t{1}\t{2}\t{3}\t{4}\n".format(current_date_iso, user, topic, search_str, count))