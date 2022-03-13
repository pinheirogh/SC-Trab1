import itertools, re
import freq_analysis, detect_language

NUM_MOST_FREQ_LETTERS = 4 # Attempt this many letters per subkey.
MAX_KEY_LENGTH = 16 # Will not attempt keys longer than this.

def encontra_distancia_seq(msg_cifrada):
    # Goes through the message and finds any 3 to 5 letter sequences
    # that are repeated. Returns a dict with the keys of the sequence and
    # values of a list of spacings (num of letters between the repeats).

    # Use a regular expression to remove non-letters from the message:
    filtro = re.compile('[^A-Z]')
    msg_cifrada = filtro.sub('', msg_cifrada.upper())

    # Compile a list of seqLen-letter sequences found in the message:
    distancia_seq = {} # Keys are sequences, values are lists of int spacings.
    for tamanho_seq in range(3, 6):
        for inicio_seq in range(len(msg_cifrada) - tamanho_seq):
            # Determine what the sequence is, and store it in seq:
            seq = msg_cifrada[inicio_seq:inicio_seq + tamanho_seq]

            # Look for this sequence in the rest of the message:
            for i in range(inicio_seq + tamanho_seq, len(msg_cifrada) - tamanho_seq):
                if msg_cifrada[i:i + tamanho_seq] == seq:
                    # Found a repeated sequence.
                    if seq not in distancia_seq:
                        distancia_seq[seq] = [] # Initialize a blank list.

                    # Append the spacing distance between the repeated
                    # sequence and the original sequence:
                    distancia_seq[seq].append(i - inicio_seq)
    return distancia_seq

def multiplos_uteis(numero):
    # Returns a list of useful factors of num. By "useful" we mean factors
    # less than MAX_KEY_LENGTH + 1 and not 1. For example,
    # multiplos_uteis(144) returns [2, 3, 4, 6, 8, 9, 12, 16]

    if numero < 2:
        return [] # Numbers less than 2 have no useful factors.

    multiplos = [] # The list of factors found.

    # When finding factors, you only need to check the integers up to
    # MAX_KEY_LENGTH.
    for i in range(2, MAX_KEY_LENGTH + 1): # Don't test 1: it's not useful.
        if numero % i == 0: #se for par
            multiplos.append(i)
            outro_multiplo = int(numero / i)
            if (outro_multiplo < MAX_KEY_LENGTH + 1) and (outro_multiplo != 1):
                multiplos.append(outro_multiplo)
    return list(set(multiplos)) # Remove duplicate factors.

def get_item_1(items):
    return items[1]

def conta_multiplos_frequentes(seq_multiplo):
    # First, get a count of how many times a factor occurs in seqFactors:
    contagem_multiplo = {} # Key is a factor, value is how often it occurs.

    # seqFactors keys are sequences, values are lists of factors of the
    # spacings. seqFactors has a value like: {'GFD': [2, 3, 4, 6, 9, 12,
    # 18, 23, 36, 46, 69, 92, 138, 207], 'ALW': [2, 3, 4, 6, ...], ...}
    for seq in seq_multiplo:
        lista_multiplo = seq_multiplo[seq]
        for multiplo in lista_multiplo:
            if multiplo not in contagem_multiplo:
                contagem_multiplo[multiplo] = 0
            contagem_multiplo[multiplo] += 1

    # Second, put the factor and its count into a tuple, and make a list
    # of these tuples so we can sort them:
    contagem_por_multiplo = []
    for multiplo in contagem_multiplo:
        # Exclude factors larger than MAX_KEY_LENGTH:
        if multiplo <= MAX_KEY_LENGTH:
            # factorsByCount is a list of tuples: (factor, factorCount)
            # factorsByCount has a value like: [(3, 497), (2, 487), ...]
            contagem_por_multiplo.append( (multiplo, contagem_multiplo[multiplo]) )

    # Sort the list by the factor count:
    contagem_por_multiplo.sort(key=get_item_1, reverse=True)

    return contagem_por_multiplo

def analise_kasiski(msg_cifrada):
    # Find out the sequences of 3 to 5 letters that occur multiple times
    # in the msg_cifrada. repeatedSeqSpacings has a value like:
    # {'EXG': [192], 'NAF': [339, 972, 633], ... }
    distancia_seq = encontra_distancia_seq(msg_cifrada)

    # (See conta_multiplos_frequentes() for a description of seqFactors.)
    seq_multiplo = {}
    for seq in distancia_seq:
        seq_multiplo[seq] = []
        for dist in distancia_seq[seq]:
            seq_multiplo[seq].extend(multiplos_uteis(dist))

    # (See conta_multiplos_frequentes() for a description of factorsByCount.)
    contagem_por_multiplo = conta_multiplos_frequentes(seq_multiplo)

    # Now we extract the factor counts from factorsByCount and
    # put them in lista_de_comprimentos so that they are easier to
    # use later:
    comprimentos_possiveis = []
    for tupla in contagem_por_multiplo:
        comprimentos_possiveis.append(tupla[0])

    return comprimentos_possiveis

