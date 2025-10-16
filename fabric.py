from subscriber import PrintOutput
from subscriber import SentToAllOutput
from subscriber import WriteToFile
from subscriber import PrintInErr
from subscriber import PrintNull

#subscribers fabric
class InputFabric:
	def __init__(self):
		self._functions = {}
		self.registerFuncton(PrintOutput())
		self.registerFuncton(SentToAllOutput())
		self.registerFuncton(WriteToFile())
		self.registerFuncton(PrintInErr())
		self.registerFuncton(PrintNull())

	def registerFuncton(self, func):

		method = getattr(func, 'key', None)
		if method is None or not callable(method):
			raise ValueError('This function is not contains method key!')

		keyValue = func.key()
		if not isinstance(keyValue, str):
			raise ValueError('Method key not returned string!')

		if not hasattr(func, 'update') or not callable(getattr(func, 'update')):
			raise ValueError('This function is not contains method update!')

		self._functions[func.key()] = func


	def getFunction(self, key: str):
		return self._functions.get(key, None)