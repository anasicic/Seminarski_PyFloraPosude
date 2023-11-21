import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import Frame, Label, messagebox
from PIL import Image, ImageTk
import datetime
import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import datetime
import numpy as np

sys.path.append(os.getcwd())

from Database.database import KorisnikDatabase, BiljkaDatabase, PosudaDatabase, SenzorDatabase

# minimalne vrijednosti sa senzora potrebne za pokretanje aktivnosti

min_vlaznost = 0.5
min_temperatura = 10
min_ph = 3


root = tk.Tk()
root.resizable(False,False)
root.title('PyFloraPosuda')
root.geometry('700x700')

db_PyFlora = 'Baza\\PyFlora.db'
tb_korisnik = 'Korisnik'
tb_biljka = 'Biljka'
tb_posuda = 'Posuda'

welcome_window = tk.Toplevel(root)
welcome_window.resizable(False, False)
main_window = tk.Toplevel(welcome_window)
main_window.resizable(False, False)
PyBiljka_window = tk.Toplevel(main_window)
PyBiljka_window.resizable(False,False)
PyBiljka_detaljno_window = tk.Toplevel(main_window)
PyBiljka_detaljno_window.resizable(False,False)
framePosude = tk.Frame(main_window, width=900,height=600)
frameBiljke = tk.Frame(PyBiljka_window,width=900,height=600)


vrijeme_mjerenja = datetime.datetime.now()
posudaDatabase = PosudaDatabase('PyFlora.db')
senzorDatabase = SenzorDatabase('PyFlora.db')

# metoda za provjeru korisnika

def provjera_korisnika():
    username = userName.get()
    lozinka = password.get()
    korisnikDatabase = KorisnikDatabase('PyFlora.db')
    odabrani_korisnik = korisnikDatabase.get_korisnik(username)
    try:
        if username == odabrani_korisnik.username and lozinka == odabrani_korisnik.password: 
            root.withdraw()
            welcome.config(text = f'{odabrani_korisnik.ime}, dobrodosli na PyFlora! \n Ovdje možete vidjeti listu biljaka i posuda. \n')
            welcome_window.deiconify()
        else:
            error_label.config(text='Incorrect userame or password, try again')
    except:
        error_label.config(text='Incorrect userame or password, try again')

# metode za posude

def obrisi_posudu(id_posude):
    try:
        posudaDatabase.delete_posuda(id_posude)
        PyPosuda_window.withdraw()
        main_window.deiconify()
        prikazi_sve_posude()
    except:
        messagebox.showerror("Upozorenje","Došlo je do greške, pokušaje ponovno!")

def prikazi_sve_posude():
    for widget in framePosude.winfo_children():
       widget.destroy()
    
    # this will clear frame and frame will be empty
    # if you want to hide the empty panel then
    framePosude.pack_forget()
    framePosude.pack()

    posude = posudaDatabase.get_all_posude_sa_senzorima()
    entries2 = []
    x = 350
    y = 0
    for i in range(len(posude)):
        if(posude[i].id_biljka is not None and posude[i].temperatura is not None):
            poruka_za_supstrate = "\n";
            if(posude[i].temperatura < min_temperatura):
                poruka_za_supstrate += "Povisi temperaturu! \n";
            if(posude[i].pH < min_ph):
                poruka_za_supstrate += "Dodaj supstrat! \n";
            if(posude[i].vlaznost < min_vlaznost):
                poruka_za_supstrate += "Zalij biljku!";
            message = f'Posuda: {posude[i].naziv_posude} \n\nBiljka: {posude[i].naziv_biljke} \nTemperatura: {posude[i].temperatura} \nVlaznost: {posude[i].vlaznost} \npH: {posude[i].pH} \n {poruka_za_supstrate}'
        else:
            message = f'Posuda: {posude[i].naziv_posude} \nPosuda je prazna! \nMožete dodati novu biljku.'

        if((i+1)%3==0 and i != 0):
            y = y + 150
            x = 100
        text_box1 = tk.Text(framePosude, height=8, width=23, bd=3, highlightthickness=1, background='#B2D3C2')
        text_box1.place(x=x, y=y)
        text_box1.bind('<ButtonRelease-1>', lambda event, id_posude=posude[i].id_posuda: 
                                odaberi_posudu(id_posude))
        text_box1.insert('end', message)
        text_box1.config(state='disable')
        entries2.append(text_box1)
        x = x + 250

    message='''
        
    Dodaj novu
    PyPosudu
    '''
    text_box12 = tk.Text(main_window, height=8, width=23, bd=3,highlightthickness=1, background='#B2D3C2')
    text_box12.place(x=100, y=100)     # ovo je prvi textbox
    text_box12.bind('<ButtonRelease-1>', dodaj_novu_posudu)
    text_box12.insert('end', message)
    text_box12.config(state='normal')

entriesbiljke = []
images = []
labs = []


def azuriraj_senzore():
    senzorDatabase = SenzorDatabase('PyFlora.db')
    senzorDatabase.dodaj_novu_vrijednost_senzor()
    prikazi_sve_posude()


