from typing import Optional, Any
import math

from aqa.math import *
from varmain.primitiv import *
from varmain.var_basic import *
from varmain.custom import *


class ShapeObject:
    def __init__(self, obj):
        self.obj = obj

    def translate(self, x=0.0, y=0.0, z=0.0):
        """
        Translates the object by the specified offsets along the x, y, and z axes.
        Args:
            x (float, optional): The offset along the x-axis. Default to 0.0.
            y (float, optional): The offset along the y-axis. Default to 0.0.
            z (float, optional): The offset along the z-axis. Default to 0.0.
        Returns:
            ShapeObject: The instance of the object, allowing for method chaining.
        """
        self.obj.translate((x, y, z))
        return self

    def combine(self, others):
        """
        Unites this shape with one or more other shape objects.

        This method performs a boolean union operation. The other objects
        are merged into this instance and then erased from the scene to
        avoid duplicates.

        Args:
            others (ShapeObject or list[ShapeObject]): A single ShapeObject
                or a list of ShapeObjects to be united with this one.

        Returns:
            ShapeObject: The current instance with the combined geometry,
                allowing for method chaining.
        """
        if not isinstance(others, list):
            others = [others]

        for other in others:
            self.obj.uniteWith(other.obj)
            other.erase()
        return self

    def erase(self):
        """
        Removes the underlying geometric object from the scene/session.

        This is typically used for temporary objects or during boolean
        operations to clean up the workspace.
        """
        self.obj.erase()

class Box(ShapeObject):
    """
    Represents a 3D box shape object.

    This class initializes a box with specified dimensions. The box is
    automatically translated so that its bottom face lies on the XY plane (z=0).

    Args:
        s (Any): Context object, must be present.
        length (float): The length of the box in the X direction.
        width (float): The width of the box in the Y direction.
        height (float): The height of the box in the Z direction.

    Attributes:
        obj: The underlying geometric representation inherited from ShapeObject.
    """

    def __init__(self, s: Any, length: float, width: float, height: float):
        o1 = ShapeObject(
            BOX(s, L=length, W=width, H=height)
        ).translate(z=height / 2)

        super().__init__(o1.obj)


class Cylinder(ShapeObject):
    """
    Represents a cylindrical or elliptical shape object.

    This class initializes a cylinder with a specified diameter and height.
    If an ellipse diameter is provided, it creates an elliptical cylinder.
    It also supports hollow structures via the wall thickness parameter.

    Args:
        s (Any): must be present ever.
        diameter (float): The primary diameter (width) of the cylinder.
        height (float): The vertical height of the cylinder.
        wall_thickness (float, optional): The thickness of the cylinder walls.
            If greater than 0, creates a hollow object. Defaults to 0.0.
        ellipse_diameter (Optional[float], optional): The secondary diameter
            (depth) for creating elliptical cylinders. Defaults to None.

    Attributes:
        obj: The underlying geometric representation inherited from ShapeObject.
    """

    def __init__(self,
                 s: Any,
                 diameter: float,
                 height: float,
                 wall_thickness: float = 0.0,
                 ellipse_diameter: Optional[float] = None
    ):
        r1 = diameter / 2
        offset = r1 - wall_thickness

        if ellipse_diameter is None:
            o1 = ShapeObject(
                CYLINDER(s, R=r1, H=height, O=offset)
            )
        else:
            r2 = ellipse_diameter / 2
            o1 = ShapeObject(
                CYLINDER(s, R1=r1, R2=r2, H=height, O=offset)
            )

        super().__init__(o1.obj)


