import re
from glooko.parsers.glooko_parser import GlookoParser
class GlookoParserID(GlookoParser):
  def parse(self, data):
    glooko_id = re.search(r'glooko_code: .*,', data)
    if glooko_id:
      glooko_id = re.sub(r'".*', '',re.sub(r'glooko_code: *"', '',glooko_id.group()))
    if not glooko_id:
      raise Exception("unable to parse glooko_id")
    return glooko_id