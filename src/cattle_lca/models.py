"""
    Container classes for data loaded from files
"""
import pandas
import copy


class DynamicData(object):
    def __init__(self, data, defaults={}):
        # Set the defaults first
        for variable, value in defaults.items():
            setattr(self, variable, value)

        # Overwrite the defaults with the real values
        for variable, value in data.items():
            setattr(self, variable, value)


class AnimalCategory(DynamicData):
    def __init__(self, data):
        defaults = {
            "pop": 0,
            "daily_milk": 0,
            "weight": 0,
            "forage": "average",
            "grazing": "pasture",
            "con_type": "concentrate",
            "con_amount": 0,
            "t_outdoors": 24,
            "t_indoors": 0,
            "t_stabled": 0,
            "mm_storage": "solid",
            "daily_spreading": "none",
            "n_sold": 0,
            "n_bought": 0,
        }

        super(AnimalCategory, self).__init__(data, defaults)


class AnimalCollection(DynamicData):
    def __init__(self, data):
        super(AnimalCollection, self).__init__(data)


class Farm(DynamicData):
    def __init__(self, data):  # , animal_collections):
        # self.animals = animal_collections.get(data.get("farm_id"))

        super(Farm, self).__init__(data)


######################################################################################
# Animal Features Data
######################################################################################
class Animal_Features(object):
    def __init__(self, data):
        self.data_frame = data

        self.animal_features = {}

        for _, row in self.data_frame.iterrows():
            birth_weight = row.get("birth_weight")
            mature_weight_bulls = row.get("mature_weight_bulls")
            mature_weight_dairy_cows = row.get("mature_weight_dairy_cows")
            mature_weight_suckler_cows = row.get("mature_weight_suckler_cows")
            dairy_cows_weight_gain = row.get("dairy_cows_weight_gain")
            suckler_cows_weight_gain = row.get("suckler_cows_weight_gain")
            DxD_calves_f_weight_gain = row.get("DxD_calves_f_weight_gain")
            DxD_calves_m_weight_gain = row.get("DxD_calves_m_weight_gain")
            DxB_calves_f_weight_gain = row.get("DxB_calves_f_weight_gain")
            DxB_calves_m_weight_gain = row.get("DxB_calves_f_weight_gain")
            BxB_calves_m_weight_gain = row.get("BxB_calves_m_weight_gain")
            BxB_calves_f_weight_gain = row.get("BxB_calves_f_weight_gain")
            DxD_heifers_less_2_yr_weight_gain = row.get(
                "DxD_heifers_less_2_yr_weight_gain"
            )
            DxD_steers_less_2_yr_weight_gain = row.get(
                "DxD_steers_less_2_yr_weight_gain"
            )
            DxB_heifers_less_2_yr_weight_gain = row.get(
                "DxB_heifers_less_2_yr_weight_gain"
            )
            DxB_steers_less_2_yr_weight_gain = row.get(
                "DxB_steers_less_2_yr_weight_gain"
            )
            BxB_heifers_less_2_yr_weight_gain = row.get(
                "BxB_heifers_less_2_yr_weight_gain"
            )
            BxB_steers_less_2_yr_weight_gain = row.get(
                "BxB_steers_less_2_yr_weight_gain"
            )
            DxD_heifers_more_2_yr_weight_gain = row.get(
                "DxD_heifers_more_2_yr_weight_gain"
            )
            DxD_steers_more_2_yr_weight_gain = row.get(
                "DxD_steers_more_2_yr_weight_gain"
            )
            DxB_heifers_more_2_yr_weight_gain = row.get(
                "DxB_heifers_more_2_yr_weight_gain"
            )
            DxB_steers_more_2_yr_weight_gain = row.get(
                "DxB_steers_more_2_yr_weight_gain"
            )
            BxB_heifers_more_2_yr_weight_gain = row.get(
                "BxB_heifers_more_2_yr_weight_gain"
            )
            BxB_steers_more_2_yr_weight_gain = row.get(
                "BxB_steers_more_2_yr_weight_gain"
            )
            bulls_weight_gain = row.get("bulls_weight_gain")
            dairy_cows_n_retention = row.get("dairy_cows_n_retention")
            suckler_cows_n_retention = row.get("suckler_cows_n_retention")
            DxD_calves_f_n_retention = row.get("DxD_calves_f_n_retention")
            DxD_calves_m_n_retention = row.get("DxD_calves_m_n_retention")
            DxB_calves_f_n_retention = row.get("DxB_calves_f_n_retention")
            DxB_calves_m_n_retention = row.get("DxB_calves_f_n_retention")
            BxB_calves_m_n_retention = row.get("BxB_calves_m_n_retention")
            BxB_calves_f_n_retention = row.get("BxB_calves_f_n_retention")
            DxD_heifers_less_2_yr_n_retention = row.get(
                "DxD_heifers_less_2_yr_n_retention"
            )
            DxD_steers_less_2_yr_n_retention = row.get(
                "DxD_steers_less_2_yr_n_retention"
            )
            DxB_heifers_less_2_yr_n_retention = row.get(
                "DxB_heifers_less_2_yr_n_retention"
            )
            DxB_steers_less_2_yr_n_retention = row.get(
                "DxB_steers_less_2_yr_n_retention"
            )
            BxB_heifers_less_2_yr_n_retention = row.get(
                "BxB_heifers_less_2_yr_n_retention"
            )
            BxB_steers_less_2_yr_n_retention = row.get(
                "BxB_steers_less_2_yr_n_retention"
            )
            DxD_heifers_more_2_yr_n_retention = row.get(
                "DxD_heifers_more_2_yr_n_retention"
            )
            DxD_steers_more_2_yr_n_retention = row.get(
                "DxD_steers_more_2_yr_n_retention"
            )
            DxB_heifers_more_2_yr_n_retention = row.get(
                "DxB_heifers_more_2_yr_n_retention"
            )
            DxB_steers_more_2_yr_n_retention = row.get(
                "DxB_steers_more_2_yr_n_retention"
            )
            BxB_heifers_more_2_yr_n_retention = row.get(
                "BxB_heifers_more_2_yr_n_retention"
            )
            BxB_steers_more_2_yr_n_retention = row.get(
                "BxB_steers_more_2_yr_n_retention"
            )
            bulls_n_retention = row.get("bulls_n_retention")

            self.animal_features = {
                "birth_weight": birth_weight,
                "mature_weight_bulls": mature_weight_bulls,
                "mature_weight_dairy_cows": mature_weight_dairy_cows,
                "mature_weight_suckler_cows": mature_weight_suckler_cows,
                "dairy_cows_weight_gain": dairy_cows_weight_gain,
                "suckler_cows_weight_gain": suckler_cows_weight_gain,
                "DxD_calves_f_weight_gain": DxD_calves_f_weight_gain,
                "DxD_calves_m_weight_gain": DxD_calves_m_weight_gain,
                "DxB_calves_f_weight_gain": DxB_calves_f_weight_gain,
                "DxB_calves_m_weight_gain": DxB_calves_m_weight_gain,
                "BxB_calves_m_weight_gain": BxB_calves_m_weight_gain,
                "BxB_calves_f_weight_gain": BxB_calves_f_weight_gain,
                "DxD_heifers_less_2_yr_weight_gain": DxD_heifers_less_2_yr_weight_gain,
                "DxD_steers_less_2_yr_weight_gain": DxD_steers_less_2_yr_weight_gain,
                "DxB_heifers_less_2_yr_weight_gain": DxB_heifers_less_2_yr_weight_gain,
                "DxB_steers_less_2_yr_weight_gain": DxB_steers_less_2_yr_weight_gain,
                "BxB_heifers_less_2_yr_weight_gain": BxB_heifers_less_2_yr_weight_gain,
                "BxB_steers_less_2_yr_weight_gain": BxB_steers_less_2_yr_weight_gain,
                "DxD_heifers_more_2_yr_weight_gain": DxD_heifers_more_2_yr_weight_gain,
                "DxD_steers_more_2_yr_weight_gain": DxD_steers_more_2_yr_weight_gain,
                "DxB_heifers_more_2_yr_weight_gain": DxB_heifers_more_2_yr_weight_gain,
                "DxB_steers_more_2_yr_weight_gain": DxB_steers_more_2_yr_weight_gain,
                "BxB_heifers_more_2_yr_weight_gain": BxB_heifers_more_2_yr_weight_gain,
                "BxB_steers_more_2_yr_weight_gain": BxB_steers_more_2_yr_weight_gain,
                "bulls_weight_gain": bulls_weight_gain,
                "dairy_cows_n_retention": dairy_cows_n_retention,
                "suckler_cows_n_retention": suckler_cows_n_retention,
                "DxD_calves_f_n_retention": DxD_calves_f_n_retention,
                "DxD_calves_m_n_retention": DxD_calves_m_n_retention,
                "DxB_calves_f_n_retention": DxB_calves_f_n_retention,
                "DxB_calves_m_n_retention": DxB_calves_m_n_retention,
                "BxB_calves_m_n_retention": BxB_calves_m_n_retention,
                "BxB_calves_f_n_retention": BxB_calves_f_n_retention,
                "DxD_heifers_less_2_yr_n_retention": DxD_heifers_less_2_yr_n_retention,
                "DxD_steers_less_2_yr_n_retention": DxD_steers_less_2_yr_n_retention,
                "DxB_heifers_less_2_yr_n_retention": DxB_heifers_less_2_yr_n_retention,
                "DxB_steers_less_2_yr_n_retention": DxB_steers_less_2_yr_n_retention,
                "BxB_heifers_less_2_yr_n_retention": BxB_heifers_less_2_yr_n_retention,
                "BxB_steers_less_2_yr_n_retention": BxB_steers_less_2_yr_n_retention,
                "DxD_heifers_more_2_yr_n_retention": DxD_heifers_more_2_yr_n_retention,
                "DxD_steers_more_2_yr_n_retention": DxD_steers_more_2_yr_n_retention,
                "DxB_heifers_more_2_yr_n_retention": DxB_heifers_more_2_yr_n_retention,
                "DxB_steers_more_2_yr_n_retention": DxB_steers_more_2_yr_n_retention,
                "BxB_heifers_more_2_yr_n_retention": BxB_heifers_more_2_yr_n_retention,
                "BxB_steers_more_2_yr_n_retention": BxB_steers_more_2_yr_n_retention,
                "bulls_n_retention": bulls_n_retention,
            }

    def get_birth_weight(self):
        return self.animal_features.get("birth_weight")

    def get_mature_weight_bulls(self):
        return self.animal_features.get("mature_weight_bulls")

    def get_mature_weight_dairy_cows(self):
        return self.animal_features.get("mature_weight_dairy_cows")

    def get_mature_weight_suckler_cows(self):
        return self.animal_features.get("mature_weight_suckler_cows")

    def get_dairy_cows_weight_gain(self):
        return self.animal_features.get("dairy_cows_weight_gain")

    def get_suckler_cows_weight_gain(self):
        return self.animal_features.get("suckler_cows_weight_gain")

    def get_DxD_calves_m_weight_gain(self):
        return self.animal_features.get("DxD_calves_m_weight_gain")

    def get_DxD_calves_f_weight_gain(self):
        return self.animal_features.get("DxD_calves_f_weight_gain")

    def get_DxB_calves_m_weight_gain(self):
        return self.animal_features.get("DxB_calves_m_weight_gain")

    def get_DxB_calves_f_weight_gain(self):
        return self.animal_features.get("DxB_calves_f_weight_gain")

    def get_BxB_calves_m_weight_gain(self):
        return self.animal_features.get("BxB_calves_m_weight_gain")

    def get_BxB_calves_f_weight_gain(self):
        return self.animal_features.get("BxB_calves_f_weight_gain")

    def get_DxD_heifers_less_2_yr_weight_gain(self):
        return self.animal_features.get("DxD_heifers_less_2_yr_weight_gain")

    def get_DxD_steers_less_2_yr_weight_gain(self):
        return self.animal_features.get("DxD_steers_less_2_yr_weight_gain")

    def get_DxB_heifers_less_2_yr_weight_gain(self):
        return self.animal_features.get("DxB_heifers_less_2_yr_weight_gain")

    def get_DxB_steers_less_2_yr_weight_gain(self):
        return self.animal_features.get("DxB_steers_less_2_yr_weight_gain")

    def get_BxB_heifers_less_2_yr_weight_gain(self):
        return self.animal_features.get("BxB_heifers_less_2_yr_weight_gain")

    def get_BxB_steers_less_2_yr_weight_gain(self):
        return self.animal_features.get("BxB_steers_less_2_yr_weight_gain")

    def get_DxD_heifers_more_2_yr_weight_gain(self):
        return self.animal_features.get("DxD_heifers_more_2_yr_weight_gain")

    def get_DxD_steers_more_2_yr_weight_gain(self):
        return self.animal_features.get("DxD_steers_more_2_yr_weight_gain")

    def get_DxB_heifers_more_2_yr_weight_gain(self):
        return self.animal_features.get("DxB_heifers_more_2_yr_weight_gain")

    def get_DxB_steers_more_2_yr_weight_gain(self):
        return self.animal_features.get("DxB_steers_more_2_yr_weight_gain")

    def get_BxB_heifers_more_2_yr_weight_gain(self):
        return self.animal_features.get("BxB_heifers_more_2_yr_weight_gain")

    def get_BxB_steers_more_2_yr_weight_gain(self):
        return self.animal_features.get("BxB_steers_more_2_yr_weight_gain")

    def get_bulls_weight_gain(self):
        return self.animal_features.get("bulls_weight_gain")

    def get_dairy_cows_n_retention(self):
        return self.animal_features.get("dairy_cows_n_retention")

    def get_suckler_cows_n_retention(self):
        return self.animal_features.get("suckler_cows_n_retention")

    def get_DxD_calves_m_n_retention(self):
        return self.animal_features.get("DxD_calves_m_n_retention")

    def get_DxD_calves_f_n_retention(self):
        return self.animal_features.get("DxD_calves_f_n_retention")

    def get_DxB_calves_m_n_retention(self):
        return self.animal_features.get("DxB_calves_m_n_retention")

    def get_DxB_calves_f_n_retention(self):
        return self.animal_features.get("DxB_calves_f_n_retention")

    def get_BxB_calves_m_n_retention(self):
        return self.animal_features.get("BxB_calves_m_n_retention")

    def get_BxB_calves_f_n_retention(self):
        return self.animal_features.get("BxB_calves_f_n_retention")

    def get_DxD_heifers_less_2_yr_n_retention(self):
        return self.animal_features.get("DxD_heifers_less_2_yr_n_retention")

    def get_DxD_steers_less_2_yr_n_retention(self):
        return self.animal_features.get("DxD_steers_less_2_yr_n_retention")

    def get_DxB_heifers_less_2_yr_n_retention(self):
        return self.animal_features.get("DxB_heifers_less_2_yr_n_retention")

    def get_DxB_steers_less_2_yr_n_retention(self):
        return self.animal_features.get("DxB_steers_less_2_yr_n_retention")

    def get_BxB_heifers_less_2_yr_n_retention(self):
        return self.animal_features.get("BxB_heifers_less_2_yr_n_retention")

    def get_BxB_steers_less_2_yr_n_retention(self):
        return self.animal_features.get("BxB_steers_less_2_yr_n_retention")

    def get_DxD_heifers_more_2_yr_n_retention(self):
        return self.animal_features.get("DxD_heifers_more_2_yr_n_retention")

    def get_DxD_steers_more_2_yr_n_retention(self):
        return self.animal_features.get("DxD_steers_more_2_yr_n_retention")

    def get_DxB_heifers_more_2_yr_n_retention(self):
        return self.animal_features.get("DxB_heifers_more_2_yr_n_retention")

    def get_DxB_steers_more_2_yr_n_retention(self):
        return self.animal_features.get("DxB_steers_more_2_yr_n_retention")

    def get_BxB_heifers_more_2_yr_n_retention(self):
        return self.animal_features.get("BxB_heifers_more_2_yr_n_retention")

    def get_BxB_steers_more_2_yr_n_retention(self):
        return self.animal_features.get("BxB_steers_more_2_yr_n_retention")

    def get_bulls_n_retention(self):
        return self.animal_features.get("bulls_n_retention")

    def get_data(self):
        return self.data_frame

    def is_loaded(self):
        if self.data_frame is not None:
            return True
        else:
            return False


