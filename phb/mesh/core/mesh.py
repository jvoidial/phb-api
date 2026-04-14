class Mesh:
    def __init__(self, board, arbitrator):
        self.board = board
        self.arbitrator = arbitrator
        self.agents = []

    def register(self, agent):
        self.agents.append(agent)

    def process(self, event):
        outputs = []

        for agent in self.agents:
            try:
                outputs.append(agent.run(event, self.board))
            except Exception as e:
                print("⚠️ agent error:", e)

        return self.arbitrator.decide(outputs, fallback=event.get("msg"))
