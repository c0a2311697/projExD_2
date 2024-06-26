import os
import random
import sys
import pygame
import pygame as pg


WIDTH, HEIGHT = 1600, 900
DELTA = {  # 移動量辞書
         pg.K_UP:(0, -5), 
         pg.K_DOWN:(0, +5), 
         pg.K_LEFT:(-5, 0), 
         pg.K_RIGHT:(+5, 0),
        }
angle = 0
direction = {
             pg.K_LEFT:0,
             pg.K_LEFT and pg.K_DOWN:45,
             pg.K_UP:90,
             pg.K_LEFT and pg.K_UP:-45,
             pg.K_DOWN:-90,
             pg.K_RIGHT:0,
             pg.K_RIGHT and pg.K_UP :45,
             pg.K_RIGHT and pg.K_DOWN:-45,
             }

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:

    """
    引数：こうかとんRect,　または,ばくだんRect
    戻り値：真理値タプル(横方向, 縦方向)
    画面内ならTure／画面外ならFalse
    """
    box_x, box_y = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向判定
        box_x = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向判定
        box_y = False
    return box_x, box_y


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bb_img = pg.Surface((20, 20))  # 1辺が20の空のSurfaceを作る
    bb_img.set_colorkey(0, 0)
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 空のSurfaceに赤い円を描く
    bb_rct = bb_img.get_rect()  # 爆弾rect
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            rect = pg.Surface((WIDTH, HEIGHT))  
            pg.draw.rect(0, 0, WIDTH/2, HEIGHT/2)  # ゲームオーバー画面のブラックアウト
            # return  # ゲームオーバー
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        for rot_k, rot_v in direction.items():
             # 向いている方向の変更
             if key_lst[rot_k] and key_lst[rot_k]:
                 kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), rot_v, 2.0)
             # 以下こうかとんの反転
             fleft = True
             kk_img = pg.transform.flip(kk_img, True, False)
             if key_lst[pg.K_LEFT]:
                if fleft == False:
                     kk_img = pg.transform.flip(kk_img, True, False)
                     fleft = True
             if key_lst[pg.K_RIGHT] or key_lst[pg.K_UP] or key_lst[pg.K_DOWN]:
                if fleft == True:
                     kk_img = pg.transform.flip(kk_img, True, False)
                     fleft = False
        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(vx, vy)
        box_x, box_y = check_bound(bb_rct)
        if not box_x:  # 横方向にはみ出たら
            vx *= -1
        if not box_y:  # 縦方向にはみ出たら
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
