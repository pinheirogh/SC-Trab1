def cifrar_mensagem(mensagem, chave, alfabeto):
    palavra_cifrada = []  # Definição do vetor com palavra cifrada

    indice_chave = 0  # Armazenamento do valor atual do índice da chave

    for caractere in mensagem:
        if caractere in alfabeto:  # Verificar se o caracter está no alfabeto para ser cifrado
            num_caractere_cifrado = (alfabeto.index(caractere) + alfabeto.index(chave[indice_chave])) % len(alfabeto)  # Se estiver, busca o indice e soma ao indice correspondente da chave módulo tamanho do alfabeto
            caractere_cifrado = alfabeto[num_caractere_cifrado]  # Transforma indice em caratere cifrado
            palavra_cifrada.append(caractere_cifrado)  # Insere caractere no vetor de palavra cifrada
            indice_chave = (indice_chave + 1) % len(chave)  # Atualiza o indice atual da chave
        else:
            palavra_cifrada.append(caractere)

    return ''.join(palavra_cifrada)

def decifrar_mensagem(mensagem, chave, alfabeto):
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
    alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    # Receber valores do terminal
    nome_arquivo = input('Digite o nome do arquivo: ')
    chave = input('Digite a chave: ').upper()

    caminho_arquivo = 'parte_02/' + nome_arquivo + '.txt' 

    f = open(caminho_arquivo, "r", encoding="utf8")
    mensagem = f.read().upper()

    print(mensagem)

    # Selecionar operação
    print('\n1 - Cifrar')
    print('2 - Decifrar')
    operacao = int(input('\nDigite a operação: '))

    # Redirecionar valores para função correspondente
    if operacao == 1:
        resultado = cifrar_mensagem(mensagem, chave, alfabeto)
        print(f'\nMensagem cifrada: {resultado}')
    elif operacao == 2:
        resultado = decifrar_mensagem(mensagem, chave, alfabeto)
        print(f'\nMensagem decifrada: {resultado}')


if __name__ == "__main__":
    main()