class Cone(ShapeObject):
    """
    Represents a conical or frustum shape object.

    This class initializes a cone with a specified bottom diameter and height.
    It can represent a full cone (if top_diameter is 0) or a truncated cone
    (frustum). It also supports eccentric (offset) cones via the eccentricity
    parameter. The base center is located at (0, 0, 0).

    Args:
        s (Any): Context object, must be present ever.
        bottom_diameter (float): The diameter of the base of the cone.
        height (float): The vertical height of the cone.
        top_diameter (float, optional): The diameter of the top of the cone.
            Set to 0.0 for a sharp-pointed cone. Defaults to 0.0.
        eccentricity (float, optional): The offset distance between the centers
            of the top and bottom faces. Defaults to 0.0.

    Attributes:
        obj: The underlying geometric representation inherited from ShapeObject.
    """

    def __init__(self,
                 s: Any,
                 bottom_diameter: float,
                 height: float,
                 top_diameter: float = 0.0,
                 eccentricity: float = 0.0
    ):
        r1 = bottom_diameter / 2
        r2 = top_diameter / 2

        o1 = ShapeObject(
            CONE(s, R1=r1, R2=r2, H=height, E=eccentricity)
        )

        super().__init__(o1.obj)


class ChamferCylinder(ShapeObject):
    """
    Represents a cylinder with chamfered (beveled) edges.

    This class creates a cylindrical body with conical transitions at one or both ends.
    It includes built-in safety logic to automatically adjust chamfer dimensions if
    they exceed the physical limits of the object, preventing geometry errors in Plant 3D.

    Args:
        s (Any): Context object (typically the script session).
        diameter (float): The outer diameter of the cylinder body.
        height (float): The total overall height of the finished object.
        chamfer (float, optional): The horizontal width of the chamfer cut.
            Defaults to 0.0.
        chamfer_angle (float, optional): The angle of the chamfer measured from
            the vertical Z-axis (in degrees). Defaults to 45.0.
        double_chamfer (bool, optional): If True, applies chamfers to both top
            and bottom ends. If False, only the bottom is chamfered.
            Defaults to False.

    Attributes:
        obj: The underlying geometric representation inherited from ShapeObject.
    """
    def __init__(self,
                 s: Any,
                 diameter: float,
                 height: float,
                 chamfer: float = 0.0,
                 chamfer_angle: float = 45.0,
                 double_chamfer: bool = False,
    ):
        max_allowed_chamfer = (diameter / 2) * 0.99
        if abs(chamfer) >= diameter / 2:
            chamfer = max_allowed_chamfer

        height_chamfer = chamfer / math.tan(math.radians(chamfer_angle))

        total_needed_h = 2 * height_chamfer if double_chamfer else height_chamfer
        if total_needed_h >= height:
            height_chamfer = (height * 0.4) / (2 if double_chamfer else 1)
            chamfer = height_chamfer * math.tan(math.radians(chamfer_angle))

        small_diameter = diameter - 2 * chamfer

        if double_chamfer:
            o1 = Cone(s, bottom_diameter=small_diameter, height=height_chamfer, top_diameter=diameter)
            o2 = Cylinder(s, diameter=diameter, height=height - 2 * height_chamfer).translate(z=height_chamfer)
            o3 = Cone(s, bottom_diameter=diameter, height=height_chamfer, top_diameter=small_diameter).translate(z=height - height_chamfer)
            o1.combine([o2, o3])
        else:
            o1 = Cone(s, bottom_diameter=small_diameter, height=height_chamfer, top_diameter=diameter)
            o2 = Cylinder(s, diameter=diameter, height=height - height_chamfer).translate(z=height_chamfer)
            o1.combine(o2)

        super().__init__(o1.obj)


class Torus(ShapeObject):
    """
    Represents a torus (doughnut-shaped) object.

    This class initializes a torus based on specified outer and inner diameters.
    The object is centered at the origin (0, 0, 0) with its central axis
    along the Z-axis.

    Args:
        s (Any): Context object, must be present ever.
        outer_diameter (float): The total width of the torus at its widest point.
        inner_diameter (float): The diameter of the hole in the center.

    Attributes:
        obj: The underlying geometric representation inherited from ShapeObject.
    """

    def __init__(self, s: Any, outer_diameter: float, inner_diameter: float):
        r1 = outer_diameter / 2
        r2 = inner_diameter / 2

        o1 = ShapeObject(
            TORUS(s, R1=r1, R2=r2)
        )

        super().__init__(o1.obj)
