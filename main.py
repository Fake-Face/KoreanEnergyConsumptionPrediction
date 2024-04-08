from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

TOETOGWH = 11630  # 1 toe = 11.63 GWh


# Under the both roadmaps, the portion of coal and LNG in the country's electricity mix will be
# lowered to 21.8% and 19.5% respectively by 2030, respectively, compared with 41.9% and 26.8% in 2018,
# respectively, the official said.


def main():
    print_data_generation_power()
    print_data_consumption_power()


def print_data_consumption_power():
    years = []
    years_tempo = []
    data_dict = {}
    # open the csv file
    with open('Total_Final_Energy_Consumption_by_Sources_20230513135544.csv', 'r') as f:
        # read the csv file
        data = f.read()
        # split the data by new line
        data = data.split('\n')
        # get the years in the first row
        # verify if the year is a number
        # Add years from 2014.01 to 2023.01
        current_year = 2014
        current_month = 1
        for i in range(0, 109):
            if current_month == 13:
                current_month = 1
                current_year += 1
            years_tempo.append((str(current_year) + '.' + str(current_month)))
            current_month += 1

        # get the data from the csv file
        for i in data[1:]:
            # split the data by comma
            i = i.split(',')
            # get the key name
            key = i[0]
            j = 1
            while key == '':
                key = i[0 + j]
                j += 1
            # get the values
            # check if the value is a number
            values = []
            for k in i[1:]:
                if k.isnumeric():
                    k = float(k)
                    k = k * TOETOGWH
                    values.append(k)
            # add the key and values to the dictionary
            data_dict[key] = values
        # transform years as datetime
        years_tempo = [str(i) for i in years_tempo]

        for i in years_tempo:
            month = int(i.split('.')[1])
            year = int(i.split('.')[0])
            years.append(datetime(year, month, 1))
        # transform the values as float
        for i in data_dict:
            data_dict[i] = [float(j) for j in data_dict[i]]
        # plot the data
        plt.close()
        plt.plot(years, data_dict['"Petroleum"'], label='Petroleum')
        plt.plot(years, data_dict['"Coal"'], label='Coal')
        plt.plot(years, data_dict['"Electricity"'], label='Electricity')
        plt.plot(years, data_dict['"Total"'], label='Sum')
        plt.plot(years, data_dict['"Natural gas"'], label='LNG')
        plt.plot(years, data_dict['"City gas"'], label='City gas')
        plt.plot(years, data_dict['"Geothermal/ solar/ etc."'], label='Renewable')
        # display nicely the x-axis
        plt.legend()
        plt.ylabel('Energy consumption in GWh')
        plt.title('Consumption of energy in South Korea')
        plt.savefig('Consumption of energy in South Korea.png')

        years_before_regression = years.copy()
        data_dict_before_regression = data_dict.copy()
        # we will try to predict till 2050
        # we will use linear regression,
        sum_energy_model = LinearRegression()
        coal_model = LinearRegression()
        electricity_model = LinearRegression()
        lng_model = LinearRegression()
        city_gas_model = LinearRegression()
        renewable_model = LinearRegression()
        petroleum_model = LinearRegression()
        # transform the years as numbers
        for i in range(0, len(years)):
            years[i] = float(years[i].year + years[i].month / 12)
        sum_energy_model.fit(np.array(years).reshape(-1, 1), data_dict['"Total"'])
        coal_model.fit(np.array(years).reshape(-1, 1), data_dict['"Coal"'])
        electricity_model.fit(np.array(years).reshape(-1, 1), data_dict['"Electricity"'])
        lng_model.fit(np.array(years).reshape(-1, 1), data_dict['"Natural gas"'])
        city_gas_model.fit(np.array(years).reshape(-1, 1), data_dict['"City gas"'])
        renewable_model.fit(np.array(years).reshape(-1, 1), data_dict['"Geothermal/ solar/ etc."'])
        petroleum_model.fit(np.array(years).reshape(-1, 1), data_dict['"Petroleum"'])
        # predict till 2050
        years = []
        for i in range(2014, 2051):
            years.append(i + 1 / 12)
        # plot the data
        plt.plot(years, sum_energy_model.predict(np.array(years).reshape(-1, 1)), label='Sum')
        plt.plot(years, coal_model.predict(np.array(years).reshape(-1, 1)), label='Coal')
        plt.plot(years, electricity_model.predict(np.array(years).reshape(-1, 1)), label='Electricity')
        plt.plot(years, lng_model.predict(np.array(years).reshape(-1, 1)), label='LNG')
        plt.plot(years, city_gas_model.predict(np.array(years).reshape(-1, 1)), label='City gas')
        plt.plot(years, renewable_model.predict(np.array(years).reshape(-1, 1)), label='Renewable')
        plt.plot(years, petroleum_model.predict(np.array(years).reshape(-1, 1)), label='Petroleum')
        # display nicely the x-axis
        plt.legend()
        plt.title('Consumption of energy in South Korea')
        plt.savefig('Consumption of energy in South Korea_2050.png')

        # modify variables for 2030
        years_before_regression.append(datetime(2027, 1, 1))
        total = sum_energy_model.predict(np.array([2030 + 1 / 12]).reshape(-1, 1))[0]
        data_dict_before_regression['"Total"'].append(total)
        data_dict_before_regression['"Coal"'].append(coal_model.predict(np.array([2030 + 1 / 12]).reshape(-1, 1))[0])
        data_dict_before_regression['"Electricity"'].append(total * 32 / 100)
        data_dict_before_regression['"Natural gas"'].append(
            lng_model.predict(np.array([2030 + 1 / 12]).reshape(-1, 1))[0])
        data_dict_before_regression['"City gas"'].append(
            city_gas_model.predict(np.array([2030 + 1 / 12]).reshape(-1, 1))[0])
        data_dict_before_regression['"Geothermal/ solar/ etc."'].append(
            renewable_model.predict(np.array([2030 + 1 / 12]).reshape(-1, 1))[0])
        data_dict_before_regression['"Petroleum"'].append(total * 37 / 100)
        # plot the data
        plt.plot(years_before_regression, data_dict_before_regression['"Total"'], label='Sum')
        plt.plot(years_before_regression, data_dict_before_regression['"Coal"'], label='Coal')
        plt.plot(years_before_regression, data_dict_before_regression['"Electricity"'], label='Electricity')
        plt.plot(years_before_regression, data_dict_before_regression['"Natural gas"'], label='LNG')
        plt.plot(years_before_regression, data_dict_before_regression['"City gas"'], label='City gas')
        plt.plot(years_before_regression, data_dict_before_regression['"Geothermal/ solar/ etc."'], label='Renewable')
        plt.plot(years_before_regression, data_dict_before_regression['"Petroleum"'], label='Petroleum')
        # display nicely the x-axis
        plt.legend()
        plt.title('Consumption of energy in South Korea')
        plt.savefig('Consumption of energy in South Korea_modified.png')

        # predict till 2050
        # reset the models
        sum_energy_model = LinearRegression()
        coal_model = LinearRegression()
        electricity_model = LinearRegression()
        lng_model = LinearRegression()
        city_gas_model = LinearRegression()
        renewable_model = LinearRegression()
        petroleum_model = LinearRegression()
        # transform the years as numbers
        for i in range(0, len(years_before_regression)):
            years_before_regression[i] = float(years_before_regression[i].year + years_before_regression[i].month / 12)
        sum_energy_model.fit(np.array(years_before_regression).reshape(-1, 1), data_dict_before_regression['"Total"'])
        coal_model.fit(np.array(years_before_regression).reshape(-1, 1), data_dict_before_regression['"Coal"'])
        electricity_model.fit(np.array(years_before_regression).reshape(-1, 1),
                              data_dict_before_regression['"Electricity"'])
        lng_model.fit(np.array(years_before_regression).reshape(-1, 1), data_dict_before_regression['"Natural gas"'])
        city_gas_model.fit(np.array(years_before_regression).reshape(-1, 1), data_dict_before_regression['"City gas"'])
        renewable_model.fit(np.array(years_before_regression).reshape(-1, 1),
                            data_dict_before_regression['"Geothermal/ solar/ etc."'])
        petroleum_model.fit(np.array(years_before_regression).reshape(-1, 1),
                            data_dict_before_regression['"Petroleum"'])
        # predict till 2050
        years = []
        for i in range(2014, 2051):
            years.append(i + 1 / 12)
        # plot the data
        plt.plot(years, sum_energy_model.predict(np.array(years).reshape(-1, 1)), label='Sum')
        plt.plot(years, coal_model.predict(np.array(years).reshape(-1, 1)), label='Coal')
        plt.plot(years, electricity_model.predict(np.array(years).reshape(-1, 1)), label='Electricity')
        plt.plot(years, lng_model.predict(np.array(years).reshape(-1, 1)), label='LNG')
        plt.plot(years, city_gas_model.predict(np.array(years).reshape(-1, 1)), label='City gas')
        plt.plot(years, renewable_model.predict(np.array(years).reshape(-1, 1)), label='Renewable')
        plt.plot(years, petroleum_model.predict(np.array(years).reshape(-1, 1)), label='Petroleum')
        # display nicely the x-axis
        plt.legend()
        plt.title('Consumption of energy in South Korea')
        plt.savefig('Consumption of energy in South Korea_modified_2050.png')


