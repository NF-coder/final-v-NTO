import numpy as np

class Portf:
	def __init__(self,mean_matrix,cov_matrix, portf_count):
		self.mean_matrix = mean_matrix
		self.cov_matrix = cov_matrix
		self.portf_count = portf_count
		self.count = len(list(self.mean_matrix.index))

	def rand(self):
		res = np.exp(np.random.randn(self.count))
		res = res / res.sum()
		return res

	def profit(self,randPortf):
		return np.matmul(self.mean_matrix.values,randPortf)

	def risk(self, randPortf):
		return np.sqrt(np.matmul(np.matmul(randPortf,self.cov_matrix.values),randPortf))

	def model(self):
		risk = np.zeros(self.portf_count)
		doh = np.zeros(self.portf_count)
		portf = np.zeros((self.portf_count,self.count))

		for n in range(self.portf_count):
			rand_p = self.rand()
			profit_p = self.profit(rand_p)
			risk_p = self.risk(rand_p)

			portf[n,:] = rand_p
			risk[n] = risk_p
			doh[n] = profit_p

		return risk,doh,portf,self.count