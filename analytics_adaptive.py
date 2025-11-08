#!/usr/bin/env python3
"""
Adaptive Learning System Analytics
Complete analytics with 5 sections:
1. Overall Performance Report
2. Subject-Specific Breakdown
3. Spaced Repetition Health
4. Constitutional Law & Evidence Deep Dive
5. Study Recommendations
"""

import sys
from datetime import datetime, timedelta
from pathlib import Path

from adaptive_learning_system import (
    AdaptiveLearningSystem,
    AdaptiveLearningDatabase,
    Subject
)


# ==================== COLORS ====================

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def colorize(text: str, color: str) -> str:
    """Add color to text"""
    return f"{color}{text}{Colors.END}"


# ==================== ANALYTICS ====================

def section_header(title: str, output_file=None):
    """Print section header"""
    line = "=" * 80
    header = f"\n{line}\n{title.upper()}\n{line}\n"

    print(colorize(header, Colors.HEADER + Colors.BOLD))

    if output_file:
        output_file.write(header)


def subsection_header(title: str, output_file=None):
    """Print subsection header"""
    line = "-" * 80
    header = f"\n{title}\n{line}\n"

    print(colorize(header, Colors.CYAN + Colors.BOLD))

    if output_file:
        output_file.write(header)


def print_and_log(text: str, output_file=None, color=None):
    """Print to console and log to file"""
    if color:
        print(colorize(text, color))
    else:
        print(text)

    if output_file:
        output_file.write(text + "\n")


def section_1_overall_performance(system: AdaptiveLearningSystem, output_file=None):
    """Section 1: Overall Performance Report"""
    section_header("Section 1: Overall Performance Report", output_file)

    stats = system.get_statistics()

    # Main metrics
    print_and_log(f"Total Cards:          {stats['total_cards']}", output_file, Colors.BOLD)
    print_and_log(f"Cards Due Today:      {stats['cards_due']}", output_file, Colors.YELLOW)
    print_and_log(f"Cards Mastered:       {stats['cards_mastered']}", output_file, Colors.GREEN)
    print_and_log(f"Overall Accuracy:     {stats['overall_accuracy']:.1f}%", output_file, Colors.CYAN)
    print_and_log(f"Average Confidence:   {stats['average_confidence']:.2f}/4", output_file, Colors.CYAN)
    print_and_log(f"Total Reviews:        {stats['total_reviews']}", output_file)

    # Progress metrics
    mastery_percentage = (stats['cards_mastered'] / stats['total_cards'] * 100) if stats['total_cards'] > 0 else 0
    due_percentage = (stats['cards_due'] / stats['total_cards'] * 100) if stats['total_cards'] > 0 else 0

    print_and_log(f"\nMastery Progress:     {mastery_percentage:.1f}%", output_file, Colors.GREEN)
    print_and_log(f"Due Cards:            {due_percentage:.1f}%", output_file, Colors.YELLOW)

    # Progress bar
    mastered_bars = int(mastery_percentage / 2)
    remaining_bars = 50 - mastered_bars
    progress_bar = "█" * mastered_bars + "░" * remaining_bars
    print_and_log(f"\nProgress: [{progress_bar}] {mastery_percentage:.1f}%", output_file, Colors.GREEN)


