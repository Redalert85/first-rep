#!/usr/bin/env python3
"""
Iowa Bar Prep Analytics Dashboard
Comprehensive analytics and recommendations for adaptive learning system
"""

import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any
from collections import defaultdict
from adaptive_learning_system import AdaptiveLearningSystem

# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_header(text: str, char: str = "="):
    """Print a formatted header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{char * 80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{char * 80}{Colors.END}\n")

def print_section(text: str):
    """Print a section header"""
    print(f"\n{Colors.BOLD}{Colors.GREEN}{'─' * 80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}{'─' * 80}{Colors.END}\n")

def print_metric(label: str, value: Any, color: str = Colors.CYAN):
    """Print a metric with label"""
    print(f"  {Colors.BOLD}{label:.<50}{color}{value}{Colors.END}")

def print_warning(text: str):
    """Print a warning message"""
    print(f"  {Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_success(text: str):
    """Print a success message"""
    print(f"  {Colors.GREEN}✓ {text}{Colors.END}")

def print_recommendation(text: str):
    """Print a recommendation"""
    print(f"  {Colors.CYAN}→ {text}{Colors.END}")

class BarPrepAnalytics:
    """Comprehensive analytics for Iowa Bar Prep system"""

    def __init__(self, db_path: str = "iowa_bar_prep.db"):
        self.system = AdaptiveLearningSystem(db_path)
        self.conn = self.system.conn
        self.report_lines = []

    def log(self, text: str):
        """Log text for both terminal and file output"""
        # Strip ANSI codes for file output
        import re
        clean_text = re.sub(r'\033\[[0-9;]*m', '', text)
        self.report_lines.append(clean_text)
        print(text)

    def overall_performance_report(self):
        """Section 1: Overall Performance Report"""
        self.log(f"{Colors.BOLD}{Colors.BLUE}{'=' * 80}{Colors.END}")
        self.log(f"{Colors.BOLD}{Colors.CYAN}1. OVERALL PERFORMANCE REPORT{Colors.END}")
        self.log(f"{Colors.BOLD}{Colors.BLUE}{'=' * 80}{Colors.END}\n")

        cursor = self.conn.cursor()

        # Total cards
        cursor.execute("SELECT COUNT(*) as count FROM cards")
        total_cards = cursor.fetchone()['count']
        self.log(f"  {Colors.BOLD}Total Cards{'.':.<50}{Colors.CYAN}{total_cards:,}{Colors.END}")

        # Due cards today
        cursor.execute("SELECT COUNT(*) as count FROM cards WHERE date(due_date) <= date('now')")
        due_today = cursor.fetchone()['count']
        color = Colors.RED if due_today > 100 else Colors.YELLOW if due_today > 50 else Colors.GREEN
        self.log(f"  {Colors.BOLD}Due Cards Today{'.':.<50}{color}{due_today:,}{Colors.END}")

        # Mastered cards
        cursor.execute("""
            SELECT COUNT(*) as count FROM cards
            WHERE ease_factor >= 2.5 AND interval_days >= 15
        """)
        mastered = cursor.fetchone()['count']
        mastery_pct = (mastered / total_cards * 100) if total_cards > 0 else 0
        self.log(f"  {Colors.BOLD}Mastered Cards{'.':.<50}{Colors.GREEN}{mastered:,} ({mastery_pct:.1f}%){Colors.END}")

        # Total reviews
        cursor.execute("SELECT COUNT(*) as count FROM performance")
        total_reviews = cursor.fetchone()['count']
        self.log(f"  {Colors.BOLD}Total Reviews{'.':.<50}{Colors.CYAN}{total_reviews:,}{Colors.END}")

        if total_reviews > 0:
            # Global accuracy
            cursor.execute("""
                SELECT AVG(CASE WHEN quality >= 3 THEN 1.0 ELSE 0.0 END) as accuracy
                FROM performance
            """)
            accuracy = cursor.fetchone()['accuracy'] or 0
            color = Colors.GREEN if accuracy >= 0.8 else Colors.YELLOW if accuracy >= 0.6 else Colors.RED
            self.log(f"  {Colors.BOLD}Global Accuracy{'.':.<50}{color}{accuracy:.1%}{Colors.END}")

            # Average quality
            cursor.execute("SELECT AVG(quality) as avg_quality FROM performance")
            avg_quality = cursor.fetchone()['avg_quality'] or 0
            self.log(f"  {Colors.BOLD}Average Quality Score{'.':.<50}{Colors.CYAN}{avg_quality:.2f}/5.0{Colors.END}")

            # Cards reviewed in last 7 days
            cursor.execute("""
                SELECT COUNT(DISTINCT card_id) as count FROM performance
                WHERE date(review_date) >= date('now', '-7 days')
            """)
            recent_reviews = cursor.fetchone()['count']
            self.log(f"  {Colors.BOLD}Cards Reviewed (Last 7 Days){'.':.<50}{Colors.CYAN}{recent_reviews:,}{Colors.END}")
        else:
            self.log(f"\n  {Colors.YELLOW}⚠️  No reviews recorded yet. Start studying to see performance metrics!{Colors.END}")

        # Study streak
        cursor.execute("""
            SELECT COUNT(DISTINCT date(review_date)) as days
            FROM performance
            WHERE date(review_date) >= date('now', '-7 days')
        """)
        study_days = cursor.fetchone()['days']
        self.log(f"  {Colors.BOLD}Study Days (Last 7 Days){'.':.<50}{Colors.CYAN}{study_days}/7{Colors.END}")

    def subject_specific_breakdown(self):
        """Section 2: Subject-Specific Breakdown"""
        self.log(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 80}{Colors.END}")
        self.log(f"{Colors.BOLD}{Colors.CYAN}2. SUBJECT-SPECIFIC BREAKDOWN{Colors.END}")
        self.log(f"{Colors.BOLD}{Colors.BLUE}{'=' * 80}{Colors.END}\n")

        cursor = self.conn.cursor()

        # Get all subjects
        cursor.execute("""
            SELECT
                subject,
                COUNT(*) as total_cards,
                SUM(CASE WHEN date(due_date) <= date('now') THEN 1 ELSE 0 END) as due_cards,
                AVG(ease_factor) as avg_ease,
                SUM(CASE WHEN ease_factor >= 2.5 AND interval_days >= 15 THEN 1 ELSE 0 END) as mastered,
                SUM(CASE WHEN ease_factor < 2.0 THEN 1 ELSE 0 END) as struggling,
                SUM(CASE WHEN ease_factor >= 2.0 AND ease_factor < 2.5 THEN 1 ELSE 0 END) as learning,
                SUM(CASE WHEN ease_factor >= 2.5 AND ease_factor < 3.0 THEN 1 ELSE 0 END) as proficient,
                SUM(CASE WHEN ease_factor >= 3.0 THEN 1 ELSE 0 END) as expert
            FROM cards
            GROUP BY subject
            ORDER BY due_cards DESC, avg_ease ASC
        """)

        subjects = cursor.fetchall()

        if not subjects:
            self.log(f"  {Colors.YELLOW}No subjects found in database{Colors.END}")
            return

        weak_subjects = []

        for row in subjects:
            subject = row['subject']
            total = row['total_cards']
            due = row['due_cards']
            avg_ease = row['avg_ease'] or 0
            mastered = row['mastered']
            mastery_pct = (mastered / total * 100) if total > 0 else 0

            # Color code by ease factor
            if avg_ease < 2.0:
                ease_color = Colors.RED
                status = "STRUGGLING"
            elif avg_ease < 2.3:
                ease_color = Colors.YELLOW
                status = "NEEDS WORK"
                weak_subjects.append((subject, avg_ease, due))
            elif avg_ease < 2.5:
                ease_color = Colors.CYAN
                status = "LEARNING"
            else:
                ease_color = Colors.GREEN
                status = "STRONG"

            self.log(f"{Colors.BOLD}{Colors.UNDERLINE}{subject}{Colors.END}")
            self.log(f"  Status: {ease_color}{status}{Colors.END}")
            self.log(f"  Total Cards: {total:,} | Due: {due:,} | Mastered: {mastered} ({mastery_pct:.1f}%)")
            self.log(f"  Average Ease Factor: {ease_color}{avg_ease:.2f}{Colors.END}")

            # Mastery distribution
            struggling = row['struggling']
            learning = row['learning']
            proficient = row['proficient']
            expert = row['expert']

            self.log(f"  Distribution:")
            if struggling > 0:
                self.log(f"    {Colors.RED}● Struggling (ease < 2.0): {struggling}{Colors.END}")
            if learning > 0:
                self.log(f"    {Colors.YELLOW}● Learning (2.0-2.5): {learning}{Colors.END}")
            if proficient > 0:
                self.log(f"    {Colors.CYAN}● Proficient (2.5-3.0): {proficient}{Colors.END}")
            if expert > 0:
                self.log(f"    {Colors.GREEN}● Mastered (≥ 3.0): {expert}{Colors.END}")

            self.log("")

        # Weak subjects summary
        if weak_subjects:
            self.log(f"\n{Colors.BOLD}{Colors.RED}⚠️  SUBJECTS NEEDING ATTENTION:{Colors.END}")
            for subject, ease, due in weak_subjects:
                self.log(f"  {Colors.RED}• {subject}: Ease {ease:.2f}, {due} cards due{Colors.END}")

    def spaced_repetition_health(self):
        """Section 3: Spaced Repetition Health"""
        self.log(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 80}{Colors.END}")
        self.log(f"{Colors.BOLD}{Colors.CYAN}3. SPACED REPETITION HEALTH{Colors.END}")
        self.log(f"{Colors.BOLD}{Colors.BLUE}{'=' * 80}{Colors.END}\n")

        cursor = self.conn.cursor()

        # Interval distribution
        self.log(f"{Colors.BOLD}Interval Distribution:{Colors.END}\n")

        intervals = [
            ("New Cards (1 day)", 1, 1),
            ("Early Learning (2-5 days)", 2, 5),
            ("Reinforcing (6-14 days)", 6, 14),
            ("Solidifying (15-30 days)", 15, 30),
            ("Mastered (30+ days)", 31, 9999)
        ]

        for label, min_interval, max_interval in intervals:
            cursor.execute("""
                SELECT COUNT(*) as count FROM cards
                WHERE interval_days >= ? AND interval_days <= ?
            """, (min_interval, max_interval))
            count = cursor.fetchone()['count']

            # Create simple bar chart
            bar_length = min(count // 10, 40)
            bar = "█" * bar_length
            self.log(f"  {label:.<35} {count:>4} {Colors.CYAN}{bar}{Colors.END}")

        # Ease factor distribution
        self.log(f"\n{Colors.BOLD}Ease Factor Distribution:{Colors.END}\n")

        ease_buckets = [
            ("Very Difficult (< 1.5)", 0, 1.5, Colors.RED),
            ("Difficult (1.5-2.0)", 1.5, 2.0, Colors.RED),
            ("Moderate (2.0-2.5)", 2.0, 2.5, Colors.YELLOW),
            ("Good (2.5-3.0)", 2.5, 3.0, Colors.CYAN),
            ("Easy (3.0-3.5)", 3.0, 3.5, Colors.GREEN),
            ("Very Easy (≥ 3.5)", 3.5, 10.0, Colors.GREEN)
        ]

        for label, min_ease, max_ease, color in ease_buckets:
            cursor.execute("""
                SELECT COUNT(*) as count FROM cards
                WHERE ease_factor >= ? AND ease_factor < ?
            """, (min_ease, max_ease))
            count = cursor.fetchone()['count']

            bar_length = min(count // 10, 40)
            bar = "█" * bar_length
            self.log(f"  {label:.<35} {count:>4} {color}{bar}{Colors.END}")

        # Overdue cards
        cursor.execute("""
            SELECT COUNT(*) as count FROM cards
            WHERE date(due_date) < date('now')
        """)
        overdue = cursor.fetchone()['count']

        if overdue > 0:
            self.log(f"\n{Colors.BOLD}{Colors.RED}⚠️  Overdue Cards: {overdue:,}{Colors.END}")
        else:
            self.log(f"\n{Colors.BOLD}{Colors.GREEN}✓ No overdue cards!{Colors.END}")

        # 7-day forecast
        self.log(f"\n{Colors.BOLD}7-Day Review Forecast:{Colors.END}\n")

        for i in range(7):
            target_date = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
            day_name = (datetime.now() + timedelta(days=i)).strftime("%A")

            cursor.execute("""
                SELECT COUNT(*) as count FROM cards
                WHERE date(due_date) = date(?)
            """, (target_date,))
            count = cursor.fetchone()['count']

            bar_length = min(count // 5, 50)
            bar = "█" * bar_length

            day_label = "TODAY" if i == 0 else day_name
            color = Colors.RED if count > 100 else Colors.YELLOW if count > 50 else Colors.CYAN

            self.log(f"  {day_label:.<20} {target_date}  {color}{count:>4} cards{Colors.END} {bar}")

    def constitutional_evidence_deep_dive(self):
        """Section 4: Constitutional Law & Evidence Deep Dive"""
        self.log(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 80}{Colors.END}")
        self.log(f"{Colors.BOLD}{Colors.CYAN}4. CONSTITUTIONAL LAW & EVIDENCE DEEP DIVE{Colors.END}")
        self.log(f"{Colors.BOLD}{Colors.BLUE}{'=' * 80}{Colors.END}\n")

        cursor = self.conn.cursor()

        critical_subjects = ["Constitutional Law", "Evidence"]

        for subject in critical_subjects:
            self.log(f"{Colors.BOLD}{Colors.UNDERLINE}{subject.upper()}{Colors.END}\n")

            # Overall stats
            cursor.execute("""
                SELECT
                    COUNT(*) as total,
                    SUM(CASE WHEN date(due_date) <= date('now') THEN 1 ELSE 0 END) as due,
                    AVG(ease_factor) as avg_ease,
                    SUM(CASE WHEN ease_factor >= 2.5 AND interval_days >= 15 THEN 1 ELSE 0 END) as mastered
                FROM cards
                WHERE subject = ?
            """, (subject,))

            row = cursor.fetchone()
            if not row or row['total'] == 0:
                self.log(f"  {Colors.YELLOW}No cards found for {subject}{Colors.END}\n")
                continue

            total = row['total']
            due = row['due']
            avg_ease = row['avg_ease'] or 0
            mastered = row['mastered']
            mastery_pct = (mastered / total * 100) if total > 0 else 0

            self.log(f"  Total Cards: {Colors.BOLD}{total:,}{Colors.END}")
            self.log(f"  Due Cards: {Colors.BOLD}{due:,}{Colors.END}")
            self.log(f"  Average Ease: {Colors.BOLD}{avg_ease:.2f}{Colors.END}")
            self.log(f"  Mastery: {Colors.BOLD}{mastered} ({mastery_pct:.1f}%){Colors.END}")

            # Topic breakdown
            self.log(f"\n  {Colors.BOLD}Topics:{Colors.END}\n")

            cursor.execute("""
                SELECT
                    topic,
                    COUNT(*) as count,
                    AVG(ease_factor) as avg_ease,
                    SUM(CASE WHEN date(due_date) <= date('now') THEN 1 ELSE 0 END) as due,
                    SUM(CASE WHEN date(due_date) < date('now') THEN 1 ELSE 0 END) as overdue
                FROM cards
                WHERE subject = ?
                GROUP BY topic
                ORDER BY due DESC, avg_ease ASC
            """, (subject,))

            topics = cursor.fetchall()

            for topic_row in topics[:15]:  # Limit to top 15 topics
                topic = topic_row['topic']
                count = topic_row['count']
                topic_ease = topic_row['avg_ease'] or 0
                topic_due = topic_row['due']
                topic_overdue = topic_row['overdue']

                # Color code by urgency
                if topic_overdue > 0:
                    color = Colors.RED
                    status = "OVERDUE"
                elif topic_ease < 2.3:
                    color = Colors.YELLOW
                    status = "NEEDS REVIEW"
                elif topic_due > 0:
                    color = Colors.CYAN
                    status = "DUE"
                else:
                    color = Colors.GREEN
                    status = "ON TRACK"

                self.log(f"    {color}• {topic}{Colors.END}")
                self.log(f"      Cards: {count} | Due: {topic_due} | Ease: {topic_ease:.2f} | Status: {color}{status}{Colors.END}")

            self.log("")

    def study_recommendations(self):
        """Section 5: Study Recommendations"""
        self.log(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 80}{Colors.END}")
        self.log(f"{Colors.BOLD}{Colors.CYAN}5. STUDY RECOMMENDATIONS{Colors.END}")
        self.log(f"{Colors.BOLD}{Colors.BLUE}{'=' * 80}{Colors.END}\n")

        cursor = self.conn.cursor()

        # Get current state
        cursor.execute("SELECT COUNT(*) as count FROM cards WHERE date(due_date) <= date('now')")
        due_cards = cursor.fetchone()['count']

        cursor.execute("SELECT COUNT(*) as count FROM cards")
        total_cards = cursor.fetchone()['count']

        cursor.execute("SELECT COUNT(*) as count FROM performance")
        has_reviews = cursor.fetchone()['count'] > 0

        self.log(f"{Colors.BOLD}Current State:{Colors.END}\n")
        self.log(f"  Total Cards in System: {Colors.BOLD}{total_cards:,}{Colors.END}")
        self.log(f"  Cards Due Now: {Colors.BOLD}{due_cards:,}{Colors.END}")

        if not has_reviews:
            self.log(f"\n{Colors.BOLD}{Colors.YELLOW}🎯 FIRST-TIME SETUP RECOMMENDATIONS:{Colors.END}\n")

            # Suggested daily targets
            daily_targets = [
                (30, "Conservative", "Lower daily commitment, longer timeline"),
                (50, "Balanced", "Recommended for most students"),
                (75, "Aggressive", "For dedicated full-time study")
            ]

            self.log(f"{Colors.BOLD}Suggested Daily Review Targets:{Colors.END}\n")

            for target, level, description in daily_targets:
                days_to_complete = due_cards // target
                self.log(f"  {Colors.BOLD}{level} ({target} cards/day):{Colors.END}")
                self.log(f"    • {description}")
                self.log(f"    • Time to first pass: ~{days_to_complete} days")
                self.log(f"    • Estimated daily time: ~{target * 2}-{target * 3} minutes")
                self.log("")

            # Priority subjects
            self.log(f"{Colors.BOLD}Priority Study Order:{Colors.END}\n")

            cursor.execute("""
                SELECT subject, COUNT(*) as count
                FROM cards
                GROUP BY subject
                ORDER BY
                    CASE
                        WHEN subject IN ('Constitutional Law', 'Evidence', 'Contracts', 'Torts', 'Criminal Law', 'Civil Procedure', 'Real Property') THEN 1
                        ELSE 2
                    END,
                    count DESC
            """)

            subjects = cursor.fetchall()
            mbe_subjects = ['Constitutional Law', 'Evidence', 'Contracts', 'Torts',
                          'Criminal Law', 'Civil Procedure', 'Real Property']

            self.log(f"  {Colors.BOLD}{Colors.GREEN}Phase 1: MBE Core Subjects{Colors.END}")
            for row in subjects:
                if row['subject'] in mbe_subjects:
                    self.log(f"    • {row['subject']} ({row['count']} cards)")

            self.log(f"\n  {Colors.BOLD}{Colors.CYAN}Phase 2: Essay-Only Subjects{Colors.END}")
            for row in subjects:
                if row['subject'] not in mbe_subjects:
                    self.log(f"    • {row['subject']} ({row['count']} cards)")

            # Optimal schedule
            self.log(f"\n{Colors.BOLD}Optimal Study Schedule:{Colors.END}\n")
            self.log(f"  {Colors.GREEN}✓{Colors.END} Study at the same time daily (consistency is key)")
            self.log(f"  {Colors.GREEN}✓{Colors.END} Morning sessions typically show better retention")
            self.log(f"  {Colors.GREEN}✓{Colors.END} Take breaks every 25-30 minutes (Pomodoro technique)")
            self.log(f"  {Colors.GREEN}✓{Colors.END} Review in multiple shorter sessions vs one long session")
            self.log(f"  {Colors.GREEN}✓{Colors.END} Don't skip days - consistency beats intensity")

            self.log(f"\n{Colors.BOLD}Expected Timeline:{Colors.END}\n")
            self.log(f"  • Week 1-2: Initial learning (cards will feel hard)")
            self.log(f"  • Week 3-4: Patterns emerge (concepts start connecting)")
            self.log(f"  • Week 5-6: Confidence builds (review intervals lengthen)")
            self.log(f"  • Week 7+: Mastery phase (most cards at long intervals)")

        else:
            # Performance-based recommendations
            self.log(f"\n{Colors.BOLD}{Colors.GREEN}📈 PERFORMANCE-BASED RECOMMENDATIONS:{Colors.END}\n")

            # Get weak subjects
            cursor.execute("""
                SELECT subject, AVG(ease_factor) as avg_ease, COUNT(*) as due_count
                FROM cards
                WHERE date(due_date) <= date('now')
                GROUP BY subject
                HAVING avg_ease < 2.3
                ORDER BY avg_ease ASC
                LIMIT 3
            """)

            weak_subjects = cursor.fetchall()

            if weak_subjects:
                self.log(f"{Colors.BOLD}Focus Areas (Lowest Ease Factor):{Colors.END}\n")
                for row in weak_subjects:
                    self.log(f"  {Colors.RED}• {row['subject']}{Colors.END}")
                    self.log(f"    Ease Factor: {row['avg_ease']:.2f} | Due Cards: {row['due_count']}")

            # Get recent accuracy
            cursor.execute("""
                SELECT AVG(CASE WHEN quality >= 3 THEN 1.0 ELSE 0.0 END) as accuracy
                FROM performance
                WHERE date(review_date) >= date('now', '-7 days')
            """)
            recent_accuracy = cursor.fetchone()['accuracy']

            if recent_accuracy and recent_accuracy < 0.75:
                self.log(f"\n{Colors.BOLD}{Colors.YELLOW}⚠️  Recent Accuracy Below Target:{Colors.END}")
                self.log(f"  Current: {recent_accuracy:.1%} | Target: 75%+")
                self.log(f"  {Colors.CYAN}→{Colors.END} Consider reducing daily card volume")
                self.log(f"  {Colors.CYAN}→{Colors.END} Focus on understanding, not memorization")
                self.log(f"  {Colors.CYAN}→{Colors.END} Review explanations thoroughly before rating")

        # General tips
        self.log(f"\n{Colors.BOLD}General Study Tips:{Colors.END}\n")
        self.log(f"  {Colors.CYAN}→{Colors.END} Be honest with your ratings (quality 0-5)")
        self.log(f"  {Colors.CYAN}→{Colors.END} Quality 3+ means you could explain it to someone")
        self.log(f"  {Colors.CYAN}→{Colors.END} Don't be afraid to rate yourself low - it helps the algorithm")
        self.log(f"  {Colors.CYAN}→{Colors.END} If you're consistently guessing, review the underlying concepts")
        self.log(f"  {Colors.CYAN}→{Colors.END} Use mnemonic devices for lists and elements")

    def generate_full_report(self):
        """Generate complete analytics report"""
        print_header("IOWA BAR PREP - ADAPTIVE LEARNING ANALYTICS")

        self.overall_performance_report()
        self.subject_specific_breakdown()
        self.spaced_repetition_health()
        self.constitutional_evidence_deep_dive()
        self.study_recommendations()

        # Footer
        self.log(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 80}{Colors.END}")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log(f"{Colors.BOLD}Report Generated: {timestamp}{Colors.END}")
        self.log(f"{Colors.BOLD}{Colors.BLUE}{'=' * 80}{Colors.END}\n")

    def save_report(self, filename: str = "analytics_adaptive_report.txt"):
        """Save report to file"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.report_lines))
        print(f"{Colors.GREEN}✓ Report saved to: {filename}{Colors.END}\n")

def main():
    """Main entry point"""
    import sys

    db_path = "iowa_bar_prep.db"

    # Check if database exists
    import os
    if not os.path.exists(db_path):
        print(f"{Colors.RED}Error: Database '{db_path}' not found.{Colors.END}")
        print(f"\n{Colors.YELLOW}Creating database and initializing with bar prep concepts...{Colors.END}\n")

        # Initialize database with concepts
        try:
            from adaptive_learning_system import populate_from_bar_tutor
            populate_from_bar_tutor()
            print(f"{Colors.GREEN}✓ Database initialized successfully!{Colors.END}\n")
        except Exception as e:
            print(f"{Colors.RED}Error initializing database: {e}{Colors.END}")
            print(f"{Colors.YELLOW}Run: python adaptive_learning_system.py{Colors.END}")
            sys.exit(1)

    # Generate analytics
    analytics = BarPrepAnalytics(db_path)
    analytics.generate_full_report()
    analytics.save_report()
    analytics.system.close()

if __name__ == "__main__":
    main()