#######################################################################################


######################################################################################
# Emissions Factors Data
######################################################################################
class Emissions_Factors(object):
    def __init__(self, data):
        self.data_frame = data

        self.emissions_factors = {}

        for _, row in self.data_frame.iterrows():
            ef_net_energy_for_maintenance_non_lactating_cow = row.get(
                "ef_net_energy_for_maintenance_non_lactating_cow"
            )
            ef_net_energy_for_maintenance_lactating_cow = row.get(
                "ef_net_energy_for_maintenance_lactating_cow"
            )
            ef_net_energy_for_maintenance_bulls = row.get(
                "ef_net_energy_for_maintenance_bulls"
            )
            ef_feeding_situation_pasture = row.get("ef_feeding_situation_pasture")
            ef_feeding_situation_large_area = row.get("ef_feeding_situation_large_area")
            ef_feeding_situation_stall = row.get("ef_feeding_situation_stall")
            ef_net_energy_for_growth_females = row.get(
                "ef_net_energy_for_growth_females"
            )
            ef_net_energy_for_growth_castrates = row.get(
                "ef_net_energy_for_growth_castrates"
            )
            ef_net_energy_for_growth_bulls = row.get("ef_net_energy_for_growth_bulls")
            ef_net_energy_for_pregnancy = row.get("ef_net_energy_for_pregnancy")
            ef_methane_conversion_factor_dairy_cow = row.get(
                "ef_methane_conversion_factor_dairy_cow"
            )
            ef_methane_conversion_factor_steer = row.get(
                "ef_methane_conversion_factor_steer"
            )
            ef_methane_conversion_factor_calves = row.get(
                "ef_methane_conversion_factor_calves"
            )
            ef_methane_conversion_factor_bulls = row.get(
                "ef_methane_conversion_factor_bulls"
            )
            ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition = row.get(
                "ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition"
            )
            ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o = row.get(
                "ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o"
            )
            ef_direct_n2o_emissions_soils = row.get("ef_direct_n2o_emissions_soils")
            ef_indirect_n2o_atmospheric_deposition_to_soils_and_water = row.get(
                "ef_indirect_n2o_atmospheric_deposition_to_soils_and_water"
            )
            ef_indirect_n2o_from_leaching_and_runoff = row.get(
                "ef_indirect_n2o_from_leaching_and_runoff"
            )
            ef_TAN_house_liquid = row.get("ef_TAN_house_liquid")
            ef_TAN_house_solid = row.get("ef_TAN_house_solid")
            ef_TAN_storage_tank = row.get("ef_TAN_storage_tank")
            ef_TAN_storage_solid = row.get("ef_TAN_storage_solid")
            ef_mcf_liquid_tank = row.get("ef_mcf_liquid_tank")
            ef_mcf_solid_storage = row.get("ef_mcf_solid_storage")
            ef_mcf_anaerobic_digestion = row.get("ef_mcf_anaerobic_digestion")
            ef_n2o_direct_storage_tank_liquid = row.get(
                "ef_n2o_direct_storage_tank_liquid"
            )
            ef_n2o_direct_storage_tank_solid = row.get(
                "ef_n2o_direct_storage_tank_solid"
            )
            ef_n2o_direct_storage_solid = row.get("ef_n2o_direct_storage_solid")
            ef_n2o_direct_storage_tank_anaerobic_digestion = row.get(
                "ef_n2o_direct_storage_tank_anaerobic_digestion"
            )
            ef_nh3_daily_spreading_none = row.get("ef_nh3_daily_spreading_none")
            ef_nh3_daily_spreading_manure = row.get("ef_nh3_daily_spreading_manure")
            ef_nh3_daily_spreading_broadcast = row.get(
                "ef_nh3_daily_spreading_broadcast"
            )
            ef_nh3_daily_spreading_injection = row.get(
                "ef_nh3_daily_spreading_injection"
            )
            ef_nh3_daily_spreading_traling_hose = row.get(
                "ef_nh3_daily_spreading_trailing_hose"
            )
            ef_urea = row.get("ef_urea")
            ef_urea_and_nbpt = row.get("ef_urea_and_nbpt")
            ef_fracGASF_urea_fertilisers_to_nh3_and_nox = row.get(
                "ef_fracGASF_urea_fertilisers_to_nh3_and_nox"
            )
            ef_fracGASF_urea_and_nbpt_to_nh3_and_nox = row.get(
                "ef_fracGASF_urea_and_nbpt_to_nh3_and_nox"
            )
            ef_frac_leach_runoff = row.get("ef_frac_leach_runoff")
            ef_ammonium_nitrate = row.get("ef_ammonium_nitrate")
            ef_fracGASF_ammonium_fertilisers_to_nh3_and_nox = row.get(
                "ef_fracGASF_ammonium_fertilisers_to_nh3_and_nox"
            )
            Frac_P_Leach = row.get("Frac_P_Leach")

            self.emissions_factors = {
                "ef_net_energy_for_maintenance_non_lactating_cow": ef_net_energy_for_maintenance_non_lactating_cow,
                "ef_net_energy_for_maintenance_lactating_cow": ef_net_energy_for_maintenance_lactating_cow,
                "ef_net_energy_for_maintenance_bulls": ef_net_energy_for_maintenance_bulls,
                "ef_feeding_situation_pasture": ef_feeding_situation_pasture,
                "ef_feeding_situation_large_area": ef_feeding_situation_large_area,
                "ef_feeding_situation_stall": ef_feeding_situation_stall,
                "ef_net_energy_for_growth_females": ef_net_energy_for_growth_females,
                "ef_net_energy_for_growth_castrates": ef_net_energy_for_growth_castrates,
                "ef_net_energy_for_growth_bulls": ef_net_energy_for_growth_bulls,
                "ef_net_energy_for_pregnancy": ef_net_energy_for_pregnancy,
                "ef_methane_conversion_factor_dairy_cow": ef_methane_conversion_factor_dairy_cow,
                "ef_methane_conversion_factor_steer": ef_methane_conversion_factor_steer,
                "ef_methane_conversion_factor_calves": ef_methane_conversion_factor_calves,
                "ef_methane_conversion_factor_bulls": ef_methane_conversion_factor_bulls,
                "ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition": ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition,
                "ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o": ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o,
                "ef_direct_n2o_emissions_soils": ef_direct_n2o_emissions_soils,
                "ef_indirect_n2o_atmospheric_deposition_to_soils_and_water": ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
                "ef_indirect_n2o_from_leaching_and_runoff": ef_indirect_n2o_from_leaching_and_runoff,
                "ef_TAN_house_liquid": ef_TAN_house_liquid,
                "ef_TAN_house_solid": ef_TAN_house_solid,
                "ef_TAN_storage_tank": ef_TAN_storage_tank,
                "ef_TAN_storage_solid": ef_TAN_storage_solid,
                "ef_mcf_liquid_tank": ef_mcf_liquid_tank,
                "ef_mcf_solid_storage": ef_mcf_solid_storage,
                "ef_mcf_anaerobic_digestion": ef_mcf_anaerobic_digestion,
                "ef_n2o_direct_storage_tank_liquid": ef_n2o_direct_storage_tank_liquid,
                "ef_n2o_direct_storage_tank_solid": ef_n2o_direct_storage_tank_solid,
                "ef_n2o_direct_storage_solid": ef_n2o_direct_storage_solid,
                "ef_n2o_direct_storage_tank_anaerobic_digestion": ef_n2o_direct_storage_tank_anaerobic_digestion,
                "ef_nh3_daily_spreading_none": ef_nh3_daily_spreading_none,
                "ef_nh3_daily_spreading_manure": ef_nh3_daily_spreading_manure,
                "ef_nh3_daily_spreading_broadcast": ef_nh3_daily_spreading_broadcast,
                "ef_nh3_daily_spreading_injection": ef_nh3_daily_spreading_injection,
                "ef_nh3_daily_spreading_traling_hose": ef_nh3_daily_spreading_traling_hose,
                "ef_urea": ef_urea,
                "ef_urea_and_nbpt": ef_urea_and_nbpt,
                "ef_fracGASF_urea_fertilisers_to_nh3_and_nox": ef_fracGASF_urea_fertilisers_to_nh3_and_nox,
                "ef_fracGASF_urea_and_nbpt_to_nh3_and_nox": ef_fracGASF_urea_and_nbpt_to_nh3_and_nox,
                "ef_frac_leach_runoff": ef_frac_leach_runoff,
                "ef_ammonium_nitrate": ef_ammonium_nitrate,
                "ef_fracGASF_ammonium_fertilisers_to_nh3_and_nox": ef_fracGASF_ammonium_fertilisers_to_nh3_and_nox,
                "ef_Frac_P_Leach": Frac_P_Leach,
            }

    def get_ef_net_energy_for_maintenance_non_lactating_cow(self):
        return self.emissions_factors.get(
            "ef_net_energy_for_maintenance_non_lactating_cow"
        )

    def get_ef_net_energy_for_maintenance_lactating_cow(self):
        return self.emissions_factors.get("ef_net_energy_for_maintenance_lactating_cow")

    def get_ef_net_energy_for_maintenance_bulls(self):
        return self.emissions_factors.get("ef_net_energy_for_maintenance_bulls")

    def get_ef_feeding_situation_pasture(self):
        return self.emissions_factors.get("ef_feeding_situation_pasture")

    def get_ef_feeding_situation_large_area(self):
        return self.emissions_factors.get("ef_feeding_situation_large_area")

    def get_ef_feeding_situation_stall(self):
        return self.emissions_factors.get("ef_feeding_situation_stall")

    def get_ef_net_energy_for_growth_females(self):
        return self.emissions_factors.get("ef_net_energy_for_growth_females")

    def get_ef_net_energy_for_growth_castrates(self):
        return self.emissions_factors.get("ef_net_energy_for_growth_castrates")

    def get_ef_net_energy_for_growth_bulls(self):
        return self.emissions_factors.get("ef_net_energy_for_growth_bulls")

    def get_ef_net_energy_for_pregnancy(self):
        return self.emissions_factors.get("ef_net_energy_for_pregnancy")

    def get_ef_methane_conversion_factor_dairy_cow(self):
        return self.emissions_factors.get("ef_methane_conversion_factor_dairy_cow")

    def get_ef_methane_conversion_factor_steer(self):
        return self.emissions_factors.get("ef_methane_conversion_factor_steer")

    def get_ef_methane_conversion_factor_calves(self):
        return self.emissions_factors.get("ef_methane_conversion_factor_calves")

    def get_ef_methane_conversion_factor_bulls(self):
        return self.emissions_factors.get("ef_methane_conversion_factor_bulls")

    def get_ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition(self):
        return self.emissions_factors.get(
            "ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition"
        )

    def get_ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o(self):
        return self.emissions_factors.get(
            "ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o"
        )

    def get_ef_direct_n2o_emissions_soils(self):
        return self.emissions_factors.get("ef_direct_n2o_emissions_soils")

    def get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(self):
        return self.emissions_factors.get(
            "ef_indirect_n2o_atmospheric_deposition_to_soils_and_water"
        )

    def get_ef_indirect_n2o_from_leaching_and_runoff(self):
        return self.emissions_factors.get("ef_indirect_n2o_from_leaching_and_runoff")

    def get_ef_TAN_house_liquid(self):
        return self.emissions_factors.get("ef_TAN_house_liquid")

    def get_ef_TAN_house_solid(self):
        return self.emissions_factors.get("ef_TAN_house_solid")

    def get_ef_TAN_storage_tank(self):
        return self.emissions_factors.get("ef_TAN_storage_tank")

    def get_ef_TAN_storage_solid(self):
        return self.emissions_factors.get("ef_TAN_storage_solid")

    def get_ef_mcf_liquid_tank(self):
        return self.emissions_factors.get("ef_mcf_liquid_tank")

    def get_ef_mcf_solid_storage(self):
        return self.emissions_factors.get("ef_mcf_solid_storage")

    def get_ef_mcf_anaerobic_digestion(self):
        return self.emissions_factors.get("ef_mcf_anaerobic_digestion")

    def get_ef_n2o_direct_storage_tank_liquid(self):
        return self.emissions_factors.get("ef_n2o_direct_storage_tank_liquid")

    def get_ef_n2o_direct_storage_tank_solid(self):
        return self.emissions_factors.get("ef_n2o_direct_storage_tank_solid")

    def get_ef_n2o_direct_storage_solid(self):
        return self.emissions_factors.get("ef_n2o_direct_storage_solid")

    def get_ef_n2o_direct_storage_tank_anaerobic_digestion(self):
        return self.emissions_factors.get(
            "ef_n2o_direct_storage_tank_anaerobic_digestion"
        )

    def get_ef_nh3_daily_spreading_none(self):
        return self.emissions_factors.get("ef_nh3_daily_spreading_none")

    def get_ef_nh3_daily_spreading_manure(self):
        return self.emissions_factors.get("ef_nh3_daily_spreading_manure")

    def get_ef_nh3_daily_spreading_broadcast(self):
        return self.emissions_factors.get("ef_nh3_daily_spreading_broadcast")

    def get_ef_nh3_daily_spreading_injection(self):
        return self.emissions_factors.get("ef_nh3_daily_spreading_injection")

    def get_ef_nh3_daily_spreading_traling_hose(self):
        return self.emissions_factors.get("ef_nh3_daily_spreading_traling_hose")

    def get_ef_urea(self):
        return self.emissions_factors.get("ef_urea")

    def get_ef_urea_and_nbpt(self):
        return self.emissions_factors.get("ef_urea_and_nbpt")

    def get_ef_fracGASF_urea_fertilisers_to_nh3_and_nox(self):
        return self.emissions_factors.get("ef_fracGASF_urea_fertilisers_to_nh3_and_nox")

    def get_ef_fracGASF_urea_and_nbpt_to_nh3_and_nox(self):
        return self.emissions_factors.get("ef_fracGASF_urea_and_nbpt_to_nh3_and_nox")

    def get_ef_frac_leach_runoff(self):
        return self.emissions_factors.get("ef_frac_leach_runoff")

    def get_ef_ammonium_nitrate(self):
        return self.emissions_factors.get("ef_ammonium_nitrate")

    def get_ef_fracGASF_ammonium_fertilisers_to_nh3_and_nox(self):
        return self.emissions_factors.get(
            "ef_fracGASF_ammonium_fertilisers_to_nh3_and_nox"
        )

    def get_ef_Frac_P_Leach(self):
        return self.emissions_factors.get("ef_Frac_P_Leach")

    def get_data(self):
        return self.data_frame

    def is_loaded(self):
        if self.data_frame is not None:
            return True
        else:
            return False


