import sqlite3
from datetime import datetime

# ================= DATABASE SETUP =================
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS books(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                author TEXT,
                qty INTEGER)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS members(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS transactions(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER,
                member_id INTEGER,
                issue_date TEXT,
                return_date TEXT)''')

# ================= FUNCTIONS =================
def add_book():
    title = input("Enter book title: ")
    author = input("Enter author name: ")
    qty = int(input("Enter quantity: "))
    cursor.execute("INSERT INTO books(title, author, qty) VALUES(?,?,?)", (title, author, qty))
    conn.commit()
    print("✅ Book added successfully!\n")

def view_books():
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    print("\n=== Books in Library ===")
    for b in books:
        print(b)
    print()

def add_member():
    name = input("Enter member name: ")
    email = input("Enter email: ")
    cursor.execute("INSERT INTO members(name, email) VALUES(?,?)", (name, email))
    conn.commit()
    print("✅ Member added successfully!\n")

def view_members():
    cursor.execute("SELECT * FROM members")
    members = cursor.fetchall()
    print("\n=== Members ===")
    for m in members:
        print(m)
    print()

def issue_book():
    book_id = int(input("Enter Book ID: "))
    member_id = int(input("Enter Member ID: "))
    
    # Check availability
    cursor.execute("SELECT qty FROM books WHERE id=?", (book_id,))
    result = cursor.fetchone()
    if result and result[0] > 0:
        issue_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO transactions(book_id, member_id, issue_date) VALUES(?,?,?)",
                       (book_id, member_id, issue_date))
        cursor.execute("UPDATE books SET qty = qty - 1 WHERE id=?", (book_id,))
        conn.commit()
        print("✅ Book issued successfully!\n")
    else:
        print("❌ Book not available!\n")

def return_book():
    trans_id = int(input("Enter Transaction ID: "))
    return_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute("SELECT book_id FROM transactions WHERE id=? AND return_date IS NULL", (trans_id,))
    result = cursor.fetchone()
    
    if result:
        book_id = result[0]
        cursor.execute("UPDATE transactions SET return_date=? WHERE id=?", (return_date, trans_id))
        cursor.execute("UPDATE books SET qty = qty + 1 WHERE id=?", (book_id,))
        conn.commit()
        print("✅ Book returned successfully!\n")
    else:
        print("❌ Invalid Transaction ID or Book already returned!\n")

def view_transactions():
    cursor.execute("SELECT * FROM transactions")
    trans = cursor.fetchall()
    print("\n=== Transactions ===")
    for t in trans:
        print(t)
    print()

# ================= MENU =================
def main():
    while True:
        print("===== Library Management System =====")
        print("1. Add Book")
        print("2. View Books")
        print("3. Add Member")
        print("4. View Members")
        print("5. Issue Book")
        print("6. Return Book")
        print("7. View Transactions")
        print("0. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_book()
        elif choice == "2":
            view_books()
        elif choice == "3":
            add_member()
        elif choice == "4":
            view_members()
        elif choice == "5":
            issue_book()
        elif choice == "6":
            return_book()
        elif choice == "7":
            view_transactions()
        elif choice == "0":
            print("Exiting... Goodbye!")
            break
        else:
            print("❌ Invalid choice, try again!\n")

if __name__ == "__main__":
    main()
    conn.close()