def ukloni():
    root.destroy()


def odaberi_posudu(id_posuda):
    posuda = posudaDatabase.get_posuda_sa_senzorima(id_posuda)
    naziv_PyPosude_label.config(text = f' Posuda: {posuda.naziv_posude}')
    if(posuda.id_biljka is not None):
        senzor_1_label.config(text = f' Temperatura: {posuda.temperatura}°C')
        senzor_2_label.config(text = f' Vlaznost: {posuda.vlaznost}%')
        senzor_3_label.config(text = f' pH: {posuda.pH}')
    else:
        senzor_1_label.config(text = f'')
        senzor_2_label.config(text = f'')
        senzor_3_label.config(text = f'')
    obrisiPosudu.bind('<ButtonRelease-1>', lambda event, id_posude=id_posuda: 
                                obrisi_posudu(id_posude))
        # obrisiPosudu.bind('<ButtonRelease-1>', lambda event: 
    #                             obrisi_posudu(id_posuda))
    azuriraj_posudu_buttton.bind('<ButtonRelease-1>', lambda event, id_posude=id_posuda: 
                                azuriraj_posudu(id_posude))
    isprazni_posudu_button.bind('<ButtonRelease-1>', lambda event, id_posude=id_posuda: 
                                isprazni_posudu(id_posude))
    button_line_chart.bind('<ButtonRelease-1>', lambda event, id_posude=id_posuda: 
                                create_line_chart_senzor_values(id_posude))
    button_scatter_plot.bind('<ButtonRelease-1>', lambda event, id_posude=id_posuda: 
                                create_scatter_senzor_values(id_posude))
    button_histogram.bind('<ButtonRelease-1>', lambda event, id_posude=id_posuda: 
                                create_histogram_senzor_values(id_posude))
    if(posuda.id_biljka is not None):
        posadenaBiljka = biljkaDatabase.get_biljka(posuda.id_biljka)
        comboboxPromijeniBiljku.set(posadenaBiljka.naziv) # ako postoji posadena biljke, prikazat ce se u comboboxu
    main_window.withdraw()
    PyPosuda_window.deiconify()

def azuriraj_posudu(id_posuda):  # kad se praznoj posudi doda biljka, onda se biljci doda početni senzor
    if(nazivi_biljka_sa_pripadajucim_id[PromijenjenaBiljka] == -1):
         messagebox.showerror("Upozorenje","Morate odabrati biljku prije azuriranja senzora!")
    else:
        posuda = posudaDatabase.get_posuda_sa_senzorima(id_posuda)
        if(posuda.id_biljka is None):
            posudaDatabase.update_posuda(nazivi_biljka_sa_pripadajucim_id[PromijenjenaBiljka], posuda.id_posuda)
            senzorDatabase.insert_senzor(id_posuda)
            azuriranaposuda = posudaDatabase.get_posuda_sa_senzorima(id_posuda)
            senzor_1_label.config(text = f' Temperatura: {azuriranaposuda.temperatura}°C')
            senzor_2_label.config(text = f' Vlaznost: {azuriranaposuda.vlaznost}')
            senzor_3_label.config(text = f' pH: {azuriranaposuda.pH}')
        else:
            messagebox.showerror("Upozorenje","Morate isprazniti posudu kako biste posadili novu biljku!")

def isprazni_posudu(id_posuda):
    posudaDatabase.update_posuda(None, id_posuda)  # id biljke ce u bazi biti set-an u null jer je biljka za ovu posudu izbrisana
    senzorDatabase.delete_senzor(id_posuda)        # posto posuda vise nema biljku, brisemo i njene senzore
    comboboxPromijeniBiljku.set('')                # postavljamo ga praznim jer posuda više nema biljku, kao i vrijednosti senzora (niže linije)
    senzor_1_label.config(text = f'')
    senzor_2_label.config(text = f'')
    senzor_3_label.config(text = f'')

def dodaj_novu_posudu(event):
    main_window.withdraw()
    UnosPosuda_window.deiconify()

def s_posude_na_profil(event):
    UnosPosuda_window.withdraw()
    welcome_window.deiconify()

def prikazi_posude(event):
    PyBiljka_window.withdraw()
    main_window.deiconify()

def prikazi_posude2(event):
    welcome_window.withdraw()
    main_window.deiconify()
   

def dodaj_posudu(event):
    
        id = None    
        if(nazivi_biljka_sa_pripadajucim_id[odabrana_biljka_za_novu_posudu] != -1):  # ako posuda nema biljku, naziv biljke je prazan te smo u dict postavili defaolutno value -1 ako je "" 
            id = nazivi_biljka_sa_pripadajucim_id[odabrana_biljka_za_novu_posudu]
        naziv_posude = posuda_entry.get()
        posadena_biljka_check = biljka_posadena_u_posudi.get()
        if (posadena_biljka_check and biljke_za_novu_posudu_combobox.get() == ''):
            messagebox.showerror("Upozorenje", "Odaberite biljku ili označite posudu kao praznu!")
        elif(not posuda_entry.get().strip()):
            messagebox.showerror("Upozorenje","Ime posude ne može biti prazno!")
        else:
            posudaDatabase.insert_posuda(id, naziv_posude, posadena_biljka_check)
            posuda_entry.delete(0, 'end')
            check_button.deselect()
            biljke_za_novu_posudu_combobox['values'] = []
            biljke_za_novu_posudu_combobox.set('')
            posadena_biljka.delete(0, 'end')
            UnosPosuda_window.withdraw()
            main_window.deiconify()
        prikazi_sve_posude()
       
