from fasteners.nuts import Nut
from primitives import *


class UBolt701(ShapeObject):

    t_max: float = 0.0 # Maximum thickness of connection plate
    dimensions = {
        10: {"V": 19, "L": 20, "M": 6, "Do": 14, "Dp": 12, "H": 2},
        15: {"V": 27, "L": 30, "M": 6, "Do": 24, "Dp": 21.3, "H": 2.7},
        20: {"V": 39, "L": 35, "M": 8, "Do": 27, "Dp": 26.9, "H": 0.1},
        25: {"V": 42, "L": 42, "M": 8, "Do": 34, "Dp": 33.7, "H": 0.3},
        32: {"V": 44, "L": 56, "M": 8, "Do": 48, "Dp": 42.4, "H": 5.6},
        40: {"V": 50, "L": 57, "M": 8, "Do": 49, "Dp": 48.3, "H": 0.7},
        50: {"V": 51, "L": 71, "M": 8, "Do": 63, "Dp": 60.3, "H": 2.7},
        65: {"V": 67, "L": 90, "M": 10, "Do": 80, "Dp": 76.1, "H": 3.9},
        80: {"V": 68, "L": 100, "M": 10, "Do": 90, "Dp": 88.9, "H": 1.1},
        100: {"V": 87, "L": 135, "M": 12, "Do": 123, "Dp": 114.3, "H": 8.7},
        125: {"V": 105, "L": 157, "M": 14, "Do": 143, "Dp": 139.7, "H": 3.3},
        150: {"V": 111, "L": 185, "M": 14, "Do": 171, "Dp": 168.3, "H": 2.7},
        200: {"V": 155, "L": 247, "M": 20, "Do": 227, "Dp": 219.1, "H": 7.9},
        250: {"V": 186, "L": 304, "M": 20, "Do": 284, "Dp": 273, "H": 11},
        300: {"V": 210, "L": 354, "M": 20, "Do": 334, "Dp": 323.9, "H": 10.1},
        350: {"V": 220, "L": 385, "M": 20, "Do": 365, "Dp": 355.6, "H": 9.4},
        400: {"V": 310, "L": 439, "M": 24, "Do": 415, "Dp": 406.4, "H": 8.6}
    }

    def __init__(self, s, dn, fix_point, t): # t - thickness of connection plate

        p = self.dimensions.get(dn)

        self.V, self.L, self.M, self.Do, self.Dp, self.H = p["V"], p["L"], p["M"], p["Do"], p["Dp"], p["H"]

        def _leg():
            o1 = ChamferCylinder(s, self.M, self.V, self.M/10).translate(z=-self.V)
            nuts = [
                Nut.iso_4032(s, self.M).translate(z=-self.Dp/2).rotate_z(90),
                Nut.iso_4032(s, self.M).rotate_y(180).translate(z=-self.Dp/2)
            ]

            if fix_point == 1:
                _t_max = self.V - self.Dp/2 - 2 * nuts[0].nut_height #13.5
                self.t_max = min(_t_max, t)

                for nut in nuts:
                    nut.translate(z=-nuts[0].nut_height + self.H/2 - self.t_max)

            else:
                _t_max = self.V - self.Dp/2 - nuts[1].nut_height
                self.t_max = min(_t_max, t)
                nuts[1].translate(z=-self.t_max)

            o1.combine(nuts)
            return o1

        o1 = TorusSector(s, self.L, self.M, 90, 270).rotate_y(90)

        legs = [
            _leg().translate(y = self.L/2),
            _leg().translate(y = -self.L/2)
        ]
        o1.combine(legs)

        if fix_point == 1:
            o1.translate(z=self.H/2)
