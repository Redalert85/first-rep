import React, { useEffect, useMemo, useRef, useState } from "react";
import {
  Activity,
  AlertCircle,
  Award,
  BarChart2,
  Bookmark,
  BookmarkCheck,
  BookOpen,
  Brain,
  Calendar,
  CheckCircle,
  ChevronDown,
  ChevronRight,
  ChevronUp,
  Clock,
  Download,
  Eye,
  FileText,
  Flame,
  Gavel,
  HelpCircle,
  MessageSquare,
  MoreVertical,
  PieChart,
  RefreshCw,
  RotateCcw,
  Settings,
  Share2,
  ExternalLink,
  Target,
  TrendingDown,
  TrendingUp,
  Star,
  Zap,
  ThumbsDown,
} from "lucide-react";
import { callGemini, useAbortController } from "./geminiClient";

const StorageKeys = {
  USER_STATS: "first_rep_user_stats",
  CARD_HISTORY: "first_rep_card_history",
  STUDY_SESSIONS: "first_rep_study_sessions",
  BOOKMARKS: "first_rep_bookmarks",
  PREFERENCES: "first_rep_preferences",
  ACHIEVEMENTS: "first_rep_achievements",
  SAVED_PLANS: "saved_plans",
  HYPO_HISTORY: "hypo_history",
};

const colorPalette = {
  amber: "bg-amber-50 text-amber-700 border-amber-100",
  emerald: "bg-emerald-50 text-emerald-700 border-emerald-100",
  blue: "bg-blue-50 text-blue-700 border-blue-100",
  purple: "bg-purple-50 text-purple-700 border-purple-100",
  orange: "bg-orange-50 text-orange-700 border-orange-100",
  red: "bg-red-50 text-red-700 border-red-100",
};

const navLinks = [
  { id: "planner", label: "Syllabus", icon: Calendar },
  { id: "hypo", label: "Issue Spotter", icon: Gavel },
  { id: "demo", label: "Flashcards", icon: Brain },
  { id: "analytics", label: "Analytics", icon: BarChart2 },
];

const useLocalStorage = (key, initialValue) => {
  const [storedValue, setStoredValue] = useState(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error(error);
      return initialValue;
    }
  });

  const setValue = (value) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.error(error);
    }
  };

  return [storedValue, setValue];
};

const HeroBadge = () => (
  <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-50 border border-amber-200 text-amber-800 text-xs font-bold uppercase tracking-wide">
    <span className="w-2 h-2 rounded-full bg-amber-600 animate-pulse" />
    Updated for July 2025 Bar
  </div>
);

const FeatureCard = ({ icon, title, description, color }) => (
  <div className="bg-white p-6 rounded-xl border border-stone-200 shadow-sm hover:shadow-md transition-shadow">
    <div className={`w-12 h-12 rounded-lg ${colorPalette[color]} border flex items-center justify-center mb-4`}>
      {icon}
    </div>
    <h3 className="text-lg font-bold text-stone-900 mb-2">{title}</h3>
    <p className="text-sm text-stone-600 leading-relaxed">{description}</p>
  </div>
);

const SectionHeader = ({ icon: Icon, title, description, accent = "text-stone-500" }) => (
  <div className="mb-10 flex flex-col md:flex-row md:items-end justify-between gap-4">
    <div>
      <h2 className="text-3xl font-serif font-medium text-stone-900 flex items-center gap-3">
        <Icon className="w-8 h-8 text-amber-700" />
        {title}
      </h2>
      {description && <p className={`${accent} mt-2 max-w-2xl`}>{description}</p>}
    </div>
  </div>
);

const App = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [userStats, setUserStats] = useLocalStorage(StorageKeys.USER_STATS, {
    totalCards: 0,
    masteredCards: 0,
    currentStreak: 0,
    longestStreak: 0,
    totalStudyTime: 0,
    lastStudyDate: null,
  });
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => setIsScrolled(window.scrollY > 20);
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const navigate = (section) => {
    setMobileMenuOpen(false);
    const element = document.getElementById(section);
    if (element) {
      element.scrollIntoView({ behavior: "smooth" });
    } else {
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  };

  const heroStats = [
    { label: "Cards Studied", value: userStats.totalCards || 0, tone: "text-amber-700" },
    { label: "Mastered", value: userStats.masteredCards || 0, tone: "text-emerald-600" },
    { label: "Day Streak", value: `${userStats.currentStreak || 0}` },
  ];

  return (
    <div className="min-h-screen bg-stone-50 font-sans text-stone-900 selection:bg-amber-100 selection:text-amber-900">
      <Navigation
        isScrolled={isScrolled}
        navigate={navigate}
        mobileMenuOpen={mobileMenuOpen}
        setMobileMenuOpen={setMobileMenuOpen}
        userStats={userStats}
      />

      <Hero navigate={navigate} stats={heroStats} />
      <Features />

      <section id="planner" className="py-24 bg-stone-50 border-y border-stone-200">
        <div className="max-w-6xl mx-auto px-6">
          <SectionHeader
            icon={Calendar}
            title="AI Syllabus Architect"
            description="Generate a high-fidelity study schedule tailored to your learning modality and timeline."
          />
          <EnhancedAIPlanner />
        </div>
      </section>

      <section id="hypo" className="py-24 bg-stone-900 text-stone-200">
        <div className="max-w-6xl mx-auto px-6">
          <SectionHeader
            icon={Gavel}
            title="Fact Pattern Generator"
            description="Apply black letter law to generated scenarios. Select a subject, read the facts, and spot the issues before revealing the model analysis."
            accent="text-stone-400"
          />
          <EnhancedHypotheticalEngine />
        </div>
      </section>

      <section id="demo" className="py-24 bg-stone-100">
        <div className="max-w-6xl mx-auto px-6">
          <div className="mb-10 text-center">
            <h2 className="text-3xl font-serif font-medium text-stone-900">Black Letter Law Drills</h2>
            <p className="text-stone-500 mt-2">Spaced repetition interface with integrated Socratic Chat.</p>
          </div>
          <EnhancedMiniTutor userStats={userStats} setUserStats={setUserStats} />
        </div>
      </section>

      <section id="analytics" className="py-24 bg-white">
        <div className="max-w-6xl mx-auto px-6">
          <SectionHeader
            icon={BarChart2}
            title="Performance Analytics"
            description="Track your progress with detailed metrics and insights."
          />
          <AnalyticsDashboard userStats={userStats} />
        </div>
      </section>

      <Footer navigate={navigate} />
    </div>
  );
};

const Navigation = ({ isScrolled, navigate, mobileMenuOpen, setMobileMenuOpen, userStats }) => (
  <nav
    className={`fixed w-full z-50 transition-all duration-300 ${
      isScrolled ? "bg-white/95 backdrop-blur-md shadow-sm py-3 border-b border-stone-200" : "bg-transparent py-6"
    }`}
    aria-label="Primary"
  >
    <div className="max-w-7xl mx-auto px-6 flex justify-between items-center">
      <button
        className="flex items-center gap-2 cursor-pointer"
        onClick={() => navigate("home")}
        aria-label="Return to home"
      >
        <div className="w-8 h-8 bg-gradient-to-br from-amber-700 to-amber-600 rounded-lg flex items-center justify-center text-white font-bold font-serif shadow-md">
          FR
        </div>
        <span className="text-xl font-bold tracking-tight text-stone-800">First-Rep</span>
        {userStats.currentStreak > 0 && (
          <span className="hidden md:flex items-center gap-1 ml-2 px-2 py-1 bg-orange-50 rounded-full text-xs font-bold text-orange-600">
            <Flame className="w-3 h-3" /> {userStats.currentStreak}
          </span>
        )}
      </button>

      <div className="hidden md:flex items-center gap-6 text-sm font-medium text-stone-600">
        {navLinks.map(({ id, label, icon: Icon }) => (
          <button key={id} onClick={() => navigate(id)} className="hover:text-amber-700 transition-colors flex items-center gap-1.5">
            <Icon className="w-4 h-4" /> {label}
          </button>
        ))}
      </div>

      <div className="flex items-center gap-3">
        <button
          onClick={() => navigate("demo")}
          className="bg-stone-900 text-white px-5 py-2.5 rounded-full text-sm font-medium hover:bg-amber-700 transition-colors shadow-lg shadow-stone-900/10"
        >
          Launch App
        </button>
        <button onClick={() => setMobileMenuOpen(!mobileMenuOpen)} className="md:hidden p-2" aria-label="Toggle menu">
          <MoreVertical className="w-5 h-5" />
        </button>
      </div>
    </div>

    {mobileMenuOpen && (
      <div className="md:hidden bg-white border-t border-stone-200 py-4 px-6 space-y-3">
        {navLinks.map(({ id, label, icon: Icon }) => (
          <button
            key={id}
            onClick={() => navigate(id)}
            className="w-full text-left py-2 text-stone-600 hover:text-amber-700 flex items-center gap-2"
          >
            <Icon className="w-4 h-4" /> {label}
          </button>
        ))}
      </div>
    )}
  </nav>
);