def profil(event):
    PyPosuda_window.withdraw()
    welcome_window.deiconify()

def idi_na_biljke(event):
    main_window.withdraw()
    PyBiljka_window.deiconify()

def korak_natrag(event):
    PyPosuda_window.withdraw()
    main_window.deiconify()
    prikazi_sve_posude()

def create_histogram_senzor_values(id_posuda):    # histogram

    senzori = posudaDatabase.get_senzore_za_posudu(id_posuda)
    brojSenzora = len(senzori)

    if(brojSenzora is None or brojSenzora == 0):
        messagebox.showerror("Upozorenje", "Posuda nema biljku te nismo u mogucnosti napraviti graficki prikaz!")

    
    else: 
        temperatura = np.array([senzori[i].temperatura for i in range(brojSenzora)])
        num_bins = 3
        n, bins, patches = plt.hist(temperatura, num_bins, facecolor='blue', alpha=1)
        plt.locator_params(axis='y', integer=True)
        plt.show()                                    

def create_line_chart_senzor_values(id_posuda):   # line chart graf

    senzori = posudaDatabase.get_senzore_za_posudu(id_posuda)
    brojSenzora = len(senzori)

    if(brojSenzora is None or brojSenzora == 0):
        messagebox.showerror("Upozorenje", "Posuda nema biljku te nismo u mogucnosti napraviti graficki prikaz!")
    else: 
        dataframetemp = pd.DataFrame({'vrijeme': np.array([senzori[i].vrijeme_mjerenja
                                                                for i in range(brojSenzora)]),
                            'temperatura': np.array([senzori[i].temperatura
                                                for i in range(brojSenzora)])})
        
        dataframevlaznost = pd.DataFrame({'vrijeme': np.array([senzori[i].vrijeme_mjerenja
                                                                for i in range(brojSenzora)]),
                            'vlaznost': np.array([senzori[i].vlaznost
                                                for i in range(brojSenzora)])})
        dataframeph = pd.DataFrame({'vrijeme': np.array([senzori[i].vrijeme_mjerenja
                                                                for i in range(brojSenzora)]),
                            'pH': np.array([senzori[i].pH
                                                for i in range(brojSenzora)])})
                                                
        # Plotting the time series of given dataframe
        firstPlot = dataframetemp.plot(x = "vrijeme")
        dataframevlaznost.plot(x = "vrijeme", ax = firstPlot)
        dataframeph.plot(x = "vrijeme", ax = firstPlot)

        
        # Giving title to the chart using plt.title
        plt.title('Vrijednosti senzora po datumu')
        
        # rotating the x-axis tick labels at 30degree
        # towards right
        plt.xticks(rotation=30, ha='right')
        
        # Providing x and y label to the chart
        plt.xlabel('datum')
        plt.ylabel('senzor')
        plt.show()


def create_scatter_senzor_values(id_posuda):

    senzori = posudaDatabase.get_senzore_za_posudu(id_posuda)
    brojSenzora = len(senzori)

    if(brojSenzora is None or brojSenzora == 0):
        messagebox.showerror("Upozorenje", "Posuda nema biljku te nismo u mogucnosti napraviti graficki prikaz!")
    else: 
        vrijeme_mjerenja = np.array([senzori[i].vrijeme_mjerenja for i in range(brojSenzora)])
        temperatura = np.array([senzori[i].temperatura for i in range(brojSenzora)])
        vlaznost = np.array([senzori[i].vlaznost for i in range(brojSenzora)])
        pH = np.array([senzori[i].pH for i in range(brojSenzora)])

        plt.scatter(vrijeme_mjerenja, temperatura)
        plt.scatter(vrijeme_mjerenja, vlaznost)
        plt.scatter(vrijeme_mjerenja, pH)

                                                
        # Plotting the time series of given dataframe
        # firstPlot = dataframetemp.plot(x = "vrijeme")
        # dataframevlaznost.plot(x = "vrijeme", ax = firstPlot)
        # dataframeph.plot(x = "vrijeme", ax = firstPlot)

        
        # Giving title to the chart using plt.title
        plt.title('Vrijednosti senzora po datumu')
        
        # rotating the x-axis tick labels at 30degree
        # towards right
        plt.xticks(rotation=30, ha='right')
        
        # Providing x and y label to the chart
        plt.xlabel('datum')
        plt.ylabel('senzor')
        plt.show()


# metode za biljke

