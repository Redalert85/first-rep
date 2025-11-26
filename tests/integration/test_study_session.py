"""
Integration Tests for Study Session Workflow

Tests end-to-end workflows including:
- Complete study session simulation
- Multi-component interaction
- Interactive tutor workflow
- Performance tracking through sessions
"""

import json
import pytest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch, MagicMock

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from bar_tutor_unified import (
    BarExamTutor,
    InteractiveBarTutor,
    LegalKnowledgeGraph,
    InterleavedPracticeEngine,
    PerformanceTracker,
    LearningState,
    atomic_write_jsonl,
)


class TestFullTutorInitialization:
    """Test complete tutor system initialization"""

    def test_bar_exam_tutor_initializes(self):
        """Test BarExamTutor initializes all components"""
        tutor = BarExamTutor()

        assert tutor.kg is not None, "Knowledge graph should be initialized"
        assert isinstance(tutor.kg, LegalKnowledgeGraph)

    def test_knowledge_graph_populated(self):
        """Test knowledge graph has concepts after init"""
        tutor = BarExamTutor()

        assert len(tutor.kg.nodes) > 0, "Should have concepts"

    def test_can_get_subject_concepts(self):
        """Test can retrieve subject concepts after init"""
        tutor = BarExamTutor()

        contracts = tutor.kg.get_subject_concepts("contracts")
        torts = tutor.kg.get_subject_concepts("torts")

        assert len(contracts) > 0
        assert len(torts) > 0


class TestInteractiveTutorSession:
    """Test interactive tutor session workflow"""

    def test_start_session(self, interactive_tutor):
        """Test starting an interactive session"""
        welcome = interactive_tutor.start_session("contracts")

        assert "Welcome" in welcome
        assert "contracts" in welcome.lower()
        assert interactive_tutor.state.session_started is True
        assert interactive_tutor.state.current_subject == "contracts"

    def test_session_tracks_time(self, interactive_tutor):
        """Test session tracks last interaction time"""
        interactive_tutor.start_session()

        assert interactive_tutor.state.last_interaction is not None
        assert isinstance(interactive_tutor.state.last_interaction, datetime)

    def test_help_command(self, interactive_tutor):
        """Test help command"""
        interactive_tutor.start_session()
        response = interactive_tutor.process_input("help")

        assert "Available Commands" in response
        assert "explain" in response.lower()
        assert "practice" in response.lower()

    def test_progress_command(self, interactive_tutor):
        """Test progress command"""
        interactive_tutor.start_session()
        response = interactive_tutor.process_input("progress")

        assert "Progress" in response
        assert "Questions Answered" in response

    def test_quit_command(self, interactive_tutor):
        """Test quit command ends session"""
        interactive_tutor.start_session()
        response = interactive_tutor.process_input("quit")

        assert "ended" in response.lower()
        assert interactive_tutor.state.session_started is False

    def test_explain_command(self, interactive_tutor):
        """Test explain command"""
        interactive_tutor.start_session("contracts")
        response = interactive_tutor.process_input("explain consideration")

        # Should either find concept or say not found
        assert len(response) > 0

    def test_unknown_command(self, interactive_tutor):
        """Test unknown command handling"""
        interactive_tutor.start_session()
        response = interactive_tutor.process_input("unknown_xyz")

        assert "help" in response.lower()


class TestPracticeWorkflow:
    """Test practice generation workflow"""

    def test_generate_and_display_practice(self, bar_exam_tutor, capsys):
        """Test generating and displaying practice"""
        engine = InterleavedPracticeEngine(bar_exam_tutor.kg)

        concepts = engine.generate_practice("contracts", 5)
        engine.display_practice(concepts)

        captured = capsys.readouterr()
        assert "INTERLEAVED PRACTICE SESSION" in captured.out
        assert len(concepts) == 5

    def test_practice_concepts_are_unique(self, bar_exam_tutor):
        """Test practice concepts don't repeat"""
        engine = InterleavedPracticeEngine(bar_exam_tutor.kg)

        concepts = engine.generate_practice("contracts", 10)
        ids = [c.concept_id for c in concepts]

        assert len(ids) == len(set(ids))

    def test_multi_subject_practice(self, bar_exam_tutor):
        """Test practicing multiple subjects"""
        engine = InterleavedPracticeEngine(bar_exam_tutor.kg)

        subjects = ["contracts", "torts", "evidence"]
        for subject in subjects:
            concepts = engine.generate_practice(subject, 3)
            assert len(concepts) == 3
            for c in concepts:
                assert c.subject == subject


