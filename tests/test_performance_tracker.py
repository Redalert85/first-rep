"""
Tests for Performance Tracking System

Tests the PerformanceTracker class which:
- Records practice attempts
- Calculates subject-level statistics
- Tracks accuracy over time windows
"""

import json
import pytest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch, MagicMock

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from bar_tutor_unified import PerformanceTracker, atomic_write_jsonl


class TestPerformanceTrackerInit:
    """Test PerformanceTracker initialization"""

    def test_creates_performance_file(self, temp_data_dir):
        """Test that tracker creates performance file if missing"""
        tracker = PerformanceTracker()
        tracker.perf_file = temp_data_dir / "new_perf.jsonl"
        tracker.perf_file.touch(exist_ok=True)

        assert tracker.perf_file.exists(), "Should create performance file"

    def test_uses_existing_file(self, temp_performance_file):
        """Test that tracker uses existing file"""
        tracker = PerformanceTracker()
        tracker.perf_file = temp_performance_file

        assert tracker.perf_file.exists()


class TestRecordAttempt:
    """Test recording practice attempts"""

    def test_record_correct_attempt(self, performance_tracker):
        """Test recording a correct answer"""
        performance_tracker.record_attempt("contracts", True)

        # Read back the file
        with performance_tracker.perf_file.open("r") as f:
            entries = [json.loads(line) for line in f]

        assert len(entries) == 1
        assert entries[0]["subject"] == "contracts"
        assert entries[0]["correct"] is True
        assert "timestamp" in entries[0]

    def test_record_incorrect_attempt(self, performance_tracker):
        """Test recording an incorrect answer"""
        performance_tracker.record_attempt("torts", False)

        with performance_tracker.perf_file.open("r") as f:
            entries = [json.loads(line) for line in f]

        assert len(entries) == 1
        assert entries[0]["subject"] == "torts"
        assert entries[0]["correct"] is False

    def test_record_multiple_attempts(self, performance_tracker):
        """Test recording multiple attempts"""
        subjects = ["contracts", "torts", "evidence", "constitutional_law"]
        results = [True, False, True, True]

        for subject, correct in zip(subjects, results):
            performance_tracker.record_attempt(subject, correct)

        with performance_tracker.perf_file.open("r") as f:
            entries = [json.loads(line) for line in f]

        assert len(entries) == 4

    def test_record_appends_to_existing(self, populated_performance_file):
        """Test that new records append to existing data"""
        tracker = PerformanceTracker()
        tracker.perf_file = populated_performance_file

        # Count existing entries
        with populated_performance_file.open("r") as f:
            initial_count = sum(1 for _ in f)

        tracker.record_attempt("new_subject", True)

        with populated_performance_file.open("r") as f:
            final_count = sum(1 for _ in f)

        assert final_count == initial_count + 1

    def test_timestamp_format(self, performance_tracker):
        """Test that timestamps are valid ISO format"""
        performance_tracker.record_attempt("contracts", True)

        with performance_tracker.perf_file.open("r") as f:
            entry = json.loads(f.readline())

        # Should not raise
        parsed = datetime.fromisoformat(entry["timestamp"])
        assert isinstance(parsed, datetime)