#######################################################################################


class Grass(object):
    def average(self, property):
        values = [
            row.get(property)
            for _, row in self.data_frame.iterrows()
            if pandas.notna(row.get(property))
        ]

        return sum(values) / len(values)

    def __init__(self, data):
        self.data_frame = data

        self.grasses = {}

        for _, row in self.data_frame.iterrows():
            genus = row.get("grass_genus".lower())
            dmd = row.get("forage_dry_matter_digestibility")
            cp = row.get("crude_protein")
            ge = row.get("gross_energy")

            self.grasses[genus] = {
                "forage_dry_matter_digestibility": dmd,
                "crude_protein": cp,
                "gross_energy": ge,
            }

        # Pre-compute averages
        self.grasses["average"] = {
            "forage_dry_matter_digestibility": self.average(
                "forage_dry_matter_digestibility"
            ),
            "crude_protein": self.average("crude_protein"),
            "gross_energy": self.average("gross_energy"),
        }

    def get_forage_dry_matter_digestibility(self, forage):
        return self.grasses.get(forage).get("forage_dry_matter_digestibility")

    def get_crude_protein(self, forage):
        return self.grasses.get(forage).get("crude_protein")

    def get_gross_energy_mje_dry_matter(self, forage):
        return self.grasses.get(forage).get("gross_energy")

    def get_data(self):
        return self.data_frame

    def is_loaded(self):
        if self.data_frame is not None:
            return True
        else:
            return False


