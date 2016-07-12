from twitter.common import app
from lib.grepg import Grepg
from util.utils import get_user_name


app.set_name("grepg")
app.set_usage("grepg -u <user_name> [-t <topic_name> -s <search_term>]")
app.add_option("-v", "--verbose", action="store_true", default=False, help="Log to stdout")
app.add_option("-u", "--user", type="string", help="username")
app.add_option("-t", "--topic", type="string", help="topic")
app.add_option("-s", "--search", type="string", help="text to search")
app.add_option("-c", "--colorize", action="store_true", default=False, help="colorize output")

def main(args, options):
  username = get_user_name(options.user)
  grepgClient = Grepg(username=username,
                      topic=options.topic,
                      search_term=options.search,
                      colorize=options.colorize,
                      verbose=options.verbose)
  if options.search:
    grepgClient.search()
  else:
    grepgClient.get_user_cheats()
app.main()
