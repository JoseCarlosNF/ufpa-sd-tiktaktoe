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

        queue_p1 = f'{self.__game_state["player"]}_{self.__uuid}'
        publisher = RabbitmqPublisher(queue_p1)
        publisher.send_message(self.__game_state)

        queue_p2 = f'P2_{self.__uuid}'
        print(f'New Game {self.__uuid}')
        consumer = RabbitmqConsumer(queue_p2, self.__get_state)
        consumer.start()

    def join(self, uuid: str):
        """
        P2 entra no jogo e obtem o estado postado por P1.
        """
        self.__uuid = uuid
        self.__game_state = GameState(player='P2').__dict__

        queue_p1 = f'P1_{self.__uuid}'
        consumer = RabbitmqConsumer(queue_p1, self.__get_state)
        print(f'Joined in Game {uuid}')
        consumer.start()

    def __opponent_observer(self):
        """
        Observa a fila do oponente, a esperada de jogadas.
        """
        opponent_player = 'P2' if self.__game_state['player'] == 'P1' else 'P1'
        queue = f'{opponent_player}_{self.__uuid}'
        consumer = RabbitmqConsumer(queue, self.__get_state)
        consumer.start()

    def __set_state(self):
        """
        Publica na fila do player, as posições do estado atual.
        """
        queue = f'{self.__game_state["player"]}_{self.__uuid}'
        publisher = RabbitmqPublisher(queue)
        publisher.send_message(self.__game_state)

    def __get_state(self, ch, method, properties, body):
        """
        O player obtem as posições da fila que está observando.
        """
        game_state = json.loads(body)
        self.__game_state['positions'] = game_state['positions']
        ch.stop_consuming()

    def __has_winner(self, game_positions: list):
        """
        Verifica se há um vencedor no momento, e casos exista, retorna-o.
        """
        for row in game_positions:
            if row.count('o') == 3:
                # linha
                return 'o'
            elif row.count('x') == 3:
                # linha
                return 'x'

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

    def loop(self):
        while True:
            [print(_) for _ in self.__game_state['positions']]
            x, y = map(int, input('entrada de coordenada: ').split(','))

            character = 'X' if self.__game_state['player'] == 'P1' else 'O'
            self.__game_state['positions'][x][y] = character
            self.__set_state()
            print('Esperando jogada do oponente...')
            self.__opponent_observer()
