import csv, datetime, os, random

from sqlalchemy import case, func

from models import Base, Book, session, engine


RANDOM_SELECTION = [
    "Role the dice, hombre!",
    "Spin the wheel!",
    "Flip a coin!",
    "Einy, meiny, miny...book!",
    "Pick a book, any book!",
    "RNGesus, take the wheel!",
    "Let the fates decide!",
    "Play the literary lottery!",
    "Bump the bookcase and see what falls out."
]


def clear_screen():
    """Clear the screen for better readability"""
    os.system('cls' if os.name == 'nt' else 'clear')


def clean_date(date):
    """Convert date string into a date object"""
    try:
        if date == '':
            date = datetime.date(1970, 1, 1)
        else:
            date = datetime.datetime.strptime(date, '%m/%d/%Y').date()
    except ValueError:
        input(f"""
    ***** DATE ERROR *****

    You entered: {date}

    The date should be formatted MM/DD/YYYY.
    Press [Enter] to continue...
""")
    else:
        return date
    

def clean_num_of_pages(num_of_pages):
    """Convert number of pages into an integer"""
    try:
        num_of_pages = int(num_of_pages)
    except ValueError:
        input("""
    ***** NUMBER OF PAGES ERROR *****
    The number of pages should only include number characters.
              
    Press [Enter] to continue...
""")
    else:
        return num_of_pages
    

def check_unread(date):
    if date == datetime.date(1970, 1, 1):
        return "Not yet read"
    return date.strftime("%-m/%-d/%Y")


def number_of_books_in_library(books):
    return len(books)
    

def view_all_books():
    """View all books in the database"""
    clear_screen()
    while True:
        books = session.query(Book).order_by(Book.author).order_by(case(
        (Book.series.isnot(None), Book.series),
        else_=Book.title
    )).all()
        print("""
    ===== All Books =====
        
    ID   | Author — Title
""")
        for book in books:
            print("    " + str(book.id) +
                    (' ' * (7 - len(str(book.id)))) +
                    f"{book.author} — {book.series_title}")
        print(f"\n    Total number of books in the library: {number_of_books_in_library(books)}")
        choice = input("\n    Enter a book id to view more details or press "
                       "[Enter] to return to the main menu.\n\n    >>> ")
        if choice in [str(book.id) for book in books]:
            book = session.query(Book).filter(Book.id == choice).first()
            view_book(book)
        elif choice == '':
            clear_screen()
            break
        else:
            clear_screen()
            print("    That was an invalid entry. Please select a book id.")


def view_book(book):
    """View a single book"""
    clear_screen()
    while True:
        print(f"""
        ===== {book.title} =====

        Author: {book.author}
        Published: {book.published_year}
        Last Read: {check_unread(book.date_last_read)}
        Pages: {book.number_of_pages}
        Genre: {book.genre}

        [E]dit | [D]elete | [B]ack | [U]pdate 'Last Read'
""")
        choice = input("\n    >>> ")
        if choice.lower() == 'e':
            edit_book(book)
        elif choice.lower() == 'd':
            delete_book(book)
            break
        elif choice.lower() == 'b' or choice == '':
            clear_screen()
            break
        elif choice.lower() == 'u':
            book.date_last_read = datetime.date.today()
            session.add(book)
            session.commit()
            clear_screen()
            print(f"    The 'last read' date has been updated for {book.title}")
            break
        else:
            clear_screen()
            print("    That was an invalid entry. "
                  "Please select a menu option.")


def add_book():
    """Add a book to the database"""
    inputting_data = True
    while inputting_data:
        clear_screen()
        print("""
        ===== Add Book =====
""")
        series = input("    Series (Leave blank if not applicable): ")
        title = input("    Title: ")
        author = input("    Author: ")
        published_year = input("    Year Published (YYYY): ")
        date_needed = True
        while date_needed:
            date_last_read = input("    Date Last Read (MM/DD/YYYY): ")
            date_last_read = clean_date(date_last_read)
            if type(date_last_read) == datetime.date:
                date_needed = False
        number_of_pages_needed = True
        while number_of_pages_needed:
            number_of_pages = input("    Number of Pages: ")
            number_of_pages = clean_num_of_pages(number_of_pages)
            if type(number_of_pages) == int:
                number_of_pages_needed = False
        genre = input("    Genre: ")
        choice = input("\n    Is all the information correct? Y/n: ")
        if choice.lower() == 'n':
            choice = input("\n    Would you like to [s]tart over or "
                            "return to the [m]enu? S/m: ")
            if choice.lower() == 'm':
                clear_screen()
                return None
            else:
                continue
        else:
            new_book = Book(
                series=series,
                title=title,
                author=author,
                published_year=published_year,
                date_last_read=date_last_read,
                number_of_pages=number_of_pages,
                genre=genre
            )
            session.add(new_book)
            session.commit()
            clear_screen()
            print("    Book added!")
            break


