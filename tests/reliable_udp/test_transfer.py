import threading
import time

from tools.reliable_udp.client import ReliableUDPClient
from tools.reliable_udp.server import ReliableUDPServer


def test_file_transfer_e2e(tmp_path) -> None:
    src = tmp_path / "src.bin"
    payload = (b"0123456789abcdef" * 4096) + b"END"
    src.write_bytes(payload)

    out_dir = tmp_path / "out"
    server = ReliableUDPServer("127.0.0.1", 9299, str(out_dir), drop_rate=0.0)

    result = {}

    def run_server() -> None:
        result["path"] = server.receive_one_file()

    t = threading.Thread(target=run_server, daemon=True)
    t.start()
    time.sleep(0.1)

    client = ReliableUDPClient("127.0.0.1", 9299, drop_rate=0.0, chunk_size=1200, timeout_s=0.1)
    try:
        client.send_file(str(src))
    finally:
        client.close()

    t.join(timeout=10)
    server.close()

    assert "path" in result
    assert result["path"].read_bytes() == payload
