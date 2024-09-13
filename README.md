# RSA


## Criptografia RSA com Comunicação TCP - Cliente e Servidor

- Descrição do Projeto
Este projeto implementa um sistema de comunicação segura entre um servidor e um cliente, utilizando Sockets TCP e criptografia RSA. A troca de mensagens é criptografada, garantindo que apenas o destinatário correto possa decriptar e entender os dados. Ambos os lados geram suas próprias chaves públicas e privadas e as utilizam para criptografar e decriptar as mensagens trocadas.

## Funcionalidades
Geração de Chaves RSA: Tanto o cliente quanto o servidor geram suas próprias chaves públicas e privadas.

Troca de Chaves: As chaves públicas são trocadas no início da comunicação.

Criptografia de Mensagens: As mensagens são criptografadas usando a chave pública do destinatário.

Decriptografia de Mensagens: As mensagens recebidas são decriptadas com a chave privada do destinatário.

Comunicação via TCP: Cliente e servidor se comunicam usando sockets TCP.

## Pré-requisitos
Python 3.7 ou superior
Bibliotecas necessárias podem ser instaladas com o comando: pip install -r requirements.txt

## Como Funciona
RSA (Criptografia de Chave Pública)
Cliente e servidor geram dois números primos grandes (p e q) e, a partir deles, calculam N e phi_n para gerar as chaves públicas e privadas.
A chave pública (composta por e e N) é usada para criptografar as mensagens.
A chave privada (composta por d e N) é usada para decriptar as mensagens.
Durante a comunicação:
O cliente criptografa a mensagem usando a chave pública do servidor.
O servidor decripta a mensagem com sua chave privada.
O servidor responde criptografando com a chave pública do cliente.
O cliente decripta a resposta com sua chave privada.
Fluxo de Comunicação
Troca de Chaves: O cliente envia sua chave pública ao servidor e recebe a chave pública do servidor.
Envio de Mensagens:
O cliente criptografa uma mensagem com a chave pública do servidor e a envia.
O servidor decripta a mensagem recebida, a processa e responde.
O cliente decripta a mensagem de resposta.
Executando o Projeto
Passo 1: Executar o Servidor
No terminal, navegue até o diretório do projeto e execute o servidor com o comando: python server.py
O servidor aguardará conexões de clientes na porta 1300.
Passo 2: Executar o Cliente
Em outro terminal, execute o cliente: python RSA_tcpclient.py
O cliente se conectará ao servidor e realizará a troca de chaves públicas.
Após a troca de chaves, o cliente enviará uma mensagem criptografada ao servidor.

## Exemplo de Código
Código do Servidor
O servidor gera as chaves RSA com os números primos p e q, calcula N, phi_n, e e d.
O servidor ouve a porta 1300 e aguarda a conexão de um cliente.
Após a conexão, ele recebe a chave pública do cliente e envia sua própria chave pública.
O servidor decripta a mensagem recebida do cliente com sua chave privada, processa a mensagem, converte para maiúsculas, criptografa com a chave pública do cliente e envia a resposta.

Código do Cliente
O cliente gera suas chaves RSA com números primos p e q.
O cliente se conecta ao servidor na porta 1300.
Ele envia sua chave pública para o servidor e recebe a chave pública do servidor.
O cliente criptografa uma mensagem com a chave pública do servidor e a envia.
Ao receber a resposta do servidor, o cliente decripta a mensagem usando sua chave privada.mas coloca