def add_books_from_file():
    """Add books to the database from a file"""
    inputting_data = True
    while inputting_data:
        clear_screen()
        print("""
        ===== Add Books =====
              
    Make sure the csv file is in the same directory as this program,
    and make sure there is no header row.
              
    The csv columns should be in this order:
    Series, Title, Author, Year Published, Number of Pages, Genre
""")
        file_name = input("    Enter the file name (include .csv extention) or [C]ancel: ")
        if file_name.lower() == 'c':
            clear_screen()
            break
        try:
            with open(file_name, newline='') as csvfile:
                data = csv.reader(csvfile)
                for row in data:
                    # Check to see if the book is already in the database
                    book = session.query(Book).filter(Book.title == row[1]).first()
                    if book:
                        continue
                    else:
                        series = row[0]
                        title = row[1]
                        author = row[2]
                        published_year = int(row[3])
                        date_last_read = datetime.date(1970, 1, 1)
                        number_of_pages = clean_num_of_pages(row[4])
                        genre = row[5]
                        new_book = Book(
                            series=series,
                            title=title,
                            author=author,
                            published_year=published_year,
                            date_last_read=date_last_read,
                            number_of_pages=number_of_pages,
                            genre=genre
                        )
                        session.add(new_book)
                session.commit()
                clear_screen()
                print("    Books added!")
                break
        except FileNotFoundError:
            clear_screen()
            print("    That file does not exist. Please try again.")
            continue


def backup_library():
    """Backup the library to a csv file"""
    clear_screen()
    print("""
    ===== Backup Library =====
""")
    file_name = input("    Enter a file name (include .csv extention) or [C]ancel: ")
    if file_name.lower() == 'c':
        clear_screen()
        return None
    with open(file_name, 'w', newline='') as csvfile:
        data = csv.writer(csvfile)
        books = session.query(Book).order_by(Book.author).order_by(case(
        (Book.series.isnot(None), Book.series),
        else_=Book.title
    )).all()
        for book in books:
            data.writerow([
                book.series,
                book.title,
                book.author,
                book.published_year,
                book.number_of_pages,
                book.genre
            ])
    clear_screen()
    print("    Backup complete!")


def edit_book(book):
    """Edit a book in the database"""
    print("Leave the field blank if you do not want to change it.")
    series = input(f"Series ({book.series}): ")
    if series == '':
        series = book.series
    title = input(f"Title ({book.title}): ")
    if title == '':
        title = book.title
    author = input(f"Author ({book.author}): ")
    if author == '':
        author = book.author
    published_year = input(f"Year Published ({book.published_year}): ")
    if published_year == '':
        published_year = book.published_year
    else:
        published_year = int(published_year)
    date_needed = True
    while date_needed:
        date_last_read = input(f"Date Last Read ({check_unread(book.date_last_read)}): ")
        if date_last_read == '':
            date_last_read = book.date_last_read
            date_needed = False
        else:
            date_last_read = clean_date(date_last_read)
            if type(date_last_read) == datetime.date:
                date_needed = False
    number_of_pages_needed = True
    while number_of_pages_needed:
        number_of_pages = input(f"Number of Pages ({book.number_of_pages}): ")
        if number_of_pages == '':
            number_of_pages = book.number_of_pages
            number_of_pages_needed = False
        else:
            number_of_pages = clean_num_of_pages(number_of_pages)
            if type(number_of_pages) == int:
                number_of_pages_needed = False
    genre = input(f"Genre ({book.genre}): ")
    if genre == '':
        genre = book.genre
    choice = input("\n    Is all the information correct? Y/n: ")
    if choice.lower() == 'n':
        choice = input("\n    Would you like to [s]tart over or "
                        "return to the [m]enu? S/m: ")
        if choice.lower() == 'm':
            clear_screen()
            return None
        else:
            edit_book(book)
    else:
        book.series = series
        book.title = title
        book.author = author
        book.published_year = published_year
        book.date_last_read = date_last_read
        book.number_of_pages = number_of_pages
        book.genre = genre
        session.add(book)
        session.commit()
        clear_screen()
        print("    The book has been updated")


def delete_book(book):
    """Delete a book from the database"""
    choice = input(f"""
    Are you sure you want to delete {book.title} by {book.author}?
    Y/n: """)
    if choice.lower() == 'y':
        session.delete(book)
        session.commit()
        clear_screen()
        print("    The book has been deleted")
    else:
        clear_screen()
            

def display_random_book():
    """Display a random book from the database"""
    random_book = session.query(Book).order_by(func.random()).first()
    view_book(random_book)


def add_book_menu():
    """Choose whether to add a single book or read in books from a file"""
    clear_screen()
    while True:
        print("""
    ===== Add Book =====
              
    1) Add a single book
    2) Read in books from a file
              
    [M]ain Menu
""")
        choice = input("    >>> ")
        if choice == '1':
            add_book()
        elif choice == '2':
            add_books_from_file()
        elif choice.lower() == 'm' or choice == '':
            clear_screen()
            break
        else:
            clear_screen()
            print("    That was an invalid entry. "
                  "Please select a menu option.")

def main_menu():
    """Display the main menu"""
    clear_screen()
    while True:
        print(f"""
    ===== Book Archive =====
              
    1) View Library
    2) Add Book(s) to Library
    3) Backup Library
    4) {random.choice(RANDOM_SELECTION)}
              
    [E]xit
""")
        choice = input("    >>> ")
        if choice == '1':
            view_all_books()
        elif choice == '2':
            add_book_menu()
        elif choice == '3':
            backup_library()
        elif choice == '4':
            display_random_book()
        elif choice.lower() == 'e':
            clear_screen()
            print("The program session has ended.\n")
            break
        else:
            clear_screen()
            print("    That was an invalid entry. "
                  "Please select a menu option.")
        

def start_app():
    """Start the Book Archive application"""
    main_menu()
    

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    start_app()