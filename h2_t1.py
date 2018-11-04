import urllib
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np


def getData(data, tag, convert_type):
    tmp = []
    last = 0
    value = 0

    for v in data(tag):

        if v.text:
            value = float(v.text) if convert_type == "float" else int(v.text)
            tmp.append(value)
            last = value
        else:
            tmp.append(last)

    tmp.reverse()
    return tmp


def save_as_pdf(fig):
    fig.savefig("energy_vs_gdp.pdf", bbox_inches='tight')


def make_graph(energy_values, gdp_values, years):

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
    ax2.legend(loc=1)
    fig.tight_layout()

    save_as_pdf(fig)
    plt.show()


def main():
    gdp_values = []
    energy_values = []
    years = []

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

        energy_values = energy_values + getData(energy_soup, "value", "float")

        gdp_values = gdp_values + getData(gdp_soup, "value", "float")

        years = years + getData(energy_soup, "date", "int")

    make_graph(energy_values, gdp_values, years)


main()
