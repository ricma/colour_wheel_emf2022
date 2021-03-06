"""
An app to show current acceleration as colour using the LED of the badge
"""
from tidal import color565
from app import TextApp
import accelerometer
from math import sqrt


class ColourWheelApp(TextApp):
    TITLE = "Colour Wheel"
    # Solzarized dark-like colours.
    BG = color565(0x00, 0x2b, 0x36) # The background colour
    FG = color565(0xfd, 0xf6, 0xe3) # A non-standard colour to use as the default text colour

    def get_acceleration(self):
        """
        return the magnitude of the acceleration

        See Also
        --------
        [[file:../../TiDAL-Firmware/modules/post.py::x,y,z = accelerometer.get_xyz()]]:
            Provides acceleration in units of g
        """
        a_x, a_y, a_z = accelerometer.get_xyz()
        return sqrt(a_x * a_x + a_y * a_y + a_z * a_z)

    def on_activate(self):
        super().on_activate() # This will clear the screen by calling TextWindow.redraw()

        # register a callback to read out the accelerometer
        def update_LED():
            self.window.redraw()
            self.window.println(f"{self.get_acceleration()}")

        self.timer = self.periodic(1_000, update_LED)
        self.window.println("Printing")
        self.window.println("acceleration ...")

    def on_deactivate(self):
        """
        clean up
        """
        print("Cancelling timers")
        self.timer.cancel()
        super().on_deactivate()

main = ColourWheelApp
