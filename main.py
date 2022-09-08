from map import Map
from camera import Camera
import settings
import pygame


def main():
    pygame.init()
    screen = pygame.display.set_mode(
        (settings.width, settings.height))
    time = pygame.time.Clock()

    map = Map()

    camera = Camera(map, 0, 0)
    map.set_camera(camera)

    running = True
    while running:
        time.tick(settings.fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            map.player.key_event(event, map)

        map.update()
        map.player.update_camera_pos(map.camera)

        # TODO: поменять цвет фона
        screen.fill("#000000")
        map.draw(screen)

        map.log.draw(screen)

        pygame.display.flip()
    # to do: сохранение
    pygame.quit()


main()
