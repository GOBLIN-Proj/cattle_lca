# IMPORTS
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


COHORTS = [
    "dairy_cows",
    "suckler_cows",
    "bulls",
    "DxD_calves_m",
    "DxD_calves_f",
    "DxB_calves_m",
    "DxB_calves_f",
    "BxB_calves_m",
    "BxB_calves_f",
    "DxD_heifers_less_2_yr",
    "DxD_steers_less_2_yr",
    "DxB_heifers_less_2_yr",
    "DxB_steers_less_2_yr",
    "BxB_heifers_less_2_yr",
    "BxB_steers_less_2_yr",
    "DxD_heifers_more_2_yr",
    "DxD_steers_more_2_yr",
    "DxB_heifers_more_2_yr",
    "DxB_steers_more_2_yr",
    "BxB_heifers_more_2_yr",
    "BxB_steers_more_2_yr",
]
###################################################################################################################
def ratio_of_net_energy_maintenance(animal, grass):
    """
        REM = Ratio of net energy maintenance to the amount of (DE) total energy
        consumed, minus poop

        DE = the digestible energy expressed as a percentage of gross energy
        (digestible dry matter )

    Parameters
    ----------

    animal: accepts the animal cohort type from the animal input data. For example,
    the input to calculate the REM for dairy cows will be:
        for i in [data].values():
            print(lca.ratio_of_net_energy_maintenance(i.animals.dairy_cows,grass))

    grass: accepts the grass database as a parameter, and utilises the digestible energy
    from the forage type that has been input into the animal and farm data.

    Returns
    -------
    The ratio of energy for maintenance as a float.

    See Also
    -------
    EQUATION 10.14 RATIO OF NET ENERGY AVAILABLE IN A DIET FOR MAINTENANCE TO DIGESTIBLE ENERGY
    2019 Refinement to the 2006 IPCC Guidelines for National Greenhouse Gas Inventories

    """

    DE = grass.get_forage_dry_matter_digestibility(animal.forage)

    return (
        1.123
        - (4.092 * (10**-3) * DE)
        + (1.126 * (10**-5) * (DE**2))
        - (25.4 / DE)
    )


def ratio_of_net_energy_growth(animal, grass):
    """
    REG = Ration of net energy for growth to total energy consumed, minus poop

        DE = the digestible energy expressed as a percentage of gross energy
        (digestible dry matter )

    Parameters
    ----------

    animal: accepts the animal cohort type from the animal input data. For example,
    the input to calculate the REM for dairy cows will be:
        for i in [data].values():
            print(lca.ratio_of_net_energy_maintenance(i.animals.dairy_cows,grass))

    grass: accepts the grass database as a parameter, and utilises the digestible energy
    from the forage type that has been input into the animal and farm data.

    Returns
    -------
    The ratio of energy for growth as a float.
    See Also
    -------
    EQUATION 10.15 RATIO OF NET ENERGY AVAILABLE FOR GROWTH IN A DIET TO DIGESTIBLE ENERGY CONSUMED
    2019 Refinement to the 2006 IPCC Guidelines for National Greenhouse Gas Inventories

    """

    DE = grass.get_forage_dry_matter_digestibility(animal.forage)

    return (
        1.164
        - (5.160 * (10**-3) * DE)
        + (1.308 * (10**-5) * (DE**2))
        - (37.4 / DE)
    )


#############################################################################################
# Energy & Enteric Fermentation
#############################################################################################


def net_energy_for_maintenance(animal, emissions_factors):
    """
    When this function is called, it returns the coefficient, which is the emisions factor for net energy
    for lactation, multiplied by the square root of animal weight to the power of 0.75.

    coefficient X (animal_weight^0.75)

    It utilises equation 10.3 from the IPCC 2006 guidelines (NEm)
    """

    coefficient = {
        "dairy_cows": emissions_factors.get_ef_net_energy_for_maintenance_lactating_cow(),
        "suckler_cows": emissions_factors.get_ef_net_energy_for_maintenance_lactating_cow(),
        "bulls": emissions_factors.get_ef_net_energy_for_maintenance_bulls(),
        "DxD_calves_m": emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow(),
        "DxD_calves_f": emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow(),
        "DxB_calves_m": emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow(),
        "DxB_calves_f": emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow(),
        "BxB_calves_m": emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow(),
        "BxB_calves_f": emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow(),
        "DxD_heifers_less_2_yr": emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow(),
        "DxD_steers_less_2_yr": emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow(),
        "DxB_heifers_less_2_yr": emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow(),
        "DxB_steers_less_2_yr": emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow(),
        "BxB_heifers_less_2_yr": emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow(),
        "BxB_steers_less_2_yr": emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow(),
        "DxD_heifers_more_2_yr": emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow(),
        "DxD_steers_more_2_yr": emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow(),
        "DxB_heifers_more_2_yr": emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow(),
        "DxB_steers_more_2_yr": emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow(),
        "BxB_heifers_more_2_yr": emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow(),
        "BxB_steers_more_2_yr": emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow(),
    }

    cfi = coefficient.get(animal.cohort)

    return cfi * (animal.weight**0.75)


def net_energy_for_activity(animal, emissions_factors):
    """
    When this function is called it utilises the net_energy_for_maintenance eq multiplied by
    the coefficient for feed situation

    The equation is based on equation 10.4 from the IPCC 2006 guidelines.
    """

    grazing_type = {
        "pasture": emissions_factors.get_ef_feeding_situation_pasture(),
        "large area": emissions_factors.get_ef_feeding_situation_large_area(),
        "stall": emissions_factors.get_ef_feeding_situation_stall(),
    }

    return grazing_type.get(animal.grazing) * net_energy_for_maintenance(
        animal, emissions_factors
    )


def net_energy_for_weight_gain(animal, animal_features, emissions_factors):

    """
    This function is the net energy for growth, it is parameterised to the animals weight gain per day.
    It utilises equation 10.6 from the IPCC 2006 guidelines (NEg)

    """

    weight_gain = {
        "dairy_cows": animal_features.get_dairy_cows_weight_gain(),
        "suckler_cows": animal_features.get_suckler_cows_weight_gain(),
        "bulls": animal_features.get_bulls_weight_gain(),
        "DxD_calves_m": animal_features.get_DxD_calves_m_weight_gain(),
        "DxD_calves_f": animal_features.get_DxD_calves_f_weight_gain(),
        "DxB_calves_m": animal_features.get_DxB_calves_m_weight_gain(),
        "DxB_calves_f": animal_features.get_DxB_calves_f_weight_gain(),
        "BxB_calves_m": animal_features.get_BxB_calves_m_weight_gain(),
        "BxB_calves_f": animal_features.get_BxB_calves_f_weight_gain(),
        "DxD_heifers_less_2_yr": animal_features.get_DxD_heifers_less_2_yr_weight_gain(),
        "DxD_steers_less_2_yr": animal_features.get_DxD_steers_less_2_yr_weight_gain(),
        "DxB_heifers_less_2_yr": animal_features.get_DxB_heifers_less_2_yr_weight_gain(),
        "DxB_steers_less_2_yr": animal_features.get_DxB_steers_less_2_yr_weight_gain(),
        "BxB_heifers_less_2_yr": animal_features.get_BxB_heifers_less_2_yr_weight_gain(),
        "BxB_steers_less_2_yr": animal_features.get_BxB_steers_less_2_yr_weight_gain(),
        "DxD_heifers_more_2_yr": animal_features.get_DxD_heifers_more_2_yr_weight_gain(),
        "DxD_steers_more_2_yr": animal_features.get_DxD_steers_more_2_yr_weight_gain(),
        "DxB_heifers_more_2_yr": animal_features.get_DxB_heifers_more_2_yr_weight_gain(),
        "DxB_steers_more_2_yr": animal_features.get_DxB_steers_more_2_yr_weight_gain(),
        "BxB_heifers_more_2_yr": animal_features.get_BxB_heifers_more_2_yr_weight_gain(),
        "BxB_steers_more_2_yr": animal_features.get_BxB_steers_more_2_yr_weight_gain(),
    }

    growth = {
        "dairy_cows": emissions_factors.get_ef_net_energy_for_growth_females(),
        "suckler_cows": emissions_factors.get_ef_net_energy_for_growth_females(),
        "bulls": emissions_factors.get_ef_net_energy_for_growth_bulls(),
        "DxD_calves_m": emissions_factors.get_ef_net_energy_for_growth_castrates(),
        "DxD_calves_f": emissions_factors.get_ef_net_energy_for_growth_females(),
        "DxB_calves_m": emissions_factors.get_ef_net_energy_for_growth_castrates(),
        "DxB_calves_f": emissions_factors.get_ef_net_energy_for_growth_females(),
        "BxB_calves_m": emissions_factors.get_ef_net_energy_for_growth_castrates(),
        "BxB_calves_f": emissions_factors.get_ef_net_energy_for_growth_females(),
        "DxD_heifers_less_2_yr": emissions_factors.get_ef_net_energy_for_growth_females(),
        "DxD_steers_less_2_yr": emissions_factors.get_ef_net_energy_for_growth_castrates(),
        "DxB_heifers_less_2_yr": emissions_factors.get_ef_net_energy_for_growth_females(),
        "DxB_steers_less_2_yr": emissions_factors.get_ef_net_energy_for_growth_castrates(),
        "BxB_heifers_less_2_yr": emissions_factors.get_ef_net_energy_for_growth_females(),
        "BxB_steers_less_2_yr": emissions_factors.get_ef_net_energy_for_growth_castrates(),
        "DxD_heifers_more_2_yr": emissions_factors.get_ef_net_energy_for_growth_females(),
        "DxD_steers_more_2_yr": emissions_factors.get_ef_net_energy_for_growth_castrates(),
        "DxB_heifers_more_2_yr": emissions_factors.get_ef_net_energy_for_growth_females(),
        "DxB_steers_more_2_yr": emissions_factors.get_ef_net_energy_for_growth_castrates(),
        "BxB_heifers_more_2_yr": emissions_factors.get_ef_net_energy_for_growth_females(),
        "BxB_steers_more_2_yr": emissions_factors.get_ef_net_energy_for_growth_castrates(),
    }

    gain = weight_gain.get(animal.cohort)
    coef = growth.get(animal.cohort)
    mature_weight_male = animal_features.get_mature_weight_bulls()
    mature_weight_dairy = animal_features.get_mature_weight_dairy_cows()
    mature_weight_suckler = animal_features.get_mature_weight_suckler_cows()

    males = [
        "bulls",
        "DxD_calves_m",
        "DxB_calves_m",
        "BxB_calves_m",
        "DxD_steers_less_2_yr",
        "DxB_steers_less_2_yr",
        "BxB_steers_less_2_yr",
        "DxD_steers_more_2_yr",
        "DxB_steers_more_2_yr",
        "BxB_steers_more_2_yr",
    ]

    if animal.cohort in males:
        return (
            22.02
            * ((animal.weight / (coef * mature_weight_male)) ** 0.75)
            * (gain**1.097)
        )
    else:
        if animal.cohort == "dairy_cows":
            return (
                22.02
                * ((animal.weight / (coef * mature_weight_dairy)) ** 0.75)
                * (gain**1.097)
            )
        elif animal.cohort == "suckler_cows":
            return (
                22.02
                * ((animal.weight / (coef * mature_weight_suckler)) ** 0.75)
                * (gain**1.097)
            )
        else:
            return (
                22.02
                * (
                    (
                        animal.weight
                        / (coef * ((mature_weight_suckler + mature_weight_dairy) / 2))
                    )
                    ** 0.75
                )
                * (gain**1.097)
            )


