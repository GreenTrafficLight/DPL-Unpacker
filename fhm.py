from binaryReader import *

class FHM():

    def __init__(self) -> None:
        pass

    class HEADER():

        def __init__(self) -> None:
            self.sign = ""
            self.byte_order_20101010 = 0
            self.timestamp = 0
            self.unknown_struct_count = 0

            self.unknown = 0
            self.size = 0
            self.unknown3 = 0
            self.unknown4 = 0
            self.unknown5 = 0
            self.unknown_16 = 0
            self.unknown_pot = 0
            self.unknown_pot2 = 0

        def read(self , br):

            self.sign = br.bytesToString(br.readBytes(4)).replace("\0", "")
            self.byte_order_20101010 = br.readUInt()
            self.timestamp = br.readUInt()
            self.unknown_struct_count = br.readUInt()
            
            self.unknown = br.readUInt()
            self.size = br.readUInt()
            self.unknown3 = br.readUInt()
            self.unknown4 = br.readUInt()
            self.unknown5 = br.readUInt()
            self.unknown_16 = br.readUInt()
            self.unknown_pot = br.readUInt()
            self.unknown_pot2 = br.readUInt()