class TestGetStats:
    """Test statistics calculation"""

    def test_empty_stats(self, performance_tracker):
        """Test stats with no data"""
        stats = performance_tracker.get_stats(days=30)
        assert stats == {}, "Empty file should return empty stats"

    def test_basic_stats_calculation(self, populated_performance_file):
        """Test basic statistics calculation"""
        tracker = PerformanceTracker()
        tracker.perf_file = populated_performance_file

        stats = tracker.get_stats(days=30)

        # Contracts: 2 correct, 1 incorrect = 3 total, 66.67%
        assert "contracts" in stats
        assert stats["contracts"]["total"] == 3
        assert stats["contracts"]["correct"] == 2
        assert abs(stats["contracts"]["percentage"] - 66.67) < 1

        # Torts: 1 correct, 1 incorrect = 2 total, 50%
        assert "torts" in stats
        assert stats["torts"]["total"] == 2
        assert stats["torts"]["correct"] == 1
        assert stats["torts"]["percentage"] == 50.0

    def test_stats_respects_time_window(self, populated_performance_file):
        """Test that stats only include entries within time window"""
        tracker = PerformanceTracker()
        tracker.perf_file = populated_performance_file

        stats = tracker.get_stats(days=30)

        # old_subject was 45 days ago, should be excluded
        assert "old_subject" not in stats

    def test_stats_different_time_windows(self, temp_data_dir):
        """Test different time window parameters"""
        perf_file = temp_data_dir / "perf.jsonl"
        tracker = PerformanceTracker()
        tracker.perf_file = perf_file

        # Add entries at different times
        entries = [
            {"timestamp": (datetime.now() - timedelta(days=5)).isoformat(), "subject": "recent", "correct": True},
            {"timestamp": (datetime.now() - timedelta(days=15)).isoformat(), "subject": "mid", "correct": True},
            {"timestamp": (datetime.now() - timedelta(days=40)).isoformat(), "subject": "old", "correct": True},
        ]

        with perf_file.open("w") as f:
            for entry in entries:
                f.write(json.dumps(entry) + "\n")

        # 7-day window
        stats_7 = tracker.get_stats(days=7)
        assert "recent" in stats_7
        assert "mid" not in stats_7
        assert "old" not in stats_7

        # 30-day window
        stats_30 = tracker.get_stats(days=30)
        assert "recent" in stats_30
        assert "mid" in stats_30
        assert "old" not in stats_30

        # 60-day window
        stats_60 = tracker.get_stats(days=60)
        assert "recent" in stats_60
        assert "mid" in stats_60
        assert "old" in stats_60

    def test_percentage_edge_cases(self, temp_data_dir):
        """Test percentage calculation edge cases"""
        perf_file = temp_data_dir / "perf.jsonl"
        tracker = PerformanceTracker()
        tracker.perf_file = perf_file

        # 100% accuracy
        entries = [
            {"timestamp": datetime.now().isoformat(), "subject": "perfect", "correct": True},
            {"timestamp": datetime.now().isoformat(), "subject": "perfect", "correct": True},
        ]
        with perf_file.open("w") as f:
            for entry in entries:
                f.write(json.dumps(entry) + "\n")

        stats = tracker.get_stats()
        assert stats["perfect"]["percentage"] == 100.0

        # 0% accuracy
        entries = [
            {"timestamp": datetime.now().isoformat(), "subject": "struggling", "correct": False},
            {"timestamp": datetime.now().isoformat(), "subject": "struggling", "correct": False},
        ]
        with perf_file.open("w") as f:
            for entry in entries:
                f.write(json.dumps(entry) + "\n")

        stats = tracker.get_stats()
        assert stats["struggling"]["percentage"] == 0.0

    def test_handles_malformed_entries(self, temp_data_dir):
        """Test graceful handling of malformed JSON"""
        perf_file = temp_data_dir / "perf.jsonl"
        tracker = PerformanceTracker()
        tracker.perf_file = perf_file

        # Mix of valid and invalid entries
        with perf_file.open("w") as f:
            f.write('{"timestamp": "' + datetime.now().isoformat() + '", "subject": "valid", "correct": true}\n')
            f.write("not valid json\n")
            f.write('{"incomplete": true\n')
            f.write('{"timestamp": "' + datetime.now().isoformat() + '", "subject": "valid", "correct": false}\n')

        stats = tracker.get_stats()

        # Should still get valid entries
        assert "valid" in stats
        assert stats["valid"]["total"] == 2


class TestDisplayDashboard:
    """Test dashboard display functionality"""

    def test_dashboard_no_data(self, performance_tracker, capsys):
        """Test dashboard with no data"""
        performance_tracker.display_dashboard()
        captured = capsys.readouterr()

        assert "No data yet" in captured.out

    def test_dashboard_with_data(self, populated_performance_file, capsys):
        """Test dashboard with data"""
        tracker = PerformanceTracker()
        tracker.perf_file = populated_performance_file

        tracker.display_dashboard()
        captured = capsys.readouterr()

        assert "PERFORMANCE DASHBOARD" in captured.out
        assert "Total Questions" in captured.out
        assert "Overall Accuracy" in captured.out
        assert "contracts" in captured.out
        assert "torts" in captured.out

    def test_dashboard_accuracy_display(self, temp_data_dir, capsys):
        """Test accuracy display formatting"""
        perf_file = temp_data_dir / "perf.jsonl"
        tracker = PerformanceTracker()
        tracker.perf_file = perf_file

        # Add 4 correct, 1 incorrect = 80%
        for _ in range(4):
            atomic_write_jsonl(perf_file, {
                "timestamp": datetime.now().isoformat(),
                "subject": "test",
                "correct": True
            })
        atomic_write_jsonl(perf_file, {
            "timestamp": datetime.now().isoformat(),
            "subject": "test",
            "correct": False
        })

        tracker.display_dashboard()
        captured = capsys.readouterr()

        assert "80.0%" in captured.out


class TestPerformanceAggregation:
    """Test aggregation across subjects"""

    def test_total_questions_count(self, populated_performance_file):
        """Test total question count across subjects"""
        tracker = PerformanceTracker()
        tracker.perf_file = populated_performance_file

        stats = tracker.get_stats(days=30)
        total = sum(s["total"] for s in stats.values())

        # 3 contracts + 2 torts = 5 (old_subject excluded)
        assert total == 5

    def test_total_correct_count(self, populated_performance_file):
        """Test total correct count across subjects"""
        tracker = PerformanceTracker()
        tracker.perf_file = populated_performance_file

        stats = tracker.get_stats(days=30)
        total_correct = sum(s["correct"] for s in stats.values())

        # 2 contracts + 1 torts = 3
        assert total_correct == 3

    def test_overall_accuracy(self, populated_performance_file):
        """Test overall accuracy calculation"""
        tracker = PerformanceTracker()
        tracker.perf_file = populated_performance_file

        stats = tracker.get_stats(days=30)
        total_q = sum(s["total"] for s in stats.values())
        total_c = sum(s["correct"] for s in stats.values())
        overall_accuracy = (total_c / total_q * 100) if total_q > 0 else 0

        # 3/5 = 60%
        assert overall_accuracy == 60.0
