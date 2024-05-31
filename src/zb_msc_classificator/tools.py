from json import JSONEncoder, dump
from typing import Any, Iterator
from collections import defaultdict


class Serialize(JSONEncoder):
    def iterencode(self, o: Any, _one_shot: bool = ...) -> Iterator[str]:
        if isinstance(o, defaultdict):
            for k, v in o.items():
                if isinstance(v, defaultdict):
                    o[k] = {
                        label: count
                        for label, count in sorted(
                            v.items(),
                            key=lambda x: x[1],
                            reverse=True
                        )
                    }
        return super().iterencode(o, _one_shot)


class Toolbox:
    def nested_dict(
            self,
            layers: int,
            data_type: type
    ):
        """

        :param layers: nr of levels in nested dict
        :param data_type: default type of content if key doesnt exist
        :return: nested default dict of n levels
        """
        if layers == 1:
            return defaultdict(data_type)
        else:
            return defaultdict(lambda: self.nested_dict(layers - 1, data_type))

    @staticmethod
    def str_spaces_to_list(string: str, delimiter: str):
        return string.split(delimiter)