def net_energy_for_lactation(animal):
    """
    This function utilised milk density and fat content to calculate the energy needed for milk production
    """

    milk_density = 1.033
    milk = animal.daily_milk * milk_density
    fat = 3.5
    return milk * (1.47 + 0.40 * fat)


def net_energy_for_pregnancy(animal, emissions_factors):
    """
    This function utilised the net energy for maintenance by the emissions factor for preganancy to
    calculate energy required for pregnany

    Equation 10.13 from IPCC 2006 guidelines is utilised.
    """

    coef = emissions_factors.get_ef_net_energy_for_pregnancy()
    nep = 0

    if animal.cohort == "dairy_cows":
        nep = coef * net_energy_for_maintenance(animal, emissions_factors)
    elif animal.cohort == "suckler_cows":
        nep = coef * net_energy_for_maintenance(animal, emissions_factors)

    return nep


def gross_energy_from_concentrate(animal, concentrates):

    dm = concentrates.get_con_dry_matter_digestibility(animal.con_type)
    mj = concentrates.get_gross_energy_mje_dry_matter(animal.con_type)

    return (animal.con_amount * dm / 100) * mj


def gross_energy_from_grass(
    animal, grass, animal_features, emissions_factors, concentrates
):

    """
    This function utilises all of the energy equations to estimate the total energy intake from grasses minus the
    energy intake from concentrates
    """

    DMD = grass.get_forage_dry_matter_digestibility(animal.forage)

    REM = ratio_of_net_energy_maintenance(animal, grass)
    REG = ratio_of_net_energy_growth(animal, grass)
    NEM = net_energy_for_maintenance(animal, emissions_factors)
    NEA = net_energy_for_activity(animal, emissions_factors)
    NEL = net_energy_for_lactation(animal)
    NEP = net_energy_for_pregnancy(animal, emissions_factors)
    NEG = net_energy_for_weight_gain(animal, animal_features, emissions_factors)
    con = gross_energy_from_concentrate(animal, concentrates)

    return ((((NEM + NEA + NEL + NEP) / REM) + (NEG / REG)) / (DMD / 100.0)) - con


def total_gross_energy(animal, grass, animal_features, emissions_factors, concentrates):

    """
    This function utilises all of the energy equations to estimate the total energy intake from grasses minus the
    energy intake from concentrates
    """

    DMD = grass.get_forage_dry_matter_digestibility(animal.forage)

    REM = ratio_of_net_energy_maintenance(animal, grass)
    REG = ratio_of_net_energy_growth(animal, grass)
    NEM = net_energy_for_maintenance(animal, emissions_factors)
    NEA = net_energy_for_activity(animal, emissions_factors)
    NEL = net_energy_for_lactation(animal)
    NEP = net_energy_for_pregnancy(animal, emissions_factors)
    NEG = net_energy_for_weight_gain(animal, animal_features, emissions_factors)
    con = gross_energy_from_concentrate(animal, concentrates)

    return (((NEM + NEA + NEL + NEP) / REM) + (NEG / REG)) / (DMD / 100.0)


##REMI ADDED Functions
def dry_matter_from_grass(
    animal, grass, animal_features, emissions_factors, concentrates
):

    """
    This function utilises all of the energy equations to estimate the total energy intake from grasses minus the
    energy intake from concentrates
    """

    DMD = grass.get_forage_dry_matter_digestibility(animal.forage)

    REM = ratio_of_net_energy_maintenance(animal, grass)
    REG = ratio_of_net_energy_growth(animal, grass)
    NEM = net_energy_for_maintenance(animal, emissions_factors)
    NEA = net_energy_for_activity(animal, emissions_factors)
    NEL = net_energy_for_lactation(animal)
    NEP = net_energy_for_pregnancy(animal, emissions_factors)
    NEG = net_energy_for_weight_gain(animal, animal_features, emissions_factors)
    con = gross_energy_from_concentrate(animal, concentrates)
    GE = grass.get_gross_energy_mje_dry_matter(animal.forage)
    dm = concentrates.get_con_dry_matter_digestibility(animal.con_type)

    share_con = con / (
        ((NEM + NEA + NEL + NEP) / REM) + (NEG / REG)
    )  # proportion that is concentrate

    DMD_average = share_con * dm + (1 - share_con) * DMD

    return (
        ((((NEM + NEA + NEL + NEP) / REM) + (NEG / REG)) / (DMD_average / 100.0) - con)
    ) / GE


##REMI ADDED Functions
def gross_amount_from_con_in_percent(
    animal, grass, animal_features, emissions_factors, share_in_percent, concentrates
):

    """
    This function utilises all of the energy equations to estimate the total energy intake from grasses minus the
    energy intake from concentrates
    """

    REM = ratio_of_net_energy_maintenance(animal, grass)
    REG = ratio_of_net_energy_growth(animal, grass)
    NEM = net_energy_for_maintenance(animal, emissions_factors)
    NEA = net_energy_for_activity(animal, emissions_factors)
    NEL = net_energy_for_lactation(animal)
    NEP = net_energy_for_pregnancy(animal, emissions_factors)
    NEG = net_energy_for_weight_gain(animal, animal_features, emissions_factors)
    dm = concentrates.get_con_dry_matter_digestibility(animal.con_type)
    DMD = grass.get_forage_dry_matter_digestibility(animal.forage)
    mj_con = concentrates.get_gross_energy_mje_dry_matter(animal.con_type)
    mj_grass = grass.get_gross_energy_mje_dry_matter(animal.forage)

    DMD_average = share_in_percent / 100.0 * dm + (100.0 - share_in_percent) / 100 * DMD
    mj_average = (
        share_in_percent / 100.0 * mj_con
        + (100.0 - share_in_percent) / 100.0 * mj_grass
    )

    return (
        ((((NEM + NEA + NEL + NEP) / REM) + (NEG / REG)) / (DMD_average / 100.0))
        / mj_average
        * (share_in_percent / (100.0))
    )


def ch4_emissions_factor(
    animal, grass, concentrates, emissions_factors, animal_features
):
    """
    Function calculates the amount of methane emissions from feed intake utilising methane conversion
    factors

        GEC = Gross Energy from Concentrates
        GEG = Gross Energy from GE_grass
        Ym  = Methane conversion factor, percent of gross energy content of methane

        returns the emissions factor per cow per year
    """
    methane_conversion_factor = {
        "dairy_cows": emissions_factors.get_ef_methane_conversion_factor_dairy_cow(),
        "suckler_cows": emissions_factors.get_ef_methane_conversion_factor_dairy_cow(),
        "bulls": emissions_factors.get_ef_methane_conversion_factor_bulls(),
        "DxD_calves_m": emissions_factors.get_ef_methane_conversion_factor_calves(),
        "DxD_calves_f": emissions_factors.get_ef_methane_conversion_factor_calves(),
        "DxB_calves_m": emissions_factors.get_ef_methane_conversion_factor_calves(),
        "DxB_calves_f": emissions_factors.get_ef_methane_conversion_factor_calves(),
        "BxB_calves_m": emissions_factors.get_ef_methane_conversion_factor_calves(),
        "BxB_calves_f": emissions_factors.get_ef_methane_conversion_factor_calves(),
        "DxD_heifers_less_2_yr": emissions_factors.get_ef_methane_conversion_factor_dairy_cow(),
        "DxD_steers_less_2_yr": emissions_factors.get_ef_methane_conversion_factor_steer(),
        "DxB_heifers_less_2_yr": emissions_factors.get_ef_methane_conversion_factor_dairy_cow(),
        "DxB_steers_less_2_yr": emissions_factors.get_ef_methane_conversion_factor_steer(),
        "BxB_heifers_less_2_yr": emissions_factors.get_ef_methane_conversion_factor_dairy_cow(),
        "BxB_steers_less_2_yr": emissions_factors.get_ef_methane_conversion_factor_steer(),
        "DxD_heifers_more_2_yr": emissions_factors.get_ef_methane_conversion_factor_dairy_cow(),
        "DxD_steers_more_2_yr": emissions_factors.get_ef_methane_conversion_factor_steer(),
        "DxB_heifers_more_2_yr": emissions_factors.get_ef_methane_conversion_factor_dairy_cow(),
        "DxB_steers_more_2_yr": emissions_factors.get_ef_methane_conversion_factor_steer(),
        "BxB_heifers_more_2_yr": emissions_factors.get_ef_methane_conversion_factor_dairy_cow(),
        "BxB_steers_more_2_yr": emissions_factors.get_ef_methane_conversion_factor_steer(),
    }

    year = 365
    Ym = methane_conversion_factor.get(animal.cohort)

    methane_energy = 55.65  # MJ/kg of CH4

    GEC = gross_energy_from_concentrate(animal, concentrates)
    GEG = gross_energy_from_grass(
        animal, grass, animal_features, emissions_factors, concentrates
    )

    GET = (GEC + GEG) * year

    return GET * (Ym / methane_energy)


