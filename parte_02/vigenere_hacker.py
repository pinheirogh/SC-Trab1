# Vigenere Cipher Hacker
# https://www.nostarch.com/crackingcodes/ (BSD Licensed)

import itertools, re
import vigenere_cipher, freq_analysis, detect_english

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
SILENT_MODE = False # If set to True, program doesn't print anything.
NUM_MOST_FREQ_LETTERS = 4 # Attempt this many letters per subkey.
MAX_KEY_LENGTH = 16 # Will not attempt keys longer than this.
NONLETTERS_PATTERN = re.compile('[^A-Z]')

def main():
    with open("parte_02/desafio1.txt") as f:
        content = f.read()

    msg_cifrada = content
    msg_decifrada = decifrador_vigenere(msg_cifrada)

    if msg_decifrada != None:
        print('Copying hacked message to clipboard:')
        print(msg_decifrada)
    else:
        print('Failed to hack encryption.')

def findRepeatSequencesSpacings(message):
    # Goes through the message and finds any 3 to 5 letter sequences
    # that are repeated. Returns a dict with the keys of the sequence and
    # values of a list of spacings (num of letters between the repeats).

    # Use a regular expression to remove non-letters from the message:
    message = NONLETTERS_PATTERN.sub('', message.upper())

    # Compile a list of seqLen-letter sequences found in the message:
    seqSpacings = {} # Keys are sequences, values are lists of int spacings.
    for seqLen in range(3, 6):
        for seqStart in range(len(message) - seqLen):
            # Determine what the sequence is, and store it in seq:
            seq = message[seqStart:seqStart + seqLen]

            # Look for this sequence in the rest of the message:
            for i in range(seqStart + seqLen, len(message) - seqLen):
                if message[i:i + seqLen] == seq:
                    # Found a repeated sequence.
                    if seq not in seqSpacings:
                        seqSpacings[seq] = [] # Initialize a blank list.

                    # Append the spacing distance between the repeated
                    # sequence and the original sequence:
                    seqSpacings[seq].append(i - seqStart)
    return seqSpacings

def getUsefulFactors(num):
    # Returns a list of useful factors of num. By "useful" we mean factors
    # less than MAX_KEY_LENGTH + 1 and not 1. For example,
    # getUsefulFactors(144) returns [2, 3, 4, 6, 8, 9, 12, 16]

    if num < 2:
        return [] # Numbers less than 2 have no useful factors.

    factors = [] # The list of factors found.

    # When finding factors, you only need to check the integers up to
    # MAX_KEY_LENGTH.
    for i in range(2, MAX_KEY_LENGTH + 1): # Don't test 1: it's not useful.
        if num % i == 0:
            factors.append(i)
            otherFactor = int(num / i)
            if otherFactor < MAX_KEY_LENGTH + 1 and otherFactor != 1:
                factors.append(otherFactor)
    return list(set(factors)) # Remove duplicate factors.

def getItemAtIndexOne(items):
    return items[1]

def getMostCommonFactors(seqFactors):
    # First, get a count of how many times a factor occurs in seqFactors:
    factorCounts = {} # Key is a factor, value is how often it occurs.

    # seqFactors keys are sequences, values are lists of factors of the
    # spacings. seqFactors has a value like: {'GFD': [2, 3, 4, 6, 9, 12,
    # 18, 23, 36, 46, 69, 92, 138, 207], 'ALW': [2, 3, 4, 6, ...], ...}
    for seq in seqFactors:
        factorList = seqFactors[seq]
        for factor in factorList:
            if factor not in factorCounts:
                factorCounts[factor] = 0
            factorCounts[factor] += 1

    # Second, put the factor and its count into a tuple, and make a list
    # of these tuples so we can sort them:
    factorsByCount = []
    for factor in factorCounts:
        # Exclude factors larger than MAX_KEY_LENGTH:
        if factor <= MAX_KEY_LENGTH:
            # factorsByCount is a list of tuples: (factor, factorCount)
            # factorsByCount has a value like: [(3, 497), (2, 487), ...]
            factorsByCount.append( (factor, factorCounts[factor]) )

    # Sort the list by the factor count:
    factorsByCount.sort(key=getItemAtIndexOne, reverse=True)

    return factorsByCount

def kasiskiExamination(msg_cifrada):
    # Find out the sequences of 3 to 5 letters that occur multiple times
    # in the msg_cifrada. repeatedSeqSpacings has a value like:
    # {'EXG': [192], 'NAF': [339, 972, 633], ... }
    repeatedSeqSpacings = findRepeatSequencesSpacings(msg_cifrada)

    # (See getMostCommonFactors() for a description of seqFactors.)
    seqFactors = {}
    for seq in repeatedSeqSpacings:
        seqFactors[seq] = []
        for spacing in repeatedSeqSpacings[seq]:
            seqFactors[seq].extend(getUsefulFactors(spacing))

    # (See getMostCommonFactors() for a description of factorsByCount.)
    factorsByCount = getMostCommonFactors(seqFactors)

    # Now we extract the factor counts from factorsByCount and
    # put them in lista_de_comprimentos so that they are easier to
    # use later:
    lista_de_comprimentos = []
    for twoIntTuple in factorsByCount:
        lista_de_comprimentos.append(twoIntTuple[0])

    return lista_de_comprimentos

