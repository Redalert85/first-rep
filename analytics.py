#!/usr/bin/env python3
"""
Analytics Report Generator for Bar Prep Study Aid
Generates comprehensive performance reports and spaced repetition analytics
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List, Tuple, Any
import sys


class BarPrepAnalytics:
    """Analytics engine for bar prep flashcard system"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.flashcards = []
        self.performance_data = []
        self.knowledge_base = []

        # Load all data sources
        self._load_flashcards()
        self._load_performance()
        self._load_knowledge_base()

    def _load_flashcards(self):
        """Load flashcard data from JSONL file"""
        flashcard_file = self.data_dir / "flashcards_v3.jsonl"

        if not flashcard_file.exists():
            print(f"⚠️  Warning: {flashcard_file} not found. Creating empty dataset.")
            return

        with open(flashcard_file, 'r') as f:
            for line in f:
                if line.strip():
                    try:
                        card = json.loads(line)
                        self.flashcards.append(card)
                    except json.JSONDecodeError as e:
                        print(f"⚠️  Error parsing flashcard: {e}")

    def _load_performance(self):
        """Load performance tracking data"""
        perf_file = self.data_dir / "performance_v3.jsonl"

        if not perf_file.exists():
            print(f"⚠️  Warning: {perf_file} not found.")
            return

        with open(perf_file, 'r') as f:
            for line in f:
                if line.strip():
                    try:
                        data = json.loads(line)
                        self.performance_data.append(data)
                    except json.JSONDecodeError as e:
                        print(f"⚠️  Error parsing performance data: {e}")

    def _load_knowledge_base(self):
        """Load all knowledge base files"""
        kb_files = [
            "ultimate_knowledge_base.json",
            "mbe_full_expansion.json",
            "essay_subjects.json"
        ]

        for kb_file in kb_files:
            kb_path = Path(kb_file)
            if kb_path.exists():
                with open(kb_path, 'r') as f:
                    data = json.load(f)
                    # Handle different JSON structures
                    if isinstance(data, dict):
                        for subject, concepts in data.items():
                            if isinstance(concepts, list):
                                self.knowledge_base.extend(concepts)
                    elif isinstance(data, list):
                        self.knowledge_base.extend(data)

    def generate_overall_performance_report(self) -> Dict[str, Any]:
        """Generate overall performance metrics"""
        now = datetime.now()
        seven_days_ago = now - timedelta(days=7)

        total_cards = len(self.flashcards)

        # Calculate due cards (cards with next review date <= today)
        due_cards = 0
        mastered_cards = 0
        total_confidence = 0.0
        cards_with_confidence = 0
        reviewed_last_7_days = 0

        for card in self.flashcards:
            # Check if card is due
            if 'next_review' in card and card['next_review']:
                try:
                    next_review = datetime.fromisoformat(card['next_review'].replace('Z', '+00:00'))
                    if next_review <= now:
                        due_cards += 1
                except (ValueError, AttributeError):
                    pass

            # Check if mastered (ease_factor > 2.5 and interval > 30 days)
            ease = card.get('ease_factor', 2.5)
            interval = card.get('interval', 1)
            if ease >= 2.5 and interval >= 30:
                mastered_cards += 1

            # Track confidence (using ease_factor as proxy)
            if 'ease_factor' in card:
                total_confidence += card['ease_factor']
                cards_with_confidence += 1

            # Check last reviewed
            if 'last_reviewed' in card and card['last_reviewed']:
                try:
                    last_reviewed = datetime.fromisoformat(card['last_reviewed'].replace('Z', '+00:00'))
                    if last_reviewed >= seven_days_ago:
                        reviewed_last_7_days += 1
                except (ValueError, AttributeError):
                    pass

        # Calculate global accuracy from performance data
        total_attempts = 0
        correct_attempts = 0

        for perf in self.performance_data:
            if 'total_questions' in perf and 'correct_answers' in perf:
                total_attempts += perf['total_questions']
                correct_attempts += perf['correct_answers']

        accuracy = (correct_attempts / total_attempts * 100) if total_attempts > 0 else 0.0
        avg_confidence = (total_confidence / cards_with_confidence) if cards_with_confidence > 0 else 2.5

        return {
            'total_cards': total_cards,
            'due_cards': due_cards,
            'mastered_cards': mastered_cards,
            'accuracy_rate': accuracy,
            'avg_confidence': avg_confidence,
            'reviewed_last_7_days': reviewed_last_7_days,
            'total_attempts': total_attempts,
            'correct_attempts': correct_attempts
        }

    def generate_subject_breakdown(self) -> Dict[str, Any]:
        """Generate subject-specific analytics"""
        subject_stats = defaultdict(lambda: {
            'total_cards': 0,
            'total_attempts': 0,
            'correct_attempts': 0,
            'accuracy': 0.0,
            'avg_ease': 0.0,
            'ease_sum': 0.0
        })

        # Analyze flashcards by subject
        for card in self.flashcards:
            subject = card.get('subject', 'Unknown')
            subject_stats[subject]['total_cards'] += 1

            if 'ease_factor' in card:
                subject_stats[subject]['ease_sum'] += card['ease_factor']

        # Analyze performance by subject
        for perf in self.performance_data:
            subject = perf.get('subject', 'Unknown')
            if 'total_questions' in perf and 'correct_answers' in perf:
                subject_stats[subject]['total_attempts'] += perf['total_questions']
                subject_stats[subject]['correct_attempts'] += perf['correct_answers']

        # Calculate averages and identify weak topics
        weak_topics = []
        mastery_distribution = defaultdict(int)

        for subject, stats in subject_stats.items():
            # Calculate accuracy
            if stats['total_attempts'] > 0:
                stats['accuracy'] = (stats['correct_attempts'] / stats['total_attempts']) * 100
            else:
                stats['accuracy'] = 0.0

            # Calculate average ease
            if stats['total_cards'] > 0:
                stats['avg_ease'] = stats['ease_sum'] / stats['total_cards']
            else:
                stats['avg_ease'] = 2.5

            # Identify weak topics (< 70% accuracy)
            if stats['accuracy'] < 70 and stats['total_attempts'] > 0:
                weak_topics.append((subject, stats['accuracy']))

            # Categorize mastery level
            if stats['avg_ease'] < 2.0:
                mastery_distribution['Struggling'] += 1
            elif stats['avg_ease'] < 2.5:
                mastery_distribution['Learning'] += 1
            elif stats['avg_ease'] < 3.0:
                mastery_distribution['Proficient'] += 1
            else:
                mastery_distribution['Mastered'] += 1

        # Sort weak topics by accuracy (lowest first)
        weak_topics.sort(key=lambda x: x[1])

        return {
            'subject_stats': dict(subject_stats),
            'weak_topics': weak_topics,
            'mastery_distribution': dict(mastery_distribution)
        }

    def generate_spaced_repetition_health(self) -> Dict[str, Any]:
        """Analyze spaced repetition system health"""
        now = datetime.now()

        # Interval buckets
        interval_buckets = {
            '1 day': 0,
            '2-5 days': 0,
            '6-14 days': 0,
            '15-30 days': 0,
            '30+ days': 0
        }

        overdue_cards = 0
        next_7_days_forecast = defaultdict(int)

        for card in self.flashcards:
            # Categorize by interval
            interval = card.get('interval', 1)
            if interval == 1:
                interval_buckets['1 day'] += 1
            elif interval <= 5:
                interval_buckets['2-5 days'] += 1
            elif interval <= 14:
                interval_buckets['6-14 days'] += 1
            elif interval <= 30:
                interval_buckets['15-30 days'] += 1
            else:
                interval_buckets['30+ days'] += 1

            # Check if overdue
            if 'next_review' in card and card['next_review']:
                try:
                    next_review = datetime.fromisoformat(card['next_review'].replace('Z', '+00:00'))
                    if next_review < now:
                        overdue_cards += 1

                    # Forecast next 7 days
                    for day in range(7):
                        check_date = now + timedelta(days=day)
                        if next_review.date() == check_date.date():
                            day_name = check_date.strftime('%A')
                            next_7_days_forecast[day_name] += 1
                except (ValueError, AttributeError):
                    pass

        return {
            'interval_distribution': interval_buckets,
            'overdue_cards': overdue_cards,
            'next_7_days_forecast': dict(next_7_days_forecast)
        }

    def format_report(self) -> str:
        """Generate formatted text report"""
        overall = self.generate_overall_performance_report()
        subjects = self.generate_subject_breakdown()
        sr_health = self.generate_spaced_repetition_health()

        report = []
        report.append("=" * 80)
        report.append("BAR PREP ANALYTICS REPORT")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 80)
        report.append("")

        # Overall Performance
        report.append("📊 OVERALL PERFORMANCE")
        report.append("-" * 80)
        report.append(f"Total Cards:              {overall['total_cards']:,}")
        report.append(f"Due Cards:                {overall['due_cards']:,}")
        report.append(f"Mastered Cards:           {overall['mastered_cards']:,} ({overall['mastered_cards']/overall['total_cards']*100:.1f}%)" if overall['total_cards'] > 0 else "Mastered Cards:           0")
        report.append(f"Global Accuracy Rate:     {overall['accuracy_rate']:.1f}% ({overall['correct_attempts']}/{overall['total_attempts']})")
        report.append(f"Average Confidence Score: {overall['avg_confidence']:.2f} (ease factor)")
        report.append(f"Cards Reviewed (7 days):  {overall['reviewed_last_7_days']:,}")
        report.append("")

        # Subject-Specific Breakdown
        report.append("📚 SUBJECT-SPECIFIC BREAKDOWN")
        report.append("-" * 80)

        subject_stats = subjects['subject_stats']
        if subject_stats:
            # Sort subjects by accuracy (lowest to highest)
            sorted_subjects = sorted(subject_stats.items(),
                                   key=lambda x: x[1]['accuracy'])

            report.append(f"{'Subject':<30} {'Cards':>8} {'Accuracy':>12} {'Avg Ease':>12}")
            report.append("-" * 80)

            for subject, stats in sorted_subjects:
                cards = stats['total_cards']
                accuracy = stats['accuracy']
                avg_ease = stats['avg_ease']

                # Add indicator for weak subjects
                indicator = "⚠️ " if accuracy < 70 and stats['total_attempts'] > 0 else "   "

                report.append(f"{indicator}{subject[:27]:<27} {cards:>8} {accuracy:>11.1f}% {avg_ease:>12.2f}")
        else:
            report.append("No subject data available")

        report.append("")

        # Weak Topics
        report.append("⚠️  WEAK TOPICS (< 70% Accuracy)")
        report.append("-" * 80)

        weak_topics = subjects['weak_topics']
        if weak_topics:
            for subject, accuracy in weak_topics[:10]:  # Top 10 weakest
                report.append(f"  • {subject:<35} {accuracy:.1f}%")
        else:
            report.append("No weak topics identified - great job!")

        report.append("")

        # Mastery Distribution
        report.append("🎯 MASTERY LEVEL DISTRIBUTION")
        report.append("-" * 80)

        mastery = subjects['mastery_distribution']
        total_subjects = sum(mastery.values())

        for level in ['Struggling', 'Learning', 'Proficient', 'Mastered']:
            count = mastery.get(level, 0)
            percentage = (count / total_subjects * 100) if total_subjects > 0 else 0
            bar = "█" * int(percentage / 2)
            report.append(f"{level:<15} {count:>3} subjects  {percentage:>5.1f}% {bar}")

        report.append("")

        # Spaced Repetition Health
        report.append("🔄 SPACED REPETITION HEALTH")
        report.append("-" * 80)

        report.append("Cards by Interval:")
        for interval, count in sr_health['interval_distribution'].items():
            percentage = (count / overall['total_cards'] * 100) if overall['total_cards'] > 0 else 0
            bar = "█" * int(percentage / 2)
            report.append(f"  {interval:<15} {count:>4} cards  {percentage:>5.1f}% {bar}")

        report.append("")
        report.append(f"Overdue Cards: {sr_health['overdue_cards']:,}")

        if sr_health['overdue_cards'] > 0:
            urgency = sr_health['overdue_cards'] / overall['total_cards'] * 100 if overall['total_cards'] > 0 else 0
            if urgency > 20:
                report.append("  ⚠️  HIGH: More than 20% of cards are overdue!")
            elif urgency > 10:
                report.append("  ⚠️  MEDIUM: 10-20% of cards are overdue")
            else:
                report.append("  ✓ Manageable backlog")

        report.append("")
        report.append("📅 NEXT 7 DAYS REVIEW FORECAST")
        report.append("-" * 80)

        forecast = sr_health['next_7_days_forecast']
        if forecast:
            max_cards = max(forecast.values()) if forecast else 1

            # Show forecast for each day
            for day in range(7):
                date = datetime.now() + timedelta(days=day)
                day_name = date.strftime('%A')
                date_str = date.strftime('%Y-%m-%d')
                count = forecast.get(day_name, 0)

                bar_length = int((count / max_cards) * 40) if max_cards > 0 else 0
                bar = "█" * bar_length

                report.append(f"{day_name:<10} ({date_str})  {count:>4} cards  {bar}")
        else:
            report.append("No reviews scheduled for the next 7 days")

        report.append("")
        report.append("=" * 80)
        report.append("END OF REPORT")
        report.append("=" * 80)

        return "\n".join(report)

    def save_report(self, filename: str = "analytics_report.txt"):
        """Save report to file and display to terminal"""
        report = self.format_report()

        # Display to terminal
        print(report)

        # Save to file
        with open(filename, 'w') as f:
            f.write(report)

        print(f"\n✅ Report saved to: {filename}")

        return report


def main():
    """Main entry point"""
    try:
        analytics = BarPrepAnalytics()
        analytics.save_report()
    except Exception as e:
        print(f"❌ Error generating analytics: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
