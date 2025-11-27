/**
 * Spaced Repetition Algorithm - SM-2 Implementation
 *
 * This implements a simplified version of the SuperMemo SM-2 algorithm
 * for optimal review scheduling of flashcards.
 *
 * Reference: https://www.supermemo.com/en/archives1990-2015/english/ol/sm2
 */

/**
 * Quality ratings (user confidence):
 * 0 - Complete blackout
 * 1 - Incorrect, but familiar
 * 2 - Incorrect, but easy to recall correct answer
 * 3 - Correct, but difficult
 * 4 - Correct, with hesitation
 * 5 - Perfect recall
 */

export class SM2Algorithm {
  constructor() {
    // Default easiness factor (2.5 is standard starting point)
    this.DEFAULT_EF = 2.5;
    this.MIN_EF = 1.3;
  }

  /**
   * Calculate next review interval and updated easiness factor
   *
   * @param {number} quality - User's confidence rating (0-5)
   * @param {number} repetitions - Number of consecutive correct responses
   * @param {number} previousInterval - Previous interval in days
   * @param {number} easinessFactor - Current easiness factor
   * @returns {Object} { interval, repetitions, easinessFactor }
   */
  calculate(quality, repetitions = 0, previousInterval = 1, easinessFactor = this.DEFAULT_EF) {
    let newRepetitions = repetitions;
    let newInterval = previousInterval;
    let newEF = easinessFactor;

    // Update easiness factor based on quality
    newEF = this.updateEasinessFactor(easinessFactor, quality);

    if (quality >= 3) {
      // Correct response
      newRepetitions++;

      if (newRepetitions === 1) {
        newInterval = 1; // First review after 1 day
      } else if (newRepetitions === 2) {
        newInterval = 6; // Second review after 6 days
      } else {
        newInterval = Math.round(previousInterval * newEF);
      }
    } else {
      // Incorrect response - reset repetitions and interval
      newRepetitions = 0;
      newInterval = 1;
    }

    return {
      interval: newInterval,
      repetitions: newRepetitions,
      easinessFactor: newEF
    };
  }

  /**
   * Update easiness factor based on quality of recall
   *
   * @param {number} currentEF - Current easiness factor
   * @param {number} quality - Quality rating (0-5)
   * @returns {number} New easiness factor
   */
  updateEasinessFactor(currentEF, quality) {
    // SM-2 formula: EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
    const newEF = currentEF + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02));

    // Enforce minimum easiness factor
    return Math.max(newEF, this.MIN_EF);
  }

  /**
   * Get human-readable interval description
   *
   * @param {number} days - Number of days
   * @returns {string} Description of interval
   */
  getIntervalDescription(days) {
    if (days < 1) return "Less than 1 day";
    if (days === 1) return "1 day";
    if (days < 7) return `${days} days`;
    if (days < 30) {
      const weeks = Math.floor(days / 7);
      return `${weeks} week${weeks > 1 ? 's' : ''}`;
    }
    const months = Math.floor(days / 30);
    return `${months} month${months > 1 ? 's' : ''}`;
  }

  /**
   * Calculate next review date
   *
   * @param {number} interval - Interval in days
   * @param {Date} lastReview - Last review date (defaults to now)
   * @returns {Date} Next review date
   */
  getNextReviewDate(interval, lastReview = new Date()) {
    const nextDate = new Date(lastReview);
    nextDate.setDate(nextDate.getDate() + interval);
    return nextDate;
  }

  /**
   * Check if card is due for review
   *
   * @param {Date} nextReviewDate - Scheduled next review date
   * @param {Date} currentDate - Current date (defaults to now)
   * @returns {boolean} True if card is due
   */
  isDue(nextReviewDate, currentDate = new Date()) {
    return currentDate >= nextReviewDate;
  }

  /**
   * Get recommended daily study count
   * Based on forgetting curve and optimal retention
   *
   * @param {number} totalCards - Total cards in deck
   * @param {number} targetDays - Days until exam
   * @returns {number} Recommended cards per day
   */
  getRecommendedDailyCount(totalCards, targetDays) {
    // Account for multiple reviews per card
    const estimatedReviews = 3.5; // Average reviews needed per card
    const totalReviews = totalCards * estimatedReviews;

    // Add 20% buffer for difficult cards
    const withBuffer = totalReviews * 1.2;

    return Math.ceil(withBuffer / targetDays);
  }
}

