from dpl import *
from pac6 import *

def main():

    #path_to_dpl_file = "E:\\MODDING\\Archive\\_Ace Combat\\Ace Combat Assault Horizon\\unpacked\\target\\DATA.PAC"
    #path_to_dpl_file = "E:\\MODDING\\Archive\\_Ace Combat\\Machstorm\\DATA00.PAC"
    path_to_dpl_file = "D:\\EMULATOR\\PS3\\rpcs3-v0.0.23-14031-28803700_win64\\dev_hdd0\\game\\NPUB31347\\USRDIR\\DATA90.PAC"
    
    file = open(path_to_dpl_file, 'rb')
    br = BinaryReader(file, ">")

    dpl = DPL()
    dpl.open(br)

    for i in range(len(dpl.m_infos)):

        data = dpl.read_file_data(br, i)

        f_out = open("f_out_" + str(i) + ".fhm", "wb")
        f_out.write(data)
        f_out.close()

    """
    path_to_pac6_file = "E:\\MODDING\\Archive\\_Ace Combat\\Ace Combat 6\\Xbox360\\DATA00.PAC"
    path_to_pac6_tbl = "E:\\MODDING\\Archive\\_Ace Combat\\Ace Combat 6\\Xbox360\\DATA.TBL"

    pac6_file = open(path_to_pac6_file, 'rb')
    pac6_file_br = BinaryReader(pac6_file, ">")
    
    pac6 = PAC6_FILE()
    pac6.open(pac6_file_br, path_to_pac6_tbl)

    data = pac6.read_file_data(pac6_file_br, 119)

    f_out = open("test", "wb")
    f_out.write(data)
    f_out.close()
    """

    print("test")


if __name__ == "__main__":
    main()