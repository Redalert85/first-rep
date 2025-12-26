"""
Pytest configuration and shared fixtures for Bar Exam Tutor tests
"""

import json
import os
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from typing import Generator
from unittest.mock import patch

import pytest

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from bar_tutor_unified import (
    KnowledgeNode,
    FlashcardEntry,
    LearningState,
    LegalKnowledgeGraph,
    InterleavedPracticeEngine,
    PerformanceTracker,
    InteractiveBarTutor,
    BarExamTutor,
    atomic_write_jsonl,
    sanitize_input,
    generate_id,
    DATA_DIR,
    PERFORMANCE_DB,
)


# ==================== FIXTURES: Knowledge Nodes ====================

@pytest.fixture
def sample_knowledge_node() -> KnowledgeNode:
    """Create a basic KnowledgeNode for testing"""
    return KnowledgeNode(
        concept_id="test_offer_acceptance",
        name="Offer and Acceptance",
        subject="contracts",
        difficulty=3,
        prerequisites=["test_formation"],
        related_concepts=["test_consideration"],
        mastery_level=0.0,
        last_reviewed=None,
        review_count=0,
        ease_factor=2.5,
        interval=1,
        rule_statement="A valid contract requires offer and acceptance",
        elements=["Offer", "Acceptance", "Meeting of minds"],
        exceptions=["Revocation before acceptance"],
        policy_rationales=["Freedom of contract"],
        common_traps=["Mirror image rule variations"],
    )


@pytest.fixture
def mastered_knowledge_node() -> KnowledgeNode:
    """Create a mastered KnowledgeNode for testing"""
    return KnowledgeNode(
        concept_id="test_mastered_concept",
        name="Mastered Concept",
        subject="contracts",
        difficulty=2,
        mastery_level=0.95,
        last_reviewed=datetime.now() - timedelta(days=1),
        review_count=10,
        ease_factor=2.8,
        interval=30,
        rule_statement="This is a mastered concept",
    )


@pytest.fixture
def low_mastery_node() -> KnowledgeNode:
    """Create a low mastery KnowledgeNode"""
    return KnowledgeNode(
        concept_id="test_low_mastery",
        name="Low Mastery Concept",
        subject="torts",
        difficulty=4,
        mastery_level=0.2,
        review_count=2,
        ease_factor=2.0,
        interval=1,
    )


@pytest.fixture
def mid_mastery_node() -> KnowledgeNode:
    """Create a mid mastery KnowledgeNode"""
    return KnowledgeNode(
        concept_id="test_mid_mastery",
        name="Mid Mastery Concept",
        subject="evidence",
        difficulty=3,
        mastery_level=0.6,
        review_count=5,
        ease_factor=2.3,
        interval=7,
    )


# ==================== FIXTURES: Knowledge Graph ====================

@pytest.fixture
def knowledge_graph() -> LegalKnowledgeGraph:
    """Create a full LegalKnowledgeGraph for testing"""
    return LegalKnowledgeGraph()


@pytest.fixture
def minimal_knowledge_graph() -> LegalKnowledgeGraph:
    """Create a minimal knowledge graph with patched initialization"""
    kg = LegalKnowledgeGraph.__new__(LegalKnowledgeGraph)
    kg.nodes = {}
    return kg


# ==================== FIXTURES: Practice Engine ====================

@pytest.fixture
def practice_engine(knowledge_graph) -> InterleavedPracticeEngine:
    """Create an InterleavedPracticeEngine for testing"""
    return InterleavedPracticeEngine(knowledge_graph)


# ==================== FIXTURES: Flashcards ====================

@pytest.fixture
def sample_flashcard() -> FlashcardEntry:
    """Create a sample FlashcardEntry for testing"""
    return FlashcardEntry(
        id="flash_001",
        front="What are the elements of a valid contract?",
        back="Offer, Acceptance, Consideration, Capacity, Legality",
        subject="Contracts",
        difficulty="Intermediate",
        ease_factor=2.5,
        interval=1,
        repetitions=0,
    )


@pytest.fixture
def reviewed_flashcard() -> FlashcardEntry:
    """Create a flashcard that has been reviewed"""
    return FlashcardEntry(
        id="flash_002",
        front="What is consideration?",
        back="A bargained-for exchange of value",
        subject="Contracts",
        difficulty="Basic",
        ease_factor=2.6,
        interval=6,
        repetitions=3,
        last_reviewed=(datetime.now() - timedelta(days=6)).isoformat(),
    )


# ==================== FIXTURES: Learning State ====================

@pytest.fixture
def fresh_learning_state() -> LearningState:
    """Create a fresh LearningState"""
    return LearningState()


@pytest.fixture
def active_learning_state() -> LearningState:
    """Create an active learning session state"""
    return LearningState(
        current_subject="torts",
        current_concept="negligence",
        session_started=True,
        questions_asked=5,
        correct_answers=3,
        current_difficulty="intermediate",
        learning_mode="guided",
        last_interaction=datetime.now(),
    )


# ==================== FIXTURES: Temporary Files ====================

@pytest.fixture
def temp_data_dir(tmp_path) -> Generator[Path, None, None]:
    """Create a temporary data directory for file operations"""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    yield data_dir


@pytest.fixture
def temp_performance_file(temp_data_dir) -> Path:
    """Create a temporary performance file"""
    perf_file = temp_data_dir / "performance.jsonl"
    perf_file.touch()
    return perf_file


@pytest.fixture
def populated_performance_file(temp_data_dir) -> Path:
    """Create a performance file with test data"""
    perf_file = temp_data_dir / "performance.jsonl"

    # Add test entries
    entries = [
        {"timestamp": (datetime.now() - timedelta(days=1)).isoformat(), "subject": "contracts", "correct": True},
        {"timestamp": (datetime.now() - timedelta(days=1)).isoformat(), "subject": "contracts", "correct": True},
        {"timestamp": (datetime.now() - timedelta(days=1)).isoformat(), "subject": "contracts", "correct": False},
        {"timestamp": (datetime.now() - timedelta(days=2)).isoformat(), "subject": "torts", "correct": True},
        {"timestamp": (datetime.now() - timedelta(days=2)).isoformat(), "subject": "torts", "correct": False},
        {"timestamp": (datetime.now() - timedelta(days=45)).isoformat(), "subject": "old_subject", "correct": True},  # Outside 30-day window
    ]

    with perf_file.open("w") as f:
        for entry in entries:
            f.write(json.dumps(entry) + "\n")

    return perf_file


# ==================== FIXTURES: Performance Tracker ====================

@pytest.fixture
def performance_tracker(temp_performance_file) -> PerformanceTracker:
    """Create a PerformanceTracker with temporary file"""
    tracker = PerformanceTracker()
    tracker.perf_file = temp_performance_file
    return tracker


# ==================== FIXTURES: Interactive Tutor ====================

@pytest.fixture
def bar_exam_tutor() -> BarExamTutor:
    """Create a BarExamTutor instance"""
    return BarExamTutor()


@pytest.fixture
def interactive_tutor(bar_exam_tutor) -> InteractiveBarTutor:
    """Create an InteractiveBarTutor instance"""
    return InteractiveBarTutor(bar_exam_tutor)


# ==================== HELPER FUNCTIONS ====================

def create_knowledge_node_with_mastery(concept_id: str, subject: str, mastery: float) -> KnowledgeNode:
    """Helper to create a KnowledgeNode with specific mastery level"""
    return KnowledgeNode(
        concept_id=concept_id,
        name=f"Test Concept {concept_id}",
        subject=subject,
        difficulty=3,
        mastery_level=mastery,
    )
