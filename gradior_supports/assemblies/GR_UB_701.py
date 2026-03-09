from gradior_supports.components.u_bolt_701 import UBolt701
from primitives import *

from aqa.math import *
from varmain.primitiv import *
from varmain.var_basic import *
from varmain.custom import *

@activate(Group="Support", Ports="1", TooltipShort="U-Bolt 701",
          TooltipLong="Gradiator u-bolt typ 701", LengthUnit="mm")
@group("MainDimensions")
@param(DN=LENGTH, TooltipLong="Nominal diameter of the U-bolt")
@param(FIX_POINT=LENGTH, TooltipLong="0 - guide point, 1 - fix point")
@param(T=LENGTH, TooltipLong="Maximum thickness of the connection plate")

# --- PART DEFINITION --

def GR_UB_701(s, dn=50, fix_point=0, t=5.0, ID="GR_UB_701", **kw):
    if fix_point not in [0, 1]:
        fix_point = 0

    o1 = UBolt701(s, dn, fix_point, t)
    insertion_point = Point3D(0, 0, 0)
    direction = Point3D(1, 0, 0) # X-axis - the axis of the pipe
    bottom = Point3D(0, 0, -o1.Dp / 2)

    Point3D.set_port(s, insertion_point, direction)
    Point3D.set_dimension(s, "Spirit", insertion_point, bottom) # just to have snap point

    second_nut_pos = Point3D(0, 0, -o1.Dp / 2 - o1.t_max)
    t = o1.t_max
    Point3D.set_dimension(s, "T", bottom, second_nut_pos)

    return o1