/**
 * Card Scheduler - Manages due dates and priorities
 */
export class CardScheduler {
  constructor() {
    this.sm2 = new SM2Algorithm();
  }

  /**
   * Get cards due for review
   *
   * @param {Array} cards - Array of card objects with review data
   * @param {Date} currentDate - Current date
   * @returns {Array} Cards that are due for review
   */
  getDueCards(cards, currentDate = new Date()) {
    return cards.filter(card => {
      if (!card.nextReviewDate) return true; // New cards are always due
      return this.sm2.isDue(new Date(card.nextReviewDate), currentDate);
    });
  }

  /**
   * Sort cards by priority (overdue first, then by difficulty)
   *
   * @param {Array} cards - Array of card objects
   * @returns {Array} Sorted cards
   */
  prioritizeCards(cards) {
    return cards.sort((a, b) => {
      // New cards first
      if (!a.nextReviewDate && b.nextReviewDate) return -1;
      if (a.nextReviewDate && !b.nextReviewDate) return 1;

      // Then by how overdue
      const now = new Date();
      const aOverdue = a.nextReviewDate ? now - new Date(a.nextReviewDate) : 0;
      const bOverdue = b.nextReviewDate ? now - new Date(b.nextReviewDate) : 0;

      if (aOverdue !== bOverdue) return bOverdue - aOverdue;

      // Finally by easiness factor (harder cards first)
      return (a.easinessFactor || 2.5) - (b.easinessFactor || 2.5);
    });
  }

  /**
   * Update card after review
   *
   * @param {Object} card - Card object
   * @param {number} quality - Quality rating
   * @returns {Object} Updated card object
   */
  updateCard(card, quality) {
    const result = this.sm2.calculate(
      quality,
      card.repetitions || 0,
      card.interval || 1,
      card.easinessFactor || 2.5
    );

    return {
      ...card,
      interval: result.interval,
      repetitions: result.repetitions,
      easinessFactor: result.easinessFactor,
      nextReviewDate: this.sm2.getNextReviewDate(result.interval),
      lastReviewDate: new Date(),
      lastQuality: quality
    };
  }

  /**
   * Get study statistics
   *
   * @param {Array} cards - Array of cards with review history
   * @returns {Object} Statistics object
   */
  getStatistics(cards) {
    const now = new Date();
    const dueCards = this.getDueCards(cards, now);

    const reviewedCards = cards.filter(c => c.lastReviewDate);
    const matureCards = reviewedCards.filter(c => c.interval >= 21);
    const youngCards = reviewedCards.filter(c => c.interval < 21 && c.interval > 0);
    const newCards = cards.filter(c => !c.lastReviewDate);

    const avgEasiness = reviewedCards.length > 0
      ? reviewedCards.reduce((sum, c) => sum + (c.easinessFactor || 2.5), 0) / reviewedCards.length
      : 2.5;

    return {
      total: cards.length,
      new: newCards.length,
      young: youngCards.length,
      mature: matureCards.length,
      due: dueCards.length,
      averageEasiness: avgEasiness.toFixed(2),
      retention: reviewedCards.length > 0
        ? ((reviewedCards.filter(c => (c.lastQuality || 0) >= 3).length / reviewedCards.length) * 100).toFixed(1)
        : 0
    };
  }
}

/**
 * Streak Calculator - Tracks daily study streaks
 */
export class StreakCalculator {
  /**
   * Calculate current streak from review history
   *
   * @param {Array} reviewDates - Array of review date strings
   * @returns {Object} { currentStreak, longestStreak }
   */
  calculateStreak(reviewDates) {
    if (reviewDates.length === 0) {
      return { currentStreak: 0, longestStreak: 0 };
    }

    // Convert to dates and sort descending
    const dates = reviewDates
      .map(d => new Date(d).toDateString())
      .filter((v, i, a) => a.indexOf(v) === i) // Unique dates only
      .sort((a, b) => new Date(b) - new Date(a));

    let currentStreak = 0;
    let longestStreak = 0;
    let tempStreak = 0;

    const today = new Date().toDateString();
    const yesterday = new Date(Date.now() - 86400000).toDateString();

    // Calculate current streak
    if (dates[0] === today || dates[0] === yesterday) {
      let checkDate = new Date();
      for (const dateStr of dates) {
        if (dateStr === checkDate.toDateString()) {
          currentStreak++;
          checkDate.setDate(checkDate.getDate() - 1);
        } else if (dateStr === checkDate.toDateString()) {
          // Continue if same date
          continue;
        } else {
          break;
        }
      }
    }

    // Calculate longest streak
    let prevDate = null;
    for (const dateStr of dates.reverse()) {
      const date = new Date(dateStr);

      if (!prevDate) {
        tempStreak = 1;
      } else {
        const dayDiff = Math.floor((date - prevDate) / 86400000);
        if (dayDiff === 1) {
          tempStreak++;
        } else {
          longestStreak = Math.max(longestStreak, tempStreak);
          tempStreak = 1;
        }
      }

      prevDate = date;
    }
    longestStreak = Math.max(longestStreak, tempStreak);

    return { currentStreak, longestStreak };
  }
}

