import sqlite3
import pandas as pd

def create_tables():
    # Connect to SQLite database (creates the database if it doesn't exist)
    conn = sqlite3.connect('flights3.db')
    c = conn.cursor()
    
    # Create airlines table
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS airlines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            AIRLINES VARCHAR(100) UNIQUE,
            RATING REAL,
            PRICES REAL
        )
    ''')
    
    # Create airports table
    c.execute('''
        CREATE TABLE IF NOT EXISTS airports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) UNIQUE
        )
    ''')
    #Routes table
    c.execute('''
        CREATE TABLE IF NOT EXISTS flights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Source VARCHAR(100),
            Destination VARCHAR(100),
            Duration_Hour INTEGER,
            Duration_Minutes INTEGER,
            Total_Stops INTEGER
        )
    ''')

    c.execute('''
            CREATE TABLE IF NOT EXISTS airline_codes(
                
                IATA VARCHAR(6),
                AIRLINE VARCHAR(100),
                ICAO VARCHAR(6)
            )
        ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS airports2 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            IATA VARCHAR(100) UNIQUE,
            Airport VARCHAR(100)
        )
    ''')
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    
                
def insert_airline_2(data):
    
    conn = sqlite3.connect('flights3.db')
    
    c = conn.cursor()
    
    for index, row in data.iterrows():
        iata = row['IATA_Code']
        airline = row['Airline_Name']
        icao = row ['ICAO_Code']

        c.execute('''
                INSERT INTO airline_codes (IATA, AIRLINE, ICAO)
                VALUES(?, ?, ?)
                ''', (iata, airline, icao))
        
    conn.commit()
    c.close()
        
            
def load_csv_data(file_path):
    # Load data from a CSV file into a pandas DataFrame
    return pd.read_csv(file_path)


def insert_flights(data):
    conn = sqlite3.connect('flights3.db')
    c = conn.cursor()
    

    stop_mapping = {'direct': 0, '1 stop': 1, '2 stops': 2, '3 stops': 3}
    for index, row in data.iterrows():
        duration = row['Duration']
        total_stops_str = row['Total Stops']
        total_stops = stop_mapping.get(total_stops_str, None)
        if (len(duration.split())!=2):
            if 'h' in duration:
                duration += '0m'
            else:
                duration = '0h' + duration
                
        duration_hour = int(duration.split('h')[0])
        duration_minute = int(duration.split('m')[0].split()[-1])
        
        
        c.execute('''
                  INSERT INTO flights (Source, Destination, Duration_Hour, Duration_Minutes, Total_Stops)
                  VALUES (?, ?, ?, ?, ?)
                ''', (row['Sources'], row['Destinations'], duration_hour, duration_minute, total_stops))
    
    conn.commit()
    conn.close()
        
def insert_airlines(data):
    # Connect to the SQLite database
    conn = sqlite3.connect('flights3.db')
    c = conn.cursor()
    
    for index, row in data.iterrows():
        c.execute('''
    INSERT OR REPLACE INTO airlines (AIRLINES, RATING, PRICES)
    VALUES (?, ?, ?)
    ''', (row['Airlines'], row['Rating'], row['Prices']))
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def insert_airports(data):
    # Connect to the SQLite database
    conn = sqlite3.connect('flights3.db')
    c = conn.cursor()
    
    # Convert the DataFrame to a list of tuples
    airports = data['Airports'].tolist()
    
    airport_tuples = [(name,) for name in airports]
    
    # Insert data into the airports table
    c.executemany('''
        INSERT OR REPLACE INTO airports (name) VALUES (?)
    ''', airport_tuples)
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    

def query_data():
    # Connect to the SQLite database
    conn = sqlite3.connect('flights3.db')
    c = conn.cursor()
    
    # Query the airlines table
    c.execute('SELECT * FROM airlines')
    airlines = c.fetchall()
    print("Airlines:")
    for airline in airlines:
        print(airline)
    
    # Query the airports table
    c.execute('SELECT * FROM airports')
    airports = c.fetchall()
    print("\nAirports:")
    for airport in airports:
        print(airport)
    
    
    c.execute('SELECT * FROM flights')
    flights = c.fetchall()
    print("Flights: ")
    for flight in flights:
        print(flight)
    # Close the connection
    
    c.execute('SELECT * FROM airline_codes')
    airlines_codes = c.fetchall()
    print("Codes: ")
    
    for code in airlines_codes:
        print(code)
      
    c.execute('SELECT * FROM airports2')
    airports_new = c.fetchall()
    
    for airport in airports_new:
        print(airport)
    
    conn.close()
    
    
def drop_tables():
    # Connect to the SQLite database
    conn = sqlite3.connect('flights3.db')
    c = conn.cursor()
    
    # Drop existing tables if they exist
    c.execute('''
        DROP TABLE IF EXISTS airlines
    ''')
    c.execute('''
        DROP TABLE IF EXISTS airports
    ''')
    
    c.execute('''
        DROP TABLE IF EXISTS flights
    ''')
    
    c.execute('''
            DROP TABLE IF EXISTS airline_codes
        ''')
    
    c.execute('''
            DROP TABLE IF EXISTS airports2
        ''')
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    
    

def insert_new_airports(data):
    conn = sqlite3.connect('flights3.db')
    c = conn.cursor()
    
    for index, row in data.iterrows():
        c.execute('''
            INSERT INTO airports2 (IATA, Airport)
            VALUES (?, ?)
        ''', (row['Airports'], row['Airport_Name']))

    conn.commit()
    conn.close()

def query_airlines(airlines_data):
    conn = sqlite3.connect('flights3.db')
    c = conn.cursor()
    
    c.execute('SELECT * FROM airlines')
    airlines = c.fetchall()
    print("Airlines:")
    for airline in airlines:
        print(airline)
    
            
if __name__ == '__main__':
    
    airlines_data = load_csv_data('Average Prices.csv')
    airports_data = load_csv_data('Airports.csv')
    get_routes = load_csv_data('Flight_Correct_Production2.csv')
    airline_codes = load_csv_data('Airline_Codes.csv')
        
    var = int(input("Enter var: "))
    
    if (var==1):
        
        create_tables()
        
        insert_flights(get_routes)
        insert_airlines(airlines_data)
        insert_airports(airports_data)
        insert_airline_2(airline_codes)
        insert_new_airports(airports_data)
        
        query_data()
        
    elif (var == 2):
    
        query_data()  
        
        query_airlines(airlines_data)  
        
        
    elif (var == 0):
        drop_tables()
    
        
    
    
    
    