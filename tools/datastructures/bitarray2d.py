from BitArray2D import BitArray2D, godel


def rotate(array: BitArray2D) -> BitArray2D:
    out = BitArray2D(columns=array.columns, rows=array.rows)
    for row in range(array.rows):
        for col in range(array.columns):
            out[col, row] = array[godel(row, col)]
    return out


def flip(array: BitArray2D) -> BitArray2D:
    out = BitArray2D(rows=array.rows, columns=array.columns)
    for row in range(array.rows):
        for col in range(array.columns):
            out[row, col] = array[godel(row, array.columns - col - 1)]
    return out
