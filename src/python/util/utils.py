import os
import yaml


def get_user_name(user_opt):
  if user_opt:
    return user_opt
  home = os.path.expanduser("~")
  user_settings_file = os.path.join(home, 'grepg.yml')
  if os.path.exists(user_settings_file):
    with open(user_settings_file) as user_config_file:
      yaml_dict = yaml.load(user_config_file)
      if 'user' in yaml_dict:
        return yaml_dict['user']
  raise Exception('Either username should be specified as --user on command line or in the {0}'.format(user_settings_file))