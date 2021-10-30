from speculator.utils import date
import unittest

class DateTest(unittest.TestCase):
    def test_shift_epoch(self):
        delorean = date.date_to_delorean(2000, 1, 1)
        shift = date.shift_epoch(delorean, 'last', 'day', 2)
        self.assertEqual(shift, 946512000)

    def test_generate_epochs(self):
        delorean = date.date_to_delorean(2000, 1, 1)
        gen = date.generate_epochs(delorean, 'last', 'day', 3)
        epochs = [e for e in gen]
        
        expected_epochs = [946684800, 946598400, 946512000]
        self.assertEqual(epochs, expected_epochs) 
        
