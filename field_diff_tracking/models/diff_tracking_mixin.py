from odoo import models, api
import difflib
from html import escape

class DiffTrackingMixin(models.AbstractModel):
    _name = 'diff.tracking.mixin'
    _description = 'Diff Tracking Mixin'

    @api.model
    def _get_diff_tracked_fields(self):
        return [
            name for name, field in self._fields.items()
            if getattr(field, 'track_diff', False)
        ]

    def write(self, vals):
        diff_tracked_fields = self._get_diff_tracked_fields()
        tracked_vals = {f: v for f, v in vals.items() if f in diff_tracked_fields}
        
        # Store old values before write
        old_values = {f: getattr(self, f) for f in tracked_vals}
        
        result = super(DiffTrackingMixin, self).write(vals)
        
        for record in self:
            for field, new_value in tracked_vals.items():
                old_value = old_values[field]
                if old_value != new_value:
                    diff = difflib.ndiff(
                        (old_value or '').splitlines(keepends=True),
                        (new_value or '').splitlines(keepends=True)
                    )
                    html_diff = record._format_diff_as_html(diff)
                    record.message_post(body=html_diff, body_is_html=True, subject=f"{field.replace('_', ' ').title()} Updated")
        
        return result

    def _format_diff_as_html(self, diff):
        html = ['<pre style="white-space: pre-wrap; word-wrap: break-word; font-family: monospace;">']
        for line in diff:
            if line.startswith('+'):
                html.append(f'<span style="background-color: #e6ffe6;">{escape(line)}</span>')
            elif line.startswith('-'):
                html.append(f'<span style="background-color: #ffe6e6;">{escape(line)}</span>')
            elif line.startswith('?'):
                html.append(f'<span style="color: #808080;">{escape(line)}</span>')
        html.append('</pre>')
        return ''.join(html)