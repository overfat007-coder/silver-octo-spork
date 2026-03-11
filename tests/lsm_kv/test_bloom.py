from tools.lsm_kv.bloom import BloomFilter


def test_bloom_membership() -> None:
    bf = BloomFilter.for_capacity(100)
    keys = [f"k{i}" for i in range(50)]
    for k in keys:
        bf.add(k)

    for k in keys:
        assert bf.might_contain(k)

    # not guaranteed false, but should be false for many non-members
    negatives = [f"x{i}" for i in range(50)]
    assert sum(1 for k in negatives if not bf.might_contain(k)) >= 20
