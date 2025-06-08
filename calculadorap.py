from abc import ABC, abstractmethod
from typing import List
import copy

class Matriz(ABC):
    def __init__(self, linhas: int, colunas: int, nome: str = ""):
        self.linhas = linhas
        self.colunas = colunas
        self.nome = nome

    @abstractmethod
    def __add__(self, other):
        pass

    @abstractmethod
    def __sub__(self, other):
        pass

    @abstractmethod
    def __mul__(self, other):
        pass

    @abstractmethod
    def transposta(self):
        pass

    @abstractmethod
    def imprimir(self):
        pass

    def eh_quadrada(self):
        return self.linhas == self.colunas

    def tipo(self):
        return self.__class__.__name__

    def traço(self):
        raise NotImplementedError("Traço só para matrizes quadradas")

    def determinante(self):
        raise NotImplementedError("Determinante só para matrizes triangulares")

    def get_elemento(self, i, j):
        raise NotImplementedError

class MatrizGeral(Matriz):
    def __init__(self, linhas: int, colunas: int, dados: List[List[float]] = None, nome: str = ""):
        super().__init__(linhas, colunas, nome)
        if dados:
            self.dados = dados
        else:
            self.dados = [[0.0]*colunas for _ in range(linhas)]

    def __add__(self, other):
        if not isinstance(other, Matriz):
            raise TypeError("Operação somente entre matrizes")
        if self.linhas != other.linhas or self.colunas != other.colunas:
            raise ValueError("Dimensões incompatíveis para soma")
        if type(self) == type(other):
            return self.soma_especializada(other)
        resultado = MatrizGeral(self.linhas, self.colunas)
        for i in range(self.linhas):
            for j in range(self.colunas):
                resultado.dados[i][j] = self.dados[i][j] + other.get_elemento(i, j)
        return resultado

    def soma_especializada(self, other):
        resultado = MatrizGeral(self.linhas, self.colunas)
        for i in range(self.linhas):
            for j in range(self.colunas):
                resultado.dados[i][j] = self.dados[i][j] + other.dados[i][j]
        return resultado

    def __sub__(self, other):
        if self.linhas != other.linhas or self.colunas != other.colunas:
            raise ValueError("Dimensões incompatíveis para subtração")
        resultado = MatrizGeral(self.linhas, self.colunas)
        for i in range(self.linhas):
            for j in range(self.colunas):
                resultado.dados[i][j] = self.dados[i][j] - other.get_elemento(i, j)
        return resultado

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            resultado = MatrizGeral(self.linhas, self.colunas)
            for i in range(self.linhas):
                for j in range(self.colunas):
                    resultado.dados[i][j] = self.dados[i][j] * other
            return resultado
        elif isinstance(other, Matriz):
            if self.colunas != other.linhas:
                raise ValueError("Dimensões incompatíveis para multiplicação")
            resultado = MatrizGeral(self.linhas, other.colunas)
            for i in range(self.linhas):
                for j in range(other.colunas):
                    soma = 0.0
                    for k in range(self.colunas):
                        soma += self.dados[i][k] * other.get_elemento(k, j)
                    resultado.dados[i][j] = soma
            return resultado
        else:
            raise TypeError("Multiplicação inválida")

    def transposta(self):
        resultado = MatrizGeral(self.colunas, self.linhas)
        for i in range(self.linhas):
            for j in range(self.colunas):
                resultado.dados[j][i] = self.dados[i][j]
        return resultado

    def get_elemento(self, i, j):
        return self.dados[i][j]

    def imprimir(self):
        print(f"Matriz {self.nome} ({self.tipo()} {self.linhas}x{self.colunas}):")
        for linha in self.dados:
            print(" ".join(f"{x:.2f}" for x in linha))

    def traço(self):
        if not self.eh_quadrada():
            raise ValueError("Traço só definido para matrizes quadradas")
        soma = 0.0
        for i in range(self.linhas):
            soma += self.dados[i][i]
        return soma

