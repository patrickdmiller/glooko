#todo parse out data
'''

both of these entries have a UTC timestamp but the event actually happened at the same time but with an EST timestamp
for example, this happened at 16:40EST but the timestamp on the pump is 16:40UTC

{
  'type': 'pumps_readings', 
  'item': 
    {'pumpTimestamp': '2022-11-18T16:40:49.000Z', 
    'pumpTimestampUtcOffset': '-05:00', 
    'pumpGuid': '9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d', 
    'syncTimestamp': '2022-11-18T22:37:26.782Z', 'type': 'manual', 'value': 7500, 'mealTag': 'none', 'mealTagSource': 'meter', 'guid': '6f1b89f7-f882-4d8b-bb0d-f2b9c6099e90', 'softDeleted': False, 'updatedAt': '2022-11-19T03:37:32.451Z', 'updatedBy': 'server'}, 'guid': '6f1b89f7-f882-4d8b-bb0d-f2b9c6099e90', 'softDeleted': False, 'updatedAt': '2022-11-19T03:37:32.451Z', 'updatedBy': 'server'}


{'type': 'pumps_normal_boluses', 'item': 
{'pumpTimestamp': '2022-11-18T06:35:29.000Z', 'pumpTimestampUtcOffset': '-05:00', 
'pumpGuid': '9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d', 
'syncTimestamp': '2022-11-18T17:37:20.256Z', 'insulinDelivered': 1.9, 'carbsInput': 22, 'guid': 'eb5ebc5e-32fc-4479-a73a-866fca11300d', 'historyShowInsulin': True, 'historyShowCarbs': True, 'softDeleted': False, 'updatedAt': '2022-11-18T22:37:21.520Z', 'updatedBy': 'server'}, 'guid': 'eb5ebc5e-32fc-4479-a73a-866fca11300d', 'softDeleted': False, 
'updatedAt': '2022-11-18T22:37:21.520Z', 'updatedBy': 'server'}

For now I'll assume that the pump timestamp (and other timestamps )

synctimestamp - the time the server received this data.
'''
import logging
from glooko.common.helpers import glooko_pump_ts_to_UTC
class DataObject:
  @classmethod
  def create_from_entry(cls, data):
    if 'type' in data:
      if data['type'] == 'pumps_normal_boluses':
        obj =  PumpsNormalBoluses(**data)
        # print(obj)
        return obj
      
      elif data['type'] == 'pumps_readings':
        # print(data)
        return GenericDataObject(**data)
      else:
        return GenericDataObject(**data)
      
  def __repr__(self):
    return f'{self.data_type} : guid:{self.guid}'
  
class GenericDataObject(DataObject):
  def __init__(self, **kwargs):
    super().__init__()
    
    self.data_type = 'generic'
    self.from_type = None
    self.guid=None
    self.attributes = {}
    if 'type' in kwargs:
      self.from_type = kwargs['type']
    if 'guid' in kwargs:
      self.guid = kwargs['guid']
    self.attributes = {}
    for k in kwargs:
      self.attributes[k] = kwargs[k]
  
class PumpsNormalBoluses(DataObject):
  def __init__(self, **kwargs):
    super().__init__()
    self.data_type = 'pumps_normal_boluses'
    if 'guid' in kwargs:
      self.guid = kwargs['guid']

    self.timestamp = None
    self.insulinDelivered = 0
    self.carbsInput = 0
    
    if 'item' not in kwargs:
      logging.warning(self.data_type, "missing item when creating object")
    else:
      self.timestamp = glooko_pump_ts_to_UTC(kwargs['item']['pumpTimestamp'])
      self.insulinDelivered = kwargs['item']['insulinDelivered']
      self.carbsInput = kwargs['item']['carbsInput']
      
    
  
  def __repr__(self):
    s = super().__repr__()
    return f'{s} ts: {self.timestamp}, insulin:{self.insulinDelivered}, carbs: {self.carbsInput}'