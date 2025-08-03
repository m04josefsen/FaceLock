import rumps
from face_lock import settings

class MenuIcon(rumps.App):
    def __init__(self):
        super(MenuIcon, self).__init__("FaceLock")

        self.selected_delay = 5

        self.menu = [
            rumps.MenuItem("Use Facial Recognition", callback=self.facial_recognition),
            {
                "Seconds": [
                    rumps.MenuItem("5 seconds", callback=self.set_seconds),
                    rumps.MenuItem("10 seconds", callback=self.set_seconds),
                    rumps.MenuItem("30 seconds", callback=self.set_seconds)
                ]
            }
        ]

        self.update_seconds_menu("5 seconds")

    @rumps.clicked("Use Facial Recognition")
    def facial_recognition(self, sender):
        sender.state = not sender.state
        rumps.alert("Test")

    @rumps.clicked("Seconds")
    def set_seconds(self, sender):
        delay = int(sender.title.split()[0])
        settings.selected_delay = delay
        self.update_seconds_menu(sender.title)
        #rumps.notification("Delay Updated", "", f"Delay set to {delay} seconds")
        print(settings.selected_delay)

    def update_seconds_menu(self, selected_title):
        for title in ["5 seconds", "10 seconds", "30 seconds"]:
            self.menu["Seconds"][title].state = (title == selected_title)

if __name__ == "__main__":
    MenuIcon().run()