import mysql.connector

HOST = 'bimod-mysql-test-db-test-db-bimod.l.aivencloud.com'
PORT = 18497
DATABASE_NAME = 'defaultdb'
USER = 'avnadmin'
PASSWORD = 'AVNS_oU1sPJb3A3A50CAq4aT'


def create_test_tables_mysql():
    conn = mysql.connector.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        database=DATABASE_NAME,
        port=PORT
    )
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS parties (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            date DATE NOT NULL,
            location VARCHAR(255) NOT NULL
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS invitees (
            id SERIAL PRIMARY KEY,
            party_id INT NOT NULL,
            name VARCHAR(255) NOT NULL,
            surname VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            phone VARCHAR(255) NOT NULL
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS gifts (
            id SERIAL PRIMARY KEY,
            party_id INT NOT NULL,
            name VARCHAR(255) NOT NULL,
            price DECIMAL NOT NULL,
            buyer VARCHAR(255) NOT NULL
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS animators (
            id SERIAL PRIMARY KEY,
            party_id INT NOT NULL,
            name VARCHAR(255) NOT NULL,
            surname VARCHAR(255) NOT NULL,
            phone VARCHAR(255) NOT NULL
        )
        """
    )

    conn.commit()
    cursor.close()
    conn.close()


def add_parties():
    conn = mysql.connector.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        database=DATABASE_NAME,
        port=PORT
    )
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO parties (name, date, location) VALUES ('Birthday Party', '2022-01-01', 'New York')
        """
    )
    cursor.execute(
        """
        INSERT INTO parties (name, date, location) VALUES ('Wedding Party', '2022-02-02', 'Los Angeles')
        """
    )
    cursor.execute(
        """
        INSERT INTO parties (name, date, location) VALUES ('Graduation Party', '2022-03-03', 'San Francisco')
        """
    )
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == '__main__':
    # create_test_tables_mysql()
    add_parties()

