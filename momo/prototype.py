import pandas as pd


class Prototype(pd.Series):
	def __init__(self, data=None, index=None):
		super().__init__(data=data, index=index)

	def set_marks(self, marks_list):
		self[:] = pd.Series(data=marks_list, index=self.index)