const Hero = ({ navigate, stats }) => (
  <section id="home" className="pt-32 pb-20 md:pt-48 md:pb-32 px-6 relative overflow-hidden">
    <div className="absolute inset-0 bg-gradient-to-br from-amber-50 via-transparent to-stone-100 opacity-50" />
    <div className="max-w-7xl mx-auto grid lg:grid-cols-2 gap-12 items-center relative z-10">
      <div className="space-y-8">
        <HeroBadge />
        <h1 className="text-5xl md:text-7xl font-serif font-medium leading-tight text-stone-900">
          Your Legal Assistant <br />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-amber-700 to-amber-600">for Bar Mastery.</span>
        </h1>
        <p className="text-xl text-stone-600 max-w-lg leading-relaxed">
          Black letter law drills, AI-generated fact patterns, and a dynamic spaced repetition engine. Designed for the modern legal scholar.
        </p>

        <div className="grid grid-cols-3 gap-4 pt-4">
          {stats.map((stat) => (
            <div key={stat.label} className="bg-white p-4 rounded-xl border border-stone-200 shadow-sm">
              <div className={`text-2xl font-bold ${stat.tone || "text-orange-500"}`}>{stat.value}</div>
              <div className="text-xs text-stone-500 font-medium">{stat.label}</div>
            </div>
          ))}
        </div>

        <div className="flex flex-col sm:flex-row gap-4 pt-4">
          <button
            onClick={() => navigate("hypo")}
            className="px-8 py-4 bg-amber-700 text-white rounded-xl font-semibold shadow-xl shadow-amber-900/10 hover:bg-amber-800 hover:transform hover:-translate-y-1 transition-all flex items-center justify-center gap-2"
          >
            Start Issue Spotting
            <Gavel className="w-5 h-5" />
          </button>
          <button
            onClick={() => navigate("planner")}
            className="px-8 py-4 bg-white text-stone-700 border border-stone-200 rounded-xl font-semibold hover:bg-stone-50 transition-colors flex items-center justify-center gap-2"
          >
            Build Study Plan
          </button>
        </div>
      </div>

      <HeroGraphic />
    </div>
  </section>
);

const HeroGraphic = () => (
  <div className="relative hidden lg:block">
    <div className="absolute inset-0 bg-gradient-to-tr from-amber-500/10 to-transparent rounded-full blur-3xl" />
    <div className="relative bg-white border border-stone-100 rounded-2xl shadow-2xl p-6 transform rotate-1 hover:rotate-0 transition-transform duration-500">
      <div className="flex items-center justify-between mb-6 border-b border-stone-100 pb-4">
        <div className="flex items-center gap-3">
          <div className="w-3 h-3 rounded-full bg-red-400" />
          <div className="w-3 h-3 rounded-full bg-amber-400" />
          <div className="w-3 h-3 rounded-full bg-emerald-400" />
        </div>
        <div className="text-xs font-mono text-stone-400">performance_engine.py</div>
      </div>
      <div className="space-y-4 font-mono text-sm">
        <StatRow label="Evidence: Hearsay" value="94% Mastery" />
        <StatRow label="Crim Pro: 4th Amendment" value="Review Due" tone="text-amber-600" />
        <StatRow label="Contracts: Battle of Forms" value="Critical Weakness" tone="text-red-500" />
        <div className="h-32 bg-stone-50 rounded-lg border border-stone-100 flex items-center justify-center relative overflow-hidden">
          <div className="absolute inset-0 flex items-center justify-center opacity-10">
            <svg viewBox="0 0 100 100" className="w-full h-full">
              <path d="M10 50 Q 50 10 90 50 T 170 50" stroke="currentColor" strokeWidth="2" fill="none" />
            </svg>
          </div>
          <span className="text-stone-400 flex items-center gap-2">
            <Zap className="w-4 h-4" /> Calculating Stats...
          </span>
        </div>
      </div>
    </div>
  </div>
);

const StatRow = ({ label, value, tone = "text-emerald-600" }) => (
  <div className="flex items-center justify-between p-3 bg-stone-50 rounded-lg border border-stone-100">
    <span className="text-stone-600">{label}</span>
    <span className={`font-bold ${tone}`}>{value}</span>
  </div>
);

const Features = () => (
  <section className="py-20 bg-white">
    <div className="max-w-7xl mx-auto px-6">
      <div className="text-center mb-16">
        <h2 className="text-3xl md:text-4xl font-serif font-medium text-stone-900 mb-4">Precision Legal Education</h2>
        <p className="text-stone-600 max-w-2xl mx-auto">
          Every feature engineered to maximize retention and accelerate mastery of complex legal doctrines.
        </p>
      </div>

      <div className="grid md:grid-cols-3 gap-8">
        <FeatureCard
          icon={<Brain className="w-6 h-6" />}
          title="Adaptive Learning"
          description="SM-2 spaced repetition algorithm tracks mastery and optimizes review intervals for maximum retention."
          color="amber"
        />
        <FeatureCard
          icon={<Gavel className="w-6 h-6" />}
          title="AI Fact Patterns"
          description="Generate unlimited hypotheticals across all MBE subjects with instant IRAC-style analysis."
          color="emerald"
        />
        <FeatureCard
          icon={<BarChart2 className="w-6 h-6" />}
          title="Performance Analytics"
          description="Granular metrics on accuracy, weak areas, and progress trajectory with predictive insights."
          color="blue"
        />
        <FeatureCard
          icon={<MessageSquare className="w-6 h-6" />}
          title="Socratic Tutor"
          description="Context-aware AI assistant provides Socratic dialogue for deeper conceptual understanding."
          color="purple"
        />
        <FeatureCard
          icon={<Calendar className="w-6 h-6" />}
          title="Study Architect"
          description="AI-generated study plans calibrated to your timeline, weaknesses, and learning modality."
          color="orange"
        />
        <FeatureCard
          icon={<Target className="w-6 h-6" />}
          title="Weakness Detection"
          description="Machine learning identifies knowledge gaps and auto-prioritizes high-impact review topics."
          color="red"
        />
      </div>
    </div>
  </section>
);

const NumberInput = ({ label, value, onChange, min = 0, max }) => (
  <div>
    <label className="block text-xs font-bold text-stone-500 uppercase mb-2">{label}</label>
    <input
      type="number"
      value={value}
      min={min}
      max={max}
      onChange={(event) => onChange(Number(event.target.value))}
      className="w-full p-2 border border-stone-200 rounded-lg text-sm focus:ring-2 focus:ring-amber-500 outline-none"
    />
  </div>
);

const DateInput = ({ label, value, onChange }) => (
  <div>
    <label className="block text-xs font-bold text-stone-500 uppercase mb-2">{label}</label>
    <input
      type="date"
      value={value}
      onChange={(event) => onChange(event.target.value)}
      className="w-full p-2 border border-stone-200 rounded-lg text-sm focus:ring-2 focus:ring-amber-500 outline-none bg-white"
    />
  </div>
);

const CheckboxInput = ({ id, label, checked, onChange }) => (
  <label htmlFor={id} className="flex items-center gap-2 text-sm text-stone-600">
    <input
      type="checkbox"
      id={id}
      checked={checked}
      onChange={(event) => onChange(event.target.checked)}
      className="w-4 h-4 text-amber-600 border-stone-300 rounded focus:ring-amber-500"
    />
    {label}
  </label>
);

const SelectInput = ({ label, options, value, onChange }) => (
  <div>
    <label className="block text-xs font-bold text-stone-500 uppercase mb-2">{label}</label>
    <select
      value={value}
      onChange={(event) => onChange(event.target.value)}
      className="w-full p-2 border border-stone-200 rounded-lg text-sm bg-white outline-none focus:ring-2 focus:ring-amber-500"
    >
      {options.map((option) => (
        <option key={option}>{option}</option>
      ))}
    </select>
  </div>
);

const InputCard = ({ label, children }) => (
  <div className="bg-stone-800 p-4 rounded-lg border border-stone-700">
    <label className="block text-xs font-bold text-stone-500 uppercase mb-2">{label}</label>
    {children}
  </div>
);

