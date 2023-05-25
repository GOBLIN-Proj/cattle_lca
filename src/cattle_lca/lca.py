# Imports
from cattle_lca.data_loader import Loader


class Cohorts:
    def __init__(self) -> None:
        self.COHORTS = [
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
class Energy:
    def __init__(self, ef_country):
        self.loader_class = Loader(ef_country)

    def ratio_of_net_energy_maintenance(self, animal):
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

        DE = self.loader_class.grass.get_forage_dry_matter_digestibility(animal.forage)

        return (
            1.123
            - (4.092 * (10**-3) * DE)
            + (1.126 * (10**-5) * (DE**2))
            - (25.4 / DE)
        )

    def ratio_of_net_energy_growth(self, animal):
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

        DE = self.loader_class.grass.get_forage_dry_matter_digestibility(animal.forage)

        return (
            1.164
            - (5.160 * (10**-3) * DE)
            + (1.308 * (10**-5) * (DE**2))
            - (37.4 / DE)
        )

    #############################################################################################
    # Energy & Enteric Fermentation
    #############################################################################################

    def net_energy_for_maintenance(self, animal):
        """
        When this function is called, it returns the coefficient, which is the emisions factor for net energy
        for lactation, multiplied by the square root of animal weight to the power of 0.75.

        coefficient X (animal_weight^0.75)

        It utilises equation 10.3 from the IPCC 2006 guidelines (NEm)
        """

        coefficient = {
            "dairy_cows": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_lactating_cow(),
            "suckler_cows": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_lactating_cow(),
            "bulls": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_bulls(),
            "DxD_calves_m": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow(),
            "DxD_calves_f": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow(),
            "DxB_calves_m": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow(),
            "DxB_calves_f": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow(),
            "BxB_calves_m": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow(),
            "BxB_calves_f": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow(),
            "DxD_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow(),
            "DxD_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow(),
            "DxB_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow(),
            "DxB_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow(),
            "BxB_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow(),
            "BxB_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow(),
            "DxD_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow(),
            "DxD_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow(),
            "DxB_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow(),
            "DxB_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow(),
            "BxB_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow(),
            "BxB_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow(),
        }

        cfi = coefficient.get(animal.cohort)

        return cfi * (animal.weight**0.75)

    def net_energy_for_activity(self, animal):
        """
        When this function is called it utilises the net_energy_for_maintenance eq multiplied by
        the coefficient for feed situation

        The equation is based on equation 10.4 from the IPCC 2006 guidelines.
        """

        grazing_type = {
            "pasture": self.loader_class.emissions_factors.get_ef_feeding_situation_pasture(),
            "large area": self.loader_class.emissions_factors.get_ef_feeding_situation_large_area(),
            "stall": self.loader_class.emissions_factors.get_ef_feeding_situation_stall(),
        }

        return grazing_type.get(animal.grazing) * self.net_energy_for_maintenance(
            animal
        )

    def net_energy_for_weight_gain(self, animal):
        """
        This function is the net energy for growth, it is parameterised to the animals weight gain per day.
        It utilises equation 10.6 from the IPCC 2006 guidelines (NEg)

        """

        weight_gain = {
            "dairy_cows": self.loader_class.animal_features.get_dairy_cows_weight_gain(),
            "suckler_cows": self.loader_class.animal_features.get_suckler_cows_weight_gain(),
            "bulls": self.loader_class.animal_features.get_bulls_weight_gain(),
            "DxD_calves_m": self.loader_class.animal_features.get_DxD_calves_m_weight_gain(),
            "DxD_calves_f": self.loader_class.animal_features.get_DxD_calves_f_weight_gain(),
            "DxB_calves_m": self.loader_class.animal_features.get_DxB_calves_m_weight_gain(),
            "DxB_calves_f": self.loader_class.animal_features.get_DxB_calves_f_weight_gain(),
            "BxB_calves_m": self.loader_class.animal_features.get_BxB_calves_m_weight_gain(),
            "BxB_calves_f": self.loader_class.animal_features.get_BxB_calves_f_weight_gain(),
            "DxD_heifers_less_2_yr": self.loader_class.animal_features.get_DxD_heifers_less_2_yr_weight_gain(),
            "DxD_steers_less_2_yr": self.loader_class.animal_features.get_DxD_steers_less_2_yr_weight_gain(),
            "DxB_heifers_less_2_yr": self.loader_class.animal_features.get_DxB_heifers_less_2_yr_weight_gain(),
            "DxB_steers_less_2_yr": self.loader_class.animal_features.get_DxB_steers_less_2_yr_weight_gain(),
            "BxB_heifers_less_2_yr": self.loader_class.animal_features.get_BxB_heifers_less_2_yr_weight_gain(),
            "BxB_steers_less_2_yr": self.loader_class.animal_features.get_BxB_steers_less_2_yr_weight_gain(),
            "DxD_heifers_more_2_yr": self.loader_class.animal_features.get_DxD_heifers_more_2_yr_weight_gain(),
            "DxD_steers_more_2_yr": self.loader_class.animal_features.get_DxD_steers_more_2_yr_weight_gain(),
            "DxB_heifers_more_2_yr": self.loader_class.animal_features.get_DxB_heifers_more_2_yr_weight_gain(),
            "DxB_steers_more_2_yr": self.loader_class.animal_features.get_DxB_steers_more_2_yr_weight_gain(),
            "BxB_heifers_more_2_yr": self.loader_class.animal_features.get_BxB_heifers_more_2_yr_weight_gain(),
            "BxB_steers_more_2_yr": self.loader_class.animal_features.get_BxB_steers_more_2_yr_weight_gain(),
        }

        growth = {
            "dairy_cows": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_females(),
            "suckler_cows": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_females(),
            "bulls": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_bulls(),
            "DxD_calves_m": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_castrates(),
            "DxD_calves_f": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_females(),
            "DxB_calves_m": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_castrates(),
            "DxB_calves_f": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_females(),
            "BxB_calves_m": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_castrates(),
            "BxB_calves_f": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_females(),
            "DxD_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_females(),
            "DxD_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_castrates(),
            "DxB_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_females(),
            "DxB_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_castrates(),
            "BxB_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_females(),
            "BxB_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_castrates(),
            "DxD_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_females(),
            "DxD_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_castrates(),
            "DxB_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_females(),
            "DxB_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_castrates(),
            "BxB_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_females(),
            "BxB_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_castrates(),
        }

        gain = weight_gain.get(animal.cohort)
        coef = growth.get(animal.cohort)
        mature_weight_male = self.loader_class.animal_features.get_mature_weight_bulls()
        mature_weight_dairy = (
            self.loader_class.animal_features.get_mature_weight_dairy_cows()
        )
        mature_weight_suckler = (
            self.loader_class.animal_features.get_mature_weight_suckler_cows()
        )

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
                            / (
                                coef
                                * ((mature_weight_suckler + mature_weight_dairy) / 2)
                            )
                        )
                        ** 0.75
                    )
                    * (gain**1.097)
                )

    def net_energy_for_lactation(self, animal):
        """
        This function utilised milk density and fat content to calculate the energy needed for milk production
        """

        milk_density = 1.033
        milk = animal.daily_milk * milk_density
        fat = 3.5
        return milk * (1.47 + 0.40 * fat)

    def net_energy_for_pregnancy(self, animal):
        """
        This function utilised the net energy for maintenance by the emissions factor for preganancy to
        calculate energy required for pregnany

        Equation 10.13 from IPCC 2006 guidelines is utilised.
        """

        coef = self.loader_class.emissions_factors.get_ef_net_energy_for_pregnancy()
        nep = 0

        if animal.cohort == "dairy_cows":
            nep = coef * self.net_energy_for_maintenance(animal)
        elif animal.cohort == "suckler_cows":
            nep = coef * self.net_energy_for_maintenance(animal)

        return nep

    def gross_energy_from_concentrate(self, animal):
        dm = self.loader_class.concentrates.get_con_dry_matter_digestibility(
            animal.con_type
        )
        mj = self.loader_class.concentrates.get_gross_energy_mje_dry_matter(
            animal.con_type
        )

        return (animal.con_amount * dm / 100) * mj

    def gross_energy_from_grass(self, animal):
        """
        This function utilises all of the energy equations to estimate the total energy intake from grasses minus the
        energy intake from concentrates
        """

        DMD = self.loader_class.grass.get_forage_dry_matter_digestibility(animal.forage)

        REM = self.ratio_of_net_energy_maintenance(animal)
        REG = self.ratio_of_net_energy_growth(animal)
        NEM = self.net_energy_for_maintenance(animal)
        NEA = self.net_energy_for_activity(animal)
        NEL = self.net_energy_for_lactation(animal)
        NEP = self.net_energy_for_pregnancy(animal)
        NEG = self.net_energy_for_weight_gain(animal)
        con = self.gross_energy_from_concentrate(animal)

        return ((((NEM + NEA + NEL + NEP) / REM) + (NEG / REG)) / (DMD / 100.0)) - con

    def total_gross_energy(self, animal):
        """
        This function utilises all of the energy equations to estimate the total energy intake from grasses minus the
        energy intake from concentrates
        """

        DMD = self.loader_class.grass.get_forage_dry_matter_digestibility(animal.forage)

        REM = self.ratio_of_net_energy_maintenance(animal)
        REG = self.ratio_of_net_energy_growth(animal)
        NEM = self.net_energy_for_maintenance(animal)
        NEA = self.net_energy_for_activity(animal)
        NEL = self.net_energy_for_lactation(animal)
        NEP = self.net_energy_for_pregnancy(animal)
        NEG = self.net_energy_for_weight_gain(animal)
        con = self.gross_energy_from_concentrate(animal)

        return (((NEM + NEA + NEL + NEP) / REM) + (NEG / REG)) / (DMD / 100.0)