#############################################################################################
# CO2 from Concentrates production
#############################################################################################


def co2_from_concentrate_production(animal, concentrates):

    concentrate_co2 = 0

    for key in animal.__dict__.keys():

        if key in COHORTS and animal.__getattribute__(key).pop != 0:

            concentrate_co2 += (
                animal.__getattribute__(key).con_amount
                * concentrates.get_con_co2_e(animal.__getattribute__(key).con_type)
            ) * animal.__getattribute__(key).pop

    return concentrate_co2 * 365


#############################################################################################
# Grazing Stage
#############################################################################################


def percent_outdoors(animal):
    hours = 24
    return animal.t_outdoors / hours


def volatile_solids_excretion_rate_GRAZING(
    animal, grass, animal_features, emissions_factors, concentrates
):
    """
    This function calculates Volitile Solids Excretion Rate (kg/day -1) to pasture

    GEC   = Gross Energy from Concentrates
    GEG   = Gross Energy from grass
    DE    = Percentage of Digestible Energy
    UE    = Urinary Energy
    ASH   = Ash content of manure
    18.45 = conversion factor for dietary GE per kg of dry matter, MJ kg-1.
    """

    DEC = concentrates.get_con_digestible_energy(animal.con_type)  # Digestibility
    UE = 0.04
    ASH = 0.08
    DMD = grass.get_forage_dry_matter_digestibility(animal.forage)
    GEC = gross_energy_from_concentrate(animal, concentrates)
    GEG = gross_energy_from_grass(
        animal, grass, animal_features, emissions_factors, concentrates
    )
    OUT = percent_outdoors(animal)

    return (((GEG * (1 - (DMD / 100))) + (UE * GEG)) * ((1 - ASH) / 18.45)) + (
        (GEC * (1 - (DEC / 100)) + (UE * GEC)) * (((1 - ASH) / 18.45))
    )


def net_excretion_GRAZING(
    animal, grass, animal_features, emissions_factors, concentrates
):

    """
    This function calculates the net Nitrogen excretion (Nex) per kg to pasture
    """

    CP = concentrates.get_con_crude_protein(
        animal.con_type
    )  # crude protein percentage (N contained in crude protein), apparently, 16% is the average N content; https://www.feedipedia.org/node/8329
    FCP = grass.get_crude_protein(animal.forage)
    GEC = gross_energy_from_concentrate(animal, concentrates)
    GEG = gross_energy_from_grass(
        animal, grass, animal_features, emissions_factors, concentrates
    )
    OUT = percent_outdoors(animal)

    N_retention = {
        "dairy_cows": animal_features.get_dairy_cows_n_retention(),
        "suckler_cows": animal_features.get_suckler_cows_n_retention(),
        "bulls": animal_features.get_bulls_n_retention(),
        "DxD_calves_m": animal_features.get_DxD_calves_m_n_retention(),
        "DxD_calves_f": animal_features.get_DxD_calves_f_n_retention(),
        "DxB_calves_m": animal_features.get_DxB_calves_m_n_retention(),
        "DxB_calves_f": animal_features.get_DxB_calves_f_n_retention(),
        "BxB_calves_m": animal_features.get_BxB_calves_m_n_retention(),
        "BxB_calves_f": animal_features.get_BxB_calves_f_n_retention(),
        "DxD_heifers_less_2_yr": animal_features.get_DxD_heifers_less_2_yr_n_retention(),
        "DxD_steers_less_2_yr": animal_features.get_DxD_steers_less_2_yr_n_retention(),
        "DxB_heifers_less_2_yr": animal_features.get_DxB_heifers_less_2_yr_n_retention(),
        "DxB_steers_less_2_yr": animal_features.get_DxB_steers_less_2_yr_n_retention(),
        "BxB_heifers_less_2_yr": animal_features.get_BxB_heifers_less_2_yr_n_retention(),
        "BxB_steers_less_2_yr": animal_features.get_BxB_steers_less_2_yr_n_retention(),
        "DxD_heifers_more_2_yr": animal_features.get_DxD_heifers_more_2_yr_n_retention(),
        "DxD_steers_more_2_yr": animal_features.get_DxD_steers_more_2_yr_n_retention(),
        "DxB_heifers_more_2_yr": animal_features.get_DxB_heifers_more_2_yr_n_retention(),
        "DxB_steers_more_2_yr": animal_features.get_DxB_steers_more_2_yr_n_retention(),
        "BxB_heifers_more_2_yr": animal_features.get_BxB_heifers_more_2_yr_n_retention(),
        "BxB_steers_more_2_yr": animal_features.get_BxB_steers_more_2_yr_n_retention(),
    }

    N_retention_fraction = N_retention.get(animal.cohort)

    return (
        (((GEC * 365) / 18.45) * ((CP / 100) / 6.25) * (1 - N_retention_fraction))
        + ((((GEG * 365) / 18.45) * (FCP / 100.0) / 6.25) * (1 - 0.02))
    ) * OUT


def ch4_emissions_for_grazing(
    animal, grass, animal_features, emissions_factors, concentrates
):
    year = 365
    return (
        volatile_solids_excretion_rate_GRAZING(
            animal, grass, animal_features, emissions_factors, concentrates
        )
        * year
        * 0.1
        * 0.67
        * 0.02
    )


def nh3_emissions_per_year_GRAZING(
    animal, grass, animal_features, emissions_factors, concentrates
):
    """
    This function returns total N-NH3 per year
    """
    total_ammonia_nitrogen = {
        "dairy_cows": emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition(),
        "suckler_cows": emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition(),
        "bulls": emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition(),
        "DxD_calves_m": emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition(),
        "DxD_calves_f": emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition(),
        "DxB_calves_m": emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition(),
        "DxB_calves_f": emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition(),
        "BxB_calves_m": emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition(),
        "BxB_calves_f": emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition(),
        "DxD_heifers_less_2_yr": emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition(),
        "DxD_steers_less_2_yr": emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition(),
        "DxB_heifers_less_2_yr": emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition(),
        "DxB_steers_less_2_yr": emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition(),
        "BxB_heifers_less_2_yr": emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition(),
        "BxB_steers_less_2_yr": emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition(),
        "DxD_heifers_more_2_yr": emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition(),
        "DxD_steers_more_2_yr": emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition(),
        "DxB_heifers_more_2_yr": emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition(),
        "DxB_steers_more_2_yr": emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition(),
        "BxB_heifers_more_2_yr": emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition(),
        "BxB_steers_more_2_yr": emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition(),
    }

    TAN = total_ammonia_nitrogen.get(animal.cohort)

    return (
        net_excretion_GRAZING(
            animal, grass, animal_features, emissions_factors, concentrates
        )
        * 0.6
        * TAN
    )


def Nleach_GRAZING(animal, grass, animal_features, emissions_factors, concentrates):

    """
    This function returns the proportion of N leached from pasture
    """

    ten_percent_nex = 0.1

    return (
        net_excretion_GRAZING(
            animal, grass, animal_features, emissions_factors, concentrates
        )
        * ten_percent_nex
    )


def PLeach_GRAZING(animal, grass, animal_features, emissions_factors, concentrates):

    """
    This function returns the proportion of P leached from pasture
    """

    return (
        net_excretion_GRAZING(
            animal, grass, animal_features, emissions_factors, concentrates
        )
        * (1.8 / 5)
    ) * 0.03


# direct and indirect (from leaching) N20 from PRP


