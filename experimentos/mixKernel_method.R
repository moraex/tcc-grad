library(farff)
library(digest)
library(PCAmixdata)
library(mixKernel)
library(tidyverse)
library(reticulate)
library(BiocManager)
library(mixOmics)
library(phyloseq)
library(rscipy)
# use the package
install.packages("BiocManager")
BiocManager::install("zlibbioc")
BiocManager::install("mixOmics")
BiocManager::install("phyloseq")
install.packages("mixKernel")
install.packages("tidyverse")
install.packages("rscipy")

# reticulate::py_config()
# repl_python()
reticulate::use_python("C:/Users/ARQ/AppData/Local/Programs/Python/Python39", required = TRUE)

getwd()
setwd("C:/Users/ARQ/Desktop/GRADUACAO/12_SEMESTRE/TCC/esperimentos")


base.location <- "./raw_datasets/"
trainset.name <- "cellcycle_FUN"
path.trainset.name <- paste(base.location,trainset.name,'/',trainset.name,'.trainvalid.temp.arff', sep= "")

trainset <- farff::readARFF(path.trainset.name)

# removendo coluna de classificacao = unsupervisionado
D <- trainset[,-ncol(trainset)]


D.numerical <- splitmix(D)$X.quanti
D.categorical <- splitmix(D)$X.quali
# 

encode_ordinal <- function(x, order = unique(x)) {
  x <- as.numeric(factor(x, levels = order, exclude = NULL))
  x
}

for(e in names(D.categorical)){
  D.categorical[[e]] <- encode_ordinal(D.categorical[[e]])
}

# DS <- cbind(D.numerical, D.categorical)
DS <- D.numerical
# Substituir os valores faltantes pela média do attr
for(i in 1:ncol(DS)){
  DS[is.na(DS[,i]), i] <- mean(DS[,i], na.rm=T)
}

# center scale para padronizacao dos dados
DS <- scale(DS, center = T, scale = T)
new.ds <- center.scale(DS)

# Adaptação para obter o numero de componentes que correspondem
# a 95% da variacao
pca <- PCAmix(X.quanti = DS, rename.level = T, ndim = ncol(DS), graph = F)

npcs <- 1
while(pca$eig[npcs, 3] <= 95 && npcs <= nrow(DS)){
  npcs <- npcs + 1
}


feats <- select.features(DS,
                         kx.func="bray",
                         method="kernel",
                         lambda = 1,
                         keepX=40,
                         nsteps=5,
                         max_iter = 10)

feats2 <- select.features(center.scale(DS),
                         kx.func="bray",
                         method="kpca",
                         n_components=57,
                         lambda = 1,
                         keepX=40,
                         nsteps=5,
                         max_iter = 8)
colnames(DS)[feats]

#########

ds.kernel <- compute.kernel(DS,
                            kernel.func = "linear")
kernel.pca.res <- kernel.pca(ds.kernel, ncomp = 57)
dunno <- kernel.pca.permute(kernel.pca.res, phychem = colnames(DS))

plotVar.kernel.pca(kernel.pca.res, ndisplay = 15)

