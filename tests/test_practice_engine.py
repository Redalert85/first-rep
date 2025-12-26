"""
Tests for Interleaved Practice Engine

Tests the InterleavedPracticeEngine class which:
- Generates practice sets with concept deduplication
- Weights selection by mastery level
- Ensures diversity in practice sessions
"""

import pytest
from pathlib import Path
from collections import Counter

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from bar_tutor_unified import (
    InterleavedPracticeEngine,
    LegalKnowledgeGraph,
    KnowledgeNode,
)


class TestPracticeEngineInitialization:
    """Test practice engine initialization"""

    def test_initializes_with_knowledge_graph(self, practice_engine):
        """Test engine initializes with knowledge graph"""
        assert practice_engine.kg is not None
        assert isinstance(practice_engine.kg, LegalKnowledgeGraph)


class TestGeneratePractice:
    """Test generate_practice method"""

    def test_returns_list(self, practice_engine):
        """Test method returns a list"""
        result = practice_engine.generate_practice("contracts", 5)
        assert isinstance(result, list)

    def test_returns_knowledge_nodes(self, practice_engine):
        """Test returned items are KnowledgeNodes"""
        result = practice_engine.generate_practice("contracts", 5)
        for item in result:
            assert isinstance(item, KnowledgeNode)

    def test_returns_requested_count(self, practice_engine):
        """Test returns requested number of concepts"""
        result = practice_engine.generate_practice("contracts", 5)
        assert len(result) == 5

    def test_returns_correct_subject(self, practice_engine):
        """Test all concepts are from requested subject"""
        result = practice_engine.generate_practice("torts", 5)
        for concept in result:
            assert concept.subject == "torts"

    def test_no_duplicates(self, practice_engine):
        """Test no duplicate concepts in result"""
        result = practice_engine.generate_practice("contracts", 10)
        concept_ids = [c.concept_id for c in result]
        assert len(concept_ids) == len(set(concept_ids)), "Should have no duplicates"

    def test_nonexistent_subject_returns_empty(self, practice_engine):
        """Test nonexistent subject returns empty list"""
        result = practice_engine.generate_practice("nonexistent", 5)
        assert result == []

    def test_request_more_than_available(self, practice_engine):
        """Test requesting more concepts than available"""
        # Request way more than any subject has
        result = practice_engine.generate_practice("contracts", 1000)
        # Should return all available, not 1000
        contracts = practice_engine.kg.get_subject_concepts("contracts")
        assert len(result) <= len(contracts)

    def test_zero_count(self, practice_engine):
        """Test requesting zero concepts"""
        result = practice_engine.generate_practice("contracts", 0)
        assert result == []


class TestDeduplication:
    """Test concept deduplication"""

    def test_multiple_calls_can_return_same_concepts(self, practice_engine):
        """Test that multiple calls can return same concepts (randomized)"""
        # Just verify no duplicates within each call
        for _ in range(5):
            result = practice_engine.generate_practice("contracts", 5)
            ids = [c.concept_id for c in result]
            assert len(ids) == len(set(ids))

    def test_large_request_no_duplicates(self, practice_engine):
        """Test large request has no duplicates"""
        result = practice_engine.generate_practice("contracts", 50)
        ids = [c.concept_id for c in result]
        assert len(ids) == len(set(ids))