def PRP_N2O_direct(animal, grass, animal_features, emissions_factors, concentrates):

    """
    this function returns the direct n2o emissions from pasture, range and paddock

    direct_n2o_emissions_factors relate to EF3PRP.

    EF3PRP = emission factor for N2O emissions from urine and dung N deposited on pasture, range and paddock by grazing animals, kg N2O–N (kg N input)-1;

    Ireland utilises a disaggregated EF3PRP which is 56% lower than the IPCC 2006 value of 0.02
    """

    direct_n2o_emissions_factors = {
        "dairy_cows": emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o(),
        "suckler_cows": emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o(),
        "bulls": emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o(),
        "DxD_calves_m": emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o(),
        "DxD_calves_f": emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o(),
        "DxB_calves_m": emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o(),
        "DxB_calves_f": emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o(),
        "BxB_calves_m": emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o(),
        "BxB_calves_f": emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o(),
        "DxD_heifers_less_2_yr": emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o(),
        "DxD_steers_less_2_yr": emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o(),
        "DxB_heifers_less_2_yr": emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o(),
        "DxB_steers_less_2_yr": emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o(),
        "BxB_heifers_less_2_yr": emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o(),
        "BxB_steers_less_2_yr": emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o(),
        "DxD_heifers_more_2_yr": emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o(),
        "DxD_steers_more_2_yr": emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o(),
        "DxB_heifers_more_2_yr": emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o(),
        "DxB_steers_more_2_yr": emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o(),
        "BxB_heifers_more_2_yr": emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o(),
        "BxB_steers_more_2_yr": emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o(),
    }

    EF = direct_n2o_emissions_factors.get(animal.cohort)
    return (
        net_excretion_GRAZING(
            animal, grass, animal_features, emissions_factors, concentrates
        )
        * EF
    )


def PRP_N2O_indirect(animal, grass, animal_features, emissions_factors, concentrates):

    """
    This functions returns indirect n2o from atmospheric deposition and leaching related to pasture, range and paddock
    """

    atmospheric_deposition = {
        "dairy_cows": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "suckler_cows": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "bulls": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "DxD_calves_m": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "DxD_calves_f": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "DxB_calves_m": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "DxB_calves_f": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "BxB_calves_m": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "BxB_calves_f": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "DxD_heifers_less_2_yr": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "DxD_steers_less_2_yr": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "DxB_heifers_less_2_yr": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "DxB_steers_less_2_yr": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "BxB_heifers_less_2_yr": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "BxB_steers_less_2_yr": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "DxD_heifers_more_2_yr": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "DxD_steers_more_2_yr": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "DxB_heifers_more_2_yr": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "DxB_steers_more_2_yr": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "BxB_heifers_more_2_yr": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "BxB_steers_more_2_yr": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
    }

    leaching = {
        "dairy_cows": emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
        "suckler_cows": emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
        "bulls": emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
        "DxD_calves_m": emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
        "DxD_calves_f": emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
        "DxB_calves_m": emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
        "DxB_calves_f": emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
        "BxB_calves_m": emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
        "BxB_calves_f": emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
        "DxD_heifers_less_2_yr": emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
        "DxD_steers_less_2_yr": emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
        "DxB_heifers_less_2_yr": emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
        "DxB_steers_less_2_yr": emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
        "BxB_heifers_less_2_yr": emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
        "BxB_steers_less_2_yr": emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
        "DxD_heifers_more_2_yr": emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
        "DxD_steers_more_2_yr": emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
        "DxB_heifers_more_2_yr": emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
        "DxB_steers_more_2_yr": emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
        "BxB_heifers_more_2_yr": emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
        "BxB_steers_more_2_yr": emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
    }

    indirect_atmosphere = atmospheric_deposition.get(animal.cohort)
    indirect_leaching = leaching.get(animal.cohort)

    NH3 = nh3_emissions_per_year_GRAZING(
        animal, grass, animal_features, emissions_factors, concentrates
    )
    NL = Nleach_GRAZING(animal, grass, animal_features, emissions_factors, concentrates)

    return (NH3 * indirect_atmosphere) + (NL * indirect_leaching)


#############################################################################################
# Housing Stage
#############################################################################################


def percent_indoors(animal):
    hours = 24
    return (animal.t_indoors + animal.t_stabled) / hours


def VS_HOUSED(animal, grass, animal_features, emissions_factors, concentrates):
    """
    This function returns the volatile solids excreted per day for the period animals are
    housed.

    # Volitile Solids Excretion Rate (kg/day -1)
    # GEcon = Gross Energy from Concentrates
    # GEgrass = Gross Energy from grass
    # DE= Percentage of Digestible Energy
    # UE = Urinary Energy
    # ASH = Ash content of manure
    # 18.45 = conversion factor for dietary GE per kg of dry matter, MJ kg-1.
    """
    DEC = concentrates.get_con_digestible_energy(
        animal.con_type
    )  # Digestibility of concentrate
    UE = 0.04
    ASH = 0.08
    DMD = grass.get_forage_dry_matter_digestibility(animal.forage)
    GEC = gross_energy_from_concentrate(animal, concentrates)
    GEG = gross_energy_from_grass(
        animal, grass, animal_features, emissions_factors, concentrates
    )
    IN = percent_indoors(animal)

    return (
        (((GEC * (1 - (DEC / 100))) + (UE * GEC)) * ((1 - ASH) / 18.45))
        + ((GEG * (1 - (DMD / 100)) + (UE * GEG)) * ((1 - ASH) / 18.45))
    ) * IN


def net_excretion_HOUSED(
    animal, grass, animal_features, emissions_factors, concentrates
):
    """
    This function returns kg of nitrogen excreted per year while animals are housed

    - this function is a produces a rate that is a little higher than the costa rica model,
    however, this is likley due to the higher energy ratios resulting from the use of IPCC equations.
    """

    CP = concentrates.get_con_crude_protein(
        animal.con_type
    )  # crude protein percentage (N contained in crude protein), apparently, 16% is the average N content; https://www.feedipedia.org/node/8329
    FCP = grass.get_crude_protein(animal.forage)
    GEC = gross_energy_from_concentrate(animal, concentrates)
    GEG = gross_energy_from_grass(
        animal, grass, animal_features, emissions_factors, concentrates
    )
    IN = percent_indoors(animal)

    N_retention = {
        "dairy_cows": animal_features.get_dairy_cows_n_retention(),
        "suckler_cows": animal_features.get_suckler_cows_n_retention(),
        "bulls": animal_features.get_bulls_n_retention(),
        "DxD_calves_m": animal_features.get_DxD_calves_m_n_retention(),
        "DxD_calves_f": animal_features.get_DxD_calves_f_n_retention(),
        "DxB_calves_m": animal_features.get_DxB_calves_m_n_retention(),
        "DxB_calves_f": animal_features.get_DxB_calves_f_n_retention(),
        "BxB_calves_m": animal_features.get_BxB_calves_m_n_retention(),
        "BxB_calves_f": animal_features.get_BxB_calves_f_n_retention(),
        "DxD_heifers_less_2_yr": animal_features.get_DxD_heifers_less_2_yr_n_retention(),
        "DxD_steers_less_2_yr": animal_features.get_DxD_steers_less_2_yr_n_retention(),
        "DxB_heifers_less_2_yr": animal_features.get_DxB_heifers_less_2_yr_n_retention(),
        "DxB_steers_less_2_yr": animal_features.get_DxB_steers_less_2_yr_n_retention(),
        "BxB_heifers_less_2_yr": animal_features.get_BxB_heifers_less_2_yr_n_retention(),
        "BxB_steers_less_2_yr": animal_features.get_BxB_steers_less_2_yr_n_retention(),
        "DxD_heifers_more_2_yr": animal_features.get_DxD_heifers_more_2_yr_n_retention(),
        "DxD_steers_more_2_yr": animal_features.get_DxD_steers_more_2_yr_n_retention(),
        "DxB_heifers_more_2_yr": animal_features.get_DxB_heifers_more_2_yr_n_retention(),
        "DxB_steers_more_2_yr": animal_features.get_DxB_steers_more_2_yr_n_retention(),
        "BxB_heifers_more_2_yr": animal_features.get_BxB_heifers_more_2_yr_n_retention(),
        "BxB_steers_more_2_yr": animal_features.get_BxB_steers_more_2_yr_n_retention(),
    }

    N_retention_fraction = N_retention.get(animal.cohort)

    return (
        ((((GEC * 365) / 18.45) * ((CP / 100) / 6.25)) * (1 - N_retention_fraction))
        + ((((GEG * 365) / 18.45) * ((FCP / 100) / 6.25)) * (1 - 0.02))
    ) * IN


def total_ammonia_nitrogen_nh4_HOUSED(
    animal, grass, animal_features, emissions_factors, concentrates
):
    """
    This function returns the total ammonia nitrate (TAN) NH4 per year
    """
    percentage_nex = 0.6

    return (
        net_excretion_HOUSED(
            animal, grass, animal_features, emissions_factors, concentrates
        )
        * percentage_nex
    )


def nh3_emissions_per_year_HOUSED(
    animal, grass, animal_features, emissions_factors, concentrates
):

    """
    This function returns the total nh3 emissions per year for housing
    """

    # N-NH3 per year
    # TAN
    storage_TAN = {
        "tank solid": emissions_factors.get_ef_TAN_house_liquid(),
        "tank liquid": emissions_factors.get_ef_TAN_house_liquid(),
        "solid": emissions_factors.get_ef_TAN_house_solid(),
        "biodigester": emissions_factors.get_ef_TAN_storage_tank(),
    }

    return (
        total_ammonia_nitrogen_nh4_HOUSED(
            animal, grass, animal_features, emissions_factors, concentrates
        )
        * storage_TAN[animal.mm_storage]
    )


def HOUSING_N2O_indirect(
    animal, grass, animal_features, emissions_factors, concentrates
):

    """
    this function returns the indirect emissions from the housing Stage
    """
    ef = (
        emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water()
    )

    indirect_n2o = (
        nh3_emissions_per_year_HOUSED(
            animal, grass, animal_features, emissions_factors, concentrates
        )
        * ef
    )

    return indirect_n2o


#############################################################################################
# Storage Stage
#############################################################################################


