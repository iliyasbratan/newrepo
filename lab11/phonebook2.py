import psycopg2
import csv

# === CONNECT TO DB ===
def connect():
    return psycopg2.connect(
        host="localhost",
        dbname="phonebook",
        user="postgres",
        password="12345678"  
    )


# === INSERT FROM CONSOLE ===
def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (name, phone))
    print("Added!")


# === INSERT FROM CSV ===
def insert_from_csv(path):
    with connect() as conn:
        with conn.cursor() as cur:
            with open(path, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (row[0], row[1]))
    print("CSV imported!")


# === UPDATE ===
def update_user(name, new_phone):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE phonebook SET phone = %s WHERE name = %s", (new_phone, name))
    print("Updated!")


# === QUERY ===
def query_all():
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM phonebook")
            for row in cur.fetchall():
                print(row)


def query_by_name(name):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM phonebook WHERE name = %s", (name,))
            print(cur.fetchall())


# === DELETE ===
def delete_user(name):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM phonebook WHERE name = %s", (name,))
    print("Deleted!")


# === SEARCH BY PATTERN ===
def search_by_pattern(pattern):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT name, phone FROM phonebook WHERE name ILIKE %s OR phone ILIKE %s", ('%' + pattern + '%', '%' + pattern + '%'))
            results = cur.fetchall()
            if results:
                for row in results:
                    print(row)
            else:
                print("No results found.")


# === DELETE BY NAME OR PHONE ===
def delete_by_name_or_phone(value):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL delete_by_name_or_phone(%s)", (value,))
    print("Deleted by name or phone!")


# === INSERT OR UPDATE USER ===
def insert_or_update_user():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL insert_or_update_user(%s, %s)", (name, phone))
    print("User inserted or updated!")


# === MAIN MENU ===
def menu():
    while True:
        print("\n1. Insert (console)")
        print("2. Insert (CSV)")
        print("3. Update user")
        print("4. View all")
        print("5. Search by name")
        print("6. Delete user")
        print("7. Search by pattern")
        print("8. Delete by name or phone")
        print("9. Insert or Update user")
        print("10. Exit")

        choice = input("Choose: ")

        if choice == '1':
            insert_from_console()
        elif choice == '2':
            insert_from_csv(input("Enter CSV path: "))
        elif choice == '3':
            update_user(input("Name to update: "), input("New phone: "))
        elif choice == '4':
            query_all()
        elif choice == '5':
            query_by_name(input("Name: "))
        elif choice == '6':
            delete_user(input("Name to delete: "))
        elif choice == '7':
            search_by_pattern(input("Enter search pattern: "))
        elif choice == '8':
            delete_by_name_or_phone(input("Enter name or phone to delete: "))
        elif choice == '9':
            insert_or_update_user()
        elif choice == '10':
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    menu()
