from primitives import *
from fasteners.nuts import *
from gradior_supports.components.u_bolt_701 import UBolt701

from aqa.math import *
from varmain.primitiv import *
from varmain.var_basic import *
from varmain.custom import *

@activate(Group="Support", Ports="1", TooltipShort="Spring hanger SH1", TooltipLong="Spring hanger SH1", LengthUnit="mm")
@group("MainDimensions")

@param(D = LENGTH, Tooltiplong="Spirit param")

# (testacpscript "first_script")

def first_script(s, D=80, ID = "first_script", **kw):
    o1 = UBolt701(s,50, 0, 5)