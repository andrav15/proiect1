import re
import csv
class CNPInvalidError(Exception):
    def __init__(self, message="CNP-ul trebuie să aiba exact 13 cifre."):
        self.message = message
        super().__init__(self.message)
class NumeInvalidError(Exception):
    def __init__(self, message="Caractere interzise in nume si prenume!Numele si prenumele trebuie sa contina doar litere,spatiu/cratima intre prenume."):
        self.message=message
        super().__init__(self.message)
def majuscula(cuv):
    return cuv.capitalize()
def validare_nume(nume_prenume):
    if not re.match(r'^[a-zA-Z\-]+$', nume_prenume):
        raise NumeInvalidError()
    return True
def validare_cnp(CNP):
    if not re.match(r'^\d{13}$', CNP):
        raise CNPInvalidError()
    v_ultima_cifra=[2,7,9,1,4,6,3,5,8,2,7,9]
    s=sum(int(CNP[i]) * v_ultima_cifra[i] for i in range(len(v_ultima_cifra)))
    x=s%11
    if x == 10:
        x=1
    else:
        x=x
    return x == int(CNP[-1])

def validare_elemente(nume_prenume_cnp):
    match_cnp=re.search(r'\b\d{13}\b', nume_prenume_cnp)
    if not match_cnp:
        raise CNPInvalidError()
    CNP=match_cnp.group(0).strip()

    nume_prenume_part=nume_prenume_cnp[:match_cnp.start()].strip()
    parts=re.split(r'\s|-', nume_prenume_part)
    if len(parts)<2:
        raise NumeInvalidError()
    nume=majuscula(parts[0])
    prenume1=majuscula(parts[1])
    prenume2=majuscula(parts[2]) if len(parts)>2 else ""

    if not validare_nume(nume) or not validare_nume(prenume1) or (prenume2 and not validare_nume(prenume2)):
        raise NumeInvalidError()
    if not validare_cnp(CNP):
        return None
    return {'nume': nume, 'prenume1': prenume1, 'prenume2': prenume2, 'CNP': CNP}
def salvare_in_fisier(lista_cursanti, tip_fisier):
    if tip_fisier == 'csv':
        filename = 'cursanti.csv'
        with open(filename, mode='wt', newline='', encoding='utf-8') as fisier:
            fieldnames=['nume','prenume1','prenume2','CNP']
            writer=csv.DictWriter(fisier, fieldnames=fieldnames)
            writer.writeheader()
            for cursant in lista_cursanti:
                writer.writerow(cursant)
    elif tip_fisier == 'txt':
        filename='cursanti.txt'
        with open(filename, mode='wt', encoding='utf-8') as fisier:
            for cursant in lista_cursanti:
                fisier.write(f"Nume: {cursant['nume']}, Prenume1: {cursant['prenume1']}, Prenume2: {cursant['prenume2']}, CNP: {cursant['CNP']}\n")
    else:
        print("Tipul fisierului introdus nu este valid.")
        return
    print(f"Datele au fost salvate în '{filename}'")


def main():
    cursanti_introdusi = []
    while True:
        nume_prenume_input=input("Date cursanti: ").strip()
        if nume_prenume_input.lower() == 'exit':
            break
        elif nume_prenume_input.lower() == 'salveaza':
            if cursanti_introdusi:
                tip_fisier=input("Tipul fisierului(csv/txt): ").strip().lower()
                if tip_fisier in ['csv', 'txt']:
                    salvare_in_fisier(cursanti_introdusi, tip_fisier)
                else:
                    print("Tipul introdus nu este valid.")
            else:
                print("Nu există date de salvat.")
        else:
            try:
                date_valide=validare_elemente(nume_prenume_input)
                if date_valide:
                    cursanti_introdusi.append(date_valide)
                else:
                    print("Datele nu sunt valide.")
            except(CNPInvalidError, NumeInvalidError) as e:
                print(e)
                print("Datele nu sunt valide.")

    print("\nToate datele salvate:")
    for nr,date in enumerate(cursanti_introdusi, start=1):
        print(f"Cursant {nr}: {date}")
    return cursanti_introdusi


if __name__ == "__main__":
    main()
