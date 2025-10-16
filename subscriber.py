import subprocess
import sys
from abc import ABC, abstractmethod

# subsctiber interface
class Subscriber(ABC):
	@abstractmethod
	def update(self, message: str): pass
	@abstractmethod
	def key(self): pass


class PrintOutput(Subscriber):
	def __init__(self): pass

	def key(self):
		return 'stdout'

	def update(self, message: str):
		print(message)


class SentToAllOutput(Subscriber):
	def __init__(self): pass

	def key(self):
		return 'wall'

	def update(self, message: str):
		try:
			process = subprocess.Popen(['wall'], stdin=subprocess.PIPE, text=True)
			process.communicate(input=message)
			return
		except Exception as e:
			return


class WriteToFile(Subscriber):
	def __init__(self):
		self._fileName = 'log.txt'

	def key(self):
		return 'file'

	def update(self, message: str):
		with open(self._fileName, 'a', encoding='utf-8') as file:
			file.write(message + '\n')

	def setFileName(self, fileName: str):
		self._fileName = fileName

class PrintNull(Subscriber):
	def __init__(self): pass

	def key(self):
		return 'null'

	def update(self, message: str):
		pass

class PrintInErr(Subscriber):
	def __init__(self): pass

	def key(self):
		return 'stderr'

	def update(self, message: str):
		sys.stderr.write(message)
		sys.stderr.write('\n')