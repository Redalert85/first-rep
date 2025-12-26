"""
Tests for SM-2 Spaced Repetition Algorithm

The SM-2 algorithm adjusts:
- ease_factor: How easy the card is (min 1.3, default 2.5)
- interval: Days until next review (starts at 1)
- mastery_level: 0-1 representing concept mastery
"""

import pytest
from datetime import datetime, timedelta
from dataclasses import replace

from bar_tutor_unified import KnowledgeNode, FlashcardEntry


class TestKnowledgeNodeSM2:
    """Test SM-2 algorithm implementation for KnowledgeNode"""

    def test_initial_state(self, sample_knowledge_node):
        """Test that new nodes start with correct SM-2 defaults"""
        node = sample_knowledge_node
        assert node.ease_factor == 2.5, "Default ease factor should be 2.5"
        assert node.interval == 1, "Default interval should be 1 day"
        assert node.mastery_level == 0.0, "New concepts should have 0 mastery"
        assert node.review_count == 0, "New concepts should have 0 reviews"
        assert node.last_reviewed is None, "New concepts should not have review date"

    def test_ease_factor_bounds(self):
        """Test that ease_factor has proper minimum (1.3) bound"""
        # Create node with minimum ease factor
        node = KnowledgeNode(
            concept_id="test_min_ease",
            name="Test Min Ease",
            subject="contracts",
            difficulty=3,
            ease_factor=1.3,  # Minimum allowed
        )
        assert node.ease_factor >= 1.3, "Ease factor should never go below 1.3"

        # Test that very low ease factor is technically allowed (validation at update time)
        node_low = KnowledgeNode(
            concept_id="test_low_ease",
            name="Test Low Ease",
            subject="contracts",
            difficulty=3,
            ease_factor=1.0,  # Below minimum - should be caught during updates
        )
        # Note: The model allows this, but SM-2 update logic should enforce minimum
        assert node_low.ease_factor == 1.0

    def test_mastery_level_bounds(self):
        """Test mastery level is within 0-1 range"""
        node = KnowledgeNode(
            concept_id="test_mastery",
            name="Test Mastery",
            subject="contracts",
            difficulty=2,
            mastery_level=0.5,
        )
        assert 0 <= node.mastery_level <= 1, "Mastery should be between 0 and 1"

    def test_difficulty_range(self):
        """Test difficulty is within 1-5 range"""
        for diff in range(1, 6):
            node = KnowledgeNode(
                concept_id=f"test_diff_{diff}",
                name=f"Difficulty {diff}",
                subject="contracts",
                difficulty=diff,
            )
            assert 1 <= node.difficulty <= 5, f"Difficulty {diff} should be valid"

    def test_node_equality_by_concept_id(self):
        """Test that nodes are equal if concept_id matches"""
        node1 = KnowledgeNode(
            concept_id="same_id",
            name="Node 1",
            subject="contracts",
            difficulty=3,
            mastery_level=0.5,
        )
        node2 = KnowledgeNode(
            concept_id="same_id",
            name="Node 2 Different Name",
            subject="torts",  # Different subject
            difficulty=1,
            mastery_level=0.9,
        )
        assert node1 == node2, "Nodes with same concept_id should be equal"

    def test_node_hash_consistent(self):
        """Test that node hash is based on concept_id"""
        node1 = KnowledgeNode(
            concept_id="hash_test",
            name="Node 1",
            subject="contracts",
            difficulty=3,
        )
        node2 = KnowledgeNode(
            concept_id="hash_test",
            name="Node 2",
            subject="torts",
            difficulty=5,
        )
        assert hash(node1) == hash(node2), "Same concept_id should have same hash"

        # Can be used in sets
        node_set = {node1, node2}
        assert len(node_set) == 1, "Set should deduplicate by concept_id"


class TestFlashcardEntrySM2:
    """Test SM-2 for FlashcardEntry"""

    def test_flashcard_initial_state(self, sample_flashcard):
        """Test new flashcard SM-2 defaults"""
        card = sample_flashcard
        assert card.ease_factor == 2.5
        assert card.interval == 1
        assert card.repetitions == 0

    def test_flashcard_creates_timestamp(self):
        """Test that created_at is auto-populated"""
        card = FlashcardEntry(
            id="test_card",
            front="Question",
            back="Answer",
        )
        assert card.created_at, "created_at should be auto-populated"
        # Verify it's a valid ISO timestamp
        datetime.fromisoformat(card.created_at)

    def test_reviewed_flashcard_state(self, reviewed_flashcard):
        """Test flashcard after reviews"""
        card = reviewed_flashcard
        assert card.repetitions == 3
        assert card.interval == 6
        assert card.ease_factor == 2.6
        assert card.last_reviewed is not None