def net_excretion_STORAGE(
    animal, grass, animal_features, emissions_factors, concentrates
):

    """
    This function returns kg of Nex per year from storage
    """

    return net_excretion_HOUSED(
        animal, grass, animal_features, emissions_factors, concentrates
    ) - nh3_emissions_per_year_HOUSED(
        animal, grass, animal_features, emissions_factors, concentrates
    )


def total_ammonia_nitrogen_nh4_STORAGE(
    animal, grass, animal_features, emissions_factors, concentrates
):

    """
    this function returns the total ammonia nitrogen (TAN) NH4 per year
    """
    percentage_nex = 0.6

    return (
        net_excretion_STORAGE(
            animal, grass, animal_features, emissions_factors, concentrates
        )
        * percentage_nex
    )


def CH4_STORAGE(animal, grass, animal_features, emissions_factors, concentrates):
    storage_MCF = {
        "tank solid": emissions_factors.get_ef_mcf_liquid_tank(),
        "tank liquid": emissions_factors.get_ef_mcf_liquid_tank(),
        "solid": emissions_factors.get_ef_mcf_solid_storage(),
        "biodigester": emissions_factors.get_ef_mcf_anaerobic_digestion(),
    }

    return (
        VS_HOUSED(animal, grass, animal_features, emissions_factors, concentrates) * 365
    ) * (0.1 * 0.67 * storage_MCF[animal.mm_storage])


def STORAGE_N2O_direct(animal, grass, animal_features, emissions_factors, concentrates):

    """
    This functions returns direct N2O emissions from manure storage
    """

    storage_N2O = {
        "tank solid": emissions_factors.get_ef_n2o_direct_storage_tank_solid(),  # crust cover for ireland
        "tank liquid": emissions_factors.get_ef_n2o_direct_storage_tank_liquid(),
        "solid": emissions_factors.get_ef_n2o_direct_storage_solid(),
        "biodigester": emissions_factors.get_ef_n2o_direct_storage_tank_anaerobic_digestion(),
    }

    return (
        net_excretion_STORAGE(
            animal, grass, animal_features, emissions_factors, concentrates
        )
        * storage_N2O[animal.mm_storage]
    )


def nh3_emissions_per_year_STORAGE(
    animal, grass, animal_features, emissions_factors, concentrates
):
    """
    This function returns the total nh3 emissions per year for storage
    """

    storage_TAN = {
        "tank solid": emissions_factors.get_ef_TAN_storage_tank(),
        "tank liquid": emissions_factors.get_ef_TAN_storage_tank(),
        "solid": emissions_factors.get_ef_TAN_storage_solid(),
        "biodigester": emissions_factors.get_ef_TAN_storage_tank(),
    }

    return (
        total_ammonia_nitrogen_nh4_STORAGE(
            animal, grass, animal_features, emissions_factors, concentrates
        )
        * storage_TAN[animal.mm_storage]
    )


def STORAGE_N2O_indirect(
    animal, grass, animal_features, emissions_factors, concentrates
):

    """
    This functions returns indirect n2o from atmospheric deposition and leaching related to storage
    """

    atmospheric_deposition = {
        "dairy_cows": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "suckler_cows": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "bulls": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "DxD_calves_m": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "DxD_calves_f": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "DxB_calves_m": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "DxB_calves_f": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "BxB_calves_m": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "BxB_calves_f": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "DxD_heifers_less_2_yr": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "DxD_steers_less_2_yr": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "DxB_heifers_less_2_yr": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "DxB_steers_less_2_yr": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "BxB_heifers_less_2_yr": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "BxB_steers_less_2_yr": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "DxD_heifers_more_2_yr": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "DxD_steers_more_2_yr": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "DxB_heifers_more_2_yr": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "DxB_steers_more_2_yr": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "BxB_heifers_more_2_yr": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "BxB_steers_more_2_yr": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
    }

    indirect_atmosphere = atmospheric_deposition.get(animal.cohort)

    NH3 = nh3_emissions_per_year_STORAGE(
        animal, grass, animal_features, emissions_factors, concentrates
    )

    return NH3 * indirect_atmosphere


###############################################################################
# Daily Spread
###############################################################################


def net_excretion_SPREAD(
    animal, grass, animal_features, emissions_factors, concentrates
):

    """
    This function returns Nex from daily spread
    """
    nex_storage = net_excretion_STORAGE(
        animal, grass, animal_features, emissions_factors, concentrates
    )
    direct_n2o = STORAGE_N2O_direct(
        animal, grass, animal_features, emissions_factors, concentrates
    )
    nh3_emissions = nh3_emissions_per_year_STORAGE(
        animal, grass, animal_features, emissions_factors, concentrates
    )
    indirect_n2o = STORAGE_N2O_indirect(
        animal, grass, animal_features, emissions_factors, concentrates
    )

    return nex_storage - direct_n2o - nh3_emissions - indirect_n2o


def total_ammonia_nitrogen_nh4_SPREAD(
    animal, grass, animal_features, emissions_factors, concentrates
):
    """
    this function returns the total ammonia nitrogen (TAN) NH4 per year from daily spread
    """
    percentage_nex = 0.6

    return (
        net_excretion_SPREAD(
            animal, grass, animal_features, emissions_factors, concentrates
        )
        * percentage_nex
    )


def SPREAD_N2O_direct(animal, grass, animal_features, emissions_factors, concentrates):

    """
    This function returns the proportion of N direct emissions from daily spread
    """

    n2o_direct = {
        "dairy_cows": emissions_factors.get_ef_direct_n2o_emissions_soils(),
        "suckler_cows": emissions_factors.get_ef_direct_n2o_emissions_soils(),
        "bulls": emissions_factors.get_ef_direct_n2o_emissions_soils(),
        "DxD_calves_m": emissions_factors.get_ef_direct_n2o_emissions_soils(),
        "DxD_calves_f": emissions_factors.get_ef_direct_n2o_emissions_soils(),
        "DxB_calves_m": emissions_factors.get_ef_direct_n2o_emissions_soils(),
        "DxB_calves_f": emissions_factors.get_ef_direct_n2o_emissions_soils(),
        "BxB_calves_m": emissions_factors.get_ef_direct_n2o_emissions_soils(),
        "BxB_calves_f": emissions_factors.get_ef_direct_n2o_emissions_soils(),
        "DxD_heifers_less_2_yr": emissions_factors.get_ef_direct_n2o_emissions_soils(),
        "DxD_steers_less_2_yr": emissions_factors.get_ef_direct_n2o_emissions_soils(),
        "DxB_heifers_less_2_yr": emissions_factors.get_ef_direct_n2o_emissions_soils(),
        "DxB_steers_less_2_yr": emissions_factors.get_ef_direct_n2o_emissions_soils(),
        "BxB_heifers_less_2_yr": emissions_factors.get_ef_direct_n2o_emissions_soils(),
        "BxB_steers_less_2_yr": emissions_factors.get_ef_direct_n2o_emissions_soils(),
        "DxD_heifers_more_2_yr": emissions_factors.get_ef_direct_n2o_emissions_soils(),
        "DxD_steers_more_2_yr": emissions_factors.get_ef_direct_n2o_emissions_soils(),
        "DxB_heifers_more_2_yr": emissions_factors.get_ef_direct_n2o_emissions_soils(),
        "DxB_steers_more_2_yr": emissions_factors.get_ef_direct_n2o_emissions_soils(),
        "BxB_heifers_more_2_yr": emissions_factors.get_ef_direct_n2o_emissions_soils(),
        "BxB_steers_more_2_yr": emissions_factors.get_ef_direct_n2o_emissions_soils(),
    }

    return net_excretion_SPREAD(
        animal, grass, animal_features, emissions_factors, concentrates
    ) * n2o_direct.get(animal.cohort)


def nh3_emissions_per_year_SPREAD(
    animal, grass, animal_features, emissions_factors, concentrates
):

    """
    this function returns nh3 emmissions per year from daily spreading
    """

    nh4 = total_ammonia_nitrogen_nh4_SPREAD(
        animal, grass, animal_features, emissions_factors, concentrates
    )

    daily_spreading = {
        "none": emissions_factors.get_ef_nh3_daily_spreading_none(),
        "manure": emissions_factors.get_ef_nh3_daily_spreading_manure(),
        "broadcast": emissions_factors.get_ef_nh3_daily_spreading_broadcast(),
        "injection": emissions_factors.get_ef_nh3_daily_spreading_injection(),
        "trailing hose": emissions_factors.get_ef_nh3_daily_spreading_traling_hose(),
    }

    return nh4 * daily_spreading[animal.daily_spreading]


def leach_nitrogen_SPREAD(
    animal, grass, animal_features, emissions_factors, concentrates
):

    """
    This function returns the proportion of nitrogen leached from spreading

    """

    ten_percent_nex = 0.1

    return (
        net_excretion_SPREAD(
            animal, grass, animal_features, emissions_factors, concentrates
        )
        * ten_percent_nex
    )


def leach_phospherous_SPREAD(
    animal, grass, animal_features, emissions_factors, concentrates
):

    """
    This function returns the proportion of kg P leach per year *(1.8/5))*0.03

    """

    return (
        net_excretion_SPREAD(
            animal, grass, animal_features, emissions_factors, concentrates
        )
        * (1.8 / 5)
    ) * 0.03


