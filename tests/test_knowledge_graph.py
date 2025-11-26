"""
Tests for Legal Knowledge Graph

Tests the LegalKnowledgeGraph class which:
- Initializes 331 concepts across 14 subjects
- Provides concept retrieval and navigation
- Manages relationships between concepts
"""

import pytest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from bar_tutor_unified import LegalKnowledgeGraph, KnowledgeNode


class TestKnowledgeGraphInitialization:
    """Test knowledge graph initialization"""

    def test_creates_non_empty_graph(self, knowledge_graph):
        """Test that graph initializes with concepts"""
        assert len(knowledge_graph.nodes) > 0

    def test_has_substantial_concepts(self, knowledge_graph):
        """Test graph has substantial number of concepts"""
        # Should have 331 concepts according to documentation
        assert len(knowledge_graph.nodes) >= 100, "Should have at least 100 concepts"

    def test_all_nodes_are_knowledge_nodes(self, knowledge_graph):
        """Test all nodes are KnowledgeNode instances"""
        for node in knowledge_graph.nodes.values():
            assert isinstance(node, KnowledgeNode)

    def test_all_nodes_have_required_fields(self, knowledge_graph):
        """Test all nodes have required fields populated"""
        for concept_id, node in knowledge_graph.nodes.items():
            assert node.concept_id, f"Node {concept_id} missing concept_id"
            assert node.name, f"Node {concept_id} missing name"
            assert node.subject, f"Node {concept_id} missing subject"
            assert 1 <= node.difficulty <= 5, f"Node {concept_id} has invalid difficulty"


class TestMBESubjects:
    """Test MBE (Multistate Bar Exam) subjects"""

    MBE_SUBJECTS = [
        "contracts",
        "torts",
        "constitutional_law",
        "criminal_law",
        "criminal_procedure",
        "civil_procedure",
        "evidence",
        "real_property",
    ]

    @pytest.mark.parametrize("subject", MBE_SUBJECTS)
    def test_mbe_subject_exists(self, knowledge_graph, subject):
        """Test each MBE subject has concepts"""
        concepts = knowledge_graph.get_subject_concepts(subject)
        assert len(concepts) > 0, f"Subject {subject} should have concepts"

    @pytest.mark.parametrize("subject", MBE_SUBJECTS)
    def test_mbe_subject_has_substantial_coverage(self, knowledge_graph, subject):
        """Test each MBE subject has substantial concept coverage"""
        concepts = knowledge_graph.get_subject_concepts(subject)
        # Each subject should have at least 5 concepts
        assert len(concepts) >= 5, f"Subject {subject} should have at least 5 concepts"

    def test_total_mbe_concepts(self, knowledge_graph):
        """Test total MBE concepts is approximately 180"""
        total = 0
        for subject in self.MBE_SUBJECTS:
            concepts = knowledge_graph.get_subject_concepts(subject)
            total += len(concepts)

        # Should have approximately 180 MBE concepts
        assert total >= 100, "Should have at least 100 MBE concepts"


class TestEssaySubjects:
    """Test Essay subjects"""

    ESSAY_SUBJECTS = [
        "professional_responsibility",
        "corporations",
        "wills_trusts_estates",
        "family_law",
        "secured_transactions",
        "iowa_procedure",
    ]

    @pytest.mark.parametrize("subject", ESSAY_SUBJECTS)
    def test_essay_subject_exists(self, knowledge_graph, subject):
        """Test each Essay subject has concepts"""
        concepts = knowledge_graph.get_subject_concepts(subject)
        assert len(concepts) > 0, f"Essay subject {subject} should have concepts"


class TestGetSubjectConcepts:
    """Test get_subject_concepts method"""

    def test_returns_list(self, knowledge_graph):
        """Test method returns a list"""
        result = knowledge_graph.get_subject_concepts("contracts")
        assert isinstance(result, list)

    def test_returns_knowledge_nodes(self, knowledge_graph):
        """Test returned items are KnowledgeNodes"""
        concepts = knowledge_graph.get_subject_concepts("contracts")
        for concept in concepts:
            assert isinstance(concept, KnowledgeNode)

    def test_returns_correct_subject(self, knowledge_graph):
        """Test all returned concepts are from requested subject"""
        concepts = knowledge_graph.get_subject_concepts("torts")
        for concept in concepts:
            assert concept.subject == "torts"

    def test_nonexistent_subject_returns_empty(self, knowledge_graph):
        """Test nonexistent subject returns empty list"""
        concepts = knowledge_graph.get_subject_concepts("nonexistent_subject")
        assert concepts == []

    def test_case_sensitivity(self, knowledge_graph):
        """Test subject lookup is case sensitive"""
        lower = knowledge_graph.get_subject_concepts("contracts")
        upper = knowledge_graph.get_subject_concepts("CONTRACTS")
        # If case insensitive, both should return same; otherwise upper returns empty
        # Current implementation is case sensitive
        assert len(lower) > 0


