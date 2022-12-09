from glooko.parsers.glooko_parser import GlookoParser
from glooko.data_objects import PumpsNormalBoluses, DataObject
import logging

class GlookoParserHistory(GlookoParser):

  def parse(self, data):    
    if "histories" not in data:
      raise Warning("no histories key found in data while parsing history")
    parsed = {}
    types_found = set()
    for entry in data['histories']:
      if 'type' in entry:
        types_found.add(entry['type'])
      obj = DataObject.create_from_entry(entry)
      logging.debug(obj)
      parsed[obj.guid] = obj
    logging.debug(f'all types found in history: {types_found}')
    return parsed
  