def SPREAD_N2O_indirect(
    animal, grass, animal_features, emissions_factors, concentrates
):

    """
    This functions returns indirect n2o from atmospheric deposition and leaching related to daily spread
    """

    atmospheric_deposition = {
        "dairy_cows": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "suckler_cows": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "bulls": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "DxD_calves_m": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "DxD_calves_f": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "DxB_calves_m": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "DxB_calves_f": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "BxB_calves_m": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "BxB_calves_f": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "DxD_heifers_less_2_yr": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "DxD_steers_less_2_yr": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "DxB_heifers_less_2_yr": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "DxB_steers_less_2_yr": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "BxB_heifers_less_2_yr": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "BxB_steers_less_2_yr": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "DxD_heifers_more_2_yr": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "DxD_steers_more_2_yr": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "DxB_heifers_more_2_yr": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "DxB_steers_more_2_yr": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "BxB_heifers_more_2_yr": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        "BxB_steers_more_2_yr": emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
    }

    leaching = {
        "dairy_cows": emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
        "suckler_cows": emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
        "bulls": emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
        "DxD_calves_m": emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
        "DxD_calves_f": emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
        "DxB_calves_m": emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
        "DxB_calves_f": emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
        "BxB_calves_m": emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
        "BxB_calves_f": emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
        "DxD_heifers_less_2_yr": emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
        "DxD_steers_less_2_yr": emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
        "DxB_heifers_less_2_yr": emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
        "DxB_steers_less_2_yr": emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
        "BxB_heifers_less_2_yr": emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
        "BxB_steers_less_2_yr": emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
        "DxD_heifers_more_2_yr": emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
        "DxD_steers_more_2_yr": emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
        "DxB_heifers_more_2_yr": emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
        "DxB_steers_more_2_yr": emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
        "BxB_heifers_more_2_yr": emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
        "BxB_steers_more_2_yr": emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
    }

    indirect_atmosphere = atmospheric_deposition.get(animal.cohort)
    indirect_leaching = leaching.get(animal.cohort)

    NH3 = nh3_emissions_per_year_SPREAD(
        animal, grass, animal_features, emissions_factors, concentrates
    )
    NL = leach_nitrogen_SPREAD(
        animal, grass, animal_features, emissions_factors, concentrates
    )

    return (NH3 * indirect_atmosphere) + (NL * indirect_leaching)


###############################################################################
# Farm & Upstream Emissions
###############################################################################

# Urea Fertiliser Emissions
def urea_N2O_direct(ef_country, total_urea, total_urea_abated, emissions_factors):

    """
    this function returns the total emissions from urea and abated urea applied to soils
    """

    ef_urea = emissions_factors.get_ef_urea()
    ef_urea_abated = emissions_factors.get_ef_urea_and_nbpt()

    return (total_urea * ef_urea) + (total_urea_abated * ef_urea_abated)


def urea_NH3(ef_country, total_urea, total_urea_abated, emissions_factors):

    """
    This function returns  the amount of urea and abated urea volatised.
    Below is the original fraction used in the Costa Rica version, however this seems to be incorrect.
    FRAC=0.02 #FracGASF ammoinium-fertilisers [fraction of synthetic fertiliser N that volatilises as NH3 and NOx under different conditions]
    """
    ef_urea = emissions_factors.get_ef_fracGASF_urea_fertilisers_to_nh3_and_nox()
    ef_urea_abated = emissions_factors.get_ef_fracGASF_urea_and_nbpt_to_nh3_and_nox()

    return (total_urea * ef_urea) + (total_urea_abated * ef_urea_abated)


def urea_nleach(ef_country, total_urea, total_urea_abated, emissions_factors):

    """
    This function returns  the amount of urea and abated urea leached from soils.

    Below is the original fraction used in the Costa Rica version, however this seems to be incorrect.
    FRAC=0.02 #FracGASF ammoinium-fertilisers [fraction of synthetic fertiliser N that volatilises as NH3 and NOx under different conditions]
    """

    leach = emissions_factors.get_ef_frac_leach_runoff()

    return (total_urea + total_urea_abated) * leach


def urea_N2O_indirect(ef_country, total_urea, total_urea_abated, emissions_factors):
    """
    this function returns the idirect emissions from urea
    """
    indirect_atmosphere = (
        emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water()
    )
    indirect_leaching = emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff()

    return (
        urea_NH3(ef_country, total_urea, total_urea_abated, emissions_factors)
        * indirect_atmosphere
    ) + (
        urea_nleach(ef_country, total_urea, total_urea_abated, emissions_factors)
        * indirect_leaching
    )


def urea_co2(total_urea, total_urea_abated):
    """
    returns the total CO2 from urea application
    """

    return ((total_urea + total_urea_abated) * 0.2) * (
        44 / 12
    )  # adjusted to the NIR version of this calculation


def urea_P_leach(total_urea, total_urea_abated, emissions_factors):
    """
    this function returns the idirect emissions from urea
    """
    frac_leach = float(emissions_factors.get_ef_Frac_P_Leach())

    return (total_urea + total_urea_abated) * frac_leach


# Nitrogen Fertiliser Emissions


def n_fertiliser_P_leach(total_n_fert, emissions_factors):
    """
    this function returns the idirect emissions from urea
    """
    frac_leach = float(emissions_factors.get_ef_Frac_P_Leach())

    return total_n_fert * frac_leach


def n_fertiliser_direct(ef_country, total_n_fert, emissions_factors):

    """
    This function returns total direct emissions from ammonium nitrate application at field level
    """
    ef = emissions_factors.get_ef_ammonium_nitrate()
    return total_n_fert * ef


def n_fertiliser_NH3(ef_country, total_n_fert, emissions_factors):

    """
    This function returns total NH3 emissions from ammonium nitrate application at field level
    """
    ef = emissions_factors.get_ef_fracGASF_ammonium_fertilisers_to_nh3_and_nox()
    return total_n_fert * ef


def n_fertiliser_nleach(ef_country, total_n_fert, emissions_factors):
    """
    This function returns total leached emissions from ammonium nitrate application at field level
    """

    ef = emissions_factors.get_ef_frac_leach_runoff()

    return total_n_fert * ef


def n_fertiliser_indirect(ef_country, total_n_fert, emissions_factors):

    """
    this function returns the indirect emissions from ammonium nitrate fertiliser
    """

    indirect_atmosphere = (
        emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water()
    )
    indirect_leaching = emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff()

    return (
        n_fertiliser_NH3(ef_country, total_n_fert, emissions_factors)
        * indirect_atmosphere
    ) + (
        n_fertiliser_nleach(ef_country, total_n_fert, emissions_factors)
        * indirect_leaching
    )


# Fertiliser Application Totals for N20 and CO2


def total_fertiliser_N20(
    ef_country, total_urea, total_urea_abated, total_n_fert, emissions_factors
):
    """
    This function returns the total direct and indirect emissions from urea and ammonium fertilisers
    """

    result = (
        urea_N2O_direct(ef_country, total_urea, total_urea_abated, emissions_factors)
        + urea_N2O_indirect(
            ef_country, total_urea, total_urea_abated, emissions_factors
        )
    ) + (
        n_fertiliser_direct(ef_country, total_n_fert, emissions_factors)
        + n_fertiliser_indirect(ef_country, total_n_fert, emissions_factors)
    )

    return result


def p_fertiliser_P_leach(total_p_fert, emissions_factors):
    """
    this function returns the idirect emissions from urea
    """
    frac_leach = float(emissions_factors.get_ef_Frac_P_Leach())

    return total_p_fert * frac_leach


################################################################################
# Total Global Warming Potential of whole farms (Upstream Processes & Fossil Fuel Energy)
################################################################################

# Emissions from on Farm Fossil Fuels


def diesel_CO2(upstream, diesel_kg):

    """
    this function returns the direct and indirect upstream CO2 emmisions from diesel
    """

    Diesel_indir = upstream.get_upstream_kg_co2e("diesel_indirect")
    Diest_dir = upstream.get_upstream_kg_co2e("diesel_direct")

    return diesel_kg * (Diest_dir + Diesel_indir)


def elec_CO2(upstream, elec_kwh):

    """
    this functino returns the upstream CO2 emissions from electricity consumption
    """

    elec_consumption = upstream.get_upstream_kg_co2e(
        "electricity_consumed"
    )  # based on Norway hydropower
    return elec_kwh * elec_consumption


# Emissions from upstream fertiliser production
def fert_upstream_CO2(
    upstream, total_n_fert, total_urea, total_urea_abated, total_p_fert, total_k_fert
):

    """
    this function returns the upstream emissions from urea and ammonium fertiliser manufature
    """
    AN_fert_CO2 = upstream.get_upstream_kg_co2e(
        "ammonium_nitrate_fertiliser"
    )  # Ammonium Nitrate Fertiliser
    Urea_fert_CO2 = upstream.get_upstream_kg_co2e("urea_fert")
    Triple_superphosphate = upstream.get_upstream_kg_co2e("triple_superphosphate")
    Potassium_chloride = upstream.get_upstream_kg_co2e("potassium_chloride")

    return (
        (total_n_fert * AN_fert_CO2)
        + (total_urea * Urea_fert_CO2)
        + (total_urea_abated * Urea_fert_CO2)
        + (total_p_fert * Triple_superphosphate)
        + (total_k_fert * Potassium_chloride)
    )


def fert_upstream_EP(
    upstream, total_n_fert, total_urea, total_urea_abated, total_p_fert, total_k_fert
):

    """
    this function returns the upstream emissions from urea and ammonium fertiliser manufature
    """
    AN_fert_PO4 = upstream.get_upstream_kg_po4e(
        "ammonium_nitrate_fertiliser"
    )  # Ammonium Nitrate Fertiliser
    Urea_fert_PO4 = upstream.get_upstream_kg_po4e("urea_fert")
    Triple_superphosphate = upstream.get_upstream_kg_po4e("triple_superphosphate")
    Potassium_chloride = upstream.get_upstream_kg_po4e("potassium_chloride")

    return (
        (total_n_fert * AN_fert_PO4)
        + (total_urea * Urea_fert_PO4)
        + (total_urea_abated * Urea_fert_PO4)
        + (total_p_fert * Triple_superphosphate)
        + (total_k_fert * Potassium_chloride)
    )