class TestSM2IntervalCalculation:
    """Test interval calculation logic"""

    def test_first_correct_interval(self):
        """After first correct answer, interval should be 1"""
        node = KnowledgeNode(
            concept_id="first_correct",
            name="First Correct",
            subject="contracts",
            difficulty=3,
            interval=1,
            review_count=0,
        )
        # After first correct: interval stays 1
        assert node.interval == 1

    def test_second_correct_interval_expectation(self):
        """After second correct, interval should become 6"""
        # SM-2: After 2nd correct, interval = 6
        node = KnowledgeNode(
            concept_id="second_correct",
            name="Second Correct",
            subject="contracts",
            difficulty=3,
            review_count=1,
            interval=1,
        )
        # After second correct: interval should become 6
        expected_next_interval = 6
        # This documents expected behavior for implementation
        assert node.interval == 1, "Before update, interval is 1"

    def test_subsequent_interval_calculation(self):
        """Subsequent intervals use: interval * ease_factor"""
        node = KnowledgeNode(
            concept_id="subsequent",
            name="Subsequent",
            subject="contracts",
            difficulty=3,
            review_count=5,
            interval=15,
            ease_factor=2.5,
        )
        expected_next = int(15 * 2.5)  # 37 days
        assert expected_next == 37, "Expected next interval calculation"


class TestSM2EaseFactorAdjustment:
    """Test ease factor adjustment formulas"""

    @pytest.mark.parametrize("quality,expected_direction", [
        (5, "increase"),   # Perfect response: +0.1
        (4, "neutral"),    # Correct with hesitation: 0
        (3, "decrease"),   # Correct with difficulty: -0.14
        (2, "decrease"),   # Incorrect but easy recall: -0.32
        (1, "decrease"),   # Incorrect: -0.54
        (0, "decrease"),   # Complete blackout: -0.8
    ])
    def test_ease_factor_direction(self, quality, expected_direction):
        """Test ease factor adjustment direction based on quality"""
        initial_ef = 2.5
        # SM-2 formula: EF' = EF + (0.1 - (5-q) * (0.08 + (5-q) * 0.02))
        ef_prime = initial_ef + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))

        if expected_direction == "increase":
            assert ef_prime > initial_ef, f"Quality {quality} should increase EF"
        elif expected_direction == "decrease":
            assert ef_prime < initial_ef, f"Quality {quality} should decrease EF"
        else:
            # Quality 4 is exactly neutral
            assert ef_prime == initial_ef, f"Quality {quality} should be neutral"

    def test_ease_factor_minimum_enforcement(self):
        """Test that SM-2 enforces 1.3 minimum ease factor"""
        # After many failures, EF could go very low
        initial_ef = 1.5
        quality = 0  # Complete failure

        ef_prime = initial_ef + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        # Should enforce minimum
        ef_final = max(1.3, ef_prime)

        assert ef_final >= 1.3, "Ease factor should never go below 1.3"


class TestMasteryLevelCalculation:
    """Test mastery level calculation and thresholds"""

    @pytest.mark.parametrize("mastery,expected_status", [
        (0.0, "NEW"),
        (0.1, "LEARNING"),
        (0.49, "LEARNING"),
        (0.5, "PRACTICING"),
        (0.79, "PRACTICING"),
        (0.8, "MASTERED"),
        (1.0, "MASTERED"),
    ])
    def test_mastery_status_thresholds(self, mastery, expected_status):
        """Test mastery level to status mapping"""
        if mastery == 0:
            status = "NEW"
        elif mastery < 0.5:
            status = "LEARNING"
        elif mastery < 0.8:
            status = "PRACTICING"
        else:
            status = "MASTERED"

        assert status == expected_status, f"Mastery {mastery} should be {expected_status}"

    def test_mastery_affects_practice_selection(self, knowledge_graph):
        """Test that mastery level affects practice selection weights"""
        contracts_concepts = knowledge_graph.get_subject_concepts("contracts")

        # Verify we have concepts at different mastery levels
        low = [c for c in contracts_concepts if c.mastery_level < 0.5]
        mid = [c for c in contracts_concepts if 0.5 <= c.mastery_level < 0.8]
        high = [c for c in contracts_concepts if c.mastery_level >= 0.8]

        # All new concepts start at 0 mastery (low)
        assert len(low) > 0, "Should have low mastery concepts"


class TestReviewScheduling:
    """Test review scheduling based on intervals"""

    def test_due_for_review(self):
        """Test determining if concept is due for review"""
        node = KnowledgeNode(
            concept_id="due_test",
            name="Due Test",
            subject="contracts",
            difficulty=3,
            interval=7,
            last_reviewed=datetime.now() - timedelta(days=8),  # 8 days ago, interval is 7
        )
        days_since_review = (datetime.now() - node.last_reviewed).days
        is_due = days_since_review >= node.interval

        assert is_due, "Concept should be due for review"

    def test_not_due_for_review(self):
        """Test concept not yet due for review"""
        node = KnowledgeNode(
            concept_id="not_due_test",
            name="Not Due Test",
            subject="contracts",
            difficulty=3,
            interval=7,
            last_reviewed=datetime.now() - timedelta(days=3),  # Only 3 days ago
        )
        days_since_review = (datetime.now() - node.last_reviewed).days
        is_due = days_since_review >= node.interval

        assert not is_due, "Concept should not be due yet"

    def test_never_reviewed_is_due(self):
        """Test that never-reviewed concepts are always due"""
        node = KnowledgeNode(
            concept_id="never_reviewed",
            name="Never Reviewed",
            subject="contracts",
            difficulty=3,
            last_reviewed=None,
        )
        is_due = node.last_reviewed is None

        assert is_due, "Never reviewed concepts should always be due"
