import random
import sqlite3
import datetime
import os

# tablica korisnik

class DbRowKorisnik:
    def __init__(self, username, password, ime, prezime):
        self.password = password
        self.username = username
        self.ime = ime
        self.prezime = prezime

class KorisnikDatabase:
    def __init__(self, database_name):
        self.database_name = database_name
        self.table_name = "Korisnik"

    def create_table(self):

        query = f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
                        username TEXT UNIQUE,
                        password TEXT UNIQUE,
                        ime TEXT,
                        prezime TEXT
                        );
                    """

        try:
            connection = sqlite3.connect(self.database_name)
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except sqlite3.Error as e:
            print('Database error', e)
            return False
        finally:
            if connection:
                connection.close()


    def insert_korisnik(self, username, password, ime, prezime):

        query = f'INSERT INTO {self.table_name} (username, password, ime, prezime) VALUES (?, ?, ?, ?);'
        try:
            connection = sqlite3.connect(self.database_name)
            cursor = connection.cursor()
            cursor.execute(query, (username, password, ime, prezime))
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except sqlite3.Error as e:
            print('Database error', e)
            return False
        finally:
            if connection:
                connection.close()

    def get_korisnik(self, username):

        query = f'SELECT * FROM {self.table_name} WHERE username = ? ;'

        try:
            connection = sqlite3.connect(self.database_name)
            cursor = connection.cursor()
            cursor.execute(query, [username])
            record = cursor.fetchone()
            cursor.close()
            if record is not None:  # provjera je li stvarno postoji taj jedan korisnik s usernemom, ako ne postoji, nece se nista vratiti
                return DbRowKorisnik (record[0], record[1], record[2], record[3])
        except sqlite3.Error as e:
            print('Database error', e)
            return False
        finally:
            if connection:
                connection.close()


# senzori

class DbRowSenzor:
    def __init__(self, id_posuda, vrijeme_mjerenja, temperatura, vlaznost, pH, osvjetljenje ):

        self.id_posuda = id_posuda
        self.vrijeme_mjerenja = vrijeme_mjerenja
        self.temperatura = temperatura
        self.vlaznost = vlaznost
        self.pH = pH
        self.osvjetljenje = osvjetljenje


class SenzorDatabase:

    def __init__ (self, database_name):

        self.database_name = database_name
        self.table_name = 'Senzor'

    def create_table(self):

        query = f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
                        id_posuda INTEGER REFERENCES POSUDA (id_posuda),
                        vrijeme_mjerenja timestamp,
                        temperatura °C INTEGER DEFAULT (CAST(RANDOM() * 40 AS INTEGER)),
                        vlaznost '%' INTEGER DEFAULT (CAST(RANDOM() * 0.8 AS REAL)),
                        pH INTEGER DEFAULT (CAST(RANDOM() * 14 AS INTEGER)),
                        osvjetljenje lx INTEGER DEFAULT (CAST(RANDOM() * 300 AS INTEGER))
                        );

                        """
        try:
            connection = sqlite3.connect(self.database_name)
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except sqlite3.Error as e:
            print('Database error', e)
            return False
        finally:
            if connection:
                connection.close()

    def insert_senzor(self, id_posuda):
        temperatura = random.randint(0, 40)
        vlaznost = round(random.uniform(0, 0.8),2)
        pH = random.randint(0, 14)
        osvjetljenje = random.randint(0, 300)
        vrijeme_mjerenja = datetime.datetime.now()


        query = f'INSERT INTO {self.table_name} (id_posuda, vrijeme_mjerenja, temperatura, vlaznost, pH, osvjetljenje) VALUES (?, ?, ?, ?, ?, ?);'
        try:
            connection = sqlite3.connect(self.database_name)
            cursor = connection.cursor()
            cursor.execute(query, (id_posuda, vrijeme_mjerenja, temperatura, vlaznost, pH, osvjetljenje))
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except sqlite3.Error as e:
            print('Database error', e)
            return False
        finally:
            if connection:
                connection.close()

    def dodaj_novu_vrijednost_senzor(self):  #" gumb sync"
        query = f'INSERT INTO {self.table_name} (id_posuda, vrijeme_mjerenja, temperatura, vlaznost, pH, osvjetljenje) VALUES (?, ?, ?, ?, ?, ?);'

        try:
            connection = sqlite3.connect(self.database_name)
            cursor = connection.cursor()
            posudaDatabase = PosudaDatabase('PyFlora.db')
            posude = posudaDatabase.get_all_posude_sa_biljkom()    # ovdje dohvatimo sve posude
            for row_id in range(0, len(posude)):                   # itreriramo kroz svaku posudu kako bi u svokoj update-ali senzore da ne budu jednake vrijednosti
                vlaznost = round(random.uniform(0, 0.8),2)
                osvjetljenje = random.randint(0, 300)
                temperatura = random.randint(0, 40)
                pH = random.randint(0, 14)
                vrijeme_mjerenja = datetime.datetime.now()
                cursor.execute(query, (posude[row_id].id_posuda, vrijeme_mjerenja, temperatura, vlaznost, pH, osvjetljenje))
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except sqlite3.Error as e:
            print('Database error', e)
            return False
        finally:
            if connection:
                connection.close()

    def delete_senzor(self, id_posuda):    # za određenu posudu brišemo senzore, to se događa u trenutku brisanja biljke jer senzori više neće biti relevantni jer posuda više nema biljku

        query = f'DELETE FROM {self.table_name} WHERE id_posuda = ? ;'

        try:
            connection = sqlite3.connect(self.database_name)
            cursor = connection.cursor()
            cursor.execute(query, (id_posuda, ))
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except sqlite3.Error as e:
            print('Database error', e)
            return False
        finally:
            if connection:
                connection.close()

