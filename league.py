from riotwatcher import RiotWatcher, LoLException

class League:
	def __init__(self):
		self.watcher = RiotWatcher("RGAPI-97a88387-e2b5-4ef9-9c78-178b8e14fa09")

	def get_cur_game(self, summ_name):
		id = self.watcher.get_summoner(name=summ_name)["id"]
		return self.watcher.get_current_game(id)

	def is_in_game(self, summ_name):
		try:
			self.get_cur_game(summ_name)
			return True
		except LoLException:
			return False