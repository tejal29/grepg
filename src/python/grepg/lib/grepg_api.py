from __future__ import print_function

import json
import urllib2

from twitter.common import log

BASE_URL = 'https://www.greppage.com/api'
ACCESS_TOKEN = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsImFsZyI6IkhTMjU2IiwidHlwIjoiSldUIn0.eyJpZCI6MjAwMDAwMDAwMCwiZW1haWwiOiJndWVzdEBndWVzdC5jb20iLCJuYW1lIjoiZ3Vlc3QiLCJleHAiOjE1MTExMzY4MzB9.gWohR7LLtROgjSl5SxbEaGRBveZQEv7Uj2rzmgYrbys'


class GrepgAPI(object):
  @staticmethod
  def get_grepg_api(base_url, access_token):
    return GrepgAPI(base_url or BASE_URL, access_token or ACCESS_TOKEN)

  def __init__(self, base_url, access_token):
    self.base_url = base_url
    self.access_token = access_token

  def sheets_uri(self, user_name):
    return ('/').join([self.base_url, 'users', user_name, 'sheets_with_stats'])

  def cheats_uri(self, user_name, sheet_id):
    return ('/').join([self.base_url, 'users', user_name, 'sheets', str(sheet_id), 'cheats'])

  def sheets(self, user_name):
    return self.get(self.sheets_uri(user_name))

  def user_topic_cheats(self, user_name, sheet_id):
    return self.get(self.cheats_uri(user_name, sheet_id))

  def get(self, url):
    try:
      request = urllib2.Request(url)
      request.add_header('Authorization', self.access_token)
      log.debug("Get {0}".format(url))
      json_response = urllib2.urlopen(request).read()
      log.debug("Fetched resp {0}".format(json_response))
      return json.loads(json_response)
    except (urllib2.HTTPError, urllib2.URLError) as e:
      raise e