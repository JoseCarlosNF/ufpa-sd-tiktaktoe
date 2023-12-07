# TikTakToe

*O clássico jogo da velha, multiplayer e distribuído*.

## :sparkles: Tecnologias utilizadas

- Python
- Docker
    - docker-compose
- RabbitMQ
- Nginx

## Por que utilizar uma arquitetura `publish/consumer`?

Para responder melhor, vamos precisar discorrer sobre dois outros assuntos.

### Design

**Requisitos**

### Arquitetura

**Orientada a eventos**

## :rocket: Como rodar o projeto

Constrói a imagem docker:
```
make build
```

Cria uma partida:
```
make create
```

Entra em uma partida
```
make joind UUID=88974a12-9a1a-4c53-9bc9-0c74d7ce49bf
```

## :test_tube: Exemplo de execução

Player 1
```
# python ufpa_sd_tiktaktoe/ -c

New Game 272f9acc-ad2a-491b-96cb-a19e2853dd95
You are (X)
[' ', ' ', ' ']
[' ', 'O', ' ']
[' ', ' ', ' ']
entrada de coordenada: 0,0
Esperando jogada do oponente...
['X', ' ', ' ']
[' ', 'O', 'O']
[' ', ' ', ' ']
entrada de coordenada: 0,1
Esperando jogada do oponente...
['X', 'X', ' ']
[' ', 'O', 'O']
[' ', 'O', ' ']
entrada de coordenada: 0,2
Esperando jogada do oponente...
X Venceu!!!
['X', 'X', 'X']
[' ', 'O', 'O']
[' ', 'O', ' ']
```

Player 2
```
#  python ufpa_sd_tiktaktoe/ -j 272f9acc-ad2a-491b-96cb-a19e2853dd95

Joined in Game 272f9acc-ad2a-491b-96cb-a19e2853dd95
You are (O)
[' ', ' ', ' ']
[' ', ' ', ' ']
[' ', ' ', ' ']
entrada de coordenada: 1,1
Esperando jogada do oponente...
['X', ' ', ' ']
[' ', 'O', ' ']
[' ', ' ', ' ']
entrada de coordenada: 1,2
Esperando jogada do oponente...
['X', 'X', ' ']
[' ', 'O', 'O']
[' ', ' ', ' ']
entrada de coordenada: 2,1
Esperando jogada do oponente...
X Venceu!!!
['X', 'X', 'X']
[' ', 'O', 'O']
[' ', 'O', ' ']
```
