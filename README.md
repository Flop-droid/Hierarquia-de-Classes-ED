# Calculadora Matricial Orientada a Objetos em Python 💻
Este projeto é uma calculadora matricial eficiente e robusta, desenvolvida em *Python*. A aplicação utiliza os princípios da Programação Orientada a Objetos (POO) para manipular diversos tipos de matrizes, incluindo as formas Geral (m x n), Diagonal e Triangulares (Superior e Inferior). A calculadora foi projetada para otimizar tanto o uso de memória quanto o desempenho, empregando estruturas de dados e algoritmos especializados para cada tipo de matriz.

## Funcionalidades Abordadas
* **Múltiplos Tipos de Matriz:** Suporte nativo para matrizes Gerais, Diagonais e Triangulares (Superior/Inferior).

* **Criação de Tipos Específicos:** Permite que o usuário crie diretamente o tipo de matriz desejado, aproveitando desde o início as otimizações de memória.

* **Otimização de Memória:** Utiliza estruturas de dados especializadas para minimizar a ocupação de memória:
  * _Diagonal:_ **Armazena apenas os n elementos da diagonal principal** em uma lista simples.
  * _Triangular:_ **Armazena apenas os elementos não nulos** em uma lista de listas de tamanhos variáveis.
  * _Geral:_ Utiliza uma **lista de listas padrão** para máxima flexibilidade.

* **Otimização de Desempenho:** Emprega polimorfismo para usar algoritmos de alto desempenho para operações entre matrizes do mesmo tipo. Por exemplo:
  * A soma de duas matrizes diagonais é uma operação **O(n)**, em vez de O(n²).
  * O cálculo do determinante de uma matriz triangular ou diagonal é uma operação **O(n)**.

* **Sobrecarga de Operadores:** Oferece uma sintaxe natural e intuitiva para operações matriciais (ex: `C = A + B`, `C = A * escalar`).

* **Operações Matriciais Essenciais:**
  1. Adição (+) e
  2. Subtração (-)
  3. Multiplicação de Matrizes (*)
  4. Multiplicação por Escalar (*)
  5. Transposição

* **Operações Específicas:**

  6. Traço: Para todas as matrizes quadradas.
  7. Determinante: Otimizado para matrizes diagonais e triangulares.

* **Menu Interativo via Console:** Uma interface de linha de comando amigável para gerenciar e operar sobre uma lista de matrizes armazenadas.

* **Usamos as seguintes bibliotecas:** abc (para Classes Base Abstratas), typing (para anotações de tipo) e copy.

## Como Começar
### Pré-requisitos

Para executar este projeto, você precisará ter o Python 3 instalado em seu sistema [baixar em: https://www.python.org].

### Execução
1. Salve o código em um arquivo, por exemplo, calculadora.py.
2. Navegue até o diretório do projeto no seu terminal.
3. Execute o script com o seguinte comando: `python calculadora.py`

----------------------------
## Como Usar
Assim que o programa estiver em execução, você será recebido por um menu interativo. Onde você poderá:
  1. Inserir uma nova matriz: O programa guiará você para escolher o tipo (Geral, Diagonal, etc.) e inserir os elementos correspondentes da matriz.
  2. Inserir uma matriz identidade: Uma forma rápida de criar uma matriz diagonal especializada.
  3. Listar todas as matrizes: Observe todas as matrizes atualmente em memória, junto com seu índice, nome, tipo e dimensões.
  4. Realizar operações: Selecione uma operação (como "Soma") e escolha as matrizes operandas da lista pelo seu índice. O resultado será armazenado como uma nova matriz.
----------------------------

## Arquitetura do Projeto
* O projeto foi desenhado em torno de uma hierarquia de classes limpa e extensível, que demonstra os princípios-chave da POO em Python.
* Matriz: Uma Classe Base Abstrata (ABC) que define a interface comum para todas as matrizes, utilizando o decorador @abstractmethod para garantir que as classes filhas implementem os métodos essenciais.
* Classes Concretas: MatrizGeral, MatrizDiagonal, MatrizTriangularInferior e MatrizTriangularSuperior herdam de Matriz e fornecem as implementações concretas, cada uma com sua própria estrutura de dados otimizada e lógica de acesso.
* CalculadoraMatricial: A classe controladora principal que gerencia a interface com o usuário, a lista de matrizes e orquestra as operações de alto nível.
* Mecanismo de Fallback: Para operações entre tipos diferentes (ex: Diagonal + Geral), as classes especializadas convertem-se para uma MatrizGeral temporária para garantir que o cálculo seja realizado corretamente, priorizando a robustez sobre a performance nesses casos mistos.

