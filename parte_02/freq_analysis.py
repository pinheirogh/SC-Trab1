def contagem_letras(msg_decifrada):
    alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # Returns a dictionary with keys of single ALFABETO and values of the count of how many times they appear in the message parameter:
    cont_letras = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0, 'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0}

    for letras in msg_decifrada.upper():
        if letras in alfabeto:
            cont_letras[letras] += 1

    return cont_letras

def get_item_0(items):
    return items[0]

def get_ordem_freq(msg_decifrada, freq_por_lingua):
    alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # Returns a string of the alphabet ALFABETO arranged in order of most frequently occurring in the message parameter.

    # First, get a dictionary of each letter and its frequency count:
    freq_letras = contagem_letras(msg_decifrada)

    # Second, make a dictionary of each frequency count to each letter(s)
    # with that frequency:
    freq_por_letra = {}
    for letra in alfabeto:
        if freq_letras[letra] not in freq_por_letra:
            freq_por_letra[freq_letras[letra]] = [letra]
        else:
            freq_por_letra[freq_letras[letra]].append(letra)

    # Third, put each list of ALFABETO in reverse "ETAOIN" order, and then
    # convert it to a string:
    for freq in freq_por_letra:
        freq_por_letra[freq].sort(key=freq_por_lingua.find, reverse=True)
        freq_por_letra[freq] = ''.join(freq_por_letra[freq])

    # Fourth, convert the freqToLetter dictionary to a list of
    # tuple pairs (key, value), then sort them:
    pares_freq = list(freq_por_letra.items())
    pares_freq.sort(key=get_item_0, reverse=True)

    # Fifth, now that the ALFABETO are ordered by frequency, extract all
    # the ALFABETO for the final string:
    ordem_freq = []
    for freqPair in pares_freq:
        ordem_freq.append(freqPair[1])

    return ''.join(ordem_freq)

def pontuacao_freq(msg_decifrada, idioma_provavel="en"):

    freq_por_lingua = 'AEOSRINDMUTCLPVGHQBFZJXKWY' if idioma_provavel == "pt" else 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
    ordem_freq = get_ordem_freq(msg_decifrada, freq_por_lingua)

    pontuacao = 0
    # Find how many matches for the six most common ALFABETO there are:
    for letras_mais_freq in freq_por_lingua[:6]:
        if letras_mais_freq in ordem_freq[:6]:
            pontuacao += 1
    # Find how many matches for the six least common ALFABETO there are:
    for letras_menos_freq in freq_por_lingua[-6:]:
        if letras_menos_freq in ordem_freq[-6:]:
            pontuacao += 1

    return pontuacao