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

    def __init__(self, *args, **kwargs):
        """
        Set min and max values for the color bar
        """
        self._min_val = 0.0
        self._max_val = 20.0   # in units of g = 9.81 ms⁻²

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

    def get_color(self, value):
        """
        get a color based on a given value
        """
        scaled = (value - self._min_val) / (self._max_val - self._min_val)
        # TODO: Add color here
        return color565(0xfd, 0x00, 0x00)

    def set_display_color(self, value):
        """
        Set the display color

        Parameter
        ---------
        value : double
            the current acceleration in units of g
        """
        c = self.get_color(value)
        # TODO: Set display color

    def on_activate(self):
        super().on_activate() # This will clear the screen by calling TextWindow.redraw()

        # register a callback to read out the accelerometer
        def update_LED():
            self.window.redraw()
            a = self.get_acceleration()
            self.set_display_color(a)
            self.window.println(f"{a}")

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
