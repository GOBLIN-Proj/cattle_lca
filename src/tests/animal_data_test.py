from cattle_lca.models import print_livestock_data, load_livestock_data
from cattle_lca.animal_data import AnimalData as ad
import pandas as pd 


def main():

        #Create some data to generate results 

    livestock_data = [
        ['ireland', 2018, 2018, 'dairy_cows', 175298, 538, 14.953, 'irish_grass', 'pasture', 'concentrate', 2.992828296, 13.5890411, 10.4109589, 0, 0, 'tank liquid', 'broadcast', 0, 0],
        ['ireland', 2018, 2018, 'suckler_cows', 30587, 600, 1.410958904, 'irish_grass', 'pasture', 'concentrate', 0.842751605, 12.2739726, 11.7260274, 0, 0, 'tank liquid', 'broadcast', 0, 0],
        ['ireland', 2018, 2018, 'DxD_heifers_more_2_yr', 384.1446311, 122.125, 0, 'irish_grass', 'pasture', 'concentrate', 0, 12.98630137, 11.01369863, 0, 0, 'tank liquid', 'broadcast', 0, 0],
        ['ireland', 2018, 2018, 'DxB_heifers_more_2_yr', 0, 94.75, 0, 'irish_grass', 'pasture', 'concentrate', 0, 12.98630137, 11.01369863, 0, 0, 'tank liquid', 'broadcast', 0, 0],
        ['ireland', 2018, 2018, 'BxB_heifers_more_2_yr', 0, 103.875, 0, 'irish_grass', 'pasture', 'concentrate', 0, 12.38356164, 11.61643836, 0, 0, 'tank liquid', 'broadcast', 0, 0],
        ['ireland', 2018, 2018, 'DxD_heifers_less_2_yr', 49298.56099, 395.875, 0, 'irish_grass', 'pasture', 'concentrate', 0, 11.56164384, 12.43835616, 0, 0, 'tank liquid', 'broadcast', 0, 0],
        ['ireland', 2018, 2018, 'DxB_heifers_less_2_yr', 30347.42586, 346.6, 0, 'irish_grass', 'pasture', 'concentrate', 0, 11.56164384, 12.43835616, 0, 0, 'tank liquid', 'broadcast', 0, 0],
        ['ireland', 2018, 2018, 'BxB_heifers_less_2_yr', 14763.98982, 412.3, 0, 'irish_grass', 'pasture', 'concentrate', 0, 11.56164384, 12.43835616, 0, 0, 'tank liquid', 'broadcast', 0, 0],
        ['ireland', 2018, 2018, 'DxD_steers_less_2_yr', 37646.17385, 463.475, 0, 'irish_grass', 'pasture', 'concentrate', 0, 11.56164384, 12.43835616, 0, 0, 'tank liquid', 'broadcast', 0, 0],
        ['ireland', 2018, 2018, 'DxB_steers_less_2_yr', 29323.04018, 474.425, 0, 'irish_grass', 'pasture', 'concentrate', 0, 11.56164384, 12.43835616, 0, 0, 'tank liquid', 'broadcast', 0, 0],
        ['ireland', 2018, 2018, 'BxB_steers_less_2_yr', 14327.92261, 479.9, 0, 'irish_grass', 'pasture', 'concentrate', 0, 11.56164384, 12.43835616, 0, 0, 'tank liquid', 'broadcast', 0, 0],
        ['ireland', 2018, 2018, 'DxD_steers_more_2_yr', 5506.073046, 140.45, 0, 'irish_grass', 'pasture', 'concentrate', 0, 18.73972603, 5.260273973, 0, 0, 'tank liquid', 'broadcast', 0, 0],
        ['ireland', 2018, 2018, 'DxB_steers_more_2_yr', 4225.590942, 129.5, 0, 'irish_grass', 'pasture', 'concentrate', 0, 18.73972603, 5.260273973, 0, 0, 'tank liquid', 'broadcast', 0, 0],
        ['ireland', 2018, 2018, 'BxB_steers_more_2_yr', 2273.779022, 162.35, 0, 'irish_grass', 'pasture', 'concentrate', 0, 18.73972603, 5.260273973, 0, 0, 'tank liquid', 'broadcast', 0, 0],
        ['ireland', 2018, 2018, 'DxD_calves_f', 46993.69321, 149.575, 0, 'irish_grass', 'pasture', 'concentrate', 1, 7.945205479, 16.05479452, 0, 0, 'tank liquid', 'broadcast', 0, 0],
        ['ireland', 2018, 2018, 'DxB_calves_f', 33164.48649, 116.725, 0, 'irish_grass', 'pasture', 'concentrate', 1, 7.945205479, 16.05479452, 0, 0, 'tank liquid', 'broadcast', 0, 0],
        ['ireland', 2018, 2018, 'BxB_calves_f', 13985.29837, 175.125, 0, 'irish_grass', 'pasture', 'concentrate', 1, 7.945205479, 16.05479452, 0, 0, 'tank liquid', 'broadcast', 0, 0],
        ['ireland', 2018, 2018, 'DxD_calves_m', 32140.1008, 122.2, 0, 'irish_grass', 'pasture', 'concentrate', 1, 7.945205479, 16.05479452, 0, 0, 'tank liquid', 'broadcast', 0, 0],
        ['ireland', 2018, 2018, 'DxB_calves_m', 31755.95617, 118.55, 0, 'irish_grass', 'pasture', 'concentrate', 1, 7.945205479, 16.05479452, 0, 0, 'tank liquid', 'broadcast', 0, 0],
        ['ireland', 2018, 2018, 'BxB_calves_m', 13424.64053, 178.775, 0, 'irish_grass', 'pasture', 'concentrate', 1, 7.945205479, 16.05479452, 0, 0, 'tank liquid', 'broadcast', 0, 0],
        ['ireland', 2018, 2018, 'bulls', 4641.388771, 773, 0, 'irish_grass', 'pasture', 'concentrate', 0.654140961, 11.56164384, 12.43835616, 0, 0, 'tank liquid', 'broadcast', 0, 0]
        ]
    
    columns = ['ef_country', 'farm_id', 'year', 'cohort', 'pop', 'weight', 'daily_milk', 'forage', 'grazing',
                'con_type', 'con_amount', 't_outdoors', 't_indoors', 'wool', 't_stabled', 'mm_storage',
                'daily_spreading', 'n_sold', 'n_bought']
    
    livestock_data_frame = pd.DataFrame(livestock_data, columns=columns)

    animals = load_livestock_data(livestock_data_frame)

    print_livestock_data(animals)

    cohorts = livestock_data_frame.cohort.unique()

    print(cohorts)

    for cohort in cohorts:
        animal = getattr(animals[2018]["animals"], cohort)
        print(f"{cohort}: bought: {ad.get_animal_bought(animal)}")
        print(f"{cohort}: sold: {ad.get_animal_sold(animal)}")
        print(f"{cohort}: population: {ad.get_animal_population(animal)}")
        print(f"{cohort}: weight: {ad.get_animal_weight(animal)}")
        print(f"{cohort}: daily milk: {ad.get_animal_daily_milk(animal)}")
        print(f"{cohort}: grazing: {ad.get_animal_grazing(animal)}")
        print(f"{cohort}: t outdoors: {ad.get_animal_t_outdoors(animal)}")

        print(f"{cohort}: t indoors: {ad.get_animal_t_indoors(animal)}")
        print(f"{cohort}: t stabled: {ad.get_animal_t_stabled(animal)}")
        print(f"{cohort}: mm storage: {ad.get_animal_mm_storage(animal)}")
        print(f"{cohort}: forage: {ad.get_animal_forage(animal)}")
        print(f"{cohort}: concentrate type: {ad.get_animal_concentrate_type(animal)}")
        print(f"{cohort}: concentrate amount: {ad.get_animal_concentrate_amount(animal)}")
        print(f"{cohort}: year: {ad.get_animal_year(animal)}")
        print(f"{cohort}: cohort: {ad.get_animal_cohort(animal)}")
        

if __name__ == '__main__': 
    main()