#######################################################################################
# concentrate file class
########################################################################################
class Concentrate(object):
    def average(self, property):
        values = [
            row.get(property)
            for _, row in self.data_frame.iterrows()
            if pandas.notna(row.get(property))
        ]

        try:
            return sum(values) / len(values)
        except ZeroDivisionError as err:
            pass

    def __init__(self, data):
        self.data_frame = data

        self.concentrates = {}

        for _, row in self.data_frame.iterrows():
            con_type = row.get("con_type".lower())
            con_dmd = row.get("con_dry_matter_digestibility")
            con_de = row.get("con_digestible_energy")
            con_cp = row.get("con_crude_protein")
            con_gross_energy = row.get("gross_energy_mje_dry_matter")
            con_co2_e = row.get("con_co2_e")
            con_po4_e = row.get("con_po4_e")

            self.concentrates[con_type] = {
                "con_dry_matter_digestibility": con_dmd,
                "con_digestible_energy": con_de,
                "con_crude_protein": con_cp,
                "gross_energy_mje_dry_matter": con_gross_energy,
                "con_co2_e": con_co2_e,
                "con_po4_e": con_po4_e,
            }

        # Pre-compute averages
        self.concentrates["average"] = {
            "con_dry_matter_digestibility": self.average(
                "con_dry_matter_digestibility"
            ),
            "con_digestible_energy": self.average("con_digestible_energy"),
            "con_crude_protein": self.average("con_crude_protein"),
        }

    def get_con_dry_matter_digestibility(self, concentrate):
        return self.concentrates.get(concentrate).get("con_dry_matter_digestibility")

    def get_con_digestible_energy(self, concentrate):
        return self.concentrates.get(concentrate).get("con_digestible_energy")

    def get_con_crude_protein(self, concentrate):
        return self.concentrates.get(concentrate).get("con_crude_protein")

    def get_gross_energy_mje_dry_matter(self, concentrate):
        return self.concentrates.get(concentrate).get("gross_energy_mje_dry_matter")

    def get_con_co2_e(self, concentrate):
        return self.concentrates.get(concentrate).get("con_co2_e")

    def get_con_po4_e(self, concentrate):
        return self.concentrates.get(concentrate).get("con_po4_e")

    def get_data(self):
        return self.data_frame

    def is_loaded(self):
        if self.data_frame is not None:
            return True
        else:
            return False


