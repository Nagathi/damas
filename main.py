import pygame
import sys

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
def desenhar_pecas():
    for linha in range(8):
        for coluna in range(8):
            if tabuleiro[linha][coluna] is not None:
                cor = tabuleiro[linha][coluna]['cor']
                pygame.draw.circle(janela, cor, (coluna * tamanho_casa + tamanho_casa // 2, linha * tamanho_casa + tamanho_casa // 2), tamanho_casa // 2 - 10)
                if tabuleiro[linha][coluna]['tipo'] == 'dama':
                    pygame.draw.circle(janela, (255, 255, 255), (coluna * tamanho_casa + tamanho_casa // 2, linha * tamanho_casa + tamanho_casa // 2), tamanho_casa // 2 - 20)

def movimento_bot():
    movimentos_possiveis = gerar_movimentos(tabuleiro, (0, 0, 255))  # Gerar movimentos para peças azuis (bot)

    if movimentos_possiveis:
        return movimentos_possiveis[0]  # Retorna o primeiro movimento possível (simulação de um bot simples)
    else:
        return None, None

# Função para movimentar as peças
def movimentar_pecas(tabuleiro, posicao_inicial, posicao_final):
    linha_inicial, coluna_inicial = posicao_inicial
    linha_final, coluna_final = posicao_final

    if tabuleiro[linha_inicial][coluna_inicial] is not None:
        cor = tabuleiro[linha_inicial][coluna_inicial]['cor']
        tipo = tabuleiro[linha_inicial][coluna_inicial]['tipo']

        if cor == (0, 0, 255):  # Bot (azul)
            if linha_final < linha_inicial and tipo != 'dama':
                print("Movimento simples não permitido para trás (peça azul)")
                return False

        elif cor == (255, 0, 0):  # Jogador (vermelho)
            if linha_final > linha_inicial and tipo != 'dama':
                print("Movimento simples não permitido para trás (peça vermelha)")
                return False

        tabuleiro[linha_final][coluna_final] = tabuleiro[linha_inicial][coluna_inicial]
        tabuleiro[linha_inicial][coluna_inicial] = None

        if abs(linha_final - linha_inicial) == 2:
            linha_captura = (linha_inicial + linha_final) // 2
            coluna_captura = (coluna_inicial + coluna_final) // 2
            tabuleiro[linha_captura][coluna_captura] = None

        if (linha_final == 0 or linha_final == 7) and tipo == 'comum':
            tabuleiro[linha_final][coluna_final]['tipo'] = 'dama'

        return True

    return False

# Função para gerar movimentos
def gerar_movimentos(tabuleiro, cor):
    movimentos = []
    for linha in range(8):
        for coluna in range(8):
            if tabuleiro[linha][coluna] is not None and tabuleiro[linha][coluna]['cor'] == cor:
                direcoes = []
                if cor == (0, 0, 255):  # Bot (azul)
                    direcoes = [(1, -1), (1, 1)]  # Movimento para frente
                elif cor == (255, 0, 0):  # Jogador (vermelho)
                    direcoes = [(-1, -1), (-1, 1)]  # Movimento para frente

                if tabuleiro[linha][coluna]['tipo'] == 'dama':
                    direcoes.extend([(1, -1), (1, 1), (-1, -1), (-1, 1)])  # Movimento em todas as direções

                for direcao in direcoes:
                    nova_linha = linha + direcao[0]
                    nova_coluna = coluna + direcao[1]
                    if 0 <= nova_linha < 8 and 0 <= nova_coluna < 8:
                        if tabuleiro[nova_linha][nova_coluna] is None:
                            movimentos.append(((linha, coluna), (nova_linha, nova_coluna)))
                        elif tabuleiro[nova_linha][nova_coluna]['cor'] != cor:
                            nova_linha = linha + 2 * direcao[0]
                            nova_coluna = coluna + 2 * direcao[1]
                            if 0 <= nova_linha < 8 and 0 <= nova_coluna < 8 and tabuleiro[nova_linha][nova_coluna] is None:
                                movimentos.append(((linha, coluna), (nova_linha, nova_coluna)))
    return movimentos

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
            posicao_selecionada, posicao_destino = movimento_bot()
            if posicao_selecionada and posicao_destino:
                if movimentar_pecas(tabuleiro, posicao_selecionada, posicao_destino):
                    while True:  # Loop para capturas múltiplas
                        movimentos_pos_captura = gerar_movimentos(tabuleiro, (0, 0, 255))  # Movimentos para peças azuis (bot)
                        nova_captura = False
                        for movimento in movimentos_pos_captura:
                            if movimento[0] == posicao_destino and abs(movimento[1][0] - movimento[0][0]) == 2:
                                posicao_selecionada, posicao_destino = movimento
                                movimentar_pecas(tabuleiro, posicao_selecionada, posicao_destino)
                                nova_captura = True
                                break
                        if not nova_captura:
                            break
                    turno_vermelho = True
            else:
                turno_vermelho = True  # Se o bot não encontrou movimentos válidos, alterna o turno de volta para o jogador humano

        # Desenhar o tabuleiro
        desenhar_tabuleiro()

        # Destacar a casa selecionada temporariamente em verde
        if posicao_selecionada:
            linha, coluna = posicao_selecionada
            pygame.draw.rect(janela, VERDE, (coluna * tamanho_casa, linha * tamanho_casa, tamanho_casa, tamanho_casa))

        # Desenhar as peças
        desenhar_pecas()

        # Atualizar a tela
        pygame.display.flip()

if __name__ == '__main__':
    main()
