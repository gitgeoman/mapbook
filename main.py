from tkinter import *

import requests
import tkintermapview
from bs4 import BeautifulSoup

# instrukcja sterująca

users = []


class User:
    """
    Represents a user with a name, surname, number of posts, and location.

    Attributes:
        name (str): The user's first name.
        surname (str): The user's surname.
        posts (str): The number of posts published by the user.
        location (str): The user's location.
        coords (list): The geographical coordinates (latitude and longitude) of the user's location.
        marker (Marker): A marker on the map representing the user's location.
    """

    def __init__(self, name, surname, posts, location):
        self.name: str = name
        self.surname: str = surname
        self.posts: str = posts
        self.location: str = location
        self.coords: list = User.get_coordinates(self)

        self.marker = map_widget.set_marker(
            self.coords[0],
            self.coords[1],
            text=f"{self.name}"
        )

    def get_coordinates(self) -> list:
        """
        Retrieves the geographical coordinates for the user's location.

        Returns:
            list: A list containing the latitude and longitude of the user's location.
        """
        url: str = f'https://pl.wikipedia.org/wiki/{self.location}'
        response = requests.get(url)
        response_html = BeautifulSoup(response.text, 'html.parser')
        return [
            float(response_html.select('.latitude')[1].text.replace(",", ".")),
            float(response_html.select('.longitude')[1].text.replace(",", "."))
        ]


def show_users() -> None:
    """
    Displays the list of users in the Listbox widget.
    """
    listbox_lista_obiektow.delete(0, END)
    for idx, user in enumerate(users):
        listbox_lista_obiektow.insert(idx, f'{user.name} {user.surname} {user.posts} {user.location}')


def add_user() -> None:
    """
    Adds a new user to the users list based on input from Entry widgets.
    """
    name = entry_imie.get()
    surname = entry_nazwisko.get()
    posts = entry_liczba_postow.get()
    location = entry_lokalizacja.get()
    users.append(User(name, surname, posts, location))

    show_users()

    entry_imie.delete(0, END)
    entry_nazwisko.delete(0, END)
    entry_liczba_postow.delete(0, END)
    entry_lokalizacja.delete(0, END)

    entry_imie.focus()


def remove_user() -> None:
    """
    Removes the selected user from the users list and deletes their marker from the map.
    """
    i = listbox_lista_obiektow.index(ACTIVE)
    users[i].marker.delete()
    users.pop(i)
    show_users()


def show_user_details() -> None:
    """
    Displays the details of the selected user and sets the map position to their coordinates.
    """
    i = listbox_lista_obiektow.index(ACTIVE)
    imie = users[i].name
    label_imie_szczegoly_obiektu_wartosc.config(text=imie)
    nazwisko = users[i].surname
    label_nazwisko_szczegoly_obiektu_wartosc.config(text=nazwisko)
    posty = users[i].posts
    label_liczba_postow_szczegoly_obiektu_wartosc.config(text=posty)
    lokalizacja = users[i].location
    label_lokalizacja_szczegoly_obiektu_wartosc.config(text=lokalizacja)
    map_widget.set_position(users[i].wspolrzedne[0], users[i].wspolrzedne[1])
    map_widget.set_zoom(12)


def edit_user_data() -> None:
    """
    Updates the user data and marker on the map with the values from the Entry widgets.

    Args:
        i (int): The index of the user to be updated in the users list.
    """
    i = listbox_lista_obiektow.index(ACTIVE)
    entry_imie.insert(0, users[i].name)
    entry_nazwisko.insert(0, users[i].surname)
    entry_liczba_postow.insert(0, users[i].posts)
    entry_lokalizacja.insert(0, users[i].location)

    button_dodaj_uzytkownika.config(text="Zapisz zmiany", command=lambda: update_user(i))


def update_user(i) -> None:
    users[i].name = entry_imie.get()
    users[i].surname = entry_nazwisko.get()
    users[i].posts = entry_liczba_postow.get()
    users[i].location = entry_lokalizacja.get()
    users[i].wspolrzedne = User.get_coordinates(users[i])
    users[i].marker.delete()
    users[i].marker = map_widget.set_marker(users[i].wspolrzedne[0], users[i].wspolrzedne[1],
                                            text=f"{users[i].name}")
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
