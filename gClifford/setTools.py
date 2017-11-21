#!/usr/bin/env python
# -*- coding: utf-8 -*-

def merge_set_from_pairs(pairs):
    """Merge to a serious of set from a list of pairs
    e.g. [1,2] [2,3] [5,6] [9,8] [1,3]  -> [1,2,3] [5,6] [8,9]

    :pairs: a list of pairs, every pair has two value

    """
    setResult = []
    for p in pairs:
        assert len(p) == 2
        setExists = False
        for s in setResult:
            if p[0] in s or p[1] in s:
                s.add(p[0])
                s.add(p[1])
                setExists = True
                break
        if not setExists:
            setResult.append(set(p))
    return setResult