def dodaj_biljku_window(event):
    PyBiljka_window.withdraw()
    UnosBiljka_window.deiconify()

def prikazi_sve_biljke():
    images.clear()   # svaki put kad idemo u bazu po nove biljke, brisemo trenutne slike jer cemo to popuniti sa dohvaćenim novim vrijednostima iz baze
    labs.clear()
    biljkeDatabase = BiljkaDatabase('PyFlora.db')
    biljke = biljkeDatabase.get_all_biljke()
    for widget in frameBiljke.winfo_children(): #cistimo trenutni frame jer cemo ga ispuniti novim vrijesnostima
        widget.destroy()
    frameBiljke.pack_forget()
    frameBiljke.pack()

    x = 350
    y = 0
    for i in range(len(biljke)):
        message = f'{biljke[i].naziv} \n Zalijevanje: {biljke[i].zalijevanje} \n Osvjetljenje: {biljke[i].osvjetljenje} \n Toplina: {biljke[i].toplina}'
        if((i+1)%3==0 and i != 0):
            y = y + 150
            x = 100
        frame1 = tk.Frame(frameBiljke, height=8, width=23, bd=3, highlightthickness=1)
        frame1.place(x=x, y=y)
        if(biljke[i].fotografija_path is not None):
            images.append(ImageTk.PhotoImage(Image.open(biljke[i].fotografija_path)))
        else:
            images.append(None)
        lab = Label(frame1, text=message)
        lab.grid()
        lab["compound"] = tk.LEFT
        lab["image"] = images[i]
        labs.append(lab)
        lab.bind('<ButtonRelease-1>', lambda event, id_biljke=biljke[i].id_biljka: 
                                    odaberi_biljku(id_biljke))
        lab.pack()
        frame1.bind('<ButtonRelease-1>', lambda event, id_biljke=biljke[i].id_biljka: 
                                    odaberi_biljku(id_biljke))
        entriesbiljke.append(frame1)
        x = x + 250
    message='''  
 Dodaj novu
 biljku
    '''
    text_box11 = tk.Text(PyBiljka_window, height=5, width=13, bd=3,highlightthickness=1)
    text_box11.place(x=100, y=100)
    text_box11.bind('<ButtonRelease-1>', dodaj_biljku_window)
    text_box11.insert('end', message)
    text_box11.config(state='normal')

def obrisi_biljku(id_biljke):
    biljkaDatabase.delete_biljka(id_biljke)
    PyBiljka_detaljno_window.withdraw()
    PyBiljka_window.deiconify()
    prikazi_sve_biljke()

def dodaj_biljku(event):
    global filename
    naziv_biljke =naziv_biljke_entry.get()
    if (not naziv_biljke_entry.get().strip()):
        messagebox.showerror("Upozorenje","Ime biljke ne moze biti prazno!")
    elif (comboboxS.get()== ''):
        messagebox.showerror("Upozorenje", "Niste odabrali razinu osvjetljenja")
    elif (comboboxT.get()== ''):
        messagebox.showerror("Upozorenje", "Niste odabrali razinu topline ")
    elif (comboboxZ.get()== ''):
        messagebox.showerror("Upozorenje", "Niste odabrali vrstu zalijevanja")
    elif (not filename.strip()):
        messagebox.showerror("Upozorenje", "Niste odabrali fotografiju")

    else:
        biljkeFilePath = f"Biljke\\\\{filename}"
        biljkaDatabase.insert_data(naziv_biljke, biljkeFilePath, selected_zalijevanje, selected_osjetljenje, selected_toplina, check_supstrat.get())
        filename = ''  
        naziv_biljke_entry.delete(0, 'end')
        comboboxZ.set('')
        comboboxS.set('')
        comboboxT.set('')
        supstrat_checkbutton.deselect()
        supstrat.delete(0)
        UnosBiljka_window.withdraw()
        PyBiljka_window.deiconify()
        prikazi_sve_biljke()

def prikazi_biljku(event):
    PyPosuda_window.withdraw()
    PyBiljka_window.deiconify()


def prikazi_biljke2(event):
    welcome_window.withdraw()
    PyBiljka_window.deiconify()

def moj_profil(event):
    PyBiljka_detaljno_window.withdraw()
    welcome_window.deiconify()

def odaberi_biljku(id_biljka):
    biljka = biljkaDatabase.get_biljka(id_biljka)
    naziv_biljke_label.config(text = f' Naziv biljke: {biljka.naziv}')
    zalijevanje_biljke.config(text = f' Zalijevanje biljke: {biljka.zalijevanje}')
    osvjetljenje_biljke.config(text = f' Osvjetljenje biljke: {biljka.osvjetljenje}')
    razina_topline.config(text = f' Razina topline {biljka.toplina}')
    obrisi_biljku_button.bind('<ButtonRelease-1>', lambda event, id_biljke=id_biljka: 
                                obrisi_biljku(id_biljke))
    azuriraj_biljku_button.bind('<ButtonRelease-1>', lambda event, id_biljke=id_biljka: 
                                 azuriraj_biljku(id_biljke))
    PyBiljka_window.withdraw()
    PyBiljka_detaljno_window.deiconify()

