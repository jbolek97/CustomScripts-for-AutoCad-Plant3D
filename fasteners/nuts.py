from primitives import ShapeObject
from varmain.divsub.cnut6_001 import * # type: ignore



class Nut(ShapeObject):
    def __init__(self, s, d_thread: float, w: float = 0.0, h: float = 0.0):
        if h <= 0:
            self.nut_height = round(750 * d_thread) / 1000
        else:
            self.nut_height = h

        o1 = ShapeObject(CNUT6_001(s, D = d_thread, W=w, H=h)).rotate_y(-90)

        super().__init__(o1.obj)

    @staticmethod
    def iso_4032(s, d_thread: float):
        dimension ={
            2.0: (1.6, 4),
            2.5: (2.0, 5),
            3.0: (2.4, 5.5),
            4.0: (3.2, 7),
            5.0: (4.7, 8),
            6.0: (5.2, 10),
            8.0: (6.8, 13),
            10.0: (8.4, 16),
            12.0: (10.8, 18),
            14.0: (12.8, 21),
            16.0: (14.8, 24),
            18.0: (15.8, 27),
            20.0: (18.0, 30),
            22.0: (19.4, 34),
            24.0: (21.5, 36),
            27.0: (23.8, 41),
            30.0: (25.6, 46),
            33.0: (28.7, 50),
            36.0: (31.0, 55),
            39.0: (33.4, 60),
            42.0: (34.0, 65),
            45.0: (36.0, 70),
            48.0: (38.0, 75),
            52.0: (42.0, 80),
            56.0: (45.0, 85),
            60.0: (48.0, 90),
            64.0: (51.0, 95)
        }
        try:
            h, w = dimension[d_thread]
        except KeyError:
            raise ValueError(f'Unsupported thread: {d_thread} mm')
        return Nut(s, d_thread, w, h)

