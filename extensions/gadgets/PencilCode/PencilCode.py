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
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__author__ = 'Sean Lip'


from extensions.gadgets import base


class PencilCode(base.BaseGadget):
    """Gadget for providing a Pencil Code editor."""

    short_description = 'Pencil Code'
    description = 'A Pencil Code editor.'
    height_px = 600
    width_px = 600
    panel = 'supplemental'
    _dependency_ids = ['pencilcode']

    _customization_arg_specs = [{
        'name': 'is_runnable',
        'description': 'Allow the learner to run the code?',
        'schema': {
            'type': 'bool',
        },
        'default_value': True
    }, {
        'name': 'is_editable',
        'description': 'Allow the learner to edit the code?',
        'schema': {
            'type': 'bool',
        },
        'default_value': True
    }, {
        'name': 'initial_code',
        'description': 'The initial code to show in the gadget',
        'schema': {
            'type': 'unicode',
            'ui_config': {
                'coding_mode': 'coffeescript',
            },
        },
        'default_value': '# Add the initial code snippet here.'
    }]
