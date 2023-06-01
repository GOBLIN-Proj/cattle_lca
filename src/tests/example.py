import pandas as pd
from cattle_lca.models import (
    load_livestock_data,
    load_farm_data,
    create_emissions_dictionary,
)
from cattle_lca.lca import ClimateChangeTotals


def main():
    # Create a dictionary to store results
    index = -1
    emissions_dict = create_emissions_dictionary([index])

    # Create some data to generate results

    livestock_data = [
        [
            "ireland",
            2018,
            2018,
            "dairy_cows",
            175298,
            538,
            14.953,
            "irish_grass",
            "pasture",
            "concentrate",
            2.992828296,
            13.5890411,
            10.4109589,
            0,
            0,
            "tank liquid",
            "broadcast",
            0,
            0,
        ],
        [
            "ireland",
            2018,
            2018,
            "suckler_cows",
            30587,
            600,
            1.410958904,
            "irish_grass",
            "pasture",
            "concentrate",
            0.842751605,
            12.2739726,
            11.7260274,
            0,
            0,
            "tank liquid",
            "broadcast",
            0,
            0,
        ],
        [
            "ireland",
            2018,
            2018,
            "DxD_heifers_more_2_yr",
            384.1446311,
            122.125,
            0,
            "irish_grass",
            "pasture",
            "concentrate",
            0,
            12.98630137,
            11.01369863,
            0,
            0,
            "tank liquid",
            "broadcast",
            0,
            0,
        ],
        [
            "ireland",
            2018,
            2018,
            "DxB_heifers_more_2_yr",
            0,
            94.75,
            0,
            "irish_grass",
            "pasture",
            "concentrate",
            0,
            12.98630137,
            11.01369863,
            0,
            0,
            "tank liquid",
            "broadcast",
            0,
            0,
        ],
        [
            "ireland",
            2018,
            2018,
            "BxB_heifers_more_2_yr",
            0,
            103.875,
            0,
            "irish_grass",
            "pasture",
            "concentrate",
            0,
            12.38356164,
            11.61643836,
            0,
            0,
            "tank liquid",
            "broadcast",
            0,
            0,
        ],
        [
            "ireland",
            2018,
            2018,
            "DxD_heifers_less_2_yr",
            49298.56099,
            395.875,
            0,
            "irish_grass",
            "pasture",
            "concentrate",
            0,
            11.56164384,
            12.43835616,
            0,
            0,
            "tank liquid",
            "broadcast",
            0,
            0,
        ],
        [
            "ireland",
            2018,
            2018,
            "DxB_heifers_less_2_yr",
            30347.42586,
            346.6,
            0,
            "irish_grass",
            "pasture",
            "concentrate",
            0,
            11.56164384,
            12.43835616,
            0,
            0,
            "tank liquid",
            "broadcast",
            0,
            0,
        ],
        [
            "ireland",
            2018,
            2018,
            "BxB_heifers_less_2_yr",
            14763.98982,
            412.3,
            0,
            "irish_grass",
            "pasture",
            "concentrate",
            0,
            11.56164384,
            12.43835616,
            0,
            0,
            "tank liquid",
            "broadcast",
            0,
            0,
        ],
        [
            "ireland",
            2018,
            2018,
            "DxD_steers_less_2_yr",
            37646.17385,
            463.475,
            0,
            "irish_grass",
            "pasture",
            "concentrate",
            0,
            11.56164384,
            12.43835616,
            0,
            0,
            "tank liquid",
            "broadcast",
            0,
            0,
        ],
        [
            "ireland",
            2018,
            2018,
            "DxB_steers_less_2_yr",
            29323.04018,
            474.425,
            0,
            "irish_grass",
            "pasture",
            "concentrate",
            0,
            11.56164384,
            12.43835616,
            0,
            0,
            "tank liquid",
            "broadcast",
            0,
            0,
        ],
        [
            "ireland",
            2018,
            2018,
            "BxB_steers_less_2_yr",
            14327.92261,
            479.9,
            0,
            "irish_grass",
            "pasture",
            "concentrate",
            0,
            11.56164384,
            12.43835616,
            0,
            0,
            "tank liquid",
            "broadcast",
            0,
            0,
        ],
        [
            "ireland",
            2018,
            2018,
            "DxD_steers_more_2_yr",
            5506.073046,
            140.45,
            0,
            "irish_grass",
            "pasture",
            "concentrate",
            0,
            18.73972603,
            5.260273973,
            0,
            0,
            "tank liquid",
            "broadcast",
            0,
            0,
        ],
        [
            "ireland",
            2018,
            2018,
            "DxB_steers_more_2_yr",
            4225.590942,
            129.5,
            0,
            "irish_grass",
            "pasture",
            "concentrate",
            0,
            18.73972603,
            5.260273973,
            0,
            0,
            "tank liquid",
            "broadcast",
            0,
            0,
        ],
        [
            "ireland",
            2018,
            2018,
            "BxB_steers_more_2_yr",
            2273.779022,
            162.35,
            0,
            "irish_grass",
            "pasture",
            "concentrate",
            0,
            18.73972603,
            5.260273973,
            0,
            0,
            "tank liquid",
            "broadcast",
            0,
            0,
        ],
        [
            "ireland",
            2018,
            2018,
            "DxD_calves_f",
            46993.69321,
            149.575,
            0,
            "irish_grass",
            "pasture",
            "concentrate",
            1,
            7.945205479,
            16.05479452,
            0,
            0,
            "tank liquid",
            "broadcast",
            0,
            0,
        ],
        [
            "ireland",
            2018,
            2018,
            "DxB_calves_f",
            33164.48649,
            116.725,
            0,
            "irish_grass",
            "pasture",
            "concentrate",
            1,
            7.945205479,
            16.05479452,
            0,
            0,
            "tank liquid",
            "broadcast",
            0,
            0,
        ],
        [
            "ireland",
            2018,
            2018,
            "BxB_calves_f",
            13985.29837,
            175.125,
            0,
            "irish_grass",
            "pasture",
            "concentrate",
            1,
            7.945205479,
            16.05479452,
            0,
            0,
            "tank liquid",
            "broadcast",
            0,
            0,
        ],
        [
            "ireland",
            2018,
            2018,
            "DxD_calves_m",
            32140.1008,
            122.2,
            0,
            "irish_grass",
            "pasture",
            "concentrate",
            1,
            7.945205479,
            16.05479452,
            0,
            0,
            "tank liquid",
            "broadcast",
            0,
            0,
        ],
        [
            "ireland",
            2018,
            2018,
            "DxB_calves_m",
            31755.95617,
            118.55,
            0,
            "irish_grass",
            "pasture",
            "concentrate",
            1,
            7.945205479,
            16.05479452,
            0,
            0,
            "tank liquid",
            "broadcast",
            0,
            0,
        ],
        [
            "ireland",
            2018,
            2018,
            "BxB_calves_m",
            13424.64053,
            178.775,
            0,
            "irish_grass",
            "pasture",
            "concentrate",
            1,
            7.945205479,
            16.05479452,
            0,
            0,
            "tank liquid",
            "broadcast",
            0,
            0,
        ],
        [
            "ireland",
            2018,
            2018,
            "bulls",
            4641.388771,
            773,
            0,
            "irish_grass",
            "pasture",
            "concentrate",
            0.654140961,
            11.56164384,
            12.43835616,
            0,
            0,
            "tank liquid",
            "broadcast",
            0,
            0,
        ],
    ]

    columns = [
        "ef_country",
        "farm_id",
        "year",
        "cohort",
        "pop",
        "weight",
        "daily_milk",
        "forage",
        "grazing",
        "con_type",
        "con_amount",
        "t_outdoors",
        "t_indoors",
        "wool",
        "t_stabled",
        "mm_storage",
        "daily_spreading",
        "n_sold",
        "n_bought",
    ]

    livestock_data_frame = pd.DataFrame(livestock_data, columns=columns)

    farm_data = {
        "ef_country": ["ireland"],
        "farm_id": [2018],
        "year": [2018],
        "total_urea": [2072487.127],
        "total_urea_abated": [0],
        "total_n_fert": [17310655.18],
        "total_p_fert": [1615261.859],
        "total_k_fert": [3922778.8],
        "diesel_kg": [0],
        "elec_kwh": [0],
    }

    farm_dataframe = pd.DataFrame(farm_data)

    # Instantiate ClimateChange Totals Class, passing Ireland as the emissions factor country
    climatechange = ClimateChangeTotals("ireland")

    # load the dataframes
    animals = load_livestock_data(livestock_data_frame)
    farms = load_farm_data(farm_dataframe)

    animals_loc = list(animals.keys())[0]
    farm_loc = list(farms.keys())[0]

    # generate results and store them in the dictionary

    emissions_dict["enteric_ch4"][index] += climatechange.CH4_enteric_ch4(
        animals[animals_loc]["animals"]
    )
    emissions_dict["manure_management_N2O"][index] += climatechange.Total_storage_N2O(
        animals[animals_loc]["animals"]
    )
    emissions_dict["manure_management_CH4"][
        index
    ] += climatechange.CH4_manure_management(animals[animals_loc]["animals"])
    emissions_dict["manure_applied_N"][index] += climatechange.Total_N2O_Spreading(
        animals[animals_loc]["animals"]
    )
    emissions_dict["N_direct_PRP"][index] += climatechange.N2O_total_PRP_N2O_direct(
        animals[animals_loc]["animals"]
    )

    emissions_dict["N_indirect_PRP"][index] += climatechange.N2O_total_PRP_N2O_indirect(
        animals[animals_loc]["animals"]
    )
    emissions_dict["N_direct_fertiliser"][index] = climatechange.N2O_direct_fertiliser(
        farms[farm_loc].total_urea,
        farms[farm_loc].total_urea_abated,
        farms[farm_loc].total_n_fert,
    )

    emissions_dict["N_indirect_fertiliser"][
        index
    ] += climatechange.N2O_fertiliser_indirect(
        farms[farm_loc].total_urea,
        farms[farm_loc].total_urea_abated,
        farms[farm_loc].total_n_fert,
    )
    emissions_dict["soils_CO2"][index] += climatechange.CO2_soils_GWP(
        farms[farm_loc].total_urea,
        farms[farm_loc].total_urea_abated,
    )

    # Add the totals
    emissions_dict["soil_organic_N_direct"][index] = (
        emissions_dict["manure_applied_N"][index]
        + emissions_dict["N_direct_PRP"][index]
    )
    emissions_dict["soil_organic_N_indirect"][index] = emissions_dict["N_indirect_PRP"][
        index
    ]

    emissions_dict["soil_inorganic_N_direct"][index] = emissions_dict[
        "N_direct_fertiliser"
    ][index]
    emissions_dict["soil_inorganic_N_indirect"][index] = emissions_dict[
        "N_indirect_fertiliser"
    ][index]

    emissions_dict["soil_N_direct"][index] = (
        emissions_dict["soil_organic_N_direct"][index]
        + emissions_dict["soil_inorganic_N_direct"][index]
    )

    emissions_dict["soil_N_indirect"][index] = (
        emissions_dict["soil_inorganic_N_indirect"][index]
        + emissions_dict["soil_organic_N_indirect"][index]
    )

    emissions_dict["soils_N2O"][index] = (
        emissions_dict["soil_N_direct"][index]
        + emissions_dict["soil_N_indirect"][index]
    )

    # Print the emission results dictionary
    print(emissions_dict)


if __name__ == "__main__":
    main()
