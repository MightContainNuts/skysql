from sqlalchemy import create_engine, text

QUERY_FLIGHT_BY_ID = """
SELECT
    flights.ID,
    flights.ORIGIN_AIRPORT,
    flights.DESTINATION_AIRPORT,
    airlines.AIRLINE,
    flights.AIRLINE_DELAY AS DELAY
FROM
    flights
    JOIN airlines ON flights.AIRLINE = airlines.ID
WHERE
    flights.ID = :flight_id
;
"""

QUERY_FLIGHT_BY_DATE = """
SELECT
    flights.ID,
    flights.ORIGIN_AIRPORT,
    flights.DESTINATION_AIRPORT,
    airlines.AIRLINE,
    flights.AIRLINE_DELAY AS DELAY

FROM
    flights
    JOIN airlines ON flights.AIRLINE = airlines.ID
WHERE
    flights.YEAR = :year
    AND flights.MONTH = :month
    AND flights.DAY = :day

"""

QUERY_DELAYED_FLIGHTS_BY_AIRLINE = """
SELECT
    flights.ID,
    flights.ORIGIN_AIRPORT,
    flights.DESTINATION_AIRPORT,
    airlines.AIRLINE,
    flights.AIRLINE_DELAY AS DELAY
FROM
    flights
    JOIN airlines ON flights.AIRLINE = airlines.ID
WHERE
    LOWER(airlines.AIRLINE) LIKE :search_airline AND
    CAST(DELAY AS INT) >0

ORDER BY airlines.AIRLINE, DELAY DESC
;
"""


class FlightData:
    """
    The FlightData class is a Data Access Layer (DAL) object that provides an
    interface to the flight data in the SQLITE database. When the object is
    created, the class forms connection to the sqlite database file, which
    remains active until the object is destroyed.
    """

    def __init__(self, db_uri):
        """
        Initialize a new engine using the given database URI
        """
        self._engine = create_engine(db_uri)

    def _execute_query(self, query, params):
        """
        Execute an SQL query with the params provided in a dictionary,
        and returns a list of records (dictionary-like objects).
        If an exception was raised, print the error, and return an empty list.
        """

        try:
            with self._engine.connect() as connection:
                result = connection.execute(text(query), params)
                return [row for row in result]
        except Exception as e:
            print(f"Error executing query: {e}")
            return []

    def get_flight_by_id(self, flight_id):
        """
        Searches for flight details using flight ID.
        If the flight was found, returns a list with a single record.
        """
        params = {"flight_id": flight_id}
        return self._execute_query(QUERY_FLIGHT_BY_ID, params)

    def get_flights_by_date(self, day, month, year):
        """
        Searches for flight details using date.
        If the flight was found, returns a list with a single record.
        """
        params = {"day": day, "month": month, "year": year}
        return self._execute_query(QUERY_FLIGHT_BY_DATE, params)

    def get_delayed_flights_by_airline(self, search_airline):
        """
        Searches for flight details using airline.
        If the flight was found, returns a list with a single record.
        """
        search_airline = search_airline.strip().lower()
        search_airline = "%" + search_airline + "%"
        params = {"search_airline": search_airline}
        print(params)
        return self._execute_query(QUERY_DELAYED_FLIGHTS_BY_AIRLINE, params)

    def __del__(self):
        """
        Closes the connection to the databse when the object is to be destroyed
        """
        self._engine.dispose()
