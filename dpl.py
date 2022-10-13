from email import header
import zlib

from binaryReader import *

from decrypt import *
from fhm import *

class DPL():

    def __init__(self) -> None:
        
        self.m_infos = []

        self.m_byte_order = False
        self.m_archieved = False

    class INFO():

        def __init__(self) -> None:
            self.header = None
            self.offset = 0
            self.size = 0
            self.unpacked_size = 0
            self.key = 0

    class HEADER():

        def __init__(self) -> None:
            self.sign = ""
            self.byte_order_20101010 = 0
            self.timestamp = 0
            self.infos_count = 0
            self.infos_size = 0

        def read(self, br):

            self.sign = br.bytesToString(br.readBytes(4)).replace("\0", "")
            self.byte_order_20101010 = br.readUInt()
            self.timestamp = br.readUInt()
            self.infos_count = br.readUInt()
            self.infos_size = br.readUInt()

    class ENTRY():

        def __init__(self) -> None:
            self.offset = 0
            self.size = 0
            self.idx = 0
            self.unknown = 0
            self.key = 0

        def read(self, br):
            self.offset = br.readULongLong()
            self.size = br.readUInt()
            self.idx = br.readUInt()
            self.unknown = br.readUInt()
            self.key = br.readUShort()
            br.seek(2, 1)

    class UNKNOWN_STRUCT():

        def __init__(self) -> None:
            self.idx = 0
            self.unknown = 0
            self.unknown_pot = 0

        def read(self, br):
            self.idx = br.readUInt()
            self.unknown = br.readUInt()
            self.unknown_pot = br.readUInt()

    def open(self, br):

        header = DPL.HEADER()
        header.read(br)

        self.m_byte_order = header.byte_order_20101010 != 20101010
        if (self.m_byte_order):
            pass

        assert header.byte_order_20101010 == 20101010

        self.m_archieved = header.timestamp != 2011082201

        for i in range(header.infos_count):
            m_info = DPL.INFO()
            self.m_infos.append(m_info)

        for i in range(header.infos_count):

            #print(br.tell())
            
            h = FHM.HEADER()
            h.read(br)

            e = DPL.ENTRY()
            e.read(br)

            self.m_infos[i].header = h

            for j in range(h.unknown_struct_count):

                s = DPL.UNKNOWN_STRUCT()
                s.read(br)

            self.m_infos[i].offset  = e.offset
            self.m_infos[i].size = e.size
            self.m_infos[i].unpacked_size = h.size + 48 if self.m_archieved else e.size
            self.m_infos[i].key = e.key

    def unpack_buf(self, buf_from, packed_size, unpacked_size, key, archieved, idx):
        data = decrypt(bytearray(buf_from), packed_size, key)
        if (archieved):
            try :
                data = zlib.decompress(data, wbits=-15, bufsize=unpacked_size)
            except :
                print(idx)
        else:
            pass

        return data

    class BLOCK_HEADER():

        def __init__(self) -> None:
            self.sign = 0
            self.type = 0
            self.idx = 0
            self.unknown = 0
            self.unpacked_size = 0
            self.packed_size = 0

        def read(self, br):
            self.sign = br.readUByte()
            self.type = br.readUByte()
            self.idx = br.readUShort()
            self.unknown = br.readUInt()
            self.unpacked_size = br.readUInt()
            self.packed_size = br.readUInt()

    def read_file_data(self, br, idx):

        buf_out = bytearray()
        
        e = self.m_infos[idx]

        # Write FHM header
        buf_out += struct.pack("{0}s".format(4), e.header.sign.encode('utf-8'))
        buf_out += struct.pack(">I", e.header.byte_order_20101010)
        buf_out += struct.pack(">I", e.header.timestamp)
        buf_out += struct.pack(">I", e.header.unknown_struct_count)
        buf_out += struct.pack(">I", e.header.unknown)
        buf_out += struct.pack(">I", e.header.size)
        buf_out += struct.pack(">I", e.header.unknown3)
        buf_out += struct.pack(">I", e.header.unknown4)
        buf_out += struct.pack(">I", e.header.unknown5)
        buf_out += struct.pack(">I", e.header.unknown_16)
        buf_out += struct.pack(">I", e.header.unknown_pot)
        buf_out += struct.pack(">I", e.header.unknown_pot2)

        br.seek(e.offset, 0)

        position = br.tell()
        curr_index = 0

        while (br.tell() < e.size + position):
            
            header = DPL.BLOCK_HEADER()
            header.read(br)
            archieved = header.type == 1

            buf_from = br.readBytes(header.packed_size)
            data = self.unpack_buf(buf_from, header.packed_size, header.unpacked_size, e.key, archieved, idx)
            buf_out += data

        return buf_out