class TestPerformanceTrackingWorkflow:
    """Test performance tracking through practice sessions"""

    def test_record_and_retrieve_performance(self, temp_data_dir):
        """Test recording performance and retrieving stats"""
        perf_file = temp_data_dir / "perf.jsonl"
        tracker = PerformanceTracker()
        tracker.perf_file = perf_file

        # Simulate practice session
        tracker.record_attempt("contracts", True)
        tracker.record_attempt("contracts", True)
        tracker.record_attempt("contracts", False)
        tracker.record_attempt("torts", True)

        # Get stats
        stats = tracker.get_stats()

        assert "contracts" in stats
        assert stats["contracts"]["total"] == 3
        assert stats["contracts"]["correct"] == 2
        assert "torts" in stats
        assert stats["torts"]["total"] == 1

    def test_performance_persists_across_instances(self, temp_data_dir):
        """Test performance data persists"""
        perf_file = temp_data_dir / "perf.jsonl"

        # First tracker instance
        tracker1 = PerformanceTracker()
        tracker1.perf_file = perf_file
        tracker1.record_attempt("contracts", True)

        # Second tracker instance
        tracker2 = PerformanceTracker()
        tracker2.perf_file = perf_file
        tracker2.record_attempt("contracts", False)

        # Third instance reads both
        tracker3 = PerformanceTracker()
        tracker3.perf_file = perf_file
        stats = tracker3.get_stats()

        assert stats["contracts"]["total"] == 2


class TestLearningStateManagement:
    """Test learning state management"""

    def test_fresh_state_defaults(self, fresh_learning_state):
        """Test fresh state has correct defaults"""
        state = fresh_learning_state

        assert state.current_subject == "contracts"
        assert state.session_started is False
        assert state.questions_asked == 0
        assert state.correct_answers == 0

    def test_state_updates_during_session(self, interactive_tutor):
        """Test state updates during session"""
        interactive_tutor.start_session("torts")

        assert interactive_tutor.state.current_subject == "torts"
        assert interactive_tutor.state.session_started is True

    def test_state_tracks_accuracy(self, active_learning_state):
        """Test state accuracy calculation"""
        state = active_learning_state

        accuracy = state.correct_answers / max(state.questions_asked, 1) * 100
        expected = 3 / 5 * 100  # 60%

        assert accuracy == expected


class TestEndToEndStudySession:
    """Test complete end-to-end study session"""

    @pytest.mark.integration
    def test_complete_study_workflow(self, temp_data_dir):
        """Test complete study workflow from start to finish"""
        # Setup
        perf_file = temp_data_dir / "perf.jsonl"

        # Initialize tutor
        tutor = BarExamTutor()
        interactive = InteractiveBarTutor(tutor)
        engine = InterleavedPracticeEngine(tutor.kg)
        tracker = PerformanceTracker()
        tracker.perf_file = perf_file

        # Start session
        welcome = interactive.start_session("contracts")
        assert "Welcome" in welcome

        # Generate practice
        concepts = engine.generate_practice("contracts", 5)
        assert len(concepts) == 5

        # Simulate answering questions
        for i, concept in enumerate(concepts):
            correct = i % 2 == 0  # Alternate correct/incorrect
            tracker.record_attempt("contracts", correct)

        # Check progress
        progress = interactive.process_input("progress")
        assert "Progress" in progress

        # Get final stats
        stats = tracker.get_stats()
        assert stats["contracts"]["total"] == 5
        assert stats["contracts"]["correct"] == 3  # 0, 2, 4 are correct

        # End session
        goodbye = interactive.process_input("quit")
        assert "ended" in goodbye.lower()

    @pytest.mark.integration
    def test_multi_subject_study_session(self, temp_data_dir):
        """Test studying multiple subjects in one session"""
        perf_file = temp_data_dir / "perf.jsonl"

        tutor = BarExamTutor()
        engine = InterleavedPracticeEngine(tutor.kg)
        tracker = PerformanceTracker()
        tracker.perf_file = perf_file

        subjects = ["contracts", "torts", "evidence"]

        for subject in subjects:
            concepts = engine.generate_practice(subject, 3)

            for i, concept in enumerate(concepts):
                tracker.record_attempt(subject, i < 2)  # 2 correct, 1 incorrect

        stats = tracker.get_stats()

        for subject in subjects:
            assert subject in stats
            assert stats[subject]["total"] == 3
            assert stats[subject]["correct"] == 2


class TestComponentIntegration:
    """Test integration between components"""

    def test_knowledge_graph_to_practice_engine(self, bar_exam_tutor):
        """Test knowledge graph integrates with practice engine"""
        engine = InterleavedPracticeEngine(bar_exam_tutor.kg)

        concepts = engine.generate_practice("contracts", 5)

        # Verify concepts come from knowledge graph
        for concept in concepts:
            assert concept.concept_id in bar_exam_tutor.kg.nodes

    def test_tutor_exposes_knowledge_graph(self, bar_exam_tutor):
        """Test tutor exposes knowledge graph"""
        assert bar_exam_tutor.kg is not None
        assert len(bar_exam_tutor.kg.nodes) > 0

    def test_interactive_tutor_uses_bar_tutor(self, interactive_tutor):
        """Test interactive tutor uses bar tutor"""
        assert interactive_tutor.bar_tutor is not None
        assert interactive_tutor.bar_tutor.kg is not None
