from pathlib import Path

from app.ingestion.hashing import calculate_file_hash


def test_calculate_file_hash_is_stable(tmp_path: Path) -> None:
    file_path = tmp_path / "sample.txt"
    file_path.write_text("AI teaching tutor", encoding="utf-8")

    first_hash = calculate_file_hash(str(file_path))
    second_hash = calculate_file_hash(str(file_path))

    assert first_hash == second_hash
    assert len(first_hash) == 64