class GrassFeed:
    def __init__(self, ef_country):
        self.energy_class = Energy(ef_country)
        self.cohorts_class = Cohorts()
        self.loader_class = Loader(ef_country)

    def dry_matter_from_grass(self, animal):
        """
        This function utilises all of the energy equations to estimate the total energy intake from grasses minus the
        energy intake from concentrates
        """

        DMD = self.loader_class.grass.get_forage_dry_matter_digestibility(animal.forage)

        REM = self.energy_class.ratio_of_net_energy_maintenance(animal)
        REG = self.energy_class.ratio_of_net_energy_growth(animal)
        NEM = self.energy_class.net_energy_for_maintenance(animal)
        NEA = self.energy_class.net_energy_for_activity(animal)
        NEL = self.energy_class.net_energy_for_lactation(animal)
        NEP = self.energy_class.net_energy_for_pregnancy(animal)
        NEG = self.energy_class.net_energy_for_weight_gain(animal)
        con = self.energy_class.gross_energy_from_concentrate(animal)
        GE = self.loader_class.grass.get_gross_energy_mje_dry_matter(animal.forage)
        dm = self.loader_class.concentrates.get_con_dry_matter_digestibility(
            animal.con_type
        )

        share_con = con / (
            ((NEM + NEA + NEL + NEP) / REM) + (NEG / REG)
        )  # proportion that is concentrate

        DMD_average = share_con * dm + (1 - share_con) * DMD

        return (
            (
                (((NEM + NEA + NEL + NEP) / REM) + (NEG / REG)) / (DMD_average / 100.0)
                - con
            )
        ) / GE

    ##REMI ADDED Functions
    def gross_amount_from_con_in_percent(self, animal, share_in_percent):
        """
        This function utilises all of the energy equations to estimate the total energy intake from grasses minus the
        energy intake from concentrates
        """

        REM = self.energy_class.ratio_of_net_energy_maintenance(animal)
        REG = self.energy_class.ratio_of_net_energy_growth(animal)
        NEM = self.energy_class.net_energy_for_maintenance(animal)
        NEA = self.energy_class.net_energy_for_activity(animal)
        NEL = self.energy_class.net_energy_for_lactation(animal)
        NEP = self.energy_class.net_energy_for_pregnancy(animal)
        NEG = self.energy_class.net_energy_for_weight_gain(animal)
        dm = self.loader_class.concentrates.get_con_dry_matter_digestibility(
            animal.con_type
        )
        DMD = self.loader_class.grass.get_forage_dry_matter_digestibility(animal.forage)
        mj_con = self.loader_class.concentrates.get_gross_energy_mje_dry_matter(
            animal.con_type
        )
        mj_grass = self.loader_class.grass.get_gross_energy_mje_dry_matter(
            animal.forage
        )

        DMD_average = (
            share_in_percent / 100.0 * dm + (100.0 - share_in_percent) / 100 * DMD
        )
        mj_average = (
            share_in_percent / 100.0 * mj_con
            + (100.0 - share_in_percent) / 100.0 * mj_grass
        )

        return (
            ((((NEM + NEA + NEL + NEP) / REM) + (NEG / REG)) / (DMD_average / 100.0))
            / mj_average
            * (share_in_percent / (100.0))
        )

    def ch4_emissions_factor(self, animal):
        """
        Function calculates the amount of methane emissions from feed intake utilising methane conversion
        factors

            GEC = Gross Energy from Concentrates
            GEG = Gross Energy from GE_grass
            Ym  = Methane conversion factor, percent of gross energy content of methane

            returns the emissions factor per cow per year
        """
        methane_conversion_factor = {
            "dairy_cows": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_dairy_cow(),
            "suckler_cows": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_dairy_cow(),
            "bulls": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_bulls(),
            "DxD_calves_m": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_calves(),
            "DxD_calves_f": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_calves(),
            "DxB_calves_m": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_calves(),
            "DxB_calves_f": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_calves(),
            "BxB_calves_m": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_calves(),
            "BxB_calves_f": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_calves(),
            "DxD_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_dairy_cow(),
            "DxD_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_steer(),
            "DxB_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_dairy_cow(),
            "DxB_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_steer(),
            "BxB_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_dairy_cow(),
            "BxB_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_steer(),
            "DxD_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_dairy_cow(),
            "DxD_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_steer(),
            "DxB_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_dairy_cow(),
            "DxB_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_steer(),
            "BxB_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_dairy_cow(),
            "BxB_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_steer(),
        }

        year = 365
        Ym = methane_conversion_factor.get(animal.cohort)

        methane_energy = 55.65  # MJ/kg of CH4

        GEC = self.energy_class.gross_energy_from_concentrate(animal)
        GEG = self.energy_class.gross_energy_from_grass(animal)

        GET = (GEC + GEG) * year

        return GET * (Ym / methane_energy)


#############################################################################################
# Grazing Stage
#############################################################################################


