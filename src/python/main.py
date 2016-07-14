from __future__ import print_function

from optparse import SUPPRESS_HELP

from twitter.common import app, log
from twitter.common.log.options import LogOptions
from lib.grepg_client import CommandError, GrepgClient
from util.utils import get_config, get_user_name, print_util

TTL = 10  # 10 s

app.set_name("grepg")
app.set_usage("grepg -u <user_name> [-t <topic_name> -s <search_term>]")
app.add_option("-v", "--verbose", action="store_true", default=False, help="Log to stdout")
app.add_option("-f", "--force", action="store_true", default=False, help="Force fetch cheats and update cached cheats. Default Cache TTL 10 seconds")
app.add_option("-u", "--user", type="string", help="username")
app.add_option("-t", "--topic", type="string", help="topic")
app.add_option("-s", "--search", type="string", help="text to search")
app.add_option("-c", "--colorize", action="store_true", help="colorize output")
app.add_option("-b", "--base-url", type="string", help=SUPPRESS_HELP)
app.add_option("-a", "--access_token", type="string", help=SUPPRESS_HELP)
app.add_option("-m", "--match-op", type="string", help=SUPPRESS_HELP)



def main(args, options):
  if options.verbose:
    LogOptions.set_disk_log_level('NONE')
    LogOptions.set_stderr_log_level('google:DEBUG')

  username = get_user_name(options.user)
  colorize = options.colorize or get_config('colorize', default=False)
  ttl = get_config('ttl_in_seconds', default=TTL)
  match_op = options.match_op or get_config('match_op', default="or")
  if not match_op in ["and", "or"]:
    print_util("Invalid match operator '{0}'. Can only be ['and', 'or']".format(match_op), 'red', colorize)
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
      grepg_client.search_user_topic_cheats()
    elif options.topic:
      grepg_client.list_user_topic_cheats()
    else:
      grepg_client.get_user_topics()
  except CommandError as e:
    print_util(e.message, 'red', options.colorize)
    exit(1)

# Disable logging to disk
LogOptions.disable_disk_logging()
app.main()
