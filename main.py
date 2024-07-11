import pygame
import sys
import copy

pygame.init()

largura = 600
altura = 600
tamanho_casa = 75

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
CINZA = (200, 200, 200)

janela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Jogo de Damas')

tabuleiro = [
    [{'cor': (0, 0, 255), 'dama': False} if (linha + coluna) % 2 != 0 and linha < 3 else
     {'cor': (255, 0, 0), 'dama': False} if (linha + coluna) % 2 != 0 and linha > 4 else None
     for coluna in range(8)]
    for linha in range(8)
]

def desenhar_tabuleiro():
    for linha in range(8):
        for coluna in range(8):
            cor = BRANCO if (linha + coluna) % 2 == 0 else PRETO
            pygame.draw.rect(janela, cor, (coluna * tamanho_casa, linha * tamanho_casa, tamanho_casa, tamanho_casa))

def desenhar_pecas():
    raio = tamanho_casa // 2 - 5
    for linha in range(8):
        for coluna in range(8):
            if tabuleiro[linha][coluna] is not None:
                cor_peca = tabuleiro[linha][coluna]['cor']
                pygame.draw.circle(janela, cor_peca, (coluna * tamanho_casa + tamanho_casa // 2, linha * tamanho_casa + tamanho_casa // 2), raio)
                if tabuleiro[linha][coluna]['dama']:
                    pygame.draw.circle(janela, CINZA, (coluna * tamanho_casa + tamanho_casa // 2, linha * tamanho_casa + tamanho_casa // 2), raio // 2)

def movimentar_pecas(tabuleiro, posicao_selecionada, posicao_destino):
    linha_sel, coluna_sel = posicao_selecionada
    linha_dest, coluna_dest = posicao_destino
    
    peca_selecionada = tabuleiro[linha_sel][coluna_sel]
    
    if not peca_selecionada:
        return False
    
    cor_peca = peca_selecionada['cor']
    is_dama = 'dama' in peca_selecionada and peca_selecionada['dama']
    
    # Movimento simples para peça normal ou dama
    if (abs(linha_dest - linha_sel) == 1 and abs(coluna_dest - coluna_sel) == 1) or \
       (is_dama and abs(linha_dest - linha_sel) == abs(coluna_dest - coluna_sel)):
        if not tabuleiro[linha_dest][coluna_dest]:
            tabuleiro[linha_dest][coluna_dest] = peca_selecionada
            tabuleiro[linha_sel][coluna_sel] = None
 
            if (cor_peca == (255, 0, 0) and linha_dest == 0) or (cor_peca == (0, 0, 255) and linha_dest == 7):
                tabuleiro[linha_dest][coluna_dest]['dama'] = True
            return True
    
    # Captura para peça normal ou dama
    if (abs(linha_dest - linha_sel) == 2 and abs(coluna_dest - coluna_sel) == 2) or \
       (is_dama and abs(linha_dest - linha_sel) == abs(coluna_dest - coluna_sel) == 2):
        linha_meio = (linha_sel + linha_dest) // 2
        coluna_meio = (coluna_sel + coluna_dest) // 2
        peca_meio = tabuleiro[linha_meio][coluna_meio]
        
        if peca_meio and peca_meio['cor'] != cor_peca:
            if not tabuleiro[linha_dest][coluna_dest]:
                tabuleiro[linha_dest][coluna_dest] = peca_selecionada
                tabuleiro[linha_meio][coluna_meio] = None
                tabuleiro[linha_sel][coluna_sel] = None

                if (cor_peca == (255, 0, 0) and linha_dest == 0) or (cor_peca == (0, 0, 255) and linha_dest == 7):
                    tabuleiro[linha_dest][coluna_dest]['dama'] = True
                return True
    
    return False


def jogo_terminado(tabuleiro):
    print("Jogo finalizado!")
    return False

def avaliacao(tabuleiro):
    return 0

def minimax(tabuleiro, profundidade, alfa, beta, maximizando):
    if profundidade == 0 or jogo_terminado(tabuleiro):
        return avaliacao(tabuleiro)
    
    if maximizando:
        melhor_valor = float('-inf')
        movimentos = gerar_movimentos(tabuleiro, (0, 0, 255))
        for movimento in movimentos:
            tabuleiro_copia = copy.deepcopy(tabuleiro)
            movimentar_pecas(tabuleiro_copia, movimento[0], movimento[1])
            valor = minimax(tabuleiro_copia, profundidade - 1, alfa, beta, False)
            melhor_valor = max(melhor_valor, valor)
            alfa = max(alfa, melhor_valor)
            if beta <= alfa:
                break
        return melhor_valor
    else:
        melhor_valor = float('inf')
        movimentos = gerar_movimentos(tabuleiro, (255, 0, 0))
        for movimento in movimentos:
            tabuleiro_copia = copy.deepcopy(tabuleiro)
            movimentar_pecas(tabuleiro_copia, movimento[0], movimento[1])
            valor = minimax(tabuleiro_copia, profundidade - 1, alfa, beta, True)
            melhor_valor = min(melhor_valor, valor)
            beta = min(beta, melhor_valor)
            if beta <= alfa:
                break 
        return melhor_valor


def movimento_bot():
    movimentos = gerar_movimentos(tabuleiro, (0, 0, 255))
    if not movimentos:
        return None, None
    
    melhor_movimento = None
    melhor_valor = float('-inf')
    
    for movimento in movimentos:
        tabuleiro_copia = copy.deepcopy(tabuleiro)
        movimentar_pecas(tabuleiro_copia, movimento[0], movimento[1])
        valor = minimax(tabuleiro_copia, 3, float('-inf'), float('inf'), False)
        if valor > melhor_valor:
            melhor_valor = valor
            melhor_movimento = movimento
    
    if melhor_movimento:
        return melhor_movimento
    else:
        return None, None


def gerar_movimentos(tabuleiro, cor):
    movimentos = []
    capturas = []

    direcao = 1 if cor == (0, 0, 255) else -1  # Direção de movimento

    for linha in range(8):
        for coluna in range(8):
            peca = tabuleiro[linha][coluna]
            if peca and peca['cor'] == cor:
                if 'dama' in peca and peca['dama']:  # Verifica se é uma dama
                    for delta in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:  # Movimentos diagonais
                        nova_linha = linha + delta[0]
                        nova_coluna = coluna + delta[1]
                        
                        while 0 <= nova_linha < 8 and 0 <= nova_coluna < 8:
                            if not tabuleiro[nova_linha][nova_coluna]:
                                movimentos.append(((linha, coluna), (nova_linha, nova_coluna)))
                            else:
                                break
                            nova_linha += delta[0]
                            nova_coluna += delta[1]


                    # Captura para damas
                    for delta in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
                        linha_meio = linha + delta[0] // 2
                        coluna_meio = coluna + delta[1] // 2
                        nova_linha = linha + delta[0]
                        nova_coluna = coluna + delta[1]

                        if (0 <= nova_linha < 8 and 0 <= nova_coluna < 8 and
                            tabuleiro[linha_meio][coluna_meio] and
                            tabuleiro[linha_meio][coluna_meio]['cor'] != cor and
                            not tabuleiro[nova_linha][nova_coluna]):
                            capturas.append(((linha, coluna), (nova_linha, nova_coluna)))

                else:  # Peça comum (não dama)
                    for delta in [(1, -1), (1, 1)]:  # Movimentos diagonais simples
                        nova_linha = linha + delta[0] * direcao
                        nova_coluna = coluna + delta[1]

                        if 0 <= nova_linha < 8 and 0 <= nova_coluna < 8:
                            if not tabuleiro[nova_linha][nova_coluna]:
                                movimentos.append(((linha, coluna), (nova_linha, nova_coluna)))

                    # Captura para peças comuns
                    for delta in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
                        linha_meio = linha + delta[0] // 2
                        coluna_meio = coluna + delta[1] // 2
                        nova_linha = linha + delta[0]
                        nova_coluna = coluna + delta[1]

                        if (0 <= nova_linha < 8 and 0 <= nova_coluna < 8 and
                            tabuleiro[linha_meio][coluna_meio] and
                            tabuleiro[linha_meio][coluna_meio]['cor'] != cor and
                            not tabuleiro[nova_linha][nova_coluna]):
                            capturas.append(((linha, coluna), (nova_linha, nova_coluna)))

    if capturas:
        return capturas
    return movimentos




def main():
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
                
                movimentos_validos = gerar_movimentos(tabuleiro, (255, 0, 0))  # Movimentos válidos para peças vermelhas
                if (posicao_selecionada, posicao_destino) in movimentos_validos:
                    movimentar_pecas(tabuleiro, posicao_selecionada, posicao_destino)
                    turno_vermelho = False
                
                selecionado = False
                posicao_selecionada = None

        # Turno do bot
        if not turno_vermelho:
            posicao_selecionada, posicao_destino = movimento_bot()
            if posicao_selecionada and posicao_destino:
                movimentar_pecas(tabuleiro, posicao_selecionada, posicao_destino)
                turno_vermelho = True
        
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