class GrazingStage:
    def __init__(self, ef_country):
        self.loader_class = Loader(ef_country)
        self.energy_class = Energy(ef_country)
        self.grass_feed_class = GrassFeed(ef_country)

    def percent_outdoors(self, animal):
        hours = 24
        return animal.t_outdoors / hours

    def volatile_solids_excretion_rate_GRAZING(self, animal):
        """
        This function calculates Volitile Solids Excretion Rate (kg/day -1) to pasture

        GEC   = Gross Energy from Concentrates
        GEG   = Gross Energy from grass
        DE    = Percentage of Digestible Energy
        UE    = Urinary Energy
        ASH   = Ash content of manure
        18.45 = conversion factor for dietary GE per kg of dry matter, MJ kg-1.
        """

        DEC = self.loader_class.concentrates.get_con_digestible_energy(
            animal.con_type
        )  # Digestibility
        UE = 0.04
        ASH = 0.08
        DMD = self.loader_class.grass.get_forage_dry_matter_digestibility(animal.forage)
        GEC = self.energy_class.gross_energy_from_concentrate(animal)
        GEG = self.energy_class.gross_energy_from_grass(animal)
        OUT = self.percent_outdoors(animal)

        return (((GEG * (1 - (DMD / 100))) + (UE * GEG)) * ((1 - ASH) / 18.45)) + (
            (GEC * (1 - (DEC / 100)) + (UE * GEC)) * (((1 - ASH) / 18.45))
        ) * OUT

    def net_excretion_GRAZING(self, animal):
        """
        This function calculates the net Nitrogen excretion (Nex) per kg to pasture
        """

        CP = self.loader_class.concentrates.get_con_crude_protein(
            animal.con_type
        )  # crude protein percentage (N contained in crude protein), apparently, 16% is the average N content; https://www.feedipedia.org/node/8329
        FCP = self.loader_class.grass.get_crude_protein(animal.forage)
        GEC = self.energy_class.gross_energy_from_concentrate(animal)
        GEG = self.energy_class.gross_energy_from_grass(animal)
        OUT = self.percent_outdoors(animal)

        N_retention = {
            "dairy_cows": self.loader_class.animal_features.get_dairy_cows_n_retention(),
            "suckler_cows": self.loader_class.animal_features.get_suckler_cows_n_retention(),
            "bulls": self.loader_class.animal_features.get_bulls_n_retention(),
            "DxD_calves_m": self.loader_class.animal_features.get_DxD_calves_m_n_retention(),
            "DxD_calves_f": self.loader_class.animal_features.get_DxD_calves_f_n_retention(),
            "DxB_calves_m": self.loader_class.animal_features.get_DxB_calves_m_n_retention(),
            "DxB_calves_f": self.loader_class.animal_features.get_DxB_calves_f_n_retention(),
            "BxB_calves_m": self.loader_class.animal_features.get_BxB_calves_m_n_retention(),
            "BxB_calves_f": self.loader_class.animal_features.get_BxB_calves_f_n_retention(),
            "DxD_heifers_less_2_yr": self.loader_class.animal_features.get_DxD_heifers_less_2_yr_n_retention(),
            "DxD_steers_less_2_yr": self.loader_class.animal_features.get_DxD_steers_less_2_yr_n_retention(),
            "DxB_heifers_less_2_yr": self.loader_class.animal_features.get_DxB_heifers_less_2_yr_n_retention(),
            "DxB_steers_less_2_yr": self.loader_class.animal_features.get_DxB_steers_less_2_yr_n_retention(),
            "BxB_heifers_less_2_yr": self.loader_class.animal_features.get_BxB_heifers_less_2_yr_n_retention(),
            "BxB_steers_less_2_yr": self.loader_class.animal_features.get_BxB_steers_less_2_yr_n_retention(),
            "DxD_heifers_more_2_yr": self.loader_class.animal_features.get_DxD_heifers_more_2_yr_n_retention(),
            "DxD_steers_more_2_yr": self.loader_class.animal_features.get_DxD_steers_more_2_yr_n_retention(),
            "DxB_heifers_more_2_yr": self.loader_class.animal_features.get_DxB_heifers_more_2_yr_n_retention(),
            "DxB_steers_more_2_yr": self.loader_class.animal_features.get_DxB_steers_more_2_yr_n_retention(),
            "BxB_heifers_more_2_yr": self.loader_class.animal_features.get_BxB_heifers_more_2_yr_n_retention(),
            "BxB_steers_more_2_yr": self.loader_class.animal_features.get_BxB_steers_more_2_yr_n_retention(),
        }

        N_retention_fraction = N_retention.get(animal.cohort)

        return (
            (((GEC * 365) / 18.45) * ((CP / 100) / 6.25) * (1 - N_retention_fraction))
            + ((((GEG * 365) / 18.45) * (FCP / 100.0) / 6.25) * (1 - 0.02))
        ) * OUT

    def ch4_emissions_for_grazing(self, animal):
        year = 365
        return (
            self.volatile_solids_excretion_rate_GRAZING(animal)
            * year
            * 0.1
            * 0.67
            * 0.02
        )

    def nh3_emissions_per_year_GRAZING(self, animal):
        """
        This function returns total N-NH3 per year
        """
        total_ammonia_nitrogen = {
            "dairy_cows": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition(),
            "suckler_cows": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition(),
            "bulls": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition(),
            "DxD_calves_m": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition(),
            "DxD_calves_f": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition(),
            "DxB_calves_m": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition(),
            "DxB_calves_f": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition(),
            "BxB_calves_m": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition(),
            "BxB_calves_f": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition(),
            "DxD_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition(),
            "DxD_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition(),
            "DxB_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition(),
            "DxB_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition(),
            "BxB_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition(),
            "BxB_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition(),
            "DxD_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition(),
            "DxD_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition(),
            "DxB_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition(),
            "DxB_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition(),
            "BxB_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition(),
            "BxB_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition(),
        }

        TAN = total_ammonia_nitrogen.get(animal.cohort)

        return self.net_excretion_GRAZING(animal) * 0.6 * TAN

    def Nleach_GRAZING(self, animal):
        """
        This function returns the proportion of N leached from pasture
        """

        ten_percent_nex = 0.1

        return self.net_excretion_GRAZING(animal) * ten_percent_nex

    def PLeach_GRAZING(self, animal):
        """
        This function returns the proportion of P leached from pasture
        """

        return (self.net_excretion_GRAZING(animal) * (1.8 / 5)) * 0.03

    # direct and indirect (from leaching) N20 from PRP

    def PRP_N2O_direct(self, animal):
        """
        this function returns the direct n2o emissions from pasture, range and paddock

        direct_n2o_emissions_factors relate to EF3PRP.

        EF3PRP = emission factor for N2O emissions from urine and dung N deposited on pasture, range and paddock by grazing animals, kg N2O–N (kg N input)-1;

        Ireland utilises a disaggregated EF3PRP which is 56% lower than the IPCC 2006 value of 0.02
        """

        direct_n2o_emissions_factors = {
            "dairy_cows": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o(),
            "suckler_cows": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o(),
            "bulls": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o(),
            "DxD_calves_m": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o(),
            "DxD_calves_f": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o(),
            "DxB_calves_m": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o(),
            "DxB_calves_f": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o(),
            "BxB_calves_m": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o(),
            "BxB_calves_f": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o(),
            "DxD_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o(),
            "DxD_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o(),
            "DxB_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o(),
            "DxB_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o(),
            "BxB_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o(),
            "BxB_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o(),
            "DxD_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o(),
            "DxD_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o(),
            "DxB_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o(),
            "DxB_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o(),
            "BxB_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o(),
            "BxB_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o(),
        }

        EF = direct_n2o_emissions_factors.get(animal.cohort)
        return self.net_excretion_GRAZING(animal) * EF

    def PRP_N2O_indirect(self, animal):
        """
        This functions returns indirect n2o from atmospheric deposition and leaching related to pasture, range and paddock
        """

        atmospheric_deposition = {
            "dairy_cows": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "suckler_cows": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "bulls": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "DxD_calves_m": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "DxD_calves_f": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "DxB_calves_m": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "DxB_calves_f": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "BxB_calves_m": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "BxB_calves_f": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "DxD_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "DxD_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "DxB_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "DxB_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "BxB_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "BxB_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "DxD_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "DxD_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "DxB_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "DxB_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "BxB_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "BxB_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        }

        leaching = {
            "dairy_cows": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
            "suckler_cows": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
            "bulls": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
            "DxD_calves_m": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
            "DxD_calves_f": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
            "DxB_calves_m": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
            "DxB_calves_f": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
            "BxB_calves_m": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
            "BxB_calves_f": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
            "DxD_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
            "DxD_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
            "DxB_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
            "DxB_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
            "BxB_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
            "BxB_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
            "DxD_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
            "DxD_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
            "DxB_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
            "DxB_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
            "BxB_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
            "BxB_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
        }

        indirect_atmosphere = atmospheric_deposition.get(animal.cohort)
        indirect_leaching = leaching.get(animal.cohort)

        NH3 = self.nh3_emissions_per_year_GRAZING(animal)
        NL = self.Nleach_GRAZING(animal)

        return (NH3 * indirect_atmosphere) + (NL * indirect_leaching)


