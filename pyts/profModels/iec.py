"""
This module contains the power-law mean-velocity profiles:
 main   - The IEC mean wind speed profile.

"""
from .mBase import profObj
from .log import nwtc as logmain
from .power import nwtc as powmain

# !!!VERSION_INCONSISTENCY
# This model needs to account for the EWM50 and EWM1 turbulence models.


class main(logmain, powmain):

    """
    The iec wind profile model.  This profile is a power-law across
    the rotor disk and logarithmic elsewhere.

    Parameters
    ----------
    grid :      :class:`tsGrid <pyts.base.tsGrid>`
                The TurbSim grid object for this simulation.

    URef :      float
                Reference velocity for the wind profile [m/s].

    RefHt :     float
                Reference height of the reference velocity [m].

    PLexp :     float,optional (0.2)
                The power-law exponent to be utilized for this
                simulation [non-dimensional], default=0.2 (per
                IEC specification).

    Z0 :        float
                Surface roughness length [m].

    Ri :        float
                The Richardon number [non-dimensional].

    turbmodel : str
                the name of the turbulence model in this simulationm, optional.

    See Also
    --------
    .power.nwtc : The iec model is this law over the rotor disk
    .log.nwtc   : The iec model is this law outside the rotor disk

    """

    def __init__(self, URef, RefHt, Z0, Ri, PLexp=0.2, turbmodel=None):
        self.Uref = URef
        self.Zref = RefHt
        self.PLexp = PLexp
        self.Z0 = Z0
        self.Ri = Ri
        self.TurbModel = turbmodel

    def __call__(self, tsrun):
        """
        Create and calculate the mean-profile object for a `tsrun`
        instance.

        Parameters
        ----------
        tsrun :         :class:`tsrun <pyts.main.tsrun>`
                        A TurbSim run object.

        Returns
        -------
        out :           :class:`profObj <.mBase.profObj>`
                        A iec wind-speed profile for the grid in `tsrun`.

        """
        out = profObj(tsrun)
        grid = tsrun.grid  # A temporary, internal shortcut.
        out[0] = logmain.model(self, grid.z)[:, None]
        zinds = ((-grid.rotor_diam / 2 <= grid.z - grid.zhub)
                 & (grid.z - grid.zhub <= grid.rotor_diam / 2))
        yinds = ((-grid.rotor_diam / 2 <= grid.y)
                 & (grid.y <= grid.rotor_diam / 2))
        out[0][zinds][:, yinds] = powmain.model(self, grid.z[zinds])
        return out
