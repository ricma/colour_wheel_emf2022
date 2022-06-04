"""
An app to show current acceleration as colour using the LED of the badge
"""
from tidal import color565, hsv_to_rgb, display
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
        super(ColourWheelApp, self).__init__(*args, **kwargs)
        self._min_val = 0.0
        self._max_val = 5.0   # in units of g = 9.81 ms⁻²
        self._min_acc_observed = 640.0
        self._max_acc_observed = 0.0
        self.update_rate_Hz = 150.0  # refresh rate

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
        get a color based on a given value linear in the interval between
          (self._min_val, self._max_val)
        """
        scaled = (value - self._min_val) / (self._max_val - self._min_val)
        color_hsv = (min(scaled, 1), 1, 1)
        color_rgb = hsv_to_rgb(*color_hsv)
        color = color565(*color_rgb)

        return color

    def set_display_color(self, value):
        """
        Set the display color

        Parameter
        ---------
        value : double
            the current acceleration in units of g
        """
        c = self.get_color(value)
        display.fill(c)

    def on_activate(self):
        super().on_activate() # This will clear the screen by calling TextWindow.redraw()

        # register a callback to read out the accelerometer
        def update_screen():
            self.window.redraw()
            a = self.get_acceleration()
            self._min_acc_observed = min(
                self._min_acc_observed, a)
            self._max_acc_observed = max(
                self._max_acc_observed, a)
            self.set_display_color(a)
            self.window.println(f"{self._min_acc_observed:.2f} <=")
            self.window.println(f"{a:.2f} <=")
            self.window.println(f"{self._max_acc_observed:.2f}")

        self.timer = self.periodic(
            1_000 / self.update_rate_Hz, update_screen)
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