#############################################################################################
# Housing Stage
#############################################################################################


class HousingStage:
    def __init__(self, ef_country):
        self.loader_class = Loader(ef_country)
        self.energy_class = Energy(ef_country)

    def percent_indoors(self, animal):
        hours = 24
        return (animal.t_indoors + animal.t_stabled) / hours

    def volatile_solids_excretion_rate_HOUSED(self, animal):
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
        DEC = self.loader_class.concentrates.get_con_digestible_energy(
            animal.con_type
        )  # Digestibility of concentrate
        UE = 0.04
        ASH = 0.08
        DMD = self.loader_class.grass.get_forage_dry_matter_digestibility(animal.forage)
        GEC = self.energy_class.gross_energy_from_concentrate(animal)
        GEG = self.energy_class.gross_energy_from_grass(animal)
        IN = self.percent_indoors(animal)

        return (
            (((GEC * (1 - (DEC / 100))) + (UE * GEC)) * ((1 - ASH) / 18.45))
            + ((GEG * (1 - (DMD / 100)) + (UE * GEG)) * ((1 - ASH) / 18.45))
        ) * IN

    def net_excretion_HOUSED(self, animal):
        """
        This function returns kg of nitrogen excreted per year while animals are housed

        - this function is a produces a rate that is a little higher than the costa rica model,
        however, this is likley due to the higher energy ratios resulting from the use of IPCC equations.
        """

        CP = self.loader_class.concentrates.get_con_crude_protein(
            animal.con_type
        )  # crude protein percentage (N contained in crude protein), apparently, 16% is the average N content; https://www.feedipedia.org/node/8329
        FCP = self.loader_class.grass.get_crude_protein(animal.forage)
        GEC = self.energy_class.gross_energy_from_concentrate(animal)
        GEG = self.energy_class.gross_energy_from_grass(animal)
        IN = self.percent_indoors(animal)

        N_retention = {
            "dairy_cows": self.loader_class.animal_features.get_dairy_cows_n_retention(),
            "suckler_cows": self.loader_class.animal_features.get_suckler_cows_n_retention(),
            "bulls": self.loader_class.animal_features.get_bulls_n_retention(),
            "DxD_calves_m": self.loader_class.animal_features.get_DxD_calves_m_n_retention(),
            "DxD_calves_f": self.loader_class.animal_features.get_DxD_calves_f_n_retention(),
            "DxB_calves_m": self.loader_class.animal_features.get_DxB_calves_m_n_retention(),
            "DxB_calves_f": self.loader_class.animal_features.get_DxB_calves_f_n_retention(),
            "BxB_calves_m": self.loader_class.animal_features.get_BxB_calves_m_n_retention(),
            "BxB_calves_f": self.loader_class.animal_features.get_BxB_calves_f_n_retention(),
            "DxD_heifers_less_2_yr": self.loader_class.animal_features.get_DxD_heifers_less_2_yr_n_retention(),
            "DxD_steers_less_2_yr": self.loader_class.animal_features.get_DxD_steers_less_2_yr_n_retention(),
            "DxB_heifers_less_2_yr": self.loader_class.animal_features.get_DxB_heifers_less_2_yr_n_retention(),
            "DxB_steers_less_2_yr": self.loader_class.animal_features.get_DxB_steers_less_2_yr_n_retention(),
            "BxB_heifers_less_2_yr": self.loader_class.animal_features.get_BxB_heifers_less_2_yr_n_retention(),
            "BxB_steers_less_2_yr": self.loader_class.animal_features.get_BxB_steers_less_2_yr_n_retention(),
            "DxD_heifers_more_2_yr": self.loader_class.animal_features.get_DxD_heifers_more_2_yr_n_retention(),
            "DxD_steers_more_2_yr": self.loader_class.animal_features.get_DxD_steers_more_2_yr_n_retention(),
            "DxB_heifers_more_2_yr": self.loader_class.animal_features.get_DxB_heifers_more_2_yr_n_retention(),
            "DxB_steers_more_2_yr": self.loader_class.animal_features.get_DxB_steers_more_2_yr_n_retention(),
            "BxB_heifers_more_2_yr": self.loader_class.animal_features.get_BxB_heifers_more_2_yr_n_retention(),
            "BxB_steers_more_2_yr": self.loader_class.animal_features.get_BxB_steers_more_2_yr_n_retention(),
        }

        N_retention_fraction = N_retention.get(animal.cohort)

        return (
            ((((GEC * 365) / 18.45) * ((CP / 100) / 6.25)) * (1 - N_retention_fraction))
            + ((((GEG * 365) / 18.45) * ((FCP / 100) / 6.25)) * (1 - 0.02))
        ) * IN

    def total_ammonia_nitrogen_nh4_HOUSED(self, animal):
        """
        This function returns the total ammonia nitrate (TAN) NH4 per year
        """
        percentage_nex = 0.6

        return self.net_excretion_HOUSED(animal) * percentage_nex

    def nh3_emissions_per_year_HOUSED(self, animal):
        """
        This function returns the total nh3 emissions per year for housing
        """

        # N-NH3 per year
        # TAN
        storage_TAN = {
            "tank solid": self.loader_class.emissions_factors.get_ef_TAN_house_liquid(),
            "tank liquid": self.loader_class.emissions_factors.get_ef_TAN_house_liquid(),
            "solid": self.loader_class.emissions_factors.get_ef_TAN_house_solid(),
            "biodigester": self.loader_class.emissions_factors.get_ef_TAN_storage_tank(),
        }

        return (
            self.total_ammonia_nitrogen_nh4_HOUSED(animal)
            * storage_TAN[animal.mm_storage]
        )

    def HOUSING_N2O_indirect(self, animal):
        """
        this function returns the indirect emissions from the housing Stage
        """
        ef = (
            self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water()
        )

        indirect_n2o = self.nh3_emissions_per_year_HOUSED(animal) * ef

        return indirect_n2o


#############################################################################################
# Storage Stage
#############################################################################################


class StorageStage:
    def __init__(self, ef_country):
        self.loader_class = Loader(ef_country)
        self.housing_class = HousingStage(ef_country)

    def net_excretion_STORAGE(self, animal):
        """
        This function returns kg of Nex per year from storage
        """

        return self.housing_class.net_excretion_HOUSED(
            animal
        ) - self.housing_class.nh3_emissions_per_year_HOUSED(animal)

    def total_ammonia_nitrogen_nh4_STORAGE(self, animal):
        """
        this function returns the total ammonia nitrogen (TAN) NH4 per year
        """
        percentage_nex = 0.6

        return self.net_excretion_STORAGE(animal) * percentage_nex

    def CH4_STORAGE(self, animal):
        storage_MCF = {
            "tank solid": self.loader_class.emissions_factors.get_ef_mcf_liquid_tank(),
            "tank liquid": self.loader_class.emissions_factors.get_ef_mcf_liquid_tank(),
            "solid": self.loader_class.emissions_factors.get_ef_mcf_solid_storage(),
            "biodigester": self.loader_class.emissions_factors.get_ef_mcf_anaerobic_digestion(),
        }

        return (
            self.housing_class.volatile_solids_excretion_rate_HOUSED(animal) * 365
        ) * (0.1 * 0.67 * storage_MCF[animal.mm_storage])

    def STORAGE_N2O_direct(self, animal):
        """
        This functions returns direct N2O emissions from manure storage
        """

        storage_N2O = {
            "tank solid": self.loader_class.emissions_factors.get_ef_n2o_direct_storage_tank_solid(),  # crust cover for ireland
            "tank liquid": self.loader_class.emissions_factors.get_ef_n2o_direct_storage_tank_liquid(),
            "solid": self.loader_class.emissions_factors.get_ef_n2o_direct_storage_solid(),
            "biodigester": self.loader_class.emissions_factors.get_ef_n2o_direct_storage_tank_anaerobic_digestion(),
        }

        return self.net_excretion_STORAGE(animal) * storage_N2O[animal.mm_storage]

    def nh3_emissions_per_year_STORAGE(self, animal):
        """
        This function returns the total nh3 emissions per year for storage
        """

        storage_TAN = {
            "tank solid": self.loader_class.emissions_factors.get_ef_TAN_storage_tank(),
            "tank liquid": self.loader_class.emissions_factors.get_ef_TAN_storage_tank(),
            "solid": self.loader_class.emissions_factors.get_ef_TAN_storage_solid(),
            "biodigester": self.loader_class.emissions_factors.get_ef_TAN_storage_tank(),
        }

        return (
            self.total_ammonia_nitrogen_nh4_STORAGE(animal)
            * storage_TAN[animal.mm_storage]
        )

    def STORAGE_N2O_indirect(self, animal):
        """
        This functions returns indirect n2o from atmospheric deposition and leaching related to storage
        """

        atmospheric_deposition = {
            "dairy_cows": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "suckler_cows": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "bulls": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "DxD_calves_m": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "DxD_calves_f": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "DxB_calves_m": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "DxB_calves_f": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "BxB_calves_m": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "BxB_calves_f": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "DxD_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "DxD_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "DxB_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "DxB_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "BxB_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "BxB_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "DxD_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "DxD_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "DxB_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "DxB_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "BxB_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "BxB_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        }

        indirect_atmosphere = atmospheric_deposition.get(animal.cohort)

        NH3 = self.nh3_emissions_per_year_STORAGE(animal)

        return NH3 * indirect_atmosphere