def azuriraj_biljku(id_biljka):
    if(not biljka_naziv.get().strip()):
        messagebox.showerror("Upozorenje","Ime biljke ne moze biti prazno!")
    else:
        biljkaDatabase.update_biljka(id_biljka, biljka_naziv.get())
        naziv_biljke_label.config(text = f' Naziv biljke: {biljka_naziv.get()}')
        biljka_naziv.delete(0, 'end')
        prikazi_sve_biljke()

def s_biljke_na_profil(event):
    UnosBiljka_window.withdraw()
    welcome_window.deiconify()

def natrag(event):
    PyBiljka_detaljno_window.withdraw()
    PyBiljka_window.deiconify()

filename = ''   # provjeri hoce li raditi bez ovoga
def odaberi_fotografiju():
    global filename
    filepath = tk.filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    filename = os.path.basename(filepath)

# sučelje za prijavu

label = tk.Label(root, text='Prijava', font='Arial 20')
label.pack(ipady=50)
userName_label = tk.Label(root, text='User Name', font='Arial 12', bg='white')
userName_label.pack()
userName = tk.Entry(root, width=20, bd=2, highlightthickness=1)
userName.pack(pady=2)
password_label = tk.Label(root, text='Password', font='Arial 12', bg='white')
password_label.pack()
password = tk.Entry(root, bd=2, show='*', highlightthickness=1)
password.pack(pady=2)
button = tk.Button(root, text='Prijavi me', font='Arial 10', bd=2, width=17, command=provjera_korisnika)
button.pack(pady=5)
error_label = tk.Label(root, fg="red", font='Arial 12', bg='white')
error_label.pack()

# sučelje za dobrodošlicu

welcome_window.title('PyPosude')
welcome_window.geometry('900x700')
welcome_window.protocol('WM_DELETE_WINDOW', ukloni)
welcome_window.withdraw()

welcome = tk.Label (welcome_window, width= 50,highlightthickness=1)
welcome.pack(pady=2)

Posude_prikaz = tk.Button(welcome_window, text='LISTA POSUDA', font='Hevletica 10', width=13)
Posude_prikaz.place(x=200, y=500)
Posude_prikaz.bind('<ButtonRelease-1>', prikazi_posude2)

lista_biljki_button = tk.Button(welcome_window, text='LISTA BILJKI', font='Hevletica 10', width=13)
lista_biljki_button.place(x=400, y=500)
lista_biljki_button.bind('<ButtonRelease-1>', prikazi_biljke2)


# sučelje za prikaz liste Py Posuda


main_window.title('PyPosude')
main_window.geometry('900x700')
main_window.protocol('WM_DELETE_WINDOW', ukloni)
main_window.withdraw()


frame1 = tk.Frame(main_window,bg="#2D6A4F",width=900,height=100)
frame1.pack()

azuriraj_senzore_button = tk.Button(frame1, text='OČITAJ SENZORE', font='Arial 10', width=22, bg='white', command=azuriraj_senzore)
azuriraj_senzore_button.place(x=600, y=40)

prijelaz_na_biljke_button = tk.Button (frame1, text='BILJKE', font='Arial 10', width=22, bg='white')
prijelaz_na_biljke_button.bind('<ButtonRelease-1>', idi_na_biljke) 
prijelaz_na_biljke_button.place(x=600, y=70)


prikazi_sve_posude()

# sučelje ze unos nove PyPosude

UnosPosuda_window = tk.Toplevel(main_window)
UnosPosuda_window.geometry('700x700')
UnosPosuda_window.title('Unos nove posude')
UnosPosuda_window.protocol('WM_DELETE_WINDOW', ukloni)
UnosPosuda_window.withdraw()

global posuda_Entry
naziv_posude_label = tk.Label (UnosPosuda_window, text='Unesite ime posude: ',font='Helvetica 10')
naziv_posude_label.place(x= 100, y =100)

posuda_entry = tk.Entry(UnosPosuda_window, font='Helvetica 10')
posuda_entry.place(x=250, y =100)

posadena_biljka = tk.Label(UnosPosuda_window, text ='Posađena biljka: ', font='Helvetica 10')
posadena_biljka.place(x=100, y =150)
posadena_biljka = tk.Entry(UnosPosuda_window, font='Helvetica 10')

biljka_posadena_u_posudi = tk.BooleanVar()

# Definiranje funkcije koja će se pokrenuti kada se promijeni stanje CheckButton-a
dostupne_biljke_za_novu_posudu=[]
biljkaDatabase = BiljkaDatabase('PyFlora.db')
biljke = biljkaDatabase.get_all_biljke()
nazivi_biljka_sa_pripadajucim_id = {"":-1}
for i in range(len(biljke)):
    nazivi_biljka_sa_pripadajucim_id[biljke[i].naziv] = biljke[i].id_biljka

