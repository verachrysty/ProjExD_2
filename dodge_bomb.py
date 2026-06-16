import os
import sys
import time 
import random 
import math
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = { # first exercice 
            pg.K_RIGHT : (+5, 0),
            pg.K_LEFT : (-5, 0),
            pg.K_DOWN : (0, +5),
            pg.K_UP : (0, -5),
}

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def gameover(screen: pg.surface) -> None:
    black_scr = pg.Surface((WIDTH, HEIGHT))
    black_scr.fill((0,0,0))
    black_scr.set_alpha(150)

    font = pg.font.Font(None, 80)
    txt_surface = font.render("Game Over", True, (255, 255, 255))
    txt_rect = txt_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    
    cry_kk_img = pg.image.load("fig/8.png")
    cry_kk_rct1 = cry_kk_img.get_rect(center=(WIDTH // 2 - 200, HEIGHT // 2))
    cry_kk_rct2 = cry_kk_img.get_rect(center=(WIDTH // 2 + 200, HEIGHT // 2))
    
    black_scr.blit(txt_surface, txt_rect)
    black_scr.blit(cry_kk_img, cry_kk_rct1)
    black_scr.blit(cry_kk_img, cry_kk_rct2)
    
    screen.blit(black_scr, (0, 0))
    pg.display.update()
    time.sleep(5)

    
def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
       
    bb_imgs = []
    bb_accs = [a for a in range(1, 11)]
    
    for r in range(1, 11):
        bb_img = pg.Surface((20 * r, 20 * r))
        bb_img.set_colorkey((0, 0, 0))
        pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)
        bb_imgs.append(bb_img)
            
    return bb_imgs, bb_accs


def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    base_img = pg.image.load("fig/3.png")
    kk_left = pg.transform.rotozoom(base_img, 0, 0.9)
    kk_right = pg.transform.flip(kk_left, True, False)
    
    kk_dict = {
        (0, 0): kk_left,
        (-5, 0): kk_left,
        (-5, -5): pg.transform.rotozoom(kk_left, -45, 1.0),
        (0, -5): pg.transform.rotozoom(kk_right, 90, 1.0),
        (+5, -5): pg.transform.rotozoom(kk_right, 45, 1.0),
        (+5, 0): kk_right,
        (+5, +5): pg.transform.rotozoom(kk_right, -45, 1.0),
        (0, +5): pg.transform.rotozoom(kk_right, -90, 1.0),
        (-5, +5): pg.transform.rotozoom(kk_left, 45, 1.0),
    }
    return kk_dict
#exercice 4
def calc_orientation(org: pg.Rect, dst: pg.Rect, current_xy: tuple[float, float]) -> tuple[float, float]:
    """
    引数のこうかとんのRectと爆弾のRectから、爆弾の次の移動速度ベクトルを計算する関数
    """
   
    dx = dst.centerx - org.centerx
    dy = dst.centery - org.centery
    dist = math.sqrt(dx**2 + dy**2)
    if dist < 300:
        return current_xy
    norm = math.sqrt(50)
    vx = (dx / dist) * norm
    vy = (dy / dist) * norm
    return vx, vy


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRect or 爆弾Rect
    戻り値：判定結果タプル（横方向判定結果，縦方向判定結果）
    True：画面内／False：画面外
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom: 
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg") 
    kk_imgs = get_kk_imgs()
    kk_img = kk_imgs[(0, 0)]
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200



    bb_img= pg.Surface((20,20))
    bb_img.set_colorkey((0,0,0))
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)
    
    bb_imgs, bb_accs = init_bb_imgs()
    bb_img= bb_imgs[0]
    bb_rct=bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery= random.randint(0, HEIGHT)
    vx, vy = +5, +5

    bb_img.set_colorkey((0,0,0))
    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct): 
            print("ゲームオーバー")
            gameover(screen)

            return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        for key, mv in DELTA.items(): # first exercice 
            if key_lst[key]:
                sum_mv[0] += mv[0]  
                sum_mv[1] += mv[1] 
        kk_rct.move_ip(sum_mv)
        kk_img = kk_imgs[tuple(sum_mv)]
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) 
        screen.blit(kk_img, kk_rct)

        vx,vy= calc_orientation(bb_rct, kk_rct, (vx, vy))
        
        idx= min(tmr // 500, 9)
        bb_img = bb_imgs[idx]
        orig_center = bb_rct.center
        bb_rct = bb_img.get_rect()
        bb_rct.center = orig_center
        avx = vx * bb_accs[idx]
        avy = vy* bb_accs[idx]
        bb_rct.move_ip(avx, avy)
        yoko, tate = check_bound(bb_rct)
        if not yoko: 
            vx *= -1
            bb_rct.move_ip(vx*2, 0)
        if not tate: 
            vy *= -1
            bb_rct.move_ip(0, vy*2)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
