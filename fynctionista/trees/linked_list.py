from fynctionista.trees.protos import LinkedList, T, U, Callable, Any


class EmptyLinkedList(LinkedList[T]):
    """
    When you're not sure how a method should
    behave, you can follow the implementation
    of the builtin equivalents
    """
    def head(self) -> T:
        """
        Returns the element inserted last
        """
        ...

    def tail(self) -> 'LinkedList':
        """
        Returns the tail of the list (i.e. w/o the head)
        """
        ...

    def add(self, item: T) -> 'LinkedList':
        """
        Inserts value in the beginning of the list
        """
        ...

    def pop(self, idx: int = -1) -> tuple[T, 'LinkedList']:
        """
        removes element @ given index and returns it along with the new list
        """
        ...

    def map(self, mapper: Callable[[T], Any]) -> 'LinkedList':
        ...

    def filter(self, filterer: Callable[[T], bool]) -> 'LinkedList':
        ...

    def reduce(self, reducer: Callable[[U, T], U]) -> U:
        """
        You can check the behaviour of functools.reduce
        """
        ...

    def is_empty(self) -> bool:
        ...

    def __getitem__(self, index: int) -> T:
        """
        i.e xs[idx]
        """
        ...

    def __len__(self) -> int:
        ...

    def __contains__(self, item: T) -> bool:
        """
        i.e 1 in xs
        """
        ...

    def __repr__(self) -> str:
        """
        Represents the class in console.
        When we print our list, we want to make our elements visible e.g.
        >> print(mylist)
        <10, 20, 30>
        """
        ...


class NonEmptyLinkedList(LinkedList[T]):
    def __init__(self, head: T, tail: 'LinkedList'):
        ...

    def head(self) -> T:
        ...

    def tail(self) -> 'LinkedList':
        ...

    def add(self, item: T) -> 'LinkedList':
        ...

    def pop(self, idx: int = -1) -> tuple[T, 'LinkedList']:
        ...

    def map(self, mapper: Callable[[T], Any]) -> 'LinkedList':
        ...

    def filter(self, filterer: Callable[[T], bool]) -> 'LinkedList':
        ...

    def reduce(self, reducer: Callable[[U, T], U]) -> U:
        ...

    def is_empty(self) -> bool:
        ...

    def __getitem__(self, index: int) -> T:
        ...

    def __len__(self) -> int:
        ...

    def __contains__(self, item: T) -> bool:
        ...

    def __repr__(self) -> str:
        ...
