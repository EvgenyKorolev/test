from subscriber import Subscriber


class Publisher:
	def __init__(self):
		self._subscribers = []

	def subscribe(self, subscriber: Subscriber):
		self._subscribers.append(subscriber)

	def unsubscribe(self, subscriber: Subscriber):
		self._subscribers.remove(subscriber)

	def notify(self, message: str):
		for subscriber in self._subscribers:
			subscriber.update(message)