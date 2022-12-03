class DataObject:
  @classmethod
  def create_from_entry(cls, data):
    print("entry : ", data)


class PumpsNormalBuses(DataObject):
  # @classmethod
  # def create(cls, **kwargs):
  #   return cls(**kwargs)
    
  def __init__(self, **kwargs):
    self.data_type = 'pumps_normal_boluses'
    print("creating ")
    for k in kwargs:
      print(k)
    
    super().__init__()
    
      
  