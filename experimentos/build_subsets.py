import numpy as np
import math
import os
import sys
import utils


class ReliefRankFeatures:
    _features = []
    Q1 = 0
    Q2 = 0
    Q3 = 0

    def __init__(self, file):
        file = utils.ReadFile().read(file)
        sample = False
        for line in file:
            if sample:
                self._features.append(line.split("\t")[1])
            if line.count("-------------"):
                sample = True

        self.Q3 = math.ceil(0.25 * len(self._features))
        self.Q2 = math.ceil(0.5 * len(self._features))
        self.Q1 = math.ceil(0.75 * len(self._features))

    def top25(self):
        return self._features[:self.Q3]

    def top50(self):
        return self._features[:self.Q2]

    def top75(self):
        return self._features[:self.Q1]

    def audit(self):
        okay = True
        reason = []
        if (2*self.Q2 - len(self._features) > 1):
            okay = False
            reason.append('2xQ2 > len(features)')

        if ((self.Q1+self.Q3) - len(self._features) > 1):
            okay = False
            reason.append('Q1+Q3 > len(features)')

        if not okay:
            print(f'rasoes: {",".join(reason)}')
        else:
            print('APARENTEMENTE OKAY')


class BuildFeatureRankedSubset:
    ReliefFeatures = None
    source_trainvalid_sataset = None
    source_prefix = 'raw_datasets/'
    _target_prefix = None
    _OSPath = None
    dataset_name = None
    dataset_test = None

    def __init__(self, method, source_file, ranked_features_file):
        self._OSPath = utils.OSPath(source_file)
        self._target_prefix = method
        self.dataset_name = self._OSPath.file_name
        self.ReliefFeatures = ReliefRankFeatures(ranked_features_file)
        self.source_trainvalid_sataset = utils.ReadFile().read(
            f"{source_file}.trainvalid.arff")
        self.dataset_test = utils.ReadFile().read(f"{source_file}.test.arff")
        self.runFile()
        self.runTest()

    def keepIndexes(self, original_feature_space, keep_features):
        return [original_feature_space.index(att) for att in keep_features] + [-1]

    def runFile(self):
        for quartil in [['Q3', self.ReliefFeatures.top25()], ['Q2', self.ReliefFeatures.top50()], ['Q1', self.ReliefFeatures.top75()]]:

            subset = []
            curr_sample_idx = 0
            original_feature_space = []
            keep_features = []
            RELATION = False

            for line in self.source_trainvalid_sataset:
                curr_sample_idx += 1
                if (not RELATION) and line.count("@RELATION"):
                    subset.append(line)
                    subset.append("\n")
                    RELATION = True

                if line.count("@DATA"):
                    subset.append(line)
                    break

                if line.count("@ATTRIBUTE"):
                    original_feature_space.append(line.split(" ")[1])
                    if line.split(" ")[1] in quartil[1]:
                        keep_features.append(line.split(" ")[1])
                        subset.append(line)

                if line.count("@ATTRIBUTE class "):
                    subset.append(line)
                    subset.append("\n")

            keep_indexes = self.keepIndexes(
                original_feature_space, keep_features)

            for line in self.source_trainvalid_sataset[curr_sample_idx:]:
                new_line = np.array(line.split(","))
                subset.append(','.join(new_line[keep_indexes].tolist()))

            # we create target folders if not exists
            target_folder = f'{self._target_prefix}/{self.dataset_name}/{quartil[0]}/'
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)

            utils.WriteFile().write(
                f'{target_folder}{self.dataset_name}.trainvalid.arff', subset)

    def runTest(self):
        for quartil in [['Q3', self.ReliefFeatures.top25()], ['Q2', self.ReliefFeatures.top50()], ['Q1', self.ReliefFeatures.top75()]]:

            subset = []
            curr_sample_idx = 0
            original_feature_space = []
            keep_features = []
            RELATION = False

            for line in self.dataset_test:
                curr_sample_idx += 1
                if (not RELATION) and line.count("@RELATION"):
                    subset.append(line)
                    subset.append("\n")
                    RELATION = True

                if line.count("@DATA"):
                    subset.append(line)
                    break

                if line.count("@ATTRIBUTE"):
                    original_feature_space.append(line.split(" ")[1])
                    if line.split(" ")[1] in quartil[1]:
                        keep_features.append(line.split(" ")[1])
                        subset.append(line)

                if line.count("@ATTRIBUTE class "):
                    subset.append(line)
                    subset.append("\n")

            keep_indexes = self.keepIndexes(
                original_feature_space, keep_features)

            for line in self.dataset_test[curr_sample_idx:]:
                new_line = np.array(line.split(","))
                subset.append(','.join(new_line[keep_indexes].tolist()))

            target_folder = f'{self._target_prefix}/{self.dataset_name}/{quartil[0]}/'
            utils.WriteFile().write(
                f'{target_folder}{self.dataset_name}.test.arff', subset)


if __name__ == '__main__':
    method_map = {
        "relief": "output_relief_method",
        "genie3": "output_genie3_method",
        "symbolic": "output_symbolic_method",
    }
    method = method_map[sys.argv[1]]
    dataset = sys.argv[2]
    ranked_features_file = sys.argv[3]
    BuildFeatureRankedSubset(method, dataset, ranked_features_file)
