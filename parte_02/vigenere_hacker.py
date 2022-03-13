import itertools, re
import freq_analysis, detect_language

NUM_MAX_SUBCHAVES_PONTUADAS = 4 # Define a qtde de pontuações mais frequentes para cada subchave
TAMANHO_MAX_CHAVE = 16 # Define o tamanho máximo de chaves

def encontra_distancia_seq(msg_cifrada):
    # Procura sequencias de 3 a 5 carecteres que se repetem na mensagem.
    # Retorna dicionario contendo as sequencias e uma lista dos valores de espaçamento entre as sequencias

    filtro = re.compile('[^A-Z]')
    msg_cifrada = filtro.sub('', msg_cifrada.upper())

    
    distancia_seq = {} # Dicionario contendo sequencias como chaves e listas de espaçamento como valores
    for tamanho_seq in range(3, 6):
        for inicio_seq in range(len(msg_cifrada) - tamanho_seq):
            seq = msg_cifrada[inicio_seq:inicio_seq + tamanho_seq]
      
            # Procura pela sequencia no resto da mensagem
            for i in range(inicio_seq + tamanho_seq, len(msg_cifrada) - tamanho_seq):
                if msg_cifrada[i:i + tamanho_seq] == seq:
                    if seq not in distancia_seq: # Achou sequencia repetida
                        distancia_seq[seq] = []

                    # Insere o espaçamento entre a sequencia repetida e a sequencia original
                    distancia_seq[seq].append(i - inicio_seq)
    return distancia_seq

def multiplos_uteis(numero):
    # Retorna lista de múltiplos úteis de um número. 
    # São úteis os que são menores que o MÁXIMO TAMANHO DEFINIDO para chaves e os que não são 1.
    
    if numero < 2:
        return []

    multiplos = []

    for i in range(2, TAMANHO_MAX_CHAVE + 1):
        if numero % i == 0: # Testa se i é múltiplo do numero
            multiplos.append(i)
            outro_multiplo = int(numero / i)
            if (outro_multiplo < TAMANHO_MAX_CHAVE + 1) and (outro_multiplo != 1):
                multiplos.append(outro_multiplo)
    return list(set(multiplos)) # Remove múltiplos repetidos

def get_item_1(items):
    return items[1]

def conta_multiplos_frequentes(seq_multiplo):
    # Retorna os múltiplos mais frequentes juntamente com suas quantidades.

    contagem_multiplo = {}

    for seq in seq_multiplo:
        lista_multiplo = seq_multiplo[seq]
        for multiplo in lista_multiplo:
            if multiplo not in contagem_multiplo:
                contagem_multiplo[multiplo] = 0
            contagem_multiplo[multiplo] += 1

    # Insere uma tupla em uma lista contendo os múltiplos e suas quantidades para posterior ordenação.
    contagem_por_multiplo = []
    for multiplo in contagem_multiplo:
        if multiplo <= TAMANHO_MAX_CHAVE:
            contagem_por_multiplo.append( (multiplo, contagem_multiplo[multiplo]) )

    # Ordena lista por quantidade de múltiplos.
    contagem_por_multiplo.sort(key=get_item_1, reverse=True)

    return contagem_por_multiplo

def analise_kasiski(msg_cifrada):
    # Analisa mensagem cifrada e procura por sequencias repetitivas de 3 a 5 caracteres.
    # Retorna lista com espaçamentos mais frequentes e seus múltiplos e portanto tamanhos de chave mais prováveis.
    
    distancia_seq = encontra_distancia_seq(msg_cifrada)

    # Insere os espaçamentos e seus múltiplos para cada sequencia no dicionário.
    seq_multiplo = {}
    for seq in distancia_seq:
        seq_multiplo[seq] = []
        for dist in distancia_seq[seq]:
            seq_multiplo[seq].extend(multiplos_uteis(dist))

    contagem_por_multiplo = conta_multiplos_frequentes(seq_multiplo) # Contém múltiplos/espaçamentos mais frequentes de todas as sequencias possíveis e seus valores, ordenados.

    # Insere somente os múltiplos de forma ordenada em lista de retorno.
    comprimentos_possiveis = []
    for tupla in contagem_por_multiplo:
        comprimentos_possiveis.append(tupla[0])

    return comprimentos_possiveis

def letras_subchave_n(indice_subchave, comprimento_chave, msg_cifrada):
    # Filtra mensagem recebida de modo a compor string com caracteres em posições proporcionais ao índice recebido.
    # Retorna string com letras na posição especificada

    filtro = re.compile('[^A-Z]')
    msg_cifrada = filtro.sub('', msg_cifrada)

    i = indice_subchave - 1 # Define a posição inicial do índice recebido
    letras = []
    while i < len(msg_cifrada):
        letras.append(msg_cifrada[i]) # Insere o caractere na posição do índice na string
        i += comprimento_chave # Incrementa o índice conforme tamanho da chave
    return ''.join(letras)

