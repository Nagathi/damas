import pygame
import sys
import copy
import random  # Importando a biblioteca random

# Definindo as constantes
largura_janela = 800
altura_janela = 800
tamanho_casa = largura_janela // 8
VERDE = (0, 255, 0)

# Inicializando o Pygame
pygame.init()

# Criando a janela do jogo
janela = pygame.display.set_mode((largura_janela, altura_janela))
pygame.display.set_caption('Jogo de Damas')

# Função para desenhar o tabuleiro
def desenhar_tabuleiro():
    for linha in range(8):
        for coluna in range(8):
            if (linha + coluna) % 2 == 0:
                cor = (255, 255, 255)
            else:
                cor = (0, 0, 0)
            pygame.draw.rect(janela, cor, (coluna * tamanho_casa, linha * tamanho_casa, tamanho_casa, tamanho_casa))

# Função para desenhar as peças
def desenhar_pecas(tabuleiro):
    for linha in range(8):
        for coluna in range(8):
            if tabuleiro[linha][coluna] is not None:
                cor = tabuleiro[linha][coluna]['cor']
                pygame.draw.circle(janela, cor, (coluna * tamanho_casa + tamanho_casa // 2, linha * tamanho_casa + tamanho_casa // 2), tamanho_casa // 2 - 10)
                if tabuleiro[linha][coluna]['tipo'] == 'dama':
                    pygame.draw.circle(janela, (255, 255, 255), (coluna * tamanho_casa + tamanho_casa // 2, linha * tamanho_casa + tamanho_casa // 2), tamanho_casa // 2 - 20)

def movimentar_pecas(tabuleiro, posicao_inicial, posicao_final):
    linha_inicial, coluna_inicial = posicao_inicial
    linha_final, coluna_final = posicao_final

    # Verifica se a posição inicial e final estão dentro dos limites do tabuleiro
    if not (0 <= linha_inicial < len(tabuleiro)) or not (0 <= coluna_inicial < len(tabuleiro[0])):
        print("Posição inicial fora dos limites.")
        return False
    if not (0 <= linha_final < len(tabuleiro)) or not (0 <= coluna_final < len(tabuleiro[0])):
        print("Posição final fora dos limites.")
        return False

    # Verifica se há uma peça na posição inicial e se a posição final está vazia
    if tabuleiro[linha_inicial][coluna_inicial] is None:
        print("Não há peça na posição inicial.")
        return False
    if tabuleiro[linha_final][coluna_final] is not None:
        print("Posição final não está vazia.")
        return False
    
    # Determina a direção do movimento
    direcao = (linha_final - linha_inicial, coluna_final - coluna_inicial)
    
    # Verifica captura de peça
    if abs(direcao[0]) == 2 and abs(direcao[1]) == 2:  # Captura é sempre movimento de 2 casas ou mais
        passo_linha = 1 if direcao[0] > 0 else -1
        passo_coluna = 1 if direcao[1] > 0 else -1
        linha_captura = linha_inicial + passo_linha
        coluna_captura = coluna_inicial + passo_coluna

        if tabuleiro[linha_captura][coluna_captura] is not None and tabuleiro[linha_captura][coluna_captura]['cor'] != tabuleiro[linha_inicial][coluna_inicial]['cor']:
            tabuleiro[linha_captura][coluna_captura] = None  # Remove a peça capturada
            tabuleiro[linha_final][coluna_final] = tabuleiro[linha_inicial][coluna_inicial]
            tabuleiro[linha_inicial][coluna_inicial] = None
            return True
    
    elif abs(direcao[0]) == 1 and abs(direcao[1]) == 1:  # Movimento normal de uma casa
        cor_peca = tabuleiro[linha_inicial][coluna_inicial]['cor']
        if tabuleiro[linha_final][coluna_final] is None:
            if direcao[0] == -1 and cor_peca == (255, 0, 0):  # Movimento para frente para peça normal (vermelha)
                tabuleiro[linha_final][coluna_final] = tabuleiro[linha_inicial][coluna_inicial]
                tabuleiro[linha_inicial][coluna_inicial] = None
                return True
            elif direcao[0] == 1 and cor_peca == (0, 0, 255):  # Movimento para frente para peça normal (azul)
                tabuleiro[linha_final][coluna_final] = tabuleiro[linha_inicial][coluna_inicial]
                tabuleiro[linha_inicial][coluna_inicial] = None
                return True
            else:
                print("Movimento inválido.")
                return False
        else:
            print("Movimento inválido.")
            return False
    else:
        print("Movimento inválido.")
        return False

def gerar_movimentos(tabuleiro, cor):
    movimentos = []
    capturas_obrigatorias = []

    for linha in range(8):
        for coluna in range(8):
            if tabuleiro[linha][coluna] is not None and tabuleiro[linha][coluna]['cor'] == cor:
                if tabuleiro[linha][coluna]['tipo'] == 'comum':  # Peça normal
                    movimentos_captura = verificar_captura_obrigatoria(tabuleiro, (255, 0, 0) if cor == (0, 0, 255) else (0, 0, 255))
                    if movimentos_captura:
                        capturas_obrigatorias.extend(movimentos_captura)
                    else:
                        direcao = 1 if cor == (0, 0, 255) else -1
                        if 0 <= linha + direcao < 8:
                            if 0 <= coluna - 1 < 8 and tabuleiro[linha + direcao][coluna - 1] is None:  # Movimento para diagonal esquerda
                                movimentos.append(((linha, coluna), (linha + direcao, coluna - 1)))
                            if 0 <= coluna + 1 < 8 and tabuleiro[linha + direcao][coluna + 1] is None:  # Movimento para diagonal direita
                                movimentos.append(((linha, coluna), (linha + direcao, coluna + 1)))
                
                elif tabuleiro[linha][coluna]['tipo'] == 'dama':  # Dama pode mover em todas as direções
                    direcoes = [(1, -1), (1, 1), (-1, -1), (-1, 1)]
                    for direcao in direcoes:
                        nova_linha = linha + direcao[0]
                        nova_coluna = coluna + direcao[1]
                        while 0 <= nova_linha < 8 and 0 <= nova_coluna < 8 and tabuleiro[nova_linha][nova_coluna] is None:
                            movimentos.append(((linha, coluna), (nova_linha, nova_coluna)))
                            nova_linha += direcao[0]
                            nova_coluna += direcao[1]
    
    if capturas_obrigatorias:
        return capturas_obrigatorias
    else:
        return movimentos

def verificar_captura_obrigatoria(tabuleiro, cor_peca):
    capturas = []

    for linha in range(8):
        for coluna in range(8):
            if tabuleiro[linha][coluna] is not None and tabuleiro[linha][coluna]['cor'] == cor_peca:
                if tabuleiro[linha][coluna]['tipo'] == 'comum':  # Peça normal
                    passo_linha = 1 if cor_peca == (255, 0, 0) else -1  # Determina direção de avanço
                    for passo_coluna in [-1, 1]:
                        linha_captura = linha + passo_linha
                        coluna_captura = coluna + passo_coluna
                        linha_alvo = linha + 2 * passo_linha
                        coluna_alvo = coluna + 2 * passo_coluna

                        if 0 <= linha_alvo < 8 and 0 <= coluna_alvo < 8:
                            if tabuleiro[linha_captura][coluna_captura] is not None and tabuleiro[linha_captura][coluna_captura]['cor'] != cor_peca and tabuleiro[linha_alvo][coluna_alvo] is None:
                                capturas.append(((linha, coluna), (linha_alvo, coluna_alvo)))
                                break  # Sai do loop interno para evitar capturas múltiplas

    return capturas

import random

def movimento_bot(tabuleiro):
    movimentos = []
    for linha in range(8):
        for coluna in range(8):
            if tabuleiro[linha][coluna] is not None and tabuleiro[linha][coluna]['cor'] == (0, 0, 255):  # Peças do bot (azul)
                posicao_inicial = (linha, coluna)
                possiveis_movimentos = gerar_movimentos(tabuleiro, (0, 0, 255))
                for movimento in possiveis_movimentos:
                    movimentos.append((posicao_inicial, movimento[1]))

    if movimentos:
        movimento_escolhido = random.choice(movimentos)
        return movimento_escolhido[0], movimento_escolhido[1]
    else:
        return None, None


def main():
    global tabuleiro
    tabuleiro = [
        [None, {'cor': (0, 0, 255), 'tipo': 'comum'}, None, {'cor': (0, 0, 255), 'tipo': 'comum'}, None, {'cor': (0, 0, 255), 'tipo': 'comum'}, None, {'cor': (0, 0, 255), 'tipo': 'comum'}],
        [{'cor': (0, 0, 255), 'tipo': 'comum'}, None, {'cor': (0, 0, 255), 'tipo': 'comum'}, None, {'cor': (0, 0, 255), 'tipo': 'comum'}, None, {'cor': (0, 0, 255), 'tipo': 'comum'}, None],
        [None, {'cor': (0, 0, 255), 'tipo': 'comum'}, None, {'cor': (0, 0, 255), 'tipo': 'comum'}, None, {'cor': (0, 0, 255), 'tipo': 'comum'}, None, {'cor': (0, 0, 255), 'tipo': 'comum'}],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [{'cor': (255, 0, 0), 'tipo': 'comum'}, None, {'cor': (255, 0, 0), 'tipo': 'comum'}, None, {'cor': (255, 0, 0), 'tipo': 'comum'}, None, {'cor': (255, 0, 0), 'tipo': 'comum'}, None],
        [None, {'cor': (255, 0, 0), 'tipo': 'comum'}, None, {'cor': (255, 0, 0), 'tipo': 'comum'}, None, {'cor': (255, 0, 0), 'tipo': 'comum'}, None, {'cor': (255, 0, 0), 'tipo': 'comum'}],
        [{'cor': (255, 0, 0), 'tipo': 'comum'}, None, {'cor': (255, 0, 0), 'tipo': 'comum'}, None, {'cor': (255, 0, 0), 'tipo': 'comum'}, None, {'cor': (255, 0, 0), 'tipo': 'comum'}, None],
    ]

    selecionado = False
    posicao_selecionada = None
    turno_vermelho = True  # True se for o turno do jogador vermelho (humano), False se for o turno do bot (azul)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and turno_vermelho and not selecionado:
                x, y = pygame.mouse.get_pos()
                coluna = x // tamanho_casa
                linha = y // tamanho_casa
                cor_peca = (255, 0, 0)  # Cor das peças vermelhas
                if (linha + coluna) % 2 != 0 and tabuleiro[linha][coluna] is not None and tabuleiro[linha][coluna]['cor'] == cor_peca:
                    posicao_selecionada = (linha, coluna)
                    selecionado = True
            elif event.type == pygame.MOUSEBUTTONDOWN and turno_vermelho and selecionado:
                x, y = pygame.mouse.get_pos()
                coluna = x // tamanho_casa
                linha = y // tamanho_casa
                posicao_destino = (linha, coluna)

                # Verifica se é possível realizar o movimento
                if (linha + coluna) % 2 != 0:
                    if movimentar_pecas(tabuleiro, posicao_selecionada, posicao_destino):
                        turno_vermelho = False

                selecionado = False
                posicao_selecionada = None

        # Turno do bot
        if not turno_vermelho:
            print("Turno do bot...")
            posicao_selecionada, posicao_destino = movimento_bot(tabuleiro)
            if posicao_selecionada and posicao_destino:
                if movimentar_pecas(tabuleiro, posicao_selecionada, posicao_destino):
                    turno_vermelho = True  # Muda para o próximo turno após o movimento do bot

        # Desenhar o tabuleiro
        desenhar_tabuleiro()

        # Destacar a casa selecionada temporariamente em verde
        if posicao_selecionada:
            linha, coluna = posicao_selecionada
            pygame.draw.rect(janela, VERDE, (coluna * tamanho_casa, linha * tamanho_casa, tamanho_casa, tamanho_casa))

        # Desenhar as peças
        desenhar_pecas(tabuleiro)

        # Atualizar a tela
        pygame.display.flip()

if __name__ == '__main__':
    main()
