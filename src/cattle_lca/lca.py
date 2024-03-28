"""
Cattle LCA Module
------------------

This module contains classes and methods for calculating the environmental impact of cattle farming, including energy requirements,
emissions, and waste management. It covers various stages of cattle lifecycle and farm operations such as grazing, housing, manure management, and fertilization practices. The module aims to provide a comprehensive assessment tool for understanding and reducing the environmental footprint associated with cattle production.

The module includes detailed assessments of greenhouse gas emissions, eutrophication potential, air quality impacts, and resource usage to support sustainable farming practices and decision-making. By integrating data from various sources and applying region-specific emission factors, the module helps in evaluating the overall environmental performance of cattle farms.

Key Features:
- Calculation of energy consumption and efficiency in cattle farming.
- Estimation of greenhouse gas emissions from enteric fermentation, manure management, and other farm activities.
- Assessment of nutrient runoff and its impact on eutrophication.
- Evaluation of ammonia emissions and their contribution to air quality issues.
- Analysis of upstream impacts related to feed production, fertilizer use, and other inputs.

"""

from cattle_lca.resource_manager.cattle_lca_data_manager import LCADataManager
import copy

class Energy:
    """
    Represents the calculations for various energy needs and intakes for animals based on their cohort,
    diet, and physiological state. It utilizes a series of equations from the IPCC 2006 guidelines and other
    resources to estimate the energy required for maintenance, growth, lactation, and pregnancy, as well as
    the energy provided by forage and concentrates.

    Attributes:
        data_manager_class (LCADataManager): An instance of LCADataManager initialized with a specific ef_country,
                                             used to access various parameters and energy factors needed for calculations.

    Methods:
        ratio_of_net_energy_maintenance(animal): Calculates the ratio of net energy available for maintenance.
        ratio_of_net_energy_growth(animal): Calculates the ratio of net energy available for growth.
        net_energy_for_maintenance(animal): Calculates the net energy required for maintaining basic physiological functions.
        net_energy_for_activity(animal): Calculates the additional net energy required for animal activities based on grazing type.
        net_energy_for_weight_gain(animal): Calculates the net energy required for animal growth.
        net_energy_for_lactation(animal): Calculates the net energy required for lactation.
        net_energy_for_pregnancy(animal): Calculates the net energy required during pregnancy.
        gross_energy_from_concentrate(animal): Calculates the total gross energy intake from concentrates.
        gross_energy_from_grass(animal): Estimates the total gross energy intake from grasses, adjusted for energy intake from concentrates.
        total_gross_energy(animal): Estimates the total gross energy intake from all sources.

    Note:
        This class requires detailed data about the animal cohorts, their diets, and physiological states to perform accurate calculations.
        These calculations are based on standards provided by IPCC guidelines and other agricultural research sources.

    """
    def __init__(self, ef_country):
        self.data_manager_class = LCADataManager(ef_country)

    def ratio_of_net_energy_maintenance(self, animal):
        """
        Calculates the Ratio of Net Energy Maintenance (REM) to the total digestible energy consumed by the animal.
        This ratio helps in understanding how much of the energy consumed is being used for maintenance activities.
        
        Parameters:
        ----------
        animal : Animal object
            The animal for which the REM is being calculated. The animal object should contain the forage type being consumed.

        Returns:
        -------
        float
            The ratio of net energy available for maintenance compared to the total energy consumed.
        
        Notes:
        -----
        The digestible energy (DE) from the forage type input into the animal and farm data is used to calculate the REM.
        """

        DE = self.data_manager_class.get_forage_digestibility(animal.forage)

        return (
            1.123
            - (4.092 * (10**-3) * DE)
            + (1.126 * (10**-5) * (DE**2))
            - (25.4 / DE)
        )

    def ratio_of_net_energy_growth(self, animal):
        """
        Calculates the Ratio of Net Energy Growth (REG) to the total digestible energy consumed by the animal.
        This ratio is essential for understanding how much of the energy consumed is utilized for growth purposes.

        Parameters:
        ----------
        animal : Animal object
            The animal cohort type from the animal input data.

        Returns:
        -------
        float
            The ratio of net energy available for growth compared to the total energy consumed.

        Notes:
        -----
        The digestible energy (DE) from the forage type input into the animal and farm data is used to calculate the REG.
        """
        DE = self.data_manager_class.get_forage_digestibility(animal.forage)

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
        Calculates the net energy required for maintenance based on the animal's weight.
        This involves activities that include basic physiological functions such as respiration, circulation, and maintaining body temperature.

        Parameters:
        ----------
        animal : Animal object
            The animal for which the energy for maintenance is being calculated.

        Returns:
        -------
        float
            The net energy required for maintenance activities, based on the animal's weight.

        Notes:
        -----
        This calculation follows equation 10.3 from the IPCC 2006 guidelines (NEm).
        """

        cfi = self.data_manager_class.get_cohort_parameter(animal.cohort, "coefficient")()

        return cfi * (animal.weight**0.75)

    def net_energy_for_activity(self, animal):
        """
        Calculates the net energy required for activities, based on the type of feeding situation (grazing type).
        This includes the energy required for movements and other physical activities other than those for basic maintenance.

        Parameters:
        ----------
        animal : Animal object
            The animal for which the energy for activity is being calculated.

        Returns:
        -------
        float
            The net energy required for activities.

        Notes:
        -----
        This uses the net energy for maintenance, multiplied by the coefficient for the animal's specific feed situation.
        """
        return self.data_manager_class.get_grazing_type(animal.grazing)() * self.net_energy_for_maintenance(animal)

    def net_energy_for_weight_gain(self, animal):
        """
        Calculates the net energy required for weight gain, tailored to the animal's specific weight gain rate and physiological state.

        Parameters:
        ----------
        animal : Animal object
            The animal for which the energy for weight gain is being calculated.

        Returns:
        -------
        float
            The net energy required for weight gain.

        Notes:
        -----
        Utilizes equation 10.6 from the IPCC 2006 guidelines (NEg) and is parameterized to the animal's daily weight gain.
        """
        gain = self.data_manager_class.get_cohort_parameter(animal.cohort, "weight_gain")()
        coef = self.data_manager_class.get_cohort_parameter(animal.cohort, "growth")()
        mature_weight = self.data_manager_class.get_cohort_parameter(animal.cohort, "mature_weight")()
        
        return (
            22.02
            * ((animal.weight / (coef * mature_weight)) ** 0.75)
            * (gain**1.097)
        )
    

    def net_energy_for_lactation(self, animal):
        """
        Calculates the energy required for lactation, considering the milk volume and fat content.

        Parameters:
        ----------
        animal : Animal object
            The lactating animal for which the energy for lactation is being calculated.

        Returns:
        -------
        float
            The net energy required for producing milk.

        Notes:
        -----
        Factors in milk density and fat content to compute the required energy for milk production.
        """
        milk = animal.daily_milk * self.data_manager_class.get_milk_density()
        fat = self.data_manager_class.get_fat()
        return milk * (1.47 + 0.40 * fat)

    def net_energy_for_pregnancy(self, animal):
        """
        Calculates the energy required for pregnancy.

        Parameters:
        ----------
        animal : Animal object
            The pregnant animal for which the energy for pregnancy is being calculated.

        Returns:
        -------
        float
            The net energy required for supporting pregnancy.

        Notes:
        -----
        Based on the net energy for maintenance and modified by the emissions factor for pregnancy.
        """
        coef = self.data_manager_class.get_cohort_parameter(animal.cohort, "pregnancy")
        if coef is None:
            nep = 0
        else:
            nep = coef() * self.net_energy_for_maintenance(animal)

        return nep


    def gross_energy_from_concentrate(self, animal):
        """
        Calculates the total gross energy intake from concentrate feeds consumed by the animal.

        Parameters:
        ----------
        animal : Animal object
            The animal for which the energy intake from concentrates is being calculated.

        Returns:
        -------
        float
            The total gross energy intake from concentrates.

        Notes:
        -----
        Accounts for the digestibility and energy content of the concentrate feed type consumed.
        """
        dm = self.data_manager_class.get_concentrate_digestibility(
            animal.con_type
        )
        mj = self.data_manager_class.get_con_dry_matter_gross_energy(
            animal.con_type
        )

        return (animal.con_amount * dm / 100) * mj

    def gross_energy_from_grass(self, animal):
        """
        Estimates the total gross energy intake from grasses for an animal, after accounting for energy contributions 
        from different physiological needs and adjusted for the energy concentrates.

        Parameters:
        ----------
        animal : Animal object
            The animal for which the gross energy intake from grasses is being estimated.

        Returns:
        -------
        float
            The total gross energy intake from grasses, adjusted for the energy already provided by concentrates.

        Notes:
        -----
        The calculation considers digestible energy from forage, energy for maintenance, activity, lactation, pregnancy, 
        weight gain, and subtracts the energy intake from concentrates.
        """

        DMD = self.data_manager_class.get_forage_digestibility(animal.forage)

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
        Calculates the total gross energy intake for an animal, encompassing all sources of energy including grass and concentrates, 
        and accounting for various physiological energy demands.

        Parameters:
        ----------
        animal : Animal object
            The animal for which the total gross energy intake is being estimated.

        Returns:
        -------
        float
            The total gross energy intake, considering all physiological energy needs and sources.

        Notes:
        -----
        This method aggregates the net energy for maintenance, activity, lactation, pregnancy, and weight gain against 
        the backdrop of the animal's diet digestibility and respective energy ratios for maintenance and growth.
        """
        DMD = self.data_manager_class.get_forage_digestibility(animal.forage)

        REM = self.ratio_of_net_energy_maintenance(animal)
        REG = self.ratio_of_net_energy_growth(animal)
        NEM = self.net_energy_for_maintenance(animal)
        NEA = self.net_energy_for_activity(animal)
        NEL = self.net_energy_for_lactation(animal)
        NEP = self.net_energy_for_pregnancy(animal)
        NEG = self.net_energy_for_weight_gain(animal)

        return (((NEM + NEA + NEL + NEP) / REM) + (NEG / REG)) / (DMD / 100.0)


