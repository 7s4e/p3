# Third-party import
from blessed import Terminal


class ConsoleBase:
    def __init__(self):
        self._trm = Terminal()