def section_2_subject_breakdown(system: AdaptiveLearningSystem, output_file=None):
    """Section 2: Subject-Specific Breakdown"""
    section_header("Section 2: Subject-Specific Breakdown", output_file)

    subject_stats = system.get_subject_statistics()

    # Table header
    header = f"{'Subject':<30s} {'Total':>8s} {'Due':>8s} {'Mastered':>10s} {'Accuracy':>10s}"
    print_and_log(header, output_file, Colors.BOLD)
    print_and_log("-" * 80, output_file)

    # Sort by total cards descending
    sorted_subjects = sorted(subject_stats.items(), key=lambda x: x[1]['total'], reverse=True)

    for subject, stats in sorted_subjects:
        mastered_pct = (stats['mastered'] / stats['total'] * 100) if stats['total'] > 0 else 0
        due_count = stats['due']

        row = f"{subject:<30s} {stats['total']:>8d} {due_count:>8d} {stats['mastered']:>10d} {stats['accuracy']:>9.1f}%"

        # Color code based on mastery
        if mastered_pct >= 50:
            print_and_log(row, output_file, Colors.GREEN)
        elif mastered_pct >= 25:
            print_and_log(row, output_file, Colors.CYAN)
        elif mastered_pct >= 10:
            print_and_log(row, output_file, Colors.YELLOW)
        else:
            print_and_log(row, output_file, Colors.RED)

    # Mastery distribution by subject
    subsection_header("Mastery Distribution by Subject", output_file)

    for subject, stats in sorted_subjects:
        total = stats['total']
        mastered = stats['mastered']
        in_progress = total - mastered - stats['due']
        due = stats['due']

        mastered_pct = (mastered / total * 100) if total > 0 else 0
        in_progress_pct = (in_progress / total * 100) if total > 0 else 0
        due_pct = (due / total * 100) if total > 0 else 0

        # Create bar chart
        bar_width = 40
        mastered_bars = int(mastered_pct * bar_width / 100)
        in_progress_bars = int(in_progress_pct * bar_width / 100)
        due_bars = int(due_pct * bar_width / 100)
        remaining_bars = bar_width - mastered_bars - in_progress_bars - due_bars

        bar = "█" * mastered_bars + "▓" * in_progress_bars + "▒" * due_bars + "░" * remaining_bars

        display = f"{subject[:28]:<28s} [{bar}] M:{mastered:3d} P:{in_progress:3d} D:{due:3d}"
        print_and_log(display, output_file)


def section_3_spaced_repetition_health(system: AdaptiveLearningSystem, output_file=None):
    """Section 3: Spaced Repetition Health"""
    section_header("Section 3: Spaced Repetition Health", output_file)

    # Interval distribution
    distribution = system.get_interval_distribution()

    subsection_header("Interval Distribution", output_file)

    intervals = [
        ('New (not reviewed)', 'new'),
        ('1 day', '1_day'),
        ('2-7 days', '2_7_days'),
        ('8-21 days', '8_21_days'),
        ('22-60 days', '22_60_days'),
        ('60+ days', '60+_days')
    ]

    for label, key in intervals:
        count = distribution[key]
        print_and_log(f"{label:<25s}: {count:>5d} cards", output_file, Colors.CYAN)

    # Calculate overdue cards
    all_cards = system.db.get_all_cards()
    now = datetime.now()
    overdue_cards = [c for c in all_cards if c.next_review and c.next_review < now and c.repetitions > 0]

    subsection_header("Overdue Analysis", output_file)
    print_and_log(f"Total Overdue Cards: {len(overdue_cards)}", output_file, Colors.RED if len(overdue_cards) > 0 else Colors.GREEN)

    if overdue_cards:
        # Group by days overdue
        overdue_1_7 = len([c for c in overdue_cards if (now - c.next_review).days <= 7])
        overdue_8_30 = len([c for c in overdue_cards if 8 <= (now - c.next_review).days <= 30])
        overdue_30_plus = len([c for c in overdue_cards if (now - c.next_review).days > 30])

        print_and_log(f"  1-7 days overdue:    {overdue_1_7}", output_file, Colors.YELLOW)
        print_and_log(f"  8-30 days overdue:   {overdue_8_30}", output_file, Colors.YELLOW)
        print_and_log(f"  30+ days overdue:    {overdue_30_plus}", output_file, Colors.RED)

    # 7-day forecast
    subsection_header("7-Day Review Forecast", output_file)

    forecast = system.get_forecast(7)

    print_and_log(f"{'Date':<15s} {'Day':>10s} {'Cards Due':>12s}", output_file, Colors.BOLD)
    print_and_log("-" * 40, output_file)

    for date_str, count in forecast:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        day_name = date_obj.strftime('%A')

        display = f"{date_str:<15s} {day_name:>10s} {count:>12d}"

        if count > 100:
            print_and_log(display, output_file, Colors.RED)
        elif count > 50:
            print_and_log(display, output_file, Colors.YELLOW)
        else:
            print_and_log(display, output_file, Colors.GREEN)