#kraj senzora

# tablica posuda

class DbRowPosuda:
    def __init__(self, id_posuda, id_biljka, naziv_posude, posadena_biljka):   
        self.id_posuda = id_posuda
        self.id_biljka = id_biljka
        self.naziv_posude = naziv_posude
        self.posadena_biljka = posadena_biljka

class DbRowPosudaSaSenzorima:
    def __init__(self, id_posuda, naziv_posude, id_biljka, temperatura, vlaznost, pH, naziv_biljke):    
        self.id_posuda = id_posuda
        self.naziv_posude = naziv_posude
        self.id_biljka = id_biljka
        self.temperatura = temperatura
        self.vlaznost = vlaznost
        self.pH = pH
        self.naziv_biljke = naziv_biljke

class DbRowPosudaSenzorValues:
    def __init__(self, vrijeme_mjerenja, temperatura, vlaznost, pH, id_biljka):   
        self.vrijeme_mjerenja = vrijeme_mjerenja
        self.temperatura = temperatura
        self.vlaznost = vlaznost
        self.pH = pH
        self.id_biljka = id_biljka

class PosudaDatabase:

    def __init__ (self, database_name):

        self.database_name = database_name
        self.table_name = 'Posuda'

    def create_table(self):

        query = f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
                        id_posuda INTEGER PRIMARY KEY,
                        id_biljka INTEGER REFERENCES BILJKA (id_biljka),
                        naziv_posude TEXT NOT NULL,
                        posadena_biljka boolean
                        );

                        """
        try:
            connection = sqlite3.connect(self.database_name)
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except sqlite3.Error as e:
            print('Database error', e)
            return False
        finally:
            if connection:
                connection.close()

    def insert_posuda(self, id_biljka, naziv_posude, posadena_biljka):
        query = f'INSERT INTO {self.table_name} (id_biljka, naziv_posude, posadena_biljka) VALUES (?, ?, ?);'
        query
        try:
            connection = sqlite3.connect(self.database_name)
            cursor = connection.cursor()
            cursor.execute(query, (id_biljka, naziv_posude, posadena_biljka))
            connection.commit()
            cursor.close()
            lastrowid = cursor.lastrowid #lastrowid je id od posude koju smo dodali unutar ove metode(znaci zadnja) i za nju moramo dodati i senzore
            senzori = SenzorDatabase('PyFlora.db')
            if(posadena_biljka):
                senzori.insert_senzor(lastrowid)
            connection.close()
            return True
        except sqlite3.Error as e:
            print('Database error', e)
            return False
        finally:
            if connection:
                connection.close()


    def update_posuda(self, id_biljka, id_posude):

        query = f'UPDATE {self.table_name} SET id_biljka = ? WHERE id_posuda = ? ;'  # kad se doda biljka u praznu posudu


        try:
            connection = sqlite3.connect(self.database_name)
            cursor = connection.cursor()
            cursor.execute(query, [id_biljka, id_posude])
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except sqlite3.Error as e:
            print('Database error', e)
            return False
        finally:
            if connection:
                connection.close()

    def get_posuda_sa_senzorima(self, id_posuda):      # metoda koja dohvaća sve podatke za neku posudu sa senzorima ali i posude koje nemaju senzore uopće (senzori će biti prazni)
        query = f'SELECT p.id_posuda, p.naziv_posude, p.id_biljka, s.temperatura, s.vlaznost, s.pH FROM Posuda p LEFT JOIN Senzor s ON p.id_posuda = s.id_posuda WHERE p.id_posuda = ? AND (s.id_posuda = ? OR s.id_posuda IS NULL)'
        try:
            connection = sqlite3.connect(self.database_name)
            cursor = connection.cursor()
            cursor.execute(query, (id_posuda, id_posuda,)) 
            record = cursor.fetchone()              
            cursor.close()
            if record is not None:
                return DbRowPosudaSaSenzorima(record[0], record[1], record[2], record[3], record[4], record[5], '')   # dohvat jedne posude - zato records, ''zanemaruje naziv biljke
        except sqlite3.Error as e:
            print('Database error', e)
            return False
        finally:
            if connection:
                connection.close()

    def get_all_posude_sa_biljkom(self):   #dohvaćaju se samo posude s biljkom pa ce se kasnije u metodi ažuriraj senzori ažurirati senzori od tih posuda

        rows = []
        query = f'SELECT * FROM {self.table_name} WHERE id_biljka is not null ORDER BY id_posuda ASC;'

        try:
            connection = sqlite3.connect(self.database_name)
            cursor = connection.cursor()
            cursor.execute(query)
            records = cursor.fetchall()
            for (id_posuda, id_biljka, naziv_posude, posadena_biljka) in records:              # možemo proizvoljno nazvati varijable
                rows.append(DbRowPosuda(id_posuda, id_biljka, naziv_posude, posadena_biljka))  # mapiranje objekta u DbRowPosuda
            cursor.close()
            return rows
        except sqlite3.Error as e:
            print('Database error', e)
            return False
        finally:
            if connection:
                connection.close()

    def get_senzore_za_posudu(self, id_posuda):  # za oređenu posudu vraćamo senzore kako bismo ih mogli prikazati grafički
        rows = []
        query = f'SELECT s.vrijeme_mjerenja, s.temperatura, s.vlaznost, s.pH, p.id_biljka FROM Posuda p,Senzor s WHERE p.id_posuda = s.id_posuda and p.id_posuda = ? and p.id_biljka is not null order by s.vrijeme_mjerenja'

        try:
            connection = sqlite3.connect(self.database_name)
            cursor = connection.cursor()
            cursor.execute(query, (id_posuda, ))
            records = cursor.fetchall()             
            for (vrijeme_mjerenja, temperatura, vlaznost, pH, id_biljka) in records:
                rows.append(DbRowPosudaSenzorValues(vrijeme_mjerenja, temperatura, vlaznost, pH, id_biljka))
            cursor.close()
            return rows
        except sqlite3.Error as e:
            print('Database error', e)
            return False
        finally:
            if connection:
                connection.close()

    def get_all_posude_sa_senzorima(self):    # dohvat svih posuda kako bismo ih mogli prikazati na gui-ju
        rows = []
        query = f'''
            SELECT p.id_posuda, p.naziv_posude, p.id_biljka, s.temperatura, s.vlaznost, s.pH, b.naziv
            FROM Posuda p
            LEFT JOIN Senzor s ON p.id_posuda = s.id_posuda
            LEFT JOIN Biljka b ON p.id_biljka = b.id_biljka
            WHERE (s.id_posuda IS NULL OR s.vrijeme_mjerenja = (SELECT MAX(vrijeme_mjerenja) FROM Senzor WHERE id_posuda = p.id_posuda))
            OR b.id_biljka IS NULL
            GROUP BY p.id_posuda, p.naziv_posude, p.id_biljka, s.temperatura, s.vlaznost, s.pH, b.naziv;
            '''

        try:
            connection = sqlite3.connect(self.database_name)
            cursor = connection.cursor()
            cursor.execute(query)
            records = cursor.fetchall()
            for (id_posuda, naziv_posude, id_biljka, temperatura, vlaznost, pH, naziv) in records:
                rows.append(DbRowPosudaSaSenzorima(id_posuda, naziv_posude, id_biljka, temperatura, vlaznost, pH, naziv))
            cursor.close()
            return rows
        except sqlite3.Error as e:
            print('Database error', e)
            return False
        finally:
            if connection:
                connection.close()

    def delete_posuda(self, id_posuda):

        query = f'DELETE FROM {self.table_name} WHERE id_posuda = ? ;'

        try:
            connection = sqlite3.connect(self.database_name)
            cursor = connection.cursor()
            cursor.execute(query, (id_posuda, ))
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except sqlite3.Error as e:
            print('Database error', e)
            return False
        finally:
            if connection:
                connection.close()

# biljke

class DbRowBiljka:
    def __init__(self, id_biljka, naziv, fotografija_path, zalijevanje, osvjetljenje, toplina, preporuke_supstrat): 
        self.id_biljka = id_biljka
        self.naziv = naziv
        self.fotografija_path = fotografija_path
        self.zalijevanje = zalijevanje
        self.osvjetljenje = osvjetljenje
        self.toplina = toplina
        self.preporuke_supstrat = preporuke_supstrat


class BiljkaDatabase:

    def __init__ (self, database_name):

        self.database_name = database_name
        self.table_name = 'Biljka'

    def create_table(self):

        query = f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
                        id_biljka INTEGER PRIMARY KEY,
                        naziv TXT,
                        fotografija path TXT,
                        zalijevanje TEXT,
                        osvjetljenje TEXT,
                        toplina REAL NOT NULL,
                        preporuka_supstrat BOOLEAN
                        );

                """
        try:
            connection = sqlite3.connect(self.database_name)
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except sqlite3.Error as e:
            print('Database error', e)
            return False
        finally:
            if connection:
                connection.close()


    def insert_data(self, naziv, fotografija, zalijevanje, osvjetljenje, toplina, preporuka_supstrat):

        query = f'INSERT INTO {self.table_name} (naziv, fotografija, zalijevanje, osvjetljenje, toplina, preporuka_supstrat) VALUES (?, ?, ?, ?, ?, ?);' 

        try:
            connection = sqlite3.connect(self.database_name)
            cursor = connection.cursor()
            cursor.execute(query, (naziv, fotografija, zalijevanje, osvjetljenje, toplina, preporuka_supstrat))
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except sqlite3.Error as e:
            print('Database error', e)
            return False
        finally:
            if connection:
                connection.close()



    def get_biljka(self, id_biljka):      # dohvaća sve podatke za neku biljku

        query = f'SELECT * FROM {self.table_name} WHERE id_biljka = ? ;'

        try:
            connection = sqlite3.connect(self.database_name)
            cursor = connection.cursor()
            cursor.execute(query, (id_biljka,))
            record = cursor.fetchone()
            cursor.close()
            if record is not None:
                return DbRowBiljka (record[0], record[1], record[2], record[3], record[4], record[5], record[6])
        except sqlite3.Error as e:
            print('Database error', e)
            return False
        finally:
            if connection:
                 connection.close()


    def get_all_biljke(self):

        rows = []
        query = f'SELECT * FROM {self.table_name} ORDER BY id_biljka ASC;'

        try:
            connection = sqlite3.connect(self.database_name)
            cursor = connection.cursor()
            cursor.execute(query)
            records = cursor.fetchall()             
            currentPath = os.getcwd() # dohvaća se trenutni path gdje je ovaj file, os.path.join(currentPath, fotografija_path) ce spojiti te vrijednosti u jedan path npr C:\\\\test + Biljke\\\\lavanda.jpg ce postati C:\\\\test\\\\Biljke\\\\lavanda.jpg
            for (id_biljka, naziv, fotografija_path, zalijevanje, osvjetljenje, toplina, preporuke_supstrat) in records:
                if(fotografija_path is not None):
                    rows.append(DbRowBiljka(id_biljka, naziv, os.path.join(currentPath, fotografija_path), zalijevanje, osvjetljenje, toplina, preporuke_supstrat))
                else:
                    rows.append(DbRowBiljka(id_biljka, naziv, None, zalijevanje, osvjetljenje, toplina, preporuke_supstrat)) #ako nema fotografije

            cursor.close()
            return rows
        except sqlite3.Error as e:
            print('Database error', e)
            return False
        finally:
            if connection:
                connection.close()


    def delete_biljka(self, id_biljka):

        query = f'DELETE FROM {self.table_name} WHERE id_biljka = ? ;'

        try:
            connection = sqlite3.connect(self.database_name)
            cursor = connection.cursor()
            cursor.execute(query, (id_biljka,))
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except sqlite3.Error as e:
            print('Database error', e)
            return False
        finally:
            if connection:
                connection.close()


    def update_biljka(self, id_biljka, naziv_biljke):

        query = f'UPDATE {self.table_name} SET naziv = ? WHERE id_biljka = ? ;'  # naziv biljke se ažurira

        try:
            connection = sqlite3.connect(self.database_name)
            cursor = connection.cursor()
            cursor.execute(query, [naziv_biljke, id_biljka])
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except sqlite3.Error as e:
            print('Database error', e)
            return False
        finally:
            if connection:
                connection.close()


