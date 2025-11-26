"""
Tests for Data Persistence Layer

Tests the atomic_write_jsonl function and related file operations:
- Atomic writes with fsync
- Directory creation
- Unicode handling
- Error handling
"""

import json
import os
import pytest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch, MagicMock

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from bar_tutor_unified import atomic_write_jsonl, generate_id


class TestAtomicWriteJSONL:
    """Test atomic_write_jsonl function"""

    def test_basic_write(self, temp_data_dir):
        """Test basic write operation"""
        filepath = temp_data_dir / "test.jsonl"
        data = {"key": "value", "number": 42}

        atomic_write_jsonl(filepath, data)

        assert filepath.exists()
        with filepath.open("r") as f:
            line = f.readline().strip()
            parsed = json.loads(line)

        assert parsed == data

    def test_creates_parent_directory(self, tmp_path):
        """Test that missing parent directories are created"""
        filepath = tmp_path / "nested" / "deep" / "path" / "file.jsonl"

        data = {"test": "nested"}
        atomic_write_jsonl(filepath, data)

        assert filepath.exists()
        with filepath.open("r") as f:
            parsed = json.loads(f.readline())
        assert parsed == data

    def test_appends_to_existing_file(self, temp_data_dir):
        """Test that writes append to existing file"""
        filepath = temp_data_dir / "append.jsonl"

        # Write first entry
        atomic_write_jsonl(filepath, {"entry": 1})
        # Write second entry
        atomic_write_jsonl(filepath, {"entry": 2})
        # Write third entry
        atomic_write_jsonl(filepath, {"entry": 3})

        with filepath.open("r") as f:
            lines = f.readlines()

        assert len(lines) == 3
        assert json.loads(lines[0])["entry"] == 1
        assert json.loads(lines[1])["entry"] == 2
        assert json.loads(lines[2])["entry"] == 3

    def test_unicode_handling(self, temp_data_dir):
        """Test proper Unicode handling"""
        filepath = temp_data_dir / "unicode.jsonl"

        data = {
            "text": "Hello, 世界! 🎓",
            "legal_term": "force majeure",
            "symbols": "§ ¶ © ® ™",
        }

        atomic_write_jsonl(filepath, data)

        with filepath.open("r", encoding="utf-8") as f:
            parsed = json.loads(f.readline())

        assert parsed["text"] == "Hello, 世界! 🎓"
        assert parsed["symbols"] == "§ ¶ © ® ™"

    def test_newline_terminated(self, temp_data_dir):
        """Test that each entry is newline terminated"""
        filepath = temp_data_dir / "newlines.jsonl"

        atomic_write_jsonl(filepath, {"first": True})
        atomic_write_jsonl(filepath, {"second": True})

        content = filepath.read_text()
        lines = content.split("\n")

        # Should have 2 data lines + 1 empty string after final newline
        assert len(lines) == 3
        assert lines[2] == ""  # Empty after final newline

    def test_complex_nested_data(self, temp_data_dir):
        """Test writing complex nested structures"""
        filepath = temp_data_dir / "complex.jsonl"

        data = {
            "concept_id": "test_123",
            "elements": ["Element A", "Element B", "Element C"],
            "metadata": {
                "created": datetime.now().isoformat(),
                "tags": ["tag1", "tag2"],
                "nested": {
                    "deep": True,
                    "values": [1, 2, 3],
                }
            },
            "scores": [0.5, 0.75, 0.9],
        }

        atomic_write_jsonl(filepath, data)

        with filepath.open("r") as f:
            parsed = json.loads(f.readline())

        assert parsed["elements"] == ["Element A", "Element B", "Element C"]
        assert parsed["metadata"]["nested"]["deep"] is True
        assert parsed["scores"] == [0.5, 0.75, 0.9]

    def test_empty_dict(self, temp_data_dir):
        """Test writing empty dictionary"""
        filepath = temp_data_dir / "empty.jsonl"

        atomic_write_jsonl(filepath, {})

        with filepath.open("r") as f:
            parsed = json.loads(f.readline())

        assert parsed == {}

    def test_special_json_values(self, temp_data_dir):
        """Test handling of special JSON values"""
        filepath = temp_data_dir / "special.jsonl"

        data = {
            "null_value": None,
            "true_value": True,
            "false_value": False,
            "zero": 0,
            "empty_string": "",
            "empty_list": [],
        }

        atomic_write_jsonl(filepath, data)

        with filepath.open("r") as f:
            parsed = json.loads(f.readline())

        assert parsed["null_value"] is None
        assert parsed["true_value"] is True
        assert parsed["false_value"] is False
        assert parsed["zero"] == 0
        assert parsed["empty_string"] == ""
        assert parsed["empty_list"] == []