########################################################################################
# Upstream class
########################################################################################
class Upstream(object):
    def __init__(self, data):
        self.data_frame = data

        self.upstream = {}

        for _, row in self.data_frame.iterrows():
            upstream_type = row.get("upstream_type".lower())
            upstream_fu = row.get("upstream_fu")
            upstream_kg_co2e = row.get("upstream_kg_co2e")
            upstream_kg_po4e = row.get("upstream_kg_po4e")
            upstream_kg_so2e = row.get("upstream_kg_so2e")
            upstream_mje = row.get("upstream_mje")
            upstream_kg_sbe = row.get("upstream_kg_sbe")

            self.upstream[upstream_type] = {
                "upstream_fu": upstream_fu,
                "upstream_kg_co2e": upstream_kg_co2e,
                "upstream_kg_po4e": upstream_kg_po4e,
                "upstream_kg_so2e": upstream_kg_so2e,
                "upstream_mje": upstream_mje,
                "upstream_kg_sbe": upstream_kg_sbe,
            }

    def get_upstream_fu(self, upstream):
        return self.upstream.get(upstream).get("upstream_fu")

    def get_upstream_kg_co2e(self, upstream):
        return self.upstream.get(upstream).get("upstream_kg_co2e")

    def get_upstream_kg_po4e(self, upstream):
        return self.upstream.get(upstream).get("upstream_kg_po4e")

    def get_upstream_kg_so2e(self, upstream):
        return self.upstream.get(upstream).get("upstream_kg_so2e")

    def get_upstream_mje(self, upstream):
        return self.upstream.get(upstream).get("upstream_mje")

    def get_upstream_kg_sbe(self, upstream):
        return self.upstream.get(upstream).get("upstream_kg_sbe")

    def get_data(self):
        return self.data_frame

    def is_loaded(self):
        if self.data_frame is not None:
            return True
        else:
            return False


