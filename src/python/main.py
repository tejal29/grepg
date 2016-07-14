from __future__ import print_function

from optparse import SUPPRESS_HELP

from twitter.common import app, log
from twitter.common.log.options import LogOptions
from lib.grepg_client import CommandError, GrepgClient
from util.utils import get_config, get_user_name, print_util

TTL = 86400  # 1 day

app.set_name("grepg")
app.set_usage("grepg -u <user_name> [-t <topic_name> -s <search_term>]")
app.add_option("-v", "--verbose", action="store_true", default=False, help="Log to stdout")
app.add_option("-f", "--force", action="store_true", default=False, help="Force fetch to get new cheats")
app.add_option("-u", "--user", type="string", help="username")
app.add_option("-t", "--topic", type="string", help="topic", default='Shell')
app.add_option("-s", "--search", type="string", help="text to search")
app.add_option("-c", "--colorize", action="store_true", default=False, help="colorize output")
app.add_option("-b", "--base-url", help=SUPPRESS_HELP)
app.add_option("-a", "--access_token", help=SUPPRESS_HELP)



def main(args, options):
  if options.verbose:
    LogOptions.set_disk_log_level('NONE')
    LogOptions.set_stderr_log_level('google:DEBUG')

  username = get_user_name(options.user)
  ttl = get_config('ttl_in_seconds', default=TTL)
  grepg_client = GrepgClient(username=username,
                            topic=options.topic,
                            search_term=options.search,
                            colorize=options.colorize,
                            force=options.force,
                            base_url=options.base_url,
                            ttl=ttl,
                            access_token=options.access_token)
  try:
    if options.search:
      grepg_client.search_user_topic_cheats()
    else:
      grepg_client.get_user_topics()
  except CommandError as e:
    print_util(e.message, 'red', options.colorize)
    exit(1)

# Disable logging to disk
LogOptions.disable_disk_logging()
app.main()
