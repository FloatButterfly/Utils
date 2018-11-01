import os


def main():
    for i in range(0, 200):
        for j in range(10, 110, 10):
            in_name = 'input_%03d_ground truth.bmp_%d' % (i, j)
            out_name = 'input_%03d_ground truth.j2k_%d' % (i, j)
            command = r'E:\pku\openjpeg-v2.3.0-windows-x64\bin\opj_compress.exe' + ' ' + '-i' + ' ' + in_name + ' ' + '-o' + ' ' \
                      + out_name + ' ' + '-r' + ' ' + str(j)
            print (command)


if __name__ == '__main__':
    main()
