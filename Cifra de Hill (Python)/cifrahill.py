# Biblioteca para conseguir pegar os parâmetros passados pelo prompt
import sys
# Biblioteca para trabalhar com matrizes
import numpy

# Tabela de conversão, que poderia ser qualquer tabela de mapeamento de 26 caracteres
tabela = {
    'Z': 0, 'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
    'J': 10, 'K': 11, 'L': 12, 'M': 13, 'N': 14, 'O': 15, 'P': 16, 'Q': 17, 'R': 18, 'S': 19,
    'T': 20, 'U': 21, 'V': 22, 'W': 23, 'X': 24, 'Y': 25}

# Lista para fazer a recuperação do caractere
lista_caracteres = list(tabela.keys())

# Chave para cifrar (Matriz do exemplo)
matriz_chave = numpy.array([numpy.array([1, 2]), numpy.array([3, 5])])

# Chave para decifrar
matriz_chave_inversa = numpy.linalg.inv(matriz_chave)

# Função para ler o arquivo
def ler_arquivo(diretorio: str) -> str:
    # Tenta abrir o arquivo
    try:
        arquivo = open(diretorio, 'r', encoding='utf-8')
    except:
        print('Erro ao abrir o arquivo')
        sys.exit()
    # Lê o arquivo todo
    texto_arquivo = arquivo.read()
    arquivo.close()
    return texto_arquivo


def escrever_arquivo(diretorio: str, conteudo: str) -> str:
    # Tenta abrir o arquivo
    try:
        arquivo = open(diretorio, 'w', encoding='utf-8')
    except:
        print('Erro ao abrir o arquivo')
        sys.exit()
    # Lê o arquivo todo
    arquivo.write(conteudo)
    arquivo.close()


def cifrar(texto_claro: str) -> str:
    #Trata as informações para se adequar a cifração com 26 caracteres, dados são perdidos
    texto_claro = texto_claro.upper()
    texto_claro = texto_claro.replace('\n', '')
    texto_claro = texto_claro.replace(' ', '')

    # verifica se é divisível por 2
    if len(texto_claro) % 2 != 0:
        texto_claro += 'A'

    # Converte de letras para número
    lista_numeros = numpy.array([tabela[c] for c in texto_claro])

    # Agrupa em grupos de 2
    matriz_lista_numeros = []
    for divisor in range(int(len(lista_numeros) / 2)):
        matriz_lista_numeros.append(lista_numeros[divisor*2: (divisor+1)*2])

    # Transforma os vetores em matrizes 2x1
    matriz_lista_numeros = [numpy.array(
        [numpy.array(m[0]), numpy.array(m[1])]) for m in matriz_lista_numeros]
    matriz_lista_numeros = numpy.array(matriz_lista_numeros)

    # Multiplica cada matriz pela chave
    matriz_lista_numeros = [numpy.dot(matriz_chave, m)
                            for m in matriz_lista_numeros]

    # Transforma as matrizes em vetores
    matriz_lista_numeros = [m.flatten() for m in matriz_lista_numeros]

    # Transforma o vetor de vetores em um vetor só
    vetor = []
    for m in matriz_lista_numeros:
        vetor.extend(m)

    #Faz o módulo dos números 
    vetor = [x % len(tabela) for x in vetor]

    # Transforma o vetor de número em caracteres
    texto_cifrado = ''
    for c in vetor:
        texto_cifrado += lista_caracteres[c]

    # Retorna o texto cifrado
    return texto_cifrado


def to_list(linha: str):
    linha = linha.replace('[ ', '')
    linha = linha.replace('[', '')
    linha = linha.replace('  ', ' ')
    linha = linha.replace(']', '')
    return [int(item) for item in linha.split(' ')]


def decifrar(texto_cifrado: str) -> str:
    # Converte de letras para número
    lista_numeros = numpy.array([tabela[c] for c in texto_cifrado])

    # Agrupa em grupos de 2
    matriz_lista_numeros = []
    for divisor in range(int(len(lista_numeros) / 2)):
        matriz_lista_numeros.append(lista_numeros[divisor*2: (divisor+1)*2])

    # Transforma os vetores em matrizes 2x1
    matriz_lista_numeros = [numpy.array(
        [numpy.array(m[0]), numpy.array(m[1])]) for m in matriz_lista_numeros]
    matriz_lista_numeros = numpy.array(matriz_lista_numeros)

    # Multiplica cada matriz pela chave de decifração
    matriz_lista_numeros = [numpy.dot(matriz_chave_inversa, m)
                            for m in matriz_lista_numeros]

    # Transforma as matrizes em vetores
    matriz_lista_numeros = [m.flatten() for m in matriz_lista_numeros]

    # Transforma o vetor de vetores em um vetor só
    vetor = []
    for m in matriz_lista_numeros:
        vetor.extend(m)

    # Tranforma os números em inteiros
    vetor = [int(x) for x in vetor]

    #Faz o módulo dos números 
    vetor = [x % len(tabela) for x in vetor]

    # Transforma o vetor de número em caracteres
    texto_decifrado = ''
    for c in vetor:
        texto_decifrado += lista_caracteres[c]

    # Retorna o texto cifrado
    return texto_decifrado


# Receber os comandos pela linha de comando
if sys.argv[1] == '-enc':
    if sys.argv[3] == '-out':
        escrever_arquivo(sys.argv[4], cifrar(ler_arquivo(sys.argv[2])))
    else:
        print(sys.argv[3], ' não é um comando reconhecido')
        sys.exit()
elif sys.argv[1] == '-dec':
    if sys.argv[3] == '-out':
        escrever_arquivo(sys.argv[4], decifrar(ler_arquivo(sys.argv[2])))
    else:
        print(sys.argv[3], ' não é um comando reconhecido')
        sys.exit()
else:
    print(sys.argv[1], ' não é um comando reconhecido')
    sys.exit()

# Como compilar
# O comando para cifrar é python cifrahill.py -enc dir_texto_claro.txt -out dir_texto_enc.txt
# O comando para decifrar é python cifrahill.py -dec dir_texto_enc.txt -out dir_texto_dect.txt