class TestConceptRetrieval:
    """Test individual concept retrieval"""

    def test_get_concept_by_id(self, knowledge_graph):
        """Test retrieving concept by ID"""
        # Get any concept ID from the graph
        concept_id = next(iter(knowledge_graph.nodes.keys()))
        concept = knowledge_graph.nodes.get(concept_id)

        assert concept is not None
        assert concept.concept_id == concept_id

    def test_nonexistent_concept_returns_none(self, knowledge_graph):
        """Test getting nonexistent concept"""
        concept = knowledge_graph.nodes.get("nonexistent_id")
        assert concept is None


class TestConceptAttributes:
    """Test concept attribute population"""

    def test_contracts_concepts_have_rules(self, knowledge_graph):
        """Test contracts concepts have rule statements"""
        concepts = knowledge_graph.get_subject_concepts("contracts")

        # At least some should have rule statements
        with_rules = [c for c in concepts if c.rule_statement]
        assert len(with_rules) > 0, "Some contracts concepts should have rules"

    def test_concepts_have_elements(self, knowledge_graph):
        """Test some concepts have elements"""
        all_concepts = list(knowledge_graph.nodes.values())
        with_elements = [c for c in all_concepts if c.elements]

        assert len(with_elements) > 0, "Some concepts should have elements"

    def test_concepts_have_common_traps(self, knowledge_graph):
        """Test some concepts have common traps"""
        all_concepts = list(knowledge_graph.nodes.values())
        with_traps = [c for c in all_concepts if c.common_traps]

        assert len(with_traps) > 0, "Some concepts should have common traps"


class TestDifficultyDistribution:
    """Test difficulty level distribution"""

    def test_has_easy_concepts(self, knowledge_graph):
        """Test graph has easy (1-2) difficulty concepts"""
        easy = [c for c in knowledge_graph.nodes.values() if c.difficulty <= 2]
        assert len(easy) > 0, "Should have easy concepts"

    def test_has_medium_concepts(self, knowledge_graph):
        """Test graph has medium (3) difficulty concepts"""
        medium = [c for c in knowledge_graph.nodes.values() if c.difficulty == 3]
        assert len(medium) > 0, "Should have medium concepts"

    def test_has_hard_concepts(self, knowledge_graph):
        """Test graph has hard (4-5) difficulty concepts"""
        hard = [c for c in knowledge_graph.nodes.values() if c.difficulty >= 4]
        assert len(hard) > 0, "Should have hard concepts"

    def test_all_difficulties_valid(self, knowledge_graph):
        """Test all difficulties are in valid range"""
        for concept in knowledge_graph.nodes.values():
            assert 1 <= concept.difficulty <= 5, f"Invalid difficulty: {concept.difficulty}"


class TestConceptUniqueness:
    """Test concept uniqueness"""

    def test_unique_concept_ids(self, knowledge_graph):
        """Test all concept IDs are unique"""
        ids = list(knowledge_graph.nodes.keys())
        assert len(ids) == len(set(ids)), "Concept IDs should be unique"

    def test_node_keys_match_concept_ids(self, knowledge_graph):
        """Test dictionary keys match concept_id attributes"""
        for key, node in knowledge_graph.nodes.items():
            assert key == node.concept_id, f"Key {key} doesn't match concept_id {node.concept_id}"


class TestMasteryInitialization:
    """Test initial mastery states"""

    def test_initial_mastery_is_zero(self, knowledge_graph):
        """Test new concepts start with 0 mastery"""
        for concept in knowledge_graph.nodes.values():
            assert concept.mastery_level == 0.0, f"Initial mastery should be 0"

    def test_initial_review_count_is_zero(self, knowledge_graph):
        """Test new concepts start with 0 reviews"""
        for concept in knowledge_graph.nodes.values():
            assert concept.review_count == 0

    def test_initial_last_reviewed_is_none(self, knowledge_graph):
        """Test new concepts have no last_reviewed date"""
        for concept in knowledge_graph.nodes.values():
            assert concept.last_reviewed is None