def test():

    database1 = KorisnikDatabase('PyFlora.db')
    database2 = PosudaDatabase('PyFlora.db')
    database3 = BiljkaDatabase('PyFlora.db')             # apstrakcija baze podataka koju smo definirali
    database4 = SenzorDatabase('PyFlora.db')
    database1.create_table()
    database2.create_table()
    database3.create_table()
    database4.create_table()



    #database1.insert_korisnik('admin', '12345a', 'Ana', 'Sicic')




    #insert u tablicu Biljka
    # database3.insert_data('lavanda', 'Biljke\\\\lavanda.jpg', 'tjedno', 'jarko', 'toplije', True)
    # database3.insert_data('maticnjak', 'Biljke\\\\maticnjak.jpg', 'tjedno', 'umjereno', 'umjereno', True,)
    # database3.insert_data('timijan', 'Biljke\\\\timijan.jpg', 'mjesecno', 'jarko', 'toplije', False)
    # database3.insert_data('ruzmarin', 'Biljke\\\\ruzmarin.jpg', 'tjedno', 'jarko', 'toplije', False)
    # database3.insert_data('origano', 'Biljke\\\\origano.jpg', 'tjedno', 'sjenovito', 'toplije', False)
    # database3.insert_data('smilje', 'Biljke\\\\smilje.jpg', 'tjedno', 'jarko', 'toplije', True)
    # database3.insert_data('bosiljak', 'Biljke\\\\bosiljak.jpg', 'tjedno', 'jarko', 'toplije', True)
    # database3.insert_data('orhideja', 'Biljke\\\\orhideja.jpg', 'tjedno', 'umjereno', 'toplije', True)
    # database3.insert_data('hortenzija', 'Biljke\\\\hortenzija.jpg', 'dnevno', 'sjenovito', 'toplije', False)
    # database3.insert_data('sekulenti', 'Biljke\\\\sekulenti.jpg', 'dnevno', 'umjereno', 'umjereno', True)







    # insert u tablicu Posuda

    # database2.insert_posuda(1, 'Istria', True)
    # database2.insert_posuda(2, 'Dalmatia', True)
    # database2.insert_posuda(3, 'Ragusa', True)
    # database2.insert_posuda(4, 'Iadera', True)






if __name__ == '__main__':
    test()