class TestAtomicWriteFileSync:
    """Test fsync behavior for data integrity"""

    def test_calls_fsync(self, temp_data_dir):
        """Test that fsync is called after write"""
        filepath = temp_data_dir / "sync.jsonl"

        with patch("os.fsync") as mock_fsync:
            atomic_write_jsonl(filepath, {"test": True})
            assert mock_fsync.called, "fsync should be called for data integrity"

    def test_file_contains_data_after_write(self, temp_data_dir):
        """Test that file contains data after atomic write (verifies write+flush)"""
        filepath = temp_data_dir / "order.jsonl"

        atomic_write_jsonl(filepath, {"test": True})

        # Verify file was written and flushed
        assert filepath.exists()
        content = filepath.read_text()
        assert "test" in content
        assert "true" in content.lower()


class TestGenerateId:
    """Test ID generation function"""

    def test_generates_12_char_id(self):
        """Test ID is 12 characters"""
        content = "test content"
        id_result = generate_id(content)
        assert len(id_result) == 12

    def test_consistent_for_same_content(self):
        """Test same content generates same ID"""
        content = "consistent content"
        id1 = generate_id(content)
        id2 = generate_id(content)
        assert id1 == id2

    def test_different_for_different_content(self):
        """Test different content generates different IDs"""
        id1 = generate_id("content A")
        id2 = generate_id("content B")
        assert id1 != id2

    def test_handles_unicode(self):
        """Test Unicode content handling"""
        id_result = generate_id("Hello 世界 🌍")
        assert len(id_result) == 12
        assert id_result.isalnum() or all(c in "0123456789abcdef" for c in id_result)

    def test_handles_empty_string(self):
        """Test empty string handling"""
        id_result = generate_id("")
        assert len(id_result) == 12

    def test_hexadecimal_output(self):
        """Test output is hexadecimal"""
        id_result = generate_id("any content")
        assert all(c in "0123456789abcdef" for c in id_result)


class TestFileErrorHandling:
    """Test error handling for file operations"""

    @pytest.mark.skipif(os.geteuid() == 0, reason="Root bypasses permission checks")
    def test_raises_on_permission_error(self, temp_data_dir):
        """Test handling of permission errors"""
        filepath = temp_data_dir / "readonly.jsonl"
        filepath.touch()

        # Make file read-only (Unix only)
        if os.name != "nt":  # Skip on Windows
            os.chmod(filepath, 0o444)

            try:
                with pytest.raises(PermissionError):
                    atomic_write_jsonl(filepath, {"test": True})
            finally:
                # Restore permissions for cleanup
                os.chmod(filepath, 0o644)

    def test_write_creates_missing_directories(self, tmp_path):
        """Test that atomic_write_jsonl creates missing parent directories"""
        nested_path = tmp_path / "deeply" / "nested" / "path" / "file.jsonl"

        # Should not raise - function creates directories
        atomic_write_jsonl(nested_path, {"test": True})

        assert nested_path.exists()
        assert nested_path.parent.exists()


class TestJSONLFormat:
    """Test JSONL format compliance"""

    def test_valid_jsonl_format(self, temp_data_dir):
        """Test output is valid JSONL"""
        filepath = temp_data_dir / "valid.jsonl"

        # Write multiple entries
        for i in range(5):
            atomic_write_jsonl(filepath, {"index": i, "data": f"entry_{i}"})

        # Validate each line is valid JSON
        with filepath.open("r") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if line:  # Skip empty lines
                    try:
                        json.loads(line)
                    except json.JSONDecodeError as e:
                        pytest.fail(f"Line {line_num} is not valid JSON: {e}")

    def test_no_pretty_printing(self, temp_data_dir):
        """Test JSON is compact (no pretty printing)"""
        filepath = temp_data_dir / "compact.jsonl"

        data = {"nested": {"deep": {"value": True}}}
        atomic_write_jsonl(filepath, data)

        with filepath.open("r") as f:
            content = f.read()

        # Should be single line (plus newline)
        lines = content.strip().split("\n")
        assert len(lines) == 1, "JSON should be compact, not pretty-printed"
