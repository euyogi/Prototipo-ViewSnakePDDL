# IMPORTANTE QUE O PLANO SEJA CORRESPONDENTE AO PROBLEMA!
# BASEADO NO PLANO GERADO PELO MADAGASCAR, NÃO SEI SE
# OUTROS FUNCIONARIAM SEM ALGUNS AJUSTES.

import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame, sys, time


# Constantes:
VAZIO_INV = -1
VAZIO = 0
CORPO = 1
CABECA = 2
MACA = 3
LADO_QUADRADO = 50

# Cores:
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 180, 0)
VERDE_ESCURO = (0, 64, 0)
VERMELHO = (200, 0, 0)
CINZA = (20, 20, 20)
CINZA_ESCURO = (70, 70, 70)
LARANJA = (200, 100, 0)

# Inicializando pygame:
pygame.init()
pygame.display.set_caption("Visualizador Snake - YOGI")
FONT = pygame.font.SysFont("Segoe UI", 15)


def main():
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print("Usage: python [visualizador-snake-ipc2018.py] [problem-name.pddl] [plan-name.txt] [opt-interval]")
        return -1

    arquivo_problema = open(sys.argv[1], "rt")
    arquivo_plano = open(sys.argv[2], "rt")

    dimensoes_mapa = {}
    mapa, coord_maca, cobra = [], [], []

    apos_objects = False
    for linha in arquivo_problema.readlines():
        x_idx = linha.rfind('s') + 1  # Início da coordenada x
        y_idx = linha.rfind('-') + 1  # Início da coordenada y

        if not apos_objects and linha.find("objects") != -1:
            apos_objects = True  # Na linha após objects temos as dimensões do mapa
        elif linha.find("goal") != -1:
            break
        elif apos_objects:
            dimensoes_mapa['y'] = int(linha[y_idx:]) + 1
            dimensoes_mapa['x'] = int(linha[x_idx:y_idx - 1]) + 1
            mapa = [0] * dimensoes_mapa['x'] * dimensoes_mapa['y']
            apos_objects = False  # Não queremos sobreescrever sem querer as dimensões
        elif linha.find("nextsnake") != -1:
            mapa[int(linha[x_idx:y_idx - 1]) + int(linha[y_idx:linha.rfind(')')]) * dimensoes_mapa['x']] = CORPO
        elif linha.find("headsnake") != -1:
            mapa[int(linha[x_idx:y_idx - 1]) + int(linha[y_idx:linha.rfind(')')]) * dimensoes_mapa['x']] = CABECA
        elif linha.find("ispoint") != -1:
            coord_maca.append(int(linha[x_idx:y_idx - 1]) + int(linha[y_idx:linha.rfind(')')]) * dimensoes_mapa['x'])
    
    # Janela
    comprimento = (dimensoes_mapa['x'] + 2) * LADO_QUADRADO
    altura = (dimensoes_mapa['y'] + 2) * LADO_QUADRADO
    janela = pygame.display.set_mode((comprimento, altura))

    # Listas com elementos que serão adicionados e retirados do mapa
    passos, novas_cabecas, antigas_cabecas, antigas_caldas, novas_macas = [], [], [], [], []

    for linha in arquivo_plano.readlines():
        if linha.find("move") != -1:
            passos.append(linha.removeprefix("STEP ").removesuffix('\n'))

            x_idx = linha.find("pos") + 3
            y_idx = x_idx + linha[x_idx:].find('-') + 1
            virgula_idx = linha[y_idx:].find(',') + y_idx
            antigas_cabecas.append((int(linha[x_idx:y_idx - 1]), int(linha[y_idx:virgula_idx])))

            x_idx = y_idx + linha[y_idx:].find("pos") + 3
            y_idx = x_idx + linha[x_idx:].find('-') + 1
            virgula_parenteses_idx = linha[y_idx:].find(',') + y_idx
            
            if virgula_parenteses_idx == y_idx - 1:
                virgula_parenteses_idx = linha.find(')')
            
            novas_cabecas.append((int(linha[x_idx:y_idx - 1]), int(linha[y_idx:virgula_parenteses_idx])))

            x_idx = y_idx + linha[y_idx:].find("pos") + 3
            y_idx = x_idx + linha[x_idx:].find('-') + 1
            virgula_idx = linha[y_idx:].find(',') + y_idx

            if linha.find("move-and-eat-spawn") != -1:
                novas_macas.append((int(linha[x_idx:y_idx - 1]), int(linha[y_idx:virgula_idx])))
            elif linha.find("move-and-eat-no-spawn") == -1:
                antigas_caldas.append((int(linha[x_idx:y_idx - 1]), int(linha[y_idx:virgula_idx])))

    arquivo_problema.close()
    arquivo_plano.close()

    rodando = True
    qnt_movimentos, pontos = 0, 0
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                break

        janela.fill(PRETO)

        if qnt_movimentos < len(novas_cabecas):  # Cada nova cabeça corresponde à 1 movimento, não excedemos
            text = FONT.render(passos[qnt_movimentos], True, BRANCO)
        else:
            text = FONT.render(f"FIM, TOTAL DE {qnt_movimentos} PASSOS/AÇÕES :)", True, BRANCO)
            for i in range(dimensoes_mapa['y']):
                for j in range(dimensoes_mapa['x']):
                    if mapa[j + i * dimensoes_mapa['x']] == 1:
                        mapa[j + i * dimensoes_mapa['x']] = -1

        # Passos
        janela.blit(text, (5, 0))

        # Posições do mapa
        pygame.draw.line(janela, CINZA, (0, LADO_QUADRADO / 2), (comprimento, LADO_QUADRADO / 2), 2)

        # Pontos
        janela.blit(FONT.render(str(pontos + 2), True, BRANCO),
                    (comprimento - LADO_QUADRADO / 1.7, LADO_QUADRADO))

        # Adiciona as maçãs da lista no mapa se tiver espaço para elas
        for coord in coord_maca:
            if mapa[coord] == VAZIO:
                mapa[coord] = MACA

        for i in range(dimensoes_mapa['y']):
            janela.blit(FONT.render(str(i), True, CINZA_ESCURO), (LADO_QUADRADO - 20, (i + 1) * LADO_QUADRADO + 3))

        for i in range(dimensoes_mapa['x']):
            janela.blit(FONT.render(str(i), True, CINZA_ESCURO), ((i + 1) * LADO_QUADRADO + 3, LADO_QUADRADO - 20))

        # Itera o mapa pintando cada quadradinho e linhas
        for i in range(dimensoes_mapa['y']):
            for j in range(dimensoes_mapa['x']):
                valor = mapa[j + i * dimensoes_mapa['x']]
                x = (j + 1) * LADO_QUADRADO
                y = (i + 1) * LADO_QUADRADO

                cor = PRETO

                if valor == CORPO:
                    cor = VERDE
                elif valor == CABECA:
                    cor = VERDE_ESCURO
                elif valor == MACA:
                    pygame.draw.rect(janela, PRETO, (x, y, LADO_QUADRADO, LADO_QUADRADO))  # Fundo do mapa
                    pygame.draw.rect(janela, VERMELHO, (x + LADO_QUADRADO / 3, y + LADO_QUADRADO / 3,
                                                        LADO_QUADRADO / 3, LADO_QUADRADO / 3))  # Maçã
                    pygame.draw.rect(janela, VERDE, (x + LADO_QUADRADO / 3 + 1, y + LADO_QUADRADO / 3 - 6,
                                                     LADO_QUADRADO / 6, LADO_QUADRADO / 6))  # Folha
                elif valor == VAZIO_INV:
                    cor = BRANCO

                if valor != MACA:
                    pygame.draw.rect(janela, cor, (x, y, LADO_QUADRADO, LADO_QUADRADO))  # Cobra ou fundo do mapa

                pygame.draw.line(janela, CINZA, (x, LADO_QUADRADO),
                                 (x, altura - LADO_QUADRADO), 2)  # Linhas verticais

            pygame.draw.line(janela, CINZA, (LADO_QUADRADO, (i + 1) * LADO_QUADRADO),
                             (comprimento - LADO_QUADRADO, (i + 1) * LADO_QUADRADO), 2)  # Linhas horizontais

        # Linha vertical laranja
        pygame.draw.line(janela, LARANJA, ((dimensoes_mapa['x'] + 1) * LADO_QUADRADO, LADO_QUADRADO),
                         ((dimensoes_mapa['x'] + 1) * LADO_QUADRADO, altura - LADO_QUADRADO), 2)
        # Linha horizontal laranja
        pygame.draw.line(janela, LARANJA, (LADO_QUADRADO, (dimensoes_mapa['y'] + 1) * LADO_QUADRADO),
                         (comprimento - LADO_QUADRADO, (dimensoes_mapa['y'] + 1) * LADO_QUADRADO), 2)

        # Enquanto ainda há passos/movimentos
        if qnt_movimentos < len(novas_cabecas):
            # Se não comemos uma maçã nesse passo/movimento, deleta a calda antiga
            if coord_maca.count(novas_cabecas[qnt_movimentos][0] + novas_cabecas[qnt_movimentos][1] * dimensoes_mapa['x']) == VAZIO:
                mapa[antigas_caldas[qnt_movimentos - pontos][0] + antigas_caldas[qnt_movimentos - pontos][1] * dimensoes_mapa['x']] = VAZIO
            # Se comemos, deleta a maçã comida e se ainda tiver cria uma nova
            else:
                coord_maca.remove(novas_cabecas[qnt_movimentos][0] + novas_cabecas[qnt_movimentos][1] * dimensoes_mapa['x'])

                if pontos < len(novas_macas):
                    coord_maca.append(novas_macas[pontos][0] + novas_macas[pontos][1] * dimensoes_mapa['x'])

                pontos += 1

            mapa[novas_cabecas[qnt_movimentos][0] + novas_cabecas[qnt_movimentos][1] * dimensoes_mapa['x']] = 2  # Cria nova cabeça
            mapa[antigas_cabecas[qnt_movimentos][0] + antigas_cabecas[qnt_movimentos][1] * dimensoes_mapa['x']] = 1  # Deleta cabeça antiga

            qnt_movimentos += 1

        # Velocidade da cobrinha (menor = mais rápido)
        if len(sys.argv) == 3:
            time.sleep(0.2)
        else:
            time.sleep(float(sys.argv[3]))

        # Atualizar a tela
        pygame.display.flip()


if __name__ == '__main__':
    main()
