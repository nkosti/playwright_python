import uuid


class Utilities:

    @staticmethod
    def get_random_text(text: str, length: int = 20) -> str:
        return text + str(uuid.uuid4().hex[:length])

    @staticmethod
    def get_test_number(request):
        return [
            marker.name for marker in request.node.own_markers if "TEST" in marker.name
        ][0]
