from PyResis.physics import residual_resistance_coef, froude_number, reynolds_number, frictional_resistance_coef


class Ship:
    """
    Class of ship object, can be initialize with zero argument.
    """

    def __init__(self, length: float, draught: float, beam: float, speed: float,
                 slenderness_coefficient: float, prismatic_coefficient: float) -> None:
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
        self.surface_area = 1.025 * (1.7 * self.length * self.draught + self.displacement / self.draught)

    @property
    def resistance(self) -> float:
        """
        Return resistance of the vehicle.

        :return: newton the resistance of the ship
        """
        total_resistance_coef = frictional_resistance_coef(self.length, self.speed) + \
                                residual_resistance_coef(self.slenderness_coefficient,
                                                         self.prismatic_coefficient,
                                                         froude_number(self.speed, self.length))
        return 1 / 2 * total_resistance_coef * 1025 * self.surface_area * self.speed ** 2

    def maximum_deck_area(self, water_plane_coef: float = 0.88) -> float:
        """
        Return the maximum deck area of the ship

        :param water_plane_coef: optional water plane coefficient
        :return: Area of the deck
        """
        return self.beam * self.length * water_plane_coef

    @property
    def reynold_number(self) -> float:
        """
        Return Reynold number of the ship

        :return: Reynold number of the ship
        """
        return reynolds_number(self.length, self.speed)

    def propulsion_power(self, propulsion_eff: float = 0.7, sea_margin: float = 0.2) -> float:
        """
        Total propulsion power of the ship.

        :param propulsion_eff: Shaft efficiency of the ship
        :param sea_margin: Sea margin take account of interaction between ship and the sea, e.g. wave
        :return: Watts shaft propulsion power of the ship
        """
        return (1 + sea_margin) * self.resistance * self.speed / propulsion_eff
