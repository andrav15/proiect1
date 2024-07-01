import re
import csv
def validare_nume(nume_prenume):
    return re.match(r'^[a-zA-Z\s\-]+$', nume_prenume) and not re.search(r'[+@!?\\/]', nume_prenume)



def validare_cnp(CNP):
    if re.match(r'^\d{13}$', CNP) and not re.search(r'[+@!?\\/]', CNP):
        v_ultima_cifra=[2,7,9,1,4,6,3,5,8,2,7,9]
        s=0
        for i in range(len(v_ultima_cifra)):
            s+=int(CNP[i])*v_ultima_cifra[i]
        x=s%11
        if x == 10:
            x=1
        else: x=x
        return x == int(CNP[-1])
    return False


def validare_elemente(nume_prenume_cnp):
    match=re.match(r'^([a-zA-Z\-]+)\s+([a-zA-Z\-]+)(?:\s|-)?([a-zA-Z\-]*)\s+(\d{13})$', nume_prenume_cnp.strip())
    if not match:
        return None
    nume=match.group(1).strip()
    prenume1=match.group(2).strip()
    prenume2=match.group(3).strip()
    CNP=match.group(4).strip()
    if not validare_nume(nume) or not validare_nume(prenume1) or (prenume2 and not validare_nume(prenume2)):
        return None
    if not validare_cnp(CNP):
        return None
    return {'nume': nume, 'prenume1': prenume1, 'prenume2': prenume2, 'CNP': CNP}

def salvare_in_fisier(lista_cursanti):
    with open("cursanti.csv",mode='wt',newline='',encoding='utf-8') as fisier:
        fieldnames = ['nume', 'prenume1', 'prenume2', 'CNP']
        writer = csv.DictWriter(fisier,fieldnames=fieldnames)
        writer.writeheader()
        for cursant in lista_cursanti:
            writer.writerow(cursant)
    print(f"Datele au fost salvate în 'cursanti.csv'")

def main():
    cursanti_introdusi=[]
    while True:
        nume_prenume_input=input("Date cursanti: ").strip()
        if nume_prenume_input.lower() == 'exit':
            break
        elif nume_prenume_input.lower() == 'salveaza':
            if cursanti_introdusi:
                salvare_in_fisier(cursanti_introdusi)
            else:
                print("Nu există date de salvat.")
        else:
            date_valide=validare_elemente(nume_prenume_input)
            if date_valide:
                cursanti_introdusi.append(date_valide)
            else:
                print("Datele nu sunt valide.")
    print("\nToate datele salvate:")
    for nr, date in enumerate(cursanti_introdusi, start=1):
        print(f"Cursant {nr}: {date}")
    return cursanti_introdusi
if __name__ == "__main__":
    main()
