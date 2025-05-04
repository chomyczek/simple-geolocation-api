class Response:
    """
    An object used to return information by an application in a uniform format.
    """

    message: str = None
    result: object = None

    def serialize(self):
        return {
            'message': self.message,
            'result': self.result,
        }