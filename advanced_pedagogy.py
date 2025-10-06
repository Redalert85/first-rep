#!/usr/bin/env python3
"""
Advanced Pedagogical Techniques for MBE Study
Implements evidence-based learning strategies from cognitive science
"""

import json
import random
import time
from datetime import datetime, timedelta
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from statistics import mean, stdev

class LearningMode(Enum):
    """Different learning modes based on cognitive science"""
    FOCUSED_PRACTICE = "focused"        # Single subject deep dive
    INTERLEAVED_PRACTICE = "interleaved" # Mixed subjects for better retention
    RETRIEVAL_PRACTICE = "retrieval"     # Testing without answers
    SPACED_REPETITION = "spaced"         # SM-2 algorithm
    DIAGNOSTIC_ASSESSMENT = "diagnostic" # Identify knowledge gaps
    ADAPTIVE_DIFFICULTY = "adaptive"     # AI adjusts difficulty
    CONCEPT_MAPPING = "mapping"          # Visual concept relationships
    SOCRATIC_DIALOGUE = "socratic"       # Guided discovery learning

class CognitiveStrategy(Enum):
    """Evidence-based cognitive strategies"""
    DUAL_CODING = "dual_coding"          # Visual + verbal learning
    ELABORATION = "elaboration"           # Deep processing
    SELF_EXPLANATION = "self_explanation" # Explain concepts to yourself
    INTERLEAVING = "interleaving"         # Mix related concepts
    SPACING = "spacing"                  # Distributed practice
    TESTING = "testing"                  # Retrieval practice
    GENERATION = "generation"            # Active recall

@dataclass
class StudySession:
    """Represents a study session with advanced tracking"""
    session_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    mode: LearningMode = LearningMode.FOCUSED_PRACTICE
    subject: str = "mixed"
    questions_attempted: int = 0
    questions_correct: int = 0
    time_spent: int = 0  # seconds
    cognitive_strategies_used: List[CognitiveStrategy] = field(default_factory=list)
    confidence_ratings: List[int] = field(default_factory=list)  # 1-5 scale
    difficulty_ratings: List[int] = field(default_factory=list)  # 1-5 scale
    meta_cognition_notes: str = ""

@dataclass
class KnowledgeNode:
    """Represents a concept in the knowledge graph"""
    concept_id: str
    name: str
    subject: str
    difficulty: int  # 1-5
    prerequisites: List[str] = field(default_factory=list)
    related_concepts: List[str] = field(default_factory=list)
    mastery_level: float = 0.0  # 0-1
    last_reviewed: Optional[datetime] = None
    review_count: int = 0
    ease_factor: float = 2.5  # SM-2 ease factor
    interval: int = 1  # days until next review

