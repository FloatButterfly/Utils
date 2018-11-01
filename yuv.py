import numpy as np


def yuv_import(filename, width, height, numfrm=None, startfrm=0):
    # Compute the size of the frames
    luma_size = height * width
    chroma_size = luma_size // 4
    frame_size = luma_size + 2 * chroma_size

    # Open the file, skip the frames and load the data into numpy array
    f = open(filename, "rb")
    f.seek(frame_size * startfrm, 0)
    data = np.fromfile(f, dtype=np.uint8)
    f.close()

    # Compute the number of the frames if necessary
    if numfrm is None:
        assert len(data) % frame_size == 0, "The number of the frames is not an integer."
        numfrm = len(data) // frame_size

    # Define the YUV buffer
    Y = np.zeros([numfrm, height, width], dtype=np.uint8)
    U = np.zeros([numfrm, height // 2, width // 2], dtype=np.uint8)
    V = np.zeros([numfrm, height // 2, width // 2], dtype=np.uint8)

    # Load each frame
    i_data = 0
    for i_frame in range(numfrm):
        Y[i_frame, :, :] = data[i_data:i_data + luma_size].reshape(height, width)
        i_data += luma_size
        # data2[i_data:i_data + chroma_size] = 0
        U[i_frame, :, :] = data[i_data:i_data + chroma_size].reshape(height // 2, width // 2)
        i_data += chroma_size
        V[i_frame, :, :] = data[i_data:i_data + chroma_size].reshape(height // 2, width // 2)
        i_data += chroma_size

    return Y, U, V


def yuv_import_2(filename, width, height, numfrm, startfrm=0):
    # Open the file
    f = open(filename, "rb")

    # Skip some frames
    luma_size = height * width
    chroma_size = luma_size // 4
    frame_size = luma_size * 3 // 2
    f.seek(frame_size * startfrm, 0)

    # Define the YUV buffer
    Y = np.zeros([numfrm, height, width], dtype=np.uint8)
    U = np.zeros([numfrm, height // 2, width // 2], dtype=np.uint8)
    V = np.zeros([numfrm, height // 2, width // 2], dtype=np.uint8)

    # Loop over the frames
    for i in range(numfrm):
        # Read the Y component
        Y[i, :, :] = np.fromfile(f, dtype=np.uint8, count=luma_size).reshape([height, width])
        # Read the U component
        U[i, :, :] = np.fromfile(f, dtype=np.uint8, count=chroma_size).reshape([height // 2, width // 2])
        # Read the V component
        V[i, :, :] = np.fromfile(f, dtype=np.uint8, count=chroma_size).reshape([height // 2, width // 2])

    # Close the file
    f.close()

    return Y, U, V


def yuv_import_3(filename, width, height, bitdepth, numfrm, startfrm=0):
    # Open the file
    f = open(filename, "rb")

    # Skip some frames
    if bitdepth == 8:
        dtype = np.uint8
        bits = 1
    elif bitdepth == 10:
        dtype = np.uint16
        bit = 2
    else:
        raise Exception()

    n_luma = height * width
    n_chroma = (height // 2) * (width // 2)
    f.seek((n_luma + 2 * n_chroma) * startfrm * bit, 0)

    # Define the YUV buffer
    Y = np.zeros([numfrm, height, width], dtype=dtype)
    U = np.zeros([numfrm, height // 2, width // 2], dtype=dtype)
    V = np.zeros([numfrm, height // 2, width // 2], dtype=dtype)

    # Loop over the frames
    for i in range(numfrm):
        # Read the Y component
        Y[i, :, :] = np.fromfile(f, dtype=dtype, count=n_luma).reshape([height, width])
        # Read the U component
        U[i, :, :] = np.fromfile(f, dtype=dtype, count=n_chroma).reshape([height // 2, width // 2])
        # Read the V component
        V[i, :, :] = np.fromfile(f, dtype=dtype, count=n_chroma).reshape([height // 2, width // 2])

    # Close the file
    f.close()

    return Y, U, V


# 保留Y, U,V填0
def yuv_import4(filename, width, height, numfrm=None, startfrm=0):
    # Compute the size of the frames
    luma_size = height * width
    chroma_size = luma_size // 4
    frame_size = luma_size + 2 * chroma_size

    # Open the file, skip the frames and load the data into numpy array
    f = open(filename, "rb")
    f.seek(frame_size * startfrm, 0)
    data = np.fromfile(f, dtype=np.uint8)
    f.close()

    # Compute the number of the frames if necessary
    if numfrm is None:
        assert len(data) % frame_size == 0, "The number of the frames is not an integer."
        numfrm = len(data) // frame_size

    # Define the YUV buffer
    Y = np.zeros([numfrm, height, width], dtype=np.uint8)
    U = np.zeros([numfrm, height // 2, width // 2], dtype=np.uint8)
    V = np.zeros([numfrm, height // 2, width // 2], dtype=np.uint8)

    # Load each frame
    i_data = 0
    for i_frame in range(numfrm):
        Y[i_frame, :, :] = data[i_data:i_data + luma_size].reshape(height, width)
        i_data += luma_size
        # U[i_frame, :, :] = data[i_data:i_data + chroma_size].reshape(height // 2, width // 2)
        # i_data += chroma_size
        # V[i_frame, :, :] = data[i_data:i_data + chroma_size].reshape(height // 2, width // 2)
        # i_data += chroma_size

    return Y, U, V


def yuv_export(filename, Y, U, V, skip=1):
    yfrm = Y.shape[0]
    ufrm = U.shape[0]
    vfrm = V.shape[0]

    if yfrm == ufrm == vfrm:
        numfrm = yfrm
    else:
        raise Exception("The length of the frames does not match.")

    with open(filename, "wb") as f:
        for i in range(numfrm):
            if i % skip == 0:
                Y[i, :, :].tofile(f)
                U[i, :, :].tofile(f)
                V[i, :, :].tofile(f)


def yuv_export_2(filename, Y, U, V):
    yfrm = Y.shape[0]
    ufrm = U.shape[0]
    vfrm = V.shape[0]

    if yfrm == ufrm == vfrm:
        numfrm = yfrm
    else:
        raise Exception("The length of the frames does not match.")

    with open(filename, "wb") as f:
        for i in range(numfrm):
            Y[i, :, :].tofile(f)
            # U[i, :, :].tofile(f)
            # V[i, :, :].tofile(f)


if __name__ == '__main__':
    in_name = "out_edges.yuv"
    out = 'out_edges_yuv400.yuv'
    Y, U, V = yuv_import4(filename, 256, 256)
    yuv_export(filename=filename, Y=Y, U=U, V=V)
