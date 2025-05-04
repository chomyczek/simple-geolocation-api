class Response:
    """
    An object used to return information by an application in a uniform format.
    """

    message: str = None
    result: object = None

    def serialize(self):
        return {
            'message': self.message,
            'result': {key: value for key, value in self.result.__dict__.items() if
                       not key.startswith('_') and not callable(key)},
        }
