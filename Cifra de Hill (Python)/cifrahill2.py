# Biblioteca para conseguir pegar os parâmetros passados pelo prompt
import sys
# Biblioteca para trabalhar com matrizes
import numpy

# Tabela de conversão, que poderia ser qualquer tabela de mapeamento
tabela = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
          'A': 10, 'Á': 11, 'Â': 12, 'Ã': 13, 'B': 14, 'C': 15, 'D': 16, 'E': 17, 'É': 18, 'Ê': 19, 
          'F': 20, 'G': 21, 'H': 22, 'I': 23, 'Í': 24, 'J': 25, 'K': 26, 'L': 27, 'M': 28, 'N': 29, 
          'O': 30, 'Ó': 31, 'Ô': 32, 'Õ': 33, 'P': 34, 'Q': 35, 'R': 36, 'S': 37, 'À': 38, '{': 39, 
          'T': 40, 'U': 41, 'Ú': 42, 'V': 43, 'W': 44, 'X': 45, 'Y': 46, 'Z': 47, 'a': 48, 'á': 49, 
          'â': 50, 'ã': 51, 'b': 52, 'c': 53, 'd': 54, 'e': 55, 'é': 56, 'ê': 57, 'f': 58, 'g': 59, 
          'h': 60, 'i': 61, 'í': 62, 'j': 63, 'k': 64, 'l': 65, 'm': 66, 'n': 67, 'o': 68, 'ó': 69, 
          'ô': 70, 'õ': 71, 'p': 72, 'q': 73, 'r': 74, 's': 75, 'à': 76, '}': 77, 't': 78, 'u': 79, 
          'ú': 80, 'v': 81, 'w': 82, 'x': 83, 'y': 84, 'z': 85, ',': 86, '.': 87, ';': 88, ':': 89,
          '!': 90, '?': 91, '@': 92, '#': 93, '$': 94, '&': 95, '§': 96, '(': 97, ')': 98, '_': 99, 
          '+': 100, '-': 101, '*': 102, '/': 103, '%': 104, '|': 105, '\\': 106, '\'': 107, '"': 108, 
          '[': 109, ']': 110}

# Lista para fazer a recuperação do caractere
lista_caracteres = list(tabela.keys())

# Chave para cifrar
matriz_chave = numpy.array([numpy.array([2, 1]), numpy.array([4, 3])])

# Chave para decifrar
matriz_chave_inversa = numpy.linalg.inv(matriz_chave)

# Função para ler o arquivo
def ler_arquivo(diretorio:str)->str:
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

# Função para escrever no arquivo 
def escrever_arquivo(diretorio:str, conteudo:str)->str:
    # Tenta abrir o arquivo
    try:
        arquivo = open(diretorio, 'w', encoding='utf-8')
    except:
        print('Erro ao abrir o arquivo')
        sys.exit()
    # Lê o arquivo todo
    arquivo.write(conteudo)
    arquivo.close()

def e_divisivel_por_4(numero:int)->bool:
    if numero == 0:
        return False
    numero %= 100
    return numero % 4 == 0


def cifrar(texto_claro:str) -> str:
    # Verifica se é divisível por 4
    while not(e_divisivel_por_4(len(texto_claro))):
        texto_claro += ' '

    # Como \n e espaço não podem ser chaves para dict eles foram substituidos por [ ]
    texto_claro = texto_claro.replace('\n', '[')
    texto_claro = texto_claro.replace(' ', ']')

    # Converte de letras para número
    lista_numeros = numpy.array([tabela[c] for c in texto_claro])

    # Agrupa em grupos de 4
    matriz_lista_numeros = []
    for divisor in range(int(len(lista_numeros) / 4)):
        matriz_lista_numeros.append(lista_numeros[divisor*4: (divisor+1)*4])
    
    # Transforma os vetores em matrizes 2x2
    matriz_lista_numeros = [numpy.array([numpy.array(m[:2]), numpy.array(m[2:])]) for m in matriz_lista_numeros]
    matriz_lista_numeros = numpy.array(matriz_lista_numeros)

    # Multiplica cada matriz pela chave
    matriz_lista_numeros = [numpy.dot(matriz_chave,m) for m in matriz_lista_numeros]
    
    # Transforma as matrizes em vetores
    matriz_lista_numeros = [m.flatten() for m in matriz_lista_numeros]

    # Transforma o vetor de vetores em strings
    texto_cifrado = ''
    for matriz in matriz_lista_numeros:
        for m in matriz:
            texto_cifrado += str(m) + ' '

        texto_cifrado = texto_cifrado[:-1]
        texto_cifrado += '\n'

    # Retorna o texto sem o último \n
    return texto_cifrado[:-1]

# Função que recebe uma string e devolve um vetor de inteiros
def to_list(linha:str):
    return [int(item) for item in linha.split(' ')]

def decifrar(texto_cifrado:str) -> str:

    vetores = texto_cifrado.split('\n')
    vetores = [to_list(linha) for linha in vetores]

    # Transforma os vetores em matrizes 2x2
    matriz_lista_numeros = [numpy.array([numpy.array(m[:2]), numpy.array(m[2:])]) for m in vetores]
    matriz_lista_numeros = numpy.array(matriz_lista_numeros)

    # Multiplica cada matriz pela chave
    matriz_lista_numeros = [numpy.dot(matriz_chave_inversa,m) for m in matriz_lista_numeros]
    
    # Transforma as matrizes em vetores
    matriz_lista_numeros = [m.flatten() for m in matriz_lista_numeros]

    # Transforma o vetor de vetores em um vetor só
    vetor = []
    for m in matriz_lista_numeros:
        vetor.extend(m)

    # Tranforma os números em inteiros
    vetor = [int(x) for x in vetor]

    texto_decifrado = ''
    for i in vetor:
        texto_decifrado += lista_caracteres[i]

    # Substitui o [ e ] por \n e espaço, ver função cifrar
    texto_decifrado = texto_decifrado.replace('[', '\n')
    texto_decifrado = texto_decifrado.replace(']', ' ')

    # Retorna o texto decifrado
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
        escrever_arquivo(sys.argv[4],decifrar(ler_arquivo(sys.argv[2])))
    else:
        print(sys.argv[3], ' não é um comando reconhecido')
        sys.exit()
else:
    print(sys.argv[1], ' não é um comando reconhecido')
    sys.exit()

# Como compilar
# O comando para cifrar é python cifrahill2.py -enc dir_texto_claro.txt -out dir_texto_enc.txt
# O comando para decifrar é python cifrahill2.py -dec dir_texto_enc.txt -out dir_texto_dect.txt