###############################################################################
# Daily Spread
###############################################################################


class DailySpread:
    def __init__(self, ef_country):
        self.loader_class = Loader(ef_country)
        self.storage_class = StorageStage(ef_country)

    def net_excretion_SPREAD(self, animal):
        """
        This function returns Nex from daily spread
        """
        nex_storage = self.storage_class.net_excretion_STORAGE(animal)
        direct_n2o = self.storage_class.STORAGE_N2O_direct(animal)
        nh3_emissions = self.storage_class.nh3_emissions_per_year_STORAGE(animal)
        indirect_n2o = self.storage_class.STORAGE_N2O_indirect(animal)

        return nex_storage - direct_n2o - nh3_emissions - indirect_n2o

    def total_ammonia_nitrogen_nh4_SPREAD(self, animal):
        """
        this function returns the total ammonia nitrogen (TAN) NH4 per year from daily spread
        """
        percentage_nex = 0.6

        return self.net_excretion_SPREAD(animal) * percentage_nex

    def SPREAD_N2O_direct(self, animal):
        """
        This function returns the proportion of N direct emissions from daily spread
        """

        n2o_direct = {
            "dairy_cows": self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils(),
            "suckler_cows": self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils(),
            "bulls": self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils(),
            "DxD_calves_m": self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils(),
            "DxD_calves_f": self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils(),
            "DxB_calves_m": self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils(),
            "DxB_calves_f": self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils(),
            "BxB_calves_m": self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils(),
            "BxB_calves_f": self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils(),
            "DxD_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils(),
            "DxD_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils(),
            "DxB_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils(),
            "DxB_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils(),
            "BxB_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils(),
            "BxB_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils(),
            "DxD_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils(),
            "DxD_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils(),
            "DxB_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils(),
            "DxB_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils(),
            "BxB_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils(),
            "BxB_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils(),
        }

        return self.net_excretion_SPREAD(animal) * n2o_direct.get(animal.cohort)

    def nh3_emissions_per_year_SPREAD(self, animal):
        """
        this function returns nh3 emmissions per year from daily spreading
        """

        nh4 = self.total_ammonia_nitrogen_nh4_SPREAD(animal)

        daily_spreading = {
            "none": self.loader_class.emissions_factors.get_ef_nh3_daily_spreading_none(),
            "manure": self.loader_class.emissions_factors.get_ef_nh3_daily_spreading_manure(),
            "broadcast": self.loader_class.emissions_factors.get_ef_nh3_daily_spreading_broadcast(),
            "injection": self.loader_class.emissions_factors.get_ef_nh3_daily_spreading_injection(),
            "trailing hose": self.loader_class.emissions_factors.get_ef_nh3_daily_spreading_traling_hose(),
        }

        return nh4 * daily_spreading[animal.daily_spreading]

    def leach_nitrogen_SPREAD(self, animal):
        """
        This function returns the proportion of nitrogen leached from spreading

        """

        ten_percent_nex = 0.1

        return self.net_excretion_SPREAD(animal) * ten_percent_nex

    def leach_phospherous_SPREAD(self, animal):
        """
        This function returns the proportion of kg P leach per year *(1.8/5))*0.03

        """

        return (self.net_excretion_SPREAD(animal) * (1.8 / 5)) * 0.03

    def SPREAD_N2O_indirect(self, animal):
        """
        This functions returns indirect n2o from atmospheric deposition and leaching related to daily spread
        """

        atmospheric_deposition = {
            "dairy_cows": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "suckler_cows": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "bulls": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "DxD_calves_m": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "DxD_calves_f": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "DxB_calves_m": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "DxB_calves_f": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "BxB_calves_m": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "BxB_calves_f": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "DxD_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "DxD_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "DxB_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "DxB_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "BxB_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "BxB_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "DxD_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "DxD_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "DxB_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "DxB_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "BxB_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
            "BxB_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(),
        }

        leaching = {
            "dairy_cows": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
            "suckler_cows": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
            "bulls": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
            "DxD_calves_m": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
            "DxD_calves_f": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
            "DxB_calves_m": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
            "DxB_calves_f": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
            "BxB_calves_m": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
            "BxB_calves_f": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
            "DxD_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
            "DxD_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
            "DxB_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
            "DxB_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
            "BxB_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
            "BxB_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
            "DxD_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
            "DxD_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
            "DxB_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
            "DxB_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
            "BxB_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
            "BxB_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(),
        }

        indirect_atmosphere = atmospheric_deposition.get(animal.cohort)
        indirect_leaching = leaching.get(animal.cohort)

        NH3 = self.nh3_emissions_per_year_SPREAD(animal)
        NL = self.leach_nitrogen_SPREAD(animal)

        return (NH3 * indirect_atmosphere) + (NL * indirect_leaching)


###############################################################################
# Farm & Upstream Emissions
###############################################################################


