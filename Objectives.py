import numpy as np
from IrrigationTechniques import CenterPivotIrrigation, SprinklerIrrigation, DripIrrigation, FurrowIrrigation


def water_usage(county_crops, county_techniques, county_gradients):
    TECHNIQUE_CLASS_MAPPING = [CenterPivotIrrigation, SprinklerIrrigation, DripIrrigation, FurrowIrrigation]
    total_water_usage = 0
    for i in range(0, len(county_crops)):
        current_county_crops = county_crops[i]
        # we use TECHNIQUE_CLASS_MAPPING to store the class signatures and instantiate an object in technique using
        # that mapping so that the appropriate irrigation technique class object can be assigned for the respective
        # county
        technique = TECHNIQUE_CLASS_MAPPING[county_techniques[i]](owning_county=i,
                                                                  gradient_angle=county_gradients[i])

        # using our definition for f_w(l), we sum over all water needed for each crop in each county
        for crop in current_county_crops:
            total_water_usage += crop.water_usage() / technique.efficiency_factor()

    return total_water_usage


def connection_factor(num_connected_technique_components):  # this utility function simply calculates d(l)
    a = 24.5
    b = 1
    return (1 / (1 + np.exp(-1 * (num_connected_technique_components - a) / 5))) + b


def technique_cost(county_crops, county_techniques, county_gradients, num_connected_technique_components):
    TECHNIQUE_CLASS_MAPPING = [CenterPivotIrrigation, SprinklerIrrigation, DripIrrigation, FurrowIrrigation]
    total_implementation_cost = 0
    for i in range(0, len(county_crops)):
        current_county_crops = county_crops[i]
        # we use TECHNIQUE_CLASS_MAPPING to store the class signatures and instantiate an object in technique using
        # that mapping so that the appropriate irrigation technique class object can be assigned for the respective
        # county
        technique = TECHNIQUE_CLASS_MAPPING[county_techniques[i]](owning_county=i,
                                                                  gradient_angle=county_gradients[i])

        # using our definition for f_c(l), we sum over the total cost for irrigation technique technology for each crop
        # in each county
        total_crop_area = 0
        for crop in current_county_crops:
            total_crop_area += crop.acres_planted

        total_implementation_cost += technique.IMPLEMENTATION_COST_PER_ACRE * total_crop_area

    return total_implementation_cost * connection_factor(num_connected_technique_components)



