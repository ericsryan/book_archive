# Book Archive App

The **Book Archive App** is a command-line application designed to help you manage your book collection. You can add books, view your library, edit book details, delete books, and even choose random books from your collection.

## Table of Contents

1. [Book Archive App](#book-archive-app)
2. [Features](#features)
3. [How to Use](#how-to-use)
    - [View Library](#1-view-library)
    - [Add Book(s) to Library](#2-add-books-to-library)
    - [Edit Book Details](#3-edit-book-details)
    - [Delete Books](#4-delete-books)
    - [Backup Library](#5-backup-library)
    - [Random Book Selection](#6-random-book-selection)
    - [Exit](#7-exit)
4. [Instructions](#instructions)
5. [Running the App](#running-the-app)
6. [Requirements](#requirements)
7. [Author](#author)

## Features

- **View Library**: View a list of all books in your library.
- **Add Book(s) to Library**: Add books manually or read in books from a CSV file.
- **Edit Book Details**: Modify the details of any book in your collection.
- **Delete Books**: Remove books from your library.
- **Backup Library**: Create a backup of your entire library in a CSV file.
- **Random Book Selection**: Let the app randomly select a book from your collection for you to read.

## How to Use

1. **View Library (Option 1)**: View all books in your library. You can see book details and choose to edit or delete a specific book.

2. **Add Book(s) to Library (Option 2)**:
   - **Add a Single Book**: Manually input book details such as series, title, author, publication year, last read date, number of pages, and genre.
   - **Read in Books from a File**: Read books from a CSV file. Make sure the file follows the format: Series, Title, Author, Year Published, Number of Pages, Genre.

3. **Edit Book Details (Option 1, [E]dit in View Book Menu)**: Edit any detail of a book in your collection.

4. **Delete Books (Option 1, [D]elete in View Book Menu)**: Delete a book from your library.

5. **Backup Library (Option 3)**: Create a backup of your library in a CSV file.

6. **Random Book Selection (Option 4)**: Let the app randomly select a book from your collection for you to read.

7. **Exit (Option [E])**: Exit the application.

## Instructions

- **Editing Fields**: When editing book details, leave a field blank if you don't want to change it.

- **Date Format**: Dates should be in MM/DD/YYYY format.

- **Number of Pages**: Only enter numerical characters for the number of pages.

## Running the App

1. **Install Dependencies**: Make sure you have Python installed. You can install the required packages using `pip`:

   ```
   pip install sqlalchemy
   ```

2. **Clone the Repository**: Clone this repository to your local machine:

   ```
   git clone https://github.com/ericsryan/book_archive.git
   ```

3. **Navigate to the Project Directory**: Change your directory to the cloned project folder:

   ```
   cd book_archive
   ```

4. **Run the App**: Start the Book Archive App by running the `app.py` file:

   ```
   python app.py
   ```

## Requirements

- Python 3.x
- `sqlalchemy` library

## Author
   Eric S. Ryan
   eric@ericsryan.com

Feel free to reach out for any questions or improvements!