#############################################################################################


def load_grass_data():
    return Grass()


def load_concentrate_data():
    return Concentrate()


def load_upstream_data():
    return Upstream()


def load_emissions_factors_data():
    return Emissions_Factors()


def load_animal_features_data():
    return Animal_Features()


def load_farm_data(farm_data_frame):
    subset = [
        "total_urea",
        "total_urea_abated",
        "total_n_fert",
        "total_p_fert",
        "total_k_fert",
        "diesel_kg",
        "elec_kwh",
    ]
    farm_data_frame.drop_duplicates(subset=subset, keep="first", inplace=True)

    scenario_list = []

    for _, row in farm_data_frame.iterrows():
        data = dict([(x, row.get(x)) for x in row.keys()])
        scenario_list.append(Farm(data))

    return dict(enumerate(scenario_list))


def load_livestock_data(animal_data_frame):
    # 1. Load each animal category into an object

    categories = []

    for _, row in animal_data_frame.iterrows():
        data = dict([(x, row.get(x)) for x in row.keys()])
        categories.append(AnimalCategory(data))

    # 2. Aggregate the animal categories into collection based on the farm ID

    collections = {}

    for category in categories:
        farm_id = category.farm_id
        cohort = category.cohort

        if farm_id not in collections:
            collections[farm_id] = {cohort: category}
        else:
            collections[farm_id][cohort] = category

    # 3. Convert the raw collection data into animal collection objects

    collection_objects = {}

    for farm_id, raw_data in collections.items():
        collection_objects[farm_id] = {"animals": AnimalCollection(raw_data)}

    return collection_objects


def print_livestock_data(data):
    for _, key in enumerate(data):
        for animal in data[key].keys():
            for cohort in data[key][animal].__dict__.keys():
                for attribute in (
                    data[key][animal].__getattribute__(cohort).__dict__.keys()
                ):
                    print(
                        f"{cohort}: {attribute} = {data[key][animal].__getattribute__(cohort).__getattribute__(attribute)}"
                    )


def create_emissions_dictionary(keys):
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
