

import os

diretorios = os.listdir(".")

for diretorio in diretorios:
	if(os.path.isdir(diretorio)):
		valid = diretorio + ".valid.arff"
		train = diretorio + ".train.arff"

		trainvalid_dataset = []

		with open(f"{diretorio}/{diretorio}.train.arff", "r") as f:
			lines_train = f.readlines()

		for line in lines_train:
			trainvalid_dataset.append(line)

		with open(f"{diretorio}/{diretorio}.valid.arff", "r") as f:
			lines_valid = f.readlines()

		samples = False
		for line in lines_valid:
			if samples:
				trainvalid_dataset.append(line)
			if line.strip() == "@DATA":
				samples = True

		with open(f"{diretorio}/{diretorio}.trainvalid.arff", "w") as f:
			f.writelines(trainvalid_dataset)

		print(f"EXITO EM: {diretorio}.trainvalid.arff\n")