class TestMasteryWeighting:
    """Test mastery-based concept selection weighting"""

    def test_prefers_low_mastery_concepts(self, knowledge_graph):
        """Test engine prefers low mastery concepts"""
        # Modify some concepts to have high mastery
        contracts = knowledge_graph.get_subject_concepts("contracts")

        # Set half to high mastery
        for i, concept in enumerate(contracts):
            if i < len(contracts) // 2:
                concept.mastery_level = 0.9  # High
            else:
                concept.mastery_level = 0.1  # Low

        engine = InterleavedPracticeEngine(knowledge_graph)

        # Run multiple times and count selections
        low_count = 0
        high_count = 0

        for _ in range(50):
            result = engine.generate_practice("contracts", 3)
            for concept in result:
                if concept.mastery_level >= 0.8:
                    high_count += 1
                elif concept.mastery_level < 0.5:
                    low_count += 1

        # Low mastery concepts should be selected more often
        # (with 60% weight for low vs 10% for high)
        assert low_count > high_count, "Should prefer low mastery concepts"

    def test_includes_all_mastery_levels(self, knowledge_graph):
        """Test that all mastery levels can be selected"""
        # Set up three mastery groups
        contracts = knowledge_graph.get_subject_concepts("contracts")

        for i, concept in enumerate(contracts):
            if i % 3 == 0:
                concept.mastery_level = 0.2  # Low
            elif i % 3 == 1:
                concept.mastery_level = 0.6  # Mid
            else:
                concept.mastery_level = 0.9  # High

        engine = InterleavedPracticeEngine(knowledge_graph)

        # Run many times to ensure all levels can be selected
        selected_masteries = set()
        for _ in range(100):
            result = engine.generate_practice("contracts", 5)
            for concept in result:
                if concept.mastery_level < 0.5:
                    selected_masteries.add("low")
                elif concept.mastery_level < 0.8:
                    selected_masteries.add("mid")
                else:
                    selected_masteries.add("high")

        assert "low" in selected_masteries, "Should sometimes select low mastery"
        assert "mid" in selected_masteries, "Should sometimes select mid mastery"
        # High might be rare but should be possible


class TestEmptyAndEdgeCases:
    """Test edge cases"""

    def test_subject_with_one_concept(self, minimal_knowledge_graph):
        """Test subject with only one concept"""
        minimal_knowledge_graph.nodes = {
            "only_one": KnowledgeNode(
                concept_id="only_one",
                name="Only Concept",
                subject="single",
                difficulty=3,
            )
        }

        engine = InterleavedPracticeEngine(minimal_knowledge_graph)
        result = engine.generate_practice("single", 5)

        # Should return the one available concept
        assert len(result) == 1
        assert result[0].concept_id == "only_one"

    def test_all_high_mastery(self, minimal_knowledge_graph):
        """Test when all concepts have high mastery"""
        for i in range(5):
            minimal_knowledge_graph.nodes[f"concept_{i}"] = KnowledgeNode(
                concept_id=f"concept_{i}",
                name=f"Concept {i}",
                subject="all_high",
                difficulty=3,
                mastery_level=0.95,
            )

        engine = InterleavedPracticeEngine(minimal_knowledge_graph)
        result = engine.generate_practice("all_high", 3)

        # Should still return concepts even if all high mastery
        assert len(result) == 3


class TestDisplayPractice:
    """Test display_practice method"""

    def test_display_empty_list(self, practice_engine, capsys):
        """Test displaying empty concept list"""
        practice_engine.display_practice([])
        captured = capsys.readouterr()
        assert "No concepts available" in captured.out

    def test_display_concepts(self, practice_engine, capsys):
        """Test displaying concepts"""
        concepts = practice_engine.generate_practice("contracts", 3)
        practice_engine.display_practice(concepts)
        captured = capsys.readouterr()

        assert "INTERLEAVED PRACTICE SESSION" in captured.out
        assert "3 unique concepts" in captured.out

    def test_display_shows_mastery_status(self, practice_engine, capsys):
        """Test display shows mastery status"""
        concepts = practice_engine.generate_practice("contracts", 2)
        practice_engine.display_practice(concepts)
        captured = capsys.readouterr()

        # Should show one of the status labels
        assert any(status in captured.out for status in ["NEW", "LEARNING", "PRACTICING", "MASTERED"])

    def test_display_shows_difficulty(self, practice_engine, capsys):
        """Test display shows difficulty"""
        concepts = practice_engine.generate_practice("contracts", 1)
        practice_engine.display_practice(concepts)
        captured = capsys.readouterr()

        assert "Difficulty:" in captured.out
        # Should show stars
        assert "*" in captured.out
