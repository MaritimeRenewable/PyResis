import math

import numpy as np
from scipy import interpolate

from PyResis.constants import CR, CRNEAREST


def residual_resistance_coef(slenderness: float, prismatic_coef: float, froude_number: float):
    """
    Residual resistance coefficient estimation from slenderness function, prismatic coefficient and Froude number.

    :param slenderness: Slenderness coefficient dimensionless :math:`L/(∇^{1/3})` where L is length of ship, ∇ is displacement
    :param prismatic_coef: Prismatic coefficient dimensionless :math:`∇/(L\cdot A_m)` where L is length of ship, ∇ is displacement Am is midsection area of the ship
    :param froude_number: Froude number of the ship dimensionless
    :return: Residual resistance of the ship
    """
    crvalue = CR(slenderness, prismatic_coef, froude_number)
    if math.isnan(Cr):
        crvalue = CRNEAREST(slenderness, prismatic_coef, froude_number)

    # if Froude number is out of interpolation range, nearest extrapolation is used
    return crvalue


def froude_number(speed: float, length: float):
    """
    Froude number utility function that return Froude number for vehicle at specific length and speed.

    :param speed: m/s speed of the vehicle
    :param length: metres length of the vehicle
    :return: Froude number of the vehicle (dimensionless)
    """
    g = 9.80665  # conventional standard value m/s^2
    return speed / np.sqrt(g * length)


def reynolds_number(length: float, speed: float, temperature: float = 25):
    """
    Reynold number utility function that return Reynold number for vehicle at specific length and speed.
    Optionally, it can also take account of temperature effect of sea water.

        Kinematic viscosity from: http://web.mit.edu/seawater/2017_MIT_Seawater_Property_Tables_r2.pdf

    :param length: metres length of the vehicle
    :param speed: m/s speed of the vehicle
    :param temperature: degree C
    :return: Reynolds number of the vehicle (dimensionless)
    """
    kinematic_viscosity = interpolate.interp1d([0, 10, 20, 25, 30, 40],
                                               np.array([18.54, 13.60, 10.50, 9.37, 8.42, 6.95]) / 10 ** 7)
    # Data from http://web.mit.edu/seawater/2017_MIT_Seawater_Property_Tables_r2.pdf
    return length * speed / kinematic_viscosity(temperature)


def frictional_resistance_coef(length: float, speed: float, **kwargs):
    """
    Flat plate frictional resistance of the ship according to ITTC formula.
    ref: https://ittc.info/media/2021/75-02-02-02.pdf

    :param length: metres length of the vehicle
    :param speed: m/s speed of the vehicle
    :param kwargs: optional could take in temperature to take account change of water property
    :return: Frictional resistance coefficient of the vehicle
    """
    return 0.075 / (np.log10(reynolds_number(length, speed, **kwargs)) - 2) ** 2