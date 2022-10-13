import os
import zlib

from binaryReader import BinaryReader
from decrypt import decrypt

class PAC6_FILE:

    def __init__(self) -> None:
        
        self.m_entries = []

    class ENTRY:

        def __init__(self) -> None:
            
            self.tome = 0
            self.compressed = False
            self.offset = 0
            self.size = 0
            self.unpacked_size = 0

        def read(self, br, info):
            self.tome = info.c[0]
            self.compressed = info.c[1] == 1
            self.offset = br.readUInt()
            self.size = br.readUInt()
            self.unpacked_size = br.readUInt()

    class INFO:

        def __init__(self) -> None:
            self.c = ""
            self.u = 0

        def read(self, br):
            self.c = br.readBytes(4)

    def open(self, br, tbl_path):

        tbl_file = open(tbl_path, 'rb')
        tbl_br = BinaryReader(tbl_file, ">")
        tbl_size = os.path.getsize(tbl_path) // 4

        count = tbl_br.readUInt()
        tomes_count = tbl_br.readUInt()

        #for i in range(tomes_count):

        for i in range(count):

            info = PAC6_FILE.INFO()
            info.read(tbl_br)

            entry = PAC6_FILE.ENTRY()
            entry.read(tbl_br, info)

            self.m_entries.append(entry)

        print("test")

    def read_file_data(self, br, idx):

        e = self.m_entries[idx]

        if not e.compressed:

            br.seek(e.offset, 0)
            buf = br.readBytes(e.size)

            data = decrypt(bytearray(buf), e.size, idx % 256)
            return data

        br.seek(e.offset, 0)
        buf = br.readBytes(e.size)
        data = decrypt(bytearray(buf), e.size, idx % 256)
        data = zlib.decompress(data)
        return data
        

