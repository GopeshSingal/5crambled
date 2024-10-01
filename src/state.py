class State:
    x: float
    y: float
    fill: bool
    dropper: bool

    def __init__(self, cp) -> None:
        self.history = []
        self.rhistory = []
        self.cp = cp

    def reset_history(self):
        self.rhistory.clear()

    def save_state(self, do=True):
        if do:
            current_state = [shape.paint.color for shape in self.cp.shapes]
            self.history.append(current_state)
        else:
            current_state = [shape.paint.color for shape in self.cp.shapes]
            self.rhistory.append(current_state)

    def revert_state(self, e):
        if self.history:
            self.save_state(False)
            old_state = self.history.pop()
            for i, shape in enumerate(self.cp.shapes):
                shape.paint.color = old_state[i]
            self.cp.update()

    def unrevert_state(self, e):
        if self.rhistory:
            self.save_state()
            old_state = self.rhistory.pop()
            for i, shape in enumerate(self.cp.shapes):
                shape.paint.color = old_state[i]
            self.cp.update()