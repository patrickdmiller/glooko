from glooko.endpoints.glooko_endpoint import GlookoEndpoint
from glooko.common import config
from datetime import datetime,timezone, timedelta
import urllib
from glooko.parsers import GlookoParserHistory
## session.get(f'https://us.api.glooko.com/api/v3/users/summary/histories?patient={glooko_id}&startDate=2022-11-17T00:00:00.000Z&endDate=2022-11-30T23:59:59.999Z')
class GlookoEndpointHistory(GlookoEndpoint):
  def __init__(self, auth, glooko_host = config.GLOOKO_HOST, glooko_host_scheme = config.GLOOKO_HOST_SCHEME):
    
    super().__init__(
      parser = GlookoParserHistory(),
      name = 'history',
      glooko_host = glooko_host,
      glooko_host_scheme = glooko_host_scheme,
      path = '/api/v3/users/summary/histories',
      auth = auth
    )
    self.url = None
    
  def build_url(self,start_date=datetime.now(timezone.utc).replace(second=0, microsecond=0)-timedelta(days=1), end_date=datetime.now(timezone.utc).replace(second=0, microsecond=0)+timedelta(days=1)):
    params = {
      'patient':self.auth.glooko_id,
      'startDate':start_date.isoformat().replace("+00:00", "Z"),
      'endDate':end_date.isoformat().replace("+00:00", "Z")
    }
    self.url = urllib.parse.urlunsplit((self.glooko_host_scheme ,self.glooko_host, self.path, urllib.parse.urlencode(params),""))
