from odoo.fields import Field


def add_diff_tracking(field_class):
    field_class.track_diff = None
    original_init = field_class.__init__

    def new_init(self, *args, **kwargs):
        track_diff = kwargs.pop("track_diff", None)
        if isinstance(track_diff, bool):
            self.track_diff = "code" if track_diff else None
        else:
            self.track_diff = track_diff
        original_init(self, *args, **kwargs)

    field_class.__init__ = new_init
    return field_class


Field = add_diff_tracking(Field)
