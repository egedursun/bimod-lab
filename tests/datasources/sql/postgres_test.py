import psycopg2

HOST = 'bimod-pg-test-db-test-db-bimod.l.aivencloud.com'
PORT = 18497
DATABASE_NAME = 'defaultdb'
USER = 'avnadmin'
PASSWORD = 'AVNS_crE7vh1r_vpEW3aKVN6'


def create_test_tables_postgres():
    conn = psycopg2.connect(
        dbname=DATABASE_NAME,
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT
    )
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sales (
            id SERIAL PRIMARY KEY,
            date DATE NOT NULL,
            amount DECIMAL NOT NULL,
            price DECIMAL NOT NULL,
            buyer VARCHAR(255) NOT NULL
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS employees (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            surname VARCHAR(255) NOT NULL,
            department VARCHAR(255) NOT NULL,
            salary DECIMAL NOT NULL
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            price DECIMAL NOT NULL,
            stock INT NOT NULL
        )
        """
    )
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == '__main__':
    create_test_tables_postgres()
