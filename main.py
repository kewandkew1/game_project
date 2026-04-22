import pygame
import sys
import os
from game_manage import GameManager
from ui_manager import UIManager

WIDTH, HEIGHT = 800, 600
FPS = 60
ASSET_DIR = "assets"

ALLOW_RECT = pygame.Rect(45,  428, 55, 28)
DENY_RECT = pygame.Rect(106, 428, 55, 28)
ID_CARD_RECT = pygame.Rect(354, 360, 54, 33)
DATA_RECT = pygame.Rect(515, 391, 131, 86)

CARD_W, CARD_H = 320, 190

GRAY = (180, 180, 180)


def run():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Who is Your Neighbor?")
    clock = pygame.time.Clock()

    fonts = {
        "big":    pygame.font.SysFont("Arial", 42, bold=True),
        "normal": pygame.font.SysFont("Arial", 20),
        "small":  pygame.font.SysFont("Arial", 16),
        "tiny":   pygame.font.SysFont("Arial", 13),
    }

    bg_path = os.path.join(ASSET_DIR, "Black_ground.png")
    try:
        bg = pygame.image.load(bg_path).convert()
        bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    except Exception:
        bg = pygame.Surface((WIDTH, HEIGHT))
        bg.fill((40, 30, 30))

    ui = UIManager(screen, fonts)

    ui.title_screen(bg, clock, FPS)
    starting_difficulty = ui.difficulty_screen(bg, clock, FPS)

    while True:
        gm = GameManager(starting_difficulty=starting_difficulty)
        gm.next_round()

        show_card = False
        show_list = False
        feedback_timer = 0
        last_correct = True
        waiting = False

        card_pos = [(WIDTH - CARD_W) // 2, (HEIGHT - CARD_H) // 2 + 20]
        dragging_card = False
        drag_offset = (0, 0)

        running = True
        while running:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gm.game_over()
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        gm.game_over()
                        pygame.quit()
                        sys.exit()

                    if not waiting:
                        if event.key == pygame.K_a:
                            last_correct = gm.check_decision("ALLOW")
                            gm.update_difficulty()
                            feedback_timer = 60
                            waiting = True
                            show_card = False
                        elif event.key == pygame.K_d:
                            last_correct = gm.check_decision("DENY")
                            gm.update_difficulty()
                            feedback_timer = 60
                            waiting = True
                            show_card = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos

                    if show_card:
                        card_rect = pygame.Rect(
                            card_pos[0], card_pos[1], CARD_W, CARD_H)
                        if card_rect.collidepoint(mx, my):
                            dragging_card = True
                            drag_offset = (mx - card_pos[0], my - card_pos[1])
                            continue

                    if not waiting and ALLOW_RECT.collidepoint(mx, my):
                        last_correct = gm.check_decision("ALLOW")
                        gm.update_difficulty()
                        feedback_timer = 60
                        waiting = True
                        show_card = False

                    elif not waiting and DENY_RECT.collidepoint(mx, my):
                        last_correct = gm.check_decision("DENY")
                        gm.update_difficulty()
                        feedback_timer = 60
                        waiting = True
                        show_card = False

                    elif ID_CARD_RECT.collidepoint(mx, my):
                        show_card = not show_card
                        if show_card:
                            card_pos = [(WIDTH - CARD_W) // 2,
                                        (HEIGHT - CARD_H) // 2 + 20]

                    elif DATA_RECT.collidepoint(mx, my):
                        show_list = not show_list

                    else:
                        if show_card:
                            card_rect = pygame.Rect(
                                card_pos[0], card_pos[1], CARD_W, CARD_H)
                            if not card_rect.collidepoint(mx, my):
                                show_card = False
                        if show_list:
                            show_list = False

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    dragging_card = False

                if event.type == pygame.MOUSEMOTION and dragging_card:
                    mx, my = event.pos
                    card_pos[0] = mx - drag_offset[0]
                    card_pos[1] = my - drag_offset[1]
                    card_pos[0] = max(0, min(WIDTH - CARD_W, card_pos[0]))
                    card_pos[1] = max(0, min(HEIGHT - CARD_H, card_pos[1]))

            if feedback_timer > 0:
                feedback_timer -= 1

            if feedback_timer == 0 and waiting:
                if gm.is_game_over():
                    result = gm.game_over()
                    restart = ui.game_over_screen(result, clock, FPS)
                    if restart:
                        starting_difficulty = ui.difficulty_screen(
                            bg, clock, FPS)
                        running = False
                    else:
                        pygame.quit()
                        sys.exit()
                else:
                    gm.next_round()
                    waiting = False

            screen.blit(bg, (0, 0))

            if gm.current_visitor:
                ui.draw_visitor(gm.current_visitor)

            ui.draw_hud(gm)

            if show_card and gm.current_visitor:
                ui.draw_id_card(gm.current_visitor, card_pos)

            if show_list:
                ui.draw_resident_list(gm.residents)

            ui.draw_feedback(last_correct, feedback_timer)
            ui.draw_hint_bar()

            pygame.display.flip()


if __name__ == "__main__":
    run()
