"""
Tests for Input Sanitization and Validation

Tests the sanitize_input function which:
- Removes control characters
- Truncates to max length
- Handles non-string input
- Preserves valid content
"""

import pytest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from bar_tutor_unified import sanitize_input


class TestSanitizeInputBasic:
    """Test basic sanitization functionality"""

    def test_normal_input_unchanged(self):
        """Test that normal input passes through unchanged"""
        text = "This is a normal question about contracts."
        result = sanitize_input(text)
        assert result == text

    def test_strips_whitespace(self):
        """Test that leading/trailing whitespace is stripped"""
        text = "   padded text   "
        result = sanitize_input(text)
        assert result == "padded text"

    def test_empty_string(self):
        """Test empty string handling"""
        result = sanitize_input("")
        assert result == ""

    def test_whitespace_only(self):
        """Test whitespace-only string"""
        result = sanitize_input("   \t\n   ")
        assert result == ""


class TestControlCharacterRemoval:
    """Test removal of control characters"""

    def test_removes_null_character(self):
        """Test removal of null character"""
        text = "Hello\x00World"
        result = sanitize_input(text)
        assert "\x00" not in result
        assert result == "HelloWorld"

    def test_removes_bell_character(self):
        """Test removal of bell character"""
        text = "Hello\x07World"
        result = sanitize_input(text)
        assert "\x07" not in result

    def test_removes_backspace(self):
        """Test removal of backspace character"""
        text = "Hello\x08World"
        result = sanitize_input(text)
        assert "\x08" not in result

    def test_removes_escape_character(self):
        """Test removal of escape character"""
        text = "Hello\x1bWorld"
        result = sanitize_input(text)
        assert "\x1b" not in result

    def test_removes_form_feed(self):
        """Test removal of form feed"""
        text = "Hello\x0cWorld"
        result = sanitize_input(text)
        assert "\x0c" not in result

    def test_removes_vertical_tab(self):
        """Test removal of vertical tab"""
        text = "Hello\x0bWorld"
        result = sanitize_input(text)
        assert "\x0b" not in result

    @pytest.mark.parametrize("control_char", [
        "\x00", "\x01", "\x02", "\x03", "\x04", "\x05", "\x06", "\x07",
        "\x08", "\x0b", "\x0c", "\x0e", "\x0f", "\x10", "\x11", "\x12",
        "\x13", "\x14", "\x15", "\x16", "\x17", "\x18", "\x19", "\x1a",
        "\x1b", "\x1c", "\x1d", "\x1e", "\x1f",
    ])
    def test_removes_all_control_characters(self, control_char):
        """Test removal of all ASCII control characters"""
        text = f"Before{control_char}After"
        result = sanitize_input(text)
        assert control_char not in result


class TestPreservedCharacters:
    """Test that valid characters are preserved"""

    def test_preserves_newline(self):
        """Test that newline is preserved"""
        text = "Line 1\nLine 2"
        result = sanitize_input(text)
        assert "\n" in result
        assert result == "Line 1\nLine 2"

    def test_preserves_carriage_return(self):
        """Test that carriage return is preserved"""
        text = "Line 1\rLine 2"
        result = sanitize_input(text)
        assert "\r" in result

    def test_preserves_tab(self):
        """Test that tab is preserved"""
        text = "Column1\tColumn2"
        result = sanitize_input(text)
        assert "\t" in result
        assert result == "Column1\tColumn2"

    def test_preserves_printable_ascii(self):
        """Test that all printable ASCII is preserved (except stripped whitespace)"""
        # chr(32) is space, which gets stripped at ends
        printable = "".join(chr(i) for i in range(33, 127))  # Skip leading space
        result = sanitize_input(printable)
        assert result == printable


class TestMaxLengthTruncation:
    """Test max length truncation"""

    def test_default_max_length(self):
        """Test default max length is 2000"""
        text = "x" * 3000
        result = sanitize_input(text)
        assert len(result) == 2000

    def test_custom_max_length(self):
        """Test custom max length"""
        text = "x" * 100
        result = sanitize_input(text, max_length=50)
        assert len(result) == 50

    def test_under_max_length_unchanged(self):
        """Test that text under max length is unchanged"""
        text = "Short text"
        result = sanitize_input(text, max_length=100)
        assert result == text

    def test_exactly_max_length(self):
        """Test text exactly at max length"""
        text = "x" * 50
        result = sanitize_input(text, max_length=50)
        assert len(result) == 50
        assert result == text

    def test_zero_max_length(self):
        """Test zero max length"""
        text = "Any text"
        result = sanitize_input(text, max_length=0)
        assert result == ""

    def test_truncation_preserves_start(self):
        """Test that truncation keeps the beginning"""
        text = "KEEP_THIS" + "x" * 2000
        result = sanitize_input(text, max_length=100)
        assert result.startswith("KEEP_THIS")


