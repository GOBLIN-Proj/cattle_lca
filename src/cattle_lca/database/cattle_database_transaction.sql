BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "grass_database" (
	"grass_genus"	REAL,
	"forage_dry_matter_digestibility"	REAL,
	"crude_protein"	REAL,
	"gross_energy"	REAL
);
CREATE TABLE IF NOT EXISTS "upstream_database" (
	"upstream_type"	TEXT,
	"upstream_fu"	TEXT,
	"upstream_kg_co2e"	REAL,
	"upstream_kg_po4e"	REAL,
	"upstream_kg_so2e"	REAL,
	"upstream_mje"	REAL,
	"upstream_kg_sbe"	REAL
);
CREATE TABLE IF NOT EXISTS "animal_features_database" (
	"ef_country"	TEXT,
	"birth_weight"	REAL,
	"mature_weight_bulls"	REAL,
	"mature_weight_dairy_cows"	REAL,
	"mature_weight_suckler_cows"	REAL,
	"dairy_cows_weight_gain"	REAL,
	"suckler_cows_weight_gain"	REAL,
	"DxD_calves_f_weight_gain"	REAL,
	"DxD_calves_m_weight_gain"	REAL,
	"DxB_calves_f_weight_gain"	REAL,
	"DxB_calves_m_weight_gain"	REAL,
	"BxB_calves_f_weight_gain"	REAL,
	"BxB_calves_m_weight_gain"	REAL,
	"DxD_heifers_less_2_yr_weight_gain"	REAL,
	"DxD_steers_less_2_yr_weight_gain"	REAL,
	"DxB_heifers_less_2_yr_weight_gain"	REAL,
	"DxB_steers_less_2_yr_weight_gain"	REAL,
	"BxB_heifers_less_2_yr_weight_gain"	REAL,
	"BxB_steers_less_2_yr_weight_gain"	REAL,
	"DxD_heifers_more_2_yr_weight_gain"	REAL,
	"DxD_steers_more_2_yr_weight_gain"	REAL,
	"DxB_heifers_more_2_yr_weight_gain"	REAL,
	"DxB_steers_more_2_yr_weight_gain"	REAL,
	"BxB_heifers_more_2_yr_weight_gain"	REAL,
	"BxB_steers_more_2_yr_weight_gain"	REAL,
	"bulls_weight_gain"	REAL,
	"dairy_cows_n_retention"	REAL,
	"suckler_cows_n_retention"	REAL,
	"DxD_calves_f_n_retention"	REAL,
	"DxD_calves_m_n_retention"	REAL,
	"DxB_calves_f_n_retention"	REAL,
	"DxB_calves_m_n_retention"	REAL,
	"BxB_calves_f_n_retention"	REAL,
	"BxB_calves_m_n_retention"	REAL,
	"DxD_heifers_less_2_yr_n_retention"	REAL,
	"DxD_steers_less_2_yr_n_retention"	REAL,
	"DxB_heifers_less_2_yr_n_retention"	REAL,
	"DxB_steers_less_2_yr_n_retention"	REAL,
	"BxB_heifers_less_2_yr_n_retention"	REAL,
	"BxB_steers_less_2_yr_n_retention"	REAL,
	"DxD_heifers_more_2_yr_n_retention"	REAL,
	"DxD_steers_more_2_yr_n_retention"	REAL,
	"DxB_heifers_more_2_yr_n_retention"	REAL,
	"DxB_steers_more_2_yr_n_retention"	REAL,
	"BxB_heifers_more_2_yr_n_retention"	REAL,
	"BxB_steers_more_2_yr_n_retention"	REAL,
	"bulls_n_retention"	REAL
);
CREATE TABLE IF NOT EXISTS "emissions_factors_database" (
	"ef_country"	TEXT,
	"ef_net_energy_for_maintenance_non_lactating_cow"	REAL,
	"ef_net_energy_for_maintenance_lactating_cow"	REAL,
	"ef_net_energy_for_maintenance_bulls"	REAL,
	"ef_feeding_situation_pasture"	REAL,
	"ef_feeding_situation_large_area"	REAL,
	"ef_feeding_situation_stall"	REAL,
	"ef_net_energy_for_growth_females"	REAL,
	"ef_net_energy_for_growth_castrates"	REAL,
	"ef_net_energy_for_growth_bulls"	REAL,
	"ef_net_energy_for_pregnancy"	REAL,
	"ef_methane_conversion_factor_dairy_cow"	REAL,
	"ef_methane_conversion_factor_steer"	REAL,
	"ef_methane_conversion_factor_calves"	REAL,
	"ef_methane_conversion_factor_bulls"	REAL,
	"ef_fracGASM_total_ammonia_nitrogen_pasture_range_paddock_deposition"	REAL,
	"ef_cpp_pasture_range_paddock_for_dairy_and_non_dairy_direct_n2o"	REAL,
	"ef_direct_n2o_emissions_soils"	REAL,
	"ef_indirect_n2o_atmospheric_deposition_to_soils_and_water"	REAL,
	"ef_indirect_n2o_from_leaching_and_runoff"	REAL,
	"ef_TAN_house_liquid"	REAL,
	"ef_TAN_house_solid"	REAL,
	"ef_TAN_storage_tank"	REAL,
	"ef_TAN_storage_solid"	REAL,
	"ef_mcf_liquid_tank"	REAL,
	"ef_mcf_solid_storage"	REAL,
	"ef_mcf_anaerobic_digestion"	REAL,
	"ef_n2o_direct_storage_tank_liquid"	REAL,
	"ef_n2o_direct_storage_tank_solid"	REAL,
	"ef_n2o_direct_storage_solid"	REAL,
	"ef_n2o_direct_storage_tank_anaerobic_digestion"	REAL,
	"ef_daily_spreading_none"	REAL,
	"ef_nh3_daily_spreading_manure"	REAL,
	"ef_nh3_daily_spreading_broadcast"	REAL,
	"ef_nh3_daily_spreading_injection"	REAL,
	"ef_nh3_daily_spreading_trailing_hose"	REAL,
	"ef_urea"	REAL,
	"ef_urea_and_nbpt"	REAL,
	"ef_fracGASF_urea_fertilisers_to_nh3_and_nox"	REAL,
	"ef_fracGASF_urea_and_nbpt_to_nh3_and_nox"	REAL,
	"ef_frac_leach_runoff"	REAL,
	"ef_ammonium_nitrate"	REAL,
	"ef_fracGASF_ammonium_fertilisers_to_nh3_and_nox"	REAL,
	"Frac_P_Leach"	REAL
);
CREATE TABLE IF NOT EXISTS "concentrate_database" (
	"con_type"	TEXT,
	"con_dry_matter_digestibility"	REAL,
	"con_digestible_energy"	REAL,
	"con_crude_protein"	REAL,
	"gross_energy_mje_dry_matter"	REAL,
	"con_co2_e"	REAL,
	"con_po4_e"	REAL
);
INSERT INTO "grass_database" VALUES ('Andropogon',60.71,9.13,NULL);
INSERT INTO "grass_database" VALUES ('Avena',NULL,16.65,NULL);
INSERT INTO "grass_database" VALUES ('Axonopus',66.64,8.9,18.1);
INSERT INTO "grass_database" VALUES ('Brachiaria',65.5,10.17,17.6);
INSERT INTO "grass_database" VALUES ('Chloris',NULL,9.9,18.3);
INSERT INTO "grass_database" VALUES ('Cratyla',51.34,NULL,NULL);
INSERT INTO "grass_database" VALUES ('Cynodon',67.36,12.97,18.0);
INSERT INTO "grass_database" VALUES ('Dichanthium',60.44,9.8,17.9);
INSERT INTO "grass_database" VALUES ('Festuca',61.69,21.9,NULL);
INSERT INTO "grass_database" VALUES ('Glyricidia',64.04,NULL,NULL);
INSERT INTO "grass_database" VALUES ('Hermarthria',65.6,8.24,NULL);
INSERT INTO "grass_database" VALUES ('Hyparrhenia',NULL,7.05,18.9);
INSERT INTO "grass_database" VALUES ('Ischaemum',65.86,9.45,NULL);
INSERT INTO "grass_database" VALUES ('Leucaena',59.56,NULL,19.0);
INSERT INTO "grass_database" VALUES ('Lolium',NULL,16.56,NULL);
INSERT INTO "grass_database" VALUES ('Lotus',NULL,20.9,18.9);
INSERT INTO "grass_database" VALUES ('Melinis',NULL,7.25,18.4);
INSERT INTO "grass_database" VALUES ('Morus',63.51,NULL,18.2);
INSERT INTO "grass_database" VALUES ('Panicum',62.84,8.83,18.1);
INSERT INTO "grass_database" VALUES ('Paspalum',NULL,10.4,17.6);
INSERT INTO "grass_database" VALUES ('Pennisetum',65.94,11.3,17.4);
INSERT INTO "grass_database" VALUES ('Phalaris',57.99,17.06,17.9);
INSERT INTO "grass_database" VALUES ('Secale',NULL,16.5,17.8);
INSERT INTO "grass_database" VALUES ('Setaria',67.99,13.62,17.8);
INSERT INTO "grass_database" VALUES ('Sorghum',61.23,12.36,18.1);
INSERT INTO "grass_database" VALUES ('Stylosanthes',55.71,NULL,18.9);
INSERT INTO "grass_database" VALUES ('Tiothonia',79.45,22.78,NULL);
INSERT INTO "grass_database" VALUES ('Trifolium',NULL,20.58,17.6);
INSERT INTO "grass_database" VALUES ('Trifolium_repens',77.3,NULL,18.3);
INSERT INTO "grass_database" VALUES ('Urochoa',NULL,8.48,NULL);
INSERT INTO "grass_database" VALUES ('Vicia',NULL,23.27,18.5);
INSERT INTO "grass_database" VALUES ('irish_grass',70.0,18.5,18.5);
INSERT INTO "upstream_database" VALUES ('ammonium_nitrate_fertiliser','kg n',6.1,0.00678,0.0241,55.71725572,0.0268);
INSERT INTO "upstream_database" VALUES ('urea_fert','kg n',3.43,0.00387,0.025,57.5,1.81e-05);
INSERT INTO "upstream_database" VALUES ('triple_superphosphate','kg p2o5',2.02,0.0453,0.037,28.27442827,0.0136);
INSERT INTO "upstream_database" VALUES ('potassium_chloride','kg k2o',0.495,0.000766,0.00172,8.316008316,0.004);
INSERT INTO "upstream_database" VALUES ('lime','kg caco3',0.204,0.0004,0.000683,3.305613306,0.00159);
INSERT INTO "upstream_database" VALUES ('agrochemicals','kg a_i',10.1,0.0325,0.0971,174.4282744,0.0839);
INSERT INTO "upstream_database" VALUES ('ww_seed','kg',0.574,0.00634,0.00388,3.40956341,0.00164);
INSERT INTO "upstream_database" VALUES ('sb_seed','kg',0.407,0.00696,0.00349,2.827442827,0.00136);
INSERT INTO "upstream_database" VALUES ('osr_seed','kg',1.73,0.0127,0.018,11.26819127,0.00542);
INSERT INTO "upstream_database" VALUES ('maize_seed','kg',1.92,0.0179,0.00796,13.16008316,0.00633);
INSERT INTO "upstream_database" VALUES ('grass_seed','kg',1.9,0.00507,0.0102,16.00831601,0.0077);
INSERT INTO "upstream_database" VALUES ('diesel_indirect','kg',0.6937,0.00089,0.00619,51.559,0.0248);
INSERT INTO "upstream_database" VALUES ('electricity_consumed','kwh_consumed',0.01028,3.96e-05,4.35e-05,0.0,1.29e-06);
INSERT INTO "upstream_database" VALUES ('transport_tractor_trailer','kg_or_tkm',0.161,0.000248,0.0011,2.141372141,0.00103);
INSERT INTO "upstream_database" VALUES ('marginal_electricity','kwh_generated',0.41976,6.402e-05,0.0002255,7.318087318,0.00352);
INSERT INTO "upstream_database" VALUES ('concentrate_feed','kg',0.577,0.00708,0.0041,3.035343035,0.00146);
INSERT INTO "upstream_database" VALUES ('concentrate_feed_iluc','kg',0.71,0.000566,0.0,0.0,0.0);
INSERT INTO "upstream_database" VALUES ('sbmedirect','kg',0.249336641,0.003934465,0.001770274,6.824616269,0.003282656);
INSERT INTO "upstream_database" VALUES ('sbme_iluc','kg',11.02618662,0.003536943,0.0,0.0,0.0);
INSERT INTO "upstream_database" VALUES ('transport_more_than_16t_ch_av','tkm',0.106,0.00139,0.00596,1.384615385,0.000666);
INSERT INTO "upstream_database" VALUES ('transport_16_to_32 t_euro_iv','tkm',0.134,0.000107,0.00049,1.752598753,0.000843);
INSERT INTO "upstream_database" VALUES ('transport_more_than32t_truck_euro_5','tkm',0.0813,6.69e-05,0.000304,1.064449064,0.000512);
INSERT INTO "upstream_database" VALUES ('liquid_tanker_transport_28t','tkm',0.0962,0.0009,0.00165,0.708939709,0.000341);
INSERT INTO "upstream_database" VALUES ('ocean_transport','tkm',0.00244,7.61e-06,8.05e-05,0.030977131,1.49e-05);
INSERT INTO "upstream_database" VALUES ('mw_collection_ch','tkm',1.26,0.0012,0.00552,16.46569647,0.00792);
INSERT INTO "upstream_database" VALUES ('landfill_waste','kg',0.517172562,0.000144623,0.000419128,-1.563107642,-0.000751855);
INSERT INTO "upstream_database" VALUES ('oil_heat_100kw_condensing','kwhth',0.33732,9.612e-05,0.0007308,4.505613306,0.0021672);
INSERT INTO "upstream_database" VALUES ('oil_heat_10_kw_condensing','kwhth',0.3402,0.00010764,0.0007488,4.550519751,0.0021888);
INSERT INTO "upstream_database" VALUES ('natual_gas_heat_more_than_100kw_condensing_modulating','kwhth',0.25668,0.00045,0.0022212,4.408316008,0.0021204);
INSERT INTO "upstream_database" VALUES ('natual_gas_heat_more_than_100kw_condensing_modulating','kwhth',0.23976,2.88e-05,0.00017712,4.221205821,0.0020304);
INSERT INTO "upstream_database" VALUES ('coal_electricity','mj fuel',0.108,0.000105,0.00016,1.783783784,0.000858);
INSERT INTO "upstream_database" VALUES ('miscanthus_combustion_direct','kwhth',NULL,5.6e-05,0.0003024,0.0,0.0);
INSERT INTO "upstream_database" VALUES ('biodiesel_trans_and_process','t seeds',192.7341117,0.179159731,0.459807925,3198.926049,1.53868343);
INSERT INTO "upstream_database" VALUES ('ww_bioethanol_trans_and_process','t ww grain',242.3483185,0.195088925,0.537325631,4055.041042,1.950474741);
INSERT INTO "upstream_database" VALUES ('sb_bioethanol_trans_and_process','t sb grain',0.0,0.0,0.0,0.0,0.0);
INSERT INTO "upstream_database" VALUES ('diesel_direct','kg',3.0468,0.0,0.0,0.0,0.0);
INSERT INTO "upstream_database" VALUES ('petrol_indirect_and_direct','kg',3.886,0.000958,0.00695,52.80665281,0.0254);
INSERT INTO "upstream_database" VALUES ('palm_oil_direct','kg',2.33,0.0057,0.0084,0.005966736,2.87e-06);
INSERT INTO "upstream_database" VALUES ('palm_oil_iluc','kg',5.330349632,0.002100208,NULL,NULL,NULL);
INSERT INTO "upstream_database" VALUES ('maize','kg dm',0.168353489,0.001481882,0.003792413,0.319186411,0.000153529);
INSERT INTO "upstream_database" VALUES ('maize_iluc_factor','kg dm',1.860524153,0.000733064,NULL,0.0,0.0);
INSERT INTO "upstream_database" VALUES ('pig_slurry_per_kg_n_excreted','kg nex',9.601107714,0.0273275,0.124925714,0.0,0.0);
INSERT INTO "animal_features_database" VALUES ('ireland',40.0,773.0,538.0,600.0,0.0,0.0,0.71,0.56,0.53,0.54,0.85,0.87,0.65,0.81,0.56,0.83,0.68,0.84,0.09,0.22,0.06,0.2,0.07,0.26,0.0,0.02,0.07,0.07,0.07,0.07,0.07,0.07,0.07,0.07,0.07,0.07,0.07,0.07,0.07,0.07,0.07,0.07,0.07,0.07,0.07,0.07);
INSERT INTO "animal_features_database" VALUES ('costa rica',40.0,773.0,538.0,600.0,0.0,0.0,0.19,0.65,0.19,0.65,0.19,0.65,0.19,0.65,0.19,0.65,0.19,0.65,0.19,0.65,0.19,0.65,0.19,0.65,0.0,0.02,0.07,0.07,0.07,0.07,0.07,0.07,0.07,0.07,0.07,0.07,0.07,0.07,0.07,0.07,0.07,0.07,0.07,0.07,0.07,0.07);
INSERT INTO "emissions_factors_database" VALUES ('ireland',0.322,0.386,0.37,0.17,0.36,0.0,0.8,1.0,1.0,0.1,0.065,0.065,0.065,0.065,0.06,0.0088,0.01,0.01,0.011,0.277,0.168,0.1,0.35,0.17,0.1,0.0959,0.005,0.0,0.005,0.0,0.0,0.68,0.342,0.0972,0.2268,0.0025,0.004,0.45,0.09675,0.1,0.014,0.02,0.03);
INSERT INTO "emissions_factors_database" VALUES ('costa rica',0.322,0.386,0.37,0.17,0.36,0.0,0.8,1.0,1.2,0.1,0.074,0.061,0.061,0.061,0.06,0.02,0.01,0.01,0.011,0.277,0.168,0.1,0.35,0.26,0.04,0.0,0.0,0.0,0.005,0.0,0.0,0.68,0.342,0.0972,0.2268,0.0025,0.004,0.45,0.09675,0.1,0.01,0.02,0.03);
INSERT INTO "concentrate_database" VALUES ('concentrate',90.0,85.0,13.8,18.45,0.577,0.00708);
INSERT INTO "concentrate_database" VALUES ('Soybean',88.1,92.8,53.5,19.7,4.547587674,0.000402464988069694);
INSERT INTO "concentrate_database" VALUES ('Maize',86.3,86.1,9.4,18.7,0.168353489,0.00148188152565454);
INSERT INTO "concentrate_database" VALUES ('Polinaza',78.0,68.8,24.2,11.6,0.136722899,0.000973090381494048);
INSERT INTO "concentrate_database" VALUES ('Yuca',22.5,62.6,24.9,19.9,0.26143796,0.00165);
INSERT INTO "concentrate_database" VALUES ('Molasses',60.0,76.6,4.1,15.152356,0.745511946,0.0);
INSERT INTO "concentrate_database" VALUES ('Hay',90.0,54.6,5.4,17.6,0.492180134,0.0071469177063879);
INSERT INTO "concentrate_database" VALUES ('Citrocom',89.7,72.0,11.65,16.729724,9.5708e-07,3.27324946179183e-11);
INSERT INTO "concentrate_database" VALUES ('Pineapple',20.6,72.0,9.1,18.2,0.205691382,4.93185478839864e-05);
INSERT INTO "concentrate_database" VALUES ('Silage',28.2,68.6,7.2,19.0,0.08868702,0.00202045892980944);
INSERT INTO "concentrate_database" VALUES ('Semolina',89.85,68.5,14.8,20.936736,1.505706349,0.000366533939851299);
INSERT INTO "concentrate_database" VALUES ('Banana',21.9,78.0,5.2,17.1,0.0,0.0);
COMMIT;
