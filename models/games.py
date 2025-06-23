class Requirement:
    def __init__(self, cpu, gpu, ram, vram, free_disk_space, os):
        self.cpu = cpu
        self.gpu = gpu
        self.ram = ram
        self.vram = vram
        self.free_disk_space = free_disk_space
        self.os=os

class GameRequirement(Requirement):
    def __init__(self, cpu, gpu, ram, vram, free_disk_space, requirement_type):
        super().__init__(cpu, gpu, ram, vram, free_disk_space)
        self.requirement_type=requirement_type
    