class FertiliserInputs:
    def __init__(self, ef_country):
        self.loader_class = Loader(ef_country)

    def urea_N2O_direct(self, total_urea, total_urea_abated):
        """
        this function returns the total emissions from urea and abated urea applied to soils
        """

        ef_urea = self.loader_class.emissions_factors.get_ef_urea()
        ef_urea_abated = self.loader_class.emissions_factors.get_ef_urea_and_nbpt()

        return (total_urea * ef_urea) + (total_urea_abated * ef_urea_abated)

    def urea_NH3(self, total_urea, total_urea_abated):
        """
        This function returns  the amount of urea and abated urea volatised.
        Below is the original fraction used in the Costa Rica version, however this seems to be incorrect.
        FRAC=0.02 #FracGASF ammoinium-fertilisers [fraction of synthetic fertiliser N that volatilises as NH3 and NOx under different conditions]
        """
        ef_urea = (
            self.loader_class.emissions_factors.get_ef_fracGASF_urea_fertilisers_to_nh3_and_nox()
        )
        ef_urea_abated = (
            self.loader_class.emissions_factors.get_ef_fracGASF_urea_and_nbpt_to_nh3_and_nox()
        )

        return (total_urea * ef_urea) + (total_urea_abated * ef_urea_abated)

    def urea_nleach(self, total_urea, total_urea_abated):
        """
        This function returns  the amount of urea and abated urea leached from soils.

        Below is the original fraction used in the Costa Rica version, however this seems to be incorrect.
        FRAC=0.02 #FracGASF ammoinium-fertilisers [fraction of synthetic fertiliser N that volatilises as NH3 and NOx under different conditions]
        """

        leach = self.loader_class.emissions_factors.get_ef_frac_leach_runoff()

        return (total_urea + total_urea_abated) * leach

    def urea_N2O_indirect(self, total_urea, total_urea_abated):
        """
        this function returns the idirect emissions from urea
        """
        indirect_atmosphere = (
            self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water()
        )
        indirect_leaching = (
            self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff()
        )

        return (self.urea_NH3(total_urea, total_urea_abated) * indirect_atmosphere) + (
            self.urea_nleach(total_urea, total_urea_abated) * indirect_leaching
        )

    def urea_co2(self, total_urea, total_urea_abated):
        """
        returns the total CO2 from urea application
        """

        return ((total_urea + total_urea_abated) * 0.2) * (
            44 / 12
        )  # adjusted to the NIR version of this calculation

    def urea_P_leach(self, total_urea, total_urea_abated):
        """
        this function returns the idirect emissions from urea
        """
        frac_leach = float(self.loader_class.emissions_factors.get_ef_Frac_P_Leach())

        return (total_urea + total_urea_abated) * frac_leach

    # Nitrogen Fertiliser Emissions

    def n_fertiliser_P_leach(self, total_n_fert):
        """
        this function returns the idirect emissions from urea
        """
        frac_leach = float(self.loader_class.emissions_factors.get_ef_Frac_P_Leach())

        return total_n_fert * frac_leach

    def n_fertiliser_direct(self, total_n_fert):
        """
        This function returns total direct emissions from ammonium nitrate application at field level
        """
        ef = self.loader_class.emissions_factors.get_ef_ammonium_nitrate()
        return total_n_fert * ef

    def n_fertiliser_NH3(self, total_n_fert):
        """
        This function returns total NH3 emissions from ammonium nitrate application at field level
        """
        ef = (
            self.loader_class.emissions_factors.get_ef_fracGASF_ammonium_fertilisers_to_nh3_and_nox()
        )
        return total_n_fert * ef

    def n_fertiliser_nleach(self, total_n_fert):
        """
        This function returns total leached emissions from ammonium nitrate application at field level
        """

        ef = self.loader_class.emissions_factors.get_ef_frac_leach_runoff()

        return total_n_fert * ef

    def n_fertiliser_indirect(self, total_n_fert):
        """
        this function returns the indirect emissions from ammonium nitrate fertiliser
        """

        indirect_atmosphere = (
            self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water()
        )
        indirect_leaching = (
            self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff()
        )

        return (self.n_fertiliser_NH3(total_n_fert) * indirect_atmosphere) + (
            self.n_fertiliser_nleach(total_n_fert) * indirect_leaching
        )

    # Fertiliser Application Totals for N20 and CO2

    def total_fertiliser_N20(self, total_urea, total_urea_abated, total_n_fert):
        """
        This function returns the total direct and indirect emissions from urea and ammonium fertilisers
        """

        result = (
            self.urea_N2O_direct(total_urea, total_urea_abated)
            + self.urea_N2O_indirect(total_urea, total_urea_abated)
        ) + (
            self.n_fertiliser_direct(total_n_fert)
            + self.n_fertiliser_indirect(total_n_fert)
        )

        return result

    def p_fertiliser_P_leach(self, total_p_fert):
        """
        this function returns the idirect emissions from urea
        """
        frac_leach = float(self.loader_class.emissions_factors.get_ef_Frac_P_Leach())

        return total_p_fert * frac_leach


################################################################################
# Total Global Warming Potential of whole farms (Upstream Processes & Fossil Fuel Energy)
################################################################################

# Emissions from on Farm Fossil Fuels


class Upstream:
    def __init__(self, ef_country):
        self.loader_class = Loader(ef_country)
        self.cohorts_class = Cohorts()

    def co2_from_concentrate_production(self, animal):
        concentrate_co2 = 0

        for key in animal.__dict__.keys():
            if (
                key in self.cohorts_class.COHORTS
                and animal.__getattribute__(key).pop != 0
            ):
                concentrate_co2 += (
                    animal.__getattribute__(key).con_amount
                    * self.loader_class.concentrates.get_con_co2_e(
                        animal.__getattribute__(key).con_type
                    )
                ) * animal.__getattribute__(key).pop

        return concentrate_co2 * 365

    def diesel_CO2(self, diesel_kg):
        """
        this function returns the direct and indirect upstream CO2 emmisions from diesel
        """

        Diesel_indir = self.loader_class.upstream.get_upstream_kg_co2e(
            "diesel_indirect"
        )
        Diest_dir = self.loader_class.upstream.get_upstream_kg_co2e("diesel_direct")

        return diesel_kg * (Diest_dir + Diesel_indir)

    def elec_CO2(self, elec_kwh):
        """
        this functino returns the upstream CO2 emissions from electricity consumption
        """

        elec_consumption = self.loader_class.upstream.get_upstream_kg_co2e(
            "electricity_consumed"
        )  # based on Norway hydropower
        return elec_kwh * elec_consumption

    # Emissions from upstream fertiliser production
    def fert_upstream_CO2(
        self, total_n_fert, total_urea, total_urea_abated, total_p_fert, total_k_fert
    ):
        """
        this function returns the upstream emissions from urea and ammonium fertiliser manufature
        """
        AN_fert_CO2 = self.loader_class.upstream.get_upstream_kg_co2e(
            "ammonium_nitrate_fertiliser"
        )  # Ammonium Nitrate Fertiliser
        Urea_fert_CO2 = self.loader_class.upstream.get_upstream_kg_co2e("urea_fert")
        Triple_superphosphate = self.loader_class.upstream.get_upstream_kg_co2e(
            "triple_superphosphate"
        )
        Potassium_chloride = self.loader_class.upstream.get_upstream_kg_co2e(
            "potassium_chloride"
        )

        return (
            (total_n_fert * AN_fert_CO2)
            + (total_urea * Urea_fert_CO2)
            + (total_urea_abated * Urea_fert_CO2)
            + (total_p_fert * Triple_superphosphate)
            + (total_k_fert * Potassium_chloride)
        )

    def fert_upstream_EP(
        self, total_n_fert, total_urea, total_urea_abated, total_p_fert, total_k_fert
    ):
        """
        this function returns the upstream emissions from urea and ammonium fertiliser manufature
        """
        AN_fert_PO4 = self.loader_class.upstream.get_upstream_kg_po4e(
            "ammonium_nitrate_fertiliser"
        )  # Ammonium Nitrate Fertiliser
        Urea_fert_PO4 = self.loader_class.upstream.get_upstream_kg_po4e("urea_fert")
        Triple_superphosphate = self.loader_class.upstream.get_upstream_kg_po4e(
            "triple_superphosphate"
        )
        Potassium_chloride = self.loader_class.upstream.get_upstream_kg_po4e(
            "potassium_chloride"
        )

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
class Allocation:
    def live_weight_output(self, animal):
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
            + (
                animal.DxD_heifers_less_2_yr.weight
                * animal.DxD_heifers_less_2_yr.n_sold
            )
            + (animal.DxD_steers_less_2_yr.weight * animal.DxD_steers_less_2_yr.n_sold)
            + (
                animal.DxB_heifers_less_2_yr.weight
                * animal.DxB_heifers_less_2_yr.n_sold
            )
            + (animal.DxB_steers_less_2_yr.weight * animal.DxB_steers_less_2_yr.n_sold)
            + (
                animal.BxB_heifers_less_2_yr.weight
                * animal.BxB_heifers_less_2_yr.n_sold
            )
            + (animal.BxB_steers_less_2_yr.weight * animal.BxB_steers_less_2_yr.n_sold)
            + (
                animal.DxD_heifers_more_2_yr.weight
                * animal.DxD_heifers_more_2_yr.n_sold
            )
            + (animal.DxD_steers_more_2_yr.weight * animal.DxD_steers_more_2_yr.n_sold)
            + (
                animal.DxB_heifers_more_2_yr.weight
                * animal.DxB_heifers_more_2_yr.n_sold
            )
            + (animal.DxB_steers_more_2_yr.weight * animal.DxB_steers_more_2_yr.n_sold)
            + (
                animal.BxB_heifers_more_2_yr.weight
                * animal.BxB_heifers_more_2_yr.n_sold
            )
            + (animal.BxB_steers_more_2_yr.weight * animal.BxB_steers_more_2_yr.n_sold)
        )

    def live_weight_bought(self, animal):
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
            + (
                animal.DxD_heifers_less_2_yr.weight
                * animal.DxD_heifers_less_2_yr.n_bought
            )
            + (
                animal.DxD_steers_less_2_yr.weight
                * animal.DxD_steers_less_2_yr.n_bought
            )
            + (
                animal.DxB_heifers_less_2_yr.weight
                * animal.DxB_heifers_less_2_yr.n_bought
            )
            + (
                animal.DxB_steers_less_2_yr.weight
                * animal.DxB_steers_less_2_yr.n_bought
            )
            + (
                animal.BxB_heifers_less_2_yr.weight
                * animal.BxB_heifers_less_2_yr.n_bought
            )
            + (
                animal.BxB_steers_less_2_yr.weight
                * animal.BxB_steers_less_2_yr.n_bought
            )
            + (
                animal.DxD_heifers_more_2_yr.weight
                * animal.DxD_heifers_more_2_yr.n_bought
            )
            + (
                animal.DxD_steers_more_2_yr.weight
                * animal.DxD_steers_more_2_yr.n_bought
            )
            + (
                animal.DxB_heifers_more_2_yr.weight
                * animal.DxB_heifers_more_2_yr.n_bought
            )
            + (
                animal.DxB_steers_more_2_yr.weight
                * animal.DxB_steers_more_2_yr.n_bought
            )
            + (
                animal.BxB_heifers_more_2_yr.weight
                * animal.BxB_heifers_more_2_yr.n_bought
            )
            + (
                animal.BxB_steers_more_2_yr.weight
                * animal.BxB_steers_more_2_yr.n_bought
            )
        )

    def live_weight_to_mje(self, animal):
        converstion_MJe = 12.36
        return self.live_weight_output(animal) * converstion_MJe

    def milk_to_kg_output(self, animal):
        # kg of milk
        kg_conversion = 1.033
        year = 365
        return (
            animal.dairy_cows.daily_milk * animal.dairy_cows.pop * year * kg_conversion
        )

    def milk_to_mje(self, animal):
        converstion_MJe = 2.5
        return self.milk_to_kg_output(animal) * converstion_MJe

    def milk_allocation_factor(self, animal):
        total = self.milk_to_mje(animal) + self.live_weight_to_mje(animal)
        return self.milk_to_mje(animal) / total

    def meat_allocation_factor(self, animal):
        return 1 - self.milk_allocation_factor(animal)