def section_4_topic_deep_dive(system: AdaptiveLearningSystem, output_file=None):
    """Section 4: Constitutional Law & Evidence Deep Dive"""
    section_header("Section 4: Constitutional Law & Evidence Deep Dive", output_file)

    # Constitutional Law
    subsection_header("Constitutional Law - Topic Analysis", output_file)

    con_law_topics = system.get_topic_statistics('constitutional_law')

    if con_law_topics:
        header = f"{'Topic':<40s} {'Total':>8s} {'Due':>8s} {'Mastered':>10s} {'Accuracy':>10s}"
        print_and_log(header, output_file, Colors.BOLD)
        print_and_log("-" * 80, output_file)

        sorted_topics = sorted(con_law_topics.items(), key=lambda x: x[1]['total'], reverse=True)

        for topic, stats in sorted_topics:
            mastered_pct = (stats['mastered'] / stats['total'] * 100) if stats['total'] > 0 else 0

            row = f"{topic:<40s} {stats['total']:>8d} {stats['due']:>8d} {stats['mastered']:>10d} {stats['accuracy']:>9.1f}%"

            if mastered_pct >= 50:
                print_and_log(row, output_file, Colors.GREEN)
            elif mastered_pct >= 25:
                print_and_log(row, output_file, Colors.CYAN)
            else:
                print_and_log(row, output_file, Colors.YELLOW)
    else:
        print_and_log("No Constitutional Law topics found", output_file, Colors.YELLOW)

    # Evidence
    subsection_header("Evidence - Topic Analysis", output_file)

    evidence_topics = system.get_topic_statistics('evidence')

    if evidence_topics:
        header = f"{'Topic':<40s} {'Total':>8s} {'Due':>8s} {'Mastered':>10s} {'Accuracy':>10s}"
        print_and_log(header, output_file, Colors.BOLD)
        print_and_log("-" * 80, output_file)

        sorted_topics = sorted(evidence_topics.items(), key=lambda x: x[1]['total'], reverse=True)

        for topic, stats in sorted_topics:
            mastered_pct = (stats['mastered'] / stats['total'] * 100) if stats['total'] > 0 else 0

            row = f"{topic:<40s} {stats['total']:>8d} {stats['due']:>8d} {stats['mastered']:>10d} {stats['accuracy']:>9.1f}%"

            if mastered_pct >= 50:
                print_and_log(row, output_file, Colors.GREEN)
            elif mastered_pct >= 25:
                print_and_log(row, output_file, Colors.CYAN)
            else:
                print_and_log(row, output_file, Colors.YELLOW)
    else:
        print_and_log("No Evidence topics found", output_file, Colors.YELLOW)


