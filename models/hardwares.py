class HardWareComponent:
    def __init__(self, name, cost=None):
        self.name = name
        self.cost = cost

class CPU(HardWareComponent):
    def __init__(self, name, core_count, socket, tdp, core_clock, boost_clock, graphics=None, smt=None, price=None):
        super().__init__(name)
        self.core_count= core_count
        self.core_clock=core_clock
        self.boost_clock=boost_clock
        self.socket=socket  
        self.tdp=tdp
        self.graphics=graphics
        self.smt=smt
        self.price=price
    def __str__(self):
        return f'CPU(name={self.name}, cores={self.core_count}, clock={self.core_clock}, socket={self.socket}, tdp={self.tdp})'

class GPU(HardWareComponent):
    def __init__(self, name, memory, chipset, tdp, core_clock, boost_clock, length, color, price=None):
        super().__init__(name)
        self.vram = memory
        self.chipset = chipset
        self.tdp = tdp
        self.core_clock = core_clock
        self.boost_clock = boost_clock
        self.length = length
        self.color = color
        self.price=price

    def __str__(self):
        return f'GPU(model={self.name}, vram={self.vram}, chip_set={self.chipset}, tdp={self.tdp}, core_clock={self.core_clock}, boost_clock={self.boost_clock}, length={self.length}, color={self.color})'

class RAM:
    def __init__(self, name, capacity,  speed, ram_type, color,  price=None,  modules=None, price_per_gb=None,  first_word_latency=None, cas_latency=None):
        self.name = name
        self.capacity = capacity
        self.ram_type = ram_type
        self.speed = speed
        self.cost = price
        self.modules=modules
        self.color=color
        self.price_per_gb=price_per_gb
        self.first_word_latency=first_word_latency
        self.cas_latency=cas_latency

    def __str__(self):
        return f'RAM(name={self.name}, capacity={self.capacity}, ram_type={self.ram_type}, speed={self.speed}, cost={self.cost})'

class Mainboard:
    def __init__(self, name, socket, form_factor, chipset, ram_type, pcie_version, max_memory, memory_slots, color,  price=None):
        self.name = name
        self.socket = socket
        self.form_factor = form_factor
        self.chipset = chipset
        self.ram_type = ram_type
        self.max_memory=max_memory
        self.memory_slots=memory_slots
        self.pcie_version = pcie_version
        self.color=color
        self.price=price
    def __str__(self):
        return f'Mainboard(name={self.name}, socket={self.socket}, form_factor={self.form_factor}, chipset={self.chipset}, ram_type={self.ram_type}, pcie_slots={self.pcie_slots}, cost={self.cost})'
    
class PSU:
    def __init__(self, name, wattage, efficiency=None, color=None, price=None, type=None, modular=None ):
        self.name = name
        self.wattage = wattage
        self.efficiency = efficiency
        self.color = color
    def __str__(self):
        return f'PSU(name={self.name}, wattage={self.wattage}, efficiency={self.efficiency}, color={self.color})'

class OS:
    def __init__(self, name, price, mode, max_memory):
        self.name=name
        self.price=price
        self.mode=mode
        self.max_memory=max_memory