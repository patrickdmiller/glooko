from glooko.common import config
from glooko.endpoints import GlookoEndpointHistory
from glooko.parsers import GlookoParserID
import pickle as pk
import os
import urllib
import requests
from lxml import html

class Glooko_Auth:
  @classmethod
  def load_or_factory(cls, cache_file = 'glooko_auth.pk', user='_', password='_', *args, **kwargs):
    #check if a file exists
    if os.path.exists(cache_file):
      print("loading from cache")
      with open(cache_file, 'rb') as f:
        obj = pk.load(f)
        if obj.user != user or obj.password!=password:
          print("different user, recreating")
        else:
          return obj
    print("instantiating")
    return cls(cache_file = cache_file, user = user, password = password, *args, **kwargs)
    
  def __init__(self, cache_file='glooko_auth.pk', user=None, password=None, glooko_host = config.GLOOKO_HOST, glooko_host_scheme = config.GLOOKO_HOST_SCHEME, debug = False):
    self.cache_file = cache_file
    self.glooko_host = glooko_host
    self.glooko_host_scheme = glooko_host_scheme
    self.cookie_jar = None
    self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
    self.glooko_id = None
    self.login_url = urllib.parse.urlunsplit((self.glooko_host_scheme, self.glooko_host,'/users/sign_in',"","" ))
    self.after_login_url = urllib.parse.urlunsplit((self.glooko_host_scheme, self.glooko_host,'/history',"","" ))
    self.session =None
    self.user = user
    self.password = password
    self.debug = debug
    
    self.get_or_refresh()
    
    
  def get_or_refresh(self):
    self.session = requests.Session()
    r = self.session.get(self.login_url, headers = self.headers)
    if self.debug:
      print(r.content)
    tree = html.fromstring(r.content)
    payload = {
      'user[email]':self.user,
      'user[password]':self.password,
      'authenticity_token':tree.xpath('//input[@name="authenticity_token"]/@value')[0]
    }
    
    if not payload['authenticity_token']:
      raise Exception("no authenticity token found. page likely changed.")
    if self.debug:
      print(payload)
    r = self.session.post(self.login_url, data=payload, headers=self.headers)
    if r.status_code != 200:
      self.error(r)
      
    self.cookie_jar = r.cookies
    r = self.session.get(self.after_login_url)
    if self.debug:
      print(r.content)
    if r.status_code != 200:
      self.error(r)
    self.glooko_id = GlookoParserID().parse(r.text)
    self.cache()
    
  def cache(self):
    print("caching!")
    with open(self.cache_file, 'wb') as f:
      pk.dump(self, f)
  
  def error(self, r):
    raise Exception("auth error", r.status_code)
  
  
  
class Glooko:
  def __init__(self, glooko_host = config.GLOOKO_HOST, glooko_host_scheme = config.GLOOKO_HOST_SCHEME, user=None, password=None, auth_object=None):
    self.glooko_host = glooko_host
    self.glooko_host_scheme = glooko_host_scheme
    self.endpoints = {}
    self.data = {}
    if auth_object:
      self.auth = auth_object
    elif user and password:
      self.auth = Glooko_Auth(
        user = user,
        password = password,
        glooko_host= glooko_host,
        glooko_host_scheme = glooko_host_scheme
      )
    else:
      raise Exception("No credentials or auth_object provided")
    
    self.add_endpoint(GlookoEndpointHistory, 'history')
    
  def add_endpoint(self, endpoint, key):
    self.endpoints[key] = (endpoint(
      auth = self.auth,
      glooko_host = self.glooko_host,
      glooko_host_scheme = self.glooko_host_scheme
    ))
    self.data[key] = None
    
  def endpoint_fetch(self, key):
    if key not in self.endpoints:
      raise Exception("no endpoint found for key", key)
    self.data[key] = self.endpoints[key].fetch()
    return self.data[key]
  
  