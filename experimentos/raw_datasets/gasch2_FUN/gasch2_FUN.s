[General]
% Compatibility = MLJ08

[Data]
File = raw_datasets/gasch2_FUN/gasch2_FUN.trainvalid.arff
TestSet = raw_datasets/gasch2_FUN/gasch2_FUN.test.arff

[Attributes]
ReduceMemoryNominalAttrs = no

[Hierarchical]
Type = Tree
WType = ExpAvgParentWeight
HSeparator = /
ClassificationThreshold = [0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,58,60,62,64,66,68,70,72,74,76,78,80,82,84,86,88,90,92,94,96,98,100]
% EvalClasses = raw_datasets/gasch2_FUN/evalclasses.txt

[Tree]
ConvertToRules = No
FTest = [0.05,0.125,0.125]

[Model]
MinimalWeight = 5.0

[kNN]
K = [1,5,10,15,20,25,30,35,40]
Distance = Euclidean
SearchMethod = BruteForce
DistanceWeighting = [Constant]
% AttributeWeighting = [list with the weights from feature ranking]
ChosenInstancesTest = [-1]

[Ensemble]
Iterations = [10]
FeatureRanking = [Genie3, Symbolic]
EnsembleMethod = RForest
SelectRandomSubspaces = SQRT
EnsembleBootstrapping = Yes
SymbolicWeight = Dynamic

[Relief]
Iterations = 1.0
Neighbours = [10, 15]

[SemiSupervised]
Iterations = 10
InternalFolds = 5
PossibleWeights = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]

[Output]
TrainErrors = No