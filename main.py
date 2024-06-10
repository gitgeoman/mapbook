from tkinter import *

import requests
import tkintermapview
from bs4 import BeautifulSoup

# instrukcja sterująca

users = []


class User:
    def __init__(self, name, surname, posts, location):
        self.name = name
        self.surname = surname
        self.posts = posts
        self.location = location
        self.wspolrzedne = User.wspolrzedne(self)
        self.marker = map_widget.set_marker(self.wspolrzedne[0], self.wspolrzedne[1],
                                            text=f"{self.name}")

    def wspolrzedne(self) -> list:
        url: str = f'https://pl.wikipedia.org/wiki/{self.location}'
        response = requests.get(url)
        response_html = BeautifulSoup(response.text, 'html.parser')
        return [
            float(response_html.select('.latitude')[1].text.replace(",", ".")),
            float(response_html.select('.longitude')[1].text.replace(",", "."))
        ]


def lista_uzytknikow():
    listbox_lista_obiektow.delete(0, END)
    for idx, user in enumerate(users):
        listbox_lista_obiektow.insert(idx, f'{user.name} {user.surname} {user.posts} {user.location}')


def dodaj_uzytkownika():
    imie = entry_imie.get()
    nazwisko = entry_nazwisko.get()
    posty = entry_liczba_postow.get()
    lokalizacja = entry_lokalizacja.get()
    users.append(User(imie, nazwisko, posty, lokalizacja))

    lista_uzytknikow()

    entry_imie.delete(0, END)
    entry_nazwisko.delete(0, END)
    entry_liczba_postow.delete(0, END)
    entry_lokalizacja.delete(0, END)

    entry_imie.focus()


def usun_uzytkownika():
    i = listbox_lista_obiektow.index(ACTIVE)
    users[i].marker.delete()
    users.pop(i)
    lista_uzytknikow()


def pokaz_szczegoly_uzytkownika():
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


def edytuj_uzytkownika():
    i = listbox_lista_obiektow.index(ACTIVE)
    entry_imie.insert(0, users[i].name)
    entry_nazwisko.insert(0, users[i].surname)
    entry_liczba_postow.insert(0, users[i].posts)
    entry_lokalizacja.insert(0, users[i].location)

    button_dodaj_uzytkownika.config(text="Zapisz zmiany", command=lambda: aktualizuj_uzytkownika(i))


def aktualizuj_uzytkownika(i):
    users[i].name = entry_imie.get()
    users[i].surname = entry_nazwisko.get()
    users[i].posts = entry_liczba_postow.get()
    users[i].location = entry_lokalizacja.get()
    users[i].wspolrzedne = User.wspolrzedne(users[i])
    users[i].marker.delete()
    users[i].marker = map_widget.set_marker(users[i].wspolrzedne[0], users[i].wspolrzedne[1],
                                            text=f"{users[i].name}")
    lista_uzytknikow()
    button_dodaj_uzytkownika.config(text="Dodaj użytkownika", command=dodaj_uzytkownika)
    entry_imie.delete(0, END)
    entry_nazwisko.delete(0, END)
    entry_liczba_postow.delete(0, END)
    entry_lokalizacja.delete(0, END)
    entry_imie.focus()


# GUI
root = Tk()
root.title("MapBook")
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
button_pokaz_szczegoly = Button(ramka_lista_obiektow, text="Pokaż szczegóły", command=pokaz_szczegoly_uzytkownika)
button_usun_obiekkt = Button(ramka_lista_obiektow, text="Usuń obiekt", command=usun_uzytkownika)
button_edytuj_obiekt = Button(ramka_lista_obiektow, text="Edytuj obiekt", command=edytuj_uzytkownika)

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

button_dodaj_uzytkownika = Button(ramka_formularz, text="Dodaj użytkownika", command=dodaj_uzytkownika)
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

map_widget = tkintermapview.TkinterMapView(ramka_szczegoly_obiektu, width=900, height=400)
map_widget.set_position(52.2, 21.0)
map_widget.set_zoom(6)
map_widget.grid(row=2, column=0, columnspan=8)

root.mainloop()
