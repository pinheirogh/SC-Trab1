def cifrar_mensagem(mensagem, chave):
    palavra_cifrada = []  # Definição do vetor com palavra cifrada

    indice_chave = 0  # Armazenamento do valor atual do índice da chave

    for caractere in mensagem:
        if caractere in ALFABETO:  # Verificar se o caracter está no alfabeto para ser cifrado
            num_caractere_cifrado = (ALFABETO.index(caractere) + ALFABETO.index(chave[indice_chave])) % len(ALFABETO)  # Se estiver, busca o indice e soma ao indice correspondente da chave módulo tamanho do alfabeto
            caractere_cifrado = ALFABETO[num_caractere_cifrado]  # Transforma indice em caratere cifrado
            palavra_cifrada.append(caractere_cifrado)  # Insere caractere no vetor de palavra cifrada
            indice_chave = (indice_chave + 1) % len(chave)  # Atualiza o indice atual da chave
        else:
            palavra_cifrada.append(caractere)

    return ''.join(palavra_cifrada)

def decifrar_mensagem(mensagem, chave):
    palavra_cifrada = []  # Definição do vetor com palavra cifrada

    indice_chave = 0  # Armazenamento do valor atual do índice da chave

    for caractere in mensagem:
        if caractere in ALFABETO:  # Verificar se o caracter está no alfabeto para ser cifrado
            num_caractere_cifrado = (ALFABETO.index(caractere) - ALFABETO.index(chave[indice_chave])) % len(ALFABETO)  # Se estiver, busca o indice e soma ao indice correspondente da chave módulo tamanho do alfabeto
            caractere_cifrado = ALFABETO[num_caractere_cifrado]  # Transforma indice em caratere cifrado
            palavra_cifrada.append(caractere_cifrado)  # Insere caractere no vetor de palavra cifrada
            indice_chave = (indice_chave + 1) % len(chave)  # Atualiza o indice atual da chave
        else:
            palavra_cifrada.append(caractere)

    return ''.join(palavra_cifrada)


ALFABETO = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Receber valores do terminal
mensagem = input('Digite a mensagem: ').upper()
chave = input('Digite a chave: ').upper()

# Selecionar operação
print()
print('1 - Cifrar')
print('2 - Decifrar')
operacao = int(input('Digite a operação: '))

# Redirecionar valores para função correspondente
if operacao == 1:
    resultado = cifrar_mensagem(mensagem, chave)
    print()
    print(f'Mensagem cifrada: {resultado}')
elif operacao == 2:
    resultado = decifrar_mensagem(mensagem, chave)
    print()
    print(f'Mensagem decifrada: {resultado}')
