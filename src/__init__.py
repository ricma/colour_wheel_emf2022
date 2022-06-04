"""
An app to show current acceleration as colour using the LED of the badge
"""
from tidal import color565, RED
from app import TextApp

class ColourWheelApp(TextApp):
    TITLE = "Colour Wheel"
    # Solzarized dark-like colours.
    BG = color565(0x00, 0x2b, 0x36) # The background colour
    FG = color565(0xfd, 0xf6, 0xe3) # A non-standard colour to use as the default text colour

    def get_acceleration(self):
        """
        return the magnitude of the acceleration
        """
        return 9.81

    def on_activate(self):
        super().on_activate() # This will clear the screen by calling TextWindow.redraw()
        self.window.println("Hallo Welt!")

        # register a callback to read out the accelerometer
        def update_LED():
            print(f"Current acceleration: {self.get_acceleration()}")

        self.timer = self.periodic(100, update_LED)

    def on_deactivate(self):
        """
        clean up
        """
        print("Cancelling timers")
        self.timer.cancel()
        super().on_deactivate()

main = ColourWheelApp
