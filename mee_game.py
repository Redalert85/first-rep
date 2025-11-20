import argparse
import json
import random
from collections import defaultdict
from dataclasses import dataclass
from statistics import mean
from typing import Dict, List, Optional, Tuple

FREQUENCY_WEIGHTS: Dict[str, float] = {
    "very_high": 1.2,
    "high": 1.1,
    "medium": 1.0,
    "low": 0.9,
    "rare": 0.8,
}


@dataclass
class ConceptCard:
    concept_id: str
    name: str
    subject: str
    difficulty: int
    rule_statement: str
    elements: List[str]
    exceptions: List[str]
    common_traps: List[str]
    mnemonic: Optional[str]
    exam_frequency: str

    @classmethod
    def from_dict(cls, data: Dict[str, object]) -> "ConceptCard":
        return cls(
            concept_id=str(data.get("concept_id", "")),
            name=str(data.get("name", "")),
            subject=str(data.get("subject", "")),
            difficulty=int(data.get("difficulty", 3)),
            rule_statement=str(data.get("rule_statement", "")),
            elements=list(data.get("elements", []) or []),
            exceptions=list(data.get("exceptions", []) or []),
            common_traps=list(data.get("common_traps", []) or []),
            mnemonic=data.get("mnemonic"),
            exam_frequency=str(data.get("exam_frequency", "medium")),
        )


@dataclass
class SubjectProfile:
    subject: str
    avg_difficulty: float
    difficulty_score: float
    frequency_weight: float
    concept_count: int


class MEEGame:
    def __init__(self, data_path: str, rounds: int = 5, seed: Optional[int] = None):
        self.data_path = data_path
        self.rounds = rounds
        self.rng = random.Random(seed)
        self.concepts = self._load_concepts()
        self.subject_profiles = self._rank_subjects()
        self.target_subjects = {p.subject for p in self.subject_profiles[:2]}
        self.question_pool = [c for c in self.concepts if c.subject in self.target_subjects]

    def _load_concepts(self) -> List[ConceptCard]:
        with open(self.data_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
        return [ConceptCard.from_dict(item) for item in raw_data]

    def _rank_subjects(self) -> List[SubjectProfile]:
        subject_map: Dict[str, List[ConceptCard]] = defaultdict(list)
        for concept in self.concepts:
            subject_map[concept.subject].append(concept)

        profiles: List[SubjectProfile] = []
        for subject, cards in subject_map.items():
            avg_difficulty = mean(card.difficulty for card in cards)
            freq_weight = mean(
                FREQUENCY_WEIGHTS.get(card.exam_frequency, FREQUENCY_WEIGHTS["medium"])
                for card in cards
            )
            heavy_hitter_bonus = sum(0.05 for card in cards if card.difficulty >= 4)
            difficulty_score = round(avg_difficulty * freq_weight + heavy_hitter_bonus, 2)
            profiles.append(
                SubjectProfile(
                    subject=subject,
                    avg_difficulty=round(avg_difficulty, 2),
                    difficulty_score=difficulty_score,
                    frequency_weight=round(freq_weight, 2),
                    concept_count=len(cards),
                )
            )

        return sorted(profiles, key=lambda p: p.difficulty_score, reverse=True)

    def _choose_card(self) -> ConceptCard:
        weights = [card.difficulty for card in self.question_pool]
        return self.rng.choices(self.question_pool, weights=weights, k=1)[0]

    def _build_prompt(self, card: ConceptCard) -> Tuple[str, List[str]]:
        prompt_builders = []
        if card.rule_statement:
            prompt_builders.append(
                (
                    f"{card.name}: Explain the rule statement in your own words.",
                    [card.rule_statement],
                )
            )
        if card.elements:
            prompt_builders.append(
                (
                    f"{card.name}: List the key elements.",
                    [" • " + element for element in card.elements],
                )
            )
        if card.common_traps:
            prompt_builders.append(
                (
                    f"{card.name}: What are the common traps or mistakes to avoid?",
                    [" ⚠️ " + trap for trap in card.common_traps],
                )
            )
        if card.exceptions:
            prompt_builders.append(
                (
                    f"{card.name}: Walk through the major exceptions.",
                    [" ✱ " + exc for exc in card.exceptions],
                )
            )
        if card.mnemonic:
            prompt_builders.append(
                (
                    f"{card.name}: Recall the mnemonic that helps you remember this concept.",
                    [card.mnemonic],
                )
            )

        if not prompt_builders:
            return (
                f"{card.name}: Summarize the doctrine and give one exam tip.",
                [card.rule_statement or "Use the facts to build a clean IRAC."],
            )

        return self.rng.choice(prompt_builders)

    def _print_subject_dashboard(self) -> None:
        print("\n🎯 Targeting the two hardest MEE subjects based on difficulty and frequency:\n")
        for profile in self.subject_profiles[:2]:
            print(
                f" • {profile.subject} | Difficulty Score: {profile.difficulty_score}"
                f" | Avg Diff: {profile.avg_difficulty} | Coverage: {profile.concept_count} concepts"
            )
        print("\nReady? We'll alternate between these subjects so the difficulty stays high!\n")

    def play(self) -> None:
        if not self.question_pool:
            print("No concepts available to run the game.")
            return

        self._print_subject_dashboard()
        score = 0
        for round_number in range(1, self.rounds + 1):
            card = self._choose_card()
            prompt, answers = self._build_prompt(card)

            print(f"Round {round_number}/{self.rounds} — Subject: {card.subject} — Concept: {card.name}")
            print(prompt)
            input("Your turn: ")
            print("\n📘 Reference Answer:")
            for line in answers:
                print(line)

            reflection = input("Did you nail it? (y/n): ").strip().lower()
            if reflection.startswith("y"):
                score += 1

            print("Tip: connect this to another doctrine or outline a quick hypo before moving on.\n")

        print(f"Session complete! You self-scored {score} out of {self.rounds} rounds.")
        print("Keep revisiting these two subjects until you can teach them without notes.")

    def preview(self, sample_rounds: int = 2) -> None:
        print("\nPreview mode: Showing the hardest subjects and sample prompts (no input required).\n")
        self._print_subject_dashboard()
        for round_number in range(1, sample_rounds + 1):
            card = self._choose_card()
            prompt, answers = self._build_prompt(card)
            print(f"Sample {round_number}: {prompt}")
            print("Reference:")
            for line in answers:
                print(line)
            print()


def main() -> None:
    parser = argparse.ArgumentParser(description="MEE hardest-subject study game")
    parser.add_argument(
        "--data-path",
        default="essay_subjects.json",
        help="Path to the essay subjects JSON data",
    )
    parser.add_argument("--rounds", type=int, default=5, help="Number of interactive rounds")
    parser.add_argument("--preview", action="store_true", help="Show prompts without user input")
    parser.add_argument("--seed", type=int, default=None, help="Optional RNG seed for reproducibility")
    args = parser.parse_args()

    game = MEEGame(data_path=args.data_path, rounds=args.rounds, seed=args.seed)

    if args.preview:
        game.preview(sample_rounds=args.rounds)
    else:
        game.play()


if __name__ == "__main__":
    main()
