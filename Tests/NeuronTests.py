import unittest
import Neurons as n

class TestNeurons(unittest.TestCase):
	def setUp(self):
		self.arr = np.array([1,2,3,4])

	def testSoftmaxFire(self):
		neuron = n.SoftMax()
		arr = neuron.fire(self.arr)
		self.assertEquals(len(arr), len(self.arr))


unittest.main()