def getNthSubkeysLetters(repeticao, comprimento_chave, msg_cifrada):
    # Returns every nth letter for each keyLength set of letters in text.
    # E.g. getNthSubkeysLetters(1, 3, 'ABCABCABC') returns 'AAA'
    #      getNthSubkeysLetters(2, 3, 'ABCABCABC') returns 'BBB'
    #      getNthSubkeysLetters(3, 3, 'ABCABCABC') returns 'CCC'
    #      getNthSubkeysLetters(1, 5, 'ABCDEFGHI') returns 'AF'

    # Use a regular expression to remove non-letters from the message:
    msg_cifrada = NONLETTERS_PATTERN.sub('', msg_cifrada)

    i = repeticao - 1
    letras = []
    while i < len(msg_cifrada):
        letras.append(msg_cifrada[i])
        i += comprimento_chave
    return ''.join(letras)

def attemptHackWithKeyLength(msg_cifrada, comprimento_chave_provavel):
    # Determine the most likely letters for each letter in the key:
    msg_cifrada_maiuscula = msg_cifrada.upper()
    # allFreqScores is a list of mostLikelyKeyLength number of lists.
    # These inner lists are the freqScores lists.
    pontuacoes_freq = []
    for repeticao in range(1, comprimento_chave_provavel + 1):
        letras_repetidas = getNthSubkeysLetters(repeticao, comprimento_chave_provavel, msg_cifrada_maiuscula)

        # freqScores is a list of tuples like:
        # [(<letter>, <Eng. Freq. match score>), ... ]
        # List is sorted by match score. Higher score means better match.
        # See the englishFreqMatchScore() comments in freq_analysis.py.
        pontuacao_freq = []

        for possivel_chave in LETTERS:
            msg_decifrada = vigenere_cipher.decryptMessage(possivel_chave, letras_repetidas)
            qtd_possivel_chave = (possivel_chave, freq_analysis.englishFreqMatchScore(msg_decifrada))
            pontuacao_freq.append(qtd_possivel_chave)
        # Sort by match score:
        pontuacao_freq.sort(key=getItemAtIndexOne, reverse=True)

        pontuacoes_freq.append(pontuacao_freq[:NUM_MOST_FREQ_LETTERS])

    for i in range(len(pontuacoes_freq)):
        # Use i + 1 so the first letter is not called the "0th" letter:
        print('Possible letters for letter %s of the key: ' % (i + 1), end='')
        for freqScore in pontuacoes_freq[i]:
            print('%s ' % freqScore[0], end='')
        print() # Print a newline.

    # Try every combination of the most likely letters for each position
    # in the key:
    for indexes in itertools.product(range(NUM_MOST_FREQ_LETTERS), repeat=comprimento_chave_provavel):
        # Create a possible key from the letters in allFreqScores:
        possibleKey = ''
        for i in range(comprimento_chave_provavel):
            possibleKey += pontuacoes_freq[i][indexes[i]][0]

        if not SILENT_MODE:
            print('Attempting with key: %s' % (possibleKey))

        decryptedText = vigenere_cipher.decryptMessage(possibleKey, msg_cifrada_maiuscula)

        if detect_english.isEnglish(decryptedText):
            # Set the hacked msg_cifrada to the original casing:
            origCase = []
            for i in range(len(msg_cifrada)):
                if msg_cifrada[i].isupper():
                    origCase.append(decryptedText[i].upper())
                else:
                    origCase.append(decryptedText[i].lower())
            decryptedText = ''.join(origCase)

            # Check with user to see if the key has been found:
            print('Possible encryption hack with key %s:' % (possibleKey))
            print(decryptedText[:200]) # Only show first 200 characters.
            print('\nEnter D if done, anything else to continue hacking:')
            response = input('> ')

            if response.strip().upper().startswith('D'):
                return decryptedText

    # No English-looking decryption found, so return None:
    return None

def decifrador_vigenere(msg_cifrada):
    lista_de_comprimentos = kasiskiExamination(msg_cifrada) # Retorna a lista de comprimentos possiveis que a chave pode ter

    print("Kasiski Examination results say the most likely key lengths are: {lista_de_comprimentos}\n")
    
    msg_decifrada = None

    for comprimento in lista_de_comprimentos:
        print(f"Attempting hack with key length {comprimento} ({NUM_MOST_FREQ_LETTERS ** comprimento} possible keys)...")

        msg_decifrada = attemptHackWithKeyLength(msg_cifrada, comprimento)
        if msg_decifrada != None:
            break

    # If none of the key lengths we found using Kasiski Examination
    # worked, start brute-forcing through key lengths:
    if msg_decifrada == None:
        print('Unable to hack message with likely key length(s). Brute forcing key length...')
        for comprimento_chave in range(1, MAX_KEY_LENGTH + 1):
            # Don't re-check key lengths already tried from Kasiski:
            if comprimento_chave not in lista_de_comprimentos:
                print(f"Attempting hack with key length {comprimento_chave} ({NUM_MOST_FREQ_LETTERS ** comprimento_chave} possible keys)...")
                msg_decifrada = attemptHackWithKeyLength(msg_cifrada, comprimento_chave)
                if msg_decifrada != None:
                    break
    return msg_decifrada


# If vigenereHacker.py is run (instead of imported as a module) call
# the main() function.
if __name__ == '__main__':
    main()