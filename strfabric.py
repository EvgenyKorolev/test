from strategy import Worker
from strategy import AllInput
from strategy import ScreenInput
from strategy import OnlyErrInput
from strategy import FileInput
from strategy import TestStrat

#subscribers fabric
class StrFabric:
	def __init__(self):
		self._functions = {}
		self.registerFuncton(AllInput())
		self.registerFuncton(ScreenInput())
		self.registerFuncton(OnlyErrInput())
		self.registerFuncton(FileInput())

	def registerFuncton(self, func):

		method = getattr(func, 'name', None)
		if method is None or not callable(method):
			raise ValueError('This function is not contains method name!')

		keyValue = func.name()
		if not isinstance(keyValue, str):
			raise ValueError('Method key not returned string!')

		if not hasattr(func, 'run') or not callable(getattr(func, 'run')):
			raise ValueError('This function is not contains method run!')

		if not hasattr(func, 'create') or not callable(getattr(func, 'create')):
			raise ValueError('This function is not contains method create!')

		self._functions[func.name()] = func


	def getFunction(self, key: str):
		if key in self._functions:
			return self._functions.get(key, None).create()
		return None

	def availableFunctionsNames(self):
		return self._functions.keys()

	def availableFunctionsCount(self):
		return len(self._functions)