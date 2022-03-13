def carrega_dicionario(idioma_provavel):

    arquivo_dicionario = open('parte_02/dictionary_en.txt') if idioma_provavel == "en" else open('parte_02/dictionary_pt.txt')
    palavras = {}

    for palavra in arquivo_dicionario.read().split('\n'):
        palavras[palavra.upper()] = None

    arquivo_dicionario.close()
    return palavras

def conta_palavras(texto_decifrado, palavras_ingles):

    texto_decifrado = texto_decifrado.upper()
    texto_decifrado = remove_simbolos(texto_decifrado)
    
    palavras_possiveis = texto_decifrado.split()

    if palavras_possiveis == []:
        return 0.0 # No words at all, so return 0.0.

    combinacoes = 0
    for palavra in palavras_possiveis:
        if palavra in palavras_ingles:
            combinacoes += 1
    return float(combinacoes) / len(palavras_possiveis)

def remove_simbolos(texto_decifrado):
    alfabeto_maiusculo = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    letras_e_espaco = alfabeto_maiusculo + alfabeto_maiusculo.lower() + ' \t\n'

    somente_letras = []
    for simbolo in texto_decifrado:
        if simbolo in letras_e_espaco:
            somente_letras.append(simbolo)
    return ''.join(somente_letras)


def legivel(texto_decifrado, idioma_provavel, porcentagem_palavra=20, porcentagem_letra=85):

    palavras_ingles = carrega_dicionario(idioma_provavel)

    palavras_combinam = (conta_palavras(texto_decifrado, palavras_ingles) * 100) >= (porcentagem_palavra)

    num_letras = len(remove_simbolos(texto_decifrado))

    porcentagem_letras_messagem = float(num_letras) / len(texto_decifrado) * 100
    combinacao_letras = porcentagem_letras_messagem >= porcentagem_letra

    return palavras_combinam and combinacao_letras