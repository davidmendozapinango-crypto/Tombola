from pathlib import Path

from src.persistence.io_safety import (append_bytes, make_safe_writer,
                                       read_bytes)


def test_safe_writer_prevents_overwrite(tmp_path):
    writer = make_safe_writer(data_dir=str(tmp_path))
    append_bytes(writer, 'test.bin', b'first')
    append_bytes(writer, 'test.bin', b'second')
    content = read_bytes(writer, 'test.bin')
    assert content == b'firstsecond'

def test_safe_writer_creates_directory(tmp_path):
    data_dir = tmp_path / 'nested'
    writer = make_safe_writer(data_dir=str(data_dir))
    append_bytes(writer, 'test.bin', b'data')
    assert (data_dir / 'test.bin').exists()