class StatusBar:
    def __init__(self, parent, statusbar):
        self.parent = parent
        self.statusbar = statusbar

    def write(self, msg):
        if msg != '\n':
            self.statusbar.showMessage(msg)
