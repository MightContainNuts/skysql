import data
from datetime import datetime
import sqlalchemy
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

SQLITE_URI = "sqlite:///data/flights.sqlite3"
IATA_LENGTH = 3


def delayed_flights_by_airline(data_manager):
    """
    Asks the user for a textual airline name (any string will work here).
    Then runs the query using the data object method
    "get_delayed_flights_by_airline".
    When results are back, calls "print_results" to show them to on the screen.
    """
    airline_input = input("Enter airline name: ")
    results = data_manager.get_delayed_flights_by_airline(airline_input)
    print_results(results)


def delayed_flights_by_airport(data_manager):
    """
    Asks the user for a textual IATA 3-letter airport code (loops until input
    is valid). Then runs the query using the data object method
    "get_delayed_flights_by_airport".When results are back, calls
    "print_results" to show them to on the screen.
    """
    valid = False
    while not valid:
        airport_input = input("Enter origin airport IATA code: ")
        # Valide input
        if airport_input.isalpha() and len(airport_input) == IATA_LENGTH:
            valid = True
    results = data_manager.get_delayed_flights_by_airport(airport_input)
    print_results(results)


def flight_by_id(data_manager):
    """
    Asks the user for a numeric flight ID,
    Then runs the query using the data object method "get_flight_by_id".
    When results are back, calls "print_results" to show them to on the screen.
    """
    valid = False
    while not valid:
        try:
            id_input = int(input("Enter flight ID: "))
        except Exception as e:
            print("Try again...", e)
        else:
            valid = True
    results = data_manager.get_flight_by_id(id_input)
    print_results(results)


def flights_by_date(data_manager):
    """
    Asks the user for date input (and loops until it's valid),
    Then runs the query using the data object method "get_flights_by_date".
    When results are back, calls "print_results" to show them to on the screen.
    """
    valid = False
    while not valid:
        try:
            date_input = input("Enter date in DD/MM/YYYY format: ")
            date = datetime.strptime(date_input, "%d/%m/%Y")
        except ValueError as e:
            print("Try again...", e)
        else:
            valid = True
    results = data_manager.get_flights_by_date(date.day, date.month, date.year)
    print_results(results)


def plot_delayed_flights_by_airline_as_percentage(data_manager):
    """
    plot percentages of delayed gflights
    :param data_manager:
    :type data_manager:
    :return:
    :rtype:
    """
    results = data_manager.plot_delayed_flights_by_airline_as_percentage()
    x, y = zip(*results)
    colors = plt.cm.viridis(np.linspace(0, 1, len(x)))
    plt.title("Percentage of delayed flights by airline")
    plt.bar(x, y, color=colors)
    plt.xlabel("Airline")
    plt.ylabel("Percentage of delayed flights")
    plt.xticks(rotation=45, fontsize=8, ha="right")
    plt.tight_layout()
    plt.show()


def plot_percentage_of_delayed_flights_by_hour(data_manager):
    """
    plot percentage of delayed flights by hour
    :param data_manager:
    :type data_manager:
    :return:
    :rtype:
    """
    results = data_manager.plot_percentage_of_delayed_flights_by_hour()
    x, y = zip(*results)
    colors = plt.cm.viridis(np.linspace(0, 1, len(x)))
    plt.title("Hour of the day")
    plt.bar(x, y, color=colors)
    plt.xlabel("Airline")
    plt.ylabel("Percentage of delayed flights")
    plt.xticks(
        ticks=range(len(x)), labels=x, rotation=0, fontsize=8, ha="center"
    )  # noqa E501
    plt.tight_layout()
    plt.show()


def plot_heatmap_delays_origin_dest(data_manager):
    """
    plot heat map of delays
    :param data_manager:
    :type data_manager:
    :return:
    :rtype:
    """
    results = data_manager.plot_heatmap_delays_origin_dest()
    df = pd.DataFrame(
        results,
        columns=[
            "ORIGIN_AIRPORT",
            "DESTINATION_AIRPORT",
            "PERCENTAGE_DELAYED",
        ],  # noqa E501
    )
    plt.title("Heatmap of delays")

    heatmap_data = df.pivot(
        index="ORIGIN_AIRPORT",
        columns="DESTINATION_AIRPORT",
        values="PERCENTAGE_DELAYED",
    )
    heatmap_data = heatmap_data.fillna(0)
    sns.heatmap(
        heatmap_data,
        annot=False,
        fmt=".1f",
        cmap="YlGnBu",
        cbar_kws={"label": "Percentage Delayed"},
    )
    plt.xticks(rotation=0, fontsize=8, ha="center")
    plt.xticks(rotation=0, fontsize=8, ha="center")
    plt.tight_layout()
    plt.show()


def print_results(results):
    """
    Get a list of flight results (List of dictionary-like objects from
    SQLAachemy).
    Even if there is one result, it should be provided in a list.
    Each object *has* to contain the columns:
    FLIGHT_ID, ORIGIN_AIRPORT, DESTINATION_AIRPORT, AIRLINE, and DELAY.
    """
    print(f"Got {len(results)} results.")
    for result in results:
        # turn result into dictionary
        result = result._mapping

        # Check that all required columns are in place
        try:
            delay = (
                int(result["DELAY"]) if result["DELAY"] else 0
            )  # If delay columns is NULL, set it to 0
            origin = result["ORIGIN_AIRPORT"]
            dest = result["DESTINATION_AIRPORT"]
            airline = result["AIRLINE"]
        except (ValueError, sqlalchemy.exc.SQLAlchemyError) as e:
            print("Error showing results: ", e)
            return

        # Different prints for delayed and non-delayed flights
        if delay and delay > 0:
            print(
                f"{result['ID']}. {origin} -> {dest} by {airline}, Delay: {delay} Minutes"  # noqa E501
            )
        else:
            print(f"{result['ID']}. {origin} -> {dest} by {airline}")


def show_menu_and_get_input():
    """
    Show the menu and get user input.
    If it's a valid option, return a pointer to the function to execute.
    Otherwise, keep asking the user for input.
    """
    print("Menu:")
    for key, value in FUNCTIONS.items():
        print(f"{key}. {value[1]}")

    # Input loop
    while True:
        try:
            choice = int(input())
            if choice in FUNCTIONS:
                return FUNCTIONS[choice][0]
        except ValueError as e:
            print("exception called", e)
        print("Try again...")


"""
Function Dispatch Dictionary
"""
FUNCTIONS = {
    1: (flight_by_id, "Show flight by ID"),
    2: (flights_by_date, "Show flights by date"),
    3: (delayed_flights_by_airline, "Delayed flights by airline"),
    4: (delayed_flights_by_airport, "Delayed flights by origin airport"),
    5: (
        plot_delayed_flights_by_airline_as_percentage,
        "Plot delayed flights by airline",
    ),  # noqa E501
    6: (
        plot_percentage_of_delayed_flights_by_hour,
        "Plot delayed flights by hour",
    ),  # noqa E501
    7: (plot_heatmap_delays_origin_dest, "Heatmap of delays"),
    8: (quit, "Exit"),
}


def main():
    # Create an instance of the Data Object using our SQLite URI
    data_manager = data.FlightData(SQLITE_URI)

    # The Main Menu loop
    while True:
        choice_func = show_menu_and_get_input()
        choice_func(data_manager)


if __name__ == "__main__":
    main()
