import unittest
from cattle_lca.resource_manager.cattle_lca_data_manager import LCADataManager  # Import your actual class module
from cattle_lca.resource_manager.data_loader import Loader


class TestDataStructureIntegrity(unittest.TestCase):

    def setUp(self):
        
        # Initialize your LCADataManager which should load your new data structure
        self.manager = LCADataManager("ireland")

        self.test_data = self.manager.cohorts_data

        self.loader_class = Loader("ireland")

        self.coefficient = {
            "dairy_cows": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_lactating_cow,
            "suckler_cows": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_lactating_cow,
            "bulls": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_bulls,
            "DxD_calves_m": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow,
            "DxD_calves_f": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow,
            "DxB_calves_m": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow,
            "DxB_calves_f": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow,
            "BxB_calves_m": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow,
            "BxB_calves_f": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow,
            "DxD_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow,
            "DxD_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow,
            "DxB_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow,
            "DxB_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow,
            "BxB_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow,
            "BxB_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow,
            "DxD_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow,
            "DxD_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow,
            "DxB_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow,
            "DxB_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow,
            "BxB_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow,
            "BxB_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_maintenance_non_lactating_cow,
            }
        
        self.weight_gain = {
            "dairy_cows": self.loader_class.animal_features.get_dairy_cows_weight_gain,
            "suckler_cows": self.loader_class.animal_features.get_suckler_cows_weight_gain,
            "bulls": self.loader_class.animal_features.get_bulls_weight_gain,
            "DxD_calves_m": self.loader_class.animal_features.get_DxD_calves_m_weight_gain,
            "DxD_calves_f": self.loader_class.animal_features.get_DxD_calves_f_weight_gain,
            "DxB_calves_m": self.loader_class.animal_features.get_DxB_calves_m_weight_gain,
            "DxB_calves_f": self.loader_class.animal_features.get_DxB_calves_f_weight_gain,
            "BxB_calves_m": self.loader_class.animal_features.get_BxB_calves_m_weight_gain,
            "BxB_calves_f": self.loader_class.animal_features.get_BxB_calves_f_weight_gain,
            "DxD_heifers_less_2_yr": self.loader_class.animal_features.get_DxD_heifers_less_2_yr_weight_gain,
            "DxD_steers_less_2_yr": self.loader_class.animal_features.get_DxD_steers_less_2_yr_weight_gain,
            "DxB_heifers_less_2_yr": self.loader_class.animal_features.get_DxB_heifers_less_2_yr_weight_gain,
            "DxB_steers_less_2_yr": self.loader_class.animal_features.get_DxB_steers_less_2_yr_weight_gain,
            "BxB_heifers_less_2_yr": self.loader_class.animal_features.get_BxB_heifers_less_2_yr_weight_gain,
            "BxB_steers_less_2_yr": self.loader_class.animal_features.get_BxB_steers_less_2_yr_weight_gain,
            "DxD_heifers_more_2_yr": self.loader_class.animal_features.get_DxD_heifers_more_2_yr_weight_gain,
            "DxD_steers_more_2_yr": self.loader_class.animal_features.get_DxD_steers_more_2_yr_weight_gain,
            "DxB_heifers_more_2_yr": self.loader_class.animal_features.get_DxB_heifers_more_2_yr_weight_gain,
            "DxB_steers_more_2_yr": self.loader_class.animal_features.get_DxB_steers_more_2_yr_weight_gain,
            "BxB_heifers_more_2_yr": self.loader_class.animal_features.get_BxB_heifers_more_2_yr_weight_gain,
            "BxB_steers_more_2_yr": self.loader_class.animal_features.get_BxB_steers_more_2_yr_weight_gain,
        }

        self.growth = {
            "dairy_cows": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_females,
            "suckler_cows": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_females,
            "bulls": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_bulls,
            "DxD_calves_m": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_castrates,
            "DxD_calves_f": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_females,
            "DxB_calves_m": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_castrates,
            "DxB_calves_f": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_females,
            "BxB_calves_m": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_castrates,
            "BxB_calves_f": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_females,
            "DxD_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_females,
            "DxD_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_castrates,
            "DxB_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_females,
            "DxB_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_castrates,
            "BxB_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_females,
            "BxB_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_castrates,
            "DxD_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_females,
            "DxD_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_castrates,
            "DxB_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_females,
            "DxB_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_castrates,
            "BxB_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_females,
            "BxB_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_net_energy_for_growth_castrates,
        }

        self.methane_conversion_factor = {
            "dairy_cows": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_dairy_cow,
            "suckler_cows": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_dairy_cow,
            "bulls": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_bulls,
            "DxD_calves_m": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_calves,
            "DxD_calves_f": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_calves,
            "DxB_calves_m": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_calves,
            "DxB_calves_f": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_calves,
            "BxB_calves_m": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_calves,
            "BxB_calves_f": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_calves,
            "DxD_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_dairy_cow,
            "DxD_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_steer,
            "DxB_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_dairy_cow,
            "DxB_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_steer,
            "BxB_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_dairy_cow,
            "BxB_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_steer,
            "DxD_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_dairy_cow,
            "DxD_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_steer,
            "DxB_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_dairy_cow,
            "DxB_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_steer,
            "BxB_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_dairy_cow,
            "BxB_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_methane_conversion_factor_steer,
        }

        self.N_retention = {
            "dairy_cows": self.loader_class.animal_features.get_dairy_cows_n_retention,
            "suckler_cows": self.loader_class.animal_features.get_suckler_cows_n_retention,
            "bulls": self.loader_class.animal_features.get_bulls_n_retention,
            "DxD_calves_m": self.loader_class.animal_features.get_DxD_calves_m_n_retention,
            "DxD_calves_f": self.loader_class.animal_features.get_DxD_calves_f_n_retention,
            "DxB_calves_m": self.loader_class.animal_features.get_DxB_calves_m_n_retention,
            "DxB_calves_f": self.loader_class.animal_features.get_DxB_calves_f_n_retention,
            "BxB_calves_m": self.loader_class.animal_features.get_BxB_calves_m_n_retention,
            "BxB_calves_f": self.loader_class.animal_features.get_BxB_calves_f_n_retention,
            "DxD_heifers_less_2_yr": self.loader_class.animal_features.get_DxD_heifers_less_2_yr_n_retention,
            "DxD_steers_less_2_yr": self.loader_class.animal_features.get_DxD_steers_less_2_yr_n_retention,
            "DxB_heifers_less_2_yr": self.loader_class.animal_features.get_DxB_heifers_less_2_yr_n_retention,
            "DxB_steers_less_2_yr": self.loader_class.animal_features.get_DxB_steers_less_2_yr_n_retention,
            "BxB_heifers_less_2_yr": self.loader_class.animal_features.get_BxB_heifers_less_2_yr_n_retention,
            "BxB_steers_less_2_yr": self.loader_class.animal_features.get_BxB_steers_less_2_yr_n_retention,
            "DxD_heifers_more_2_yr": self.loader_class.animal_features.get_DxD_heifers_more_2_yr_n_retention,
            "DxD_steers_more_2_yr": self.loader_class.animal_features.get_DxD_steers_more_2_yr_n_retention,
            "DxB_heifers_more_2_yr": self.loader_class.animal_features.get_DxB_heifers_more_2_yr_n_retention,
            "DxB_steers_more_2_yr": self.loader_class.animal_features.get_DxB_steers_more_2_yr_n_retention,
            "BxB_heifers_more_2_yr": self.loader_class.animal_features.get_BxB_heifers_more_2_yr_n_retention,
            "BxB_steers_more_2_yr": self.loader_class.animal_features.get_BxB_steers_more_2_yr_n_retention,
        }

        self.total_ammonia_nitrogen = {
            "dairy_cows": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
            "suckler_cows": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
            "bulls": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
            "DxD_calves_m": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
            "DxD_calves_f": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
            "DxB_calves_m": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
            "DxB_calves_f": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
            "BxB_calves_m": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
            "BxB_calves_f": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
            "DxD_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
            "DxD_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
            "DxB_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
            "DxB_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
            "BxB_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
            "BxB_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
            "DxD_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
            "DxD_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
            "DxB_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
            "DxB_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
            "BxB_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
            "BxB_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
        }

        self.direct_n2o_emissions_factors = {
            "dairy_cows": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
            "suckler_cows": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
            "bulls": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
            "DxD_calves_m": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
            "DxD_calves_f": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
            "DxB_calves_m": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
            "DxB_calves_f": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
            "BxB_calves_m": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
            "BxB_calves_f": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
            "DxD_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
            "DxD_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
            "DxB_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
            "DxB_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
            "BxB_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
            "BxB_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
            "DxD_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
            "DxD_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
            "DxB_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
            "DxB_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
            "BxB_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
            "BxB_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
        }

        self.atmospheric_deposition = {
            "dairy_cows": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
            "suckler_cows": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
            "bulls": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
            "DxD_calves_m": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
            "DxD_calves_f": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
            "DxB_calves_m": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
            "DxB_calves_f": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
            "BxB_calves_m": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
            "BxB_calves_f": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
            "DxD_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
            "DxD_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
            "DxB_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
            "DxB_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
            "BxB_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
            "BxB_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
            "DxD_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
            "DxD_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
            "DxB_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
            "DxB_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
            "BxB_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
            "BxB_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
        }

        self.leaching = {
            "dairy_cows": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
            "suckler_cows": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
            "bulls": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
            "DxD_calves_m": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
            "DxD_calves_f": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
            "DxB_calves_m": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
            "DxB_calves_f": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
            "BxB_calves_m": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
            "BxB_calves_f": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
            "DxD_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
            "DxD_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
            "DxB_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
            "DxB_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
            "BxB_heifers_less_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
            "BxB_steers_less_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
            "DxD_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
            "DxD_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
            "DxB_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
            "DxB_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
            "BxB_heifers_more_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
            "BxB_steers_more_2_yr": self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff,
        }


    def test_cohort_coefficient_data_integrity(self):
        # Loop through each cohort in the old coefficient data structure
        for cohort, expected_value in self.coefficient.items():
            with self.subTest(cohort=cohort, attribute='coefficient'):
                # Check if the cohort exists in the new data structure
                self.assertIn(cohort, self.test_data, f"{cohort} is missing in new data structure")
                
                # Now check if 'coefficient' exists for this cohort in new data structure
                self.assertIn('coefficient', self.test_data[cohort], f"'coefficient' data is missing for {cohort}")
                
                # Retrieve the actual value from the new data structure
                actual_value = self.test_data[cohort]['coefficient']

                
                # Now assert the actual value matches the expected value from the old structure
                self.assertEqual(actual_value(), expected_value(), f"Mismatch in 'coefficient' for {cohort}")


    def test_cohort_weight_gain_data_integrity(self):
        # Loop through each cohort in the old coefficient data structure
        for cohort, expected_value in self.weight_gain.items():
            with self.subTest(cohort=cohort, attribute='weight_gain'):
                # Check if the cohort exists in the new data structure
                self.assertIn(cohort, self.test_data, f"{cohort} is missing in new data structure")
                
                # Now check if 'coefficient' exists for this cohort in new data structure
                self.assertIn('weight_gain', self.test_data[cohort], f"'weight_gain' data is missing for {cohort}")
                
                # Retrieve the actual value from the new data structure
                actual_value = self.test_data[cohort]['weight_gain']

                
                # Now assert the actual value matches the expected value from the old structure
                self.assertEqual(actual_value(), expected_value(), f"Mismatch in 'weight_gain' for {cohort}")


    def test_cohort_growth_gain_data_integrity(self):
        # Loop through each cohort in the old coefficient data structure
        for cohort, expected_value in self.growth.items():
            with self.subTest(cohort=cohort, attribute='growth'):
                # Check if the cohort exists in the new data structure
                self.assertIn(cohort, self.test_data, f"{cohort} is missing in new data structure")
                
                # Now check if 'coefficient' exists for this cohort in new data structure
                self.assertIn('growth', self.test_data[cohort], f"'growth' data is missing for {cohort}")
                
                # Retrieve the actual value from the new data structure
                actual_value = self.test_data[cohort]['growth']

                
                # Now assert the actual value matches the expected value from the old structure
                self.assertEqual(actual_value(), expected_value(), f"Mismatch in 'growth' for {cohort}")

    def test_cohort_N_retention_data_integrity(self):
        # Loop through each cohort in the old coefficient data structure
        for cohort, expected_value in self.N_retention.items():
            with self.subTest(cohort=cohort, attribute='N_retention'):
                # Check if the cohort exists in the new data structure
                self.assertIn(cohort, self.test_data, f"{cohort} is missing in new data structure")
                
                # Now check if 'coefficient' exists for this cohort in new data structure
                self.assertIn('N_retention', self.test_data[cohort], f"'N_retention' data is missing for {cohort}")
                
                # Retrieve the actual value from the new data structure
                actual_value = self.test_data[cohort]['N_retention']

                
                # Now assert the actual value matches the expected value from the old structure
                self.assertEqual(actual_value(), expected_value(), f"Mismatch in 'N_retention' for {cohort}")

    def test_cohort_N_retention_data_integrity(self):
        # Loop through each cohort in the old coefficient data structure
        for cohort, expected_value in self.N_retention.items():
            with self.subTest(cohort=cohort, attribute='N_retention'):
                # Check if the cohort exists in the new data structure
                self.assertIn(cohort, self.test_data, f"{cohort} is missing in new data structure")
                
                # Now check if 'coefficient' exists for this cohort in new data structure
                self.assertIn('N_retention', self.test_data[cohort], f"'N_retention' data is missing for {cohort}")
                
                # Retrieve the actual value from the new data structure
                actual_value = self.test_data[cohort]['N_retention']

                
                # Now assert the actual value matches the expected value from the old structure
                self.assertEqual(actual_value(), expected_value(), f"Mismatch in 'N_retention' for {cohort}")

    def test_cohort_total_ammonia_nitrogen_data_integrity(self):
        # Loop through each cohort in the old coefficient data structure
        for cohort, expected_value in self.total_ammonia_nitrogen.items():
            with self.subTest(cohort=cohort, attribute='total_ammonia_nitrogen'):
                # Check if the cohort exists in the new data structure
                self.assertIn(cohort, self.total_ammonia_nitrogen, f"{cohort} is missing in new data structure")
                
                # Now check if 'coefficient' exists for this cohort in new data structure
                self.assertIn('total_ammonia_nitrogen', self.test_data[cohort], f"'total_ammonia_nitrogen' data is missing for {cohort}")
                
                # Retrieve the actual value from the new data structure
                actual_value = self.test_data[cohort]['total_ammonia_nitrogen']

                
                # Now assert the actual value matches the expected value from the old structure
                self.assertEqual(actual_value(), expected_value(), f"Mismatch in 'total_ammonia_nitrogen' for {cohort}")

    def test_cohort_direct_n2o_emissions_factors_data_integrity(self):
        # Loop through each cohort in the old coefficient data structure
        for cohort, expected_value in self.direct_n2o_emissions_factors.items():
            with self.subTest(cohort=cohort, attribute='direct_n2o_emissions_factors'):
                # Check if the cohort exists in the new data structure
                self.assertIn(cohort, self.test_data, f"{cohort} is missing in new data structure")
                
                # Now check if 'coefficient' exists for this cohort in new data structure
                self.assertIn('direct_n2o_emissions_factors', self.test_data[cohort], f"'direct_n2o_emissions_factors' data is missing for {cohort}")
                
                # Retrieve the actual value from the new data structure
                actual_value = self.test_data[cohort]['direct_n2o_emissions_factors']

                
                # Now assert the actual value matches the expected value from the old structure
                self.assertEqual(actual_value(), expected_value(), f"Mismatch in 'direct_n2o_emissions_factors' for {cohort}")

    def test_cohort_atmospheric_deposition_data_integrity(self):
        # Loop through each cohort in the old coefficient data structure
        for cohort, expected_value in self.atmospheric_deposition.items():
            with self.subTest(cohort=cohort, attribute='atmospheric_deposition'):
                # Check if the cohort exists in the new data structure
                self.assertIn(cohort, self.test_data, f"{cohort} is missing in new data structure")
                
                # Now check if 'coefficient' exists for this cohort in new data structure
                self.assertIn('atmospheric_deposition', self.test_data[cohort], f"'atmospheric_deposition' data is missing for {cohort}")
                
                # Retrieve the actual value from the new data structure
                actual_value = self.test_data[cohort]['atmospheric_deposition']

                
                # Now assert the actual value matches the expected value from the old structure
                self.assertEqual(actual_value(), expected_value(), f"Mismatch in 'atmospheric_deposition' for {cohort}")

    def test_cohort_leaching_data_integrity(self):
        # Loop through each cohort in the old coefficient data structure
        for cohort, expected_value in self.leaching.items():
            with self.subTest(cohort=cohort, attribute='leaching'):
                # Check if the cohort exists in the new data structure
                self.assertIn(cohort, self.test_data, f"{cohort} is missing in new data structure")
                
                # Now check if 'coefficient' exists for this cohort in new data structure
                self.assertIn('leaching', self.test_data[cohort], f"'leaching' data is missing for {cohort}")
                
                # Retrieve the actual value from the new data structure
                actual_value = self.test_data[cohort]['leaching']

                
                # Now assert the actual value matches the expected value from the old structure
                self.assertEqual(actual_value(), expected_value(), f"Mismatch in 'leaching' for {cohort}")

if __name__ == '__main__':
    unittest.main()
