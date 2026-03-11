from tools.reliable_udp.protocol import Segment


def test_segment_roundtrip() -> None:
    seg = Segment(type="DATA", seq=7, ack=3, payload=b"abc", filename="f.bin", total_size=10)
    restored = Segment.from_bytes(seg.to_bytes())
    assert restored.type == "DATA"
    assert restored.seq == 7
    assert restored.ack == 3
    assert restored.payload == b"abc"
    assert restored.filename == "f.bin"
    assert restored.total_size == 10