const EnhancedAIPlanner = () => {
  const [loading, setLoading] = useState(false);
  const [plan, setPlan] = useState(null);
  const [savedPlans, setSavedPlans] = useLocalStorage(StorageKeys.SAVED_PLANS, []);
  const [showSaved, setShowSaved] = useState(false);
  const [error, setError] = useState("");
  const requestSignal = useAbortController();

  const [formData, setFormData] = useState({
    weeks: 10,
    hours: 6,
    weakness: "Contracts",
    style: "Textual (Outlines)",
    examDate: "",
    mbeOnly: false,
  });

  const handleGenerate = async () => {
    setLoading(true);
    setError("");
    const prompt = `Act as a Senior Bar Exam Tutor. Create a detailed, ${formData.weeks}-week study plan.
    Context: Student studies ${formData.hours} hrs/day. ${formData.mbeOnly ? "MBE focus only." : "Include essay prep."}
    Weakness: ${formData.weakness} (Front-load this subject).
    Learning Style: ${formData.style}.
    ${formData.examDate ? `Exam Date: ${formData.examDate}` : ""}

    Output format: HTML with proper structure
    - Use <h3> for week headers
    - Use <ul> and <li> for daily tasks
    - Use <strong> for key deliverables and milestones
    - Use <em> for important notes
    - Include specific page numbers and practice question counts
    - Add checkpoint assessments every 2 weeks`;

    try {
      const result = await callGemini(prompt, "", requestSignal());
      const cleanResult = result.replace(/```html/g, "").replace(/```/g, "");
      setPlan(cleanResult);
    } catch (apiError) {
      if (apiError.message !== "Request was cancelled.") {
        setError(apiError.message || "Unable to generate plan right now.");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleSave = () => {
    if (plan) {
      const newPlan = {
        id: Date.now(),
        created: new Date().toISOString(),
        config: formData,
        content: plan,
      };
      setSavedPlans([newPlan, ...savedPlans.slice(0, 4)]);
    }
  };

  const handleExport = () => {
    if (!plan) return;
    const blob = new Blob([plan], { type: "text/html" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `bar-prep-plan-${formData.weeks}weeks.html`;
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6">
      <div className="bg-stone-50 rounded-xl shadow-lg border border-stone-200 overflow-hidden flex flex-col md:flex-row">
        <div className="p-8 border-b md:border-b-0 md:border-r border-stone-200 md:w-1/3 bg-white">
          <div className="space-y-5">
            <NumberInput label="Timeline (Weeks)" value={formData.weeks} min={1} max={52} onChange={(value) => setFormData({ ...formData, weeks: value })} />
            <NumberInput label="Hours / Day" value={formData.hours} min={1} max={16} onChange={(value) => setFormData({ ...formData, hours: value })} />
            <DateInput label="Exam Date (Optional)" value={formData.examDate} onChange={(value) => setFormData({ ...formData, examDate: value })} />
            <SelectInput
              label="Priority Subject"
              options={["Contracts", "Torts", "Real Property", "Evidence", "Crim Pro", "Con Law", "Civil Procedure"]}
              value={formData.weakness}
              onChange={(value) => setFormData({ ...formData, weakness: value })}
            />
            <SelectInput
              label="Learning Modality"
              options={["Textual (Outlines)", "Visual (Flowcharts)", "Auditory (Lectures)", "Practice-Based (MCQ heavy)", "Hybrid (Mixed methods)"]}
              value={formData.style}
              onChange={(value) => setFormData({ ...formData, style: value })}
            />
            <CheckboxInput id="mbeOnly" label="MBE Focus Only" checked={formData.mbeOnly} onChange={(checked) => setFormData({ ...formData, mbeOnly: checked })} />
            <button
              onClick={handleGenerate}
              disabled={loading}
              className="w-full py-3 bg-stone-900 text-white rounded-lg font-bold text-sm hover:bg-amber-700 transition-colors shadow-md disabled:opacity-50 flex justify-center gap-2"
            >
              {loading ? <RefreshCw className="w-4 h-4 animate-spin" /> : "Generate Strategy"}
            </button>
            {savedPlans.length > 0 && (
              <button
                onClick={() => setShowSaved(!showSaved)}
                className="w-full py-2 bg-stone-100 text-stone-700 rounded-lg text-sm hover:bg-stone-200 transition-colors flex items-center justify-center gap-2"
              >
                <BookOpen className="w-4 h-4" />
                Saved Plans ({savedPlans.length})
                {showSaved ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
              </button>
            )}
            {error && (
              <div className="flex items-center gap-2 text-sm text-red-600 bg-red-50 border border-red-100 rounded-lg p-3">
                <AlertCircle className="w-4 h-4" /> {error}
              </div>
            )}
          </div>
        </div>

        <div className="p-8 md:w-2/3 bg-stone-50 min-h-[500px]">
          {plan ? (
            <div className="h-full flex flex-col">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-serif font-bold text-stone-900">Strategic Roadmap</h3>
                <div className="flex gap-2">
                  <button onClick={handleSave} className="text-stone-400 hover:text-amber-600 transition-colors" title="Save Plan">
                    <BookmarkCheck className="w-5 h-5" />
                  </button>
                  <button className="text-stone-400 hover:text-stone-600 disabled:opacity-50" aria-label="Download plan" onClick={handleExport} disabled={!plan}>
                    <Download className="w-5 h-5" />
                  </button>
                </div>
              </div>
              <div className="prose prose-stone prose-sm max-w-none overflow-y-auto max-h-[500px] pr-2 custom-scrollbar">
                <div dangerouslySetInnerHTML={{ __html: plan }} />
              </div>
            </div>
          ) : (
            <div className="h-full flex flex-col items-center justify-center text-stone-400 space-y-4">
              <div className="w-16 h-16 bg-white rounded-full flex items-center justify-center border border-stone-200 shadow-sm">
                {loading ? <RefreshCw className="w-8 h-8 animate-spin text-amber-500" /> : <Calendar className="w-8 h-8 text-stone-300" />}
              </div>
              <p className="text-center">
                {loading
                  ? "Analyzing constraints and generating optimal path..."
                  : "Configure your parameters to generate a personalized study path."}
              </p>
            </div>
          )}
        </div>
      </div>

      {showSaved && savedPlans.length > 0 && (
        <div className="bg-white rounded-lg border border-stone-200 p-6">
          <h4 className="font-bold text-stone-900 mb-4">Previously Generated Plans</h4>
          <div className="space-y-3">
            {savedPlans.map((savedPlan) => (
              <div
                key={savedPlan.id}
                className="p-4 bg-stone-50 rounded-lg border border-stone-200 hover:border-amber-300 transition-colors cursor-pointer"
                onClick={() => setPlan(savedPlan.content)}
              >
                <div className="flex justify-between items-start">
                  <div>
                    <div className="text-sm font-bold text-stone-900">
                      {savedPlan.config.weeks} Week Plan - {savedPlan.config.weakness}
                    </div>
                    <div className="text-xs text-stone-500 mt-1">
                      {new Date(savedPlan.created).toLocaleDateString()} • {savedPlan.config.hours}hrs/day • {savedPlan.config.style}
                    </div>
                  </div>
                  <button className="text-amber-600 hover:text-amber-700">
                    <Eye className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

const EnhancedHypotheticalEngine = () => {
  const [subject, setSubject] = useState("Torts");
  const [difficulty, setDifficulty] = useState("Medium");
  const [factPattern, setFactPattern] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showAnswer, setShowAnswer] = useState(false);
  const [analysis, setAnalysis] = useState(null);
  const [userAnswer, setUserAnswer] = useState("");
  const [history, setHistory] = useLocalStorage(StorageKeys.HYPO_HISTORY, []);
  const [bookmarked, setBookmarked] = useState(false);
  const [feedback, setFeedback] = useState(null);
  const [error, setError] = useState("");
  const requestSignal = useAbortController();

  const subjects = ["Torts", "Contracts", "Criminal Law", "Evidence", "Property", "Con Law", "Civil Procedure"];
  const difficulties = ["Easy", "Medium", "Hard", "Bar Exam Level"];

  const generateHypo = async () => {
    setLoading(true);
    setShowAnswer(false);
    setAnalysis(null);
    setUserAnswer("");
    setBookmarked(false);
    setFeedback(null);
    setError("");

    const difficultyContext = {
      Easy: "single-issue, straightforward facts",
      Medium: "2-3 interrelated issues with moderate complexity",
      Hard: "multiple overlapping issues with nuanced fact patterns",
      "Bar Exam Level": "maximum complexity with subtle distinctions and policy considerations",
    };

    const prompt = `Generate a ${difficultyContext[difficulty]} bar exam hypothetical for ${subject}.
        Requirements:
        - Dense, realistic fact pattern with specific details
        - Clear call of the question
        - Test commonly tested sub-topics
        - Include red herrings for ${difficulty !== "Easy" ? "advanced" : "basic"} issue spotters
        - 150-250 words

        Format: Plain text, end with "Question: [the actual question to answer]"`;

    try {
      const facts = await callGemini(prompt, "", requestSignal());
      setFactPattern(facts);

      const analysisPrompt = `Provide comprehensive IRAC analysis for this ${subject} fact pattern:

        ${facts}

        Requirements:
        - Identify ALL issues (main and subsidiary)
        - State applicable rules with case citations where relevant
        - Apply facts to each element
        - Reach clear conclusions
        - Note any close calls or policy considerations

        Format as structured HTML with <h4> for issues, <p> for analysis.`;

      const ans = await callGemini(analysisPrompt, "", requestSignal());
      setAnalysis(ans);
    } catch (apiError) {
      if (apiError.message !== "Request was cancelled.") {
        setError(apiError.message || "Unable to generate hypothetical.");
      }
    } finally {
      setLoading(false);
    }
  };

  const evaluateAnswer = async () => {
    if (!userAnswer.trim() || !analysis) return;

    const prompt = `Compare the student's answer to the model analysis.

      Fact Pattern: ${factPattern}

      Model Analysis: ${analysis}

      Student Answer: ${userAnswer}

      Provide:
      1. Issues Spotted: List what they identified
      2. Issues Missed: What they overlooked
      3. Accuracy: Rate their rule statements (1-5)
      4. Application: Quality of fact-to-law analysis (1-5)
      5. Overall: Strengths and areas for improvement

      Be constructive and specific.`;

    try {
      const evaluation = await callGemini(prompt, "", requestSignal());
      setFeedback(evaluation);
    } catch (apiError) {
      if (apiError.message !== "Request was cancelled.") {
        setError(apiError.message || "Unable to evaluate answer.");
      }
    }
  };

  const handleBookmark = () => {
    if (factPattern && !bookmarked) {
      const newItem = {
        id: Date.now(),
        subject,
        difficulty,
        factPattern,
        analysis,
        created: new Date().toISOString(),
      };
      setHistory([newItem, ...history.slice(0, 19)]);
      setBookmarked(true);
    }
  };

  return (
    <div className="space-y-6">
      <div className="grid md:grid-cols-4 gap-6">
        <div className="md:col-span-1 space-y-4">
          <InputCard label="Domain">
            <select
              value={subject}
              onChange={(event) => setSubject(event.target.value)}
              className="w-full p-2 bg-stone-900 border border-stone-600 rounded text-stone-200 text-sm outline-none focus:border-amber-500"
            >
              {subjects.map((option) => (
                <option key={option}>{option}</option>
              ))}
            </select>
          </InputCard>
          <InputCard label="Difficulty">
            <select
              value={difficulty}
              onChange={(event) => setDifficulty(event.target.value)}
              className="w-full p-2 bg-stone-900 border border-stone-600 rounded text-stone-200 text-sm outline-none focus:border-amber-500"
            >
              {difficulties.map((option) => (
                <option key={option}>{option}</option>
              ))}
            </select>
          </InputCard>
          <button
            onClick={generateHypo}
            disabled={loading}
            className="w-full py-4 bg-amber-700 hover:bg-amber-600 text-white rounded-lg font-bold shadow-lg transition-all flex items-center justify-center gap-2 disabled:opacity-50"
          >
            {loading ? <RefreshCw className="w-5 h-5 animate-spin" /> : (<>
              Generate New <ChevronRight className="w-5 h-5" />
            </>)}
          </button>
          {factPattern && (
            <button
              onClick={handleBookmark}
              disabled={bookmarked}
              className="w-full py-3 bg-stone-700 hover:bg-stone-600 text-white rounded-lg text-sm transition-all flex items-center justify-center gap-2 disabled:opacity-50"
            >
              {bookmarked ? <BookmarkCheck className="w-4 h-4" /> : <Bookmark className="w-4 h-4" />}
              {bookmarked ? "Saved" : "Save to History"}
            </button>
          )}
          {error && (
            <div className="flex items-center gap-2 text-sm text-red-200 bg-red-900/30 border border-red-800/50 rounded-lg p-3">
              <AlertCircle className="w-4 h-4" /> {error}
            </div>
          )}
        </div>

        <div className="md:col-span-3 bg-stone-800 rounded-xl border border-stone-700 p-8 min-h-[400px] relative">
          {!factPattern && !loading && (
            <div className="absolute inset-0 flex flex-col items-center justify-center text-stone-600 space-y-3">
              <Gavel className="w-12 h-12" />
              <p className="text-center">Select a subject and difficulty to begin issue spotting practice.</p>
            </div>
          )}

          {factPattern && (
            <div className="space-y-6 animate-fadeIn">
              <div>
                <div className="flex justify-between items-center mb-3">
                  <h3 className="text-amber-500 font-bold uppercase text-xs tracking-wider">Fact Pattern</h3>
                  <div className="flex gap-2 text-xs">
                    <span className="px-2 py-1 bg-stone-700 rounded text-stone-300">{subject}</span>
                    <span className="px-2 py-1 bg-amber-900/30 rounded text-amber-400">{difficulty}</span>
                  </div>
                </div>
                <div className="prose prose-invert prose-sm max-w-none text-stone-300 leading-relaxed">
                  <div dangerouslySetInnerHTML={{ __html: factPattern.replace(/\n/g, "<br/>") }} />
                </div>
              </div>

              {!showAnswer && (
                <div className="border-t border-stone-700 pt-6">
                  <label className="block text-emerald-500 font-bold uppercase text-xs tracking-wider mb-3">
                    Your Answer (Optional)
                  </label>
                  <textarea
                    value={userAnswer}
                    onChange={(event) => setUserAnswer(event.target.value)}
                    placeholder="Type your IRAC analysis here before revealing the model answer..."
                    className="w-full p-4 bg-stone-900 border border-stone-600 rounded-lg text-stone-200 text-sm outline-none focus:border-emerald-500 min-h-[150px] resize-y"
                  />
                  {userAnswer.trim() && (
                    <button
                      onClick={evaluateAnswer}
                      className="mt-3 px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-sm font-medium transition-colors flex items-center gap-2"
                    >
                      <CheckCircle className="w-4 h-4" /> Get AI Feedback
                    </button>
                  )}
                </div>
              )}

              {feedback && !showAnswer && (
                <div className="bg-stone-900/70 border border-emerald-700/30 rounded-lg p-5">
                  <h4 className="text-emerald-400 font-bold text-sm mb-3 flex items-center gap-2">
                    <Award className="w-4 h-4" /> AI Evaluation
                  </h4>
                  <div className="prose prose-invert prose-sm max-w-none text-stone-300">
                    <div dangerouslySetInnerHTML={{ __html: feedback.replace(/\n/g, "<br/>") }} />
                  </div>
                </div>
              )}

              {analysis && (
                <div className="pt-6 border-t border-stone-700">
                  {!showAnswer ? (
                    <button
                      onClick={() => setShowAnswer(true)}
                      className="text-sm font-medium text-amber-500 hover:text-amber-400 flex items-center gap-2 transition-colors"
                    >
                      <FileText className="w-4 h-4" /> Reveal Model Analysis
                    </button>
                  ) : (
                    <div className="animate-slideUp space-y-4">
                      <h3 className="text-emerald-500 font-bold uppercase text-xs tracking-wider mb-3">Model Analysis</h3>
                      <div className="prose prose-invert prose-sm max-w-none text-stone-300 bg-stone-900/50 p-6 rounded-lg border border-stone-600">
                        <div dangerouslySetInnerHTML={{ __html: analysis.replace(/\n/g, "<br/>") }} />
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}

          {loading && (
            <div className="absolute inset-0 flex flex-col items-center justify-center gap-3 bg-stone-900/60 backdrop-blur-sm rounded-xl">
              <RefreshCw className="w-8 h-8 animate-spin text-amber-400" />
              <p className="text-sm text-stone-200">Drafting new fact pattern...</p>
            </div>
          )}
        </div>
      </div>

      {history.length > 0 && (
        <div className="bg-stone-800 rounded-lg border border-stone-700 p-6">
          <h4 className="text-white font-bold mb-4 flex items-center gap-2">
            <Clock className="w-5 h-5" /> Recent Practice Sessions
          </h4>
          <div className="grid md:grid-cols-2 gap-3">
            {history.slice(0, 6).map((item) => (
              <div
                key={item.id}
                className="p-4 bg-stone-900/50 rounded-lg border border-stone-700 hover:border-amber-700 transition-colors cursor-pointer"
                onClick={() => {
                  setFactPattern(item.factPattern);
                  setAnalysis(item.analysis);
                  setSubject(item.subject);
                  setDifficulty(item.difficulty);
                  setShowAnswer(false);
                }}
              >
                <div className="flex justify-between items-start mb-2">
                  <span className="text-xs font-bold text-amber-500">{item.subject}</span>
                  <span className="text-xs text-stone-500">{new Date(item.created).toLocaleDateString()}</span>
                </div>
                <div className="text-sm text-stone-300 line-clamp-2">{item.factPattern.substring(0, 100)}...</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

const EnhancedMiniTutor = ({ userStats, setUserStats }) => {
  const [currentCardIndex, setCurrentCardIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);
  const [sessionStats, setSessionStats] = useState({ correct: 0, total: 0, startTime: Date.now() });
  const [chatOpen, setChatOpen] = useState(false);
  const [chatQuery, setChatQuery] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [chatLoading, setChatLoading] = useState(false);
  const [filterSubject, setFilterSubject] = useState("All");
  const [showSettings, setShowSettings] = useState(false);
  const [cardHistory, setCardHistory] = useLocalStorage(StorageKeys.CARD_HISTORY, []);
  const [bookmarks, setBookmarks] = useLocalStorage(StorageKeys.BOOKMARKS, []);
  const chatEndRef = useRef(null);
  const requestSignal = useAbortController();

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatHistory]);

  const allCards = [
    {
      id: 1,
      subject: "Real Property",
      topic: "Adverse Possession",
      question: "Elements of Adverse Possession",
      answer:
        "Possession must be: (1) Continuous for statutory period, (2) Open & Notorious, (3) Actual & Exclusive, (4) Hostile (without owner's permission).",
      subtext: "Mnemonic: COAH",
      difficulty: "Medium",
    },
    {
      id: 2,
      subject: "Evidence",
      topic: "Hearsay Exceptions",
      question: "Excited Utterance vs. Present Sense Impression",
      answer:
        "Excited Utterance: Statement relating to startling event made while under stress of excitement. Present Sense Impression: Statement describing event made while perceiving it or immediately thereafter.",
      subtext: "Time gap and emotional state are key distinctions.",
      difficulty: "Hard",
    },
    {
      id: 3,
      subject: "Criminal Procedure",
      topic: "Search & Seizure",
      question: "Search Incident to Lawful Arrest (SILA)",
      answer: "Police may search the person and areas within their 'wingspan' (immediate control) for weapons or evidence without a warrant.",
      subtext: "Chimel v. California - Cannot search entire house",
      difficulty: "Medium",
    },
    {
      id: 4,
      subject: "Torts",
      topic: "Negligence",
      question: "Res Ipsa Loquitur Inference",
      answer:
        "Jury may infer breach if: (1) Accident normally doesn't occur without negligence, (2) Instrumentality under defendant's exclusive control, (3) Plaintiff did not contribute to accident.",
      subtext: "Avoids directed verdict for defendant.",
      difficulty: "Easy",
    },
    {
      id: 5,
      subject: "Contracts",
      topic: "Formation",
      question: "Battle of the Forms - UCC §2-207",
      answer:
        "Between merchants: (1) Contract formed even with different terms, (2) Additional terms become part of contract unless material, prior objection, or offeror objects within reasonable time, (3) Different terms knock out each other (majority rule).",
      subtext: "Critical for MBE - memorize the knockout rule",
      difficulty: "Hard",
    },
    {
      id: 6,
      subject: "Constitutional Law",
      topic: "Equal Protection",
      question: "Levels of Scrutiny",
      answer:
        "Strict Scrutiny: Suspect class (race, national origin, alienage) or fundamental right - must be narrowly tailored to compelling interest. Intermediate: Quasi-suspect (gender, legitimacy) - substantially related to important interest. Rational Basis: All others - rationally related to legitimate interest.",
      subtext: "Most EP claims fail under rational basis",
      difficulty: "Medium",
    },
    {
      id: 7,
      subject: "Criminal Law",
      topic: "Homicide",
      question: "Murder vs. Manslaughter",
      answer:
        "Murder: Unlawful killing with malice aforethought (intent to kill, intent to cause serious bodily harm, depraved heart, felony murder). Voluntary Manslaughter: Killing in heat of passion with adequate provocation. Involuntary: Unintentional killing from criminal negligence or unlawful act.",
      subtext: "Cooling off period defeats heat of passion",
      difficulty: "Medium",
    },
    {
      id: 8,
      subject: "Civil Procedure",
      topic: "Personal Jurisdiction",
      question: "Minimum Contacts Test",
      answer:
        "Court has PJ if defendant has minimum contacts with forum such that maintenance of suit doesn't offend traditional notions of fair play and substantial justice. Consider: (1) Purposeful availment, (2) Foreseeability, (3) Reasonableness factors.",
      subtext: "International Shoe Co. v. Washington",
      difficulty: "Hard",
    },
    {
      id: 9,
      subject: "Evidence",
      topic: "Character Evidence",
      question: "Propensity Rule and Exceptions",
      answer:
        "General Rule: Character evidence inadmissible to prove conforming conduct. Criminal D Exceptions: (1) D may introduce pertinent good character, (2) Prosecution may rebut, (3) Victim's character admissible in self-defense cases. Civil: Generally inadmissible except when character is essential element.",
      subtext: "MIMIC exceptions: Motive, Intent, Mistake, Identity, Common plan",
      difficulty: "Hard",
    },
    {
      id: 10,
      subject: "Torts",
      topic: "Products Liability",
      question: "Strict Liability for Defective Products",
      answer:
        "Elements: (1) D is commercial seller, (2) Product defective (manufacturing, design, or warning), (3) Defect existed when left D's control, (4) P was foreseeable user, (5) Injury caused by defect. No privity required.",
      subtext: "Design defect: consumer expectation or risk-utility test",
      difficulty: "Medium",
    },
    {
      id: 11,
      subject: "Contracts",
      topic: "Remedies",
      question: "Expectation Damages Formula",
      answer:
        "Put non-breaching party in position they would have been in if contract fully performed. Formula: Loss in Value + Other Loss - Cost Avoided - Loss Avoided. Include consequential if foreseeable and certain.",
      subtext: "Mitigation required - cannot recover avoidable losses",
      difficulty: "Medium",
    },
    {
      id: 12,
      subject: "Real Property",
      topic: "Future Interests",
      question: "Remainders: Vested vs. Contingent",
      answer:
        "Vested Remainder: Created in ascertained person with no conditions precedent (except natural termination of prior estate). Contingent: Created in unascertained person OR subject to condition precedent. Vested subject to open: Class gift where class can still grow.",
      subtext: "Preference for vested construction - resolves ambiguity",
      difficulty: "Hard",
    },
  ];

  const filteredCards = filterSubject === "All" ? allCards : allCards.filter((card) => card.subject === filterSubject);
  const card = filteredCards[currentCardIndex] || allCards[0];
  const subjects = ["All", ...new Set(allCards.map((c) => c.subject))];
  const isBookmarked = bookmarks.includes(card.id);

  const handleRate = (quality) => {
    const newTotal = sessionStats.total + 1;
    const newCorrect = sessionStats.correct + (quality >= 3 ? 1 : 0);

    setSessionStats((prev) => ({
      ...prev,
      correct: newCorrect,
      total: newTotal,
    }));

    setUserStats((prev) => ({
      ...prev,
      totalCards: prev.totalCards + 1,
      masteredCards: quality === 5 ? prev.masteredCards + 1 : prev.masteredCards,
      lastStudyDate: new Date().toISOString(),
    }));

    setCardHistory((prev) => [
      {
        cardId: card.id,
        quality,
        timestamp: Date.now(),
        subject: card.subject,
      },
      ...prev.slice(0, 999),
    ]);

    setChatOpen(false);
    setChatHistory([]);
    setIsFlipped(false);
    setTimeout(() => {
      if (currentCardIndex < filteredCards.length - 1) {
        setCurrentCardIndex((prev) => prev + 1);
      } else {
        setCurrentCardIndex(0);
      }
    }, 300);
  };

  const handleAskTutor = async () => {
    if (!chatQuery.trim()) return;
    setChatLoading(true);
    const newHistory = [...chatHistory, { role: "user", text: chatQuery }];
    setChatHistory(newHistory);
    setChatQuery("");

    const prompt = `Context: Law student studying ${card.subject} - ${card.topic}.
    Black Letter Rule: ${card.answer}.

    Student Question: ${chatQuery}

    Respond as a Socratic law professor:
    - Ask probing questions to deepen understanding
    - Use hypothetical variations
    - Connect to related doctrines
    - Be precise with legal terminology
    - Keep response concise (3-4 sentences)`;

    try {
      const response = await callGemini(prompt, "", requestSignal());
      setChatHistory([...newHistory, { role: "ai", text: response }]);
    } catch (apiError) {
      if (apiError.message !== "Request was cancelled.") {
        setChatHistory([...newHistory, { role: "ai", text: apiError.message || "Unable to process question." }]);
      }
    } finally {
      setChatLoading(false);
    }
  };

  const toggleBookmark = () => {
    if (isBookmarked) {
      setBookmarks(bookmarks.filter((id) => id !== card.id));
    } else {
      setBookmarks([...bookmarks, card.id]);
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleAskTutor();
    }
  };

  const accuracy = sessionStats.total === 0 ? 0 : Math.round((sessionStats.correct / sessionStats.total) * 100);
  const studyDuration = Math.floor((Date.now() - sessionStats.startTime) / 60000);

  return (
    <div className="bg-white rounded-2xl shadow-xl border border-stone-200 overflow-hidden">
      <div className="bg-stone-50 border-b border-stone-200 px-6 py-4">
        <div className="flex flex-wrap justify-between items-center gap-4">
          <div className="flex items-center gap-6">
            <TopStat icon={<Target className="w-4 h-4 text-amber-700" />} label="Accuracy" value={`${accuracy}%`} />
            <TopStat icon={<CheckCircle className="w-4 h-4 text-emerald-600" />} label="Correct" value={`${sessionStats.correct}/${sessionStats.total}`} />
            <TopStat icon={<Clock className="w-4 h-4 text-blue-600" />} label="Session" value={`${studyDuration}min`} />
          </div>

          <div className="flex items-center gap-3">
            <select
              value={filterSubject}
              onChange={(event) => {
                setFilterSubject(event.target.value);
                setCurrentCardIndex(0);
                setIsFlipped(false);
              }}
              className="text-sm px-3 py-1.5 border border-stone-200 rounded-lg bg-white outline-none focus:border-amber-500"
            >
              {subjects.map((subjectOption) => (
                <option key={subjectOption}>{subjectOption}</option>
              ))}
            </select>
            <button
              onClick={toggleBookmark}
              className={`p-2 rounded-lg transition-colors ${
                isBookmarked ? "bg-amber-100 text-amber-700" : "bg-white border border-stone-200 text-stone-400 hover:text-amber-600"
              }`}
              aria-label="Toggle bookmark"
            >
              {isBookmarked ? <BookmarkCheck className="w-4 h-4" /> : <Bookmark className="w-4 h-4" />}
            </button>
            <button
              onClick={() => setShowSettings(!showSettings)}
              className="p-2 rounded-lg bg-white border border-stone-200 text-stone-600 hover:text-stone-900"
              aria-label="Toggle settings"
            >
              <Settings className="w-4 h-4" />
            </button>
          </div>
        </div>

        {showSettings && (
          <div className="mt-4 pt-4 border-t border-stone-200">
            <div className="flex items-center justify-between text-sm">
              <span className="text-stone-600">Cards in deck: {filteredCards.length}</span>
              <span className="text-stone-600">Position: {currentCardIndex + 1}/{filteredCards.length}</span>
              <button
                onClick={() => {
                  setCurrentCardIndex(0);
                  setIsFlipped(false);
                }}
                className="text-amber-700 hover:text-amber-800 font-medium flex items-center gap-1"
              >
                <RotateCcw className="w-3 h-3" /> Reset
              </button>
            </div>
          </div>
        )}
      </div>

      <div className="flex flex-col md:flex-row">
        <div className="bg-stone-50 border-b md:border-b-0 md:border-r border-stone-200 p-6 md:w-72">
          <div className="space-y-6">
            <div>
              <div className="flex items-center gap-2 mb-4">
                <Activity className="w-5 h-5 text-amber-700" />
                <span className="font-bold text-stone-800">Session Progress</span>
              </div>
              <div className="space-y-3">
                <ProgressCard label="Mastery Rate" value={`${accuracy}%`} highlight={accuracy >= 70} />
                <NumericCard label="Remaining" value={filteredCards.length - currentCardIndex} tone="text-amber-600" />
                <NumericCard label="Bookmarked" value={bookmarks.length} tone="text-blue-600" />
              </div>
            </div>

            {cardHistory.length > 0 && (
              <div>
                <div className="text-xs font-bold text-stone-400 uppercase mb-2">Last 5 Cards</div>
                <div className="space-y-1">
                  {cardHistory.slice(0, 5).map((historyItem, index) => (
                    <div key={index} className="flex items-center justify-between text-xs p-2 bg-white rounded border border-stone-200">
                      <span className="text-stone-600 truncate">
                        {allCards.find((c) => c.id === historyItem.cardId)?.topic}
                      </span>
                      <span
                        className={`font-bold ${
                          historyItem.quality >= 4 ? "text-emerald-600" : historyItem.quality >= 3 ? "text-amber-600" : "text-red-500"
                        }`}
                      >
                        {historyItem.quality >= 4 ? "✓" : historyItem.quality >= 3 ? "~" : "✗"}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <div className="text-xs text-stone-400 font-mono pt-4 border-t border-stone-200">
              <div className="flex items-center gap-1 mb-1">
                <Zap className="w-3 h-3" />
                <span>SM-2 Algorithm Active</span>
              </div>
              <div className="text-stone-300">Next review: {currentCardIndex < filteredCards.length - 1 ? "After rating" : "Deck complete"}</div>
            </div>
          </div>
        </div>

        <div className="flex-1 p-8 md:p-12 bg-gradient-to-br from-stone-50 to-white flex flex-col relative min-h-[600px]">
          <div className="flex-1 flex flex-col items-center justify-center">
            <Flashcard
              card={card}
              isFlipped={isFlipped}
              chatOpen={chatOpen}
              chatHistory={chatHistory}
              chatLoading={chatLoading}
              chatQuery={chatQuery}
              onFlip={() => !isFlipped && !chatOpen && setIsFlipped(true)}
              onChatToggle={() => setChatOpen((prev) => !prev)}
              onChatQueryChange={setChatQuery}
              onAskTutor={handleAskTutor}
              onChatKeyPress={handleKeyPress}
              chatEndRef={chatEndRef}
            />

            <RatingBar isFlipped={isFlipped} onRate={handleRate} />
          </div>
        </div>
      </div>
    </div>
  );
};

const TopStat = ({ icon, label, value }) => (
  <div className="flex items-center gap-2">
    {icon}
    <span className="text-sm font-bold text-stone-900">{value}</span>
    <span className="text-xs text-stone-500">{label}</span>
  </div>
);

const ProgressCard = ({ label, value, highlight }) => (
  <div className="bg-white p-4 rounded-lg border border-stone-200 shadow-sm">
    <div className="text-xs text-stone-400 font-bold uppercase mb-1">{label}</div>
    <div className="flex items-end gap-2">
      <div className="text-3xl font-mono font-bold text-stone-900">{value}</div>
      {highlight && <TrendingUp className="w-4 h-4 text-emerald-600 mb-1" />}
    </div>
  </div>
);

const NumericCard = ({ label, value, tone }) => (
  <div className="bg-white p-4 rounded-lg border border-stone-200 shadow-sm">
    <div className="text-xs text-stone-400 font-bold uppercase mb-1">{label}</div>
    <div className={`text-2xl font-mono font-bold ${tone}`}>{value}</div>
  </div>
);

const Flashcard = ({
  card,
  isFlipped,
  chatOpen,
  chatHistory,
  chatLoading,
  chatQuery,
  onFlip,
  onChatToggle,
  onChatQueryChange,
  onAskTutor,
  onChatKeyPress,
  chatEndRef,
}) => (
  <div className="relative w-full max-w-2xl aspect-[3/2] perspective-1000 cursor-pointer group mb-8" onClick={onFlip}>
    <div
      className={`relative w-full h-full transition-all duration-500 transform-style-3d shadow-2xl rounded-2xl border-2 ${
        isFlipped ? "border-emerald-200" : "border-amber-200"
      } bg-white ${isFlipped ? "rotate-y-180" : ""}`}
      style={{ transformStyle: "preserve-3d", transform: isFlipped ? "rotateY(180deg)" : "rotateY(0deg)" }}
    >
      <div className="absolute inset-0 backface-hidden p-10 flex flex-col items-center justify-center text-center">
        <div className="absolute top-6 left-6 flex gap-2">
          <span className="text-xs font-bold text-amber-700 bg-amber-50 px-3 py-1.5 rounded-full uppercase tracking-wide border border-amber-200">
            {card.subject}
          </span>
          <span
            className={`text-xs font-bold px-3 py-1.5 rounded-full uppercase tracking-wide ${
              card.difficulty === "Easy"
                ? "bg-green-50 text-green-700 border border-green-200"
                : card.difficulty === "Medium"
                ? "bg-blue-50 text-blue-700 border border-blue-200"
                : "bg-red-50 text-red-700 border border-red-200"
            }`}
          >
            {card.difficulty}
          </span>
        </div>
        <div className="absolute top-6 right-6 text-xs font-mono text-stone-300">{card.id}</div>
        <h3 className="text-3xl font-serif text-stone-900 leading-snug px-4">{card.question}</h3>
        <div className="absolute bottom-8 flex flex-col items-center gap-2">
          <p className="text-stone-400 text-xs uppercase tracking-widest animate-pulse">Tap to Flip</p>
          <ChevronDown className="w-5 h-5 text-stone-300 animate-bounce" />
        </div>
      </div>

      <div
        className="absolute inset-0 backface-hidden p-10 flex flex-col items-center justify-center text-center bg-gradient-to-br from-white to-stone-50 rotate-y-180"
        style={{ transform: "rotateY(180deg)", backfaceVisibility: "hidden" }}
      >
        <span className="absolute top-6 left-6 text-xs font-bold text-stone-400 uppercase tracking-wide">{card.topic}</span>

        {!chatOpen ? (
          <div className="w-full h-full flex flex-col justify-center px-4">
            <p className="text-lg text-stone-800 leading-relaxed font-medium mb-4">{card.answer}</p>
            <p className="mt-2 text-sm text-stone-500 italic font-serif border-t border-stone-200 pt-4">{card.subtext}</p>
            <button
              onClick={(event) => {
                event.stopPropagation();
                onChatToggle();
              }}
              className="mt-6 mx-auto flex items-center gap-2 text-xs font-bold text-amber-700 bg-amber-50 px-5 py-2.5 rounded-full hover:bg-amber-100 transition-colors border border-amber-200 shadow-sm"
            >
              <MessageSquare className="w-4 h-4" /> Ask Socratic Tutor
            </button>
          </div>
        ) : (
          <div className="w-full h-full flex flex-col text-left" onClick={(event) => event.stopPropagation()}>
            <div className="flex justify-between items-center mb-3 border-b border-stone-200 pb-3">
              <span className="text-xs font-bold text-amber-700 uppercase flex items-center gap-2">
                <Brain className="w-4 h-4" /> Socratic Chat
              </span>
              <button onClick={onChatToggle} className="hover:bg-stone-100 p-1 rounded" aria-label="Close chat">
                <ChevronRight className="w-4 h-4 text-stone-400 hover:text-stone-600 rotate-180" />
              </button>
            </div>
            <div className="flex-1 overflow-y-auto mb-3 space-y-3 custom-scrollbar pr-1 max-h-64">
              {chatHistory.length === 0 && (
                <div className="text-sm text-stone-400 italic text-center mt-8 space-y-2">
                  <HelpCircle className="w-8 h-8 mx-auto text-stone-300" />
                  <p>Ask a question about this rule...</p>
                  <div className="text-xs space-y-1 text-stone-400">
                    <p>• "How does this apply if..."</p>
                    <p>• "What's the exception for..."</p>
                    <p>• "Compare this to..."</p>
                  </div>
                </div>
              )}
              {chatHistory.map((message, index) => (
                <div
                  key={`${message.role}-${index}`}
                  className={`text-sm p-3 rounded-lg ${
                    message.role === "user"
                      ? "bg-stone-100 text-stone-800 ml-8"
                      : "bg-amber-50 text-stone-800 mr-8 border border-amber-100"
                  }`}
                >
                  {message.text}
                </div>
              ))}
              {chatLoading && (
                <div className="flex items-center gap-2 text-xs text-amber-600 ml-4">
                  <RefreshCw className="w-3 h-3 animate-spin" />
                  <span>Professor thinking...</span>
                </div>
              )}
              <div ref={chatEndRef} />
            </div>
            <div className="relative">
              <input
                type="text"
                value={chatQuery}
                onChange={(event) => onChatQueryChange(event.target.value)}
                onKeyDown={onChatKeyPress}
                placeholder="Type your question and press Enter..."
                className="w-full pl-3 pr-10 py-2.5 border border-stone-300 rounded-lg text-sm focus:ring-2 focus:ring-amber-500 focus:border-transparent outline-none"
              />
              <button
                onClick={(event) => {
                  event.stopPropagation();
                  onAskTutor();
                }}
                className="absolute right-2 top-2.5 text-amber-600 hover:text-amber-800 disabled:opacity-50"
                disabled={!chatQuery.trim() || chatLoading}
                aria-label="Send question"
              >
                <ChevronRight className="w-5 h-5" />
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  </div>
);

const RatingBar = ({ isFlipped, onRate }) => (
  <div className={`w-full max-w-2xl transition-all duration-300 ${isFlipped ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4 pointer-events-none"}`}>
    <div className="bg-white rounded-xl border border-stone-200 p-6 shadow-lg">
      <div className="text-xs font-bold text-stone-400 uppercase mb-3 text-center">Rate Your Confidence</div>
      <div className="grid grid-cols-4 gap-3">
        <RatingButton
          label="Again"
          icon={<ThumbsDown className="w-5 h-5" />}
          tone="border-red-200 bg-white text-red-700 hover:bg-red-50"
          interval="<1 day"
          onClick={() => onRate(1)}
        />
        <RatingButton
          label="Hard"
          icon={<AlertCircle className="w-5 h-5" />}
          tone="border-orange-200 bg-white text-orange-700 hover:bg-orange-50"
          interval="1-3 days"
          onClick={() => onRate(2)}
        />
        <RatingButton
          label="Good"
          icon={<CheckCircle className="w-5 h-5" />}
          tone="border-stone-200 bg-white text-stone-700 hover:bg-stone-50"
          interval="4-7 days"
          onClick={() => onRate(3)}
        />
        <RatingButton
          label="Easy"
          icon={<Star className="w-5 h-5" />}
          tone="border-emerald-300 bg-emerald-700 text-white hover:bg-emerald-800"
          interval="14+ days"
          onClick={() => onRate(5)}
        />
      </div>
      <div className="mt-4 text-center text-xs text-stone-400">Spaced repetition will optimize your review schedule</div>
    </div>
  </div>
);

const RatingButton = ({ label, icon, tone, interval, onClick }) => (
  <button
    onClick={onClick}
    className={`px-4 py-4 rounded-lg border-2 font-bold text-sm transition-all shadow-sm hover:shadow-md flex flex-col items-center gap-1 ${tone}`}
  >
    {icon}
    <span>{label}</span>
    <span className="text-xs text-stone-500">{interval}</span>
  </button>
);

const AnalyticsDashboard = ({ userStats }) => {
  const [cardHistory] = useLocalStorage(StorageKeys.CARD_HISTORY, []);
  const subjectStats = useMemo(() => {
    const stats = {};
    cardHistory.forEach((entry) => {
      if (!stats[entry.subject]) {
        stats[entry.subject] = { total: 0, correct: 0, avg: 0 };
      }
      stats[entry.subject].total += 1;
      if (entry.quality >= 3) {
        stats[entry.subject].correct += 1;
      }
    });
    Object.keys(stats).forEach((subject) => {
      stats[subject].avg = Math.round((stats[subject].correct / stats[subject].total) * 100);
    });
    return stats;
  }, [cardHistory]);

  const dailyActivity = useMemo(() => {
    const days = {};
    cardHistory.forEach((entry) => {
      const date = new Date(entry.timestamp).toLocaleDateString();
      days[date] = (days[date] || 0) + 1;
    });
    return days;
  }, [cardHistory]);

  const subjects = Object.keys(subjectStats).sort();
  const totalAccuracy = cardHistory.length > 0 ? Math.round((cardHistory.filter((entry) => entry.quality >= 3).length / cardHistory.length) * 100) : 0;

  return (
    <div className="space-y-6">
      <div className="grid md:grid-cols-4 gap-6">
        <StatCard
          icon={<Target className="w-6 h-6" />}
          title="Overall Accuracy"
          value={`${totalAccuracy}%`}
          subtitle={`${cardHistory.filter((entry) => entry.quality >= 3).length}/${cardHistory.length} correct`}
          color="emerald"
        />
        <StatCard
          icon={<Flame className="w-6 h-6" />}
          title="Current Streak"
          value={`${userStats.currentStreak} days`}
          subtitle={`Best: ${userStats.longestStreak || 0} days`}
          color="orange"
        />
        <StatCard
          icon={<BookOpen className="w-6 h-6" />}
          title="Cards Studied"
          value={userStats.totalCards || 0}
          subtitle={`${userStats.masteredCards || 0} mastered`}
          color="blue"
        />
        <StatCard
          icon={<Clock className="w-6 h-6" />}
          title="Study Time"
          value={`${Math.floor((userStats.totalStudyTime || 0) / 60)}h`}
          subtitle={`Last: ${userStats.lastStudyDate ? new Date(userStats.lastStudyDate).toLocaleDateString() : "Never"}`}
          color="purple"
        />
      </div>

      <div className="bg-white rounded-xl border border-stone-200 shadow-sm p-6">
        <h3 className="text-lg font-bold text-stone-900 mb-4 flex items-center gap-2">
          <PieChart className="w-5 h-5 text-amber-700" />
          Performance by Subject
        </h3>
        {subjects.length === 0 ? (
          <div className="text-center py-12 text-stone-400">
            <BarChart2 className="w-12 h-12 mx-auto mb-3 opacity-30" />
            <p>Start studying to see your performance data</p>
          </div>
        ) : (
          <div className="space-y-3">
            {subjects.map((subject) => {
              const stat = subjectStats[subject];
              const barWidth = stat.avg;
              const color = barWidth >= 80 ? "bg-emerald-500" : barWidth >= 60 ? "bg-amber-500" : "bg-red-500";
              return (
                <div key={subject} className="space-y-1">
                  <div className="flex justify-between items-center text-sm">
                    <span className="font-medium text-stone-700">{subject}</span>
                    <span className="text-stone-500">{stat.avg}% ({stat.correct}/{stat.total})</span>
                  </div>
                  <div className="h-2 bg-stone-100 rounded-full overflow-hidden">
                    <div className={`h-full ${color} transition-all duration-500`} style={{ width: `${barWidth}%` }} />
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      <div className="bg-white rounded-xl border border-stone-200 shadow-sm p-6">
        <h3 className="text-lg font-bold text-stone-900 mb-4 flex items-center gap-2">
          <Activity className="w-5 h-5 text-amber-700" />
          Recent Activity
        </h3>
        {Object.keys(dailyActivity).length === 0 ? (
          <div className="text-center py-12 text-stone-400">
            <Calendar className="w-12 h-12 mx-auto mb-3 opacity-30" />
            <p>No activity yet - start your first study session!</p>
          </div>
        ) : (
          <div className="grid grid-cols-7 gap-2">
            {Object.entries(dailyActivity)
              .slice(-21)
              .map(([date, count]) => {
                const intensity = count > 20 ? 4 : count > 10 ? 3 : count > 5 ? 2 : 1;
                const colorClass = { 1: "bg-emerald-100", 2: "bg-emerald-300", 3: "bg-emerald-500", 4: "bg-emerald-700" }[intensity];
                return (
                  <div
                    key={date}
                    className={`aspect-square rounded ${colorClass} flex items-center justify-center text-xs font-bold text-white group relative`}
                  >
                    <span className="opacity-0 group-hover:opacity-100">{count}</span>
                    <div className="absolute bottom-full mb-2 hidden group-hover:block bg-stone-900 text-white px-2 py-1 rounded text-xs whitespace-nowrap">
                      {date}: {count} cards
                    </div>
                  </div>
                );
              })}
          </div>
        )}
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <InsightCard
          title="Strengths"
          icon={<TrendingUp className="w-5 h-5" />}
          color="from-amber-50 to-orange-50"
          border="border-amber-200"
          items={subjects.filter((subject) => subjectStats[subject].avg >= 75).slice(0, 3).map((subject) => `${subject} (${subjectStats[subject].avg}%)`)}
          emptyText="Keep studying to identify your strong subjects"
        />
        <InsightCard
          title="Focus Areas"
          icon={<TrendingDown className="w-5 h-5" />}
          color="from-red-50 to-pink-50"
          border="border-red-200"
          items={subjects.filter((subject) => subjectStats[subject].avg < 60).slice(0, 3).map((subject) => `${subject} (${subjectStats[subject].avg}%)`)}
          emptyText="All subjects above 60% - excellent work!"
        />
      </div>
    </div>
  );
};

const StatCard = ({ icon, title, value, subtitle, color }) => (
  <div className="bg-white p-6 rounded-xl border border-stone-200 shadow-sm hover:shadow-md transition-shadow">
    <div className={`w-12 h-12 rounded-lg ${colorPalette[color]} border flex items-center justify-center mb-4`}>{icon}</div>
    <div className="text-xs font-bold text-stone-400 uppercase mb-1">{title}</div>
    <div className="text-3xl font-bold text-stone-900 mb-1">{value}</div>
    <div className="text-xs text-stone-500">{subtitle}</div>
  </div>
);

const InsightCard = ({ title, icon, color, border, items, emptyText }) => (
  <div className={`bg-gradient-to-br ${color} rounded-xl border ${border} shadow-sm p-6`}>
    <h4 className="font-bold text-stone-900 mb-3 flex items-center gap-2">
      {icon}
      {title}
    </h4>
    <div className="space-y-2 text-sm">
      {items.length > 0 ? (
        items.map((item) => (
          <div key={item} className="flex items-center gap-2 text-stone-800">
            <CheckCircle className="w-4 h-4 text-emerald-600" />
            <span>{item}</span>
          </div>
        ))
      ) : (
        <p className="text-stone-700 italic">{emptyText}</p>
      )}
    </div>
  </div>
);

const Footer = ({ navigate }) => (
  <footer className="bg-white text-stone-600 py-12 border-t border-stone-200">
    <div className="max-w-7xl mx-auto px-6 grid md:grid-cols-4 gap-8">
      <div className="col-span-1 md:col-span-2">
        <div className="flex items-center gap-2 mb-4 text-stone-900">
          <div className="w-6 h-6 bg-amber-700 rounded flex items-center justify-center text-xs font-bold text-white">FR</div>
          <span className="font-bold">First-Rep</span>
        </div>
        <p className="text-sm max-w-xs mb-4">
          Precision legal pedagogy. <br />
          Built for the United States Bar Exam.
        </p>
        <div className="flex gap-2">
          <button className="p-2 bg-stone-100 rounded hover:bg-stone-200 transition-colors" aria-label="Share">
            <Share2 className="w-4 h-4" />
          </button>
          <button className="p-2 bg-stone-100 rounded hover:bg-stone-200 transition-colors" aria-label="External link">
            <ExternalLink className="w-4 h-4" />
          </button>
        </div>
      </div>
      <div>
        <h4 className="text-stone-900 font-bold mb-4">Tools</h4>
        <ul className="space-y-2 text-sm">
          <li><button onClick={() => navigate("planner")} className="hover:text-amber-700">Syllabus Architect</button></li>
          <li><button onClick={() => navigate("hypo")} className="hover:text-amber-700">Issue Spotter</button></li>
          <li><button onClick={() => navigate("demo")} className="hover:text-amber-700">Flashcards</button></li>
          <li><button onClick={() => navigate("analytics")} className="hover:text-amber-700">Analytics</button></li>
        </ul>
      </div>
      <div>
        <h4 className="text-stone-900 font-bold mb-4">Legal</h4>
        <ul className="space-y-2 text-sm">
          <li><a href="#" className="hover:text-amber-700">Terms of Use</a></li>
          <li><a href="#" className="hover:text-amber-700">Privacy Policy</a></li>
          <li><a href="#" className="hover:text-amber-700">Data & Security</a></li>
        </ul>
      </div>
    </div>
    <div className="max-w-7xl mx-auto px-6 pt-8 mt-8 border-t border-stone-100 text-xs text-center md:text-left text-stone-400">
      &copy; 2025 First-Rep. Not affiliated with the NCBE. Made with precision for legal scholars.
    </div>
  </footer>
);

const styles = `
  .custom-scrollbar::-webkit-scrollbar {
    width: 6px;
  }
  .custom-scrollbar::-webkit-scrollbar-track {
    background: #f5f5f4;
    border-radius: 3px;
  }
  .custom-scrollbar::-webkit-scrollbar-thumb {
    background: #d6d3d1;
    border-radius: 3px;
  }
  .custom-scrollbar::-webkit-scrollbar-thumb:hover {
    background: #a8a29e;
  }
  .perspective-1000 {
    perspective: 1000px;
  }
  .rotate-y-180 {
    transform: rotateY(180deg);
  }
  .backface-hidden {
    backface-visibility: hidden;
    -webkit-backface-visibility: hidden;
  }
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }
  @keyframes slideUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
  }
  .animate-fadeIn {
    animation: fadeIn 0.4s ease-out;
  }
  .animate-slideUp {
    animation: slideUp 0.3s ease-out;
  }
`;

if (typeof document !== "undefined") {
  const styleSheet = document.createElement("style");
  styleSheet.textContent = styles;
  document.head.appendChild(styleSheet);
}

export default App;
