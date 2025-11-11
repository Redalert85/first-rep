#!/usr/bin/env python3
"""
Session Analytics for Iowa Bar Prep
Comprehensive analysis of study sessions and performance trends
"""

import sqlite3
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List


class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    DIM = '\033[2m'


def get_session_data(db_path: str = "iowa_bar_prep.db"):
    """Get all session and performance data"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    # Get all sessions
    sessions = conn.execute("""
        SELECT session_date, cards_reviewed, avg_quality, duration_minutes
        FROM sessions
        ORDER BY session_date ASC
    """).fetchall()

    # Get all performance records
    performance = conn.execute("""
        SELECT p.review_date, p.quality, p.time_seconds, c.subject
        FROM performance p
        JOIN cards c ON p.card_id = c.card_id
        ORDER BY p.review_date ASC
    """).fetchall()

    conn.close()

    return sessions, performance


def analyze_sessions(sessions: List) -> Dict:
    """Analyze session statistics"""
    if not sessions:
        return None

    total_sessions = len(sessions)
    total_cards = sum(s['cards_reviewed'] for s in sessions)
    total_minutes = sum(s['duration_minutes'] for s in sessions)

    avg_cards_per_session = total_cards / total_sessions
    avg_duration = total_minutes / total_sessions
    avg_quality = sum(s['avg_quality'] for s in sessions) / total_sessions

    # Find best session
    best_session = max(sessions, key=lambda s: s['avg_quality'])

    # Find longest session
    longest_session = max(sessions, key=lambda s: s['cards_reviewed'])

    # Calculate consistency (sessions per week)
    if len(sessions) >= 2:
        first_date = datetime.fromisoformat(sessions[0]['session_date'])
        last_date = datetime.fromisoformat(sessions[-1]['session_date'])
        days_span = (last_date - first_date).days + 1
        sessions_per_week = (total_sessions / days_span) * 7 if days_span > 0 else 0
    else:
        sessions_per_week = 0

    return {
        'total_sessions': total_sessions,
        'total_cards': total_cards,
        'total_minutes': total_minutes,
        'total_hours': total_minutes / 60,
        'avg_cards_per_session': avg_cards_per_session,
        'avg_duration': avg_duration,
        'avg_quality': avg_quality,
        'best_session': best_session,
        'longest_session': longest_session,
        'sessions_per_week': sessions_per_week,
    }


def analyze_trends(sessions: List) -> Dict:
    """Analyze quality and performance trends"""
    if len(sessions) < 2:
        return None

    # Get quality trend (last 7 sessions)
    recent_sessions = sessions[-7:]
    quality_trend = [s['avg_quality'] for s in recent_sessions]

    # Calculate if improving
    if len(quality_trend) >= 2:
        first_half = sum(quality_trend[:len(quality_trend)//2]) / (len(quality_trend)//2)
        second_half = sum(quality_trend[len(quality_trend)//2:]) / (len(quality_trend) - len(quality_trend)//2)
        improving = second_half > first_half
    else:
        improving = None

    # Day of week analysis
    day_stats = defaultdict(lambda: {'sessions': 0, 'cards': 0, 'quality': []})
    for s in sessions:
        date = datetime.fromisoformat(s['session_date'])
        day_name = date.strftime('%A')
        day_stats[day_name]['sessions'] += 1
        day_stats[day_name]['cards'] += s['cards_reviewed']
        day_stats[day_name]['quality'].append(s['avg_quality'])

    # Calculate average quality per day
    for day in day_stats:
        day_stats[day]['avg_quality'] = sum(day_stats[day]['quality']) / len(day_stats[day]['quality'])

    # Find best day
    if day_stats:
        best_day = max(day_stats.items(), key=lambda x: x[1]['avg_quality'])
    else:
        best_day = None

    return {
        'quality_trend': quality_trend,
        'improving': improving,
        'day_stats': dict(day_stats),
        'best_day': best_day,
    }


def analyze_time_by_subject(performance: List) -> Dict:
    """Analyze time spent per subject"""
    subject_time = defaultdict(lambda: {'total_seconds': 0, 'count': 0, 'quality_sum': 0})

    for p in performance:
        if p['time_seconds']:
            subject = p['subject']
            subject_time[subject]['total_seconds'] += p['time_seconds']
            subject_time[subject]['count'] += 1
            subject_time[subject]['quality_sum'] += p['quality']

    # Calculate averages
    for subject in subject_time:
        data = subject_time[subject]
        data['avg_seconds'] = data['total_seconds'] / data['count']
        data['avg_quality'] = data['quality_sum'] / data['count']
        data['total_minutes'] = data['total_seconds'] / 60

    return dict(subject_time)


def create_ascii_chart(values: List[float], width: int = 50, height: int = 10) -> List[str]:
    """Create an ASCII line chart"""
    if not values:
        return []

    min_val = min(values)
    max_val = max(values)
    value_range = max_val - min_val if max_val != min_val else 1

    chart = []
    for y in range(height, 0, -1):
        threshold = min_val + (value_range * y / height)
        line = ""
        for val in values:
            if val >= threshold:
                line += "█"
            else:
                line += " "
        chart.append(line)

    return chart


def display_header():
    """Display header"""
    print("\n" + Colors.BOLD + Colors.CYAN + "=" * 80)
    print("                      SESSION ANALYTICS - DEEP DIVE")
    print("=" * 80 + Colors.RESET)
    print(f"{Colors.DIM}Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}{Colors.RESET}\n")


def display_session_overview(stats: Dict):
    """Display session overview"""
    print(Colors.BOLD + Colors.BLUE + "📊 SESSION OVERVIEW" + Colors.RESET)
    print("─" * 80)
    print(f"\n{Colors.BOLD}Total Study Sessions:{Colors.RESET} {stats['total_sessions']}")
    print(f"{Colors.BOLD}Total Cards Reviewed:{Colors.RESET} {stats['total_cards']}")
    print(f"{Colors.BOLD}Total Study Time:{Colors.RESET} {int(stats['total_hours'])} hours {int((stats['total_minutes'] % 60))} minutes")
    print(f"{Colors.BOLD}Average Quality:{Colors.RESET} {Colors.GREEN if stats['avg_quality'] >= 3.5 else Colors.YELLOW}{stats['avg_quality']:.2f}/5.0{Colors.RESET}")
    print(f"\n{Colors.BOLD}Per Session Averages:{Colors.RESET}")
    print(f"  Cards: {stats['avg_cards_per_session']:.1f}")
    print(f"  Duration: {stats['avg_duration']:.1f} minutes")
    print(f"  Consistency: {stats['sessions_per_week']:.1f} sessions/week")
    print()


def display_best_sessions(stats: Dict):
    """Display best session info"""
    print(Colors.BOLD + Colors.BLUE + "🏆 BEST SESSIONS" + Colors.RESET)
    print("─" * 80)

    best = stats['best_session']
    longest = stats['longest_session']

    print(f"\n{Colors.BOLD}Highest Quality:{Colors.RESET}")
    best_date = datetime.fromisoformat(best['session_date']).strftime('%B %d, %Y')
    print(f"  Date: {best_date}")
    print(f"  Cards: {best['cards_reviewed']}")
    print(f"  Quality: {Colors.GREEN}{best['avg_quality']:.2f}{Colors.RESET}")
    print(f"  Duration: {best['duration_minutes']} minutes")

    print(f"\n{Colors.BOLD}Longest Session:{Colors.RESET}")
    long_date = datetime.fromisoformat(longest['session_date']).strftime('%B %d, %Y')
    print(f"  Date: {long_date}")
    print(f"  Cards: {Colors.CYAN}{longest['cards_reviewed']}{Colors.RESET}")
    print(f"  Quality: {longest['avg_quality']:.2f}")
    print(f"  Duration: {longest['duration_minutes']} minutes")
    print()


def display_trends(trends: Dict, sessions: List):
    """Display quality trends"""
    print(Colors.BOLD + Colors.BLUE + "📈 QUALITY TRENDS" + Colors.RESET)
    print("─" * 80)

    print(f"\n{Colors.BOLD}Recent Sessions (Quality):{Colors.RESET}")

    # Show last 7 sessions
    recent = sessions[-7:]
    for i, s in enumerate(recent, 1):
        date = datetime.fromisoformat(s['session_date']).strftime('%b %d')
        quality_bar = "█" * int(s['avg_quality'])
        color = Colors.GREEN if s['avg_quality'] >= 3.5 else Colors.YELLOW
        print(f"  {i}. {date:>6} | {color}{quality_bar}{Colors.RESET} {s['avg_quality']:.2f}")

    if trends['improving'] is not None:
        status = f"{Colors.GREEN}📈 IMPROVING{Colors.RESET}" if trends['improving'] else f"{Colors.YELLOW}📉 Fluctuating{Colors.RESET}"
        print(f"\n{Colors.BOLD}Trend:{Colors.RESET} {status}")

    # Best day of week
    if trends['best_day']:
        day, stats_day = trends['best_day']
        print(f"\n{Colors.BOLD}Best Study Day:{Colors.RESET} {day} (avg quality: {Colors.GREEN}{stats_day['avg_quality']:.2f}{Colors.RESET})")

    print()


def display_time_analysis(time_by_subject: Dict):
    """Display time analysis by subject"""
    print(Colors.BOLD + Colors.BLUE + "⏱️  TIME ANALYSIS BY SUBJECT" + Colors.RESET)
    print("─" * 80)

    # Sort by total time
    sorted_subjects = sorted(
        time_by_subject.items(),
        key=lambda x: x[1]['total_minutes'],
        reverse=True
    )

    print(f"\n{'SUBJECT':<30} {'TIME':<15} {'AVG/CARD':<12} {'AVG QUALITY'}")
    print("─" * 80)

    for subject, data in sorted_subjects:
        subject_name = subject.replace('_', ' ').title()[:28]
        hours = int(data['total_minutes'] // 60)
        mins = int(data['total_minutes'] % 60)
        time_str = f"{hours}h {mins}m" if hours > 0 else f"{mins}m"

        quality_color = Colors.GREEN if data['avg_quality'] >= 3.5 else Colors.YELLOW

        print(f"{subject_name:<30} {time_str:<15} {data['avg_seconds']:.1f}s      {quality_color}{data['avg_quality']:.2f}{Colors.RESET}")

    print()


def display_insights(stats: Dict, trends: Dict):
    """Display insights and recommendations"""
    print(Colors.BOLD + Colors.BLUE + "💡 INSIGHTS & RECOMMENDATIONS" + Colors.RESET)
    print("─" * 80)
    print()

    insights = []

    # Study frequency
    if stats['sessions_per_week'] >= 5:
        insights.append(f"{Colors.GREEN}✓ Excellent consistency! You're studying {stats['sessions_per_week']:.1f}x per week.{Colors.RESET}")
    elif stats['sessions_per_week'] >= 3:
        insights.append(f"{Colors.YELLOW}• Good consistency at {stats['sessions_per_week']:.1f}x per week. Try for daily sessions!{Colors.RESET}")
    else:
        insights.append(f"{Colors.YELLOW}• Consider increasing frequency to 5-7x per week for better retention.{Colors.RESET}")

    # Quality trends
    if trends and trends['improving']:
        insights.append(f"{Colors.GREEN}✓ Your quality scores are improving! Keep up the momentum.{Colors.RESET}")

    # Average quality
    if stats['avg_quality'] >= 4.0:
        insights.append(f"{Colors.GREEN}✓ Outstanding avg quality ({stats['avg_quality']:.2f})! You're mastering the material.{Colors.RESET}")
    elif stats['avg_quality'] >= 3.5:
        insights.append(f"{Colors.GREEN}✓ Good avg quality ({stats['avg_quality']:.2f}). Continue your current approach.{Colors.RESET}")
    else:
        insights.append(f"{Colors.YELLOW}• Avg quality is {stats['avg_quality']:.2f}. Consider reviewing difficult cards more carefully.{Colors.RESET}")

    # Session length
    if stats['avg_cards_per_session'] < 20:
        insights.append(f"{Colors.YELLOW}• Try longer sessions (30+ cards) to build momentum.{Colors.RESET}")

    for insight in insights:
        print(insight)

    print()


def main():
    """Main analytics display"""
    sessions, performance = get_session_data()

    if not sessions:
        print("\n⚠️  No session data found!")
        print("Start studying with daily_study.py to generate analytics.\n")
        return

    # Analyze data
    stats = analyze_sessions(sessions)
    trends = analyze_trends(sessions)
    time_by_subject = analyze_time_by_subject(performance) if performance else {}

    # Display sections
    display_header()
    display_session_overview(stats)
    display_best_sessions(stats)
    display_trends(trends, sessions)

    if time_by_subject:
        display_time_analysis(time_by_subject)

    display_insights(stats, trends)

    print("─" * 80)
    print(f"{Colors.DIM}Run: python3 card_history.py [card_id] to see individual card review history{Colors.RESET}")
    print(Colors.CYAN + "=" * 80 + Colors.RESET)
    print()


if __name__ == "__main__":
    main()