class TestNonStringInput:
    """Test handling of non-string input"""

    def test_none_input(self):
        """Test None input returns empty string"""
        result = sanitize_input(None)
        assert result == ""

    def test_integer_input(self):
        """Test integer input returns empty string"""
        result = sanitize_input(42)
        assert result == ""

    def test_float_input(self):
        """Test float input returns empty string"""
        result = sanitize_input(3.14)
        assert result == ""

    def test_list_input(self):
        """Test list input returns empty string"""
        result = sanitize_input(["a", "b", "c"])
        assert result == ""

    def test_dict_input(self):
        """Test dict input returns empty string"""
        result = sanitize_input({"key": "value"})
        assert result == ""

    def test_boolean_input(self):
        """Test boolean input returns empty string"""
        result = sanitize_input(True)
        assert result == ""
        result = sanitize_input(False)
        assert result == ""


class TestUnicodeHandling:
    """Test Unicode character handling"""

    def test_preserves_unicode_letters(self):
        """Test that Unicode letters are preserved"""
        text = "Hello, 世界! Привет! مرحبا!"
        result = sanitize_input(text)
        assert "世界" in result
        assert "Привет" in result
        assert "مرحبا" in result

    def test_preserves_emojis(self):
        """Test that emojis are preserved"""
        text = "Study hard! 📚📖✏️"
        result = sanitize_input(text)
        assert "📚" in result
        assert "📖" in result
        assert "✏️" in result

    def test_preserves_legal_symbols(self):
        """Test that legal symbols are preserved"""
        text = "Section § Paragraph ¶ Copyright © Trademark ™"
        result = sanitize_input(text)
        assert "§" in result
        assert "¶" in result
        assert "©" in result
        assert "™" in result

    def test_preserves_currency_symbols(self):
        """Test that currency symbols are preserved"""
        text = "Damages: $1,000 or €500 or £300"
        result = sanitize_input(text)
        assert "$" in result
        assert "€" in result
        assert "£" in result


class TestEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_mixed_valid_and_control_chars(self):
        """Test mixed valid content with control characters"""
        text = "Valid\x00Text\x07With\x1bControl\x0cChars"
        result = sanitize_input(text)
        assert result == "ValidTextWithControlChars"

    def test_only_control_characters(self):
        """Test string with only control characters"""
        text = "\x00\x01\x02\x03\x04\x05"
        result = sanitize_input(text)
        assert result == ""

    def test_control_chars_with_whitespace(self):
        """Test control chars surrounded by whitespace"""
        text = "  \x00\x07  "
        result = sanitize_input(text)
        assert result == ""

    def test_truncation_then_strip(self):
        """Test that truncation happens before stripping"""
        text = "Content" + " " * 2000  # Content followed by spaces
        result = sanitize_input(text, max_length=100)
        # After truncation at 100, then strip
        assert len(result) <= 100

    def test_very_long_unicode(self):
        """Test very long Unicode string"""
        text = "世" * 3000
        result = sanitize_input(text)
        assert len(result) == 2000

    def test_multiline_with_control_chars(self):
        """Test multiline text with embedded control characters"""
        text = "Line 1\x00\nLine 2\x07\nLine 3"
        result = sanitize_input(text)
        assert result == "Line 1\nLine 2\nLine 3"
        # Verify newlines are preserved
        assert result.count("\n") == 2


class TestSecurityConsiderations:
    """Test security-related sanitization"""

    def test_removes_ansi_escape_sequences(self):
        """Test removal of ANSI escape sequences"""
        # ANSI escape starts with \x1b
        text = "Normal\x1b[31mRed Text\x1b[0m"
        result = sanitize_input(text)
        assert "\x1b" not in result

    def test_handles_null_byte_injection(self):
        """Test handling of null byte injection attempts"""
        text = "command\x00--dangerous-flag"
        result = sanitize_input(text)
        assert "\x00" not in result
        assert result == "command--dangerous-flag"

    def test_preserves_html_entities(self):
        """Test that HTML entities are preserved (not security concern at this layer)"""
        text = "&lt;script&gt;alert('xss')&lt;/script&gt;"
        result = sanitize_input(text)
        assert result == text  # HTML escaping is a different concern

    def test_preserves_sql_like_content(self):
        """Test that SQL-like content is preserved (sanitization is different from SQL escaping)"""
        text = "SELECT * FROM users WHERE id = 1"
        result = sanitize_input(text)
        assert result == text
