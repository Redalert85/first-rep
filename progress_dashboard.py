#!/usr/bin/env python3
"""
Progress Dashboard for Iowa Bar Prep
Comprehensive analytics and study tracking
"""

import sqlite3
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List, Tuple


# ANSI color codes for terminal output
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

    # Colors
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'

    # Backgrounds
    BG_RED = '\033[101m'
    BG_GREEN = '\033[102m'
    BG_YELLOW = '\033[103m'
    BG_BLUE = '\033[104m'


def create_progress_bar(percentage: float, width: int = 30) -> str:
    """Create a visual progress bar"""
    filled = int(width * percentage / 100)
    empty = width - filled

    # Color based on percentage
    if percentage >= 80:
        color = Colors.GREEN
    elif percentage >= 50:
        color = Colors.YELLOW
    else:
        color = Colors.RED

    bar = color + '█' * filled + Colors.DIM + '░' * empty + Colors.RESET
    return f"[{bar}] {percentage:5.1f}%"


def get_database_stats(db_path: str = "iowa_bar_prep.db") -> Dict:
    """Get comprehensive database statistics"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    stats = {
        'total_cards': 0,
        'cards_seen': 0,
        'cards_never_seen': 0,
        'cards_mastered': 0,
        'total_reviews': 0,
        'overall_accuracy': 0.0,
        'subjects': {},
        'studied_today': 0,
        'studied_this_week': 0,
        'study_dates': [],
    }

    # Get all cards
    cards = conn.execute("SELECT * FROM cards").fetchall()

    stats['total_cards'] = len(cards)

    now = datetime.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today_start - timedelta(days=today_start.weekday())

    total_correct = 0
    total_seen = 0

    # Track study dates for streak calculation
    study_dates_set = set()

    for card in cards:
        # Overall stats
        times_seen = card['times_seen']
        times_correct = card['times_correct']

        if times_seen > 0:
            stats['cards_seen'] += 1
            total_seen += times_seen
            total_correct += times_correct
        else:
            stats['cards_never_seen'] += 1

        # Check if mastered (high ease factor, long interval, multiple correct reviews)
        ease_factor = card['ease_factor']
        interval = card['interval']
        if ease_factor >= 2.5 and interval >= 21 and times_correct >= 3:
            stats['cards_mastered'] += 1

        # Track when reviewed
        if card['last_reviewed']:
            try:
                last_review = datetime.fromisoformat(card['last_reviewed'])
                study_dates_set.add(last_review.date())

                if last_review >= today_start:
                    stats['studied_today'] += 1
                if last_review >= week_start:
                    stats['studied_this_week'] += 1
            except:
                pass

        # Subject stats
        subject = card['subject']
        if subject not in stats['subjects']:
            stats['subjects'][subject] = {
                'total': 0,
                'seen': 0,
                'mastered': 0,
                'correct': 0,
                'total_seen_count': 0,
                'due': 0,
            }

        stats['subjects'][subject]['total'] += 1
        if times_seen > 0:
            stats['subjects'][subject]['seen'] += 1
        stats['subjects'][subject]['correct'] += times_correct
        stats['subjects'][subject]['total_seen_count'] += times_seen

        if ease_factor >= 2.5 and interval >= 21 and times_correct >= 3:
            stats['subjects'][subject]['mastered'] += 1

        # Check if due
        if card['next_review'] is None:
            stats['subjects'][subject]['due'] += 1
        else:
            try:
                next_review = datetime.fromisoformat(card['next_review'])
                if next_review <= now:
                    stats['subjects'][subject]['due'] += 1
            except:
                pass

    stats['total_reviews'] = total_seen
    stats['overall_accuracy'] = (total_correct / total_seen * 100) if total_seen > 0 else 0.0
    stats['study_dates'] = sorted(study_dates_set)

    conn.close()
    return stats


def calculate_study_streak(study_dates: List) -> Tuple[int, int]:
    """Calculate current streak and longest streak"""
    if not study_dates:
        return 0, 0

    current_streak = 0
    longest_streak = 0
    temp_streak = 1

    today = datetime.now().date()

    # Check current streak
    if study_dates[-1] == today or study_dates[-1] == today - timedelta(days=1):
        current_streak = 1
        check_date = study_dates[-1]

        for i in range(len(study_dates) - 2, -1, -1):
            expected_date = check_date - timedelta(days=1)
            if study_dates[i] == expected_date:
                current_streak += 1
                check_date = study_dates[i]
            elif study_dates[i] < expected_date:
                break

    # Calculate longest streak
    for i in range(1, len(study_dates)):
        if study_dates[i] == study_dates[i-1] + timedelta(days=1):
            temp_streak += 1
            longest_streak = max(longest_streak, temp_streak)
        else:
            temp_streak = 1

    longest_streak = max(longest_streak, temp_streak, current_streak)

    return current_streak, longest_streak


def project_completion_date(stats: Dict) -> str:
    """Project completion date based on current pace"""
    cards_remaining = stats['total_cards'] - stats['cards_mastered']

    if cards_remaining == 0:
        return "COMPLETED! 🎉"

    if stats['studied_this_week'] == 0:
        return "N/A (no recent activity)"

    # Calculate daily average over the week
    daily_avg = stats['studied_this_week'] / 7

    if daily_avg == 0:
        return "N/A (no recent activity)"

    # Estimate days to complete (assuming mastery rate)
    mastery_rate = stats['cards_mastered'] / stats['cards_seen'] if stats['cards_seen'] > 0 else 0.1

    # Need to review cards multiple times to master them
    reviews_needed = cards_remaining * 5  # Rough estimate: 5 reviews to master
    days_to_complete = reviews_needed / daily_avg

    completion_date = datetime.now() + timedelta(days=days_to_complete)

    return f"{completion_date.strftime('%B %d, %Y')} (~{int(days_to_complete)} days)"


def identify_weak_subjects(stats: Dict) -> List[Tuple[str, float]]:
    """Identify subjects needing attention"""
    weak_subjects = []

    for subject, data in stats['subjects'].items():
        if data['total_seen_count'] == 0:
            accuracy = 0.0
        else:
            accuracy = (data['correct'] / data['total_seen_count']) * 100

        mastery_pct = (data['mastered'] / data['total']) * 100

        # Weak if low accuracy or low mastery
        weakness_score = 100 - ((accuracy + mastery_pct) / 2)

        weak_subjects.append((subject, weakness_score, accuracy, mastery_pct))

    # Sort by weakness score
    weak_subjects.sort(key=lambda x: x[1], reverse=True)

    return weak_subjects


def display_header():
    """Display dashboard header"""
    print("\n" + Colors.BOLD + Colors.CYAN + "=" * 80)
    print("                    IOWA BAR PREP - PROGRESS DASHBOARD")
    print("=" * 80 + Colors.RESET)
    print(f"{Colors.DIM}Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}{Colors.RESET}\n")


def display_overall_stats(stats: Dict):
    """Display overall statistics"""
    print(Colors.BOLD + Colors.BLUE + "📊 OVERALL PROGRESS" + Colors.RESET)
    print("─" * 80)

    # Calculate percentages
    seen_pct = (stats['cards_seen'] / stats['total_cards']) * 100
    mastery_pct = (stats['cards_mastered'] / stats['total_cards']) * 100

    print(f"\n{Colors.BOLD}Total Cards:{Colors.RESET} {stats['total_cards']}")
    print(f"{Colors.BOLD}Cards Studied:{Colors.RESET} {stats['cards_seen']} / {stats['total_cards']} {create_progress_bar(seen_pct, 20)}")
    print(f"{Colors.BOLD}Cards Mastered:{Colors.RESET} {stats['cards_mastered']} / {stats['total_cards']} {create_progress_bar(mastery_pct, 20)}")
    print(f"{Colors.BOLD}Cards Never Seen:{Colors.RESET} {Colors.YELLOW}{stats['cards_never_seen']}{Colors.RESET}")
    print(f"{Colors.BOLD}Total Reviews:{Colors.RESET} {stats['total_reviews']}")
    print(f"{Colors.BOLD}Overall Accuracy:{Colors.RESET} {Colors.GREEN if stats['overall_accuracy'] >= 80 else Colors.YELLOW}{stats['overall_accuracy']:.1f}%{Colors.RESET}")
    print()


def display_recent_activity(stats: Dict):
    """Display recent study activity"""
    print(Colors.BOLD + Colors.BLUE + "📅 RECENT ACTIVITY" + Colors.RESET)
    print("─" * 80)

    current_streak, longest_streak = calculate_study_streak(stats['study_dates'])

    print(f"\n{Colors.BOLD}Studied Today:{Colors.RESET} {Colors.GREEN if stats['studied_today'] > 0 else Colors.RED}{stats['studied_today']} cards{Colors.RESET}")
    print(f"{Colors.BOLD}Studied This Week:{Colors.RESET} {stats['studied_this_week']} cards")
    print(f"{Colors.BOLD}Current Streak:{Colors.RESET} {Colors.CYAN}{current_streak} day{'s' if current_streak != 1 else ''}{Colors.RESET}")
    print(f"{Colors.BOLD}Longest Streak:{Colors.RESET} {Colors.MAGENTA}{longest_streak} day{'s' if longest_streak != 1 else ''}{Colors.RESET}")

    # Projected completion
    completion = project_completion_date(stats)
    print(f"{Colors.BOLD}Projected Completion:{Colors.RESET} {Colors.CYAN}{completion}{Colors.RESET}")
    print()


def display_subject_progress(stats: Dict):
    """Display progress by subject"""
    print(Colors.BOLD + Colors.BLUE + "📚 PROGRESS BY SUBJECT" + Colors.RESET)
    print("─" * 80)
    print()

    # Sort subjects by mastery percentage
    subjects_sorted = sorted(
        stats['subjects'].items(),
        key=lambda x: (x[1]['mastered'] / x[1]['total']) * 100,
        reverse=True
    )

    print(f"{'SUBJECT':<30} {'MASTERY':<35} {'DUE':<8} {'ACCURACY'}")
    print("─" * 80)

    for subject, data in subjects_sorted:
        mastery_pct = (data['mastered'] / data['total']) * 100
        accuracy = (data['correct'] / data['total_seen_count']) * 100 if data['total_seen_count'] > 0 else 0.0

        # Format subject name
        subject_name = subject.replace('_', ' ').title()[:28]

        # Color code due cards
        if data['due'] > 20:
            due_color = Colors.RED
        elif data['due'] > 10:
            due_color = Colors.YELLOW
        else:
            due_color = Colors.GREEN

        # Color code accuracy
        if accuracy >= 80:
            acc_color = Colors.GREEN
        elif accuracy >= 60:
            acc_color = Colors.YELLOW
        else:
            acc_color = Colors.RED

        print(f"{subject_name:<30} {create_progress_bar(mastery_pct, 20)} {due_color}{data['due']:>3}{Colors.RESET}    {acc_color}{accuracy:>5.1f}%{Colors.RESET}")

    print()


def display_weak_subjects(stats: Dict):
    """Display subjects needing attention"""
    print(Colors.BOLD + Colors.BLUE + "⚠️  SUBJECTS NEEDING ATTENTION" + Colors.RESET)
    print("─" * 80)
    print()

    weak = identify_weak_subjects(stats)

    # Show top 5 weakest
    print(f"{'SUBJECT':<30} {'MASTERY':<12} {'ACCURACY':<12} {'PRIORITY'}")
    print("─" * 80)

    for i, (subject, weakness, accuracy, mastery) in enumerate(weak[:5], 1):
        subject_name = subject.replace('_', ' ').title()[:28]

        if weakness >= 70:
            priority = f"{Colors.RED}HIGH{Colors.RESET}"
        elif weakness >= 50:
            priority = f"{Colors.YELLOW}MEDIUM{Colors.RESET}"
        else:
            priority = f"{Colors.GREEN}LOW{Colors.RESET}"

        print(f"{subject_name:<30} {mastery:>5.1f}%      {accuracy:>5.1f}%      {priority}")

    print()


def display_recommendations(stats: Dict):
    """Display study recommendations"""
    print(Colors.BOLD + Colors.BLUE + "💡 RECOMMENDATIONS FOR TOMORROW" + Colors.RESET)
    print("─" * 80)
    print()

    recommendations = []

    # Check if studied today
    if stats['studied_today'] == 0:
        recommendations.append(f"{Colors.YELLOW}• Start your study session! You haven't studied any cards today.{Colors.RESET}")

    # Check streak
    current_streak, _ = calculate_study_streak(stats['study_dates'])
    if current_streak == 0:
        recommendations.append(f"{Colors.RED}• Resume your study streak! Study at least 10 cards to build momentum.{Colors.RESET}")
    elif current_streak > 0 and stats['studied_today'] > 0:
        recommendations.append(f"{Colors.GREEN}• Great job! Keep your {current_streak}-day streak alive tomorrow!{Colors.RESET}")

    # Find subjects with most due cards
    subjects_by_due = sorted(
        stats['subjects'].items(),
        key=lambda x: x[1]['due'],
        reverse=True
    )

    if subjects_by_due[0][1]['due'] > 0:
        subject = subjects_by_due[0][0].replace('_', ' ').title()
        due_count = subjects_by_due[0][1]['due']
        recommendations.append(f"{Colors.CYAN}• Focus on {subject} - {due_count} cards are due for review.{Colors.RESET}")

    # Check weak subjects
    weak = identify_weak_subjects(stats)
    if weak and weak[0][1] > 60:  # High weakness score
        subject = weak[0][0].replace('_', ' ').title()
        recommendations.append(f"{Colors.MAGENTA}• Spend extra time on {subject} - it needs more attention.{Colors.RESET}")

    # Daily goal
    daily_goal = 30
    if stats['studied_today'] < daily_goal:
        remaining = daily_goal - stats['studied_today']
        recommendations.append(f"{Colors.BLUE}• Daily goal: Study {remaining} more cards to reach your target of {daily_goal}.{Colors.RESET}")
    else:
        recommendations.append(f"{Colors.GREEN}• Daily goal achieved! You've studied {stats['studied_today']} cards today.{Colors.RESET}")

    # Print recommendations
    for rec in recommendations:
        print(rec)

    print()


def display_footer():
    """Display footer with commands"""
    print("─" * 80)
    print(f"{Colors.DIM}Commands: python3 daily_study.py | python3 subject_study.py | python3 enhance_cards.py{Colors.RESET}")
    print(Colors.CYAN + "=" * 80 + Colors.RESET)
    print()


def main():
    """Main dashboard display"""
    # Get all statistics
    stats = get_database_stats()

    # Display dashboard sections
    display_header()
    display_overall_stats(stats)
    display_recent_activity(stats)
    display_subject_progress(stats)
    display_weak_subjects(stats)
    display_recommendations(stats)
    display_footer()


if __name__ == "__main__":
    main()