def letras_subchave_n(sub_chave, comprimento_chave, msg_cifrada):
    # Returns every nth letter for each keyLength set of letters in text.
    # E.g. letras_subchave_n(1, 3, 'ABCABCABC') returns 'AAA'
    #      letras_subchave_n(2, 3, 'ABCABCABC') returns 'BBB'
    #      letras_subchave_n(3, 3, 'ABCABCABC') returns 'CCC'
    #      letras_subchave_n(1, 5, 'ABCDEFGHI') returns 'AF'

    # Use a regular expression to remove non-letters from the message:
    filtro = re.compile('[^A-Z]')
    msg_cifrada = filtro.sub('', msg_cifrada)

    i = sub_chave - 1
    letras = []
    while i < len(msg_cifrada):
        letras.append(msg_cifrada[i])
        i += comprimento_chave
    return ''.join(letras)

def quebra_cifra(msg_cifrada, comprimento, idioma_provavel):
    alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # Determine the most likely letters for each letter in the key:
    msg_cifrada_maiuscula = msg_cifrada.upper()
    # allFreqScores is a list of mostLikelyKeyLength number of lists.
    # These inner lists are the freqScores lists.
    lista_pontuacao_freq = []
    for sub_chave in range(1, comprimento + 1):
        letras = letras_subchave_n(sub_chave, comprimento, msg_cifrada_maiuscula)

        pontuacao_freq = []

        for possivel_subchave in alfabeto:
            msg_decifrada = decifrar_mensagem(possivel_subchave, letras, alfabeto)
            qtd_possivel_chave = (possivel_subchave, freq_analysis.pontuacao_freq(msg_decifrada, idioma_provavel))
            pontuacao_freq.append(qtd_possivel_chave)

        pontuacao_freq.sort(key=get_item_1, reverse=True)

        lista_pontuacao_freq.append(pontuacao_freq[:NUM_MOST_FREQ_LETTERS])

    # Try every combination of the most likely letters for each position
    # in the key:
    for indices in itertools.product(range(NUM_MOST_FREQ_LETTERS), repeat=comprimento):

        # Create a possible key from the letters in allFreqScores:
        possivel_chave = ''
        for i in range(comprimento):
            possivel_chave += lista_pontuacao_freq[i][indices[i]][0]

        print('Possível chave: %s' % (possivel_chave))

        texto_decifrado = decifrar_mensagem(possivel_chave, msg_cifrada_maiuscula, alfabeto)

        if detect_language.legivel(texto_decifrado, idioma_provavel):

            # Check with user to see if the key has been found:
            print(f'\nTexto decifrado com a chave "{possivel_chave}":\n')
            print(texto_decifrado)

            print(f'\nEstá correto? Aperte S para sim e N para não [S/N]')
            response = input('> ')

            if response.strip().upper().startswith('S'):
                return texto_decifrado

    # No English-looking decryption found, so return None:
    return None

def decifrador_vigenere(msg_cifrada, idioma_provavel): 
    lista_de_comprimentos = analise_kasiski(msg_cifrada) # Retorna a lista de comprimentos possiveis que a chave pode ter

    print(f"\nComprimentos possíveis da chave: {lista_de_comprimentos}")
    
    msg_decifrada = None

    for comprimento in lista_de_comprimentos:
        print(f"Tentando hackear com comprimento de chave {comprimento}\n")

        msg_decifrada = quebra_cifra(msg_cifrada, comprimento, idioma_provavel)

        if msg_decifrada != None:
            break

    # If none of the key lengths we found using Kasiski Examination
    # worked, start brute-forcing through key lengths:
    # if msg_decifrada == None:
    #     print('Unable to hack message with likely key length(s). Brute forcing key length...')
    #     for comprimento_chave in range(1, MAX_KEY_LENGTH + 1):
    #         # Don't re-check key lengths already tried from Kasiski:
    #         if comprimento_chave not in lista_de_comprimentos:
    #             print(f"Attempting hack with key length {comprimento_chave} ({NUM_MOST_FREQ_LETTERS ** comprimento_chave} possible keys)...")
    #             msg_decifrada = quebra_cifra(msg_cifrada, comprimento_chave)
    #             if msg_decifrada != None:
    #                 break


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

    msg_cifrada = input('Digite a mensagem: ')
    idioma_provavel = input('Digite o provável idioma: ')

    with open("parte_02/desafio2.txt") as f:
        msg_cifrada = f.read()

    msg_decifrada = decifrador_vigenere(msg_cifrada, idioma_provavel)

    if msg_decifrada == None:
        print('Failed to hack encryption.')

# If vigenereHacker.py is run (instead of imported as a module) call
# the main() function.
if __name__ == '__main__':
    main()