################################################################################
# Totals
################################################################################


class ClimateChangeTotals:
    def __init__(self, ef_country):
        self.cohorts_class = Cohorts()
        self.grass_feed_class = GrassFeed(ef_country)
        self.grazing_class = GrazingStage(ef_country)
        self.spread_class = DailySpread(ef_country)
        self.housing_class = HousingStage(ef_country)
        self.storage_class = StorageStage(ef_country)
        self.fertiliser_class = FertiliserInputs(ef_country)
        self.upstream_class = Upstream(ef_country)

    def Enteric_CH4(self, animal):
        return self.grass_feed_class.ch4_emissions_factor(animal)

    def CH4_enteric_ch4(self, animal):
        result = 0
        for key in animal.__dict__.keys():
            if (
                key in self.cohorts_class.COHORTS
                and animal.__getattribute__(key).pop != 0
            ):
                result += (
                    self.Enteric_CH4(animal.__getattribute__(key))
                    * animal.__getattribute__(key).pop
                )

        return result

    def CH4_manure_management(self, animal):
        result = 0

        for key in animal.__dict__.keys():
            if (
                key in self.cohorts_class.COHORTS
                and animal.__getattribute__(key).pop != 0
            ):
                result += (
                    self.Total_manure_ch4(animal.__getattribute__(key))
                    * animal.__getattribute__(key).pop
                )

        return result

    def PRP_Total(self, animal):
        """
        this function returns the emissions total (N20-N) related to Pasture, Range and Paddock
        """
        mole_weight = 44 / 28

        return (
            self.grazing_class.PRP_N2O_direct(animal)
            + self.grazing_class.PRP_N2O_indirect(animal)
        ) * mole_weight

    def Total_N2O_Spreading(self, animal):
        """
        This function returns the total N20 related to manure storage and spreading
        """
        mole_weight = 44 / 28

        Spreading = 0

        for key in animal.__dict__.keys():
            if (
                key in self.cohorts_class.COHORTS
                and animal.__getattribute__(key).pop != 0
            ):
                Spreading += (
                    self.spread_class.SPREAD_N2O_direct(animal.__getattribute__(key))
                    + self.spread_class.SPREAD_N2O_indirect(
                        animal.__getattribute__(key)
                    )
                    * animal.__getattribute__(key).pop
                )

        return Spreading * mole_weight

    def Total_storage_N2O(self, animal):
        """
        This function returns the total N20 related to manure storage
        """

        mole_weight = 44 / 28

        n2o_direct = 0
        n2o_indirect_storage = 0
        n2o_indirect_housing = 0

        for key in animal.__dict__.keys():
            if (
                key in self.cohorts_class.COHORTS
                and animal.__getattribute__(key).pop != 0
            ):
                n2o_direct += (
                    self.storage_class.STORAGE_N2O_direct(animal.__getattribute__(key))
                    * animal.__getattribute__(key).pop
                )
                n2o_indirect_storage += (
                    self.storage_class.STORAGE_N2O_indirect(
                        animal.__getattribute__(key)
                    )
                    * animal.__getattribute__(key).pop
                )
                n2o_indirect_housing += (
                    self.housing_class.HOUSING_N2O_indirect(
                        animal.__getattribute__(key)
                    )
                    * animal.__getattribute__(key).pop
                )

        return (n2o_direct + n2o_indirect_storage + n2o_indirect_housing) * mole_weight

    def N2O_total_PRP_N2O_direct(self, animal):
        """
        this function returns the direct n2o emissions from pasture, range and paddock
        """

        mole_weight = 44 / 28

        PRP_direct = 0

        for key in animal.__dict__.keys():
            if (
                key in self.cohorts_class.COHORTS
                and animal.__getattribute__(key).pop != 0
            ):
                PRP_direct += (
                    self.grazing_class.PRP_N2O_direct(animal.__getattribute__(key))
                    * animal.__getattribute__(key).pop
                )

        return PRP_direct * mole_weight

    def N2O_total_PRP_N2O_indirect(self, animal):
        mole_weight = 44 / 28

        PRP_indirect = 0

        for key in animal.__dict__.keys():
            if (
                key in self.cohorts_class.COHORTS
                and animal.__getattribute__(key).pop != 0
            ):
                PRP_indirect += (
                    self.grazing_class.PRP_N2O_indirect(animal.__getattribute__(key))
                    * animal.__getattribute__(key).pop
                )

        return PRP_indirect * mole_weight

    def Total_manure_ch4(self, animal):
        """
        this function returns the total ch4 related to manure storage
        """

        return self.grazing_class.ch4_emissions_for_grazing(
            animal
        ) + self.storage_class.CH4_STORAGE(animal)

    def CO2_soils_GWP(self, total_urea, total_urea_abated):
        return self.fertiliser_class.urea_co2(total_urea, total_urea_abated)

    def N2O_direct_fertiliser(self, total_urea, total_urea_abated, total_n_fert):
        """
        This function returns the total direct and indirect emissions from urea and ammonium fertilisers
        """

        mole_weight = 44 / 28

        result = (
            self.fertiliser_class.urea_N2O_direct(total_urea, total_urea_abated)
            + self.fertiliser_class.n_fertiliser_direct(total_n_fert)
        ) * mole_weight

        return result

    def N2O_fertiliser_indirect(self, total_urea, total_urea_abated, total_n_fert):
        mole_weight = 44 / 28

        Fertilizer_indirect = (
            self.fertiliser_class.n_fertiliser_indirect(total_n_fert)
            + self.fertiliser_class.urea_N2O_indirect(total_urea, total_urea_abated)
        ) * mole_weight

        return Fertilizer_indirect

    def upstream_and_inputs_and_fuel_co2(
        self,
        diesel_kg,
        elec_kwh,
        total_n_fert,
        total_urea,
        total_urea_abated,
        total_p_fert,
        total_k_fert,
        animal,
    ):
        return (
            self.upstream_class.diesel_CO2(diesel_kg)
            + self.upstream_class.elec_CO2(elec_kwh)
            + self.upstream_class.fert_upstream_CO2(
                total_n_fert,
                total_urea,
                total_urea_abated,
                total_p_fert,
                total_k_fert,
            )
            + self.upstream_class.co2_from_concentrate_production(animal)
        )


