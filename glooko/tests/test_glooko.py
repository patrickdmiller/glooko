import unittest
import logging
from glooko import Glooko
from glooko.common.helpers import glooko_pump_ts_to_UTC

logging.basicConfig(level=logging.DEBUG)

class TestGlooko(unittest.TestCase):
  def test_main(self):
    glooko = Glooko(glooko_host='localhost:3000', glooko_host_scheme='HTTP', user='testuser', password='testpassword')
    result = glooko.endpoint_fetch(endpoint_key = 'history')
    glooko.close()
    # self.assertEqual(result, b'blah')  
    print(glooko_pump_ts_to_UTC('2022-11-18T16:40:49.000Z'))

if __name__ == '__main__':
    unittest.main()
    
    
