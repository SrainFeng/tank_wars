import pygame


class TankSprite(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        # 目标 surface ，该精灵会贴入目标 surface
        self.target_surface = screen
        # 该精灵的总图像
        self.master_image = None
        # 每一帧的宽和高
        self.frame_width = 0
        self.frame_height = 0
        # 当前帧的图像与序号
        self.image = None
        self.frame = 0
        # 记录上一帧的变量
        self.old_frame = -1
        # 首帧与尾帧的位置
        self.frist_frame = 0
        self.last_frame = 0
        # 记录上一帧播放的时间
        self.last_time = 0
        # 记录总图像帧的列数
        self.columns = 1
        # 记录精灵的位置的矩形
        self.rect = None
        self.speed = 0

        # 要求使用参数初始化一些类的属性
    def load(self, image_name, width, height, column):
        self.master_image = pygame.image.load(image_name).convert_alpha()
        self.frame_width = width
        self.frame_height = height
        self.columns = column
        master_size = self.master_image.get_rect()
        self.last_frame = (master_size.width // width) * (master_size.height // height) - 1

    def update(self):
        pass
