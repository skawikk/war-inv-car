#  mixin for change value of added_by field to current logged user
class GetInitialAuthorMixin:

    def get_initial(self):
        initial = super().get_initial()
        initial.copy()
        initial["added_by"] = self.request.user
        return initial