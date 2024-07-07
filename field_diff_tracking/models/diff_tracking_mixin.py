from odoo import models, api
import difflib
from html import escape
import re

class DiffTrackingMixin(models.AbstractModel):
    _name = "diff.tracking.mixin"
    _description = "Diff Tracking Mixin"

    @api.model
    def _get_diff_tracked_fields(self):
        return [
            (name, field)
            for name, field in self._fields.items()
            if getattr(field, "track_diff", False)
        ]

    def write(self, vals):
        diff_tracked_fields = self._get_diff_tracked_fields()
        tracked_vals = {f: v for f, v in vals.items() if f in dict(diff_tracked_fields)}
        old_values = {f: getattr(self, f) for f in tracked_vals}
        result = super(DiffTrackingMixin, self).write(vals)
        for record in self:
            for field, new_value in tracked_vals.items():
                old_value = old_values[field]
                if old_value != new_value:
                    field_obj = dict(diff_tracked_fields)[field]
                    diff_style = getattr(field_obj, "track_diff", "code")
                    field_string = field_obj.string or field.replace("_", " ").title()
                    footer = f"<i class='text-muted'>({escape(field_string)})</i>"
                    html_diff = record._format_diff(old_value, new_value, diff_style)
                    full_html = f"{html_diff}{footer}"
                    record.message_post(
                        body=full_html,
                        body_is_html=True,
                        subject=f"{field_string} Updated",
                    )
        return result

    def _format_diff(self, old_value, new_value, diff_style):
        if diff_style == "code":
            old_lines = (old_value or "").splitlines(keepends=True)
            new_lines = (new_value or "").splitlines(keepends=True)
        elif diff_style == "text":
            old_lines = self._split_into_sentences(old_value or "")
            new_lines = self._split_into_sentences(new_value or "")
        else:
            return ""

        diff = list(difflib.ndiff(old_lines, new_lines))
        
        html = [
            '<div style="width: 100%; overflow-x: auto;">'
            '<pre style="white-space: pre; font-family: \'Courier New\', Courier, monospace; margin: 0;">'
        ]
        
        for line in diff:
            if line.startswith("+"):
                html.append(f'<span style="background-color: #e6ffe6;">{escape(line)}</span>')
            elif line.startswith("-"):
                html.append(f'<span style="background-color: #ffe6e6;">{escape(line)}</span>')
            elif line.startswith("?"):
                html.append(f'<span style="color: #808080;">{escape(line)}</span>')
        
        html.append("</pre></div>")
        return "".join(html)

    def _split_into_sentences(self, text):
        sentences = re.findall(r'[^.!?]+[.!?]*', text.strip())
        return [s.strip() + '\n' for s in sentences if s.strip()]