"""
Cattle LCA Data Manager
------------------------

This module contains the LCADataManager class, which is responsible for aggregating and managing all data relevant 
to the life cycle assessment (LCA) of cattle within a specified region (Ireland). It consolidates emissions factors, 
animal characteristics, and other environmental impact parameters specific to various cattle cohorts (e.g., dairy cows, bulls, calves) 
and management practices (e.g., feeding, manure management). This centralized management supports the calculation and analysis of environmental 
impacts associated with different livestock management strategies.
"""
from cattle_lca.resource_manager.data_loader import Loader

class LCADataManager:
    """
    The LCADataManager class is responsible for aggregating and managing all data relevant to the life cycle assessment (LCA) of 
    cattle within a specified region (Ireland). It consolidates emissions factors, animal characteristics, and other environmental 
    impact parameters specific to various cattle cohorts (e.g., dairy cows, bulls, calves) and management practices (e.g., feeding, manure management). 
    This centralized management supports the calculation and analysis of environmental impacts associated with different livestock management strategies.

    The class utilizes data from the Loader class, which provides access to country-specific information. 
    This enables the LCADataManager to provide tailored data for accurate LCA modeling. 
    Parameters such as methane conversion factors, nitrogen retention rates, and energy coefficients are organized by cattle cohort, 
    allowing for detailed and nuanced environmental impact assessments.

    Through its methods, the LCADataManager offers an interface to retrieve specific data points necessary for LCA calculations, 
    such as greenhouse gas emissions, energy use, and nutrient balances. This supports the development of sustainable cattle farming practices 
    by providing the necessary data to assess environmental impacts and identify areas for improvement.

    Attributes:
        loader_class (Loader): An instance of the Loader class to load country-specific emissions factors and animal features.
        cohorts_data (dict): A comprehensive dictionary containing various parameters for different cattle cohorts.
        grazing_type (dict): Emissions factors associated with different types of grazing environments.
        milk_density (float): The average density of milk, critical for various calculations in LCA.
        fat (float): The average fat percentage in milk.
        storage_TAN (dict): Total Ammonia Nitrogen (TAN) factors for different manure storage types.
        storage_MCF (dict): Methane Conversion Factors (MCF) applicable to different storage scenarios.
        storage_N2O (dict): Nitrous Oxide (N2O) emissions factors for varying manure storage types.
        daily_spreading (dict): Ammonia emissions factors for different manure spreading practices.
    
    Args:
        ef_country (str): A country identifier used to load specific datasets applicable to the given region.
    """
    def __init__(self, ef_country):

        self.loader_class = Loader(ef_country)

        self.cohorts_data = {
            "dairy_cows": {
                "gender": "female",
                "methane_conversion_factor": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_dairy_cow,
                "N_retention": self.loader_class.animal_features.get_dairy_cows_n_retention,
                "total_ammonia_nitrogen": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
                "direct_n2o_emissions_factors": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
                "atmospheric_deposition": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
                "leaching": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
                "coefficient": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_lactating_cow,
                "weight_gain": self.loader_class.animal_features.get_dairy_cows_weight_gain,
                "growth": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_females,
                "mature_weight": self.loader_class.animal_features.get_mature_weight_dairy_cows,
                "pregnancy": self.loader_class.emissions_factors.get_ef_net_energy_for_pregnancy,
                "proportion_n2o_to_soils":self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils
            },
            "suckler_cows": {
                "gender": "female",
                "methane_conversion_factor": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_dairy_cow,  
                "N_retention": self.loader_class.animal_features.get_suckler_cows_n_retention,
                "total_ammonia_nitrogen": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
                "direct_n2o_emissions_factors": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
                "atmospheric_deposition": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
                "leaching": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
                "coefficient": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_lactating_cow, 
                "weight_gain": self.loader_class.animal_features.get_suckler_cows_weight_gain,
                "growth": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_females,
                "mature_weight": self.loader_class.animal_features.get_mature_weight_suckler_cows,
                "pregnancy": self.loader_class.emissions_factors.get_ef_net_energy_for_pregnancy,
                "proportion_n2o_to_soils":self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils
            },
            "bulls": {
                "gender": "male",
                "methane_conversion_factor": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_bulls,
                "N_retention": self.loader_class.animal_features.get_bulls_n_retention,
                "total_ammonia_nitrogen": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
                "direct_n2o_emissions_factors": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
                "atmospheric_deposition": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
                "leaching": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
                "coefficient": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_bulls,
                "weight_gain": self.loader_class.animal_features.get_bulls_weight_gain,
                "growth": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_bulls,
                "mature_weight": self.loader_class.animal_features.get_mature_weight_bulls,
                "pregnancy": None,
                "proportion_n2o_to_soils":self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils
                
            },
            
            "DxD_calves_m": {
                "gender": "male",
                "methane_conversion_factor": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_calves,
                "N_retention": self.loader_class.animal_features.get_DxD_calves_m_n_retention,
                "total_ammonia_nitrogen": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
                "direct_n2o_emissions_factors": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
                "atmospheric_deposition": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
                "leaching": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
                "coefficient": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow,
                "weight_gain": self.loader_class.animal_features.get_DxD_calves_m_weight_gain,
                "growth": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_castrates,
                "mature_weight": self.loader_class.animal_features.get_mature_weight_bulls,
                "pregnancy": None,
                "proportion_n2o_to_soils":self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils
            },
            "DxD_calves_f": {
                "gender":"female",
                "methane_conversion_factor": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_calves,
                "N_retention": self.loader_class.animal_features.get_DxD_calves_f_n_retention,
                "total_ammonia_nitrogen": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
                "direct_n2o_emissions_factors": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
                "atmospheric_deposition": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
                "leaching": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
                "coefficient": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow,
                "weight_gain": self.loader_class.animal_features.get_DxD_calves_f_weight_gain,
                "growth": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_females,
                "mature_weight": self.loader_class.animal_features.get_mature_weight_dairy_cows,
                "pregnancy": None,
                "proportion_n2o_to_soils":self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils
            },
            "DxB_calves_m": {
                "gender":"male",
                "methane_conversion_factor": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_calves,
                "N_retention": self.loader_class.animal_features.get_DxB_calves_m_n_retention,
                "total_ammonia_nitrogen": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
                "direct_n2o_emissions_factors": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
                "atmospheric_deposition": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
                "leaching": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
                "coefficient": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow,
                "weight_gain": self.loader_class.animal_features.get_DxB_calves_m_weight_gain,
                "growth": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_castrates,
                "mature_weight": self.loader_class.animal_features.get_mature_weight_bulls,
                "pregnancy": None,
                "proportion_n2o_to_soils":self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils
            },
            "DxB_calves_f": {
                "gender":"female",
                "methane_conversion_factor": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_calves,
                "N_retention": self.loader_class.animal_features.get_DxB_calves_f_n_retention,
                "total_ammonia_nitrogen": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
                "direct_n2o_emissions_factors": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
                "atmospheric_deposition": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
                "leaching": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
                "coefficient": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow,
                "weight_gain": self.loader_class.animal_features.get_DxB_calves_f_weight_gain,
                "growth": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_females,
                "mature_weight": self.mature_weight_average,
                "pregnancy": None,
                "proportion_n2o_to_soils":self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils
            },
            "BxB_calves_m": {
                "gender":"male",
                "methane_conversion_factor": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_calves,
                "N_retention": self.loader_class.animal_features.get_BxB_calves_m_n_retention,
                "total_ammonia_nitrogen": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
                "direct_n2o_emissions_factors": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
                "atmospheric_deposition": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
                "leaching": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
                "coefficient": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow,
                "weight_gain": self.loader_class.animal_features.get_BxB_calves_m_weight_gain,
                "growth": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_castrates,
                "mature_weight": self.loader_class.animal_features.get_mature_weight_bulls,
                "pregnancy": None,
                "proportion_n2o_to_soils":self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils
            },
            "BxB_calves_f": {
                "gender":"female",
                "methane_conversion_factor": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_calves,
                "N_retention": self.loader_class.animal_features.get_BxB_calves_f_n_retention,
                "total_ammonia_nitrogen": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
                "direct_n2o_emissions_factors": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
                "atmospheric_deposition": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
                "leaching": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
                "coefficient": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow,
                "weight_gain": self.loader_class.animal_features.get_BxB_calves_f_weight_gain,
                "growth": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_females,
                "mature_weight": self.loader_class.animal_features.get_mature_weight_suckler_cows,
                "pregnancy": None,
                "proportion_n2o_to_soils":self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils
            },
            "DxD_heifers_less_2_yr": {
                "gender":"female",
                "methane_conversion_factor": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_dairy_cow,
                "N_retention": self.loader_class.animal_features.get_DxD_heifers_less_2_yr_n_retention,
                "total_ammonia_nitrogen": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
                "direct_n2o_emissions_factors": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
                "atmospheric_deposition": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
                "leaching": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
                "coefficient": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow,
                "weight_gain": self.loader_class.animal_features.get_DxD_heifers_less_2_yr_weight_gain,
                "growth": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_females,
                "mature_weight": self.loader_class.animal_features.get_mature_weight_dairy_cows,
                "pregnancy": None,
                "proportion_n2o_to_soils":self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils
            },
            "DxD_steers_less_2_yr": {
                "gender":"male",
                "methane_conversion_factor": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_steer,
                "N_retention": self.loader_class.animal_features.get_DxD_steers_less_2_yr_n_retention,
                "total_ammonia_nitrogen": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
                "direct_n2o_emissions_factors": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
                "atmospheric_deposition": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
                "leaching": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
                "coefficient": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow,
                "weight_gain": self.loader_class.animal_features.get_DxD_steers_less_2_yr_weight_gain,
                "growth": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_castrates,
                "mature_weight": self.loader_class.animal_features.get_mature_weight_bulls,
                "pregnancy": None,
                "proportion_n2o_to_soils":self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils
            },
            "DxB_heifers_less_2_yr": {
                "gender":"female",
                "methane_conversion_factor": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_dairy_cow,
                "N_retention": self.loader_class.animal_features.get_DxB_heifers_less_2_yr_n_retention,
                "total_ammonia_nitrogen": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
                "direct_n2o_emissions_factors": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
                "atmospheric_deposition": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
                "leaching": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
                "coefficient": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow,
                "weight_gain": self.loader_class.animal_features.get_DxB_heifers_less_2_yr_weight_gain,
                "growth": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_females,
                "mature_weight": self.mature_weight_average,
                "pregnancy": None,
                "proportion_n2o_to_soils":self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils
            },
            "DxB_steers_less_2_yr": {
                "gender":"male",
                "methane_conversion_factor": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_steer,
                "N_retention": self.loader_class.animal_features.get_DxB_steers_less_2_yr_n_retention,
                "total_ammonia_nitrogen": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
                "direct_n2o_emissions_factors": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
                "atmospheric_deposition": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
                "leaching": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
                "coefficient": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow,
                "weight_gain": self.loader_class.animal_features.get_DxB_steers_less_2_yr_weight_gain,
                "growth": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_castrates,
                "mature_weight": self.loader_class.animal_features.get_mature_weight_bulls,
                "pregnancy": None,
                "proportion_n2o_to_soils":self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils

            },
            "BxB_heifers_less_2_yr": {
                "gender":"female",
                "methane_conversion_factor": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_dairy_cow,
                "N_retention": self.loader_class.animal_features.get_BxB_heifers_less_2_yr_n_retention,
                "total_ammonia_nitrogen": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
                "direct_n2o_emissions_factors": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
                "atmospheric_deposition": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
                "leaching": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
                "coefficient": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow,
                "weight_gain": self.loader_class.animal_features.get_BxB_heifers_less_2_yr_weight_gain,
                "growth": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_females,
                "mature_weight": self.loader_class.animal_features.get_mature_weight_suckler_cows,
                "pregnancy": None,
                "proportion_n2o_to_soils":self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils
            },
            "BxB_steers_less_2_yr": {
                "gender":"male",
                "methane_conversion_factor": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_steer,
                "N_retention": self.loader_class.animal_features.get_BxB_steers_less_2_yr_n_retention,
                "total_ammonia_nitrogen": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
                "direct_n2o_emissions_factors": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
                "atmospheric_deposition": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
                "leaching": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
                "coefficient": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow,
                "weight_gain": self.loader_class.animal_features.get_BxB_steers_less_2_yr_weight_gain,
                "growth": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_castrates,
                "mature_weight": self.loader_class.animal_features.get_mature_weight_bulls,
                "pregnancy": None,
                "proportion_n2o_to_soils":self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils
            },
            "DxD_heifers_more_2_yr": {
                "gender":"female",
                "methane_conversion_factor": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_dairy_cow,
                "N_retention": self.loader_class.animal_features.get_DxD_heifers_more_2_yr_n_retention,
                "total_ammonia_nitrogen": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
                "direct_n2o_emissions_factors": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
                "atmospheric_deposition": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
                "leaching": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
                "coefficient": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow,
                "weight_gain": self.loader_class.animal_features.get_DxD_heifers_more_2_yr_weight_gain,
                "growth": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_females,
                "mature_weight": self.loader_class.animal_features.get_mature_weight_dairy_cows,
                "pregnancy": None,
                "proportion_n2o_to_soils":self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils
            },
            "DxD_steers_more_2_yr": {
                "gender":"male",
                "methane_conversion_factor": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_steer,
                "N_retention": self.loader_class.animal_features.get_DxD_steers_more_2_yr_n_retention,
                "total_ammonia_nitrogen": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
                "direct_n2o_emissions_factors": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
                "atmospheric_deposition": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
                "leaching": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
                "coefficient": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow,
                "weight_gain": self.loader_class.animal_features.get_DxD_steers_more_2_yr_weight_gain,
                "growth": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_castrates,
                "mature_weight": self.loader_class.animal_features.get_mature_weight_bulls,
                "pregnancy": None,
                "proportion_n2o_to_soils":self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils
            },
            "DxB_heifers_more_2_yr": {
                "gender":"female",
                "methane_conversion_factor": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_dairy_cow,
                "N_retention": self.loader_class.animal_features.get_DxB_heifers_more_2_yr_n_retention,
                "total_ammonia_nitrogen": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
                "direct_n2o_emissions_factors": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
                "atmospheric_deposition": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
                "leaching": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
                "coefficient": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow,
                "weight_gain": self.loader_class.animal_features.get_DxB_heifers_more_2_yr_weight_gain,
                "growth": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_females,
                "mature_weight": self.mature_weight_average,
                "pregnancy": None,
                "proportion_n2o_to_soils":self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils
            },
            "DxB_steers_more_2_yr": {
                "gender":"male",
                "methane_conversion_factor": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_steer,
                "N_retention": self.loader_class.animal_features.get_DxB_steers_more_2_yr_n_retention,
                "total_ammonia_nitrogen": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
                "direct_n2o_emissions_factors": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
                "atmospheric_deposition": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
                "leaching": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
                "coefficient": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow,
                "weight_gain": self.loader_class.animal_features.get_DxB_steers_more_2_yr_weight_gain,
                "growth": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_castrates,
                "mature_weight": self.loader_class.animal_features.get_mature_weight_bulls,
                "pregnancy": None,
                "proportion_n2o_to_soils":self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils
            },
            "BxB_heifers_more_2_yr": {
                "gender":"female",
                "methane_conversion_factor": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_dairy_cow,
                "N_retention": self.loader_class.animal_features.get_BxB_heifers_more_2_yr_n_retention,
                "total_ammonia_nitrogen": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
                "direct_n2o_emissions_factors": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
                "atmospheric_deposition": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
                "leaching": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
                "coefficient": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow,
                "weight_gain": self.loader_class.animal_features.get_BxB_heifers_more_2_yr_weight_gain,
                "growth": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_females,
                "mature_weight": self.loader_class.animal_features.get_mature_weight_suckler_cows,
                "pregnancy": None,
                "proportion_n2o_to_soils":self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils
            },
            "BxB_steers_more_2_yr": {
                "gender":"male",
                "methane_conversion_factor": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_steer,
                "N_retention": self.loader_class.animal_features.get_BxB_steers_more_2_yr_n_retention,
                "total_ammonia_nitrogen": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
                "direct_n2o_emissions_factors": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
                "atmospheric_deposition": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
                "leaching": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
                "coefficient": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow,
                "weight_gain": self.loader_class.animal_features.get_BxB_steers_more_2_yr_weight_gain,
                "growth": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_castrates,
                "mature_weight": self.loader_class.animal_features.get_mature_weight_bulls,
                "pregnancy": None,
                "proportion_n2o_to_soils":self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils
            },
            "DxD_heifers_more_2_yr": {
                "gender":"female",
                "methane_conversion_factor": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_dairy_cow,
                "N_retention": self.loader_class.animal_features.get_DxD_heifers_more_2_yr_n_retention,
                "total_ammonia_nitrogen": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
                "direct_n2o_emissions_factors": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
                "atmospheric_deposition": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
                "leaching": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
                "coefficient": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow,
                "weight_gain": self.loader_class.animal_features.get_DxD_heifers_more_2_yr_weight_gain,
                "growth": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_females,
                "mature_weight": self.loader_class.animal_features.get_mature_weight_dairy_cows,
                "pregnancy": None,
                "proportion_n2o_to_soils":self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils
            },
            "DxD_steers_more_2_yr": {
                "gender":"male",
                "methane_conversion_factor": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_steer,
                "N_retention": self.loader_class.animal_features.get_DxD_steers_more_2_yr_n_retention,
                "total_ammonia_nitrogen": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
                "direct_n2o_emissions_factors": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
                "atmospheric_deposition": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
                "leaching": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
                "coefficient": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow,
                "weight_gain": self.loader_class.animal_features.get_DxD_steers_more_2_yr_weight_gain,
                "growth": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_castrates,
                "mature_weight": self.loader_class.animal_features.get_mature_weight_bulls,
                "pregnancy": None,
                "proportion_n2o_to_soils":self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils
            },
            "DxB_heifers_more_2_yr": {
                "gender":"female",
                "methane_conversion_factor": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_dairy_cow,
                "N_retention": self.loader_class.animal_features.get_DxB_heifers_more_2_yr_n_retention,
                "total_ammonia_nitrogen": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
                "direct_n2o_emissions_factors": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
                "atmospheric_deposition": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
                "leaching": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
                "coefficient": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow,
                "weight_gain": self.loader_class.animal_features.get_DxB_heifers_more_2_yr_weight_gain,
                "growth": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_females,
                "mature_weight": self.mature_weight_average,
                "pregnancy": None,
                "proportion_n2o_to_soils":self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils

            },
            "DxB_steers_more_2_yr": {
                "gender":"male",
                "methane_conversion_factor": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_steer,
                "N_retention": self.loader_class.animal_features.get_DxB_steers_more_2_yr_n_retention,
                "total_ammonia_nitrogen": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
                "direct_n2o_emissions_factors": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
                "atmospheric_deposition": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
                "leaching": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
                "coefficient": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow,
                "weight_gain": self.loader_class.animal_features.get_DxB_steers_more_2_yr_weight_gain,
                "growth": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_castrates,
                "mature_weight": self.loader_class.animal_features.get_mature_weight_bulls,
                "pregnancy": None,
                "proportion_n2o_to_soils":self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils
            },
            "BxB_heifers_more_2_yr": {
                "gender":"female",
                "methane_conversion_factor": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_dairy_cow,
                "N_retention": self.loader_class.animal_features.get_BxB_heifers_more_2_yr_n_retention,
                "total_ammonia_nitrogen": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
                "direct_n2o_emissions_factors": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
                "atmospheric_deposition": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
                "leaching": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
                "coefficient": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow,
                "weight_gain": self.loader_class.animal_features.get_BxB_heifers_more_2_yr_weight_gain,
                "growth": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_females,
                "mature_weight": self.loader_class.animal_features.get_mature_weight_suckler_cows,
                "pregnancy": None,
                "proportion_n2o_to_soils":self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils
            },
            "BxB_steers_more_2_yr": {
                "gender":"male",   
                "methane_conversion_factor": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_steer,
                "N_retention": self.loader_class.animal_features.get_BxB_steers_more_2_yr_n_retention,
                "total_ammonia_nitrogen": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
                "direct_n2o_emissions_factors": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
                "atmospheric_deposition": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
                "leaching": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
                "coefficient": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow,
                "weight_gain": self.loader_class.animal_features.get_BxB_steers_more_2_yr_weight_gain,
                "growth": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_castrates,
                "mature_weight": self.loader_class.animal_features.get_mature_weight_bulls,
                "pregnancy": None,
                "proportion_n2o_to_soils":self.loader_class.emissions_factors.get_ef_direct_n2o_emissions_soils
            }

        }

        self.grazing_type = {
            "pasture": self.loader_class.emissions_factors.get_ef_feeding_situation_pasture,
            "large area": self.loader_class.emissions_factors.get_ef_feeding_situation_large_area,
            "stall": self.loader_class.emissions_factors.get_ef_feeding_situation_stall,
        }


        self.milk_density = 1.033  # kg/l

        self.fat = 3.5  # %


        self.storage_TAN = {
            "tank solid": self.loader_class.emissions_factors.get_ef_TAN_house_liquid,
            "tank liquid": self.loader_class.emissions_factors.get_ef_TAN_house_liquid,
            "solid": self.loader_class.emissions_factors.get_ef_TAN_house_solid,
            "biodigester": self.loader_class.emissions_factors.get_ef_TAN_storage_tank,
        }

        self.storage_MCF = {
            "tank solid": self.loader_class.emissions_factors.get_ef_mcf_liquid_tank,
            "tank liquid": self.loader_class.emissions_factors.get_ef_mcf_liquid_tank,
            "solid": self.loader_class.emissions_factors.get_ef_mcf_solid_storage,
            "biodigester": self.loader_class.emissions_factors.get_ef_mcf_anaerobic_digestion,
        }

        self.storage_N2O = {
            "tank solid": self.loader_class.emissions_factors.get_ef_n2o_direct_storage_tank_solid,  # crust cover for ireland
            "tank liquid": self.loader_class.emissions_factors.get_ef_n2o_direct_storage_tank_liquid,
            "solid": self.loader_class.emissions_factors.get_ef_n2o_direct_storage_solid,
            "biodigester": self.loader_class.emissions_factors.get_ef_n2o_direct_storage_tank_anaerobic_digestion,
        }

        self.daily_spreading = {
            "none": self.loader_class.emissions_factors.get_ef_nh3_daily_spreading_none,
            "manure": self.loader_class.emissions_factors.get_ef_nh3_daily_spreading_manure,
            "broadcast": self.loader_class.emissions_factors.get_ef_nh3_daily_spreading_broadcast,
            "injection": self.loader_class.emissions_factors.get_ef_nh3_daily_spreading_injection,
            "trailing hose": self.loader_class.emissions_factors.get_ef_nh3_daily_spreading_traling_hose,
        }


    def mature_weight_average(self):
        """
        Calculates the average mature weight of dairy and suckler cows. This is used for cohorts where specific mature weight data is not available.
        
        Returns:
            float: The average mature weight of dairy and suckler cows.
        """
        return (self.loader_class.animal_features.get_mature_weight_suckler_cows() + self.loader_class.animal_features.get_mature_weight_dairy_cows()) / 2
    

    def get_cohort_keys(self):
        """
        Retrieves the keys (names) of all cattle cohorts available in the data.
        
        Returns:
            list: A list of all cattle cohort names.
        """
        return self.cohorts_data.keys()
    

    def get_cohort_parameter(self, cohort, parameter):
        """
        Retrieves a specific parameter value for a given cattle cohort.

        Args:
            cohort (str): The name of the cattle cohort.
            parameter (str): The parameter to retrieve from the cohort data.
        
        Returns:
            Various: The value of the requested parameter for the specified cohort.
        """
        return self.cohorts_data[cohort][parameter]
    

    def get_grazing_type(self, grazing_type):
        """
        Retrieves the coefficient for a specific type of grazing.

        Args:
            grazing_type (str): The type of grazing (e.g., 'pasture', 'large area').
        
        Returns:
            float: The coefficient associated with the specified type of grazing.
        """
        return self.grazing_type[grazing_type]
    

    def get_milk_density(self):
        """
        Retrieves the density of milk.

        Returns:
            float: The density of milk in kg/l.
        """
        return self.milk_density
    

    def get_fat(self):
        """
        Retrieves the fat content of milk.

        Returns:
            float: The fat content of milk as a percentage.
        """
        return self.fat
    

    def get_concentrate_digestibility(self, con_type):
        """
        Retrieves the dry matter digestibility of a concentrate type.

        Args:
            con_type (str): The type of concentrate.

        Returns:
            float: The dry matter digestibility of the specified concentrate type.
        """
        return self.loader_class.concentrates.get_con_dry_matter_digestibility(con_type)
    

    def get_con_dry_matter_gross_energy(self, con_type):
        """
        Retrieves the gross energy of a concentrate type.

        Args:
            con_type (str): The type of concentrate.

        Returns:   
            float: The gross energy of the specified concentrate type in MJ/kg dry matter.
        """
        return self.loader_class.concentrates.get_gross_energy_mje_dry_matter(con_type)
    

    def get_forage_digestibility(self, forage):
        """
        Retrieves the dry matter digestibile energy proportion of gross energy of a forage type.

        Args:
            forage (str): The type of forage.

        Returns:
            float: The dry matter digestibile energy proportion of gross energy of the specified forage type.
        """
        return self.loader_class.grass.get_forage_dry_matter_digestibility(forage)
    

    def get_grass_dry_matter_gross_energy(self, forage):
        """
        Retrieves the gross energy of a forage type.

        Args:
            forage (str): The type of forage.

        Returns:
            float: The gross energy of the specified forage type in MJ/kg dry matter.
        """
        return self.loader_class.grass.get_gross_energy_mje_dry_matter(forage)
    

    def get_grass_crude_protein(self, forage):
        """
        Retrieves the crude protein content of a forage type.

        Args:
            forage (str): The type of forage.

        Returns:
            float: The crude protein content of the specified forage type.
        """
        return self.loader_class.grass.get_crude_protein(forage)


    def get_concentrate_crude_protein(self, con_type):
        """
        Retrieves the crude protein content of a concentrate type.

        Args:
            con_type (str): The type of concentrate.

        Returns:
            float: The crude protein content of the specified concentrate type.
        """
        return self.loader_class.concentrates.get_con_crude_protein(con_type)
    

    def get_concentrate_digestable_energy(self, con_type):
        """
        Retrieves the digestible energy proprotion of gross energy available of a concentrate type.

        Args:
            con_type (str): The type of concentrate.

        Returns:
            float: The digestible energy proportion of the specified concentrate type.
        """
        return self.loader_class.concentrates.get_con_digestible_energy(con_type)
    
    def get_storage_TAN(self, storage_type):
        """
        Retrieves the emissions factor for TAN storage.

        Args:
            storage_type (str): The type of storage (e.g., 'tank solid', 'solid').

        Returns:
            float: The emissions factor for the specified type of TAN storage.
        """
        return self.storage_TAN[storage_type]
    
    
    def get_storage_MCF(self, storage_type):
        """
        Retrieves the emissions factor for MCF storage.

        Args:
            storage_type (str): The type of storage (e.g., 'tank solid', 'solid').

        Returns:
            float: The emissions factor for the specified type of MCF storage.
        """
        return self.storage_MCF[storage_type]
    

    def get_storage_N2O(self, storage_type):
        """
        Retrieves the emissions factor for N2O storage.

        Args:
            storage_type (str): The type of storage (e.g., 'tank solid', 'solid').

        Returns:
            float: The emissions factor for the specified type of N2O storage.
        """
        return self.storage_N2O[storage_type]
    

    def get_daily_spreading(self, spreading_type):
        """
        Retrieves the emissions factor for daily spreading.

        Args:
            spreading_type (str): The type of spreading (e.g., 'none', 'manure').

        Returns:
            float: The emissions factor for the specified type of daily spreading.
        """
        return self.daily_spreading[spreading_type]
    

    def get_ef_urea(self):
        """
        Retrieves the emissions factor for urea.

        Returns:
            float: The emissions factor for urea.
        """
        return self.loader_class.emissions_factors.get_ef_urea()
    

    def get_ef_urea_abated(self):
        """
        Retrieves the emissions factor for abated urea.

        Returns:
            float: The emissions factor for abated urea.
        """
        return self.loader_class.emissions_factors.get_ef_urea_and_nbpt()
    

    def get_ef_urea_to_nh3_and_nox(self):
        """
        Retrieves the emissions factor for urea to NH3 and NOx.

        Returns:
            float: The emissions factor for urea to NH3 and NOx.
        """
        return self.loader_class.emissions_factors.get_ef_fracGASF_urea_fertilisers_to_nh3_and_nox()
    

    def get_ef_urea_abated_to_nh3_and_nox(self):
        """
        Retrieves the emissions factor for abated urea to NH3 and NOx.

        Returns:
            float: The emissions factor for abated urea to NH3 and NOx.
        """
        return self.loader_class.emissions_factors.get_ef_fracGASF_urea_and_nbpt_to_nh3_and_nox()


    def get_ef_fration_leach_runoff(self):
        """
        Retrieves the fraction of leaching and runoff.

        Returns:
            float: The fraction of leaching and runoff.

        """
        return self.loader_class.emissions_factors.get_ef_frac_leach_runoff()
    

    def get_indirect_atmospheric_deposition(self):
        """
        Retrieves the emissions factor for indirect N2O from atmospheric deposition to soils and water.

        Returns:
            float: The emissions factor for indirect N2O from atmospheric deposition to soils and water.
        """
        return self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water()
    

    def get_indirect_leaching(self):
        """
        Retrieves the emissions factor for indirect N2O from leaching and runoff.

        Returns:
            float: The emissions factor for indirect N2O from leaching and runoff.
        """
        return self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff()


    def get_ef_urea_co2(self):
        """
        Retrieves the emissions factor for CO2 from urea.

        Returns:
            float: The emissions factor for CO2 from urea.
        """
        return float(self.loader_class.emissions_factors.get_ef_urea_co2())
    

    def get_ef_lime_co2(self):
        """
        Retrieves the emissions factor for CO2 from lime.

        Returns:
            float: The emissions factor for CO2 from lime.
        """
        return float(self.loader_class.emissions_factors.get_ef_lime_co2())
    

    def get_frac_p_leach(self):
        """
        Retrieves the fraction of P leaching.

        Returns:
            float: The fraction of P leaching.
        """
        return float(self.loader_class.emissions_factors.get_ef_Frac_P_Leach())
    

    def get_ef_AN_fertiliser(self):
        """
        Retrieves the emissions factor for ammonium nitrate fertiliser.

        Returns:
            float: The emissions factor for ammonium nitrate fertiliser.
        """
        return self.loader_class.emissions_factors.get_ef_ammonium_nitrate()
    

    def get_ef_AN_fertiliser_to_nh3_and_nox(self):
        """
        Retrieves the emissions factor for ammonium nitrate fertiliser to NH3 and NOx.

        Returns:
            float: The emissions factor for ammonium nitrate fertiliser to NH3 and NOx.
        """
        return self.loader_class.emissions_factors.get_ef_fracGASF_ammonium_fertilisers_to_nh3_and_nox()
    

    def get_upstream_diesel_co2e_indirect(self):
        """
        Retrieves the upstream emissions co2e factor for diesel (indirect).

        Returns:
            float: The upstream emissions co2e factor for diesel (indirect).
        """
        return self.loader_class.upstream.get_upstream_kg_co2e(
            "diesel_indirect"
        )
    

    def get_upstream_diesel_co2e_direct(self):
        """
        Retrieves the upstream emissions co2e factor for diesel (direct).

        Returns:
            float: The upstream emissions co2e factor for diesel (direct).
        """
        return self.loader_class.upstream.get_upstream_kg_co2e("diesel_direct")
    

    def get_upstream_diesel_po4e_indirect(self):
        """
        Retrieves the upstream emissions po4e factor for diesel (indirect).

        Returns:
            float: The upstream emissions po4e factor for diesel (indirect).
        """
        return self.loader_class.upstream.get_upstream_kg_po4e(
            "diesel_indirect"
        )
    

    def get_upstream_diesel_po4e_direct(self):
        """
        Retrieves the upstream emissions po4e factor for diesel (direct).

        Returns:
            float: The upstream emissions po4e factor for diesel (direct).
        """
        return self.loader_class.upstream.get_upstream_kg_po4e("diesel_direct")
    

    def get_upstream_electricity_co2e(self):
        """
        Retrieves the upstream emissions co2e factor for electricity.

        Returns:
            float: The upstream emissions co2e factor for electricity.
        """
        return self.loader_class.upstream.get_upstream_kg_co2e("electricity_consumed"
        )  # based on Norway hydropower
    

    def get_upstream_electricity_po4e(self):
        """
        Retrieves the upstream emissions po4e factor for electricity.

        Returns:
            float: The upstream emissions po4e factor for electricity.
        """
        return self.loader_class.upstream.get_upstream_kg_po4e("electricity_consumed") # based on Norway hydropower
    

    def get_upstream_AN_fertiliser_co2e(self):
        """
        Retrieves the upstream emissions co2e factor for ammonium nitrate fertiliser.

        Returns:
            float: The upstream emissions co2e factor for ammonium nitrate fertiliser.
        """
        return self.loader_class.upstream.get_upstream_kg_co2e("ammonium_nitrate_fertiliser")
    

    def get_upstream_urea_fertiliser_co2e(self):
        """
        Retrieves the upstream emissions co2e factor for urea fertiliser.

        Returns:
            float: The upstream emissions co2e factor for urea fertiliser.
        """
        return self.loader_class.upstream.get_upstream_kg_co2e("urea_fert")
    
    
    def get_upstream_triple_phosphate_co2e(self):
        """
        Retrieves the upstream emissions co2e factor for triple superphosphate.

        Returns:
            float: The upstream emissions co2e factor for triple superphosphate.
        """
        return self.loader_class.upstream.get_upstream_kg_co2e("triple_superphosphate")
    

    def get_upstream_potassium_chloride_co2e(self):
        """
        Retrieves the upstream emissions co2e factor for potassium chloride.

        Returns:
            float: The upstream emissions co2e factor for potassium chloride.
        """
        return self.loader_class.upstream.get_upstream_kg_co2e("potassium_chloride")
    

    def get_upstream_lime_co2e(self):
        """
        Retrieves the upstream emissions co2e factor for lime.

        Returns:
            float: The upstream emissions co2e factor for lime.
        """
        return self.loader_class.upstream.get_upstream_kg_co2e("lime")
    

    def get_upstream_AN_fertiliser_po4e(self):
        """
        Retrieves the upstream emissions po4e factor for ammonium nitrate fertiliser.

        Returns:
            float: The upstream emissions po4e factor for ammonium nitrate fertiliser.
        """
        return  self.loader_class.upstream.get_upstream_kg_po4e(
            "ammonium_nitrate_fertiliser"
        )  
    

    def get_upstream_urea_fertiliser_po4e(self):
        """
        Retrieves the upstream emissions po4e factor for urea fertiliser.

        Returns:
            float: The upstream emissions po4e factor for urea fertiliser.
        """
        return  self.loader_class.upstream.get_upstream_kg_po4e(
            "urea_fert"
        )
    
    def get_upstream_triple_phosphate_po4e(self):
        """
        Retrieves the upstream emissions po4e factor for triple superphosphate.

        Returns:
            float: The upstream emissions po4e factor for triple superphosphate.
        """
        return  self.loader_class.upstream.get_upstream_kg_po4e(
            "triple_superphosphate"
        )
    
    def get_upstream_potassium_chloride_po4e(self):
        """
        Retrieves the upstream emissions po4e factor for potassium chloride.

        Returns:
            float: The upstream emissions po4e factor for potassium chloride.
        """
        return  self.loader_class.upstream.get_upstream_kg_po4e(
            "potassium_chloride"
        )
    
    def get_upstream_lime_po4e(self):
        """
        Retrieves the upstream emissions po4e factor for lime.

        Returns:
            float: The upstream emissions po4e factor for lime.
        """
        return  self.loader_class.upstream.get_upstream_kg_po4e(
            "lime"
        )

    def get_upstream_concentrate_co2e(self, con_type):
        """
        Retrieves the upstream emissions co2e factor for concentrate.

        Returns:
            float: The upstream emissions co2e factor for concentrate.
        """
        return self.loader_class.concentrates.get_con_co2_e(con_type)
    
    def get_upstream_concentrate_po4e(self, con_type):
        """
        Retrieves the upstream emissions po4e factor for concentrate.

        Returns:
            float: The upstream emissions po4e factor for concentrate.
        """
        return self.loader_class.concentrates.get_con_po4_e(con_type)
    






