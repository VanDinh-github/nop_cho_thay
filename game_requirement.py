class Requirement:
    def __init__(self,  CPU : str , RAM : str , GPU : str , DirectX : str = None, Storage : str =None, OS : str = None , AdditionalNotes : str=None):
        self.OS = OS
        self.CPU = CPU
        self.RAM = RAM
        self.GPU = GPU
        self.DirectX = DirectX
        self.Storage = Storage
        self.AdditionalNotes = AdditionalNotes
    def __str__(self):
        print(f'{self.OS}, {self.CPU}, {self.GPU}, {self.RAM}')
class Game:
    def __init__(self, Name: str, Minimum: Requirement, Recommended = None, Image=None):
        self.Name = Name
        self.Minimum = Minimum
        self.Recommended = Recommended
        self.Image=Image
    def __str__(self):
        return_list = [self.Name, 'Minimum configuration:',f'OS : {self.Minimum.OS}', 
                       f'CPU : {self.Minimum.CPU}', f'RAM : {self.Minimum.RAM}', f'GPU : {self.Minimum.GPU}', 
                       f'DirectX : {self.Minimum.DirectX}', f'Storage : {self.Minimum.Storage}', 
                       f'Additional Notes : {self.Minimum.AdditionalNotes}']
        return '\n'.join(return_list)