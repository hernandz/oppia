# coding: utf-8
#
# Copyright 2014 The Oppia Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, softwar
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Rules for CodeEvaluation objects."""

__author__ = 'Koji Ashida'

import re

from extensions.rules import base


def normalize_code(code_str):
    """Normalizes a code string. In particular:

    - Removes trailing whitespace.
    - Removes blank newlines.
    - Removes whitespace at the end of each line (but not at the beginning).
    """
    return '\n'.join(filter(
        None, [s.rstrip() for s in code_str.rstrip().split('\n')]))


class CodeEquals(base.CodeEvaluationRule):
    description = (
        'has code equal to {{x|UnicodeString}}')

    def _evaluate(self, subject):
        normalized_code = normalize_code(subject['code'])
        normalized_expected_code = normalize_code(self.x)
        return self._fuzzify_truth_value(
            normalized_code == normalized_expected_code)


class CodeContains(base.CodeEvaluationRule):
    description = (
        'has code that contains {{x|UnicodeString}}')

    def _evaluate(self, subject):
        normalized_code = normalize_code(subject['code'])
        normalized_snippet = normalize_code(self.x)
        return self._fuzzify_truth_value(
            normalized_code.find(normalized_snippet) != -1)


class CodeDoesNotContain(base.CodeEvaluationRule):
    description = (
        'has code that does not contain {{x|UnicodeString}}')

    def _evaluate(self, subject):
        normalized_code = ' '.join(subject['code'].split())
        normalized_snippet = ' '.join(self.x.split())
        return self._fuzzify_truth_value(
            normalized_code.find(normalized_snippet) == -1)


class OutputEquals(base.CodeEvaluationRule):
    description = (
        'has output equal to {{x|UnicodeString}}')

    def _evaluate(self, subject):
        normalized_output = ' '.join(subject['output'].split())
        normalized_expected_output = ' '.join(self.x.split())
        return self._fuzzify_truth_value(
            normalized_output == normalized_expected_output)


class OutputContains(base.CodeEvaluationRule):
    description = (
        'has output that contains {{x|UnicodeString}}')

    def _evaluate(self, subject):
        normalized_output = ' '.join(subject['output'].split())
        normalized_snippet = ' '.join(self.x.split())
        return self._fuzzify_truth_value(
            normalized_output.find(normalized_snippet) != -1)


class OutputDoesNotContain(base.CodeEvaluationRule):
    description = (
        'has output that does not contain {{x|UnicodeString}}')

    def _evaluate(self, subject):
        normalized_output = ' '.join(subject['output'].split())
        normalized_snippet = ' '.join(self.x.split())
        return self._fuzzify_truth_value(
            normalized_output.find(normalized_snippet) == -1)


class ResultsInError(base.CodeEvaluationRule):
    description = 'results in an error when run'

    def _evaluate(self, subject):
        return self._fuzzify_truth_value(bool(subject['error'].strip()))


class ErrorContains(base.CodeEvaluationRule):
    description = (
        'has error message that contains {{x|UnicodeString}}')

    def _evaluate(self, subject):
        normalized_error = ' '.join(subject['error'].split())
        normalized_snippet = ' '.join(self.x.split())
        return self._fuzzify_truth_value(
            normalized_error.find(normalized_snippet) != -1)


class FuzzyMatches(base.CodeEvaluationRule):
    description = 'is similar to {{training_data|ListOfCodeEvaluation}}'

    def _evaluate(self, subject):
        # TODO(bhenning): This is where a third party library could be used to
        # intelligently normalize and compare different submissions of code.
        # Also, this should return a value between 0 and 1 depending on how
        # closely it matches the training data, rather than doing a crisp
        # comparison on stripped code.

        # A very naive approach to 'normalizing' the code is to strip out all
        # comments and whitespace. This normalization currently assumes Python.
        def _normalize(python_code):
            # Remove comments.
            stripped = re.sub(r'#.*', '', python_code)
            # Remove whitespace (including newlines).
            return re.sub(r'\s+', '', stripped)

        code = _normalize(subject['code'])
        for possibility in self.training_data:
            if _normalize(possibility['code']) == code:
                return self._fuzzify_truth_value(True)
        return self._fuzzify_truth_value(False)