def check_box_za_posadenu_biljku(data):
    if biljka_posadena_u_posudi.get():
        entries3=[]
        biljkaDatabase = BiljkaDatabase('PyFlora.db')
        biljke = biljkaDatabase.get_all_biljke()
        for i in range(len(biljke)):
            entries3.append(biljke[i].naziv)
        data['values']=entries3
        
    else:
        entries3=[]
        data['values']=entries3

# Stvaranje CheckButton-a
biljke_za_novu_posudu_combobox = ttk.Combobox(UnosPosuda_window, values=dostupne_biljke_za_novu_posudu, font='Helvetica 10')
biljke_za_novu_posudu_combobox.config(state='readonly')
check_button = tk.Checkbutton(UnosPosuda_window, font='Helvetica 10', variable=biljka_posadena_u_posudi, command=lambda data=biljke_za_novu_posudu_combobox: check_box_za_posadenu_biljku(data))
check_button.place(x=245, y=150)

lista_biljki_label = tk.Label(UnosPosuda_window, text='Odaberite biljku: ', font='Helvetica 10')
lista_biljki_label.place(x=100, y=200)

odabrana_biljka_za_novu_posudu=""
def odaberi_biljku_za_novu_posudu(event):
     # Dohvaćanje odabrane stavke iz ComboBox-a
    global odabrana_biljka_za_novu_posudu
    odabrana_biljka_za_novu_posudu = biljke_za_novu_posudu_combobox.get()

# # Stvaranje ComboBox-a

# # Dodavanje funkcije on_select kao handlera događaja odabira stavke
biljke_za_novu_posudu_combobox.bind("<<ComboboxSelected>>",  odaberi_biljku_za_novu_posudu)


biljke_za_novu_posudu_combobox.place(x=250,y=200)

spremi_posudu_button = tk.Button(UnosPosuda_window, text = 'SPREMI', font='Hevletica 10', width=10)
spremi_posudu_button.bind('<ButtonRelease-1>', dodaj_posudu) 
spremi_posudu_button.place(x=250, y = 500)

povratak_profil_button = tk.Button(UnosPosuda_window, text = 'MOJ PROFIL', font='Helvetica 10', width=10)
povratak_profil_button.bind('<ButtonRelease-1>', s_posude_na_profil) 
povratak_profil_button.place(x=350, y = 500)


# sučelje za prikaz detalja o PyPosudama

PyPosuda_window = tk.Toplevel(main_window)
PyPosuda_window.geometry('700x700')
PyPosuda_window.title('PyPosuda')
PyPosuda_window.protocol('WM_DELETE_WINDOW', ukloni)
PyPosuda_window.withdraw()

frame1 = tk.Frame(PyPosuda_window,bg="#2D6A4F",width=700,height=100)
frame1.pack()


message = ''''''


biljka_button = tk.Button(PyPosuda_window, text='BILJKE', font='Arial 10', width=12, bg='white')
biljka_button.place(x=450, y=40)
biljka_button.bind('<ButtonRelease-1>', prikazi_biljku)  

profil_button = tk.Button(PyPosuda_window, text='MOJ PROFIL', font='Arial 10', width=12, bg='white')
profil_button.place(x=450, y=15)
profil_button.bind('<ButtonRelease-1>', profil)  


button_line_chart = tk.Button(PyPosuda_window, text='Line chart', font='Arial 10', width=10, bg='white')   #todo: PROMIJENI NAZIVE BUTTONA
button_line_chart.place(x=80, y=350)
button_scatter_plot = tk.Button(PyPosuda_window, text='Scatter plot', font='Arial 10', width=10, bg='white')
button_scatter_plot.place(x=80, y=380)
button_histogram = tk.Button(PyPosuda_window, text='Histogram', font='Arial 10', width=10, bg='white')
button_histogram.place(x=80, y=410)

naziv_PyPosude_label = tk.Label(PyPosuda_window, text='Naziv PyPosude', font='Arial 15')
naziv_PyPosude_label.place(x=80, y=100)
senzor_1_label = tk.Label(PyPosuda_window, text='- vrijednost senzora 1', font='Arial 10')
senzor_1_label.place(x=80, y=150)
senzor_2_label = tk.Label(PyPosuda_window, text='- vrijednost senzora 2', font='Arial 10')
senzor_2_label.place(x=80, y=180)
senzor_3_label = tk.Label(PyPosuda_window, text='- vrijednost senzora 3', font='Arial 10')

comboboxvaluesPromijeniBiljku=[]
biljkaDatabase = BiljkaDatabase('PyFlora.db')
biljke = biljkaDatabase.get_all_biljke()
nazivi_biljka_sa_pripadajucim_id = {"":-1}
for i in range(len(biljke)):
    nazivi_biljka_sa_pripadajucim_id[biljke[i].naziv] = biljke[i].id_biljka
    comboboxvaluesPromijeniBiljku.append(biljke[i].naziv)

comboboxPromijeniBiljku = ttk.Combobox(PyPosuda_window, values=comboboxvaluesPromijeniBiljku, font='Helvetica 10')
comboboxPromijeniBiljku.config(state='readonly')


