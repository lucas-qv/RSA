import random
import unittest
import json
from socket import *
import json
import time

# Funções RSA

def mdc(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def inverso_modular(e, phi_n):
    x1, x2, x3 = 1, 0, e
    y1, y2, y3 = 0, 1, phi_n

    while y3 != 0:
        q = x3 // y3
        t1, t2, t3 = x1 - q * y1, x2 - q * y2, x3 - q * y3
        x1, x2, x3 = y1, y2, y3
        y1, y2, y3 = t1, t2, t3

    if x1 < 0:
        x1 += phi_n
    return x1

def eh_primo(n, k=40):
    if n == 2 or n == 3:
        return True
    if n % 2 == 0 or n == 1:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2

    iteracoes = 0  # Variável para contar as iterações
    inicio = time.time()  # Captura o tempo de início

    for _ in range(k):
        print(f"Verificando se {n} é primo, iteração {_ + 1}")
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            iteracoes += 1
            print(f"Continuando iteração {_ + 1}: x = {x}")
            continue
        for j in range(r - 1):
            x = pow(x, 2, n)
            print(f"Iteração {j + 1} no loop interno para número {n}: x = {x}")
            if x == n - 1:
                break
        else:
            return False
        iteracoes += 1

    fim = time.time()  # Captura o tempo de fim
    print(f"Total de iterações: {iteracoes}")
    print(f"Tempo total: {fim - inicio:.6f} segundos")
    return True

def RetornaN(p, q):
    if not (eh_primo(p) and eh_primo(q)):
        raise ValueError('Ambos os números devem ser primos.')
    elif p == q:
        raise ValueError('Os números primos devem ser diferentes.')
    N = p * q
    return N

def RetornaTotiente(p, q):
    return (p - 1) * (q - 1)

def retornaE(phi_n):
    e = random.randrange(1, phi_n)
    while mdc(e, phi_n) != 1:
        e = random.randrange(1, phi_n)
    return e

def retornaD(e, phi_n):
    return inverso_modular(e, phi_n)

def criptografar(chave_publica, mensagem):
    e, N = chave_publica
    print(f"\n\nCriptografando com chave pública (e={e}, N={N})")
    criptografado = []
    for i, char in enumerate(mensagem):
        codificado = ord(char)
        criptografado_char = pow(codificado, e, N)
        print(f"Caracter {i+1} ('{char}') -> codificado para {codificado}, criptografado para {criptografado_char}")
        criptografado.append(criptografado_char)
    return criptografado

def decriptografar(chave_privada, criptografado):
    d, N = chave_privada
    print(f"\n\nDecriptografando com chave privada (d={d}, N={N})")
    decriptografado = []
    for i, char in enumerate(criptografado):
        decriptografado_char = pow(char, d, N)
        print(f"Valor {i+1} ({char}) decriptografado para {decriptografado_char} -> '{chr(decriptografado_char)}'")
        decriptografado.append(chr(decriptografado_char))
    return ''.join(decriptografado)

if __name__ == '__main__':
    # Executa os testes unitários sem sair após a conclusão dos testes
    # unittest.main(exit=False)

    # Exemplo de uso fora dos testes
    p = 2**4253-1
    q = 2**4423-1
    
    N = RetornaN(p, q)
    phi_n = RetornaTotiente(p, q)
    e = retornaE(phi_n)
    d = retornaD(e, phi_n)
    
    chave_publica = {'e': e, 'N': N}
    chave_privada = (d, N)

    print("chave pública server: ", chave_publica)
    
    print("chave privada server: " ,chave_privada)

    
    serverPort = 1300
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(("", serverPort))
    serverSocket.listen(5)
    print("TCP Server\n")
    
    try:
        # Aceita a conexão do cliente
        connectionSocket, addr = serverSocket.accept()
        print("Conexão aceita de:", addr)
        
        # Recebe a chave pública do cliente
        chave_publica_client_json = connectionSocket.recv(1000000000).decode('utf-8')
        chave_publica_client = json.loads(chave_publica_client_json)       
        chave_publica_client = (chave_publica_client['e'], chave_publica_client['N'])

        print("\n\nChave pública client:", chave_publica_client)
        
      
        # Envia a chave pública do servidor para o cliente
        chave_publica_json = json.dumps(chave_publica)
        connectionSocket.send(chave_publica_json.encode('utf-8'))
        
        # Recebe a mensagem criptografada do cliente
        modifiedSentence = connectionSocket.recv(1000000000)
        mensagem_criptografada_recebida = json.loads(modifiedSentence.decode('utf-8'))
        print("\n\nMensagem Criptografada Recebida:", mensagem_criptografada_recebida)
        
        # Descriptografa a mensagem
        mensagem_decriptografada = decriptografar(chave_privada, mensagem_criptografada_recebida)
        print("\n\nMensagem Decriptografada:", mensagem_decriptografada)
        
        # Processa a mensagem
        mensagem_decriptografadaUpper = mensagem_decriptografada.upper()
        
        # Criptografa a mensagem para o cliente
        mensagem_criptografada_enviada = criptografar(chave_publica_client, mensagem_decriptografadaUpper)
        print("\n\nMensagem Criptografada Enviada:", mensagem_criptografada_enviada)
        
        # Envia a mensagem criptografada de volta para o cliente
        mensagem_criptografada_enviada_json = json.dumps(mensagem_criptografada_enviada)
        connectionSocket.send(mensagem_criptografada_enviada_json.encode('utf-8'))
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        connectionSocket.close()
        serverSocket.close()