class GrassFeed:
    """
    The GrassFeed class provides methods to calculate various energy-related metrics for animals, specifically focusing on those fed primarily on grass. 
    It takes into account the dry matter intake from grass, the proportion of the diet made up of concentrates, 
    and methane emissions based on the animal's diet.

    Attributes:
    ----------
    energy_class : Energy
        An instance of the Energy class, used to calculate various energy metrics for the animal.
    data_manager_class : LCADataManager
        An instance of the LCADataManager class, used to access data necessary for energy and emissions calculations.

    Methods:
    -------
    dry_matter_from_grass(animal)
        Calculates the dry matter intake from grasses for an animal, adjusted for the energy intake from concentrates.
    gross_amount_from_con_in_percent(animal, share_in_percent)
        Estimates the total energy intake from concentrates, as a percentage of the animal's total diet.
    ch4_emissions_factor(animal)
        Calculates the methane emissions factor based on the feed intake and methane conversion factors.

    """
    def __init__(self, ef_country):
        self.energy_class = Energy(ef_country)
        self.data_manager_class = LCADataManager(ef_country)


    def dry_matter_from_grass(self, animal):
        """
        Estimates the dry matter intake from grasses for an animal, adjusted for the energy intake from concentrates.

        Parameters:
        ----------
        animal : Animal object
            The animal for which the dry matter intake from grass is being estimated.

        Returns:
        -------
        float
            The total dry matter intake from grasses, after adjusting for the energy provided by concentrates and accounting for different physiological energy needs.

        Notes:
        -----
        The calculation considers net energy for maintenance, activity, lactation, pregnancy, weight gain, and the digestible energy from forage. This method ensures a more accurate estimation of the actual dry matter intake from grass for the specified animal.
        """

        DMD = self.data_manager_class.get_forage_digestibility(animal.forage)

        REM = self.energy_class.ratio_of_net_energy_maintenance(animal)
        REG = self.energy_class.ratio_of_net_energy_growth(animal)
        NEM = self.energy_class.net_energy_for_maintenance(animal)
        NEA = self.energy_class.net_energy_for_activity(animal)
        NEL = self.energy_class.net_energy_for_lactation(animal)
        NEP = self.energy_class.net_energy_for_pregnancy(animal)
        NEG = self.energy_class.net_energy_for_weight_gain(animal)
        con = self.energy_class.gross_energy_from_concentrate(animal)
        GE = self.data_manager_class.get_grass_dry_matter_gross_energy(animal.forage)
        dm = self.data_manager_class.get_concentrate_digestibility(
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
        Estimates the total energy intake from concentrates, as a percentage of the animal's total diet, adjusted for the energy intake from grass.

        Parameters:
        ----------
        animal : Animal object
            The animal for which the energy intake from concentrates is being estimated.
        share_in_percent : float
            The percentage of the diet made up by concentrates.

        Returns:
        -------
        float
            The energy intake from concentrates, expressed as a percentage of the total diet.

        Notes:
        -----
        This method provides an estimate of how much energy the animal is obtaining from concentrates as opposed to grass, helping to balance the diet according to physiological energy demands.
        """
        REM = self.energy_class.ratio_of_net_energy_maintenance(animal)
        REG = self.energy_class.ratio_of_net_energy_growth(animal)
        NEM = self.energy_class.net_energy_for_maintenance(animal)
        NEA = self.energy_class.net_energy_for_activity(animal)
        NEL = self.energy_class.net_energy_for_lactation(animal)
        NEP = self.energy_class.net_energy_for_pregnancy(animal)
        NEG = self.energy_class.net_energy_for_weight_gain(animal)
        dm = self.data_manager_class.get_concentrate_digestibility(
            animal.con_type
        )
        DMD = self.data_manager_class.get_forage_digestibility(animal.forage)
        mj_con = self.data_manager_class.get_con_dry_matter_gross_energy(
            animal.con_type
        )
        mj_grass = self.data_manager_class.get_grass_dry_matter_gross_energy(
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
        Calculates the methane emissions factor based on the feed intake, specifically the gross energy from concentrates and grasses, and the methane conversion factor associated with the animal's cohort.

        Parameters:
        ----------
        animal : Animal object
            The animal for which the methane emissions factor is being estimated.

        Returns:
        -------
        float
            The methane emissions factor per animal per year, taking into account the animal's total energy intake from all feed sources.

        """
        year = 365
        Ym = self.data_manager_class.get_cohort_parameter(animal.cohort, "methane_conversion_factor")()

        methane_energy = 55.65  # MJ/kg of CH4

        GEC = self.energy_class.gross_energy_from_concentrate(animal)
        GEG = self.energy_class.gross_energy_from_grass(animal)

        GET = (GEC + GEG) * year

        return GET * (Ym / methane_energy)


#############################################################################################
# Grazing Stage
#############################################################################################


class GrazingStage:
    """
    The GrazingStage class calculates various metrics related to the environmental impact of grazing animals. 
    This includes the volatile solids excretion rate to pasture, net nitrogen excretion, methane emissions from grazing, ammonia emissions, 
    nitrogen and phosphorus leaching, and direct and indirect N2O emissions from pasture.

    Attributes:
    ----------
    energy_class : Energy
        An instance of the Energy class, used for calculations involving energy metrics of animals.
    grass_feed_class : GrassFeed
        An instance of the GrassFeed class, used to calculate energy intake from grasses.
    data_manager_class : LCADataManager
        An instance of the LCADataManager class, used to access data necessary for the calculations.

    Methods:
    -------
    percent_outdoors(animal)
        Calculates the percentage of time an animal spends outdoors based on its time outdoors attribute.
    volatile_solids_excretion_rate_GRAZING(animal)
        Calculates the rate at which volatile solids are excreted to pasture by the animal.
    net_excretion_GRAZING(animal)
        Calculates the net nitrogen excretion per kilogram to pasture by the animal.
    ch4_emissions_for_grazing(animal)
        Estimates the methane emissions from the animal excretion while grazing.
    nh3_emissions_per_year_GRAZING(animal)
        Calculates the total ammonia emissions per year from the animal while grazing.
    Nleach_GRAZING(animal)
        Estimates the amount of nitrogen leached from the pasture due to the grazing animal.
    PLeach_GRAZING(animal)
        Estimates the amount of phosphorus leached from the pasture due to the grazing animal.
    PRP_N2O_direct(animal)
        Calculates the direct nitrous oxide emissions from pasture, range, and paddock due to the grazing animal.
    PRP_N2O_indirect(animal)
        Calculates the indirect nitrous oxide emissions from atmospheric deposition and leaching related to pasture, 
        range, and paddock due to the grazing animal.
    """

    def __init__(self, ef_country):
        self.energy_class = Energy(ef_country)
        self.grass_feed_class = GrassFeed(ef_country)
        self.data_manager_class = LCADataManager(ef_country)

    def percent_outdoors(self, animal):
        """
        Calculates the percentage of the day that the animal spends outdoors.

        Parameters:
        ----------
        animal : object
            The animal object containing relevant data such as time spent outdoors.

        Returns:
        -------
        float
            The percentage of the day the animal spends outdoors.
        """
        hours = 24
        return animal.t_outdoors / hours

    def volatile_solids_excretion_rate_GRAZING(self, animal):
        """
        Calculates the volatile solids excretion rate (kg/day) to pasture for grazing animals. This measure
        is an indicator of the amount of waste produced by the animal that can contribute to
        greenhouse gas emissions.

        Parameters:
        ----------
        animal : object
            The animal object containing relevant dietary and physical information.

        Returns:
        -------
        float
            The volatile solids excretion rate to pasture.
            This function calculates Volitile Solids Excretion Rate (kg/day -1) to pasture

        Notes:
        ------
            GEC   = Gross Energy from Concentrates
            GEG   = Gross Energy from grass
            DE    = Percentage of Digestible Energy
            UE    = Urinary Energy
            ASH   = Ash content of manure
            18.45 = conversion factor for dietary GE per kg of dry matter, MJ kg-1.
        """

        DEC = self.data_manager_class.get_concentrate_digestable_energy(
            animal.con_type
        )  # Digestibility
        UE = 0.04
        ASH = 0.08
        DMD = self.data_manager_class.get_forage_digestibility(animal.forage)
        GEC = self.energy_class.gross_energy_from_concentrate(animal)
        GEG = self.energy_class.gross_energy_from_grass(animal)
        OUT = self.percent_outdoors(animal)

        return (((GEG * (1 - (DMD / 100))) + (UE * GEG)) * ((1 - ASH) / 18.45)) + (
            (GEC * (1 - (DEC / 100)) + (UE * GEC)) * (((1 - ASH) / 18.45))
        ) * OUT

    def net_excretion_GRAZING(self, animal):
        """
        Calculates the net nitrogen excretion (kg/day) per kg to pasture. This is a measure of the nitrogen
        that is excreted by grazing animals and can impact soil and water quality.

        Parameters:
        ----------
        animal : object
            The animal object containing relevant dietary and physical information.

        Returns:
        -------
        float
            The net nitrogen excretion rate to pasture.
        """
        CP = self.data_manager_class.get_concentrate_crude_protein(
            animal.con_type
        )  # crude protein percentage (N contained in crude protein), apparently, 16% is the average N content; https://www.feedipedia.org/node/8329
        FCP = self.data_manager_class.get_grass_crude_protein(animal.forage)
        GEC = self.energy_class.gross_energy_from_concentrate(animal)
        GEG = self.energy_class.gross_energy_from_grass(animal)
        OUT = self.percent_outdoors(animal)


        N_retention_fraction = self.data_manager_class.get_cohort_parameter(animal.cohort, "N_retention")()

        return (
            (((GEC * 365) / 18.45) * ((CP / 100) / 6.25) * (1 - N_retention_fraction))
            + ((((GEG * 365) / 18.45) * (FCP / 100.0) / 6.25) * (1 - 0.02))
        ) * OUT

    def ch4_emissions_for_grazing(self, animal):
        """
        Calculates the methane emissions for grazing based on the animal's excretion rates and time spent
        outdoors.

        Parameters:
        ----------
        animal : object
            The animal object containing relevant dietary, physical, and grazing information.

        Returns:
        -------
        float
            The annual methane emissions from grazing.
        """
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
        Calculates the total ammonia emissions per year from grazing animals. Ammonia emissions contribute
        to air quality issues and can lead to nitrogen deposition in ecosystems.

        Parameters:
        ----------
        animal : object
            The animal object containing relevant dietary and physical information.

        Returns:
        -------
        float
            The total ammonia emissions per year from grazing.
        """
        TAN = self.data_manager_class.get_cohort_parameter(animal.cohort, "total_ammonia_nitrogen")()

        return self.net_excretion_GRAZING(animal) * 0.6 * TAN


    def Nleach_GRAZING(self, animal):
        """
        Calculates the proportion of nitrogen that is leached from pasture as a result of grazing.

        Parameters:
        ----------
        animal : object
            The animal object containing relevant dietary and physical information.

        Returns:
        -------
        float
            The amount of nitrogen leached from pasture due to grazing.
        """
        ten_percent_nex = 0.1

        return self.net_excretion_GRAZING(animal) * ten_percent_nex


    def PLeach_GRAZING(self, animal):
        """
        Calculates the proportion of phosphorus that is leached from pasture as a result of grazing.

        Parameters:
        ----------
        animal : object
            The animal object containing relevant dietary and physical information.

        Returns:
        -------
        float
            The amount of phosphorus leached from pasture due to grazing.
        """
        return (self.net_excretion_GRAZING(animal) * (1.8 / 5)) * 0.03

    # direct and indirect (from leaching) N20 from PRP

    def PRP_N2O_direct(self, animal):
        """
        Returns the direct nitrous oxide (N2O) emissions from pasture, range, and paddock (PRP) as a result
        of animal grazing.

        Parameters:
        ----------
        animal : object
            The animal object containing relevant dietary and physical information.

        Returns:
        -------
        float
            The direct N2O emissions from PRP due to grazing.
        """
        EF = self.data_manager_class.get_cohort_parameter(animal.cohort, "direct_n2o_emissions_factors")()

        return self.net_excretion_GRAZING(animal) * EF

    def PRP_N2O_indirect(self, animal):
        """
        Returns indirect nitrous oxide (N2O) emissions from atmospheric deposition and leaching related to
        pasture, range, and paddock (PRP). These indirect emissions contribute to the overall greenhouse gas
        footprint of grazing practices.

        Parameters:
        ----------
        animal : object
            The animal object containing relevant dietary and physical information.

        Returns:
        -------
        float
            The indirect N2O emissions from PRP due to grazing.
        """
        indirect_atmosphere = self.data_manager_class.get_cohort_parameter(animal.cohort, "atmospheric_deposition")()
        indirect_leaching = self.data_manager_class.get_cohort_parameter(animal.cohort, "leaching")()

        NH3 = self.nh3_emissions_per_year_GRAZING(animal)
        NL = self.Nleach_GRAZING(animal)

        return (NH3 * indirect_atmosphere) + (NL * indirect_leaching)


#############################################################################################
# Housing Stage
#############################################################################################


class HousingStage:
    """
    Represents the housing stage of animals, calculating various emissions and excretion rates
    associated with animals being indoors.

    Attributes:
    ----------
    data_manager_class : LCADataManager
        An instance of LCADataManager to access various data related to livestock and their environmental impacts.
    energy_class : Energy
        An instance of Energy class to access energy-related calculations for livestock.

    Methods:
    -------
    percent_indoors(animal):
        Calculates the percentage of time an animal spends indoors.
    volatile_solids_excretion_rate_HOUSED(animal):
        Calculates the rate of volatile solids excreted by housed animals per day.
    net_excretion_HOUSED(animal):
        Calculates the amount of nitrogen excreted per year by animals while they are housed.
    total_ammonia_nitrogen_nh4_HOUSED(animal):
        Calculates the total ammonia nitrogen excreted per year by housed animals.
    nh3_emissions_per_year_HOUSED(animal):
        Calculates the total ammonia emissions per year from housing.
    HOUSING_N2O_indirect(animal):
        Calculates indirect nitrous oxide emissions from the housing stage.
    """
    def __init__(self, ef_country):
        self.data_manager_class = LCADataManager(ef_country)
        self.energy_class = Energy(ef_country)

    def percent_indoors(self, animal):
        """
        Calculates the percentage of the day that the animal spends indoors including time stabled.

        Parameters:
        ----------
        animal : object
            The animal object containing relevant data such as time spent indoors and stabled.

        Returns:
        -------
        float
            The percentage of the day the animal spends indoors.
        """
        hours = 24
        return (animal.t_indoors + animal.t_stabled) / hours

    def volatile_solids_excretion_rate_HOUSED(self, animal):
        """
        Calculates the rate of volatile solids excreted by housed animals per day, considering the energy
        content of their diet and time spent indoors.

        Parameters:
        ----------
        animal : object
            The animal object containing relevant dietary and housing information.

        Returns:
        -------
        float
            The daily rate of volatile solids excretion for housed animals.

        Notes:
        ------
            Volitile Solids Excretion Rate (kg/day -1)
            GEcon = Gross Energy from Concentrates
            GEgrass = Gross Energy from grass
            DE= Percentage of Digestible Energy
            UE = Urinary Energy
            ASH = Ash content of manure
            18.45 = conversion factor for dietary GE per kg of dry matter, MJ kg-1.
        """
        DEC = self.data_manager_class.get_concentrate_digestable_energy(
            animal.con_type
        )  # Digestibility of concentrate
        UE = 0.04
        ASH = 0.08
        DMD = self.data_manager_class.get_forage_digestibility(animal.forage)
        GEC = self.energy_class.gross_energy_from_concentrate(animal)
        GEG = self.energy_class.gross_energy_from_grass(animal)
        IN = self.percent_indoors(animal)

        return (
            (((GEC * (1 - (DEC / 100))) + (UE * GEC)) * ((1 - ASH) / 18.45))
            + ((GEG * (1 - (DMD / 100)) + (UE * GEG)) * ((1 - ASH) / 18.45))
        ) * IN

    def net_excretion_HOUSED(self, animal):
        """
        Calculates the amount of nitrogen excreted per year by animals while they are housed, factoring in
        the protein content of their diet and the time they spend indoors.

        Parameters:
        ----------
        animal : object
            The animal object containing relevant dietary and housing information.

        Returns:
        -------
        float
            The annual amount of nitrogen excreted by housed animals.
        """
        CP = self.data_manager_class.get_concentrate_crude_protein(
            animal.con_type
        )  # crude protein percentage (N contained in crude protein), apparently, 16% is the average N content; https://www.feedipedia.org/node/8329
        FCP = self.data_manager_class.get_grass_crude_protein(animal.forage)
        GEC = self.energy_class.gross_energy_from_concentrate(animal)
        GEG = self.energy_class.gross_energy_from_grass(animal)
        IN = self.percent_indoors(animal)

        N_retention_fraction = self.data_manager_class.get_cohort_parameter(animal.cohort, "N_retention")()

        return (
            ((((GEC * 365) / 18.45) * ((CP / 100) / 6.25)) * (1 - N_retention_fraction))
            + ((((GEG * 365) / 18.45) * ((FCP / 100) / 6.25)) * (1 - 0.02))
        ) * IN
    

    def total_ammonia_nitrogen_nh4_HOUSED(self, animal):
        """
        Calculates the total ammonia nitrogen (TAN NH4) excreted by housed animals.

        Parameters:
        ----------
        animal : object
            The animal object containing relevant excretion information.

        Returns:
        -------
        float
            The total ammonia nitrogen excreted by housed animals.
        """
        percentage_nex = 0.6

        return self.net_excretion_HOUSED(animal) * percentage_nex

    def nh3_emissions_per_year_HOUSED(self, animal):
        """
        Calculates the total ammonia (NH3) emissions per year resulting from animal housing.

        Parameters:
        ----------
        animal : object
            The animal object containing relevant housing and manure management information.

        Returns:
        -------
        float
            The total ammonia emissions per year from animal housing.
        """
        # N-NH3 per year
        # TAN

        return (
            self.total_ammonia_nitrogen_nh4_HOUSED(animal)
            * self.data_manager_class.get_storage_TAN(animal.mm_storage)()
        )

    def HOUSING_N2O_indirect(self, animal):
        """
        Calculates indirect nitrous oxide (N2O) emissions associated with the housing stage of animal
        rearing, considering ammonia emissions and atmospheric deposition.

        Parameters:
        ----------
        animal : object
            The animal object containing relevant housing and emissions information.

        Returns:
        -------
        float
            Indirect N2O emissions resulting from animal housing.
        """
        ef = (
            self.data_manager_class.get_indirect_atmospheric_deposition()
        )

        indirect_n2o = self.nh3_emissions_per_year_HOUSED(animal) * ef

        return indirect_n2o


#############################################################################################
# Storage Stage
#############################################################################################


class StorageStage:
    """
    Represents the manure storage stage of farm management, calculating various emissions and excretion rates
    associated with the storage of animal waste.

    Attributes:
    ----------
    housing_class : HousingStage
        An instance of HousingStage to access calculations related to the housing phase of animal management.
    data_manager_class : LCADataManager
        An instance of LCADataManager to access various data related to livestock and environmental impacts.

    Methods:
    -------
    net_excretion_STORAGE(animal):
        Calculates the net nitrogen excretion from storage.
    total_ammonia_nitrogen_nh4_STORAGE(animal):
        Calculates the total ammonia nitrogen excreted per year from storage.
    CH4_STORAGE(animal):
        Calculates the methane emissions from manure storage per year.
    STORAGE_N2O_direct(animal):
        Calculates direct nitrous oxide emissions from manure storage.
    nh3_emissions_per_year_STORAGE(animal):
        Calculates the total ammonia emissions per year from manure storage.
    STORAGE_N2O_indirect(animal):
        Calculates indirect nitrous oxide emissions from manure storage.
    """
    def __init__(self, ef_country):
        self.housing_class = HousingStage(ef_country)
        self.data_manager_class = LCADataManager(ef_country)

    def net_excretion_STORAGE(self, animal):
        """
        Calculates the net nitrogen excretion from manure storage.

        Parameters:
        ----------
        animal : object
            The animal object containing relevant housing information.

        Returns:
        -------
        float
            The net nitrogen excretion from manure storage.
        """
        return self.housing_class.net_excretion_HOUSED(
            animal
        ) - self.housing_class.nh3_emissions_per_year_HOUSED(animal)

    def total_ammonia_nitrogen_nh4_STORAGE(self, animal):
        """
        Calculates the total ammonia nitrogen (TAN NH4) excreted per year from manure storage.

        Parameters:
        ----------
        animal : object
            The animal object containing relevant excretion information.

        Returns:
        -------
        float
            The total ammonia nitrogen from manure storage per year.
        """
        percentage_nex = 0.6

        return self.net_excretion_STORAGE(animal) * percentage_nex

    def CH4_STORAGE(self, animal):
        """
        Calculates methane (CH4) emissions from manure storage per year.

        Parameters:
        ----------
        animal : object
            The animal object containing relevant waste management information.

        Returns:
        -------
        float
            Methane emissions from manure storage per year.
        """
        return (
            self.housing_class.volatile_solids_excretion_rate_HOUSED(animal) * 365
        ) * (0.1 * 0.67 * self.data_manager_class.get_storage_MCF(animal.mm_storage)())

    def STORAGE_N2O_direct(self, animal):
        """
        Calculates direct nitrous oxide (N2O) emissions from manure storage.

        Parameters:
        ----------
        animal : object
            The animal object containing relevant waste management information.

        Returns:
        -------
        float
            Direct N2O emissions from manure storage.
        """
        return self.net_excretion_STORAGE(animal) * self.data_manager_class.get_storage_N2O(animal.mm_storage)()


    def nh3_emissions_per_year_STORAGE(self, animal):
        """
        Calculates total ammonia (NH3) emissions per year resulting from manure storage.

        Parameters:
        ----------
        animal : object
            The animal object containing relevant storage information.

        Returns:
        -------
        float
            Total ammonia emissions per year from manure storage.
        """
        return (
            self.total_ammonia_nitrogen_nh4_STORAGE(animal)
            * self.data_manager_class.get_storage_TAN(animal.mm_storage)()
        )

    def STORAGE_N2O_indirect(self, animal):
        """
        Calculates indirect nitrous oxide (N2O) emissions associated with the storage stage of waste management,
        considering ammonia emissions and atmospheric deposition.

        Parameters:
        ----------
        animal : object
            The animal object containing relevant storage information.

        Returns:
        -------
        float
            Indirect N2O emissions resulting from manure storage.
        """
        indirect_atmosphere = self.data_manager_class.get_cohort_parameter(animal.cohort, "atmospheric_deposition")()

        NH3 = self.nh3_emissions_per_year_STORAGE(animal)

        return NH3 * indirect_atmosphere


###############################################################################
# Daily Spread
###############################################################################


class DailySpread:
    """
    A class to calculate the environmental impacts associated with daily manure spreading. 
    It addresses various factors such as nitrogen and phosphorus excretion, ammonia emissions,
    and nitrous oxide emissions from spreading manure on fields.
    
    Attributes:
    ----------
        storage_class (StorageStage): An instance of the StorageStage class to access methods related to manure storage.
        data_manager_class (LCADataManager): An instance of the LCADataManager class to access necessary data and parameters.
    
    Parameters:
    ----------
        ef_country (str): Environmental factor region identifier to tailor calculations to specific regional data.

    Methods:
    -------
        net_excretion_SPREAD(animal):
            Calculates the net nitrogen excretion from manure storage, accounting for losses.
        total_ammonia_nitrogen_nh4_SPREAD(animal):
            Calculates the total ammonia nitrogen released from daily manure spreading.
        SPREAD_N2O_direct(animal):
            Calculates direct nitrous oxide emissions associated with nitrogen applied to fields through manure spreading.
        nh3_emissions_per_year_SPREAD(animal):
            Calculates ammonia emissions per year resulting from daily manure spreading.
        leach_nitrogen_SPREAD(animal):
            Estimates the proportion of nitrogen that is leached into the environment as a result of manure spreading.
        leach_phospherous_SPREAD(animal):
            Estimates the proportion of phosphorus that is leached into the environment as a result of manure spreading.
        SPREAD_N2O_indirect(animal):
            Calculates indirect nitrous oxide emissions associated with volatilization and leaching due to manure spreading.
    """
    def __init__(self, ef_country):
        self.storage_class = StorageStage(ef_country)
        self.data_manager_class = LCADataManager(ef_country)

    def net_excretion_SPREAD(self, animal):
        """
        Calculates the net nitrogen excretion (Nex) from manure storage, accounting for losses.
        
        Parameters:
            animal (Animal): An instance of the Animal class containing relevant data for the animal.
        
        Returns:
            float: Net nitrogen excretion from storage, used in daily spread.
        """
        nex_storage = self.storage_class.net_excretion_STORAGE(animal)
        direct_n2o = self.storage_class.STORAGE_N2O_direct(animal)
        nh3_emissions = self.storage_class.nh3_emissions_per_year_STORAGE(animal)
        indirect_n2o = self.storage_class.STORAGE_N2O_indirect(animal)

        return nex_storage - direct_n2o - nh3_emissions - indirect_n2o

    def total_ammonia_nitrogen_nh4_SPREAD(self, animal):
        """
        Calculates the total ammonia nitrogen (TAN) released from daily manure spreading.
        
        Parameters:
            animal (Animal): An instance of the Animal class containing relevant data for the animal.
        
        Returns:
            float: Total ammonia nitrogen from daily spreading per year.
        """
        percentage_nex = 0.6

        return self.net_excretion_SPREAD(animal) * percentage_nex

    def SPREAD_N2O_direct(self, animal):
        """
        Calculates direct nitrous oxide (N2O) emissions associated with nitrogen applied to fields through manure spreading.
        
        Parameters:
            animal (Animal): An instance of the Animal class containing relevant data for the animal.
        
        Returns:
            float: Direct N2O emissions from daily spreading.
        """
        return self.net_excretion_SPREAD(animal) * self.data_manager_class.get_cohort_parameter(animal.cohort,"proportion_n2o_to_soils")()

    def nh3_emissions_per_year_SPREAD(self, animal):
        """
        Calculates ammonia (NH3) emissions per year resulting from daily manure spreading.
        
        Parameters:
            animal (Animal): An instance of the Animal class containing relevant data for the animal.
        
        Returns:
            float: Ammonia emissions per year from daily spreading.
        """
        nh4 = self.total_ammonia_nitrogen_nh4_SPREAD(animal)

        return nh4 * self.data_manager_class.get_daily_spreading(animal.daily_spreading)()


    def leach_nitrogen_SPREAD(self, animal):
        """
        Estimates the proportion of nitrogen that is leached into the environment as a result of manure spreading.
        
        Parameters:
            animal (Animal): An instance of the Animal class containing relevant data for the animal.
        
        Returns:
            float: Amount of nitrogen leached per year from daily spreading.
        """
        ten_percent_nex = 0.1

        return self.net_excretion_SPREAD(animal) * ten_percent_nex

    def leach_phospherous_SPREAD(self, animal):
        """
        Estimates the proportion of phosphorus that is leached into the environment as a result of manure spreading.
        
        Parameters:
            animal (Animal): An instance of the Animal class containing relevant data for the animal.
        
        Returns:
            float: Amount of phosphorus leached per year from daily spreading.
        """
        return (self.net_excretion_SPREAD(animal) * (1.8 / 5)) * 0.03

    def SPREAD_N2O_indirect(self, animal):
        """
        Calculates indirect nitrous oxide (N2O) emissions associated with volatilization and leaching due to manure spreading.
        
        Parameters:
            animal (Animal): An instance of the Animal class containing relevant data for the animal.
        
        Returns:
            float: Indirect N2O emissions from daily spreading.
        """
        indirect_atmosphere = self.data_manager_class.get_cohort_parameter(animal.cohort, "atmospheric_deposition")()
        indirect_leaching = self.data_manager_class.get_cohort_parameter(animal.cohort, "leaching")()

        NH3 = self.nh3_emissions_per_year_SPREAD(animal)
        NL = self.leach_nitrogen_SPREAD(animal)

        return (NH3 * indirect_atmosphere) + (NL * indirect_leaching)


###############################################################################
# Farm & Upstream Emissions
###############################################################################


class FertiliserInputs:
    """
    A class to manage and calculate emissions and other impacts associated with fertiliser application, including urea and ammonium nitrate.

    Attributes:
    ----------
        data_manager_class (LCADataManager): An instance of the LCADataManager class to access necessary data and parameters for emission factors and other related data.

    Parameters:
    ----------
        ef_country (str): The environmental factor region identifier to tailor calculations to specific regional data.

    """
    def __init__(self, ef_country):
        self.data_manager_class = LCADataManager(ef_country)

    def urea_N2O_direct(self, total_urea, total_urea_abated):
        """
        Calculates direct N2O emissions from both standard and abated urea applied to soils.

        Parameters:
            total_urea (float): Total amount of urea applied (kg).
            total_urea_abated (float): Total amount of abated urea applied (kg).

        Returns:
            float: Total direct N2O emissions (kg).
        """
        ef_urea = self.data_manager_class.get_ef_urea()
        ef_urea_abated = self.data_manager_class.get_ef_urea_abated()

        return (total_urea * ef_urea) + (total_urea_abated * ef_urea_abated)

    def urea_NH3(self, total_urea, total_urea_abated):
        """
        Estimates the amount of NH3 volatilized from both standard and abated urea applications.

        Parameters:
            total_urea (float): Total amount of urea applied (kg).
            total_urea_abated (float): Total amount of abated urea applied (kg).

        Returns:
            float: Total NH3 emissions (kg).
        """
        ef_urea = (
            self.data_manager_class.get_ef_urea_to_nh3_and_nox()
        )
        ef_urea_abated = (
            self.data_manager_class.get_ef_urea_abated_to_nh3_and_nox()
        )

        return (total_urea * ef_urea) + (total_urea_abated * ef_urea_abated)

    def urea_nleach(self, total_urea, total_urea_abated):
        """
        Calculates the amount of urea and abated urea leached from soils after application.

        Parameters:
            total_urea (float): Total amount of urea applied (kg).
            total_urea_abated (float): Total amount of abated urea applied (kg).

        Returns:
            float: Total leached urea (kg).
        """
        leach = self.data_manager_class.get_ef_fration_leach_runoff()

        return (total_urea + total_urea_abated) * leach

    def urea_N2O_indirect(self, total_urea, total_urea_abated):
        """
        Calculates indirect emissions from urea and abated urea application, considering atmospheric deposition and leaching.

        Parameters:
            total_urea (float): Total amount of urea applied (kg).
            total_urea_abated (float): Total amount of abated urea applied (kg).

        Returns:
            float: Total indirect N2O emissions (kg).
        """
        indirect_atmosphere = (
            self.data_manager_class.get_indirect_atmospheric_deposition()
        )
        indirect_leaching = (
            self.data_manager_class.get_indirect_leaching()
        )

        return (self.urea_NH3(total_urea, total_urea_abated) * indirect_atmosphere) + (
            self.urea_nleach(total_urea, total_urea_abated) * indirect_leaching
        )

    def urea_co2(self, total_urea):
        """
        Calculates the total CO2 emissions resulting from the application of urea.

        Parameters:
            total_urea (float): Total amount of urea applied (kg).

        Returns:
            float: Total CO2 emissions (kg).
        """
        ef_urea_co2 = self.data_manager_class.get_ef_urea_co2()

        return (total_urea  * ef_urea_co2) * (
            44 / 12
        )  # adjusted to the NIR version of this calculation


    def lime_co2(self, total_lime):
        """
        Calculates total CO2 emissions from the application of lime.

        Parameters:
            total_lime (float): Total amount of lime applied (kg).

        Returns:
            float: Total CO2 emissions from lime application (kg).
        """
        ef_lime_co2 = self.data_manager_class.get_ef_lime_co2()

        return (total_lime * ef_lime_co2) * (
            44 / 12
        )  # adjusted to the NIR version of this calculation

    def urea_P_leach(self, total_urea, total_urea_abated):
        """
        Calculates the amount of phosphorus leached from urea and abated urea application.

        Parameters:
            total_urea (float): Total amount of urea applied (kg).
            total_urea_abated (float): Total amount of abated urea applied (kg).

        Returns:
            float: Total phosphorus leached (kg).
        """
        frac_leach = self.data_manager_class.get_frac_p_leach()

        return (total_urea + total_urea_abated) * frac_leach

    # Nitrogen Fertiliser Emissions

    def n_fertiliser_P_leach(self, total_n_fert):
        """
        Calculates the amount of phosphorus leached due to the application of nitrogen fertilisers.

        Parameters:
            total_n_fert (float): Total amount of nitrogen fertiliser applied (kg).

        Returns:
            float: Total phosphorus leached due to nitrogen fertiliser application (kg).
        """
        frac_leach = self.data_manager_class.get_frac_p_leach()

        return total_n_fert * frac_leach

    def n_fertiliser_direct(self, total_n_fert):
        """
        Calculates direct N2O emissions resulting from the application of nitrogen fertilisers at field level.

        Parameters:
            total_n_fert (float): Total amount of nitrogen fertiliser applied (kg).

        Returns:
            float: Total direct N2O emissions from nitrogen fertiliser application (kg).
        """
        ef = self.data_manager_class.get_ef_AN_fertiliser()

        return total_n_fert * ef

    def n_fertiliser_NH3(self, total_n_fert):
        """
        Calculates total NH3 emissions resulting from the application of nitrogen fertilisers at field level.

        Parameters:
            total_n_fert (float): Total amount of nitrogen fertiliser applied (kg).

        Returns:
            float: Total NH3 emissions from nitrogen fertiliser application (kg).
        """
        ef = (
            self.data_manager_class.get_ef_AN_fertiliser_to_nh3_and_nox()
        )
        return total_n_fert * ef

    def n_fertiliser_nleach(self, total_n_fert):
        """
        Calculates the total nitrogen leached from the application of nitrogen fertilisers at field level.

        Parameters:
            total_n_fert (float): Total amount of nitrogen fertiliser applied (kg).

        Returns:
            float: Total nitrogen leached from nitrogen fertiliser application (kg).
        """
        ef = self.data_manager_class.get_ef_fration_leach_runoff()

        return total_n_fert * ef


    def n_fertiliser_indirect(self, total_n_fert):
        """
        Calculates the indirect N2O emissions from the use of nitrogen fertilisers, accounting for atmospheric deposition and leaching.

        Parameters:
            total_n_fert (float): Total amount of nitrogen fertiliser applied (kg).

        Returns:
            float: Total indirect N2O emissions from nitrogen fertiliser application (kg).
        """
        indirect_atmosphere = (
            self.data_manager_class.get_indirect_atmospheric_deposition()
        )
        indirect_leaching = (
            self.data_manager_class.get_indirect_leaching()
        )

        return (self.n_fertiliser_NH3(total_n_fert) * indirect_atmosphere) + (
            self.n_fertiliser_nleach(total_n_fert) * indirect_leaching
        )

    # Fertiliser Application Totals for N20 and CO2

    def total_fertiliser_N20(self, total_urea, total_urea_abated, total_n_fert):
        """
        Returns the total N2O emissions, both direct and indirect, from the application of both urea and ammonium nitrate fertilisers.

        Parameters:
            total_urea (float): Total amount of urea applied (kg).
            total_urea_abated (float): Total amount of abated urea applied (kg).
            total_n_fert (float): Total amount of nitrogen fertiliser applied (kg).

        Returns:
            float: Total N2O emissions from all fertiliser applications (kg).
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
        Calculates the amount of phosphorus leached due to the application of phosphorus fertilisers.

        Parameters:
            total_p_fert (float): Total amount of phosphorus fertiliser applied (kg).

        Returns:
            float: Total phosphorus leached from phosphorus fertiliser application (kg).
        """
        frac_leach = float(self.data_manager_class.get_frac_p_leach())

        return total_p_fert * frac_leach


################################################################################
# Total Global Warming Potential of whole farms (Upstream Processes & Fossil Fuel Energy)
################################################################################

class Upstream:
    """
    Handles the calculation of upstream emissions related to concentrate production, diesel usage, and electricity consumption 
    for the environmental impact assessment of sheep farming operations. It focuses on CO2 and PO4 emissions from various 
    sources including fertiliser production, diesel fuel, and electricity used in farm operations.

    Attributes:
        data_manager_class (LCADataManager): Provides access to necessary data for calculations.

    Methods:
        co2_from_concentrate_production: Calculates CO2 emissions from concentrate production for sheep.
        po4_from_concentrate_production: Calculates PO4 emissions from concentrate production for sheep.
        diesel_CO2: Estimates CO2 emissions from diesel fuel usage.
        diesel_PO4: Estimates PO4 emissions from diesel fuel usage.
        elec_CO2: Calculates CO2 emissions from electricity consumption.
        elec_PO4: Calculates PO4 emissions from electricity consumption.
        fert_upstream_CO2: Estimates CO2 emissions from the production of various fertilisers.
        fert_upstream_EP: Estimates PO4 emissions from the production of various fertilisers.
    """
    def __init__(self, ef_country):
        self.data_manager_class = LCADataManager(ef_country)

    def co2_from_concentrate_production(self, animal):
        """
        Calculates CO2e emissions from the production of concentrates consumed by the animal cohorts.

        Parameters:
            animal (object): An object containing data about different animal cohorts and their concentrate consumption.

        Returns:
            float: The total CO2e emissions from concentrate production for all animal cohorts (kg/year).
        """
        concentrate_co2 = 0

        for key in animal.__dict__.keys():
            if (
                key in self.data_manager_class.get_cohort_keys()
                and animal.__getattribute__(key).pop != 0
            ):
                concentrate_co2 += (
                    animal.__getattribute__(key).con_amount
                    * self.data_manager_class.get_upstream_concentrate_co2e(
                        animal.__getattribute__(key).con_type
                    )
                ) * animal.__getattribute__(key).pop

        return concentrate_co2 * 365
    
        # Imported Feeds
    def po4_from_concentrate_production(self, animal):
        """
        Calculates phosphorus (PO4e) emissions from the production of concentrates consumed by the animal cohorts.

        Parameters:
            animal (object): An object containing data about different animal cohorts and their concentrate consumption.

        Returns:
            float: The total PO4e emissions from concentrate production for all animal cohorts (kg/year).
        """
        concentrate_p = 0

        for key in animal.__dict__.keys():
            if (
                key in self.data_manager_class.get_cohort_keys()
                and animal.__getattribute__(key).pop != 0
            ):
                concentrate_p += (
                    animal.__getattribute__(key).con_amount
                    * self.data_manager_class.get_upstream_concentrate_po4e(
                        animal.__getattribute__(key).con_type
                    )
                ) * animal.__getattribute__(key).pop

        return concentrate_p * 365

    def diesel_CO2(self, diesel_kg):
        """
        Calculates CO2e emissions from diesel consumption, including both direct and indirect upstream emissions.

        Parameters:
            diesel_kg (float): The amount of diesel consumed (kg).

        Returns:
            float: The total CO2e emissions from diesel consumption (kg).
        """
        Diesel_indir = self.data_manager_class.get_upstream_diesel_co2e_indirect()
        Diest_dir = self.data_manager_class.get_upstream_diesel_co2e_direct()

        return diesel_kg * (Diest_dir + Diesel_indir)
    

    def diesel_PO4(self, diesel_kg):
        """
        Calculates phosphorus (PO4e) emissions from diesel consumption, including both direct and indirect upstream emissions.

        Parameters:
            diesel_kg (float): The amount of diesel consumed (kg).

        Returns:
            float: The total PO4e emissions from diesel consumption (kg).
        """
        Diesel_indir = self.data_manager_class.get_upstream_diesel_po4e_indirect()
        Diest_dir = self.data_manager_class.get_upstream_diesel_po4e_direct()

        return diesel_kg * (Diest_dir + Diesel_indir)


    def elec_CO2(self, elec_kwh):
        """
        Calculates CO2e emissions from electricity consumption.

        Parameters:
            elec_kwh (float): The amount of electricity consumed (kWh).

        Returns:
            float: The total CO2e emissions from electricity consumption (kg).
        """
        elec_consumption = self.data_manager_class.get_upstream_electricity_co2e()

        return elec_kwh * elec_consumption


    def elec_PO4(self, elec_kwh):
        """
        Calculates phosphorus emissions (PO4e) from electricity consumption.

        Parameters:
            elec_kwh (float): The amount of electricity consumed (kWh).

        Returns:
            float: The total PO4e emissions from electricity consumption (kg).
        """
        elec_consumption = self.data_manager_class.get_upstream_electricity_po4e()

        return elec_kwh * elec_consumption

    # Emissions from upstream fertiliser production
    def fert_upstream_CO2(
        self, total_n_fert, total_urea, total_urea_abated, total_p_fert, total_k_fert, total_lime_fert
    ):
        """
        Calculates the total upstream CO2e emissions from the production of various fertilizers.

        Parameters:
            total_n_fert (float): Total nitrogen fertilizer applied (kg).
            total_urea (float): Total urea applied (kg).
            total_urea_abated (float): Total abated urea applied (kg).
            total_p_fert (float): Total phosphorus fertilizer applied (kg).
            total_k_fert (float): Total potassium fertilizer applied (kg).
            total_lime_fert (float): Total lime fertilizer applied (kg).

        Returns:
            float: The total upstream CO2e emissions from fertilizer production (kg).
        """
        AN_fert_CO2 = self.data_manager_class.get_upstream_AN_fertiliser_co2e()# Ammonium Nitrate Fertiliser
        Urea_fert_CO2 = self.data_manager_class.get_upstream_urea_fertiliser_co2e()
        Triple_superphosphate = self.data_manager_class.get_upstream_triple_phosphate_co2e()
        Potassium_chloride = self.data_manager_class.get_upstream_potassium_chloride_co2e()
        Lime = self.data_manager_class.get_upstream_lime_co2e()

        return (
            (total_n_fert * AN_fert_CO2)
            + (total_urea * Urea_fert_CO2)
            + (total_urea_abated * Urea_fert_CO2)
            + (total_p_fert * Triple_superphosphate)
            + (total_k_fert * Potassium_chloride)
            + (total_lime_fert * Lime)
        )

    def fert_upstream_EP(
        self, total_n_fert, total_urea, total_urea_abated, total_p_fert, total_k_fert, total_lime_fert
    ):
        """
        Calculates the total upstream emissions (PO4e) from the production of various fertilizers.

        Parameters:
            total_n_fert (float): Total nitrogen fertilizer applied (kg).
            total_urea (float): Total urea applied (kg).
            total_urea_abated (float): Total abated urea applied (kg).
            total_p_fert (float): Total phosphorus fertilizer applied (kg).
            total_k_fert (float): Total potassium fertilizer applied (kg).
            total_lime_fert (float): Total lime fertilizer applied (kg).

        Returns:
            float: The total upstream emissions (PO4e) from fertilizer production (kg).
        """
        AN_fert_PO4 =self.data_manager_class.get_upstream_AN_fertiliser_po4e()# Ammonium Nitrate Fertiliser
        Urea_fert_PO4 = self.data_manager_class.get_upstream_urea_fertiliser_po4e()
        Triple_superphosphate = self.data_manager_class.get_upstream_triple_phosphate_po4e()
        Potassium_chloride = self.data_manager_class.get_upstream_potassium_chloride_po4e()
        Lime = self.data_manager_class.get_upstream_lime_po4e()

        return (
            (total_n_fert * AN_fert_PO4)
            + (total_urea * Urea_fert_PO4)
            + (total_urea_abated * Urea_fert_PO4)
            + (total_p_fert * Triple_superphosphate)
            + (total_k_fert * Potassium_chloride)
            + (total_lime_fert * Lime)
        )


################################################################################
# Allocation
################################################################################
class Allocation:
    """
    This class is responsible for calculating the allocations of live weight and milk production 
    for various animal cohorts within a farm system. It provides methods to calculate total live 
    weight outputs and inputs, convert these weights to energy units, and determine allocation 
    factors for milk and meat based on these energy values.

    Methods in this class allow for the calculation of the total output in terms of live weight 
    and milk, as well as the conversion of these outputs to energy equivalents for allocation 
    purposes.
    """
    def live_weight_output(self, animal):
        """
        Calculates the total live weight output from all animal cohorts.

        Parameters:
            animal (object): An object containing data about different animal cohorts and their live weights and number sold.

        Returns:
            float: The total live weight output for all animal cohorts (kg).
        """
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
        """
        Calculates the total live weight bought for all animal cohorts.

        Parameters:
            animal (object): An object containing data about different animal cohorts and their live weights and number bought.

        Returns:
            float: The total live weight bought for all animal cohorts (kg).
        """
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
        """
        Converts the total live weight output to Megajoules of energy (MJe).

        Parameters:
            animal (object): An object containing data about different animal cohorts.

        Returns:
            float: The total energy output from live weight for all animal cohorts (MJe).
        """
        converstion_MJe = 12.36
        return self.live_weight_output(animal) * converstion_MJe

    def milk_to_kg_output(self, animal):
        """
        Calculates the total milk output in kilograms for dairy cows.

        Parameters:
            animal (object): An object containing data about the dairy cow cohort.

        Returns:
            float: The total milk output for dairy cows (kg/year).
        """
        # kg of milk
        kg_conversion = 1.033
        year = 365
        return (
            animal.dairy_cows.daily_milk * animal.dairy_cows.pop * year * kg_conversion
        )

    def milk_to_mje(self, animal):
        """
        Converts the total milk output to Megajoules of energy (MJe).

        Parameters:
            animal (object): An object containing data about the dairy cow cohort.

        Returns:
            float: The total energy output from milk for dairy cows (MJe).
        """
        converstion_MJe = 2.5
        return self.milk_to_kg_output(animal) * converstion_MJe

    def milk_allocation_factor(self, animal):
        """
        Calculates the allocation factor for milk based on its energy content compared to the total energy content of milk and meat.

        Parameters:
            animal (object): An object containing data about the dairy cow cohort and other animal cohorts contributing to meat production.

        Returns:
            float: The allocation factor for milk.
        """
        total = self.milk_to_mje(animal) + self.live_weight_to_mje(animal)
        return self.milk_to_mje(animal) / total

    def meat_allocation_factor(self, animal):
        """
        Calculates the allocation factor for meat based on its energy content compared to the total energy content of milk and meat.

        Parameters:
            animal (object): An object containing data about the dairy cow cohort and other animal cohorts contributing to meat production.

        Returns:
            float: The allocation factor for meat.
        """
        return 1 - self.milk_allocation_factor(animal)


################################################################################
# Totals
################################################################################


class ClimateChangeTotals:
    """
    This class calculates total greenhouse gas emissions associated with various farm activities 
    including enteric fermentation, manure management, soil management, and the upstream 
    impacts of fuel and feed production. It utilizes data from various other classes to 
    accumulate total emissions related to climate change.

    Attributes:
    ----------
        data_manager_class (LCADataManager): Manages lifecycle assessment data.
        grass_feed_class (GrassFeed): Manages grass feed-related calculations.
        grazing_class (GrazingStage): Manages grazing-related calculations.
        spread_class (DailySpread): Manages nutrient spreading-related calculations.
        housing_class (HousingStage): Manages housing-related calculations.
        storage_class (StorageStage): Manages manure storage-related calculations.
        fertiliser_class (FertiliserInputs): Manages fertiliser input-related calculations.
        upstream_class (Upstream): Manages upstream emissions calculations.
    """
    def __init__(self, ef_country):
        self.data_manager_class = LCADataManager(ef_country)
        self.grass_feed_class = GrassFeed(ef_country)
        self.grazing_class = GrazingStage(ef_country)
        self.spread_class = DailySpread(ef_country)
        self.housing_class = HousingStage(ef_country)
        self.storage_class = StorageStage(ef_country)
        self.fertiliser_class = FertiliserInputs(ef_country)
        self.upstream_class = Upstream(ef_country)

    def create_emissions_dictionary(self, keys):
        """
        Creates a dictionary template for emissions calculations with zero-initialized values.

        Parameters:
            keys (list): List of animal cohorts or other categories for emissions calculation.

        Returns:
            dict: A dictionary of dictionaries for organizing emissions data.
        """
        key_list = [
            "enteric_ch4",
            "manure_management_N2O",
            "manure_management_CH4",
            "manure_applied_N",
            "N_direct_PRP",
            "N_direct_PRP",
            "N_indirect_PRP",
            "N_direct_fertiliser",
            "N_indirect_fertiliser",
            "soils_CO2",
            "soil_organic_N_direct",
            "soil_organic_N_indirect",
            "soil_inorganic_N_direct",
            "soil_inorganic_N_indirect",
            "soil_histosol_N_direct",
            "crop_residue_direct",
            "soil_N_direct",
            "soil_N_indirect",
            "soils_N2O",
        ]

        keys_dict = dict.fromkeys(keys)

        emissions_dict = dict.fromkeys(key_list)

        for key in emissions_dict.keys():
            emissions_dict[key] = copy.deepcopy(keys_dict)
            for inner_k in keys_dict.keys():
                emissions_dict[key][inner_k] = 0

        return emissions_dict
    

    def create_expanded_emissions_dictionary(self, keys):
        """
        Extends the basic emissions dictionary template with additional categories for more 
        detailed emissions calculations.

        Parameters:
            keys (list): List of animal cohorts or other categories for detailed emissions calculation.

        Returns:
            dict: An expanded dictionary of dictionaries for organizing detailed emissions data.
        """
        key_list = [
            "enteric_ch4",
            "manure_management_N2O",
            "manure_management_CH4",
            "manure_applied_N",
            "N_direct_PRP",
            "N_direct_PRP",
            "N_indirect_PRP",
            "N_direct_fertiliser",
            "N_indirect_fertiliser",
            "soils_CO2",
            "soil_organic_N_direct",
            "soil_organic_N_indirect",
            "soil_inorganic_N_direct",
            "soil_inorganic_N_indirect",
            "soil_histosol_N_direct",
            "crop_residue_direct",
            "soil_N_direct",
            "soil_N_indirect",
            "soils_N2O",
            "upstream_fuel_fert",
            "upstream_feed",
            "upstream",
        ]

        keys_dict = dict.fromkeys(keys)

        emissions_dict = dict.fromkeys(key_list)

        for key in emissions_dict.keys():
            emissions_dict[key] = copy.deepcopy(keys_dict)
            for inner_k in keys_dict.keys():
                emissions_dict[key][inner_k] = 0

        return emissions_dict

    def Enteric_CH4(self, animal):
        """
        Calculates methane emissions from enteric fermentation for a given animal.

        Parameters:
            animal (AnimalCategory): The animal cohort for which emissions are being calculated.

        Returns:
            float: Total methane emissions from enteric fermentation for the specified animal (kg CH4).
        """
        return self.grass_feed_class.ch4_emissions_factor(animal)

    def CH4_enteric_ch4(self, animal):
        """
        Accumulates total methane emissions from enteric fermentation across all animal cohorts.

        Parameters:
            animal (AnimalCollection): Collection of animal cohorts within the farm system.

        Returns:
            float: Total methane emissions from enteric fermentation across all cohorts (kg CH4).
        """
        result = 0
        for key in animal.__dict__.keys():
            if (
                key in self.data_manager_class.get_cohort_keys()
                and animal.__getattribute__(key).pop != 0
            ):
                result += (
                    self.Enteric_CH4(animal.__getattribute__(key))
                    * animal.__getattribute__(key).pop
                )

        return result

    def CH4_manure_management(self, animal):
        """
        Calculates methane emissions from manure management for animal cohorts.

        Parameters:
            animal (AnimalCollection): Collection of animal cohorts within the farm system.

        Returns:
            float: Total methane emissions from manure management across all cohorts (kg CH4).
        """
        result = 0

        for key in animal.__dict__.keys():
            if (
                key in self.data_manager_class.get_cohort_keys()
                and animal.__getattribute__(key).pop != 0
            ):
                result += (
                    self.Total_manure_ch4(animal.__getattribute__(key))
                    * animal.__getattribute__(key).pop
                )

        return result

    def PRP_Total(self, animal):
        """
        Calculates the total N2O emissions related to Pasture, Range, and Paddock (PRP) for a given animal.

        Parameters:
            animal (AnimalCategory): The animal cohort for which emissions are being calculated.

        Returns:
            float: Total N2O emissions from PRP for the specified animal.
        """
        mole_weight = 44 / 28

        return (
            self.grazing_class.PRP_N2O_direct(animal)
            + self.grazing_class.PRP_N2O_indirect(animal)
        ) * mole_weight

    def Total_N2O_Spreading(self, animal):
        """
        Calculates the total N2O emissions related to the spreading of manure for a given animal collection.

        Parameters:
            animal (AnimalCategory): The animal collection for which emissions are being calculated.

        Returns:
            float: Total N2O emissions from manure spreading for the specified animal collection.
        """
        mole_weight = 44 / 28

        Spreading = 0

        for key in animal.__dict__.keys():
            if (
                key in self.data_manager_class.get_cohort_keys()
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
        Calculates the total N2O emissions related to the storage of manure for a given animal collection.

        Parameters:
            animal (AnimalCategory): The animal collection for which emissions are being calculated.

        Returns:
            float: Total N2O emissions from manure storage for the specified animal collection.
        """
        mole_weight = 44 / 28

        n2o_direct = 0
        n2o_indirect_storage = 0
        n2o_indirect_housing = 0

        for key in animal.__dict__.keys():
            if (
                key in self.data_manager_class.get_cohort_keys()
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
        Calculates the direct N2O emissions from pasture, range, and paddock for a given animal collection.

        Parameters:
            animal (AnimalCategory): The animal cohort collection for which emissions are being calculated.

        Returns:
            float: Direct N2O emissions from PRP for the specified animal collection.
        """
        mole_weight = 44 / 28

        PRP_direct = 0

        for key in animal.__dict__.keys():
            if (
                key in self.data_manager_class.get_cohort_keys()
                and animal.__getattribute__(key).pop != 0
            ):
                PRP_direct += (
                    self.grazing_class.PRP_N2O_direct(animal.__getattribute__(key))
                    * animal.__getattribute__(key).pop
                )

        return PRP_direct * mole_weight

    def N2O_total_PRP_N2O_indirect(self, animal):
        """
        Calculates the indirect N2O emissions from pasture, range, and paddock for a given animal collection.

        Parameters:
            animal (AnimalCategory): The animal cohort collection for which emissions are being calculated.

        Returns:
            float: Indirect N2O emissions from PRP for the specified animal collection.
        """
        mole_weight = 44 / 28

        PRP_indirect = 0

        for key in animal.__dict__.keys():
            if (
                key in self.data_manager_class.get_cohort_keys()
                and animal.__getattribute__(key).pop != 0
            ):
                PRP_indirect += (
                    self.grazing_class.PRP_N2O_indirect(animal.__getattribute__(key))
                    * animal.__getattribute__(key).pop
                )

        return PRP_indirect * mole_weight

    def Total_manure_ch4(self, animal):
        """
        Calculates the total methane emissions related to manure management for a given animal collection.

        Parameters:
            animal (AnimalCategory): The animal collection for which emissions are being calculated.

        Returns:
            float: Total methane emissions from manure management for the specified animal collection.
        """
        return self.grazing_class.ch4_emissions_for_grazing(
            animal
        ) + self.storage_class.CH4_STORAGE(animal)

    def CO2_soils_GWP(self, total_urea, total_lime):
        """
        Calculates the global warming potential from CO2 emissions related to soil management through urea and lime application.

        Parameters:
            total_urea (float): Total amount of urea used (kg).
            total_lime (float): Total amount of lime used (kg).

        Returns:
            float: CO2 emissions from soil management.
        """
        return self.fertiliser_class.urea_co2(total_urea) + self.fertiliser_class.lime_co2(total_lime)

    def N2O_direct_fertiliser(self, total_urea, total_urea_abated, total_n_fert):
        """
        Calculates the total direct N2O emissions from urea and ammonium fertilizers.

        Parameters:
            total_urea (float): Total amount of urea used (kg).
            total_urea_abated (float): Total amount of urea with emissions-reducing treatments applied (kg).
            total_n_fert (float): Total amount of nitrogen fertilizer used (kg).

        Returns:
            float: Total direct N2O emissions from fertilizer application.
        """
        mole_weight = 44 / 28

        result = (
            self.fertiliser_class.urea_N2O_direct(total_urea, total_urea_abated)
            + self.fertiliser_class.n_fertiliser_direct(total_n_fert)
        ) * mole_weight

        return result

    def N2O_fertiliser_indirect(self, total_urea, total_urea_abated, total_n_fert):
        """
        Calculates the total indirect N2O emissions from urea and ammonium fertilizers.

        Parameters:
            total_urea (float): Total amount of urea used (kg).
            total_urea_abated (float): Total amount of urea with emissions-reducing treatments applied (kg).
            total_n_fert (float): Total amount of nitrogen fertilizer used (kg).

        Returns:
            float: Total indirect N2O emissions from fertilizer application.
        """
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
        total_lime_fert,
    ):
        """
        Calculates the total CO2 emissions from various upstream activities and inputs. 
        This includes emissions from the use of diesel, electricity, and different types of fertilizers. 

        Parameters:
        - diesel_kg: The amount of diesel used, in kilograms.
        - elec_kwh: The amount of electricity consumed, in kilowatt-hours.
        - total_n_fert: The total amount of nitrogen fertilizer used, in kilograms.
        - total_urea: The total amount of urea used, in kilograms.
        - total_urea_abated: The total amount of abated urea (urea treated to reduce emissions) used, in kilograms.
        - total_p_fert: The total amount of phosphorus fertilizer used, in kilograms.
        - total_k_fert: The total amount of potassium fertilizer used, in kilograms.
        - total_lime_fert: The total amount of lime fertilizer used, in kilograms.

        Returns:
        Total CO2 emissions from all specified sources, measured in equivalent kilograms of CO2.
        """
        return (
            self.upstream_class.diesel_CO2(diesel_kg)
            + self.upstream_class.elec_CO2(elec_kwh)
            + self.upstream_class.fert_upstream_CO2(
                total_n_fert,
                total_urea,
                total_urea_abated,
                total_p_fert,
                total_k_fert,
                total_lime_fert,
            )
            
        )
    
    def co2_from_concentrate_production(self, animal):
        """
        Calculates the CO2e emissions from the production of concentrates fed to the animal.
        This function looks at the type and amount of concentrate feed and uses predefined emission factors to estimate the CO2e impact.

        Parameters:
        - animal: The animal collection for which the CO2e emissions are being calculated.
        This object should contain the type and amount of concentrate feed consumed.

        Returns:
        The total CO2e emissions from the production of concentrate feed, measured in equivalent kilograms of CO2.

        """
        return self.upstream_class.co2_from_concentrate_production(animal)


###############################################################################
# Water Quality EP PO4e
###############################################################################


class EutrophicationTotals:
    """
    A class responsible for calculating the total eutrophication potential associated with a given farming operation. 
    This includes contributions from manure management, soil management, fertiliser application, and upstream processes 
    related to feed and fuel production.

    Attributes:
    ----------
        data_manager_class (LCADataManager): An instance of the LCADataManager class to access necessary emission factors and conversion values.
        grazing_class (GrazingStage): An instance of the GrazingStage class to access grazing-related eutrophication contributions.
        housing_class (HousingStage): An instance of the HousingStage class to access housing-related eutrophication contributions.
        storage_class (StorageStage): An instance of the StorageStage class to access storage-related eutrophication contributions.
        spread_class (DailySpread): An instance of the DailySpread class to access spreading-related eutrophication contributions.
        fertiliser_class (FertiliserInputs): An instance of the FertiliserInputs class to access fertiliser-related eutrophication contributions.
        upstream_class (Upstream): An instance of the Upstream class to access upstream-related eutrophication contributions.

    Methods:
    --------
        create_emissions_dictionary(keys): Creates a structured dictionary for tracking eutrophication emissions.
        create_expanded_emissions_dictionary(keys): Creates a more detailed structured dictionary for tracking eutrophication emissions, including upstream processes.
        total_manure_NH3_EP(animal): Calculates the total ammonia emissions from manure management, converted to phosphate equivalents.
        total_fertiliser_soils_NH3_and_LEACH_EP(total_urea, total_urea_abated, total_n_fert): Calculates total ammonia and leaching from fertiliser application to soils, converted to phosphate equivalents.
        total_grazing_soils_NH3_and_LEACH_EP(animal): Calculates total ammonia and leaching from grazing management to soils, converted to phosphate equivalents.
        fertiliser_soils_P_LEACH_EP(total_urea, total_urea_abated, total_n_fert, total_p_fert): Calculates total phosphorus leaching from fertiliser application, contributing to eutrophication.
        grazing_soils_P_LEACH_EP(animal): Calculates total phosphorus leaching from grazing, contributing to eutrophication.
        total_fertilser_soils_EP(total_urea, total_urea_abated, total_n_fert, total_p_fert): Aggregates total eutrophication potential from fertiliser applications to soils.
        total_grazing_soils_EP(animal): Aggregates total eutrophication potential from grazing management.
        upstream_and_inputs_and_fuel_po4(diesel_kg, elec_kwh, total_n_fert, total_urea, total_urea_abated, total_p_fert, total_k_fert, total_lime_fert): Calculates total eutrophication potential from upstream activities and inputs, including fuel and electricity usage.
        po4_from_concentrate_production(animal): Calculates total phosphorus emissions from concentrate production used in animal diets.
    """
    def __init__(self, ef_country):
        self.data_manager_class = LCADataManager(ef_country)
        self.grazing_class = GrazingStage(ef_country)
        self.housing_class = HousingStage(ef_country)
        self.storage_class = StorageStage(ef_country)
        self.spread_class = DailySpread(ef_country)
        self.fertiliser_class = FertiliserInputs(ef_country)
        self.upstream_class = Upstream(ef_country)


    def create_emissions_dictionary(self, keys):
        """
        Creates a dictionary to store eutrophication emissions data for different categories.
        
        Parameters:
        -----------
            keys: A list of keys representing different farm activities or emission sources.
        
        Returns:
        --------
            A dictionary with initialized values for each key and sub-key.
        """
        key_list = [
            "manure_management",
            "soils",
        ]

        keys_dict = dict.fromkeys(keys)

        emissions_dict = dict.fromkeys(key_list)

        for key in emissions_dict.keys():
            emissions_dict[key] = copy.deepcopy(keys_dict)
            for inner_k in keys_dict.keys():
                emissions_dict[key][inner_k] = 0

        return emissions_dict
    

    def create_expanded_emissions_dictionary(self, keys):
        """
        Creates an expanded dictionary to store detailed eutrophication emissions data.
        
        Parameters:
            keys: A list of keys representing different farm activities or emission sources.
        
        Returns:
            An expanded dictionary with initialized values for each category and sub-category.
        """
        key_list = [
            "manure_management",
            "soils",
            "upstream_fuel_fert",
            "upstream_feed",
            "upstream",

        ]

        keys_dict = dict.fromkeys(keys)

        emissions_dict = dict.fromkeys(key_list)

        for key in emissions_dict.keys():
            emissions_dict[key] = copy.deepcopy(keys_dict)
            for inner_k in keys_dict.keys():
                emissions_dict[key][inner_k] = 0

        return emissions_dict
    
    # Manure Management
    def total_manure_NH3_EP(self, animal):
        """
        Calculates total ammonia emissions from manure, converted to equivalent phosphorus, contributing to eutrophication potential.
        
        Parameters:
            animal: Animal data object containing manure emission details.
        
        Returns:
            Total ammonia emissions from manure management converted to phosphorus equivalent.
        """
        indirect_atmosphere = (
            self.data_manager_class.get_indirect_atmospheric_deposition()
        )

        NH3N = 0

        for key in animal.__dict__.keys():
            if (
                key in self.data_manager_class.get_cohort_keys()
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
        Calculates total ammonia and leaching emissions from fertilizer application, converted to phosphorus equivalent.
        
        Parameters:
            total_urea: Total amount of urea applied.
            total_urea_abated: Total amount of urea with abatement measures applied.
            total_n_fert: Total amount of nitrogen fertilizers applied.
        
        Returns:
            Total ammonia and leaching emissions from fertilizers, converted to phosphorus equivalent.
        """
        indirect_atmosphere = (
            self.data_manager_class.get_indirect_atmospheric_deposition()
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
        Calculates total ammonia and leaching emissions from grazing soils, converted to phosphorus equivalent.
        
        Parameters:
            animal: Animal data object containing grazing information.
        
        Returns:
            Total ammonia and leaching emissions from grazing, converted to phosphorus equivalent.
        """
        indirect_atmosphere = (
            self.data_manager_class.get_indirect_atmospheric_deposition()
        )

        NH3N = 0

        LEACH = 0

        for key in animal.__dict__.keys():
            if (
                key in self.data_manager_class.get_cohort_keys()
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
        """
        Calculates phosphorus leaching from fertilizer application on soils.
        
        Parameters:
            total_urea: Total amount of urea applied.
            total_urea_abated: Total amount of urea with abatement measures applied.
            total_n_fert: Total amount of nitrogen fertilizers applied.
            total_p_fert: Total amount of phosphorus fertilizers applied.
        
        Returns:
            Total phosphorus leaching from fertilizers application.
        """
        PLEACH = (
            self.fertiliser_class.urea_P_leach(total_urea, total_urea_abated)
            + self.fertiliser_class.n_fertiliser_P_leach(total_n_fert)
            + self.fertiliser_class.p_fertiliser_P_leach(total_p_fert)
        )

        return PLEACH * 3.06

    def grazing_soils_P_LEACH_EP(self, animal):
        """
        Calculates phosphorus leaching from grazing soils.
        
        Parameters:
            animal: Animal data object containing grazing information.
        
        Returns:
            Total phosphorus leaching from grazing activities.
        """
        PLEACH = 0

        for key in animal.__dict__.keys():
            if (
                key in self.data_manager_class.get_cohort_keys()
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
        """
        Calculates total eutrophication potential from fertilizer application on soils.
        
        Parameters:
            total_urea, total_urea_abated, total_n_fert, total_p_fert: Amounts of different fertilizers applied.
        
        Returns:
            Total eutrophication potential from fertilizer application.
        """
        return self.total_fertiliser_soils_NH3_and_LEACH_EP(
            total_urea, total_urea_abated, total_n_fert
        ) + self.fertiliser_soils_P_LEACH_EP(
            total_urea, total_urea_abated, total_n_fert, total_p_fert
        )

    def total_grazing_soils_EP(self, animal):
        """
        Calculates total eutrophication potential from grazing soils.
        
        Parameters:
            animal: Animal data object containing grazing information.
        
        Returns:
            Total eutrophication potential from grazing activities.
        """
        return self.total_grazing_soils_NH3_and_LEACH_EP(animal
        ) + self.grazing_soils_P_LEACH_EP(animal)

    
    def upstream_and_inputs_and_fuel_po4(
        self,
        diesel_kg,
        elec_kwh,
        total_n_fert,
        total_urea,
        total_urea_abated,
        total_p_fert,
        total_k_fert,
        total_lime_fert,
    ):
        """
        Calculates total phosphorus emissions from upstream activities, inputs, and fuel related to livestock production.
        
        Parameters:
            diesel_kg, elec_kwh, total_n_fert, total_urea, total_urea_abated, total_p_fert, total_k_fert, total_lime_fert: Quantities of inputs used.
        
        Returns:
            Total phosphorus emissions from upstream activities.
        """
        return (
            self.upstream_class.diesel_PO4(diesel_kg)
            + self.upstream_class.elec_CO2(elec_kwh)
            + self.upstream_class.fert_upstream_CO2(
                total_n_fert,
                total_urea,
                total_urea_abated,
                total_p_fert,
                total_k_fert,
                total_lime_fert,
            )
        )
    
    def po4_from_concentrate_production(self, animal):
        """
        Calculates the total phosphorus emissions (PO4 equivalent) resulting from the production of concentrate feeds used in animal diet.
        This method considers the entire lifecycle of concentrate production including the acquisition of raw materials, processing, and transportation.

        Parameters:
            animal: An object representing the animal cohort, containing data related to the type and amount of concentrate consumed.

        Returns:
            The total phosphorus emissions (PO4 equivalent) from concentrate production for the given animal cohort over a specified period, contributing to the eutrophication potential of the system.
        """
        return self.upstream_class.po4_from_concentrate_production(animal)


###############################################################################
# Air Quality Ammonia
###############################################################################


class AirQualityTotals:
    """
    This class calculates the total ammonia (NH3) emissions contributing to air quality impacts from various farm management practices including manure management, soil management, and fertilization strategies. The calculations are based on the lifecycle of animal cohorts and their feed, manure handling practices, as well as fertiliser application rates.

    Attributes:
    ----------
        data_manager_class (LCADataManager): A class instance that provides access to necessary emission factors and data specific to a given country or region.
        grazing_class (GrazingStage): A class instance to calculate emissions from grazing practices.
        housing_class (HousingStage): A class instance to calculate emissions from animal housing practices.
        storage_class (StorageStage): A class instance to calculate emissions from manure storage practices.
        spread_class (DailySpread): A class instance to calculate emissions from manure spreading practices.
        fertiliser_class (FertiliserInputs): A class instance to calculate emissions from fertiliser application.
    """
    def __init__(self, ef_country):
        self.data_manager_class = LCADataManager(ef_country)
        self.grazing_class = GrazingStage(ef_country)
        self.housing_class = HousingStage(ef_country)
        self.storage_class = StorageStage(ef_country)
        self.spread_class = DailySpread(ef_country)
        self.fertiliser_class = FertiliserInputs(ef_country)


    def create_emissions_dictionary(self, keys):
        """
        Creates a nested dictionary structure to store NH3 emission values from various sources categorized by specific keys (e.g., animal types).

        Parameters:
            keys (list): A list of string keys representing different emission categories or animal types.

        Returns:
            dict: A nested dictionary structured to hold emission values.
        """
        key_list = [
            "manure_management",
            "soils",
        ]

        keys_dict = dict.fromkeys(keys)

        emissions_dict = dict.fromkeys(key_list)

        for key in emissions_dict.keys():
            emissions_dict[key] = copy.deepcopy(keys_dict)
            for inner_k in keys_dict.keys():
                emissions_dict[key][inner_k] = 0

        return emissions_dict

    # Manure Management
    def total_manure_NH3_AQ(self, animal):
        """
        Calculates total NH3 emissions from manure management practices for the specified animal collection.

        Parameters:
            animal (Animal): An instance representing a specific animal collection.

        Returns:
            float: Total NH3 emissions (kg) from manure management for the specified animal collection.
        """
        NH3N = 0

        for key in animal.__dict__.keys():
            if (
                key in self.data_manager_class.get_cohort_keys()
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
        """
        Calculates total NH3 emissions from fertiliser application to soils.

        Parameters:
            total_urea (float): Total urea fertiliser applied (kg).
            total_urea_abated (float): Total abated urea fertiliser applied (kg).
            total_n_fert (float): Total nitrogen fertiliser applied (kg).

        Returns:
            float: Total NH3 emissions (kg) from fertiliser application to soils.
        """
        NH3N = self.fertiliser_class.urea_NH3(
            total_urea, total_urea_abated
        ) + self.fertiliser_class.n_fertiliser_NH3(total_n_fert)

        return NH3N

    def total_grazing_soils_NH3_AQ(self, animal):
        """
        Calculates total NH3 emissions from soils during grazing for the specified animal collection.

        Parameters:
            animal (Animal): An instance representing a specific animal collection.

        Returns:
            float: Total NH3 emissions (kg) from soils during grazing for the specified animal collection.
        """
        NH3N = 0

        for key in animal.__dict__.keys():
            if (
                key in self.data_manager_class.get_cohort_keys()
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
