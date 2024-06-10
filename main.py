from tkinter import *
import requests
import tkintermapview
from bs4 import BeautifulSoup
import psycopg2 as ps

# Database connection parameters
db_params = ps.connect(
    database="postgres",
    user="postgres",
    password="postgres",
    host="localhost",
    port="65432"
)

users = []
markers = []  # List to keep track of markers


class User:
    """
      A class to represent a User.

      Attributes:
          id (int): The ID of the user.
          name (str): The first name of the user.
          surname (str): The surname of the user.
          posts (int): The number of posts the user has made.
          location (str): The location of the user.
          coords (list): The coordinates of the user's location.
          marker: The marker object for the user on the map.
      """

    def __init__(self, id, name, surname, posts, location, coords):
        """
              Constructs all the necessary attributes for the User object.

              Args:
                  id (int): The ID of the user.
                  name (str): The first name of the user.
                  surname (str): The surname of the user.
                  posts (int): The number of posts the user has made.
                  location (str): The location of the user.
                  coords (list): The coordinates of the user's location.
              """
        self.id = id
        self.name = name
        self.surname = surname
        self.posts = posts
        self.location = location
        self.coords = coords
        self.marker = map_widget.set_marker(
            float(self.coords[0]),
            float(self.coords[1]),
            text=f"{self.name}"
        )
        markers.append(self.marker)  # Track the marker


def get_coordinates(location) -> list:
    """
        Retrieves the coordinates of a given location from Wikipedia.

        Args:
            location (str): The name of the location.

        Returns:
            list: A list containing the latitude and longitude of the location.
        """
    url = f'https://pl.wikipedia.org/wiki/{location}'
    response = requests.get(url)
    response_html = BeautifulSoup(response.text, 'html.parser')
    return [
        float(response_html.select('.latitude')[1].text.replace(",", ".")),
        float(response_html.select('.longitude')[1].text.replace(",", "."))
    ]


def clear_markers() -> None:
    """
       Clears all markers from the map.
    """
    for marker in markers:
        marker.delete()
    markers.clear()


def show_users() -> None:
    """
        Fetches and displays all users from the database.
        Clears existing markers and user list before displaying new data.
    """
    cursor = db_params.cursor()
    sql_show_users = "SELECT id, name, surname, posts, location, ST_AsText(coords) FROM public.users"
    cursor.execute(sql_show_users)
    users_db = cursor.fetchall()
    cursor.close()

    clear_markers()  # Clear existing markers before adding new ones

    users.clear()
    listbox_lista_obiektow.delete(0, END)
    for idx, user in enumerate(users_db):
        user_obj = User(user[0], user[1], user[2], user[3], user[4],
                        [user[5][6:-1].split()[1], user[5][6:-1].split()[0]])
        users.append(user_obj)
        listbox_lista_obiektow.insert(idx, f'{user[1]} {user[2]} {user[3]} {user[4]}')


def add_user() -> None:
    """
        Adds a new user to the database and updates the UI.
    """
    name = entry_imie.get()
    surname = entry_nazwisko.get()
    posts = entry_liczba_postow.get()
    location = entry_lokalizacja.get()
    coords = get_coordinates(location)

    cursor = db_params.cursor()
    sql_insert_user = f"""
    INSERT INTO public.users (name, surname, posts, location, coords) 
    VALUES (%s, %s, %s, %s, ST_GeomFromText(%s))
    RETURNING id
    """
    cursor.execute(sql_insert_user, (name, surname, posts, location, f'POINT({coords[1]} {coords[0]})'))
    user_id = cursor.fetchone()[0]
    db_params.commit()
    cursor.close()

    user = User(id=user_id, name=name, surname=surname, posts=posts, location=location, coords=coords)
    users.append(user)

    show_users()

    entry_imie.delete(0, END)
    entry_nazwisko.delete(0, END)
    entry_liczba_postow.delete(0, END)
    entry_lokalizacja.delete(0, END)
    entry_imie.focus()


