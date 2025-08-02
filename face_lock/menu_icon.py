import rumps

class MenuIcon(rumps.App):
    def __init__(self):
        super(MenuIcon, self).__init__("FaceLock")
        self.menu = ["Use Facial Recognition"]

    @rumps.clicked("Use Facial Recognition")
    def onoff(self, sender):
        sender.state = not sender.state
        rumps.alert("Test")

if __name__ == "__main__":
    MenuIcon().run()