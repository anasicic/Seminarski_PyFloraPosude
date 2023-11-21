Aplikacija PyFlora Posude

Za ispravno funkcioniranje PyFlora Posude aplikacije, potrebno je instalirati sljedeće pakete pomoću pip. Ovi paketi omogućuju napredne funkcionalnosti u radu s slikama, analizi podataka te vizualizaciji i numeričkim operacijama:
- Pillow (PIL fork): Biblioteka za obradu slika. Instalirajte pomoću naredbe pip install Pillow
- pandas: Biblioteka za analizu i manipulaciju podacima. Instalirajte pomoću naredbe pip install pandas
- matplotlib: Biblioteka za vizualizaciju podataka. Instalirajte pomoću naredbe pip install matplotlib
- numpy: Biblioteka za numeričke operacije. Instalirajte pomoću naredbe pip install numpy

Svi ostali potrebni paketi i moduli, uključujući tkinter, random, sqlite3, datetime, os, i sys, već su dostupni unutar standardne biblioteke Pythona te ih nije potrebno dodatno instalirati

Za instalaciju potrebnih paketa, možete koristiti pip naredbe iz terminala ili naredbenog retka. Nakon instalacije, aplikaciju možete pokrenuti kako biste iskoristili sve funkcionalnosti

Baza podataka se sastoji od 4 tablice: Korisnik, Biljka, Posuda, Senzor
Posuda i senzori odnos 1: M (jedna posuda može imati više senzora) - razlog zašto su senzori u zasebnoj tablici
Posuda i biljka odnos 1: 1(posuda ne mora nužno imati biljku ili može imati samo jednu)
Aplikacija se sastoji od dva paketa: GUI i DATABASE
Aplikacija se pokreće iz gui.py
GUI i DATABASE su direktno povezani - dinamički
Moduli unutar paketa aplikacije su: gui.py i database.py
Zaseban modul za dohvat podatka trenutne temperature s meteo stranice je request.py
Vrijednosti korištene za senzore su random generirane (temperatura, vlažnost, pH) na temelju koji se pokreću određene aktivnosti u posudi. Vanjska trenutna temperatura dobivena preko request.py nije korištena jer su sve biljke kućne i vanjska temperatura ne predstavlja bitan element za aktivnosti njege biljke.
Postoji samo jedan korisnik-administrator u bazi podataka koji ima pristup aplikaciji - navedeno u zadatku


Sučelje za prijavu
1.   Nakon unosa korisničkog imena i lozinke, poziv select za unesene podatke (get_korisnik), logika u klasi database.py
2.   Ako za selektirani redak vrijedi da je username == odabrani_korisnik.username and lozinka == odabrani_korisnik.password (logika u gui.py), zatvara se prozor za prijavu i otvara prozor dobrodošlice


Sučelje dobrodošlice
1.   Nakon ispravno unesenih podataka, otvara se prozor dobrodošlice koji predstavlja korisnikov profil s kojeg može doći do liste posuda i liste biljki
2.1. Odabirom gumba lista posuda zatvara se prozor dobrodošlice i otvara se prozor s listom posuda, logika u gui.py (metoda prikazi_posude2)
2.2. Odabirom gumba lista biljki zatvara se prozor dobrodošlice i otvara se prozor s listom biljki, logika u gui.py (metoda prikazi_biljke2)


Sučelja za posude
1.   Na sučelju se nalazi gumb za unos nove posude, gumb očitaj senzore u posudama, gumb za otvaranje prozora s listom biljki, posude koje mogu imati biljku ili biti prazne (veza posuda i biljka 1:1), gumb line chart, gumb scatter plot i gumb histogram
2.   Posude se dohvaćaju preko poziva select (get_all_posude_sa_senzorima()), logika u klasi database.py
3.   Odabirom određene posude dolazi se do prozora koji daje detaljan prikaz određene posude 
4.   Gumb očitaj senzore preko insert operacije u klasi database-py generira random vrijednosti za temperaturu, vlaznost i pH, te se na osnovu definiranih minimalnih vrijednosti (gui.py) pokreću određene aktivnosti
4.   Prozor s detaljnim prikazom posude sadrži gumb Obriši, gumb Ažuriraj, gumb Isprazni posudu (logika u klasi database.py), gumb Natrag (logika u gui.py)
4.1. Ukoliko se želi ažurirati posuda (poziv update - update_posuda, poziv insert - insert_senzor, poziv select - get_posuda_sa_senzorima(id_posuda)i  logika u klasi database.py), prvo se treba isprazniti (update_posuda i delete_senzor), a zatim se dodaje nova biljka
4.2. Gumb natrag vraća aplikaciju na prikaz svih posuda
5.   Odabirom gumba za unos nove posude otvara se novi prozor koji predstavlja formu za unos podataka o posudi (logika u klasi database.py - metoda insert_posuda)
5.1. Ukoliko unos podataka zadovolji sve zadane provjere, podaci se uspješno spremaju i nova posuda je vidljiva na prozoru s listom posuda
5.2. Nakon spremanja unesenih podataka, otvara se prozor s listom posuda gdje se vidi i nova posuda
6.   Gumbi line chart, scatter plot i histogram dohvaćaju podatke preko poziva select (get_senzore_za_posudu(self, id_posuda)) - spajanje tablica za senzore i posudu. Podaci se selectiraju samo za posude koje sadrže biljku kroz određeno vrijeme mjerenja
7.   Gumb za ažuriranje vrijednosti radi na principu generiranja random vrijednosti prilikom svakog klika na gumb, logika u klasi database.py (metoda dodaj_novu_vrijednost_senzor())
8.   Gumb lista biljki vodi do prikaza svih biljki


Sučelja za biljke
1.   Na sučelju se nalazi gumb za unos nove biljke, gumb za otvaranje prozora s listom posuda, gumb moj profil i lista svih biljki
2.   Biljke se dohvaćaju preko poziva select (get_all_biljke()), logika u klasi database.py
3.   Odabirom gumba za unos nove biljke otvara se novi prozor koji predstavlja formu za unos podataka o posudi (logika u klasi database.py - metoda insert_data)
3.1. Ukoliko unos podataka zadovolji sve zadane provjere, podaci se uspješno spremaju i nova biljka je vidljiva na prozoru s listom biljki
4.   Odabirom određene posude dolazi se do prozora koji daje prikaz o njezi biljke (select poziv - get_biljka(id_biljka), logika u klasi database.py)
5.   U istom prozoru imamo mogućnost ažuriranja imena biljke (update_biljka - logika u klasi database.py)
5.1. Ukoliko je unos naziva biljke prošao provjere ispravnosti, biljka se sprema i vidljiva na prozoru s listom biljki
6.   Gumb obriši briše biljku (delete_biljka - logika u klasi database.py) i vraća aplikaciju na prozor s listom biljki
7.   Gumb natrag aplikaciju vraća na prethodni prozor s listom biljki
8.   Gumb posude aplikaciju vraća na prozor s listom posuda
9.   Gumb moj profil aplikaciju vraća na prozor dobrodošlice s listom biljki i listom posuda


