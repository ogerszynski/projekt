import tkinter as tk
from tkinter import messagebox, ttk
import networkx as nx
import matplotlib.pyplot as plt

#interfejs graficzny
root = tk.Tk()
root.title("API - Znajdz najkrotsza sciezke do osoby z potrzebnym sprzetem")

#kto zna kogo
znajomosci = {
    'Kamil': ['Kamil', 'Magda', 'Piotr', 'Daniel'],
    'Magda': ['Kamil', 'Magda', 'Ewa', 'Liliana'],
    'Ewa': ['Magda', 'Ewa', 'Liliana', 'Daniel'],
    'Piotr': ['Kamil', 'Piotr'],
    'Nikodem': ['Nikodem', 'Mikolaj'],
    'Mikolaj': ['Nikodem', 'Mikolaj', 'Daniel'],
    'Liliana': ['Magda', 'Ewa', 'Liliana'],
    'Daniel': ['Kamil', 'Ewa', 'Mikolaj', 'Daniel']
}

#kto ma jaki sprzęt
sprzet = {
    'Kamil': {'kamera': None, 'statyw': None},
    'Magda': {'kamera': 'kamera', 'statyw': None},
    'Ewa': {'kamera': None, 'statyw': None},
    'Piotr': {'kamera': 'kamera', 'statyw': 'statyw'},
    'Nikodem': {'kamera': None, 'statyw': None},
    'Mikolaj': {'kamera': 'kamera', 'statyw': None},
    'Liliana': {'kamera': 'kamera', 'statyw': None},
    'Daniel': {'kamera': None, 'statyw': None}
}

#graf
graf_znajomosci = nx.DiGraph()
for osoba, znajomi in znajomosci.items():
    for znajomy in znajomi:
        graf_znajomosci.add_edge(osoba, znajomy)

#rysuj graf
def rysuj_graf():
    plt.figure(figsize=(10, 10))
    pos = nx.circular_layout(graf_znajomosci)
    nx.draw(graf_znajomosci, pos, with_labels=True, font_weight='bold', node_size=2500, node_color='skyblue', font_size=12, font_color='black', arrowsize=25, node_shape='o')
    plt.title("graf znajomosci - circular layout")
    plt.show()

#rysuj ścieżkę
def rysuj_graf_sciezki():
    osoba_poczatkowa = combobox_imie.get()
    selected_sprzet = combobox_sprzet.get()

    if osoba_poczatkowa and selected_sprzet:
        sprzet_poszukiwany = 'kamera' if selected_sprzet in ['kamera', 'kamera_i_statyw'] else 'statyw'

        sciezka = znajdz_najkrotsza_sciezke(osoba_poczatkowa, sprzet_poszukiwany)

        if sciezka:
            graf_sciezki = graf_znajomosci.subgraph(sciezka)
            plt.figure(figsize=(8, 8))
            pos = nx.circular_layout(graf_sciezki)
            nx.draw(graf_sciezki, pos, with_labels=True, font_weight='bold', node_size=1500, node_color='lightcoral', font_size=10, font_color='black', arrowsize=15, node_shape='o')
            plt.title(f"Graf ścieżki dostępu do {selected_sprzet} dla {osoba_poczatkowa}")
            plt.show()
        else:
            messagebox.showinfo("brak sciezki", f"Nie znaleziono sciezki do osoby z {selected_sprzet} dla {osoba_poczatkowa}")
    else:
        messagebox.showinfo("blad", "Prosze wybrac osobe i sprzet.")

#schemat blokowy
def rysuj_schemat():
    messagebox.showinfo("schemat blokowy", """
+-------------------------+              +-------------------------+
|        Rozpocznij       |              |        Rozpocznij       |
|  analizę posiadanych    |              |   analizę znajomości   |
|      przedmiotów        |              |        i sprzętu       |
|         i sprzętu       |              +------------+------------+
+-------------+-----------+                           |
              |                                       |
              v                                       |
+-------------+-------------+                         |
| Dla każdej osoby w grafie|                         |
|     Zapytaj o posiadany |                         |
|        sprzęt i          |                         |
|    znajomości           |                         |
+-------------+-----------+                         |
              |                                     |
              v                                     |
+-------------+-------------+              +--------+--------+
| Sprawdź dostępność do   |              | Sprawdź dostępność  |
| sprzętu u danej osoby    |              | do danej osoby w    |
|                         |              | grafie (znajomość) |
+-------------+-------------+              +--------+--------+
              |                                     |
              v                                     |
+-------------+-------------+              +--------+--------+
|  Jeśli dostępny sprzęt   |              |  Jeśli dostępna      |
|   to sprawdź, czy jest   |              |  znajomość, to        |
|    bezpośrednią osobą    |              |  sprawdź, czy jest    |
|  docelową lub czy jest   |              |  bezpośrednią osobą   |
|  osobą pośrednią z       |              |  docelową lub czy jest|
|  dostępnym sprzętem      |              |  osobą pośrednią z    |
|                         |              |  dostępnym sprzętem   |
+-------------------------+              +----------------------+
              |                                     |
              v                                     v
+-------------------------+              +----------------------+
| Znaleziono najkrótszą    |              | Znaleziono najkrótszą|
| ścieżkę do osoby z       |              | ścieżkę do osoby z   |
| dostępnym sprzętem       |              | dostępnym sprzętem    |
+-------------------------+              +----------------------+
""")

#funkcja - spraqdzenie znajomosci
def czy_sie_znaja(imie1, imie2):
    return imie2 in znajomosci[imie1]

#funkcja wymień znajomych
def znajdz_przyjaciol(imie):
    return [osoba for osoba in znajomosci[imie] if osoba != imie]

