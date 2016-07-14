from __future__ import print_function

from datetime import datetime, timedelta
import os
import yaml

from termcolor import cprint

def user_dir():
  return os.path.expanduser("~")


def get_user_name(user_opt):
 return user_opt if user_opt else get_config('user')

def get_config(key_name, default=None):
  home = user_dir()
  user_settings_file = os.path.join(home, 'grepg.yml')
  if os.path.exists(user_settings_file):
    with open(user_settings_file) as user_config_file:
      try:
        yaml_dict = yaml.load(user_config_file)
        if key_name in yaml_dict:
          return yaml_dict[key_name]
      except Exception as e:
        raise e


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
    return '{0} min(s)'.format(detla.minute)
  else:
    return '{0} second(s)'.format(detla.second)