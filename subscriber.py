import subprocess
import sys
from abc import ABC, abstractmethod
import sqlite3
from datetime import datetime

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

class SendToSQLite:
	def __init__(self, db_path='logs.db'):
		self.db_path = db_path
		self._create_table()

	def key(self):
		return 'sindb'

	def update(self, message: str):
		_log_message(self, message)
    
	def _create_table(self):
		"""Создание таблицы logs если она не существует"""
		create_table_query = """
		CREATE TABLE IF NOT EXISTS logs (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			message TEXT NOT NULL,
			timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
		)
		"""
		self._execute_query(create_table_query)
    
	def _execute_query(self, query, params=None):
		try:
			with sqlite3.connect(self.db_path) as conn:
				cursor = conn.cursor()
				if params:
					cursor.execute(query, params)
				else:
					cursor.execute(query)
				conn.commit()
				return cursor
		except sqlite3.Error as e:
			print(f"Ошибка базы данных: {e}")
			return None
    
	def _log_message(self, message):
		insert_query = "INSERT INTO logs (message, timestamp) VALUES (?, ?)"
		timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
		result = self._execute_query(insert_query, (message, timestamp))
		if result:
			print(f"Сообщение успешно записано в лог: '{message}'")
		else:
			print("Ошибка при записи сообщения в лог")