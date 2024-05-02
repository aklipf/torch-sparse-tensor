from typing import Iterable

from .base import BaseSparse
from .mapping import Mapping


class SparseIndexingMixin(BaseSparse):

    def __getitem__(self, indexing: Iterable[slice | None] | Mapping):
        if isinstance(indexing, Mapping):
            assert indexing.is_source(self)

            if self._values is None:
                values = None
            else:
                values = self._values[indexing.mapping]

            return self.__class__(
                indexing.target.indices, values=values, shape=indexing.target.shape
            )
        elif not isinstance(indexing, tuple):
            indexing = (indexing,)

        result = self.clone()
        for i, idx in enumerate(indexing):
            assert idx == slice(None) or idx is None

            if idx is None:
                result.unsqueeze_(i)

        return result
