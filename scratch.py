import numpy as np
import pandas as pd 

def pretick(data):
    print('hi')
    print(data)
    # df = pd.DataFrame(data = data)



def main():

    data = b'Open,High,Low,Close,Volume\n11099.8,11205.2,11099.7,11205.1,76\n11423.6,11443.7,11388.2,11408.1,106\n11382.2,11392.1,11311.4,11321.5,46\n11421.3,11501.5,11396.1,11491.4,64\n11450.4,11455.4,11359.5,11374.6,65\n11363.8,11449.2,11303.1,11333.2,53\n11335.3,11370.4,11335.1,11360.1,22\n11233.6,11263.5,11183.1,11233.2,107\n11307.9,11328.0,11161.8,11161.8,65\n11120.8,11130.8,10999.8,10999.8,61\n11044.3,11104.4,11019.1,11069.1,75\n11015.9,11126.3,11005.7,11106.0,64\n11155.5,11180.6,11034.6,11039.6,59\n'
    data = data.decode('utf-8')

    data = data.split('\n')
    data_formatted = []
    data.pop()
    col_names = data.pop(0).split(',')
    for row in data:
        elems = row.split(',')
        elems_formatted = []
        for elem in elems:
            elems_formatted.append(float(elem))
        data_formatted.append(elems_formatted)
 
    data_formatted = np.array(data_formatted)
    # print(data_formatted)
    print(col_names)
    df = pd.DataFrame(data_formatted, columns = col_names)

    pretick(df)

if __name__ == "__main__":
    main()