###############################################################################
# Water Quality EP PO4e
###############################################################################


class EutrophicationTotals:
    def __init__(self, ef_country):
        self.loader_class = Loader(ef_country)
        self.cohorts_class = Cohorts()
        self.grazing_class = GrazingStage(ef_country)
        self.housing_class = HousingStage(ef_country)
        self.storage_class = StorageStage(ef_country)
        self.spread_class = DailySpread(ef_country)
        self.fertiliser_class = FertiliserInputs(ef_country)

    # Manure Management
    def total_manure_NH3_EP(self, animal):
        """
        Convert N to PO4  = 0.42

        """

        indirect_atmosphere = (
            self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water()
        )

        NH3N = 0

        for key in animal.__dict__.keys():
            if (
                key in self.cohorts_class.COHORTS
                and animal.__getattribute__(key).pop != 0
            ):
                NH3N += (
                    self.storage_class.nh3_emissions_per_year_STORAGE(
                        animal.__getattribute__(key)
                    )
                    + self.housing_class.nh3_emissions_per_year_HOUSED(
                        animal.__getattribute__(key)
                    )
                ) * animal.__getattribute__(key).pop

        return (NH3N * indirect_atmosphere) * 0.42

    # SOILS
    def total_fertiliser_soils_NH3_and_LEACH_EP(
        self, total_urea, total_urea_abated, total_n_fert
    ):
        """
        Convert N to PO4  = 0.42

        """
        indirect_atmosphere = (
            self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water()
        )

        NH3N = self.fertiliser_class.urea_NH3(
            total_urea, total_urea_abated
        ) + self.fertiliser_class.n_fertiliser_NH3(total_n_fert)

        LEACH = self.fertiliser_class.urea_nleach(
            total_urea, total_urea_abated
        ) + self.fertiliser_class.n_fertiliser_nleach(total_n_fert)

        return (NH3N * indirect_atmosphere) + LEACH * 0.42

    def total_grazing_soils_NH3_and_LEACH_EP(self, animal):
        """
        Convert N to PO4  = 0.42

        """
        indirect_atmosphere = (
            self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water()
        )

        NH3N = 0

        LEACH = 0

        for key in animal.__dict__.keys():
            if (
                key in self.cohorts_class.COHORTS
                and animal.__getattribute__(key).pop != 0
            ):
                NH3N += (
                    self.grazing_class.nh3_emissions_per_year_GRAZING(
                        animal.__getattribute__(key)
                    )
                    + self.spread_class.nh3_emissions_per_year_SPREAD(
                        animal.__getattribute__(key)
                    )
                ) * animal.__getattribute__(key).pop

                LEACH += (
                    self.grazing_class.Nleach_GRAZING(animal.__getattribute__(key))
                    + self.spread_class.leach_nitrogen_SPREAD(
                        animal.__getattribute__(key)
                    )
                ) * animal.__getattribute__(key).pop

        return (NH3N * indirect_atmosphere) + LEACH * 0.42

    def fertiliser_soils_P_LEACH_EP(
        self, total_urea, total_urea_abated, total_n_fert, total_p_fert
    ):
        PLEACH = (
            self.fertiliser_class.urea_P_leach(total_urea, total_urea_abated)
            + self.fertiliser_class.n_fertiliser_P_leach(total_n_fert)
            + self.fertiliser_class.p_fertiliser_P_leach(total_p_fert)
        )

        return PLEACH * 3.06

    def grazing_soils_P_LEACH_EP(self, animal):
        PLEACH = 0

        for key in animal.__dict__.keys():
            if (
                key in self.cohorts_class.COHORTS
                and animal.__getattribute__(key).pop != 0
            ):
                PLEACH += (
                    self.spread_class.leach_phospherous_SPREAD(
                        animal.__getattribute__(key)
                    )
                    + self.grazing_class.PLeach_GRAZING(animal.__getattribute__(key))
                ) * animal.__getattribute__(key).pop

        return PLEACH * 3.06

    def total_fertilser_soils_EP(
        self,
        total_urea,
        total_urea_abated,
        total_n_fert,
        total_p_fert,
    ):
        return self.total_fertiliser_soils_NH3_and_LEACH_EP(
            total_urea, total_urea_abated, total_n_fert
        ) + self.fertiliser_soils_P_LEACH_EP(
            total_urea, total_urea_abated, total_n_fert, total_p_fert
        )

    def total_grazing_soils_EP(self, animal):
        return self.total_grazing_soils_NH3_and_LEACH_EP(
            self, animal
        ) + self.grazing_soils_P_LEACH_EP(animal)

    # Imported Feeds
    def EP_from_concentrate_production(self, animal):
        concentrate_p = 0

        for key in animal.__dict__.keys():
            if (
                key in self.cohorts_class.COHORTS
                and animal.__getattribute__(key).pop != 0
            ):
                concentrate_p += (
                    animal.__getattribute__(key).con_amount
                    * self.loader_class.concentrates.get_con_po4_e(
                        animal.__getattribute__(key).con_type
                    )
                ) * animal.__getattribute__(key).pop

        return concentrate_p * 365


###############################################################################
# Air Quality Ammonia
###############################################################################


class AirQualityTotals:
    def __init__(self, ef_country):
        self.loader_class = Loader(ef_country)
        self.cohorts_class = Cohorts()
        self.grazing_class = GrazingStage(ef_country)
        self.housing_class = HousingStage(ef_country)
        self.storage_class = StorageStage(ef_country)
        self.spread_class = DailySpread(ef_country)
        self.fertiliser_class = FertiliserInputs(ef_country)
        self.upstream_class = Upstream(ef_country)

    # Manure Management
    def total_manure_NH3_AQ(self, animal):
        NH3N = 0

        for key in animal.__dict__.keys():
            if (
                key in self.cohorts_class.COHORTS
                and animal.__getattribute__(key).pop != 0
            ):
                NH3N += (
                    self.storage_class.nh3_emissions_per_year_STORAGE(
                        animal.__getattribute__(key)
                    )
                    + self.housing_class.nh3_emissions_per_year_HOUSED(
                        animal.__getattribute__(key)
                    )
                ) * animal.__getattribute__(key).pop

        return NH3N

    # SOILS
    def total_fertiliser_soils_NH3_AQ(
        self, total_urea, total_urea_abated, total_n_fert
    ):
        NH3N = self.fertiliser_class.urea_NH3(
            total_urea, total_urea_abated
        ) + self.fertiliser_class.n_fertiliser_NH3(total_n_fert)

        return NH3N

    def total_grazing_soils_NH3_AQ(self, animal):
        NH3N = 0

        for key in animal.__dict__.keys():
            if (
                key in self.cohorts_class.COHORTS
                and animal.__getattribute__(key).pop != 0
            ):
                NH3N += (
                    self.grazing_class.nh3_emissions_per_year_GRAZING(
                        animal.__getattribute__(key)
                    )
                    + self.spread_class.nh3_emissions_per_year_SPREAD(
                        animal.__getattribute__(key)
                    )
                ) * animal.__getattribute__(key).pop

        return NH3N
