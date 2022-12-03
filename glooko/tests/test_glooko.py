


import unittest
from glooko import Glooko

class TestGlooko(unittest.TestCase):
  def test_main(self):
    glooko = Glooko(glooko_host='localhost:3000', glooko_host_scheme='HTTP', user='testuser', password='testpassword')
    result = glooko.endpoint_fetch('history')
    self.assertEqual(result, b'blah')  


if __name__ == '__main__':
    unittest.main()
    
    