def print_data_generation_power():
    years = []
    # open the csv file
    with open('Generation_amount_of_energy_by_source_20230427164049.csv', 'r') as f:
        # read the csv file
        data = f.read()
        # split the data by new line
        data = data.split('\n')
        # get the years in the first row
        # verify if the year is a number
        for i in data[0].split(','):
            if i.isnumeric():
                years.append(i)
        # create a dictionary to store the data
        data_dict = {}
        # get the data from the csv file
        for i in data[1:]:
            # split the data by comma
            i = i.split(',')
            # get the key name
            key = i[0]
            j = 1
            while key == '':
                key = i[0 + j]
                j += 1
            # get the values
            # check if the value is a number
            values = []
            for k in i[1:]:
                if k.isnumeric():
                    values.append(k)
            # add the key and values to the dictionary
            data_dict[key] = values
        # transform years as datetime
        years = [int(i) for i in years]
        # transform the values as float
        for i in data_dict:
            data_dict[i] = [float(j) for j in data_dict[i]]

        plot_generation(data_dict, years, 'Generation of energy in South Korea.png')

        # we will try to predict when the renewable energy will be more than coal, LNG and oil
        # we will use linear regression,
        # but first we will calculate the percentage of coal, LNG and oil in 2030
        sum_energy_model = LinearRegression()
        sum_energy_model.fit(np.array(years).reshape(-1, 1), data_dict['Sum'])
        predicted_energy = sum_energy_model.predict(np.array(2030).reshape(-1, 1))
        data_dict['Sum'].append(predicted_energy[0])
        data_dict['Coal'].append(predicted_energy[0] * 0.218)
        data_dict['LNG'].append(predicted_energy[0] * 0.195)
        sum_oil_model = LinearRegression()
        sum_oil_model.fit(np.array(years).reshape(-1, 1), data_dict['Oil'])
        predicted_oil = sum_oil_model.predict(np.array(2030).reshape(-1, 1))
        data_dict['Oil'].append(predicted_oil[0])
        sum_renewable_model = LinearRegression()
        sum_renewable_model.fit(np.array(years).reshape(-1, 1), data_dict['Renewable and others'])
        predicted_renewable = [predicted_energy[0] * 0.302]
        data_dict['Renewable and others'].append(predicted_renewable[0])
        sum_nuclear_model = LinearRegression()
        sum_nuclear_model.fit(np.array(years).reshape(-1, 1), data_dict['nuclear power'])
        predicted_nuclear = [predicted_energy[0] * 0.239]
        data_dict['nuclear power'].append(predicted_nuclear[0])
        years.append(2030)

        # plot the data
        plot_generation(data_dict, years, 'Generation of energy in South Korea_2030.png', 3)

        # expanding the model to 2050 passing through 2040
        predicted_energy = sum_energy_model.predict(np.array(2040).reshape(-1, 1))
        data_dict['Sum'].append(predicted_energy[0])
        predicted_energy = sum_energy_model.predict(np.array(2050).reshape(-1, 1))
        data_dict['Sum'].append(predicted_energy[0])
        predicted_oil = sum_oil_model.predict(np.array(2040).reshape(-1, 1))
        data_dict['Oil'].append(predicted_oil[0])
        predicted_oil = sum_oil_model.predict(np.array(2050).reshape(-1, 1))
        data_dict['Oil'].append(predicted_oil[0])
        predicted_renewable = sum_renewable_model.predict(np.array(2040).reshape(-1, 1))
        data_dict['Renewable and others'].append(predicted_renewable[0])
        predicted_renewable = sum_renewable_model.predict(np.array(2050).reshape(-1, 1))
        data_dict['Renewable and others'].append(predicted_renewable[0])
        sum_coal_model = LinearRegression()
        sum_coal_model.fit(np.array(years).reshape(-1, 1), data_dict['Coal'])
        predicted_coal = sum_coal_model.predict(np.array(2040).reshape(-1, 1))
        data_dict['Coal'].append(predicted_coal[0])
        predicted_coal = sum_coal_model.predict(np.array(2050).reshape(-1, 1))
        data_dict['Coal'].append(predicted_coal[0])
        sum_lng_model = LinearRegression()
        sum_lng_model.fit(np.array(years).reshape(-1, 1), data_dict['LNG'])
        predicted_lng = sum_lng_model.predict(np.array(2040).reshape(-1, 1))
        data_dict['LNG'].append(predicted_lng[0])
        predicted_lng = sum_lng_model.predict(np.array(2050).reshape(-1, 1))
        data_dict['LNG'].append(predicted_lng[0])
        sum_nuclear_model = LinearRegression()
        sum_nuclear_model.fit(np.array(years).reshape(-1, 1), data_dict['nuclear power'])
        predicted_nuclear = sum_nuclear_model.predict(np.array(2040).reshape(-1, 1))
        data_dict['nuclear power'].append(predicted_nuclear[0])
        predicted_nuclear = sum_nuclear_model.predict(np.array(2050).reshape(-1, 1))
        data_dict['nuclear power'].append(predicted_nuclear[0])
        years.append(2040)
        years.append(2050)

        # plot the data
        plot_generation(data_dict, years,'Generation of energy in South Korea_2050.png', 7)

        # we will try to predict the 2060 and 2070 years
        predicted_energy = sum_energy_model.predict(np.array(2060).reshape(-1, 1))
        data_dict['Sum'].append(predicted_energy[0])
        predicted_energy = sum_energy_model.predict(np.array(2070).reshape(-1, 1))
        data_dict['Sum'].append(predicted_energy[0])
        predicted_oil = sum_oil_model.predict(np.array(2060).reshape(-1, 1))
        data_dict['Oil'].append(predicted_oil[0])
        predicted_oil = sum_oil_model.predict(np.array(2070).reshape(-1, 1))
        data_dict['Oil'].append(predicted_oil[0])
        predicted_renewable = sum_renewable_model.predict(np.array(2060).reshape(-1, 1))
        data_dict['Renewable and others'].append(predicted_renewable[0])
        predicted_renewable = sum_renewable_model.predict(np.array(2070).reshape(-1, 1))
        data_dict['Renewable and others'].append(predicted_renewable[0])
        predicted_coal = sum_coal_model.predict(np.array(2060).reshape(-1, 1))
        data_dict['Coal'].append(predicted_coal[0])
        predicted_coal = sum_coal_model.predict(np.array(2070).reshape(-1, 1))
        data_dict['Coal'].append(predicted_coal[0])
        predicted_lng = sum_lng_model.predict(np.array(2060).reshape(-1, 1))
        data_dict['LNG'].append(predicted_lng[0])
        predicted_lng = sum_lng_model.predict(np.array(2070).reshape(-1, 1))
        data_dict['LNG'].append(predicted_lng[0])
        predicted_nuclear = sum_nuclear_model.predict(np.array(2060).reshape(-1, 1))
        data_dict['nuclear power'].append(predicted_nuclear[0])
        predicted_nuclear = sum_nuclear_model.predict(np.array(2070).reshape(-1, 1))
        data_dict['nuclear power'].append(predicted_nuclear[0])
        years.append(2060)
        years.append(2070)

        # plot the data
        plot_generation(data_dict, years,'Generation of energy in South Korea_2070.png', 10)

        # we will plot data for total energy consumption


def plot_generation(data_dict, years, name, ticks=1):
    # check if data is under 0, and if it is, set it to 0
    for key in data_dict:
        for i in range(len(data_dict[key])):
            if data_dict[key][i] < 0:
                data_dict[key][i] = 0
    plt.plot(years, data_dict['Coal'], label='Coal')
    plt.plot(years, data_dict['LNG'], label='LNG')
    plt.plot(years, data_dict['Oil'], label='Oil')
    plt.plot(years, data_dict['Sum'], label='Sum')
    plt.plot(years, data_dict['nuclear power'], label='nuclear power')
    plt.plot(years, data_dict['Renewable and others'], label='Renewable')
    plt.xlabel('Year')
    plt.ylabel('Energy generation in GWh')
    plt.title('Energy generation in South Korea')
    plt.xticks(np.arange(min(years), max(years) + 1, ticks))
    plt.legend()
    plt.savefig(name)


main()
