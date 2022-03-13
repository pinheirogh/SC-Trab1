def carrega_dicionario(idioma_provavel):

    arquivo_dicionario = open('parte_02/dictionary_en.txt') if idioma_provavel == "en" else open('parte_02/dictionary_pt.txt')
    palavras = {}

    for palavra in arquivo_dicionario.read().split('\n'):
        palavras[palavra.upper()] = None

    arquivo_dicionario.close()
    return palavras

def conta_palavras(texto_decifrado, palavras_idioma):
    # Retorna fração de porcentagem entre as palavras do texto decifrado e as palavras do idioma

    texto_decifrado = texto_decifrado.upper()
    texto_decifrado = remove_simbolos(texto_decifrado)
    
    palavras_possiveis = texto_decifrado.split()

    if palavras_possiveis == []:
        return 0.0 # No words at all, so return 0.0.

    combinacoes = 0
    for palavra in palavras_possiveis:
        if palavra in palavras_idioma:
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
    # Analise porcentagem de palavras do texto correspondentes a palavras reais do idioma escolhido

    palavras_idioma = carrega_dicionario(idioma_provavel)

    palavras_combinam = (conta_palavras(texto_decifrado, palavras_idioma) * 100) >= (porcentagem_palavra) # True se porcentagem de palavras iguais é maior ou igual a 20% 

    num_letras = len(remove_simbolos(texto_decifrado))
    porcentagem_letras_mensagem = float(num_letras) / len(texto_decifrado) * 100
    combinacao_letras = porcentagem_letras_mensagem >= porcentagem_letra # True se porcentagem de letras na mensagem é maior que 85%

    return palavras_combinam and combinacao_letras