import json
from dataclasses import dataclass, field
from typing import Union
from uuid import uuid4

from services.rabbitmq import RabbitmqConsumer, RabbitmqPublisher


@dataclass
class GameState:
    player: Union['P1', 'P2']
    state: Union['has_won', 'tie', 'running'] = 'running'
    positions: list = field(
        default_factory=lambda: [[' ', ' ', ' '] for _ in range(3)]
    )


class Game:
    def new(self):
        """
        Inicialização e criação das duas filas.
        """
        self.__uuid = str(uuid4())
        self.__game_state = GameState(player='P1').__dict__

        queue_p1 = f'{self.__uuid}_P1'
        publisher = RabbitmqPublisher(queue_p1)
        publisher.send_message(self.__game_state)

        queue_p2 = f'{self.__uuid}_P2'
        print(f'New Game {self.__uuid}')
        print('You are (X)')
        consumer = RabbitmqConsumer(queue_p2, self.__get_state)
        consumer.start()

    def join(self, uuid: str):
        """
        P2 entra no jogo e obtem o estado postado por P1.
        """
        self.__uuid = uuid
        self.__game_state = GameState(player='P2').__dict__

        queue_p1 = f'{self.__uuid}_P1'
        consumer = RabbitmqConsumer(queue_p1, self.__get_state)
        print(f'Joined in Game {uuid}')
        print('You are (O)')
        consumer.start()

    def __opponent_observer(self):
        """
        Observa a fila do oponente, a esperada de jogadas.
        """
        opponent_player = 'P2' if self.__game_state['player'] == 'P1' else 'P1'
        queue = f'{self.__uuid}_{opponent_player}'
        consumer = RabbitmqConsumer(queue, self.__get_state)
        consumer.start()

    def __set_state(self):
        """
        Publica na fila do player, as posições do estado atual.
        """
        queue = f'{self.__uuid}_{self.__game_state["player"]}'
        publisher = RabbitmqPublisher(queue)
        publisher.send_message(self.__game_state)

    def __get_state(self, ch, method, properties, body):
        """
        O player obtem as posições da fila que está observando.
        """
        game_state = json.loads(body)
        self.__game_state['positions'] = game_state['positions']
        ch.stop_consuming()
        has_won = self.__has_won()
        if self.__has_won():
            print(f'{has_won} Venceu!!!')
            self.__print_positions()
            self.__close_game()

    def __close_game(self):
        """
        Encerra a aplicação
        """
        self.__game_state['state'] = 'has_won'
        self.__set_state()
        exit(0)

    def __print_positions(self):
        game_positions = self.__game_state['positions']
        for row in range(3):
            for collumn in range(3):
                if game_positions[row][collumn] == None:
                    game_positions[row][collumn] = ' '
                
        print(*game_positions,sep='\n')

    def __has_won(self):
        """
        Verifica se há um vencedor no momento, e casos exista, retorna-o.
        """
        game_positions = [_ for _ in self.__game_state['positions']]

        for row in range(3):
            for collumn in range(3):
                if game_positions[row][collumn] == ' ':
                    game_positions[row][collumn] = None

        for row in game_positions:
            if row.count('O') == 3:
                # linha
                return 'O'
            elif row.count('X') == 3:
                # linha
                return 'X'

        for collumn in range(3):
            if (
                game_positions[0][collumn]
                == game_positions[1][collumn]
                == game_positions[2][collumn]
            ):
                # coluna
                return game_positions[0][collumn]

        if (
            game_positions[0][0]
            == game_positions[1][1]
            == game_positions[2][2]
            and game_positions[0][0] != ' '
        ):
            # diagonal principal
            return game_positions[0][0]

        if (
            game_positions[0][2]
            == game_positions[1][1]
            == game_positions[2][0]
            and game_positions[0][2] != ' '
        ):
            # diagonal secundaria
            return game_positions[0][2]
        return False

    def loop(self):
        """
        Loop principal. Onde as entradas são obtidas.
        """
        while True:
            self.__print_positions()
            x, y = map(int, input('entrada de coordenada: ').split(','))

            character = 'X' if self.__game_state['player'] == 'P1' else 'O'
            self.__game_state['positions'][x][y] = character

            self.__set_state()
            print('Esperando jogada do oponente...')
            self.__opponent_observer()
