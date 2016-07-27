grepg
===

`grepg` (pronounced Grep G) is a python client for [GrepPage](https://www.greppage.com).  It allows you to access your cheat sheets without leaving the terminal.

![grepg screenshot](https://github.com/tejal29/grepg/raw/master/img/screenshot.png)

#Installation
To install `grepg` run

```
sudo pip install grepg
```

#Requirements
- python 2.7.3 and greater


#Usage

Enter user and topic name followed by an optional search string.

```
Usage: grepg -u <user_name> [-t <topic_name> -s <search_term>]

Options:
  -h, --help, --short-help
                        show this help message and exit.
  --long-help           show options from all registered modules, not just the
                        __main__ module.
  -v, --verbose         Log to stdout [default: False]
  -f, --force           Force fetch cheats and update cached cheats. Default
                        Cache TTL 10 seconds [default: False]
  -u USER, --user=USER  username
  -t TOPIC, --topic=TOPIC
                        topic
  -s SEARCH, --search=SEARCH
                        text to search
  -c, --colorize        colorize output [default: False]

Examples:
  grepg -u tejal29
  grepg -u tejal29 -t python
  grepg -u tejal29 -t python -s open

Defaults:
  To set default user, create a file in ~/.grepg.yml with
  user: test
  ttl_in_seconds: 86400 # 1 day
```


##List all topics for a user

```
$ grepg -u tejal29
User: tejal29, Last Fetched: 4 second(s) ago
Available Topics =>
scala	Shell	Vertica	Mac	Javascript	Python	Misc

```

##List all cheats for the `scala` topic for user `tejal29`

```
$ grepg -u tejal29 -t scala
User: tejal29, Topic: scala, Last Fetched: 0 second(s) ago
Convert List of string to Set
‘this is a list this’.split(‘ ‘).map(Word(_)).toSet

Case class example
case class Person(firstName: String, lastName:String)
...
```

##Search for a specific string

```
$ grepg -u tejal29 -t scala -s 'case class'
User: tejal29, Topic: scala, Search-Term: case, Last fetched: 5 second(s) ago
Case class example
case class Person(firstName: String, lastName:String)

Case Multiple match
val c: Char = 'f'
c match {
   case ‘,’ | ‘.’ => println(‘punctuation’)
   case _       => println(‘not punctuation’)
}

```


#Configuration
Setup defaults in `~/.grepg.yml`
Adding `ttl_in_seconds` will fetch all the cheats from until the cache is expired. If you want to access newly added cheats append `-f` to force fetch
```
user: tejal29
colorize: true
ttl_in_seconds: 86400 # 1 day

```

Now, you can do

```
$ grepg -t python
User: tejal29, Topic: python, Last fetched: 5 second(s) ago
...
```

#Advanced usage
`grepg -s` does a simply does an 'or' when multiple search terms specified on command line and cheat descriptions. In order to get finer results, you can change the `match_op` to 'and'
You can do that on command line via `--match-op`. The below command gives one match result instead of 2 shown in [Search for a specific string](#search-for-a-specific-string).

```
$ grepg -u tejal29 -t scala -s 'case class' --match-op and
User: tejal29, Topic: scala, Search-Term: case, Last fetched: 5 second(s) ago
Case class example
case class Person(firstName: String, lastName:String)

```
You can also specify the default `match_op` in `~/.grepg.yml`
```
user: tejal29
match_op: and
```

#Development
To run grepg client in dev mode,
```
./pants run src/python/grepg:bin -- -u tejal29 -t scala -s 'class case'
```
To execute tests run
```./pants test tests/python/grepg::```


# Installing grepg locally
First run pants goal setup_py
```
./pants setup-py src/python/grepg:grepg-packaged
```
This should place a dist/grepg-<version>.tar.gz in your workspace.
Unzip the tar
```
cd dist && tar -xvf grepg-<version>.tar.gz
```
Finally install the local package
```
cd grepg-<version>
pip install -e .
```
Now install grep locally from this zip.
#License
grepg is under the [MIT License](http://www.opensource.org/licenses/MIT).

#Related Projects
Ruby client for grepg https://github.com/evidanary/grepg