def remove_user() -> None:
    """
    Removes the selected user from the database and updates the UI.
    """
    i = listbox_lista_obiektow.index(ACTIVE)
    user = users[i]

    cursor = db_params.cursor()
    sql_delete_user = f"DELETE FROM public.users WHERE id = %s"
    cursor.execute(sql_delete_user, (user.id,))
    db_params.commit()
    cursor.close()

    user.marker.delete()
    markers.remove(user.marker)  # Remove the marker from the list
    users.pop(i)
    show_users()


def show_user_details() -> None:
    """
     Displays details of the selected user and centers the map on their location.
     """
    i = listbox_lista_obiektow.index(ACTIVE)
    user = users[i]
    label_imie_szczegoly_obiektu_wartosc.config(text=user.name)
    label_nazwisko_szczegoly_obiektu_wartosc.config(text=user.surname)
    label_liczba_postow_szczegoly_obiektu_wartosc.config(text=user.posts)
    label_lokalizacja_szczegoly_obiektu_wartosc.config(text=user.location)
    map_widget.set_position(float(user.coords[0]), float(user.coords[1]))
    map_widget.set_zoom(12)


def edit_user_data() -> None:
    """
    Populates the form with the selected user's data for editing.
    Changes the "Add User" button to "Save Changes".
    """
    i = listbox_lista_obiektow.index(ACTIVE)
    user = users[i]
    entry_imie.insert(0, user.name)
    entry_nazwisko.insert(0, user.surname)
    entry_liczba_postow.insert(0, user.posts)
    entry_lokalizacja.insert(0, user.location)

    button_dodaj_uzytkownika.config(text="Zapisz zmiany", command=lambda: update_user(i))


def update_user(i) -> None:
    """
    Updates the user's data in the database and updates the UI.
    """
    user = users[i]
    user.name = entry_imie.get()
    user.surname = entry_nazwisko.get()
    user.posts = entry_liczba_postow.get()
    user.location = entry_lokalizacja.get()
    user.coords = get_coordinates(entry_lokalizacja.get())
    user.marker.delete()
    markers.remove(user.marker)  # Remove the old marker from the list

    user.marker = map_widget.set_marker(user.coords[0], user.coords[1], text=f"{user.name}")
    markers.append(user.marker)  # Add the new marker to the list

    cursor = db_params.cursor()
    sql_update_user = f"""
    UPDATE public.users 
    SET name = %s, surname = %s, posts = %s, location = %s, coords = ST_GeomFromText(%s)
    WHERE id = %s
    """
    cursor.execute(sql_update_user, (
        user.name, user.surname, user.posts, user.location, f'POINT({user.coords[1]} {user.coords[0]})', user.id))
    db_params.commit()
    cursor.close()

    show_users()
    button_dodaj_uzytkownika.config(text="Dodaj użytkownika", command=add_user)
    entry_imie.delete(0, END)
    entry_nazwisko.delete(0, END)
    entry_liczba_postow.delete(0, END)
    entry_lokalizacja.delete(0, END)
    entry_imie.focus()


# GUI
root = Tk()
root.title("MapApp")
root.geometry("1024x760")

# ramki do porządkowania struktury
ramka_lista_obiektow = Frame(root)
ramka_formularz = Frame(root)
ramka_szczegoly_obiektu = Frame(root)

ramka_lista_obiektow.grid(column=0, row=0, padx=50)
ramka_formularz.grid(column=1, row=0)
ramka_szczegoly_obiektu.grid(column=0, row=1, columnspan=2, padx=50, pady=20)

# lista obiektów

label_lista_obiektow = Label(ramka_lista_obiektow, text="Lista obiektów: ")
listbox_lista_obiektow = Listbox(ramka_lista_obiektow, width=50)
button_pokaz_szczegoly = Button(ramka_lista_obiektow, text="Pokaż szczegóły", command=show_user_details)
button_usun_obiekkt = Button(ramka_lista_obiektow, text="Usuń obiekt", command=remove_user)
button_edytuj_obiekt = Button(ramka_lista_obiektow, text="Edytuj obiekt", command=edit_user_data)

