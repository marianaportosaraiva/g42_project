from classes.university import University
from classes.program import Program
from classes.faculty import Faculty
from classes.partnership import Partnership

def main():

    caminho_bd = 'data/g42_database.sqlite'
    
    University.read(caminho_bd)
    Program.read(caminho_bd)
    Faculty.read(caminho_bd)
    Partnership.read(caminho_bd)

    print("\n Resumo dos dados carregados:")
    print(f"- Universidades: {len(University.lst)}")
    print(f"- Programas: {len(Program.lst)}")
    print(f"- Faculdades: {len(Faculty.lst)}")
    print(f"- Associações: {len(Partnership.lst)}")

    print("\n Leitura Individual:")
    
    if len(University.lst) > 0:
        id_primeira_univ = University.lst[0]
        primeira_univ = University.obj[id_primeira_univ]
        print(f"- O nome da primeira universidade é: {primeira_univ.name}")

    if len(Program.lst) > 0:
        id_primeiro_prog = Program.lst[0]
        primeiro_prog = Program.obj[id_primeiro_prog]
        print(f"- O primeiro programa é da categoria: {primeiro_prog.category}")
        

if __name__ == "__main__":
    main()