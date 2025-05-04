from typing import Dict


class Response:
    """
    An object used to return information by an application in a uniform format.
    """

    message: str = None
    result: object = None

    def serialize(self) -> Dict:
        """
        Convert object to dictionary.
        :return: Converted object, ready for flask jsonify function.
        """
        return {
            "message": self.message,
            "result": (
                None
                if not self.result
                else {
                    key: value
                    for key, value in self.result.__dict__.items()
                    if not key.startswith("_") and not callable(key)
                }
            ),
        }