def quebrar_cifra(msg_cifrada, comprimento_chave, idioma_provavel):
    # Tenta quebrar a cifra através da análise do texto de acordo com o idioma especificado
    # Continua rodando até a cifra seja quebrada ou não seja possível quebrá-la

    alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    msg_cifrada_maiuscula = msg_cifrada.upper()

    # Testa cada uma das letras do alfabeto como subchave de string filtrada nas posições especificadas e armazena a pontuação por frequencia da letra em questão.
    # Após testar cada uma das letras retorna lista de tamanho 'comprimento_chave' contendo em cada posição as subchaves mais pontuadas para aquela posição.
    lista_pontuacao_freq = []
    for indice_subchave in range(1, comprimento_chave + 1):
        letras_posicao_n = letras_subchave_n(indice_subchave, comprimento_chave, msg_cifrada_maiuscula) # Busca a string

        pontuacao_freq = []

        for possivel_subchave in alfabeto:
            msg_decifrada = decifrar_mensagem(possivel_subchave, letras_posicao_n, alfabeto)
            pontuacao_freq_subchave = (possivel_subchave, freq_analysis.pontuacao_por_freq(msg_decifrada, idioma_provavel)) # Busca a pontuação da subchave em questão para a string
            pontuacao_freq.append(pontuacao_freq_subchave) # ['A', 8]

        pontuacao_freq.sort(key=get_item_1, reverse=True) # Ordena subchaves pela pontuação

        lista_pontuacao_freq.append(pontuacao_freq[:NUM_MAX_SUBCHAVES_PONTUADAS]) # Pega somente as 4 (ou x) pontuações mais frequentes para cada subchave
    
    print(f'Lista de pontuação das subchaves por posicao na chave:\n{lista_pontuacao_freq}\n')

    # Utiliza 'itertools' para gerar todos os índices possíveis na geração de chaves de tamanho 'comprimento_chave'.
    for indices in itertools.product(range(NUM_MAX_SUBCHAVES_PONTUADAS), repeat=comprimento_chave):

        possivel_chave = ''
        
        # Pega os indices gerados e coleta as subchaves correspondente na lista de subchaves com maior pontuação.
        for i in range(comprimento_chave):
            possivel_chave += lista_pontuacao_freq[i][indices[i]][0]

        print('Possível chave: %s' % (possivel_chave))

        texto_decifrado = decifrar_mensagem(possivel_chave, msg_cifrada_maiuscula, alfabeto)

        # Analisa legibilidade da mensagem decifrada de acordo com idioma definido
        # Uso opcional, porém irá imprimir todas as possibilidades de decifração
        if detect_language.legivel(texto_decifrado, idioma_provavel):

            print(f'\nTexto decifrado com a chave "{possivel_chave}":\n')
            print(texto_decifrado)

            print(f'\nEstá correto? Aperte S para sim e N para não [S/N]')
            response = input('> ')

            if response.strip().upper().startswith('S'):
                return texto_decifrado

    # Retorna None se não foi possível decifrar a mensagem
    return None

def decifrador_vigenere(msg_cifrada, idioma_provavel): 
    lista_de_comprimentos = analise_kasiski(msg_cifrada) # Retorna a lista de comprimentos possiveis que a chave pode ter ordenada por frequencia

    print(f"\nPossíveis comprimentos de chave, segundo Kasiski: {lista_de_comprimentos}")
    
    msg_decifrada = None

    for comprimento in lista_de_comprimentos:
        print(f"\nTentando hackear com comprimento de chave {comprimento}\n")

        msg_decifrada = quebrar_cifra(msg_cifrada, comprimento, idioma_provavel)

        if msg_decifrada != None:
            break


    return msg_decifrada

def decifrar_mensagem(chave, mensagem, alfabeto):
    palavra_cifrada = []  # Definição do vetor com palavra cifrada

    indice_chave = 0  # Armazenamento do valor atual do índice da chave

    for caractere in mensagem:
        if caractere in alfabeto:  # Verificar se o caracter está no alfabeto para ser cifrado
            num_caractere_cifrado = (alfabeto.index(caractere) - alfabeto.index(chave[indice_chave])) % len(alfabeto)  # Se estiver, busca o indice e soma ao indice correspondente da chave módulo tamanho do alfabeto
            caractere_cifrado = alfabeto[num_caractere_cifrado]  # Transforma indice em caratere cifrado
            palavra_cifrada.append(caractere_cifrado)  # Insere caractere no vetor de palavra cifrada
            indice_chave = (indice_chave + 1) % len(chave)  # Atualiza o indice atual da chave
        else:
            palavra_cifrada.append(caractere)

    return ''.join(palavra_cifrada)

def main():

    nome_arquivo = input('Digite o nome do arquivo: ')
    idioma_provavel = input('Digite o provável idioma: ')

    caminho_arquivo = 'parte_02/' + nome_arquivo + '.txt' 

    f = open(caminho_arquivo, "r", encoding="utf8")
    msg_cifrada = f.read()

    print(msg_cifrada)

    msg_decifrada = decifrador_vigenere(msg_cifrada, idioma_provavel)

    if msg_decifrada == None:
        print('Failed to hack encryption.')

# If vigenereHacker.py is run (instead of imported as a module) call
# the main() function.
if __name__ == '__main__':
    main()