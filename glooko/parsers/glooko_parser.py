from abc import ABC, abstractmethod

class GlookoParser(ABC):
  @abstractmethod
  def parse(self, data):
    pass
  
