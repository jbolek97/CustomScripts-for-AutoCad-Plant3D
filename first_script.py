from primitives import *

from aqa.math import *
from varmain.primitiv import *
from varmain.var_basic import *
from varmain.custom import *

@activate(Group="Support", Ports="1", TooltipShort="Spring hanger SH1", TooltipLong="Spring hanger SH1", LengthUnit="mm")
@group("MainDimensions")

@param(D = LENGTH, Tooltiplong="Spirit param")

# (testacpscript "first_script")

def first_script(s, ID = "first_script", **kw):
    o1 = ChamferCylinder(s, diameter=50, height=80, chamfer=5, chamfer_angle=45, double_chamfer=True)