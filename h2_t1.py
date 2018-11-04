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
    ax2 = ax1.twinx()

    ax2.set_ylabel("GDP", color=gdp_color)
    ax2.plot(t, gdp_values, label="GDP", color=gdp_color)
    ax2.tick_params(axis='y', labelcolor=gdp_color)
    fig.tight_layout()
    fig.legend(loc=1, bbox_to_anchor=(1, 1), bbox_transform=ax2.transAxes)
    save_as_pdf(fig)
    plt.show()


def load_data(url, value):
    tmp = []
    convert_type = "float" if value == "value" else "int"
    req = urllib.request.urlopen(url)
    data = req.read()
    soup = BeautifulSoup(data, "xml")
    pages = int(soup.find('data')['pages'])

    for i in range(1, pages + 1):
        page = "?page=" + str(i)
        data_req = urllib.request.urlopen(url + page)
        data_read = data_req.read()
        data_soup = BeautifulSoup(data_read, "xml")
        tmp = tmp + getData(data_soup, value, convert_type)

    return tmp


def main():
    gdp_values = load_data(
        "http://api.worldbank.org/countries/fin/indicators/NY.GDP.PCAP.CD", "value")
    energy_values = load_data(
        "http://api.worldbank.org/countries/fin/indicators/EG.USE.PCAP.KG.OE", "value")
    years = load_data(
        "http://api.worldbank.org/countries/fin/indicators/NY.GDP.PCAP.CD", "date")

    make_graph(energy_values, gdp_values, years)


main()
