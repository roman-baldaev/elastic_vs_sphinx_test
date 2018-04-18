from abc import abstractmethod, ABC


class Test(ABC):

    def __init__(self, object_test_name, *args):
        self.object_test_name = object_test_name
        self.pieces_with_different_size = args

    @abstractmethod
    def search_string(self, str):
        ...

    @property
    @abstractmethod
    def test_results(self):
        ...

    @property
    @abstractmethod
    def size_distribution(self):
        ...

    @abstractmethod
    def size_of_piece(self, piece):
        ...

    def sizes_of_all_pieces(self):
        sizes = {}

        for piece in self.pieces_with_different_size:
            sizes[piece] = self.size_of_piece(piece)


