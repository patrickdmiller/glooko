from glooko.parsers.glooko_parser import GlookoParser
from glooko.data_objects import PumpsNormalBuses, DataObject

class GlookoParserHistory(GlookoParser):
  
  #TODO
  def parse(self, data):
    
    if "histories" not in data:
      raise Warning("no histories key found in data while parsing history")
    parsed = {}
    for entry in data['histories']:
      DataObject.create_from_entry(entry)
    return data
  