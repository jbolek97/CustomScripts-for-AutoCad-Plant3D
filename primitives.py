from aqa.math import *
from varmain.primitiv import *
from varmain.var_basic import *
from varmain.custom import *


class ShapeObject:
    def __init__(self, obj):
        self.obj = obj

    def translate(self, x= 0.0, y= 0.0, z= 0.0):
        """
        Translates the object by the specified offsets along the x, y, and z axes.
        Parameters:
            x (float, optional): The offset along the x-axis. Default to 0.0.
            y (float, optional): The offset along the y-axis. Default to 0.0.
            z (float, optional): The offset along the z-axis. Default to 0.0.
        Returns:
            self: The instance of the object, allowing for method chaining.
        """
        self.obj.translate((x, y, z))
        return self


class Box(ShapeObject):
    """
    Represents a 3D box shape object.
    Attributes:
        s (object): must be present ever
        length (float): The length of the box. In X direction.
        width (float): The width of the box. In Y direction.
        height (float): The height of the box. In Z direction.
    Methods:
        __init__(s, length, width, height):
        Initializes the Box object. The bottom face of the box is at z = 0.0
    """

    def __init__(self, s, length, width, height):
        o1 = ShapeObject(
            BOX(s, L=width, W=height, H=length)
        ).translate(z = height/2)
        super().__init__(o1.obj)


class Cylinder(ShapeObject):
    def __init__(selfself, ):