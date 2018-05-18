import os
import math
import numpy as np
from scipy import interpolate

fn = os.path.join(os.path.dirname(__file__), 'cr.txt')
cr_list = np.loadtxt(fn)
cr_points = cr_list.T[:3].T
cr_values = cr_list.T[3].T / 1000
cr = interpolate.LinearNDInterpolator(cr_points, cr_values)
cr_nearest = interpolate.NearestNDInterpolator(cr_points, cr_values)

def frictional_resistance_coef(length, speed, **kwargs):
    """
    Flat plate frictional resistance of the ship according to ITTC formula.
    ref: https://ittc.info/media/2021/75-02-02-02.pdf

    :param length: metres length of the vehicle
    :param speed: m/s speed of the vehicle
    :param kwargs: optional could take in temperature to take account change of water property
    :return: Frictional resistance coefficient of the vehicle
    """
    Cf = 0.075 / (np.log10(reynolds_number(length, speed, **kwargs)) - 2) ** 2
    return Cf


def reynolds_number(length, speed, temperature=25):
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
    Re = length * speed / kinematic_viscosity(temperature)
    return Re


def froude_number(speed, length):
    """
    Froude number utility function that return Froude number for vehicle at specific length and speed.

    :param speed: m/s speed of the vehicle
    :param length: metres length of the vehicle
    :return: Froude number of the vehicle (dimensionless)
    """
    g = 9.80665  # conventional standard value m/s^2
    Fr = speed / np.sqrt(g * length)
    return Fr



def residual_resistance_coef(slenderness, prismatic_coef, froude_number):
    """
    Residual resistance coefficient estimation from slenderness function, prismatic coefficient and Froude number.

    :param slenderness: Slenderness coefficient dimensionless :math:`L/(∇^{1/3})` where L is length of ship, ∇ is displacement
    :param prismatic_coef: Prismatic coefficient dimensionless :math:`∇/(L\cdot A_m)` where L is length of ship, ∇ is displacement Am is midsection area of the ship
    :param froude_number: Froude number of the ship dimensionless 
    :return: Residual resistance of the ship
    """
    Cr = cr(slenderness, prismatic_coef, froude_number)
    if math.isnan(Cr):
        Cr = cr_nearest(slenderness, prismatic_coef, froude_number)

    # if Froude number is out of interpolation range, nearest extrapolation is used
    return Cr


class Ship():
    """
    Class of ship object, can be initialize with zero argument.
    """
    def __init__(self):
        pass

    def dimension(self, length, draught, beam, speed,
                 slenderness_coefficient, prismatic_coefficient):
        """
        Assign values for the main dimension of a ship.

        :param length: metres length of the vehicle
        :param draught: metres draught of the vehicle
        :param beam: metres beam of the vehicle
        :param speed: m/s speed of the vehicle
        :param slenderness_coefficient: Slenderness coefficient dimensionless :math:`L/(∇^{1/3})` where L is length of ship,
            ∇ is displacement
        :param prismatic_coefficient: Prismatic coefficient dimensionless :math:`∇/(L\cdot A_m)` where L is length of ship,
            ∇ is displacement Am is midsection area of the ship
        """
        self.length = length
        self.draught = draught
        self.beam = beam
        self.speed = speed
        self.slenderness_coefficient = slenderness_coefficient
        self.prismatic_coefficient = prismatic_coefficient
        self.displacement = (self.length / self.slenderness_coefficient) ** 3
        self.surface_area = 1.025 * (1.7 * self.length * self.draught +
                                     self.displacement / self.draught)

    def resistance(self):
        """
        Return resistance of the vehicle.

        :return: newton the resistance of the ship
        """
        self.total_resistance_coef = frictional_resistance_coef(self.length, self.speed) + \
                                residual_resistance_coef(self.slenderness_coefficient,
                                                         self.prismatic_coefficient,
                                                         froude_number(self.speed, self.length))
        RT = 1 / 2 * self.total_resistance_coef * 1025 * self.surface_area * self.speed ** 2
        return RT

    def maximum_deck_area(self, water_plane_coef=0.88):
        """
        Return the maximum deck area of the ship

        :param water_plane_coef: optional water plane coefficient
        :return: Area of the deck
        """
        AD = self.beam * self.length * water_plane_coef
        return AD

    def get_reynold_number(self):
        """
        Return Reynold number of the ship

        :return: Reynold number of the ship
        """
        return reynolds_number(self.length, self.speed)

    def prop_power(self, propulsion_eff=0.7, sea_margin=0.2):
        """
        Total propulsion power of the ship.

        :param propulsion_eff: Shaft efficiency of the ship
        :param sea_margin: Sea margin take account of interaction between ship and the sea, e.g. wave
        :return: Watts shaft propulsion power of the ship
        """
        PP = (1 + sea_margin) * self.resistance() * self.speed/propulsion_eff
        return PP

if __name__ == '__main__':
    s1 = Ship()
    s1.dimension(5.72, 0.248, 0.76, 0.2, 6.99, 0.613)
    print(s1.prop_power())