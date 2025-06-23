from models.hardwares import CPU, GPU, RAM, Mainboard, PSU, OS

class PC:
    def __init__(self, cpu : CPU, gpu: GPU, ram : RAM, mainboard : Mainboard, psu : PSU, os, cost=None):
        self.cpu=cpu
        self.gpu=gpu
        self.ram=ram
        self.mainboard=mainboard
        self.psu=psu
        self.os=os
        self.cost=cost
    def check_compatible(self):
        if self.cpu.socket != 'None' and self.cpu.socket != self.mainboard.socket:
            return "Lỗi: Socket CPU ({}) không tương thích với Mainboard ({})".format(self.cpu.socket, self.mainboard.socket)
        elif self.ram.ram_type not in self.mainboard.ram_type:
            return "Lỗi: Loại RAM ({}) không tương thích với Mainboard ({})".format(self.ram.ram_type, self.mainboard.ram_type)
        elif self.cpu.tdp + self.gpu.tdp + 100 > self.psu.wattage:
            return "Lỗi: Công suất PSU ({:.0f}W) không đủ (cần tối thiểu {:.0f}W)".format(self.psu.wattage, self.cpu.tdp + self.gpu.tdp + 100)
        else:
            return "Cấu hình tương thích!"

    def __str__(self):
        return f'PC(cpu={self.cpu}, gpu={self.gpu}, ram={self.ram}, mainboard={self.mainboard}, psu={self.psu}, os={self.os}, cost={self.cost})'
    def get_cpu(self):
        pass
    def get_gpu(self):
        pass
    def get_ram(self):
        pass
    def get_mainboard(self):
        pass
    def get_psu(self):
        pass
    def get_os(self):
        pass
    def total_cost(self):
        pass


