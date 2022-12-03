from abc import ABC, abstractmethod
from glooko.common import config, enums

class GlookoEndpoint(ABC):  
  def __init__(self, parser, name, path, auth, glooko_host = config.GLOOKO_HOST, glooko_host_scheme = config.GLOOKO_HOST_SCHEME):
    self.parser = parser
    self.name = name
    self.path = path
    self.auth = auth
    self.glooko_host = glooko_host  
    self.glooko_host_scheme = glooko_host_scheme
  @abstractmethod
  def build_url(self, *args, **kwargs):
    pass

  def fetch(self, url=None):
    if not self.auth or not self.auth.session or self.auth.glooko_id:
      self.handle_error(error_code = enums.ErrorCode.NO_AUTH)
    
    #fetch it. 
    if not self.url:
      self.build_url()
    r = self.auth.session.get(self.url)
    if r.status_code != 200:
      self.error(r)
    return self.parser.parse(r.content)
  
  def handle_error(self, error_code):
    if error_code == enums.ErrorCode.NO_AUTH :
      #have to recreate auth
      if self.auth.user is None or self.auth.password is None:
        raise Exception("please reinsantiate auth obj and pass it the correct values")
    elif error_code == enums.ErrorCode.Expired:
      self.auth.get_or_refresh()