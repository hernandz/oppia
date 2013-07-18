from oppia.apps.widget import models


class MultipleChoiceInput(models.BaseWidget):
    """Definition of a widget.

    Do NOT make any changes to this widget definition while the Oppia app is
    running, otherwise things will break.

    This class represents a widget, whose id is the name of the class. It is
    auto-discovered from apps/widget/models.py when the default widgets are
    refreshed.
    """

    # The human-readable name of the widget.
    name = 'Multiple choice input'

    # The category the widget falls under in the widget repository.
    category = 'Basic Input'

    # A description of the widget.
    description = 'A multiple-choice input widget.'

    # Customization parameters and their descriptions, types and default
    # values.
    params = [{
        'name': 'choices',
        'description': 'The options that the reader can select from.',
        'obj_type': 'List',
        'values': [
            ['Default choice']
        ]
    }]

    # Actions that the reader can perform on this widget which trigger a
    # feedback interaction, and the associated classifiers. Interactive widgets
    # must have at least one of these.
    handlers = [{
        'name': 'submit', 'classifier': 'MultipleChoiceClassifier'
    }]