PromijeniBiljku = tk.Label(PyPosuda_window, text='Odaberite biljku: ', font='Helvetica 10')
PromijeniBiljku.place(x=80, y=270)

PromijenjenaBiljka=""
def promijeni_biljku_combobox(event):
     # Dohvaćanje odabrane stavke iz ComboBox-a
    global PromijenjenaBiljka
    PromijenjenaBiljka = comboboxPromijeniBiljku.get()

comboboxPromijeniBiljku.bind("<<ComboboxSelected>>",  promijeni_biljku_combobox)
comboboxPromijeniBiljku.place(x=80,y=300)

# # Stvaranje ComboBox-a

# # Dodavanje funkcije on_select kao handlera događaja odabira stavke
biljke_za_novu_posudu_combobox.bind("<<ComboboxSelected>>",  odaberi_biljku_za_novu_posudu)

senzor_3_label.place(x=80, y=210)
obrisiPosudu = tk.Button(PyPosuda_window, text='Obrisi', font='Hevletica 10', width=12)
obrisiPosudu.place(x=450, y = 120)
azuriraj_posudu_buttton = tk.Button(PyPosuda_window, text='Ažuriraj', font='Hevletica 10', width=12)
azuriraj_posudu_buttton.place(x=450, y = 150)
isprazni_posudu_button = tk.Button(PyPosuda_window, text='Isprazni posudu', font='Hevletica 10', width=12)
isprazni_posudu_button.place(x=450, y = 210)
korak_natrag_button = tk.Button(PyPosuda_window, text='Natrag', font='Hevletica 10', width=12)
korak_natrag_button.bind('<ButtonRelease-1>', korak_natrag)  # preko lambde
korak_natrag_button.place(x=450, y = 180)



# sučelje za prikaz liste biljki

PyBiljka_window.geometry('900x700')
PyBiljka_window.title('Biljke')
PyBiljka_window.protocol('WM_DELETE_WINDOW', ukloni)
PyBiljka_window.withdraw()

frame1 = tk.Frame(PyBiljka_window,bg="#2D6A4F",width=900,height=100)
frame1.pack()

posude_button = tk.Button(frame1, text='POSUDE', font='Arial 10', width=10, bg='white')
posude_button.place(x=490, y=40)
posude_button.bind('<ButtonRelease-1>', prikazi_posude)

prikazi_sve_biljke()


# sučelje ze unos nove biljke

lista_biljka_zalijevanje = ['dnevno', 'tjedno', 'mjesecno']
lista_biljka_osvjetljenje = ['jarko', 'sjenovito', 'umjereno']
lista_biljka_toplina = ['toplije', 'umjereno', 'hladnije']

UnosBiljka_window = tk.Toplevel(PyBiljka_window)
UnosBiljka_window.geometry('700x700')
UnosBiljka_window.title('Unos nove biljke')
UnosBiljka_window.protocol('WM_DELETE_WINDOW', ukloni)
UnosBiljka_window.withdraw()


naziv_biljke_label = tk.Label (UnosBiljka_window, text='Unesite ime biljke: ',font='Helvetica 10')
naziv_biljke_label.place(x= 100, y =100)

naziv_biljke_entry = tk.Entry(UnosBiljka_window, font='Helvetica 10')
naziv_biljke_entry.place(x=280, y =100)

zalijevanje_biljka = tk.Label(UnosBiljka_window, text ='Odaberite vrstu zalijevanja: ', font='Helvetica 10')
zalijevanje_biljka.place(x=100, y =150)

comboboxZ = ttk.Combobox(UnosBiljka_window,values=lista_biljka_zalijevanje)
comboboxZ.config(state='readonly')



selected_zalijevanje=lista_biljka_zalijevanje
def odaberi_biljku_za_novu_posudu(event):
     # Dohvaćanje odabrane stavke iz ComboBox-a
     global selected_zalijevanje
     try:
        selected_zalijevanje = comboboxZ.get()
        print("Odabrana stavka:", selected_zalijevanje)
     except tk.TclError:
        messagebox.showwarning("Upozorenje", "Niste odabrali ispravnu vrijednost.")



# # Stvaranje ComboBox-a

# # Dodavanje funkcije on_select kao handlera događaja odabira stavke
comboboxZ.bind("<<ComboboxSelected>>",  odaberi_biljku_za_novu_posudu)


comboboxZ.place(x=280,y=150)

svjetlost_biljka_label = tk.Label(UnosBiljka_window, text ='Odaberite razinu osvjetljenja: ', font='Helvetica 10')
svjetlost_biljka_label.place(x=100, y =200)


comboboxS = ttk.Combobox(UnosBiljka_window,values=lista_biljka_osvjetljenje)
comboboxS.config(state='readonly')


selected_osjetljenje=lista_biljka_osvjetljenje

def odaberi_biljku_za_novu_posudu(event):
     # Dohvaćanje odabrane stavke iz ComboBox
     global selected_osjetljenje
     try:
        selected_osjetljenje = comboboxS.get()
        print("Odabrana stavka:", selected_osjetljenje)
     except tk.TclError:
        # Ignoriranje unosa korisnika
        pass


