import pytest
import operator as op
from typing import Callable, Any
from fynctionista.trees.linked_list import EmptyLinkedList, NonEmptyLinkedList


class TestLinkedList:
    requires = pytest.mark.requires.with_args

    @pytest.fixture
    def generate_minmax_numeric(self, generate_val) -> Callable[[type, int, int], int]:
        yield lambda tt, mn, mx: max(min(generate_val(tt), mx), mn)

    @pytest.fixture
    def generate_list(self, generate_val) -> Callable[..., tuple[NonEmptyLinkedList, list[Any]]]:
        """
        Returns a function which creates
        a NonEmptyList with generated data and returns
        a tuple with the linked list & a list of the data
        """
        def _generator(size: int, *allowed_types: type) -> NonEmptyLinkedList:
            xs = EmptyLinkedList()
            data = []
            for _ in range(size):
                value = generate_val(*allowed_types)
                xs = xs.add(value)
                data.insert(0, value)
            return xs, data
        yield _generator

    @requires(EmptyLinkedList.add)
    def test_single_addition_returns_non_empty_instance(self, generate_val):
        # given an empty list
        xs = EmptyLinkedList()
        # when
        ys = xs.add(generate_val())
        # then
        assert isinstance(xs, EmptyLinkedList)
        assert isinstance(ys, NonEmptyLinkedList)

    @requires(
        EmptyLinkedList.add,
        NonEmptyLinkedList.add,
        NonEmptyLinkedList.tail,
        EmptyLinkedList.__repr__,
        NonEmptyLinkedList.__repr__
    )
    def test_multiple_additions_return_multiple_instances(self, generate_val):
        # given an empty list
        xs = EmptyLinkedList()
        # when add data
        ys = xs.add(generate_val())
        zs = ys.add(generate_val())
        # then
        assert ys is not zs
        assert ys.tail() is zs
        assert zs.tail() is xs

    @requires(EmptyLinkedList.is_empty)
    def test_empty_is_empty(self):
        # given an empty list
        xs = EmptyLinkedList()
        # then
        assert xs.is_empty() is True

    @requires(EmptyLinkedList.add, NonEmptyLinkedList.is_empty)
    def test_nonempty_is_not_empty(self, generate_list):
        # given a nonempty list
        xs, _ = generate_list(1)
        # then
        assert xs.is_empty() is False

    @requires(EmptyLinkedList.__len__)
    def test_empty_length(self):
        # given an empty list
        xs = EmptyLinkedList()
        # then
        assert len(xs) == 0

    @requires(EmptyLinkedList.add, NonEmptyLinkedList.add, NonEmptyLinkedList.__len__)
    @pytest.mark.parametrize("entries", range(1, 10, 4))
    def test_nonempty_length(self, generate_list, entries):
        # given a nonempty list
        xs, _ = generate_list(entries, int)
        # then
        assert len(xs) == entries

    @requires(EmptyLinkedList.head)
    def test_empty_head_raises_error(self):
        # given an empty list
        xs = EmptyLinkedList()
        # then
        with pytest.raises(IndexError):
            xs.head()

    @requires(EmptyLinkedList.add, NonEmptyLinkedList.head)
    @pytest.mark.parametrize("ttype", (float, str, bytes))
    def test_nonempty_single_head(self, generate_list, ttype):
        # given
        xs, data = generate_list(1, ttype)
        # then
        assert xs.head() == data[0]

    @requires(
        EmptyLinkedList.add,
        NonEmptyLinkedList.add,
        NonEmptyLinkedList.head,
        NonEmptyLinkedList.tail
    )
    @pytest.mark.parametrize("entries", range(1, 10, 4))
    def test_nonempty_multiple_heads(self, generate_list, entries):
        # given a nonempty list
        xs, data = generate_list(entries)
        # then
        for expected_head in data:
            assert xs.head() == expected_head
            xs = xs.tail()
        assert isinstance(xs, EmptyLinkedList)

    @requires(EmptyLinkedList.tail)
    def test_empty_tail_raises_error(self):
        # given an empty list
        xs = EmptyLinkedList()
        # then
        with pytest.raises(Exception):
            xs.tail()

    @requires(EmptyLinkedList.add, NonEmptyLinkedList.tail)
    def test_nonempty_tail(self, generate_val):
        # given a nonempty list
        xs = EmptyLinkedList()
        # when
        ys = xs.add(generate_val())
        zs = xs.add(generate_val())
        # then
        assert ys.tail() is xs
        assert zs.tail() is xs
        assert ys is not zs

    @requires(EmptyLinkedList.pop)
    @pytest.mark.parametrize("idx", ({"idx": 0}, {}))
    def test_empty_head_raises_error(self, idx):
        # given an empty list
        xs = EmptyLinkedList()
        # then
        assert xs.pop.__defaults__ is not None
        with pytest.raises(IndexError):
            xs.pop(**idx)

    @requires(EmptyLinkedList.add, NonEmptyLinkedList.pop)
    @pytest.mark.parametrize("idx", ({"idx": 0}, {}))
    def test_nonempty_single_pop_returns_head(self, idx, generate_list):
        # given nonempty list
        xs, data = generate_list(1)
        # when
        item, ys = xs.pop(**idx)
        # then
        assert item == data[0]
        assert isinstance(ys, EmptyLinkedList)

    @requires(EmptyLinkedList.add, NonEmptyLinkedList.add, NonEmptyLinkedList.pop)
    @pytest.mark.parametrize("entries,idx", ([3, 4], [3, -5]))
    def test_pop_out_of_bounds_raises_error(self, generate_list, entries, idx):
        # given nonempty list
        xs, data = generate_list(entries)
        # then
        with pytest.raises(IndexError):
            xs.pop(idx)

    @requires(EmptyLinkedList.add, NonEmptyLinkedList.add, NonEmptyLinkedList.pop)
    @pytest.mark.parametrize("entries", (7, 32, 64))
    def test_nonempty_multiple_pops(self, generate_list, generate_minmax_numeric, entries):
        # given nonempty list
        total_entries = 64
        xs_0, data = generate_list(total_entries)
        # and generated in bound ints
        idx_1, idx_2, idx_3 = (
            generate_minmax_numeric(int, -entries, entries) for _ in range(3)
        )
        # when
        item_1, xs_1 = xs_0.pop(idx_1)
        item_2, xs_2 = xs_1.pop(idx_2)
        item_3, xs_3 = xs_2.pop(idx_3)
        # then
        assert len(xs_1) == total_entries - 1
        assert len(xs_2) == total_entries - 2
        assert len(xs_3) == total_entries - 3
        assert item_1 == data.pop(idx_1)
        assert item_2 == data.pop(idx_2)
        assert item_3 == data.pop(idx_3)

    @requires(EmptyLinkedList.map)
    @pytest.mark.parametrize(
        "mapper", (lambda x: x, lambda _: 1, lambda _: 1 / 0)
    )
    def test_empty_list_maps_itself(self, mapper):
        # given an empty list
        xs = EmptyLinkedList()
        # when
        ys = xs.map(mapper)
        # then
        assert xs is ys

    @requires(
        EmptyLinkedList.add,
        NonEmptyLinkedList.add,
        NonEmptyLinkedList.head,
        NonEmptyLinkedList.tail,
        NonEmptyLinkedList.map,
    )
    @pytest.mark.parametrize("entries", (1, 3, 5))
    def test_nonempty_map_returns_different_instances(self, generate_list, entries):
        # given a nonempty list
        xs, data = generate_list(entries)
        # when
        ys = xs.map(lambda _: _)
        # then
        for _ in range(entries):
            assert xs is not ys
            assert xs.head() == ys.head()
            xs, ys = xs.tail(), ys.tail()
        assert isinstance(xs, EmptyLinkedList)
        assert isinstance(ys, EmptyLinkedList)

    @requires(EmptyLinkedList.add, NonEmptyLinkedList.add, NonEmptyLinkedList.map)
    @pytest.mark.parametrize("entries", (1, 3, 5))
    @pytest.mark.parametrize(
        "mapper", (lambda _: 1, lambda x: x * 2, lambda x: 1 / x if x % 2 else None)
    )
    def test_nonempty_maps_all_entries(self, generate_list, entries, mapper):
        # given a nonempty list
        xs, data = generate_list(entries, int, float)
        # and apply mapper on raw data
        mapped_data = list(map(mapper, data))
        # when
        ys = xs.map(mapper)
        # then
        for i in range(entries):
            assert xs.head() == data[i]
            assert ys.head() == mapped_data[i]
            xs, ys = xs.tail(), ys.tail()
        assert isinstance(xs, EmptyLinkedList)
        assert isinstance(ys, EmptyLinkedList)

    @requires(EmptyLinkedList.add, NonEmptyLinkedList.add, NonEmptyLinkedList.map)
    def test_nonempty_list_raises_mappers_error(self, generate_list):
        # given a nonempty list
        xs = EmptyLinkedList().add(1).add(0).add(1)
        # then
        with pytest.raises(ZeroDivisionError):
            xs.map(lambda x: 1 / x)

    @requires(EmptyLinkedList.filter)
    @pytest.mark.parametrize(
        "filterer", (lambda _: 1, lambda _: 0, lambda _: 1 / 0)
    )
    def test_empty_list_filters_itself(self, filterer):
        # given an empty list
        xs = EmptyLinkedList()
        # when
        ys = xs.filter(filterer)
        # then
        assert xs is ys

    @requires(EmptyLinkedList.add, NonEmptyLinkedList.add, NonEmptyLinkedList.filter)
    @pytest.mark.parametrize("entries", (1, 3, 5))
    @pytest.mark.parametrize("constant", (0, 1, True, False, "", "A", None))
    def test_nonempty_filter_consts_return_same_or_empty(self, generate_list, entries, constant):
        # given a nonempty list
        xs, data = generate_list(entries)
        # when
        ys = xs.filter(lambda _: constant)
        # then
        assert xs is not ys
        if not constant:
            isinstance(ys, EmptyLinkedList)
        else:
            isinstance(ys, NonEmptyLinkedList)
            for i in range(entries):
                assert xs.head() == ys.head()
                xs, ys = xs.tail(), ys.tail()
            assert isinstance(xs, EmptyLinkedList)
            assert isinstance(ys, EmptyLinkedList)

    @requires(EmptyLinkedList.add, NonEmptyLinkedList.add, NonEmptyLinkedList.filter)
    @pytest.mark.parametrize("entries", (1, 3, 5))
    def test_nonempty_filter_has_no_effect_on_data(self, generate_list, entries):
        # given a nonempty list
        xs, data = generate_list(entries, bytes, int, float, str)
        # when
        ys = xs.filter(lambda x: x * 2)
        # then
        assert xs is not ys
        for i in range(entries):
            assert xs.head() == ys.head()
            xs, ys = xs.tail(), ys.tail()
        assert isinstance(xs, EmptyLinkedList)
        assert isinstance(ys, EmptyLinkedList)

    @requires(EmptyLinkedList.add, NonEmptyLinkedList.add, NonEmptyLinkedList.filter)
    def test_nonempty_filter_raises_mappers_error(self, generate_list):
        # given a nonempty list
        xs = EmptyLinkedList().add(1).add(0).add(1)
        # then
        with pytest.raises(ZeroDivisionError):
            xs.filter(lambda x: 1 / x)

    @requires(EmptyLinkedList.reduce)
    @pytest.mark.parametrize(
        "reducer", (lambda x, y: 1, lambda _: 0, lambda x, y: 1 / 0)
    )
    def test_empty_list_reduce_raises_error(self, reducer):
        # given an empty list
        xs = EmptyLinkedList()
        # then
        with pytest.raises(TypeError):
            xs.reduce(reducer)

    @requires(EmptyLinkedList.add, NonEmptyLinkedList.add, NonEmptyLinkedList.reduce)
    @pytest.mark.parametrize("entries", (1, 3, 5))
    def test_nonempty_reduces_top_down(self, generate_list, entries):
        # given a list of strings
        xs, data = generate_list(entries, str)
        expected_result = "".join(data)
        # when
        result = xs.reduce(op.iadd)
        # then
        assert result == expected_result