################################################################################
# Allocation
################################################################################
def live_weight_output(animal):
    return (
        (animal.dairy_cows.weight * animal.dairy_cows.n_sold)
        + (animal.suckler_cows.weight * animal.suckler_cows.n_sold)
        + (animal.bulls.weight * animal.bulls.n_sold)
        + (animal.DxD_calves_m.weight * animal.DxD_calves_m.n_sold)
        + (animal.DxD_calves_f.weight * animal.DxD_calves_f.n_sold)
        + (animal.DxB_calves_m.weight * animal.DxB_calves_m.n_sold)
        + (animal.DxB_calves_f.weight * animal.DxB_calves_f.n_sold)
        + (animal.BxB_calves_m.weight * animal.BxB_calves_m.n_sold)
        + (animal.BxB_calves_f.weight * animal.BxB_calves_f.n_sold)
        + (animal.DxD_heifers_less_2_yr.weight * animal.DxD_heifers_less_2_yr.n_sold)
        + (animal.DxD_steers_less_2_yr.weight * animal.DxD_steers_less_2_yr.n_sold)
        + (animal.DxB_heifers_less_2_yr.weight * animal.DxB_heifers_less_2_yr.n_sold)
        + (animal.DxB_steers_less_2_yr.weight * animal.DxB_steers_less_2_yr.n_sold)
        + (animal.BxB_heifers_less_2_yr.weight * animal.BxB_heifers_less_2_yr.n_sold)
        + (animal.BxB_steers_less_2_yr.weight * animal.BxB_steers_less_2_yr.n_sold)
        + (animal.DxD_heifers_more_2_yr.weight * animal.DxD_heifers_more_2_yr.n_sold)
        + (animal.DxD_steers_more_2_yr.weight * animal.DxD_steers_more_2_yr.n_sold)
        + (animal.DxB_heifers_more_2_yr.weight * animal.DxB_heifers_more_2_yr.n_sold)
        + (animal.DxB_steers_more_2_yr.weight * animal.DxB_steers_more_2_yr.n_sold)
        + (animal.BxB_heifers_more_2_yr.weight * animal.BxB_heifers_more_2_yr.n_sold)
        + (animal.BxB_steers_more_2_yr.weight * animal.BxB_steers_more_2_yr.n_sold)
    )


def live_weight_bought(animal):
    return (
        (animal.dairy_cows.weight * animal.dairy_cows.n_bought)
        + (animal.suckler_cows.weight * animal.suckler_cows.n_bought)
        + (animal.bulls.weight * animal.bulls.n_bought)
        + (animal.DxD_calves_m.weight * animal.DxD_calves_m.n_bought)
        + (animal.DxD_calves_f.weight * animal.DxD_calves_f.n_bought)
        + (animal.DxB_calves_m.weight * animal.DxB_calves_m.n_bought)
        + (animal.DxB_calves_f.weight * animal.DxB_calves_f.n_bought)
        + (animal.BxB_calves_m.weight * animal.BxB_calves_m.n_bought)
        + (animal.BxB_calves_f.weight * animal.BxB_calves_f.n_bought)
        + (animal.DxD_heifers_less_2_yr.weight * animal.DxD_heifers_less_2_yr.n_bought)
        + (animal.DxD_steers_less_2_yr.weight * animal.DxD_steers_less_2_yr.n_bought)
        + (animal.DxB_heifers_less_2_yr.weight * animal.DxB_heifers_less_2_yr.n_bought)
        + (animal.DxB_steers_less_2_yr.weight * animal.DxB_steers_less_2_yr.n_bought)
        + (animal.BxB_heifers_less_2_yr.weight * animal.BxB_heifers_less_2_yr.n_bought)
        + (animal.BxB_steers_less_2_yr.weight * animal.BxB_steers_less_2_yr.n_bought)
        + (animal.DxD_heifers_more_2_yr.weight * animal.DxD_heifers_more_2_yr.n_bought)
        + (animal.DxD_steers_more_2_yr.weight * animal.DxD_steers_more_2_yr.n_bought)
        + (animal.DxB_heifers_more_2_yr.weight * animal.DxB_heifers_more_2_yr.n_bought)
        + (animal.DxB_steers_more_2_yr.weight * animal.DxB_steers_more_2_yr.n_bought)
        + (animal.BxB_heifers_more_2_yr.weight * animal.BxB_heifers_more_2_yr.n_bought)
        + (animal.BxB_steers_more_2_yr.weight * animal.BxB_steers_more_2_yr.n_bought)
    )


def live_weight_to_mje(animal):
    converstion_MJe = 12.36
    return live_weight_output(animal) * converstion_MJe


def milk_to_kg_output(animal):
    # kg of milk
    kg_conversion = 1.033
    year = 365
    return animal.dairy_cows.daily_milk * animal.dairy_cows.pop * year * kg_conversion


def milk_to_mje(animal):
    converstion_MJe = 2.5
    return milk_to_kg_output(animal) * converstion_MJe


def milk_allocation_factor(animal):
    total = milk_to_mje(animal) + live_weight_to_mje(animal)
    return milk_to_mje(animal) / total


def meat_allocation_factor(animal):
    return 1 - milk_allocation_factor(animal)


################################################################################
# Totals
################################################################################


def CH4_enteric_ch4(animal, grass, concentrates, emissions_factors, animal_features):

    result = 0
    for key in animal.__dict__.keys():

        if key in COHORTS and animal.__getattribute__(key).pop != 0:

            result += (
                Enteric_CH4(
                    animal.__getattribute__(key),
                    grass,
                    concentrates,
                    emissions_factors,
                    animal_features,
                )
                * animal.__getattribute__(key).pop
            )

    return result


def CH4_manure_management(
    animal, grass, animal_features, emissions_factors, concentrates
):
    result = 0

    for key in animal.__dict__.keys():

        if key in COHORTS and animal.__getattribute__(key).pop != 0:

            result += (
                Total_manure_ch4(
                    animal.__getattribute__(key),
                    grass,
                    animal_features,
                    emissions_factors,
                    concentrates,
                )
                * animal.__getattribute__(key).pop
            )

    return result


def PRP_Total(animal, grass, animal_features, emissions_factors, concentrates):

    """
    this function returns the emissions total (N20-N) related to Pasture, Range and Paddock
    """
    mole_weight = 44 / 28

    return (
        PRP_N2O_direct(animal, grass, animal_features, emissions_factors, concentrates)
        + PRP_N2O_indirect(
            animal, grass, animal_features, emissions_factors, concentrates
        )
    ) * mole_weight


def Total_N2O_Spreading(
    animal, grass, animal_features, emissions_factors, concentrates
):

    """
    This function returns the total N20 related to manure storage and spreading
    """
    mole_weight = 44 / 28

    Spreading = 0

    for key in animal.__dict__.keys():

        if key in COHORTS and animal.__getattribute__(key).pop != 0:

            Spreading += (
                SPREAD_N2O_direct(
                    animal.__getattribute__(key),
                    grass,
                    animal_features,
                    emissions_factors,
                    concentrates,
                )
                + SPREAD_N2O_indirect(
                    animal.__getattribute__(key),
                    grass,
                    animal_features,
                    emissions_factors,
                    concentrates,
                )
                * animal.__getattribute__(key).pop
            )

    return Spreading * mole_weight


def Total_storage_N2O(animal, grass, animal_features, emissions_factors, concentrates):

    """
    This function returns the total N20 related to manure storage
    """

    mole_weight = 44 / 28

    n2o_direct = 0
    n2o_indirect_storage = 0
    n2o_indirect_housing = 0

    for key in animal.__dict__.keys():

        if key in COHORTS and animal.__getattribute__(key).pop != 0:

            n2o_direct += (
                STORAGE_N2O_direct(
                    animal.__getattribute__(key),
                    grass,
                    animal_features,
                    emissions_factors,
                    concentrates,
                )
                * animal.__getattribute__(key).pop
            )
            n2o_indirect_storage += (
                STORAGE_N2O_indirect(
                    animal.__getattribute__(key),
                    grass,
                    animal_features,
                    emissions_factors,
                    concentrates,
                )
                * animal.__getattribute__(key).pop
            )
            n2o_indirect_housing += (
                HOUSING_N2O_indirect(
                    animal.__getattribute__(key),
                    grass,
                    animal_features,
                    emissions_factors,
                    concentrates,
                )
                * animal.__getattribute__(key).pop
            )

    return (n2o_direct + n2o_indirect_storage + n2o_indirect_housing) * mole_weight


def N2O_total_PRP_N2O_direct(
    animal, grass, animal_features, emissions_factors, concentrates
):

    """
    this function returns the direct n2o emissions from pasture, range and paddock
    """

    mole_weight = 44 / 28

    PRP_direct = 0

    for key in animal.__dict__.keys():

        if key in COHORTS and animal.__getattribute__(key).pop != 0:

            PRP_direct += (
                PRP_N2O_direct(
                    animal.__getattribute__(key),
                    grass,
                    animal_features,
                    emissions_factors,
                    concentrates,
                )
                * animal.__getattribute__(key).pop
            )

    return PRP_direct * mole_weight


