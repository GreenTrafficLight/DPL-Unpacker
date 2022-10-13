from Containers import *
from Utilities import *

import argparse, os

# All credits got to the open-horizon repository
# https://github.com/undefined-darkness/open-horizon

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--Input")
    parser.add_argument("-o", "--Output")

    args = parser.parse_args()

    if args.Input:

        file =  args.Input.split("\\")[-1]
        filename = os.path.splitext(file)[0]

        try:
            with open(args.Input, "rb") as f_in:
                br = BinaryReader(f_in, ">")

                dpl = DPL()
                dpl.open(br)

                for i in range(len(dpl.m_infos)):

                    print(str(i + 1) + " / " + str(len(dpl.m_infos)))

                    data = dpl.read_file_data(br, i)

                    if args.Output == None:
                        f_out = open(filename + "_" + str(i) + ".fhm", "wb")
                    else:
                        f_out = open(args.Output + "//" + filename + "_" + str(i) + ".fhm", "wb")
                    f_out.write(data)
                    f_out.close()
        except IOError:
            print('Error While Opening the file!')


if __name__ == "__main__":
    main()