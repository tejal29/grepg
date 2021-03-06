from __future__ import print_function

from optparse import SUPPRESS_HELP
import sys

from twitter.common import app, log
from twitter.common.app.application import Application as App
from twitter.common.log.options import LogOptions
from grepg.lib.grepg_client import CommandError, GrepgClient
from grepg.util.utils import get_config, get_user_name, log_query, print_util

TTL = 10  # 10 s

def main(args, options):
  if options.verbose:
    LogOptions.set_disk_log_level('NONE')
    LogOptions.set_stderr_log_level('google:DEBUG')

  username = get_user_name(options.user)

  if options.colorize and not options.no_colorize:
    print("Cannot have both --colorize and --no-colorize on command line")
    exit(1)

  colorize = options.colorize or get_config('colorize', default=False)
  log_queries_dir = options.log_queries_dir or get_config('log_queries_dir', default=None)
  if not options.no_colorize:
    colorize = False
  ttl = get_config('ttl_in_seconds', default=TTL)
  match_op = options.match_op or get_config('match_op', default="or")
  if not match_op.upper() in ["AND", "OR"]:
    print_util("Invalid match operator '{0}'. Can only be ['AND', 'OR']".format(match_op), 'red', colorize)
    exit(1)
  grepg_client = GrepgClient(username=username,
                            topic=options.topic,
                            search_term=options.search,
                            colorize=colorize,
                            force=options.force,
                            ttl=ttl,
                            match_op=match_op,
                            base_url=options.base_url,
                            access_token=options.access_token)
  try:
    if options.search:
      count = grepg_client.search_user_topic_cheats()
    elif options.topic:
      count = grepg_client.list_user_topic_cheats()
    else:
      count = grepg_client.get_user_topics()
    log_query(log_queries_dir, username, options.topic, options.search, count)
  except CommandError as e:
    log_query(log_queries_dir, username, options.topic, options.search, 0)
    print_util(e.message, 'red', colorize)
    exit(1)


def main_run():
  # Disable logging to disk
  LogOptions.disable_disk_logging()
  # To set usage for help
  add_options(app)
  app_obj = App()
  # Actually add options to the app object
  add_options(app_obj)
  app_obj.init()
  app_obj.shutdown(main(app_obj._argv, app_obj._option_values))

def add_options(app_obj):
  app_obj.set_name("grepg")
  app_obj.set_usage("grepg -u <user_name> [-t <topic_name> -s <search_term>]")
  app_obj.add_option("-v", "--verbose", action="store_true", default=False, help="Log to stdout")
  app_obj.add_option("-f", "--force", action="store_true", default=False, help="Force fetch cheats and update cached cheats. Default Cache TTL 10 seconds")
  app_obj.add_option("-u", "--user", type="string", help="username")
  app_obj.add_option("-t", "--topic", type="string", help="topic")
  app_obj.add_option("-s", "--search", type="string", help="text to search")
  app_obj.add_option("-c", "--colorize", action="store_true", help="colorize output")
  app_obj.add_option("-n", "--no-colorize", default= True, action="store_false", help="no colorize output")
  app_obj.add_option("-b", "--base-url", type="string", help=SUPPRESS_HELP)
  app_obj.add_option("-a", "--access_token", type="string", help=SUPPRESS_HELP)
  app_obj.add_option("-m", "--match-op", type="string", help="Match operator to match multiple search token. One of:  'And', 'Or'")
  app_obj.add_option("-l", "--log-queries-dir", type="string", help="Directory where you want all the queries to be written")