# funkcja szukania ścieżki
def znajdz_najkrotsza_sciezke(osoba_poczatkowa, sprzet_poszukiwany):
    osoby_z_sprzetem = [osoba for osoba, sprzet_osoby in sprzet.items() if sprzet_osoby[sprzet_poszukiwany] is not None]

    najkrotsza_sciezka = None
    najkrotsza_dlugosc = float('inf')

    for osoba_z_sprzetem in osoby_z_sprzetem:
        sciezka = nx.shortest_path(graf_znajomosci, source=osoba_poczatkowa, target=osoba_z_sprzetem)
        dlugosc_sciezki = len(sciezka)

        if dlugosc_sciezki < najkrotsza_dlugosc:
            najkrotsza_sciezka = sciezka
            najkrotsza_dlugosc = dlugosc_sciezki

    return najkrotsza_sciezka

# funkcje przycisków
def znajdz_najkrotsza_sciezke_btn():
    selected_imie = combobox_imie.get()
    selected_sprzet = combobox_sprzet.get()

    if selected_imie and selected_sprzet:
        osoba_poczatkowa = selected_imie

        if selected_sprzet == 'kamera':
            sprzet_poszukiwany = 'kamera'
        elif selected_sprzet == 'statyw':
            sprzet_poszukiwany = 'statyw'
        elif selected_sprzet == 'kamera_i_statyw':
            sprzet_poszukiwany = 'kamera'
        else:
            messagebox.showinfo("blad", "Nieprawidlowy sprzet.")
            return

        sciezka = znajdz_najkrotsza_sciezke(osoba_poczatkowa, sprzet_poszukiwany)

        if sciezka:
            messagebox.showinfo("najkrotsza sciezka", f"Najkrotsza sciezka do osoby z {selected_sprzet} dla {osoba_poczatkowa}: {', '.join(sciezka)}")
        else:
            messagebox.showinfo("brak sciezki", f"Nie znaleziono sciezki do osoby z {selected_sprzet} dla {osoba_poczatkowa}")
    else:
        messagebox.showinfo("blad", "Prosze wybrac osobe i sprzet.")

def sprawdz_znajomosc_btn():
    selected_imie1 = combobox_imie1.get()
    selected_imie2 = combobox_imie2.get()

    if selected_imie1 and selected_imie2:
        imie1 = selected_imie1
        imie2 = selected_imie2

        if czy_sie_znaja(imie1, imie2):
            messagebox.showinfo("wynik", f"{imie1} i {imie2} sie znaja!")
        else:
            messagebox.showinfo("wynik", f"{imie1} i {imie2} sie nie znaja.")
    else:
        messagebox.showinfo("blad", "Prosze wybrac dwie osoby.")

def znajdz_przyjaciol_btn():
    selected_imie = combobox_imie3.get()

    if selected_imie:
        imie = selected_imie
        przyjaciele = znajdz_przyjaciol(imie)
        messagebox.showinfo("przyjaciele", f"Przyjaciele {imie}: {', '.join(przyjaciele)}")
    else:
        messagebox.showinfo("blad", "Prosze wybrac osobe.")


#przyciski grafu i schematu
przycisk_rysuj_graf = tk.Button(root, text="GRAF", command=rysuj_graf)
przycisk_rysuj_graf.pack(pady=5)
przycisk_rysuj_schemat = tk.Button(root, text="SCHEMAT BLOKOWY", command=rysuj_schemat)
przycisk_rysuj_schemat.pack(pady=5)

#wybor imienia
label_imie1 = tk.Label(root, text="Imię 1.:")
label_imie1.pack()
combobox_imie1 = ttk.Combobox(root, values=list(znajomosci.keys()), state="readonly")
combobox_imie1.pack()

label_imie2 = tk.Label(root, text="Imię2. ")
label_imie2.pack()
combobox_imie2 = ttk.Combobox(root, values=list(znajomosci.keys()), state="readonly")
combobox_imie2.pack()

#sprawdz znajomych
przycisk_sprawdz_znajomosc = tk.Button(root, text="Czy się znają", command=sprawdz_znajomosc_btn)
przycisk_sprawdz_znajomosc.pack(pady=5)


label_imie3 = tk.Label(root, text="Imię:")
label_imie3.pack()
combobox_imie3 = ttk.Combobox(root, values=list(znajomosci.keys()), state="readonly")
combobox_imie3.pack()

przycisk_znajdz_przyjaciol = tk.Button(root, text="Pokaż znajomych", command=znajdz_przyjaciol_btn)
przycisk_znajdz_przyjaciol.pack(pady=5)

#wybor sciezki
label_imie = tk.Label(root, text="Imię:")
label_imie.pack()
combobox_imie = ttk.Combobox(root, values=list(znajomosci.keys()), state="readonly")
combobox_imie.pack()

#wybierz sprzet
label_sprzet = tk.Label(root, text="SPRZĘT:")
label_sprzet.pack()
combobox_sprzet = ttk.Combobox(root, values=['kamera', 'statyw', 'kamera_i_statyw'], state="readonly")
combobox_sprzet.pack()

#przycisk sciezki
przycisk_znajdz_najkrotsza_sciezke = tk.Button(root, text="ŚCIEŻKA", command=znajdz_najkrotsza_sciezke_btn)
przycisk_znajdz_najkrotsza_sciezke.pack(pady=5)

#przycisk grafu sciezki
przycisk_rysuj_graf_sciezki = tk.Button(root, text="GRAF ŚCIEŻKI", command=rysuj_graf_sciezki)
przycisk_rysuj_graf_sciezki.pack(pady=5)

root.mainloop()