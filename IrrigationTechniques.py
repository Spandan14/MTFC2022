import numpy as np


# the following classes contain data for each irrigation technique and also functions for calculating the efficiency
# factor of each technique
class CenterPivotIrrigation:
    def __init__(self, owning_county, gradient_angle):
        self.owning_county = owning_county
        self.gradient_angle = gradient_angle
        self.IMPLEMENTATION_COST_PER_ACRE = 17

    def efficiency_factor(self):
        a = 0.6479
        b = 4
        return a * np.cos(np.deg2rad(b * self.gradient_angle))


class SprinklerIrrigation:
    def __init__(self, owning_county, gradient_angle):
        self.owning_county = owning_county
        self.gradient_angle = gradient_angle
        self.IMPLEMENTATION_COST_PER_ACRE = 23.31

    def efficiency_factor(self):
        a = 0.75
        return a * np.cos(np.deg2rad(self.gradient_angle))


class DripIrrigation:
    def __init__(self, owning_county, gradient_angle):
        self.owning_county = owning_county
        self.gradient_angle = gradient_angle
        self.IMPLEMENTATION_COST_PER_ACRE = 38.44519536

    def efficiency_factor(self):
        a = 0.9
        return a


class FurrowIrrigation:
    def __init__(self, owning_county, gradient_angle):
        self.owning_county = owning_county
        self.gradient_angle = gradient_angle
        self.IMPLEMENTATION_COST_PER_ACRE = 8

    def efficiency_factor(self):
        a = 2.92541
        b = 2.26544
        c = -0.557759
        return ((a * ((self.gradient_angle - c) ** 3)) / (np.exp(b * (self.gradient_angle - c)) - 1)) + 0.25