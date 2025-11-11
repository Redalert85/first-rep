#!/usr/bin/env python3
"""
Card Review History Viewer for Iowa Bar Prep
View detailed review history and performance trends for individual cards
"""

import sqlite3
import sys
from datetime import datetime
from typing import List, Dict, Optional


class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    DIM = '\033[2m'


def get_card_info(card_id: str, db_path: str = "iowa_bar_prep.db") -> Optional[Dict]:
    """Get card information"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    card = conn.execute("""
        SELECT * FROM cards WHERE card_id = ?
    """, (card_id,)).fetchone()

    conn.close()

    if not card:
        return None

    return dict(card)


def get_card_performance(card_id: str, db_path: str = "iowa_bar_prep.db") -> List[Dict]:
    """Get performance history for a card"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    performance = conn.execute("""
        SELECT review_date, quality, time_seconds
        FROM performance
        WHERE card_id = ?
        ORDER BY review_date ASC
    """, (card_id,)).fetchall()

    conn.close()

    return [dict(p) for p in performance]


def search_cards(search_term: str, db_path: str = "iowa_bar_prep.db") -> List[Dict]:
    """Search for cards by text"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    cards = conn.execute("""
        SELECT card_id, subject, card_type, front
        FROM cards
        WHERE front LIKE ? OR back LIKE ?
        LIMIT 20
    """, (f'%{search_term}%', f'%{search_term}%')).fetchall()

    conn.close()

    return [dict(c) for c in cards]


def quality_to_label(quality: int) -> str:
    """Convert quality score to label"""
    labels = {
        0: "No Idea",
        1: "Vague",
        2: "Uncertain",
        3: "Confident",
        4: "Mastered",
        5: "Perfect"
    }
    return labels.get(quality, "Unknown")


def quality_to_color(quality: int) -> str:
    """Get color for quality score"""
    if quality >= 4:
        return Colors.GREEN
    elif quality >= 3:
        return Colors.YELLOW
    else:
        return Colors.RED


def analyze_performance_trend(performance: List[Dict]) -> Dict:
    """Analyze performance trends"""
    if not performance:
        return {}

    first_quality = performance[0]['quality']
    last_quality = performance[-1]['quality']
    avg_quality = sum(p['quality'] for p in performance) / len(performance)

    # Calculate quality trend
    quality_improvement = last_quality - first_quality

    # Calculate time trend (if available)
    times = [p['time_seconds'] for p in performance if p['time_seconds']]
    if len(times) >= 2:
        first_time = times[0]
        last_time = times[-1]
        time_improvement = first_time - last_time
        avg_time = sum(times) / len(times)
    else:
        first_time = None
        last_time = None
        time_improvement = None
        avg_time = None

    # Determine trend
    if quality_improvement > 0:
        trend = "improving"
    elif quality_improvement < 0:
        trend = "declining"
    else:
        trend = "stable"

    return {
        'first_quality': first_quality,
        'last_quality': last_quality,
        'avg_quality': avg_quality,
        'quality_improvement': quality_improvement,
        'first_time': first_time,
        'last_time': last_time,
        'time_improvement': time_improvement,
        'avg_time': avg_time,
        'trend': trend,
        'total_reviews': len(performance),
    }


def display_card_header(card: Dict):
    """Display card header"""
    print("\n" + Colors.BOLD + Colors.CYAN + "=" * 80)
    print("                        CARD REVIEW HISTORY")
    print("=" * 80 + Colors.RESET)
    print(f"\n{Colors.BOLD}Card ID:{Colors.RESET} {card['card_id']}")
    print(f"{Colors.BOLD}Subject:{Colors.RESET} {card['subject'].replace('_', ' ').title()}")
    if card['topic']:
        print(f"{Colors.BOLD}Topic:{Colors.RESET} {card['topic']}")
    print(f"{Colors.BOLD}Type:{Colors.RESET} {card['card_type'].upper()}")
    print(f"{Colors.BOLD}Difficulty:{Colors.RESET} {'⭐' * card['difficulty']}")


def display_card_content(card: Dict):
    """Display card content"""
    print("\n" + Colors.BOLD + Colors.BLUE + "📄 CARD CONTENT" + Colors.RESET)
    print("─" * 80)
    print(f"\n{Colors.BOLD}FRONT:{Colors.RESET}")
    print(Colors.DIM + "─" * 80 + Colors.RESET)
    front_preview = card['front'][:200] + "..." if len(card['front']) > 200 else card['front']
    print(front_preview)

    print(f"\n{Colors.BOLD}BACK:{Colors.RESET}")
    print(Colors.DIM + "─" * 80 + Colors.RESET)
    back_preview = card['back'][:200] + "..." if len(card['back']) > 200 else card['back']
    print(back_preview)
    print()


def display_current_status(card: Dict):
    """Display current SM-2 status"""
    print(Colors.BOLD + Colors.BLUE + "📊 CURRENT STATUS" + Colors.RESET)
    print("─" * 80)
    print(f"\n{Colors.BOLD}Times Reviewed:{Colors.RESET} {card['times_seen']}")
    print(f"{Colors.BOLD}Times Correct:{Colors.RESET} {Colors.GREEN}{card['times_correct']}{Colors.RESET}")
    print(f"{Colors.BOLD}Times Incorrect:{Colors.RESET} {Colors.RED}{card['times_incorrect']}{Colors.RESET}")

    if card['times_seen'] > 0:
        accuracy = (card['times_correct'] / card['times_seen']) * 100
        acc_color = Colors.GREEN if accuracy >= 80 else (Colors.YELLOW if accuracy >= 60 else Colors.RED)
        print(f"{Colors.BOLD}Accuracy:{Colors.RESET} {acc_color}{accuracy:.1f}%{Colors.RESET}")

    print(f"\n{Colors.BOLD}SM-2 Parameters:{Colors.RESET}")
    print(f"  Ease Factor: {card['ease_factor']:.2f}")
    print(f"  Interval: {card['interval']} days")
    print(f"  Repetitions: {card['repetitions']}")

    if card['next_review']:
        next_review = datetime.fromisoformat(card['next_review'])
        now = datetime.now()
        if next_review > now:
            days_until = (next_review - now).days
            print(f"  Next Review: {next_review.strftime('%B %d, %Y')} ({days_until} days)")
        else:
            print(f"  Next Review: {Colors.YELLOW}DUE NOW{Colors.RESET}")
    print()


def display_review_history(performance: List[Dict]):
    """Display review history"""
    print(Colors.BOLD + Colors.BLUE + "📝 REVIEW HISTORY" + Colors.RESET)
    print("─" * 80)

    if not performance:
        print("\nNo reviews recorded yet.")
        return

    print(f"\n{'#':<4} {'DATE':<20} {'QUALITY':<25} {'TIME':<10}")
    print("─" * 80)

    for i, p in enumerate(performance, 1):
        review_date = datetime.fromisoformat(p['review_date']).strftime('%b %d, %Y %I:%M%p')
        quality = p['quality']
        quality_label = quality_to_label(quality)
        quality_color = quality_to_color(quality)

        quality_bar = "█" * quality
        quality_str = f"{quality_color}{quality_bar}{Colors.RESET} {quality} ({quality_label})"

        time_str = f"{p['time_seconds']}s" if p['time_seconds'] else "N/A"

        print(f"{i:<4} {review_date:<20} {quality_str:<35} {time_str:<10}")

    print()


def display_performance_analysis(analysis: Dict):
    """Display performance analysis"""
    print(Colors.BOLD + Colors.BLUE + "📈 PERFORMANCE ANALYSIS" + Colors.RESET)
    print("─" * 80)

    if not analysis:
        print("\nInsufficient data for analysis.")
        return

    print(f"\n{Colors.BOLD}Total Reviews:{Colors.RESET} {analysis['total_reviews']}")
    print(f"{Colors.BOLD}Average Quality:{Colors.RESET} {analysis['avg_quality']:.2f}/5.0")

    # Quality trend
    improvement = analysis['quality_improvement']
    if improvement > 0:
        trend_icon = "📈"
        trend_color = Colors.GREEN
        trend_text = f"IMPROVING (+{improvement})"
    elif improvement < 0:
        trend_icon = "📉"
        trend_color = Colors.RED
        trend_text = f"DECLINING ({improvement})"
    else:
        trend_icon = "➡️"
        trend_color = Colors.YELLOW
        trend_text = "STABLE"

    print(f"{Colors.BOLD}Quality Trend:{Colors.RESET} {trend_icon} {trend_color}{trend_text}{Colors.RESET}")
    print(f"  First: {analysis['first_quality']} → Last: {analysis['last_quality']}")

    # Time trend
    if analysis['avg_time']:
        print(f"\n{Colors.BOLD}Time Analysis:{Colors.RESET}")
        print(f"  Average: {analysis['avg_time']:.1f} seconds")

        if analysis['time_improvement'] is not None:
            if analysis['time_improvement'] > 0:
                print(f"  Trend: {Colors.GREEN}⚡ Getting faster (-{analysis['time_improvement']:.1f}s){Colors.RESET}")
            elif analysis['time_improvement'] < 0:
                print(f"  Trend: {Colors.YELLOW}🐌 Taking longer (+{abs(analysis['time_improvement']):.1f}s){Colors.RESET}")
            else:
                print(f"  Trend: Consistent")

    print()


def display_recommendations(card: Dict, analysis: Dict):
    """Display recommendations"""
    print(Colors.BOLD + Colors.BLUE + "💡 RECOMMENDATIONS" + Colors.RESET)
    print("─" * 80)
    print()

    recommendations = []

    # Check if it's a leech
    if card['times_seen'] >= 5 and card['times_correct'] < card['times_seen'] * 0.6:
        recommendations.append(f"{Colors.RED}⚠️  LEECH DETECTED: This card is difficult. Consider rewriting or splitting it.{Colors.RESET}")

    # Check quality trend
    if analysis and analysis['trend'] == 'declining':
        recommendations.append(f"{Colors.YELLOW}• Quality is declining. Review the fundamentals before continuing.{Colors.RESET}")
    elif analysis and analysis['trend'] == 'improving':
        recommendations.append(f"{Colors.GREEN}✓ Quality is improving! Keep up the good work.{Colors.RESET}")

    # Check time
    if analysis and analysis['avg_time'] and analysis['avg_time'] > 60:
        recommendations.append(f"{Colors.YELLOW}• This card takes a long time. Consider simplifying the content.{Colors.RESET}")

    # Check mastery
    if card['ease_factor'] >= 2.5 and card['interval'] >= 21:
        recommendations.append(f"{Colors.GREEN}✓ Card is mastered! Long-term retention achieved.{Colors.RESET}")

    if not recommendations:
        recommendations.append(f"{Colors.GREEN}• Continue reviewing as scheduled.{Colors.RESET}")

    for rec in recommendations:
        print(rec)

    print()


def display_search_results(cards: List[Dict]):
    """Display search results"""
    print("\n" + Colors.BOLD + Colors.CYAN + "SEARCH RESULTS" + Colors.RESET)
    print("─" * 80)
    print(f"\nFound {len(cards)} matching cards:\n")

    print(f"{'#':<4} {'CARD ID':<18} {'SUBJECT':<20} {'TYPE':<10} {'PREVIEW'}")
    print("─" * 80)

    for i, card in enumerate(cards, 1):
        subject = card['subject'].replace('_', ' ').title()[:18]
        front_preview = card['front'].replace('\n', ' ')[:40]
        print(f"{i:<4} {card['card_id']:<18} {subject:<20} {card['card_type']:<10} {front_preview}...")

    print(f"\n{Colors.DIM}Use: python3 card_history.py [card_id] to view detailed history{Colors.RESET}")
    print()


def main():
    """Main card history viewer"""
    if len(sys.argv) < 2:
        print("\n" + Colors.BOLD + "CARD REVIEW HISTORY VIEWER" + Colors.RESET)
        print("\nUsage:")
        print(f"  {Colors.CYAN}python3 card_history.py [card_id]{Colors.RESET}          # View specific card")
        print(f"  {Colors.CYAN}python3 card_history.py --search \"term\"{Colors.RESET}    # Search for cards")
        print("\nExamples:")
        print(f"  python3 card_history.py 1740f942a30e7048")
        print(f"  python3 card_history.py --search \"mailbox rule\"")
        print(f"  python3 card_history.py --search \"commerce clause\"")
        print()
        return

    # Handle search
    if sys.argv[1] == "--search":
        if len(sys.argv) < 3:
            print(f"\n{Colors.RED}Error: Please provide a search term{Colors.RESET}")
            print("Usage: python3 card_history.py --search \"term\"\n")
            return

        search_term = " ".join(sys.argv[2:])
        cards = search_cards(search_term)

        if not cards:
            print(f"\n{Colors.YELLOW}No cards found matching: {search_term}{Colors.RESET}\n")
            return

        display_search_results(cards)
        return

    # View specific card
    card_id = sys.argv[1]

    # Get card info
    card = get_card_info(card_id)
    if not card:
        print(f"\n{Colors.RED}Error: Card not found: {card_id}{Colors.RESET}\n")
        return

    # Get performance history
    performance = get_card_performance(card_id)

    # Analyze performance
    analysis = analyze_performance_trend(performance)

    # Display all sections
    display_card_header(card)
    display_card_content(card)
    display_current_status(card)
    display_review_history(performance)
    display_performance_analysis(analysis)
    display_recommendations(card, analysis)

    print("─" * 80)
    print(Colors.CYAN + "=" * 80 + Colors.RESET)
    print()


if __name__ == "__main__":
    main()