/**
 * Progress Analyzer - Analyzes learning patterns
 */
export class ProgressAnalyzer {
  /**
   * Identify weak subjects
   *
   * @param {Object} subjectStats - Object with subject performance data
   * @param {number} threshold - Accuracy threshold (default 60%)
   * @returns {Array} List of weak subjects
   */
  identifyWeakSubjects(subjectStats, threshold = 60) {
    return Object.entries(subjectStats)
      .filter(([_, stats]) => stats.avg < threshold)
      .sort((a, b) => a[1].avg - b[1].avg)
      .map(([subject, stats]) => ({
        subject,
        accuracy: stats.avg,
        totalCards: stats.total,
        gap: threshold - stats.avg
      }));
  }

  /**
   * Predict exam readiness
   *
   * @param {Object} stats - Overall statistics
   * @param {number} daysUntilExam - Days remaining until exam
   * @returns {Object} Readiness assessment
   */
  predictReadiness(stats, daysUntilExam) {
    const { total, mature, retention } = stats;

    const maturityRate = total > 0 ? (mature / total) * 100 : 0;
    const retentionRate = parseFloat(retention);

    let readiness = 'Not Ready';
    let confidence = 0;

    if (maturityRate >= 70 && retentionRate >= 80) {
      readiness = 'Excellent';
      confidence = 95;
    } else if (maturityRate >= 50 && retentionRate >= 70) {
      readiness = 'Good';
      confidence = 75;
    } else if (maturityRate >= 30 && retentionRate >= 60) {
      readiness = 'Fair';
      confidence = 55;
    } else {
      readiness = 'Needs Improvement';
      confidence = 30;
    }

    return {
      readiness,
      confidence,
      maturityRate: maturityRate.toFixed(1),
      retentionRate,
      daysRemaining: daysUntilExam,
      recommendedDailyCards: Math.ceil((total - mature) / Math.max(daysUntilExam, 1))
    };
  }

  /**
   * Generate study recommendations
   *
   * @param {Object} stats - Study statistics
   * @param {Array} weakSubjects - List of weak subjects
   * @returns {Array} List of recommendations
   */
  getRecommendations(stats, weakSubjects) {
    const recommendations = [];

    if (stats.due > 50) {
      recommendations.push({
        priority: 'high',
        type: 'workload',
        message: `You have ${stats.due} cards due for review. Consider increasing daily study time.`
      });
    }

    if (parseFloat(stats.retention) < 70) {
      recommendations.push({
        priority: 'high',
        type: 'retention',
        message: 'Retention rate is below 70%. Slow down and focus on understanding over speed.'
      });
    }

    if (weakSubjects.length > 0) {
      recommendations.push({
        priority: 'medium',
        type: 'subjects',
        message: `Focus on weak subjects: ${weakSubjects.slice(0, 3).map(s => s.subject).join(', ')}`
      });
    }

    if (parseFloat(stats.averageEasiness) < 2.0) {
      recommendations.push({
        priority: 'medium',
        type: 'difficulty',
        message: 'Many cards are marked difficult. Consider supplemental resources or tutoring.'
      });
    }

    if (stats.new > stats.young + stats.mature) {
      recommendations.push({
        priority: 'low',
        type: 'new_cards',
        message: 'Balance new card introduction with reviewing existing cards.'
      });
    }

    return recommendations;
  }
}

// Export instances for easy use
export const sm2Algorithm = new SM2Algorithm();
export const cardScheduler = new CardScheduler();
export const streakCalculator = new StreakCalculator();
export const progressAnalyzer = new ProgressAnalyzer();