class AdvancedPedagogyEngine:
    """
    Advanced pedagogical engine implementing evidence-based learning strategies
    """

    def __init__(self):
        self.knowledge_graph = {}  # concept_id -> KnowledgeNode
        self.study_sessions = []
        self.user_profile = {
            'learning_style': 'visual',  # visual, auditory, kinesthetic, reading
            'attention_span': 45,  # minutes
            'preferred_subjects': [],
            'weak_areas': [],
            'strong_areas': [],
            'optimal_study_time': 'morning',  # morning, afternoon, evening
            'motivation_level': 5,  # 1-10
        }
        self.performance_history = defaultdict(list)
        self.adaptive_difficulty = {
            'current_level': 'intermediate',
            'success_streak': 0,
            'failure_streak': 0,
            'last_adjustment': datetime.now()
        }

    def initialize_knowledge_graph(self):
        """Initialize the MBE knowledge graph with all concepts"""
        concepts = {
            # Contracts
            'contracts_formation': KnowledgeNode('contracts_formation', 'Contract Formation', 'contracts', 2),
            'contracts_offer_acceptance': KnowledgeNode('contracts_offer_acceptance', 'Offer & Acceptance', 'contracts', 3),
            'contracts_consideration': KnowledgeNode('contracts_consideration', 'Consideration', 'contracts', 2),
            'contracts_performance': KnowledgeNode('contracts_performance', 'Performance & Breach', 'contracts', 3),
            'contracts_remedies': KnowledgeNode('contracts_remedies', 'Remedies & Damages', 'contracts', 4),

            # Torts
            'torts_negligence': KnowledgeNode('torts_negligence', 'Negligence', 'torts', 3),
            'torts_intentional': KnowledgeNode('torts_intentional', 'Intentional Torts', 'torts', 2),
            'torts_strict_liability': KnowledgeNode('torts_strict_liability', 'Strict Liability', 'torts', 3),
            'torts_defamation': KnowledgeNode('torts_defamation', 'Defamation & Privacy', 'torts', 4),

            # Constitutional Law
            'conlaw_due_process': KnowledgeNode('conlaw_due_process', 'Due Process', 'conlaw', 4),
            'conlaw_equal_protection': KnowledgeNode('conlaw_equal_protection', 'Equal Protection', 'conlaw', 4),
            'conlaw_first_amendment': KnowledgeNode('conlaw_first_amendment', 'First Amendment', 'conlaw', 5),

            # Criminal Law
            'crim_mens_rea': KnowledgeNode('crim_mens_rea', 'Mens Rea', 'crim', 3),
            'crim_homicide': KnowledgeNode('crim_homicide', 'Homicide', 'crim', 4),
            'crim_parties': KnowledgeNode('crim_parties', 'Parties to Crime', 'crim', 4),

            # Evidence
            'evidence_relevance': KnowledgeNode('evidence_relevance', 'Relevance', 'evidence', 2),
            'evidence_hearsay': KnowledgeNode('evidence_hearsay', 'Hearsay', 'evidence', 5),
            'evidence_character': KnowledgeNode('evidence_character', 'Character Evidence', 'evidence', 3),

            # Civil Procedure
            'civpro_jurisdiction': KnowledgeNode('civpro_jurisdiction', 'Jurisdiction', 'civpro', 4),
            'civpro_pleadings': KnowledgeNode('civpro_pleadings', 'Pleadings', 'civpro', 3),
            'civpro_discovery': KnowledgeNode('civpro_discovery', 'Discovery', 'civpro', 4),
        }

        # Add prerequisites and relationships
        concepts['contracts_offer_acceptance'].prerequisites = ['contracts_formation']
        concepts['contracts_performance'].prerequisites = ['contracts_formation', 'contracts_offer_acceptance']
        concepts['contracts_remedies'].prerequisites = ['contracts_performance']

        self.knowledge_graph = concepts

        # Validate knowledge graph integrity
        self._validate_knowledge_graph()

    def _validate_knowledge_graph(self):
        """
        Validate knowledge graph integrity - catch typos and broken prerequisites
        """
        errors = []

        # Check that all prerequisite IDs exist
        for concept_id, concept in self.knowledge_graph.items():
            for prereq_id in concept.prerequisites:
                if prereq_id not in self.knowledge_graph:
                    errors.append(f"Broken prerequisite: {concept_id} requires non-existent {prereq_id}")

        # Check for circular dependencies (basic check)
        visited = set()
        for concept_id in self.knowledge_graph:
            if self._has_circular_dependency(concept_id, visited, set()):
                errors.append(f"Circular dependency detected involving {concept_id}")

        if errors:
            print("⚠️ Knowledge Graph Validation Errors:")
            for error in errors:
                print(f"  • {error}")
        else:
            print("✅ Knowledge graph validation passed")

    def _has_circular_dependency(self, concept_id, visited, current_path):
        """Check for circular dependencies using DFS"""
        if concept_id in current_path:
            return True
        if concept_id in visited:
            return False

        current_path.add(concept_id)
        for prereq_id in self.knowledge_graph[concept_id].prerequisites:
            if prereq_id in self.knowledge_graph and self._has_circular_dependency(prereq_id, visited, current_path):
                return True

        current_path.remove(concept_id)
        visited.add(concept_id)
        return False

    def adaptive_difficulty_algorithm(self, performance_history: List[Dict]) -> str:
        """
        Adaptive difficulty adjustment based on performance patterns
        Uses Bayesian Knowledge Tracing and Elo rating system concepts
        """
        if not performance_history:
            return 'intermediate'

        recent_performance = performance_history[-10:]  # Last 10 questions
        
        # Handle both 'correct' and 'accuracy' keys, default to True if missing
        accuracy = sum(1 for p in recent_performance if p.get('correct', p.get('accuracy', True))) / len(recent_performance)

        # Adjust difficulty based on accuracy and streak
        if accuracy >= 0.85 and self.adaptive_difficulty['success_streak'] >= 3:
            self.adaptive_difficulty['success_streak'] += 1
            if self.adaptive_difficulty['current_level'] != 'expert':
                self.adaptive_difficulty['current_level'] = 'advanced'
        elif accuracy >= 0.70:
            self.adaptive_difficulty['success_streak'] += 1
        elif accuracy < 0.50:
            self.adaptive_difficulty['failure_streak'] += 1
            if self.adaptive_difficulty['failure_streak'] >= 2:
                if self.adaptive_difficulty['current_level'] != 'foundational':
                    self.adaptive_difficulty['current_level'] = 'intermediate'
        else:
            # Reset streaks for mixed performance
            self.adaptive_difficulty['success_streak'] = 0
            self.adaptive_difficulty['failure_streak'] = 0

        return self.adaptive_difficulty['current_level']

    def spaced_repetition_scheduler(self, concept: KnowledgeNode) -> bool:
        """
        SM-2 spaced repetition algorithm
        Returns True if concept should be reviewed today
        """
        if not concept.last_reviewed:
            return True  # New concept

        days_since_review = (datetime.now() - concept.last_reviewed).days
        return days_since_review >= concept.interval

    def interleaved_practice_generator(self, subject: str, count: int = 10) -> List[Dict]:
        """
        Generate interleaved practice with GUARANTEED unique concepts

        FIXED: No more duplicate concepts in practice sets
        """
        print(f"\n🔄 Generating Interleaved Practice - {subject.upper()}")
        print("=" * 60)

        # Get all concepts for subject
        available_concepts = [
            node for node in self.knowledge_graph.values()
            if node.subject.lower() == subject.lower()
        ]

        if not available_concepts:
            raise ValueError(f"No concepts found for subject: {subject}")

        # CRITICAL FIX: Ensure we don't request more than available
        if count > len(available_concepts):
            print(f"⚠️  Requested {count} questions but only {len(available_concepts)} concepts available")
            count = len(available_concepts)

        # Calculate priority weights for each concept
        concept_weights = []
        for concept in available_concepts:
            # Higher weight for lower mastery
            weight = (1.5 - concept.mastery_level)

            # Higher weight if overdue for review
            if concept.last_reviewed:
                days_since = (datetime.now() - concept.last_reviewed).days
                if days_since > concept.interval:
                    weight *= 2.0

            concept_weights.append((concept, weight))

        # Stratify by difficulty
        easy = [(c, w) for c, w in concept_weights if c.difficulty <= 2]
        medium = [(c, w) for c, w in concept_weights if c.difficulty == 3]
        hard = [(c, w) for c, w in concept_weights if c.difficulty >= 4]

        # Calculate how many from each stratum
        easy_count = max(1, int(count * 0.25))
        medium_count = max(1, int(count * 0.50))
        hard_count = count - easy_count - medium_count

        # Sample WITHOUT replacement (key fix)
        selected = []
        selected.extend(self._weighted_sample_unique(easy, easy_count))
        selected.extend(self._weighted_sample_unique(medium, medium_count))
        selected.extend(self._weighted_sample_unique(hard, hard_count))

        # Take exactly count
        selected = selected[:count]

        # Shuffle to prevent difficulty clustering
        random.shuffle(selected)

        # Display results
        print(f"\nSelected {len(selected)} UNIQUE concepts for practice:")
        for concept in selected:
            icon = '🆕' if concept.mastery_level < 0.3 else '📈' if concept.mastery_level < 0.7 else '✅'
            print(f"   {icon} {concept.name} (Mastery: {concept.mastery_level*100:.0f}%, Difficulty: {concept.difficulty}/5)")

        # Show difficulty distribution
        dist = {'easy': 0, 'medium': 0, 'hard': 0}
        for c in selected:
            if c.difficulty <= 2:
                dist['easy'] += 1
            elif c.difficulty == 3:
                dist['medium'] += 1
            else:
                dist['hard'] += 1

        print(f"\n📊 Difficulty Distribution: Easy({dist['easy']}) | Medium({dist['medium']}) | Hard({dist['hard']})")

        return selected

    def _weighted_sample_unique(self, weighted_concepts: List[Tuple], n: int) -> List:
        """
        Sample concepts with weights, WITHOUT replacement

        This ensures no duplicates
        """
        if not weighted_concepts:
            return []

        if n >= len(weighted_concepts):
            # Return all concepts if we need more than available
            return [concept for concept, weight in weighted_concepts]

        selected = []
        remaining = list(weighted_concepts)

        for _ in range(n):
            if not remaining:
                break

            # Calculate total weight of remaining concepts
            total_weight = sum(weight for _, weight in remaining)

            # Weighted random selection
            rand = random.uniform(0, total_weight)
            cumulative = 0

            for i, (concept, weight) in enumerate(remaining):
                cumulative += weight
                if rand <= cumulative:
                    selected.append(concept)
                    # CRITICAL: Remove from remaining to prevent duplicates
                    remaining.pop(i)
                    break

        return selected

    def elaborative_interrogation_engine(self, question: Dict, user_answer: str, is_correct: bool) -> Dict:
        """
        Implement elaborative interrogation - force deeper thinking about why/how rules work
        Based on research showing this significantly improves retention and understanding
        """
        subject = question.get('subject', 'general')

        # Base interrogation prompts that force causal reasoning
        base_prompts = {
            'why': "WHY does this legal rule exist? What policy rationale supports it?",
            'how': "HOW does this principle interact with related concepts in this subject?",
            'when': "WHEN would the result differ? What exceptions or distinctions apply?",
            'what_if': "WHAT IF the facts were slightly different? How would that change the analysis?"
        }

        # Subject-specific elaborative questions
        subject_specific = {
            'contracts': {
                'why': "Why does contract law require consideration, offer, and acceptance?",
                'how': "How does this contract principle relate to remedies available if breached?",
                'when': "When might a court imply terms or find a contract despite missing elements?",
                'what_if': "What if parties partially performed - does that change enforceability?"
            },
            'torts': {
                'why': "Why does tort law balance individual rights with reasonable behavior expectations?",
                'how': "How does this tort concept relate to available defenses and damages?",
                'when': "When might strict liability apply instead of negligence analysis?",
                'what_if': "What if multiple defendants contributed - how does causation work?"
            },
            'constitutional_law': {
                'why': "Why does this constitutional protection exist and what rights does it safeguard?",
                'how': "How does this constitutional principle interact with government powers?",
                'when': "When would courts apply strict scrutiny vs. rational basis review?",
                'what_if': "What if this were a state vs. federal government action?"
            }
        }

        # Get subject-specific prompts or fall back to general
        prompts = subject_specific.get(subject, base_prompts)

        # Generate follow-up questions based on correctness and answer type
        follow_ups = []

        if is_correct:
            # Even correct answers benefit from deeper analysis
            follow_ups = [
                prompts['why'],
                prompts['how'],
                "Can you think of a real-world example where this principle applies?",
                "How might this rule be tested on the bar exam?"
            ]
        else:
            # Incorrect answers get diagnostic follow-ups
            error_type = self._categorize_error(question, user_answer)
            follow_ups = [
                f"Let's diagnose: {error_type['analysis']}",
                "What rule did you think applied here?",
                prompts['when'],  # When would this be different?
                "How would you approach this differently next time?"
            ]

        return {
            'interrogation_prompts': follow_ups,
            'subject_specific': subject in subject_specific,
            'cognitive_level': 'deep_processing' if is_correct else 'error_correction'
        }

    def _categorize_error(self, question: Dict, wrong_answer: str) -> Dict:
        """
        Categorize the type of error for targeted remediation
        Type A: Issue-spotting failure
        Type B: Rule-application error
        Type C: Distractor susceptibility
        """
        correct_answer = question.get('answer', '')
        options = question.get('options', {})

        # Simple heuristic for error categorization
        if wrong_answer in ['A', 'B', 'C', 'D']:
            wrong_text = options.get(wrong_answer, '').lower()
            correct_text = options.get(correct_answer, '').lower()

            # Type A: Completely missed the issue
            if any(word in wrong_text for word in ['irrelevant', 'unrelated', 'none']):
                return {
                    'type': 'A',
                    'analysis': 'Issue-spotting failure: You may have missed identifying the correct legal issue'
                }

            # Type B: Applied wrong rule to right issue
            elif any(word in correct_text for word in ['breach', 'negligence', 'consideration']) and wrong_answer != correct_answer:
                return {
                    'type': 'B',
                    'analysis': 'Rule-application error: You identified the issue but applied the wrong legal rule'
                }

            # Type C: Fell for distractor
            else:
                return {
                    'type': 'C',
                    'analysis': 'Distractor susceptibility: You knew the rule but were tempted by a common wrong answer'
                }

        return {
            'type': 'unknown',
            'analysis': 'Error type unclear - let\'s analyze the reasoning step by step'
        }

    def confidence_calibration_tracker(self, question: Dict, user_answer: str, confidence_rating: int, is_correct: bool) -> Dict:
        """
        Track confidence-accuracy calibration to develop metacognitive awareness
        Bar students need accurate self-assessment to avoid overconfidence traps
        """
        if not hasattr(self, 'calibration_history'):
            self.calibration_history = []

        # Store calibration data point
        calibration_point = {
            'timestamp': datetime.now(),
            'subject': question.get('subject', 'unknown'),
            'confidence': confidence_rating,  # 1-5 scale
            'correct': is_correct,
            'question_id': question.get('id', 'unknown'),
            'answer': user_answer
        }

        self.calibration_history.append(calibration_point)

        # Analyze recent calibration (last 20 questions)
        recent = self.calibration_history[-20:] if len(self.calibration_history) >= 5 else self.calibration_history

        if len(recent) >= 5:
            # Calculate calibration metrics
            high_confidence = [p for p in recent if p['confidence'] >= 4]
            high_conf_correct = sum(1 for p in high_confidence if p['correct']) / len(high_confidence) if high_confidence else 0

            low_confidence = [p for p in recent if p['confidence'] <= 2]
            low_conf_correct = sum(1 for p in low_confidence if p['correct']) / len(low_confidence) if low_confidence else 0

            overall_accuracy = sum(1 for p in recent if p['correct']) / len(recent)

            # Generate calibration feedback
            feedback = self._generate_calibration_feedback(
                high_conf_correct, low_conf_correct, overall_accuracy, confidence_rating, is_correct
            )

            return {
                'calibration_feedback': feedback,
                'current_metrics': {
                    'high_confidence_accuracy': high_conf_correct,
                    'low_confidence_accuracy': low_conf_correct,
                    'overall_accuracy': overall_accuracy,
                    'calibration_score': self._calculate_calibration_score(recent)
                },
                'needs_calibration': self._detect_calibration_issues(recent)
            }

        return {
            'calibration_feedback': "Keep tracking confidence ratings - need more data for calibration analysis",
            'current_metrics': None,
            'needs_calibration': False
        }

    def _generate_calibration_feedback(self, high_conf_acc, low_conf_acc, overall_acc, confidence, is_correct):
        """Generate personalized calibration feedback"""
        feedback_parts = []

        # Overconfidence detection
        if confidence >= 4 and not is_correct:
            feedback_parts.append("⚠️ **CALIBRATION ALERT**: You were very confident but incorrect. This suggests a conceptual blind spot.")

        # Underconfidence detection
        if confidence <= 2 and is_correct:
            feedback_parts.append("📈 **Confidence Boost**: You were unsure but correct! You're likely underestimating your knowledge.")

        # General calibration assessment
        if high_conf_acc < 0.8 and len(self.calibration_history) >= 10:
            feedback_parts.append("🎯 **Calibration Tip**: When you're very confident, you're right less than 80% of the time. Consider double-checking high-confidence answers.")

        if abs(high_conf_acc - low_conf_acc) > 0.3:
            feedback_parts.append("📊 **Calibration Gap**: Big difference between high/low confidence accuracy suggests inconsistent self-assessment.")

        # Positive reinforcement
        if high_conf_acc >= 0.9 and overall_acc >= 0.7:
            feedback_parts.append("✅ **Well Calibrated**: Your confidence ratings are well-aligned with actual performance!")

        return " ".join(feedback_parts) if feedback_parts else "Keep practicing with confidence ratings to improve self-assessment!"

    def _calculate_calibration_score(self, recent_points):
        """Calculate overall calibration score (0-1, higher is better)"""
        if not recent_points:
            return 0.5

        # Perfect calibration would mean confidence correlates perfectly with accuracy
        # This is a simplified metric
        confidence_levels = [p['confidence'] for p in recent_points]
        accuracies = [1 if p['correct'] else 0 for p in recent_points]

        # Calculate correlation-like metric
        try:
            conf_mean = mean(confidence_levels)
            acc_mean = mean(accuracies)

            # Simple correlation approximation
            numerator = sum((c - conf_mean) * (a - acc_mean) for c, a in zip(confidence_levels, accuracies))
            denominator = (stdev(confidence_levels) * stdev(accuracies)) if stdev(confidence_levels) > 0 and stdev(accuracies) > 0 else 1

            correlation = numerator / (len(recent_points) * denominator) if denominator != 0 else 0

            # Convert to 0-1 scale (correlation can be -1 to 1)
            calibration_score = (correlation + 1) / 2

            return max(0, min(1, calibration_score))  # Clamp to 0-1

        except:
            return 0.5  # Default neutral score

    def _detect_calibration_issues(self, recent_points):
        """Detect if student has calibration problems needing intervention"""
        if len(recent_points) < 10:
            return False

        high_conf = [p for p in recent_points if p['confidence'] >= 4]
        if len(high_conf) >= 3:
            high_conf_acc = sum(1 for p in high_conf if p['correct']) / len(high_conf)
            if high_conf_acc < 0.7:  # Less than 70% accuracy on high confidence answers
                return True

        return False

    def socratic_dialogue_engine(self, question: Dict, user_answer: str) -> Dict:
        """
        Implement Socratic dialogue for wrong answers
        Guides student through reasoning process
        """
        correct_answer = question.get('answer', 'A')
        explanation = question.get('why_correct', f'The correct answer is {correct_answer} because it properly applies the legal rule to these facts.')

        dialogue_steps = [
            {
                'question': f"Why did you choose answer {user_answer}?",
                'follow_up': "What rule or principle led you to that choice?"
            },
            {
                'question': f"What would be the consequence if {user_answer} were correct?",
                'follow_up': "Does that consequence make sense in this fact pattern?"
            },
            {
                'question': f"Let's look at the correct answer {correct_answer}. What rule supports this?",
                'follow_up': "How does this rule apply to these specific facts?"
            },
            {
                'question': "What key distinction are you missing here?",
                'follow_up': "How can you remember this distinction for next time?"
            }
        ]

        tested_rule = question.get('tested_rule', 'the applicable legal rule')
        subject = question.get('subject', 'general')
        subtype = question.get('subtype', 'general')

        return {
            'dialogue_steps': dialogue_steps,
            'key_insight': f"The critical issue is: {tested_rule}",
            'remediation_strategy': self.generate_remediation_strategy(subject, subtype)
        }

    def generate_remediation_strategy(self, subject: str, topic: str) -> Dict:
        """Generate personalized remediation strategies"""
        strategies = {
            'contracts': {
                'formation': ['Review UCC §2-205 firm offers', 'Practice battle of the forms scenarios'],
                'remedies': ['Compare expectation vs reliance vs restitution', 'Calculate damages in hypotheticals'],
            },
            'torts': {
                'negligence': ['Map duty → breach → causation → damages', 'Practice proximate cause distinctions'],
                'defamation': ['Distinguish defamation vs opinion vs privilege', 'Analyze public vs private figures'],
            },
            'constitutional_law': {
                'equal_protection': ['Apply tiered scrutiny framework', 'Practice suspect vs quasi-suspect classifications'],
                'due_process': ['Distinguish procedural vs substantive', 'Analyze fundamental rights triggers'],
            }
        }

        return strategies.get(subject, {}).get(topic, ['Review subject outline', 'Practice 10 similar questions'])

    def concept_mapping_visualizer(self, subject: str) -> Dict:
        """
        Generate visual concept map for a subject
        """
        subject_concepts = [c for c in self.knowledge_graph.values() if c.subject == subject]

        # Create adjacency matrix for concept relationships
        concept_names = [c.name for c in subject_concepts]
        relationships = {}

        for concept in subject_concepts:
            relationships[concept.name] = {
                'prerequisites': [self.knowledge_graph[pid].name for pid in concept.prerequisites if pid in self.knowledge_graph],
                'related': [self.knowledge_graph[rid].name for rid in concept.related_concepts if rid in self.knowledge_graph],
                'difficulty': concept.difficulty,
                'mastery': concept.mastery_level
            }

        return {
            'subject': subject,
            'concepts': concept_names,
            'relationships': relationships,
            'visualization_type': 'network_graph',
            'ascii_art': self.generate_concept_map_ascii(subject_concepts, relationships)
        }

    def generate_concept_map_ascii(self, concepts: List[KnowledgeNode], relationships: Dict) -> str:
        """Generate ASCII art concept map"""
        lines = []
        lines.append(f"📚 {concepts[0].subject.upper()} CONCEPT MAP")
        lines.append("=" * 50)

        for concept in concepts:
            mastery_indicator = "🟢" if concept.mastery_level > 0.7 else "🟡" if concept.mastery_level > 0.4 else "🔴"
            lines.append(f"{mastery_indicator} {concept.name} (Difficulty: {concept.difficulty})")

            if concept.prerequisites:
                lines.append(f"  └── Prerequisites: {', '.join(relationships[concept.name]['prerequisites'])}")

            if concept.related_concepts:
                lines.append(f"  └── Related: {', '.join(relationships[concept.name]['related'])}")

            lines.append("")

        return "\n".join(lines)

    def generate_personalized_study_plan(self, user_performance: Dict) -> Dict:
        """
        Generate comprehensive study plan using all pedagogical techniques
        """
        weak_subjects = user_performance.get('weak_subjects', [])
        time_available = user_performance.get('study_hours_per_week', 20)
        exam_date = user_performance.get('exam_date', datetime.now() + timedelta(days=90))

        weeks_until_exam = max(1, (exam_date - datetime.now()).days // 7)

        plan = {
            'total_weeks': weeks_until_exam,
            'focus_subjects': weak_subjects,
            'daily_structure': {
                'morning_session': {
                    'duration': 90,  # minutes
                    'mode': LearningMode.SPACED_REPETITION,
                    'strategy': CognitiveStrategy.SPACING
                },
                'afternoon_session': {
                    'duration': 90,
                    'mode': LearningMode.INTERLEAVED_PRACTICE,
                    'strategy': CognitiveStrategy.INTERLEAVING
                },
                'evening_session': {
                    'duration': 60,
                    'mode': LearningMode.CONCEPT_MAPPING,
                    'strategy': CognitiveStrategy.DUAL_CODING
                }
            },
            'weekly_milestones': self.generate_weekly_milestones(weak_subjects, weeks_until_exam),
            'adaptive_goals': self.generate_adaptive_goals(user_performance),
            'cognitive_strategies_schedule': self.schedule_cognitive_strategies(weeks_until_exam)
        }

        return plan

    def generate_weekly_milestones(self, weak_subjects: List[str], weeks: int) -> List[Dict]:
        """Generate progressive weekly milestones"""
        milestones = []

        for week in range(1, weeks + 1):
            milestone = {
                'week': week,
                'focus': weak_subjects[week % len(weak_subjects)] if weak_subjects else 'mixed_review',
                'questions_target': 50 + (week * 10),  # Progressive increase
                'accuracy_target': min(70 + (week * 2), 90),  # Progressive accuracy
                'techniques': self.get_week_techniques(week)
            }
            milestones.append(milestone)

        return milestones

    def get_week_techniques(self, week: int) -> List[str]:
        """Get recommended techniques for each week"""
        techniques_by_week = {
            1: ['Focused Practice', 'Self-Explanation'],
            2: ['Interleaved Practice', 'Dual Coding'],
            3: ['Retrieval Practice', 'Concept Mapping'],
            4: ['Spaced Repetition', 'Elaboration'],
            5: ['Diagnostic Assessment', 'Socratic Dialogue'],
            6: ['Adaptive Difficulty', 'Generation'],
        }

        return techniques_by_week.get(week % 6 + 1, ['Mixed Techniques'])

    def generate_adaptive_goals(self, performance: Dict) -> Dict:
        """Generate adaptive goals based on current performance"""
        current_accuracy = performance.get('overall_accuracy', 0.65)
        current_speed = performance.get('avg_time_per_question', 120)  # seconds

        goals = {
            'accuracy_target': min(current_accuracy + 0.05, 0.85),
            'speed_target': max(current_speed - 5, 90),  # seconds
            'weak_subject_improvement': '15% accuracy increase',
            'consistency_target': 'Maintain 70%+ accuracy across all subjects'
        }

        return goals

    def schedule_cognitive_strategies(self, weeks: int) -> Dict:
        """Schedule cognitive strategies throughout study period"""
        schedule = {}

        for week in range(1, weeks + 1):
            week_strategies = []

            # Alternate strategies each week
            if week % 4 == 1:
                week_strategies.extend([CognitiveStrategy.SPACING, CognitiveStrategy.TESTING])
            elif week % 4 == 2:
                week_strategies.extend([CognitiveStrategy.INTERLEAVING, CognitiveStrategy.ELABORATION])
            elif week % 4 == 3:
                week_strategies.extend([CognitiveStrategy.DUAL_CODING, CognitiveStrategy.SELF_EXPLANATION])
            else:
                week_strategies.extend([CognitiveStrategy.GENERATION, CognitiveStrategy.SPACING])

            schedule[f'week_{week}'] = week_strategies

        return schedule

    def meta_cognition_reflection(self, session: StudySession) -> Dict:
        """
        Generate meta-cognition reflection prompts
        """
        reflection_questions = [
            "What learning strategies worked well today?",
            "What concepts are still confusing?",
            "How confident do you feel about today's material?",
            "What could you do differently tomorrow?",
            "Are you spacing out your study sessions effectively?",
            "How well are you interleaving different subjects?"
        ]

        insights = {
            'session_quality_score': self.calculate_session_quality(session),
            'recommended_adjustments': self.generate_session_adjustments(session),
            'reflection_questions': reflection_questions,
            'progress_toward_goals': self.assess_goal_progress(session)
        }

        return insights

    def calculate_session_quality(self, session: StudySession) -> float:
        """Calculate session quality score (0-1)"""
        # Handle empty sessions gracefully
        if session.questions_attempted == 0:
            return 0.5  # Neutral score for empty sessions
        
        factors = {
            'accuracy': session.questions_correct / max(session.questions_attempted, 1),
            'time_efficiency': min(session.time_spent / max((session.questions_attempted * 90), 1), 1),  # 90 sec target
            'strategies_used': min(len(session.cognitive_strategies_used) / 3, 1),  # Normalize to 3 strategies
            'confidence': sum(session.confidence_ratings) / max(len(session.confidence_ratings), 1) / 5 if session.confidence_ratings else 0.5
        }

        # Weighted average
        weights = {'accuracy': 0.4, 'time_efficiency': 0.2, 'strategies_used': 0.2, 'confidence': 0.2}
        quality_score = sum(factors[key] * weights[key] for key in factors)

        return min(quality_score, 1.0)

    def generate_session_adjustments(self, session: StudySession) -> List[str]:
        """Generate specific adjustments based on session performance"""
        adjustments = []

        accuracy = session.questions_correct / max(session.questions_attempted, 1)

        if accuracy < 0.6:
            adjustments.append("Focus on foundational concepts before advanced topics")
        elif accuracy > 0.85:
            adjustments.append("Increase difficulty or move to interleaved practice")

        avg_time = session.time_spent / max(session.questions_attempted, 1)
        if avg_time > 120:
            adjustments.append("Work on time management - aim for 90-108 seconds per question")
        elif avg_time < 60:
            adjustments.append("Slow down and focus on deep understanding, not speed")

        if len(session.cognitive_strategies_used) < 2:
            adjustments.append("Incorporate more cognitive strategies (dual coding, self-explanation)")

        return adjustments if adjustments else ["Continue current approach - you're performing well!"]

    def assess_goal_progress(self, session: StudySession) -> Dict:
        """Assess progress toward long-term goals"""
        # This would integrate with long-term performance tracking
        return {
            'weekly_accuracy_trend': 'improving',
            'subjects_mastered': [],
            'subjects_needing_work': [],
            'overall_progress': 0.65  # percentage to goal
        }