# # Stvaranje ComboBox-a

# # Dodavanje funkcije on_select kao handlera događaja odabira stavke
comboboxS.bind("<<ComboboxSelected>>",  odaberi_biljku_za_novu_posudu)


comboboxS.place(x=280,y=200)

Toplina_biljka = tk.Label(UnosBiljka_window, text ='Odaberite razinu topline: ', font='Helvetica 10')
Toplina_biljka.place(x=100, y =250)


comboboxT = ttk.Combobox(UnosBiljka_window,values=lista_biljka_toplina)
comboboxT.config(state='readonly')


selected_toplina=lista_biljka_toplina
def odaberi_biljku_za_novu_posudu(event):
     # Dohvaćanje odabrane stavke iz ComboBox-a
     global selected_toplina
     selected_toplina = comboboxT.get()
     print("Odabrana stavka:", selected_toplina)


# # Stvaranje ComboBox-a

# # Dodavanje funkcije on_select kao handlera događaja odabira stavke
comboboxT.bind("<<ComboboxSelected>>",  odaberi_biljku_za_novu_posudu)


comboboxT.place(x=280,y=250)



supstrat = tk.Label(UnosBiljka_window, text ='Supstrat: ', font='Helvetica 10')
supstrat.place(x=450, y =250)
supstrat = tk.Entry(UnosBiljka_window, font='Helvetica 10')
check_supstrat = tk.BooleanVar()
supstrat_checkbutton = tk.Checkbutton(UnosBiljka_window, variable=check_supstrat)
supstrat_checkbutton.place(x=500, y=250)


# Definiranje funkcije koja će se pokrenuti kada se promijeni stanje CheckButton-a


spremi_biljku_button = tk.Button(UnosBiljka_window, text='SPREMI', font='Hevletica 10', width=10)
spremi_biljku_button.place(x=100, y = 500)
spremi_biljku_button.bind('<ButtonRelease-1>', dodaj_biljku)  # preko lambde

odaberi_fotografiju_button = tk.Button(UnosBiljka_window, text='Odaberite fotografiju', font='Hevletica 10',  width=15, command=odaberi_fotografiju)
odaberi_fotografiju_button.place(x=100, y = 300)

biljke_povratak_button = tk.Button(UnosBiljka_window, text='MOJ PROFIL', font='Hevletica 10', width=13)
biljke_povratak_button.place(x=400, y=500)
biljke_povratak_button.bind('<ButtonRelease-1>', s_biljke_na_profil)


# sučelje za prikaz detalja o biljci



PyBiljka_detaljno_window.geometry('800x600')
PyBiljka_detaljno_window.title('Biljke')
PyBiljka_detaljno_window.protocol('WM_DELETE_WINDOW', ukloni)
PyBiljka_detaljno_window.withdraw()

frame1 = tk.Frame(PyBiljka_detaljno_window,bg="#2D6A4F",width=900,height=100)
frame1.pack()

moj_profil_button = tk.Button(PyBiljka_detaljno_window, text='MOJ PROFIL', font='Arial 10', width=10, bg='white')
moj_profil_button.bind('<ButtonRelease-1>', moj_profil) 
moj_profil_button.place(x=400, y=20)

azuriraj_biljku_button = tk.Button(PyBiljka_detaljno_window, text='Ažuriraj', font='Arial 10', width=10, bg='white')
azuriraj_biljku_button.place(x=400, y=150)

obrisi_biljku_button = tk.Button(PyBiljka_detaljno_window, text='Obriši', font='Hevletica 10', width=10)
obrisi_biljku_button.place(x=400, y = 180)

natrag_na_biljke_button = tk.Button(PyBiljka_detaljno_window, text='Natrag', font='Hevletica 10', width=10)
natrag_na_biljke_button.bind('<ButtonRelease-1>', natrag) 
natrag_na_biljke_button.place(x=400, y = 210)



naziv_biljke_label = tk.Label(PyBiljka_detaljno_window, text='Naziv Biljke', font='Arial 15')
naziv_biljke_label.place(x=80, y=100)
zalijevanje_biljke = tk.Label(PyBiljka_detaljno_window, text='Njega biljke', font='Arial 10')
zalijevanje_biljke.place(x=80, y=150)
osvjetljenje_biljke = tk.Label(PyBiljka_detaljno_window, text='- vrijednost 1', font='Arial 10')
osvjetljenje_biljke.place(x=80, y=180)
razina_topline = tk.Label(PyBiljka_detaljno_window, text='- vrijednost 2', font='Arial 10')
razina_topline.place(x=80, y=210)

biljka_naziv = tk.Label (PyBiljka_detaljno_window, text='Promijeni naziv biljke: ',font='Helvetica 10')
biljka_naziv.place(x= 85, y =260)

biljka_naziv = tk.Entry(PyBiljka_detaljno_window, font='Helvetica 10')
biljka_naziv.place(x=85, y =320)


root.mainloop()






