import pygame
import os

WIDTH, HEIGHT = 800, 600
ASSET_DIR = "assets"
FACE_DIR = os.path.join(ASSET_DIR, "faces")

CARD_W, CARD_H = 320, 190

WHITE = (255, 255, 255)
BLACK = (0,   0,   0)
GRAY = (180, 180, 180)
DARK_GRAY = (60,  60,  60)
CARD_BG = (245, 240, 220)
CARD_BORDER = (90,  70,  40)
GREEN = (50,  180, 50)
RED = (200, 50,  50)
YELLOW = (255, 220, 50)
BLUE_DARK = (30,  60,  120)
ORANGE = (220, 140, 30)


class UIManager:
    def __init__(self, screen, fonts):
        self.screen = screen
        self.fonts = fonts
        self._img_cache = {}

    def load_img(self, path, size=None):
        key = (path, size)
        if key not in self._img_cache:
            try:
                img = pygame.image.load(path).convert_alpha()
                if size:
                    img = pygame.transform.scale(img, size)
            except Exception:
                img = pygame.Surface(size or (64, 64), pygame.SRCALPHA)
                img.fill((200, 100, 200, 180))
            self._img_cache[key] = img
        return self._img_cache[key]

    def _make_grayscale(self, surface):
        return pygame.transform.grayscale(surface)

    def _center_x(self, surf, offset_x=0):
        return WIDTH // 2 - surf.get_width() // 2 + offset_x

    def draw_visitor(self, visitor):
        char_w, char_h = 200, 200
        baseline_y = 300
        center_x = (123 + 660) // 2

        actual_photo = getattr(visitor, "display_photo",
                               None) or visitor.id_card.get("photo_id", "")
        actual_path = os.path.join(FACE_DIR, actual_photo)
        face_img = self.load_img(actual_path, (char_w, char_h))

        fx = center_x - char_w // 2
        fy = baseline_y - char_h
        self.screen.blit(face_img, (fx, fy))

    def draw_id_card(self, visitor, pos):
        cx, cy = pos

        shadow = pygame.Surface((CARD_W, CARD_H), pygame.SRCALPHA)
        shadow.fill((0, 0, 0, 80))
        self.screen.blit(shadow, (cx + 5, cy + 5))

        pygame.draw.rect(self.screen, CARD_BG,
                         (cx, cy, CARD_W, CARD_H), border_radius=6)
        pygame.draw.rect(self.screen, CARD_BORDER,
                         (cx, cy, CARD_W, CARD_H), width=3, border_radius=6)
        pygame.draw.rect(self.screen, BLUE_DARK,
                         (cx, cy, CARD_W, 30),     border_radius=6)

        header = self.fonts["small"].render(
            "DORMITORY RESIDENT ID", True, WHITE)
        self.screen.blit(header, (cx + CARD_W // 2 -
                         header.get_width() // 2, cy + 7))

        photo_x, photo_y = cx + 15, cy + 45
        photo_path = os.path.join(
            FACE_DIR, visitor.id_card.get("photo_id", ""))
        face_img = self.load_img(photo_path, (90, 90))
        pygame.draw.rect(self.screen, DARK_GRAY,
                         (photo_x - 2, photo_y - 2, 94, 94))
        self.screen.blit(face_img, (photo_x, photo_y))

        tx, ty, gap = cx + 120, cy + 40, 32
        fields = [
            ("Name", visitor.id_card.get("name",      "—")),
            ("Room", visitor.id_card.get("room",       "—")),
            ("ID",   visitor.id_card.get("student_id", "—")),
        ]
        for label, value in fields:
            lbl = self.fonts["small"].render(f"{label}:", True, DARK_GRAY)
            val = self.fonts["normal"].render(str(value),  True, BLACK)
            self.screen.blit(lbl, (tx,      ty))
            self.screen.blit(val, (tx + 65, ty))
            ty += gap

        hint = self.fonts["tiny"].render(
            "[drag to move  |  click outside to close]", True, GRAY)
        self.screen.blit(
            hint, (cx + CARD_W // 2 - hint.get_width() // 2, cy + CARD_H - 22))

    def draw_resident_list(self, residents):
        panel_w, panel_h = 340, 420
        px = WIDTH - panel_w - 10
        py = (HEIGHT - panel_h) // 2

        panel_surf = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        panel_surf.fill((20, 15, 10, 220))
        self.screen.blit(panel_surf, (px, py))
        pygame.draw.rect(self.screen, CARD_BORDER,
                         (px, py, panel_w, panel_h), width=2, border_radius=4)

        title = self.fonts["small"].render("RESIDENT LIST", True, YELLOW)
        self.screen.blit(title, (px + panel_w // 2 -
                         title.get_width() // 2, py + 8))
        pygame.draw.line(self.screen, CARD_BORDER,
                         (px + 5, py + 28), (px + panel_w - 5, py + 28), 1)

        row_h = 75
        for i, res in enumerate(residents):
            ry = py + 35 + i * row_h
            photo_path = os.path.join(FACE_DIR, res.photo_id or "")
            face_gray = self._make_grayscale(
                self.load_img(photo_path, (55, 55)))
            self.screen.blit(face_gray, (px + 8, ry + 5))

            name_s = self.fonts["small"].render(res.name, True, WHITE)
            room_s = self.fonts["tiny"].render(
                f"Room: {res.room}  ID: {res.student_id}", True, GRAY)
            self.screen.blit(name_s, (px + 72, ry + 8))
            self.screen.blit(room_s, (px + 72, ry + 30))

            if i < len(residents) - 1:
                pygame.draw.line(self.screen, DARK_GRAY,
                                 (px + 5,          ry + row_h - 3),
                                 (px + panel_w - 5, ry + row_h - 3), 1)

        hint = self.fonts["tiny"].render(
            "[click DATA folder to toggle]", True, GRAY)
        self.screen.blit(hint, (px + panel_w // 2 -
                         hint.get_width() // 2, py + panel_h - 18))

    def draw_hud(self, gm):
        sc = self.fonts["normal"].render(f"Score: {gm.score}", True, WHITE)
        self.screen.blit(sc, (WIDTH - sc.get_width() - 10, 10))

        rd = self.fonts["normal"].render(f"Round: {gm.round_num}", True, WHITE)
        self.screen.blit(rd, (WIDTH - rd.get_width() - 10, 34))

        heart_str = "♥ " * gm.lives + "♡ " * (3 - gm.lives)
        hv = self.fonts["normal"].render(heart_str, True, RED)
        self.screen.blit(hv, (10, 10))

        diff_names = {1: "Easy", 2: "Normal", 3: "Hard"}
        dv = self.fonts["tiny"].render(
            f"Difficulty: {diff_names.get(gm.difficulty, '?')}", True, GRAY)
        self.screen.blit(dv, (10, 34))

    def draw_feedback(self, correct, timer):
        if timer <= 0:
            return
        alpha = min(255, timer * 6)
        color = GREEN if correct else RED
        text = "CORRECT!" if correct else "WRONG!"
        surf = self.fonts["big"].render(text, True, color)
        surf.set_alpha(alpha)
        self.screen.blit(
            surf, (WIDTH // 2 - surf.get_width() // 2, HEIGHT // 2 - 60))

    def draw_hint_bar(self):
        hint = self.fonts["tiny"].render(
            "A = Allow   D = Deny   |   Click I.D. card or DATA folder to inspect",
            True, GRAY
        )
        self.screen.blit(
            hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 18))

    def title_screen(self, bg, clock, fps=60):
        while True:
            self.screen.blit(bg, (0, 0))
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            self.screen.blit(overlay, (0, 0))

            title = self.fonts["big"].render(
                "Who is Your Neighbor?", True, YELLOW)
            sub = self.fonts["small"].render(
                "Press ENTER or SPACE to start", True, WHITE)
            quit_ = self.fonts["tiny"].render("Press Q to quit", True, GRAY)

            self.screen.blit(title, (self._center_x(title), 200))
            self.screen.blit(sub,   (self._center_x(sub),   300))
            self.screen.blit(quit_, (self._center_x(quit_), 560))
            pygame.display.flip()
            clock.tick(fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        return
                    if event.key == pygame.K_q:
                        pygame.quit()
                        raise SystemExit

    def difficulty_screen(self, bg, clock, fps=60):
        options = ["Easy", "Normal", "Hard"]
        selected = 0
        btn_w, btn_h = 180, 50
        btn_gap = 24
        total_w = len(options) * btn_w + (len(options) - 1) * btn_gap
        start_x = WIDTH // 2 - total_w // 2
        btn_y = HEIGHT // 2 + 20

        btn_rects = [
            pygame.Rect(start_x + i * (btn_w + btn_gap), btn_y, btn_w, btn_h)
            for i in range(len(options))
        ]
        btn_colors = [GREEN, ORANGE, RED]
        btn_selected = [(min(c[0] + 60, 255), min(c[1] + 60, 255), min(c[2] + 60, 255))
                        for c in btn_colors]

        while True:
            self.screen.blit(bg, (0, 0))
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            self.screen.blit(overlay, (0, 0))

            title = self.fonts["big"].render("Select Difficulty", True, YELLOW)
            self.screen.blit(title, (self._center_x(title), 160))

            desc_map = {
                0: "Obvious errors — great for beginners",
                1: "Moderate errors — balanced challenge",
                2: "Subtle errors — for sharp eyes only",
            }
            desc = self.fonts["small"].render(desc_map[selected], True, GRAY)
            self.screen.blit(desc, (self._center_x(desc), 240))

            hint = self.fonts["tiny"].render(
                "← → Arrow Keys to select   ENTER to confirm", True, GRAY)
            self.screen.blit(hint, (self._center_x(hint), HEIGHT - 40))

            for i, rect in enumerate(btn_rects):
                color = btn_selected[i] if i == selected else btn_colors[i]
                pygame.draw.rect(self.screen, color, rect, border_radius=8)
                if i == selected:
                    pygame.draw.rect(self.screen, WHITE, rect,
                                     width=3, border_radius=8)
                label = self.fonts["normal"].render(
                    options[i], True, BLACK if i != selected else WHITE)
                self.screen.blit(label, (rect.centerx - label.get_width() // 2,
                                         rect.centery - label.get_height() // 2))

            pygame.display.flip()
            clock.tick(fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        selected = (selected - 1) % len(options)
                    elif event.key == pygame.K_RIGHT:
                        selected = (selected + 1) % len(options)
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        return selected + 1
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        raise SystemExit
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i, rect in enumerate(btn_rects):
                        if rect.collidepoint(event.pos):
                            selected = i
                            return selected + 1

    def stats_screen(self, clock, fps=60):
        import io
        import matplotlib.pyplot as plt
        import generate_graphs as gg

        BG_C      = (30,  30,  46)
        SIDEBAR_C = (42,  42,  62)
        ACCENT_C  = (74,  144, 217)
        TEXT_C    = (205, 214, 244)
        MUTED_C   = (100, 110, 140)

        SIDEBAR_W = 185
        BTN_H     = 44
        BTN_GAP   = 6

        df, err = gg.load_data()

        if err:
            while True:
                self.screen.fill(BG_C)
                msg  = self.fonts["normal"].render("No stats yet — play a game first.", True, RED)
                hint = self.fonts["tiny"].render("Press any key or click to go back", True, MUTED_C)
                self.screen.blit(msg,  (WIDTH // 2 - msg.get_width()  // 2, HEIGHT // 2 - 20))
                self.screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 14))
                pygame.display.flip()
                clock.tick(fps)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        raise SystemExit
                    if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                        return
            return

        graph_defs = [
            ("Decision Time",     gg.graph_decision_time_histogram),
            ("Error Types",       gg.graph_error_type_pie),
            ("Accuracy & Time",   gg.graph_accuracy_and_time_per_round),
            ("Score Progression", gg.graph_score_progression),
            ("Summary",           None),
        ]

        cache    = {}
        selected = 0
        summary  = gg.build_summary_text(df)

        def get_surf(idx):
            if idx not in cache:
                _, builder = graph_defs[idx]
                fig = builder(df)
                buf = io.BytesIO()
                fig.savefig(buf, format="png", dpi=90, bbox_inches="tight")
                plt.close(fig)
                buf.seek(0)
                cache[idx] = pygame.image.load(buf).convert()
            return cache[idx]

        start_y   = 54
        btn_rects = [
            pygame.Rect(8, start_y + i * (BTN_H + BTN_GAP), SIDEBAR_W - 16, BTN_H)
            for i in range(len(graph_defs))
        ]
        save_rect = pygame.Rect(8, HEIGHT - 104, SIDEBAR_W - 16, 44)
        back_rect = pygame.Rect(8, HEIGHT -  54, SIDEBAR_W - 16, 44)
        graph_area = pygame.Rect(SIDEBAR_W + 4, 4, WIDTH - SIDEBAR_W - 8, HEIGHT - 8)

        while True:
            self.screen.fill(BG_C)
            pygame.draw.rect(self.screen, SIDEBAR_C, (0, 0, SIDEBAR_W, HEIGHT))

            title_s = self.fonts["small"].render("STATISTICS", True, ACCENT_C)
            self.screen.blit(title_s, (SIDEBAR_W // 2 - title_s.get_width() // 2, 14))
            pygame.draw.line(self.screen, (55, 55, 80), (8, 40), (SIDEBAR_W - 8, 40))

            mx, my = pygame.mouse.get_pos()

            for i, (label, _) in enumerate(graph_defs):
                r   = btn_rects[i]
                sel = (i == selected)
                hov = r.collidepoint(mx, my)
                if sel:
                    pygame.draw.rect(self.screen, ACCENT_C, r, border_radius=5)
                    fc = WHITE
                elif hov:
                    pygame.draw.rect(self.screen, (55, 95, 150), r, border_radius=5)
                    fc = WHITE
                else:
                    fc = TEXT_C
                ls = self.fonts["tiny"].render(label, True, fc)
                self.screen.blit(ls, (r.centerx - ls.get_width() // 2,
                                      r.centery - ls.get_height() // 2))

            for rect, txt, base_c in [
                (save_rect, "Save All", (40, 110, 40)),
                (back_rect, "Back",     (110, 40, 40)),
            ]:
                c = tuple(min(v + 35, 255) for v in base_c) if rect.collidepoint(mx, my) else base_c
                pygame.draw.rect(self.screen, c, rect, border_radius=5)
                ls = self.fonts["tiny"].render(txt, True, WHITE)
                self.screen.blit(ls, (rect.centerx - ls.get_width() // 2,
                                      rect.centery - ls.get_height() // 2))

            _, builder = graph_defs[selected]
            if builder is None:
                y = graph_area.y + 10
                for line in summary.split("\n"):
                    s = self.fonts["small"].render(line, True, TEXT_C)
                    self.screen.blit(s, (graph_area.x + 10, y))
                    y += 24
            else:
                if selected not in cache:
                    ld = self.fonts["normal"].render("Rendering...", True, TEXT_C)
                    self.screen.blit(ld, (graph_area.centerx - ld.get_width() // 2,
                                          graph_area.centery - ld.get_height() // 2))
                    pygame.display.flip()
                    get_surf(selected)

                surf = cache.get(selected)
                if surf:
                    sw, sh = surf.get_size()
                    scale  = min(graph_area.width / sw, graph_area.height / sh)
                    nw, nh = int(sw * scale), int(sh * scale)
                    scaled = pygame.transform.smoothscale(surf, (nw, nh))
                    gx = graph_area.x + (graph_area.width  - nw) // 2
                    gy = graph_area.y + (graph_area.height - nh) // 2
                    self.screen.blit(scaled, (gx, gy))

            hint_s = self.fonts["tiny"].render(
                "<- -> to switch   |   ESC / Back to return   |   S to save all", True, MUTED_C)
            self.screen.blit(hint_s, (SIDEBAR_W + 10, HEIGHT - 16))

            pygame.display.flip()
            clock.tick(fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_b):
                        return
                    if event.key == pygame.K_LEFT:
                        selected = (selected - 1) % len(graph_defs)
                    if event.key == pygame.K_RIGHT:
                        selected = (selected + 1) % len(graph_defs)
                    if event.key == pygame.K_s:
                        gg.save_all(df)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i, r in enumerate(btn_rects):
                        if r.collidepoint(event.pos):
                            selected = i
                    if back_rect.collidepoint(event.pos):
                        return
                    if save_rect.collidepoint(event.pos):
                        gg.save_all(df)

    def game_over_screen(self, result, clock, fps=60):
        btn_w, btn_h = 180, 50
        btn_gap = 20
        btn_y = 380

        btn_defs = [
            ("Restart",    GREEN,              "restart"),
            ("View Stats", (74, 144, 217),     "stats"),
            ("Quit",       RED,                "quit"),
        ]
        total_w = len(btn_defs) * btn_w + (len(btn_defs) - 1) * btn_gap
        start_x = WIDTH // 2 - total_w // 2
        buttons = [
            {"label": lbl, "color": col, "action": act,
             "rect": pygame.Rect(start_x + i * (btn_w + btn_gap), btn_y, btn_w, btn_h)}
            for i, (lbl, col, act) in enumerate(btn_defs)
        ]

        while True:
            self.screen.fill((10, 10, 20))

            mx, my = pygame.mouse.get_pos()

            title  = self.fonts["big"].render("GAME OVER", True, RED)
            score  = self.fonts["normal"].render(f"Final Score:   {result['score']}", True, WHITE)
            rounds = self.fonts["normal"].render(f"Rounds Played: {result['rounds']}", True, WHITE)
            hint   = self.fonts["tiny"].render("R / S / Q to use keyboard", True, DARK_GRAY)

            self.screen.blit(title,  (self._center_x(title),  160))
            self.screen.blit(score,  (self._center_x(score),  265))
            self.screen.blit(rounds, (self._center_x(rounds), 300))
            self.screen.blit(hint,   (self._center_x(hint),   460))

            for btn in buttons:
                hovered = btn["rect"].collidepoint(mx, my)
                color = tuple(min(c + 50, 255) for c in btn["color"]) if hovered else btn["color"]
                pygame.draw.rect(self.screen, color, btn["rect"], border_radius=8)
                if hovered:
                    pygame.draw.rect(self.screen, WHITE, btn["rect"], width=2, border_radius=8)
                lbl = self.fonts["normal"].render(btn["label"], True, WHITE)
                self.screen.blit(lbl, (btn["rect"].centerx - lbl.get_width() // 2,
                                       btn["rect"].centery - lbl.get_height() // 2))

            pygame.display.flip()
            clock.tick(fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for btn in buttons:
                        if btn["rect"].collidepoint(event.pos):
                            if btn["action"] == "restart":
                                return True
                            elif btn["action"] == "quit":
                                pygame.quit()
                                raise SystemExit
                            elif btn["action"] == "stats":
                                self.stats_screen(clock, fps)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        raise SystemExit
                    if event.key == pygame.K_r:
                        return True
                    if event.key == pygame.K_s:
                        self.stats_screen(clock, fps)
