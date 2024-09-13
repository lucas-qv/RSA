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
 
# Testes unitários
class TestRSA(unittest.TestCase):
    def test_mdc(self):
        # Testa a função mdc para garantir que está calculando corretamente.
        self.assertEqual(mdc(3, 20), 1)
        self.assertEqual(mdc(12, 15), 3)
 
    def test_inverso_modular(self):
        # Testa a função inverso_modular para garantir que retorna o valor correto de `d`.
        self.assertEqual(inverso_modular(3, 20), 7)  # 3 * 7 mod 20 = 1
        self.assertEqual(inverso_modular(7, 40), 23)  # 7 * 23 mod 40 = 1
 
    def test_eh_primo(self):
        # Testa a função eh_primo para garantir que identifica corretamente números primos.
        self.assertTrue(eh_primo(3))
        self.assertTrue(eh_primo(11))
        self.assertFalse(eh_primo(4))
 
    def test_criptografar_decriptografar(self):
        p = 3
        q = 11
        N = RetornaN(p, q)
        phi_n = RetornaTotiente(p, q)
        e = 3  # Sabemos que e = 3 funciona
        d = inverso_modular(e, phi_n)
 
        print(f"Valores de teste -> p: {p}, q: {q}, N: {N}, phi(N): {phi_n}, e: {e}, d: {d}")
 
        chave_publica = (e, N)
        chave_privada = (d, N)
 
        mensagem = "A"
        mensagem_criptografada = criptografar(chave_publica, mensagem)
        print(f"Mensagem criptografada: {mensagem_criptografada}")
        # Corrigido o valor esperado para [32]
        self.assertEqual(mensagem_criptografada, [32])  # Deve criptografar para 32
 
        mensagem_decriptografada = decriptografar(chave_privada, mensagem_criptografada)
        print(f"Mensagem decriptografada: {mensagem_decriptografada}")
        self.assertEqual(mensagem_decriptografada, "A")  # Deve decriptografar para "A"
 
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
    chave_publica = json.dumps(chave_publica)
    chave_privada = (d, N)
 
    print("chave pública client: ", chave_publica)
   
    print("chave privada client: " ,chave_privada)
 
       
    mensagem = "The information security is of significant importance to ensure the privacy of communications"
   
    print("\n\nMensagem Original: ", mensagem)
 
 
    # Conexão TCP
    serverName = "10.1.70.2"
    serverPort = 1300
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
 
 
    print(bytes(chave_publica, "utf-8"))
    # Envio da chave pública client
    clientSocket.send(bytes(chave_publica, "utf-8"))
 
    # Recebimento da chave pública server
    modifiedSentence = clientSocket.recv(1000000000)
    chave_publica_server = str(modifiedSentence, "utf-8")
    print("\n\nChave pública server: " + chave_publica_server)  
     
 
    chave_publica_server = json.loads(chave_publica_server)
   
    chave_publica_server = (chave_publica_server['e'], chave_publica_server['N'])
   
 
    #criptografia da mensagem pro server
    mensagem_criptografada_enviada = criptografar(chave_publica_server, mensagem)
    print("\n\nMensagem Criptografada Enviada: ", mensagem_criptografada_enviada)
 
    #Envio da mensagem criptografada
    clientSocket.send(bytes(json.dumps(mensagem_criptografada_enviada), "utf-8"))
   
    # Recebimento da mensagem criptografada do server
    modifiedSentence = clientSocket.recv(1000000000)
    mensagem_criptografada_recebida = json.loads(str(modifiedSentence, "utf-8"))
    print("\n\nMensagem Criptografada Recebida: ", mensagem_criptografada_recebida)
 
    #Descriptografando a mensagem
    mensagem_decriptografada = decriptografar(chave_privada, mensagem_criptografada_recebida)
    print("\n\nMensagem Decriptografada: ", mensagem_decriptografada)
 