class MatrizDiagonal(Matriz):
    def __init__(self, n: int, diagonal: List[float] = None, nome: str = ""):
        super().__init__(n, n, nome)
        if diagonal:
            self.diagonal = diagonal
        else:
            self.diagonal = [0.0]*n

    def __add__(self, other):
        if not isinstance(other, MatrizDiagonal):
            return MatrizGeral(self.linhas, self.colunas, self.to_array()) + other
        if self.linhas != other.linhas:
            raise ValueError("Dimensões incompatíveis para soma")
        resultado = MatrizDiagonal(self.linhas)
        for i in range(self.linhas):
            resultado.diagonal[i] = self.diagonal[i] + other.diagonal[i]
        return resultado

    def __sub__(self, other):
        if not isinstance(other, MatrizDiagonal):
            return MatrizGeral(self.linhas, self.colunas, self.to_array()) - other
        if self.linhas != other.linhas:
            raise ValueError("Dimensões incompatíveis para subtração")
        resultado = MatrizDiagonal(self.linhas)
        for i in range(self.linhas):
            resultado.diagonal[i] = self.diagonal[i] - other.diagonal[i]
        return resultado

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            resultado = MatrizDiagonal(self.linhas)
            for i in range(self.linhas):
                resultado.diagonal[i] = self.diagonal[i] * other
            return resultado
        elif isinstance(other, MatrizDiagonal):
            if self.linhas != other.linhas:
                raise ValueError("Dimensões incompatíveis para multiplicação")
            resultado = MatrizDiagonal(self.linhas)
            for i in range(self.linhas):
                resultado.diagonal[i] = self.diagonal[i] * other.diagonal[i]
            return resultado
        else:
            return MatrizGeral(self.linhas, self.colunas, self.to_array()) * other

    def transposta(self):
        return copy.deepcopy(self)

    def traço(self):
        return sum(self.diagonal)

    def determinante(self):
        prod = 1.0
        for val in self.diagonal:
            prod *= val
        return prod

    def get_elemento(self, i, j):
        if i == j:
            return self.diagonal[i]
        else:
            return 0.0

    def to_array(self):
        matriz = [[0.0]*self.colunas for _ in range(self.linhas)]
        for i in range(self.linhas):
            matriz[i][i] = self.diagonal[i]
        return matriz

    def imprimir(self):
        print(f"Matriz {self.nome} ({self.tipo()} {self.linhas}x{self.colunas}):")
        for i in range(self.linhas):
            linha = []
            for j in range(self.colunas):
                linha.append(f"{self.diagonal[i]:.2f}" if i == j else "0.00")
            print(" ".join(linha))

class MatrizTriangularInferior(Matriz):
    def __init__(self, n: int, dados: List[List[float]] = None, nome: str = ""):
        super().__init__(n, n, nome)
        if dados:
            self.dados = dados
        else:
            self.dados = [[0.0]*(i+1) for i in range(n)]

    def __add__(self, other):
        if not isinstance(other, MatrizTriangularInferior):
            return MatrizGeral(self.linhas, self.colunas, self.to_array()) + other
        if self.linhas != other.linhas:
            raise ValueError("Dimensões incompatíveis para soma")
        resultado = MatrizTriangularInferior(self.linhas)
        for i in range(self.linhas):
            for j in range(i+1):
                resultado.dados[i][j] = self.dados[i][j] + other.dados[i][j]
        return resultado

    def __sub__(self, other):
        if not isinstance(other, MatrizTriangularInferior):
            return MatrizGeral(self.linhas, self.colunas, self.to_array()) - other
        if self.linhas != other.linhas:
            raise ValueError("Dimensões incompatíveis para subtração")
        resultado = MatrizTriangularInferior(self.linhas)
        for i in range(self.linhas):
            for j in range(i+1):
                resultado.dados[i][j] = self.dados[i][j] - other.dados[i][j]
        return resultado

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            resultado = MatrizTriangularInferior(self.linhas)
            for i in range(self.linhas):
                for j in range(i+1):
                    resultado.dados[i][j] = self.dados[i][j] * other
            return resultado
        else:
            return MatrizGeral(self.linhas, self.colunas, self.to_array()) * other

    def transposta(self):
        resultado = MatrizTriangularSuperior(self.linhas)
        for i in range(self.linhas):
            for j in range(i+1):
                resultado.dados[j][i] = self.dados[i][j]
        return resultado

    def traço(self):
        return sum(self.dados[i][i] for i in range(self.linhas))

    def determinante(self):
        prod = 1.0
        for i in range(self.linhas):
            prod *= self.dados[i][i]
        return prod

    def get_elemento(self, i, j):
        if j <= i:
            return self.dados[i][j]
        else:
            return 0.0

    def to_array(self):
        matriz = [[0.0]*self.colunas for _ in range(self.linhas)]
        for i in range(self.linhas):
            for j in range(i+1):
                matriz[i][j] = self.dados[i][j]
        return matriz

    def imprimir(self):
        print(f"Matriz {self.nome} ({self.tipo()} {self.linhas}x{self.colunas}):")
        for i in range(self.linhas):
            linha = []
            for j in range(self.colunas):
                linha.append(f"{self.dados[i][j]:.2f}" if j <= i else "0.00")
            print(" ".join(linha))

