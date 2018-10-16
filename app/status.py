class Status:
    def __init__(self, name, status, in_progress):
        self.name = name
        self.status = status
        self.in_progress = in_progress

    def __str__(self):
        return '%s: %s (%s)' % (self.name, self.status, 'in progress' if self.in_progress else 'finished')