def N2O_total_PRP_N2O_indirect(
    animal, grass, animal_features, emissions_factors, concentrates
):

    mole_weight = 44 / 28

    PRP_indirect = 0

    for key in animal.__dict__.keys():

        if key in COHORTS and animal.__getattribute__(key).pop != 0:

            PRP_indirect += (
                PRP_N2O_indirect(
                    animal.__getattribute__(key),
                    grass,
                    animal_features,
                    emissions_factors,
                    concentrates,
                )
                * animal.__getattribute__(key).pop
            )

    return PRP_indirect * mole_weight


def Total_manure_ch4(animal, grass, animal_features, emissions_factors, concentrates):

    """
    this function returns the total ch4 related to manure storage
    """

    return ch4_emissions_for_grazing(
        animal, grass, animal_features, emissions_factors, concentrates
    ) + CH4_STORAGE(animal, grass, animal_features, emissions_factors, concentrates)


def Enteric_CH4(animal, grass, concentrates, emissions_factors, animal_features):

    return ch4_emissions_factor(
        animal, grass, concentrates, emissions_factors, animal_features
    )


def CO2_soils_GWP(ef_country, total_urea, total_urea_abated):
    return urea_co2(total_urea, total_urea_abated)


def N2O_direct_fertiliser(
    ef_country, total_urea, total_urea_abated, total_n_fert, emissions_factors
):
    """
    This function returns the total direct and indirect emissions from urea and ammonium fertilisers
    """

    mole_weight = 44 / 28

    result = (
        urea_N2O_direct(ef_country, total_urea, total_urea_abated, emissions_factors)
        + n_fertiliser_direct(ef_country, total_n_fert, emissions_factors)
    ) * mole_weight

    return result


def N2O_fertiliser_indirect(
    ef_country, emissions_factors, total_urea, total_urea_abated, total_n_fert
):

    mole_weight = 44 / 28

    Fertilizer_indirect = (
        n_fertiliser_indirect(ef_country, total_n_fert, emissions_factors)
        + urea_N2O_indirect(
            ef_country, total_urea, total_urea_abated, emissions_factors
        )
    ) * mole_weight

    return Fertilizer_indirect


def upstream_and_inputs_and_fuel_co2(
    upstream,
    diesel_kg,
    elec_kwh,
    total_n_fert,
    total_urea,
    total_urea_abated,
    total_p_fert,
    total_k_fert,
    animal,
    concentrates,
):

    return (
        diesel_CO2(upstream, diesel_kg)
        + elec_CO2(upstream, elec_kwh)
        + fert_upstream_CO2(
            upstream,
            total_n_fert,
            total_urea,
            total_urea_abated,
            total_p_fert,
            total_k_fert,
        )
        + co2_from_concentrate_production(animal, concentrates)
    )


###############################################################################
# Water Quality EP PO4e
###############################################################################

# Manure Management
def total_manure_NH3_EP(
    animal, grass, concentrates, emissions_factors, animal_features
):
    """
    Convert N to PO4  = 0.42

    """

    indirect_atmosphere = (
        emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water()
    )

    NH3N = 0

    for key in animal.__dict__.keys():
        if key in COHORTS and animal.__getattribute__(key).pop != 0:

            NH3N += (
                nh3_emissions_per_year_STORAGE(
                    animal.__getattribute__(key),
                    grass,
                    animal_features,
                    emissions_factors,
                    concentrates,
                )
                + nh3_emissions_per_year_HOUSED(
                    animal.__getattribute__(key),
                    grass,
                    animal_features,
                    emissions_factors,
                    concentrates,
                )
            ) * animal.__getattribute__(key).pop

    return (NH3N * indirect_atmosphere) * 0.42


# SOILS
def total_fertiliser_soils_NH3_and_LEACH_EP(
    ef_country, emissions_factors, total_urea, total_urea_abated, total_n_fert
):
    """
    Convert N to PO4  = 0.42

    """
    indirect_atmosphere = (
        emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water()
    )

    NH3N = urea_NH3(
        ef_country, total_urea, total_urea_abated, emissions_factors
    ) + n_fertiliser_NH3(ef_country, total_n_fert, emissions_factors)

    LEACH = urea_nleach(
        ef_country, total_urea, total_urea_abated, emissions_factors
    ) + n_fertiliser_nleach(ef_country, total_n_fert, emissions_factors)

    return (NH3N * indirect_atmosphere) + LEACH * 0.42


def total_grazing_soils_NH3_and_LEACH_EP(
    animal, grass, animal_features, emissions_factors, concentrates
):
    """
    Convert N to PO4  = 0.42

    """
    indirect_atmosphere = (
        emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water()
    )

    NH3N = 0

    LEACH = 0

    for key in animal.__dict__.keys():
        if key in COHORTS and animal.__getattribute__(key).pop != 0:
            NH3N += (
                nh3_emissions_per_year_GRAZING(
                    animal.__getattribute__(key),
                    grass,
                    animal_features,
                    emissions_factors,
                    concentrates,
                )
                + nh3_emissions_per_year_SPREAD(
                    animal.__getattribute__(key),
                    grass,
                    animal_features,
                    emissions_factors,
                    concentrates,
                )
            ) * animal.__getattribute__(key).pop

            LEACH += (
                Nleach_GRAZING(
                    animal.__getattribute__(key),
                    grass,
                    animal_features,
                    emissions_factors,
                    concentrates,
                )
                + leach_nitrogen_SPREAD(
                    animal.__getattribute__(key),
                    grass,
                    animal_features,
                    emissions_factors,
                    concentrates,
                )
            ) * animal.__getattribute__(key).pop

    return (NH3N * indirect_atmosphere) + LEACH * 0.42


def fertiliser_soils_P_LEACH_EP(
    emissions_factors, total_urea, total_urea_abated, total_n_fert, total_p_fert
):

    PLEACH = (
        urea_P_leach(total_urea, total_urea_abated, emissions_factors)
        + n_fertiliser_P_leach(total_n_fert, emissions_factors)
        + p_fertiliser_P_leach(total_p_fert, emissions_factors)
    )

    return PLEACH * 3.06


def grazing_soils_P_LEACH_EP(
    animal, grass, animal_features, emissions_factors, concentrates
):

    PLEACH = 0

    for key in animal.__dict__.keys():
        if key in COHORTS and animal.__getattribute__(key).pop != 0:

            PLEACH += (
                leach_phospherous_SPREAD(
                    animal.__getattribute__(key),
                    grass,
                    animal_features,
                    emissions_factors,
                    concentrates,
                )
                + PLeach_GRAZING(
                    animal.__getattribute__(key),
                    grass,
                    animal_features,
                    emissions_factors,
                    concentrates,
                )
            ) * animal.__getattribute__(key).pop

    return PLEACH * 3.06


def total_fertilser_soils_EP(
    ef_country,
    emissions_factors,
    total_urea,
    total_urea_abated,
    total_n_fert,
    total_p_fert,
):

    return total_fertiliser_soils_NH3_and_LEACH_EP(
        ef_country, emissions_factors, total_urea, total_urea_abated, total_n_fert
    ) + fertiliser_soils_P_LEACH_EP(
        emissions_factors, total_urea, total_urea_abated, total_n_fert, total_p_fert
    )


def total_grazing_soils_EP(
    animal, grass, animal_features, emissions_factors, concentrates
):

    return total_grazing_soils_NH3_and_LEACH_EP(
        animal, grass, animal_features, emissions_factors, concentrates
    ) + grazing_soils_P_LEACH_EP(
        animal,
        grass,
        animal_features,
        emissions_factors,
        concentrates,
    )


# Imported Feeds
def EP_from_concentrate_production(animal, concentrates):

    concentrate_p = 0

    for key in animal.__dict__.keys():

        if key in COHORTS and animal.__getattribute__(key).pop != 0:

            concentrate_p += (
                animal.__getattribute__(key).con_amount
                * concentrates.get_con_po4_e(animal.__getattribute__(key).con_type)
            ) * animal.__getattribute__(key).pop

    return concentrate_p * 365


###############################################################################
# Air Quality Ammonia
###############################################################################

# Manure Management
def total_manure_NH3_AQ(
    animal, grass, concentrates, emissions_factors, animal_features
):

    NH3N = 0

    for key in animal.__dict__.keys():
        if key in COHORTS and animal.__getattribute__(key).pop != 0:

            NH3N += (
                nh3_emissions_per_year_STORAGE(
                    animal.__getattribute__(key),
                    grass,
                    animal_features,
                    emissions_factors,
                    concentrates,
                )
                + nh3_emissions_per_year_HOUSED(
                    animal.__getattribute__(key),
                    grass,
                    animal_features,
                    emissions_factors,
                    concentrates,
                )
            ) * animal.__getattribute__(key).pop

    return NH3N


# SOILS
def total_fertiliser_soils_NH3_AQ(
    ef_country, emissions_factors, total_urea, total_urea_abated, total_n_fert
):

    NH3N = urea_NH3(
        ef_country, total_urea, total_urea_abated, emissions_factors
    ) + n_fertiliser_NH3(ef_country, total_n_fert, emissions_factors)

    return NH3N


def total_grazing_soils_NH3_AQ(
    animal, grass, animal_features, emissions_factors, concentrates
):

    NH3N = 0

    for key in animal.__dict__.keys():
        if key in COHORTS and animal.__getattribute__(key).pop != 0:
            NH3N += (
                nh3_emissions_per_year_GRAZING(
                    animal.__getattribute__(key),
                    grass,
                    animal_features,
                    emissions_factors,
                    concentrates,
                )
                + nh3_emissions_per_year_SPREAD(
                    animal.__getattribute__(key),
                    grass,
                    animal_features,
                    emissions_factors,
                    concentrates,
                )
            ) * animal.__getattribute__(key).pop

    return NH3N
