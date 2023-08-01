import unittest


from model import IrisModel, IrisSpecies


class TestIrisModel(unittest.TestCase):
   def test_model_initialization(self):
       new_model = IrisModel()
       self.assertIn('iris_model.pkl',new_model.model_fname_)
