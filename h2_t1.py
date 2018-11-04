import urllib
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np

gdp_values = []
energy_values = []
years = []


def getData(data, value, convert_type):
    tmp = []
    last = 0
    value = 0
    for v in data(value):
        value = convert_type == "float" if float(v.text) else int(v.text)
        if v.text:
            tmp.append(value)
        else:
            tmp.append(last)
    last = value
    print(tmp)
    tmp = tmp.reverse()
    print(tmp)
    return tmp


def makeGraph():
    energy_values.reverse()
    gdp_values.reverse()

    fig, ax1 = plt.subplots()
    energy_color = "tab:red"
    gdp_color = "tab:blue"
    t = np.arange(min(years), max(years) + 1, 1)

    ax1.set_xlabel("Year")
    ax1.set_ylabel("Energy", color=energy_color)
    ax1.plot(t, energy_values, label="Energy", color=energy_color)
    ax1.tick_params(axis='y', labelcolor=energy_color)
    ax1.legend(loc=0)
    ax2 = ax1.twinx()

    ax2.set_ylabel("GDP", color=gdp_color)
    ax2.plot(t, gdp_values, label="GDP", color=gdp_color)
    ax2.tick_params(axis='y', labelcolor=gdp_color)
    ax2.legend(loc=0)
    fig.tight_layout()

    plt.show()


def main():

    for i in range(1, 3):
        page = "?page=" + str(i)
        gdp_req = urllib.request.urlopen(
            "http://api.worldbank.org/countries/fin/indicators/NY.GDP.PCAP.CD" + page)
        gdp_data = gdp_req.read()

        energy_req = urllib.request.urlopen(
            "http://api.worldbank.org/countries/fin/indicators/EG.USE.PCAP.KG.OE" + page)
        energy_data = energy_req.read()

        gdp_soup = BeautifulSoup(gdp_data, "xml")
        energy_soup = BeautifulSoup(energy_data, "xml")

        sum(energy_values, getData(energy_soup, "value", "float"))
        sum(gdp_values, getData(gdp_soup, "value", "float"))
        sum(years, getData(energy_soup, "value", "int"))

        makeGraph()


main()
