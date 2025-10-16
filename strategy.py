from abc import ABC, abstractmethod
from fabric import InputFabric
import subprocess
from subscriber import PrintOutput
from subscriber import SentToAllOutput
from subscriber import WriteToFile
from subscriber import PrintInErr
from subscriber import PrintNull
from publisher import Publisher


class WorkerStrategy(ABC):
	@abstractmethod
	def run(self, command: str): pass

	@abstractmethod
	def name(self): pass

	def _runCommand(self, command: str):
		try:
			result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
			return result.stdout, result.stderr, result.returncode
		except subprocess.CalledProcessError as e:
			return e.stdout, e.stderr, e.returncode
		except Exception as e:
			return "", str(e), -1


class AllInput(WorkerStrategy):
	def __init__(self):
		inputFabric = InputFabric()
		self._publ = Publisher()
		self._publ.subscribe(inputFabric.getFunction('file'))
		self._publ.subscribe(inputFabric.getFunction('stdout'))
		self._publ.subscribe(inputFabric.getFunction('wall'))
		self._publ.subscribe(inputFabric.getFunction('null'))
		self._publ.subscribe(inputFabric.getFunction('stderr'))

	def run(self, command: str):
		stdout, stderr, returncode = self._runCommand(command)
		self._publ.notify(stdout)
		if stderr:
			self._publ.notify(stderr)

	def name(self):
		return "AllInput"

	@staticmethod
	def create():
		return AllInput()


class ScreenInput(WorkerStrategy):
	def __init__(self):
		inputFabric = InputFabric()
		self._publ = Publisher()
		self._publ.subscribe(inputFabric.getFunction('stdout'))

	def run(self, command: str):
		stdout, stderr, returncode = self._runCommand(command)
		self._publ.notify(stdout)
		if stderr:
			self._publ.notify(stderr)

	def name(self):
		return "ScreenInput"

	@staticmethod
	def create():
		return ScreenInput()


class OnlyErrInput(WorkerStrategy):
	def __init__(self):
		inputFabric = InputFabric()
		self._publ = Publisher()
		self._publ.subscribe(inputFabric.getFunction('stdout'))
		self._publ.subscribe(inputFabric.getFunction('file'))

	def run(self, command: str):
		stdout, stderr, returncode = self._runCommand(command)
		if stderr:
			self._publ.notify(stderr)

	def name(self):
		return "OnlyErrInput"

	@staticmethod
	def create():
		return OnlyErrInput()


class FileInput(WorkerStrategy):
	def __init__(self):
		inputFabric = InputFabric()
		self._publ = Publisher()
		self._publ.subscribe(inputFabric.getFunction('file'))

	def run(self, command: str):
		stdout, stderr, returncode = self._runCommand(command)
		self._publ.notify(stdout)
		if stderr:
			self._publ.notify(stderr)

	def name(self):
		return "FileInput"

	@staticmethod
	def create():
		return FileInput()


class Worker:
	def __init__(self, strategy: WorkerStrategy):
		self._strategy = strategy

	def setStrategy(self, strategy: WorkerStrategy):
		self._strategy = strategy

	def exec(self, command: str):
		self._strategy.run(command)


class TestStrat(WorkerStrategy):
	def __init__(self):
		inputFabric = InputFabric()
		self._publ = Publisher()
		self._publ.subscribe(inputFabric.getFunction('null'))

	def run(self, command: str):
		stdout, stderr, returncode = self._runCommand(command)
		self._publ.notify(stdout)
		if stderr:
			self._publ.notify(stderr)

	def name(self):
		return "TestStrat"

	@staticmethod
	def create():
		return AllInput()