# Field Diff Tracking

## Overview

The Field Diff Tracking module provides a mixin for Odoo models to track and display differences in text, char, and HTML fields. This module enhances Odoo's native change tracking by providing a more detailed and visually appealing diff view in the chatter.

## Features

- Track changes in text, char, and HTML fields
- Display detailed diffs in the chatter
- Support for both code-style and text-style diff formatting
- Easy integration with existing Odoo models

## Installation

1. Add this module to your Odoo addons path.
2. Update your Odoo addons list.
3. Install the module through the Odoo Apps menu.

## Usage

To use the diff tracking functionality in your model:

1. Inherit from the `diff.tracking.mixin` model:

```python
from odoo import models, fields

class YourModel(models.Model):
    _name = 'your.model'
    _inherit = ['mail.thread', 'diff.tracking.mixin']

    your_field = fields.Text(track_diff='code')  # or 'text' for text-style diff
```

2. The `track_diff` parameter can be set to either `'code'` or `'text'` to specify the diff style.

3. Changes to the tracked fields will now show detailed diffs in the chatter.

## Configuration

No additional configuration is needed. Once installed and properly inherited, the module will automatically track and display diffs for the specified fields.

## Technical Details

- The module extends Odoo's native `Field` class to add the `track_diff` attribute.
- The `DiffTrackingMixin` handles the diff generation and posting to the chatter.
- Two diff styles are supported: 'code' for line-by-line comparison and 'text' for sentence-level comparison.

## Support

For questions or support, please create an issue in the repository.

## License

This module is licensed under the LGPL-3 License.