class MatrizTriangularSuperior(Matriz):
    def __init__(self, n: int, dados: List[List[float]] = None, nome: str = ""):
        super().__init__(n, n, nome)
        if dados:
            self.dados = dados
        else:
            self.dados = [[0.0]*(n - i) for i in range(n)]

    def __add__(self, other):
        if not isinstance(other, MatrizTriangularSuperior):
            return MatrizGeral(self.linhas, self.colunas, self.to_array()) + other
        if self.linhas != other.linhas:
            raise ValueError("Dimensões incompatíveis para soma")
        resultado = MatrizTriangularSuperior(self.linhas)
        for i in range(self.linhas):
            for j in range(self.colunas - i):
                resultado.dados[i][j] = self.dados[i][j] + other.dados[i][j]
        return resultado

    def __sub__(self, other):
        if not isinstance(other, MatrizTriangularSuperior):
            return MatrizGeral(self.linhas, self.colunas, self.to_array()) - other
        if self.linhas != other.linhas:
            raise ValueError("Dimensões incompatíveis para subtração")
        resultado = MatrizTriangularSuperior(self.linhas)
        for i in range(self.linhas):
            for j in range(self.colunas - i):
                resultado.dados[i][j] = self.dados[i][j] - other.dados[i][j]
        return resultado

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            resultado = MatrizTriangularSuperior(self.linhas)
            for i in range(self.linhas):
                for j in range(self.colunas - i):
                    resultado.dados[i][j] = self.dados[i][j] * other
            return resultado
        else:
            return MatrizGeral(self.linhas, self.colunas, self.to_array()) * other

    def transposta(self):
        resultado = MatrizTriangularInferior(self.linhas)
        for i in range(self.linhas):
            for j in range(self.colunas - i):
                resultado.dados[j][i] = self.dados[i][j]
        return resultado

    def traço(self):
        soma = 0.0
        for i in range(self.linhas):
            soma += self.dados[i][0] if i == 0 else self.dados[i][0] if i == 0 else self.dados[i][0]  # diagonal está no índice 0 da linha i
        return soma

    def determinante(self):
        prod = 1.0
        for i in range(self.linhas):
            prod *= self.dados[i][0]  # diagonal principal está na posição 0 de cada linha
        return prod

    def get_elemento(self, i, j):
        if j >= i:
            return self.dados[i][j - i]
        else:
            return 0.0

    def to_array(self):
        matriz = [[0.0]*self.colunas for _ in range(self.linhas)]
        for i in range(self.linhas):
            for j in range(self.colunas - i):
                matriz[i][j + i] = self.dados[i][j]
        return matriz

    def imprimir(self):
        print(f"Matriz {self.nome} ({self.tipo()} {self.linhas}x{self.colunas}):")
        for i in range(self.linhas):
            linha = []
            for j in range(self.colunas):
                linha.append(f"{self.dados[i][j - i]:.2f}" if j >= i else "0.00")
            print(" ".join(linha))

