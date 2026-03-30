from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


class CreatorOrModeratorMixin(UserPassesTestMixin):
    creator_field = 'creator'

    def test_func(self):
        obj = self.get_object()
        creator = getattr(obj,self.creator_field)
        return (
            self.request.user == creator or
            self.request.user.groups.filter(name="Moderators").exists()
        )

    def handle_no_permission(self):

        return redirect('no_permission')