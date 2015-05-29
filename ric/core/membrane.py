from collective.contact.membrane.behaviors.personmembraneuser import PersonMembraneUserAdapter


class RICPersonMembraneUserAdapter(PersonMembraneUserAdapter):

    def getUserName(self):
        if self.context.userid:
            if isinstance(self.context.userid, unicode):
                # no need to use portal encoding for transitional encoding
                # from unicode to ascii. utf-8 should be fine.
                self.context.userid = self.context.userid.encode('utf-8')
            return self.context.userid
        else:
            # return nothing to not list user in plone
            return ''
            return super(RICPersonMembraneUserAdapter, self).getUserName()