class CalculadoraMatricial:
    def __init__(self):
        self.lista_matrizes = []

    def inserir_matriz(self, matriz: Matriz):
        self.lista_matrizes.append(matriz)

    def remover_matriz(self, indice: int):
        if 0 <= indice < len(self.lista_matrizes):
            del self.lista_matrizes[indice]
        else:
            print("Índice inválido")

    def imprimir_matriz(self, indice: int):
        if 0 <= indice < len(self.lista_matrizes):
            self.lista_matrizes[indice].imprimir()
        else:
            print("Índice inválido")

    def listar_matrizes(self):
        print("Lista de Matrizes:")
        for idx, m in enumerate(self.lista_matrizes):
            print(f"{idx}: {m.nome} - {m.tipo()} {m.linhas}x{m.colunas}")

    def zerar_lista(self):
        self.lista_matrizes.clear()

    def inserir_identidade(self, n: int, nome: str = ""):
        diag = [1.0]*n
        identidade = MatrizDiagonal(n, diag, nome)
        self.inserir_matriz(identidade)

    def ler_matriz_teclado(self):
        try:
            tipo = input("Tipo (Geral, Diagonal, TriangularInferior, TriangularSuperior): ").strip()
            nome = input("Nome da matriz: ").strip()
            if tipo.lower() == "geral":
                m = int(input("Número de linhas: "))
                n = int(input("Número de colunas: "))
                dados = []
                print(f"Digite os elementos da matriz {m}x{n} linha por linha:")
                for _ in range(m):
                    linha = list(map(float, input().split()))
                    if len(linha) != n:
                        raise ValueError("Número de elementos inválido na linha")
                    dados.append(linha)
                matriz = MatrizGeral(m, n, dados, nome)
            elif tipo.lower() == "diagonal":
                n = int(input("Ordem da matriz diagonal (n x n): "))
                diag = list(map(float, input(f"Digite os {n} elementos da diagonal principal: ").split()))
                if len(diag) != n:
                    raise ValueError("Número de elementos da diagonal inválido")
                matriz = MatrizDiagonal(n, diag, nome)
            elif tipo.lower() == "triangularinferior":
                n = int(input("Ordem da matriz triangular inferior (n x n): "))
                dados = []
                print(f"Digite os elementos da matriz triangular inferior linha por linha (apenas elementos da parte inferior):")
                for i in range(n):
                    linha = list(map(float, input(f"Linha {i+1} (tamanho {i+1}): ").split()))
                    if len(linha) != i+1:
                        raise ValueError("Número de elementos inválido na linha")
                    dados.append(linha)
                matriz = MatrizTriangularInferior(n, dados, nome)
            elif tipo.lower() == "triangul Superior".lower() or tipo.lower() == "triangularesuperior":
                n = int(input("Ordem da matriz triangular superior (n x n): "))
                dados = []
                print(f"Digite os elementos da matriz triangular superior linha por linha (apenas elementos da parte superior):")
                for i in range(n):
                    linha = list(map(float, input(f"Linha {i+1} (tamanho {n - i}): ").split()))
                    if len(linha) != n - i:
                        raise ValueError("Número de elementos inválido na linha")
                    dados.append(linha)
                matriz = MatrizTriangularSuperior(n, dados, nome)
            else:
                print("Tipo inválido")
                return
            self.inserir_matriz(matriz)
            print("Matriz inserida com sucesso!")
        except Exception as e:
            print(f"Erro na leitura da matriz: {e}")

    def menu(self):
        while True:
            print("\n--- Calculadora Matricial ---")
            print("1. Listar matrizes")
            print("2. Imprimir matriz")
            print("3. Inserir matriz do teclado")
            print("4. Inserir matriz identidade")
            print("5. Remover matriz")
            print("6. Zerar lista")
            print("7. Operações (Soma, Subtração, Multiplicação, Transposição, Traço, Determinante)")
            print("0. Sair")
            opc = input("Escolha uma opção: ")
            if opc == "1":
                self.listar_matrizes()
            elif opc == "2":
                idx = int(input("Índice da matriz para imprimir: "))
                self.imprimir_matriz(idx)
            elif opc == "3":
                self.ler_matriz_teclado()
            elif opc == "4":
                try:
                    n = int(input("Ordem da matriz identidade: "))
                    nome = input("Nome da matriz identidade: ")
                    self.inserir_identidade(n, nome)
                    print("Matriz identidade inserida.")
                except:
                    print("Entrada inválida.")
            elif opc == "5":
                idx = int(input("Índice da matriz para remover: "))
                self.remover_matriz(idx)
            elif opc == "6":
                self.zerar_lista()
                print("Lista zerada.")
            elif opc == "7":
                self.menu_operacoes()
            elif opc == "0":
                print("Saindo...")
                break
            else:
                print("Opção inválida.")

    def menu_operacoes(self):
        print("\n--- Operações ---")
        print("1. Soma (C = A + B)")
        print("2. Subtração (C = A - B)")
        print("3. Multiplicação por escalar (C = a * A)")
        print("4. Multiplicação matricial (C = A * B)")
        print("5. Transposição")
        print("6. Traço (matriz quadrada)")
        print("7. Determinante (matriz triangular)")
        print("0. Voltar")
        opc = input("Escolha uma operação: ")
        try:
            if opc == "1":
                a = int(input("Índice da matriz A: "))
                b = int(input("Índice da matriz B: "))
                C = self.lista_matrizes[a] + self.lista_matrizes[b]
                nome = input("Nome para matriz resultado: ")
                C.nome = nome
                self.inserir_matriz(C)
                print("Soma realizada e matriz inserida.")
            elif opc == "2":
                a = int(input("Índice da matriz A: "))
                b = int(input("Índice da matriz B: "))
                C = self.lista_matrizes[a] - self.lista_matrizes[b]
                nome = input("Nome para matriz resultado: ")
                C.nome = nome
                self.inserir_matriz(C)
                print("Subtração realizada e matriz inserida.")
            elif opc == "3":
                a = int(input("Índice da matriz A: "))
                escalar = float(input("Valor escalar: "))
                C = self.lista_matrizes[a] * escalar
                nome = input("Nome para matriz resultado: ")
                C.nome = nome
                self.inserir_matriz(C)
                print("Multiplicação por escalar realizada e matriz inserida.")
            elif opc == "4":
                a = int(input("Índice da matriz A: "))
                b = int(input("Índice da matriz B: "))
                C = self.lista_matrizes[a] * self.lista_matrizes[b]
                nome = input("Nome para matriz resultado: ")
                C.nome = nome
                self.inserir_matriz(C)
                print("Multiplicação matricial realizada e matriz inserida.")
            elif opc == "5":
                a = int(input("Índice da matriz A: "))
                C = self.lista_matrizes[a].transposta()
                nome = input("Nome para matriz resultado: ")
                C.nome = nome
                self.inserir_matriz(C)
                print("Transposição realizada e matriz inserida.")
            elif opc == "6":
                a = int(input("Índice da matriz A: "))
                matriz = self.lista_matrizes[a]
                if matriz.eh_quadrada():
                    print(f"Traço da matriz: {matriz.traço()}")
                else:
                    print("Matriz não é quadrada.")
            elif opc == "7":
                a = int(input("Índice da matriz A: "))
                matriz = self.lista_matrizes[a]
                try:
                    det = matriz.determinante()
                    print(f"Determinante da matriz: {det}")
                except NotImplementedError:
                    print("Determinante não implementado para este tipo de matriz.")
            elif opc == "0":
                return
            else:
                print("Opção inválida.")
        except Exception as e:
            print(f"Erro na operação: {e}")

if __name__ == "__main__":
    calc = CalculadoraMatricial()
    calc.menu()
