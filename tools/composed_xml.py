"""Independent XML view for repository validation, never imported by Kotomi.

The runtime owns validation and persistence. This tiny read-only reference view
lets Data's standalone checks inspect Japanese and source values together.
"""
from copy import deepcopy
from pathlib import Path
import xml.etree.ElementTree as ET


def parse(path):
    path = Path(path)
    source = ET.parse(path).getroot()
    reference = source.get('shared_target')
    if not reference:
        return ET.ElementTree(source)
    target = ET.parse(path.parent / reference).getroot()

    def key(node):
        return node.tag, tuple((name, node.get(name)) for name in ('id', 'name', 'ref', 'schema') if name in node.attrib)

    def merge(target, source):
        result = deepcopy(target)
        result.attrib.update(source.attrib)
        if source.tag in {'words', 'contexts'}:
            result[:] = []
        for child in source:
            match = next((item for item in target if key(item) == key(child)), None)
            composed = merge(match, child) if match is not None else deepcopy(child)
            existing = next((item for item in result if key(item) == key(child)), None)
            if existing is None:
                result.append(composed)
            else:
                result[list(result).index(existing)] = composed
        return result
    return ET.ElementTree(merge(target, source))