def section_5_study_recommendations(system: AdaptiveLearningSystem, output_file=None):
    """Section 5: Study Recommendations"""
    section_header("Section 5: Study Recommendations", output_file)

    stats = system.get_statistics()
    subject_stats = system.get_subject_statistics()

    # Daily study targets
    subsection_header("Daily Study Targets", output_file)

    cards_due = stats['cards_due']
    cards_remaining = stats['total_cards'] - stats['cards_mastered']

    print_and_log(f"Cards Due Today:      {cards_due}", output_file, Colors.YELLOW)
    print_and_log(f"Cards Not Mastered:   {cards_remaining}", output_file, Colors.CYAN)

    # Calculate study timeline
    daily_target_options = [20, 30, 50, 75, 100]

    subsection_header("Study Timeline Projections", output_file)

    print_and_log(f"{'Daily Target':<20s} {'Days to Master':>20s} {'Calendar Date':>20s}", output_file, Colors.BOLD)
    print_and_log("-" * 65, output_file)

    for target in daily_target_options:
        days_needed = cards_remaining / target if target > 0 else 0
        completion_date = datetime.now() + timedelta(days=int(days_needed))

        display = f"{target:>3d} cards/day      {int(days_needed):>20d} days    {completion_date.strftime('%Y-%m-%d'):>20s}"
        print_and_log(display, output_file, Colors.CYAN)

    # Priority subjects
    subsection_header("Priority Subjects (Least Mastered)", output_file)

    # Calculate mastery percentage for each subject
    subject_mastery = []
    for subject, subj_stats in subject_stats.items():
        mastery_pct = (subj_stats['mastered'] / subj_stats['total'] * 100) if subj_stats['total'] > 0 else 0
        subject_mastery.append((subject, mastery_pct, subj_stats['total'], subj_stats['mastered']))

    # Sort by mastery percentage (ascending)
    subject_mastery.sort(key=lambda x: x[1])

    print_and_log(f"{'Subject':<30s} {'Mastery':>12s} {'Cards':>10s}", output_file, Colors.BOLD)
    print_and_log("-" * 55, output_file)

    for subject, mastery_pct, total, mastered in subject_mastery[:10]:
        display = f"{subject:<30s} {mastery_pct:>11.1f}% {f'{mastered}/{total}':>10s}"

        if mastery_pct < 10:
            print_and_log(display, output_file, Colors.RED)
        elif mastery_pct < 25:
            print_and_log(display, output_file, Colors.YELLOW)
        else:
            print_and_log(display, output_file, Colors.CYAN)

    # Recommendations
    subsection_header("Personalized Recommendations", output_file)

    recommendations = []

    # Check if there are many due cards
    if cards_due > 50:
        recommendations.append("⚠️  You have a backlog of due cards. Focus on reviews before learning new material.")
    elif cards_due > 0:
        recommendations.append("✓ Start your session with due card reviews to maintain retention.")
    else:
        recommendations.append("🎉 No cards due! Great time to learn new material or preview upcoming concepts.")

    # Check mastery progress
    mastery_pct = (stats['cards_mastered'] / stats['total_cards'] * 100) if stats['total_cards'] > 0 else 0

    if mastery_pct < 10:
        recommendations.append("📚 You're in the early stages. Aim for 30-50 new cards per day to build momentum.")
    elif mastery_pct < 25:
        recommendations.append("📈 Good progress! Maintain a steady pace of 20-30 cards per day.")
    elif mastery_pct < 50:
        recommendations.append("💪 You're halfway there! Keep up the consistent daily reviews.")
    elif mastery_pct < 75:
        recommendations.append("🎯 Excellent progress! Focus on weak subjects to round out your knowledge.")
    else:
        recommendations.append("⭐ Outstanding mastery! Focus on maintaining your intervals and reinforcing weak areas.")

    # Subject-specific recommendations
    if subject_mastery:
        weakest_subject = subject_mastery[0][0]
        recommendations.append(f"🎯 Priority subject: {weakest_subject} - needs the most attention.")

    # Study strategy
    if stats['average_confidence'] < 2.0:
        recommendations.append("💡 Low average confidence. Consider reviewing fundamental concepts before advancing.")
    elif stats['average_confidence'] >= 3.0:
        recommendations.append("✨ High confidence! You're retaining material well. Keep up the great work!")

    for rec in recommendations:
        print_and_log(f"\n{rec}", output_file, Colors.GREEN)


# ==================== MAIN ====================

def main():
    """Generate comprehensive analytics report"""
    db_path = "iowa_bar_prep.db"

    # Check if database exists
    if not Path(db_path).exists():
        print(colorize(f"Error: Database not found at {db_path}", Colors.RED))
        print("Please run import_knowledge_to_adaptive.py first.")
        sys.exit(1)

    # Initialize system
    system = AdaptiveLearningSystem(db_path)

    # Open output file
    output_path = "analytics_adaptive_report.txt"
    with open(output_path, 'w') as output_file:
        # Report header
        header = f"""
{'=' * 80}
IOWA BAR PREP - ADAPTIVE LEARNING ANALYTICS REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'=' * 80}
"""
        print(colorize(header, Colors.HEADER + Colors.BOLD))
        output_file.write(header)

        # Generate all sections
        section_1_overall_performance(system, output_file)
        section_2_subject_breakdown(system, output_file)
        section_3_spaced_repetition_health(system, output_file)
        section_4_topic_deep_dive(system, output_file)
        section_5_study_recommendations(system, output_file)

        # Footer
        footer = f"\n{'=' * 80}\nReport saved to: {output_path}\n{'=' * 80}\n"
        print(colorize(footer, Colors.HEADER + Colors.BOLD))
        output_file.write(footer)

    # Close system
    system.close()


if __name__ == "__main__":
    main()
