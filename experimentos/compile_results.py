import os

diretorio = "raw_datasets/"
target = "pooled_ref_results.txt"

auprc_w = "(weighted)"
pooled = "Pooled AUPRC"
testing = "Testing error"
original = "Original:"


def writeValue(data):
    with open(target, 'a+') as f:
        f.write(data)


'''
for dataset in os.listdir(diretorio):
    for subset in os.listdir(f"{diretorio}{dataset}"):
        if os.path.isdir(f'{diretorio}{dataset}/{subset}'):
            _path = f'{diretorio}{dataset}/{subset}/{dataset}.out'
            with open(_path, 'r') as f:
                is_testing = False
                is_original = False
                for linha in f:
                    if is_testing and is_original:
                        if pooled in linha:
                            print(_path)
                            metric, raw_value = linha.split(":")
                            new_value = round(float(raw_value), 3)
                            new_line = f"{new_value}: ({float(raw_value)})\n"
                            writeValue(new_line)
                            break
                        # if pooled in linha:
                            # print(linha)
                    if testing in linha:
                        is_testing = True
                    if is_testing and original in linha:
                        is_original = True
'''
for dataset in os.listdir(diretorio):
    if os.path.isdir(f'{diretorio}{dataset}'):
        _path = f'{diretorio}{dataset}/{dataset}.out'
        with open(_path, 'r') as f:
            is_testing = False
            is_original = False
            for linha in f:
                if is_testing and is_original:
                    if pooled in linha:
                        print(_path)
                        metric, raw_value = linha.split(":")
                        new_value = round(float(raw_value), 3)
                        new_line = f"{new_value}: ({float(raw_value)})\n"
                        writeValue(new_line)
                        writeValue(new_line)
                        writeValue(new_line)
                        break
                    # if pooled in linha:
                        # print(linha)
                if testing in linha:
                    is_testing = True
                if is_testing and original in linha:
                    is_original = True