label_lista_obiektow.grid(row=0, column=0, columnspan=3)
listbox_lista_obiektow.grid(row=1, column=0, columnspan=3)
button_pokaz_szczegoly.grid(row=2, column=0)
button_usun_obiekkt.grid(row=2, column=1)
button_edytuj_obiekt.grid(row=2, column=2)

# formularz

label_formularz = Label(ramka_formularz, text="Formularz: ")
label_imie = Label(ramka_formularz, text="Imię: ")
label_nazwisko = Label(ramka_formularz, text="Nazwisko: ")
label_liczba_postow = Label(ramka_formularz, text="Liczba postów: ")
label_lokalizacja = Label(ramka_formularz, text="Lokalizacja: ")

entry_imie = Entry(ramka_formularz)
entry_nazwisko = Entry(ramka_formularz)
entry_liczba_postow = Entry(ramka_formularz)
entry_lokalizacja = Entry(ramka_formularz)

label_formularz.grid(row=0, column=0, columnspan=2)
label_imie.grid(row=1, column=0, sticky=W)
label_nazwisko.grid(row=2, column=0, sticky=W)
label_liczba_postow.grid(row=3, column=0, sticky=W)
label_lokalizacja.grid(row=4, column=0, sticky=W)

entry_imie.grid(row=1, column=1)
entry_nazwisko.grid(row=2, column=1)
entry_liczba_postow.grid(row=3, column=1)
entry_lokalizacja.grid(row=4, column=1)

button_dodaj_uzytkownika = Button(ramka_formularz, text="Dodaj użytkownika", command=add_user)
button_dodaj_uzytkownika.grid(row=5, column=1, columnspan=2)

# szczegóły obiektu

label_szczegoly_obiektu = Label(ramka_szczegoly_obiektu, text="Szczegóły użytkownika:")
label_imie_szczegoly_obiektu = Label(ramka_szczegoly_obiektu, text="Imię: ")
label_nazwisko_szczegoly_obiektu = Label(ramka_szczegoly_obiektu, text="Nazwisko: ")
label_liczba_postow_szczegoly_obiektu = Label(ramka_szczegoly_obiektu, text="Liczba postów: ")
label_lokalizacja_szczegoly_obiektu = Label(ramka_szczegoly_obiektu, text="Lokalizacja: ")

label_imie_szczegoly_obiektu_wartosc = Label(ramka_szczegoly_obiektu, text="...", width=10)
label_nazwisko_szczegoly_obiektu_wartosc = Label(ramka_szczegoly_obiektu, text="...", width=10)
label_liczba_postow_szczegoly_obiektu_wartosc = Label(ramka_szczegoly_obiektu, text="...", width=10)
label_lokalizacja_szczegoly_obiektu_wartosc = Label(ramka_szczegoly_obiektu, text="...", width=10)

label_szczegoly_obiektu.grid(row=0, column=0, sticky=W)
label_imie_szczegoly_obiektu.grid(row=1, column=0, sticky=W)
label_imie_szczegoly_obiektu_wartosc.grid(row=1, column=1)
label_nazwisko_szczegoly_obiektu.grid(row=1, column=2)
label_nazwisko_szczegoly_obiektu_wartosc.grid(row=1, column=3)
label_liczba_postow_szczegoly_obiektu.grid(row=1, column=4)
label_liczba_postow_szczegoly_obiektu_wartosc.grid(row=1, column=5)
label_lokalizacja_szczegoly_obiektu.grid(row=1, column=6)
label_lokalizacja_szczegoly_obiektu_wartosc.grid(row=1, column=7)

# map widget
map_widget = tkintermapview.TkinterMapView(ramka_szczegoly_obiektu, width=900, height=400)
map_widget.set_position(52.2, 21.0)
map_widget.set_zoom(6)
map_widget.grid(row=2, column=0, columnspan=8)

root.mainloop()
