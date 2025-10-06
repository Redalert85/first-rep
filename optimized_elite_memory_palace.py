"""
Optimized Elite Memory Palace System
===================================

A single-file, runnable, **data-optimized** memory palace engine with:
- R-tree-like spatial index (minimal but functional): O(log n) insertion, fast k-NN queries
- Columnar compressed storage (zlib + NumPy) with ~47%+ memory savings (target)
- Cross‑modal coherence engine (stubbed but complete API)
- Adaptive neuroplasticity review scheduler
- Predictive analytics (simplified ensemble)

Run (demo):
    python optimized_elite_memory_palace.py --demo

Run tests:
    python optimized_elite_memory_palace.py --test

Requires:
    Python 3.10+
    numpy

Notes:
- **Fixed event loop bug**: uses a safe async runner that works even if an event loop is already running (e.g., notebooks/sandboxes). No more `RuntimeError: asyncio.run() cannot be called from a running event loop`.
- The spatial index is a compact, educational R-tree (Guttman-style) variant suitable for thousands of points.
- "Performance claims" are goals/targets. This file focuses on correctness + clean API so you can extend/benchmark.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import math
import random
import threading
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass, field
from collections import defaultdict

import numpy as np

# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ElitePalace")

# =============================================================================
# Utilities: Safe async runner (handles already-running event loops)
# =============================================================================

def _safe_asyncio_run(coro):
    """Run a coroutine safely.

    - If no loop is running, uses asyncio.run(coro).
    - If a loop is running (e.g., Jupyter/REPL/sandbox), spins up a new thread
      and runs the coroutine to completion in its own fresh event loop.
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        # No running loop -> safe
        return asyncio.run(coro)
    else:
        # A loop is running. Run the coroutine to completion in a separate thread.
        result: Dict[str, Any] = {}
        error: Dict[str, BaseException] = {}

        def _runner():
            try:
                result["value"] = asyncio.run(coro)
            except BaseException as exc:  # propagate exception to main thread
                error["exc"] = exc

        t = threading.Thread(target=_runner, daemon=True)
        t.start()
        t.join()
        if "exc" in error:
            raise error["exc"]
        return result.get("value")

# =============================================================================
# Spatial Index (Minimal R-tree)
# =============================================================================

BBox = Tuple[float, float, float, float, float, float]
Point3D = Tuple[float, float, float]

@dataclass
class SpatialEntry:
    location_id: str
    bbox: BBox
    position: Point3D

class SpatialLeafNode:
    def __init__(self):
        self.entries: List[SpatialEntry] = []
        self.bbox: Optional[BBox] = None

class SpatialInternalNode:
    def __init__(self):
        self.children: List[Union[SpatialLeafNode, 'SpatialInternalNode']] = []
        self.bbox: Optional[BBox] = None

class OptimizedSpatialIndex:
    """Tiny, self-contained R-tree-ish index for 3D points.
    Supports add_location() and k-NN via bbox pruning.
    
    This implementation **propagates splits upward** (root included),
    so no node silently exceeds `max_entries`.
    """

    def __init__(self, max_entries: int = 16):
        self.max_entries = max_entries
        self.root: Union[SpatialLeafNode, SpatialInternalNode, None] = None
        self.size = 0

    # --------------- Public API ---------------
    def add_location(self, location_id: str, position: Point3D) -> None:
        bbox = self._point_to_bbox(position)
        entry = SpatialEntry(location_id, bbox, position)
        if self.root is None:
            self.root = SpatialLeafNode()
        maybe_split = self._insert(self.root, entry)
        if maybe_split is not None:
            # Root split: promote returned internal node as new root
            self.root = maybe_split
        self.size += 1
        self._recalc_bbox_upwards(self.root)

    def find_nearest(self, position: Point3D, k: int = 5) -> List[Tuple[str, float]]:
        if self.root is None:
            return []
        candidates: List[Tuple[str, Point3D]] = []
        self._nearest(self.root, position, candidates, k * 4)
        dists = [(loc_id, self._dist(position, p)) for loc_id, p in candidates]
        dists.sort(key=lambda t: t[1])
        # De-dup in case of overlapping nodes
        seen = set()
        out = []
        for loc_id, d in dists:
            if loc_id in seen:
                continue
            seen.add(loc_id)
            out.append((loc_id, d))
            if len(out) >= k:
                break
        return out

    # --------------- Core ops ---------------
    def _insert(self, node: Union[SpatialLeafNode, SpatialInternalNode], entry: SpatialEntry) -> Optional[SpatialInternalNode]:
        """Insert entry and **return a new internal node if `node` splits**, else None.
        This lets callers propagate splits up to the root.
        """
        if isinstance(node, SpatialLeafNode):
            node.entries.append(entry)
            node.bbox = self._expand_bbox(node.bbox, entry.bbox)
            if len(node.entries) > self.max_entries:
                return self._split_leaf(node)
            return None

        # Internal node: choose child with minimal bbox enlargement
        child = min(node.children, key=lambda c: self._bbox_enlargement(self._get_bbox(c), entry.bbox))
        child_split = self._insert(child, entry)

        # If child split, replace child with the two children of returned internal node
        if child_split is not None:
            idx = node.children.index(child)
            node.children.pop(idx)
            node.children[idx:idx] = child_split.children

        # Recalculate bbox
        node.bbox = self._calc_bbox(node)

        # Split this node if it now exceeds capacity
        if len(node.children) > self.max_entries:
            return self._split_internal(node)
        return None

    def _nearest(self, node: Union[SpatialLeafNode, SpatialInternalNode], q: Point3D,
                 out: List[Tuple[str, Point3D]], max_candidates: int) -> None:
        if isinstance(node, SpatialLeafNode):
            out.extend((e.location_id, e.position) for e in node.entries)
            return
        # sort children by bbox distance to query
        children = sorted(node.children, key=lambda c: self._bbox_point_dist(self._get_bbox(c), q))
        for ch in children:
            if len(out) >= max_candidates:
                break
            self._nearest(ch, q, out, max_candidates)

    # --------------- Splitting helpers ---------------
    def _split_leaf(self, leaf: SpatialLeafNode) -> SpatialInternalNode:
        # Linear split heuristic: pick two farthest entries as seeds
        entries = leaf.entries
        i1, i2 = self._farthest_pair(entries)
        g1, g2 = SpatialLeafNode(), SpatialLeafNode()
        g1.entries.append(entries[i1]); g2.entries.append(entries[i2])
        for idx, e in enumerate(entries):
            if idx in (i1, i2):
                continue
            # Choose group with least enlargement cost
            cost1 = self._bbox_enlargement(self._calc_bbox(g1), e.bbox)
            cost2 = self._bbox_enlargement(self._calc_bbox(g2), e.bbox)
            (g1 if cost1 <= cost2 else g2).entries.append(e)
        g1.bbox = self._calc_bbox(g1)
        g2.bbox = self._calc_bbox(g2)
        parent = SpatialInternalNode()
        parent.children = [g1, g2]
        parent.bbox = self._expand_bbox(g1.bbox, g2.bbox)
        return parent

    def _split_internal(self, node: SpatialInternalNode) -> SpatialInternalNode:
        children = node.children
        # seeds = farthest bbox pair
        i1, i2 = self._farthest_bbox_pair([self._get_bbox(c) for c in children])
        g1, g2 = SpatialInternalNode(), SpatialInternalNode()
        g1.children.append(children[i1]); g2.children.append(children[i2])
        for idx, c in enumerate(children):
            if idx in (i1, i2):
                continue
            cost1 = self._bbox_enlargement(self._calc_bbox(g1), self._get_bbox(c))
            cost2 = self._bbox_enlargement(self._calc_bbox(g2), self._get_bbox(c))
            (g1 if cost1 <= cost2 else g2).children.append(c)
        g1.bbox = self._calc_bbox(g1)
        g2.bbox = self._calc_bbox(g2)
        parent = SpatialInternalNode()
        parent.children = [g1, g2]
        parent.bbox = self._expand_bbox(g1.bbox, g2.bbox)
        return parent

    def _recalc_bbox_upwards(self, node: Union[SpatialLeafNode, SpatialInternalNode]) -> Optional[BBox]:
        if isinstance(node, SpatialLeafNode):
            node.bbox = self._calc_bbox(node)
            return node.bbox
        # internal
        for ch in node.children:
            self._recalc_bbox_upwards(ch)
        node.bbox = self._calc_bbox(node)
        return node.bbox

    # --------------- Geometry helpers ---------------
    def _point_to_bbox(self, p: Point3D, m: float = 0.05) -> BBox:
        x, y, z = p
        return (x - m, y - m, z - m, x + m, y + m, z + m)

    def _expand_bbox(self, a: Optional[BBox], b: Optional[BBox]) -> Optional[BBox]:
        if a is None:
            return b
        if b is None:
            return a
        return (
            min(a[0], b[0]), min(a[1], b[1]), min(a[2], b[2]),
            max(a[3], b[3]), max(a[4], b[4]), max(a[5], b[5])
        )

    def _get_bbox(self, node: Union[SpatialLeafNode, SpatialInternalNode]) -> Optional[BBox]:
        # Return None instead of a zero-sized origin bbox to avoid biasing heuristics
        return node.bbox

    def _calc_bbox(self, node: Union[SpatialLeafNode, SpatialInternalNode]) -> Optional[BBox]:
        if isinstance(node, SpatialLeafNode):
            if not node.entries:
                return None
            b = node.entries[0].bbox
            for e in node.entries[1:]:
                b = self._expand_bbox(b, e.bbox)
            return b
        if not node.children:
            return None
        b = self._get_bbox(node.children[0])
        for ch in node.children[1:]:
            b = self._expand_bbox(b, self._get_bbox(ch))
        return b

    def _bbox_enlargement(self, a: Optional[BBox], b: Optional[BBox]) -> float:
        if a is None:
            return self._bbox_volume(b)
        if b is None:
            return 0.0
        v_old = self._bbox_volume(a)
        v_new = self._bbox_volume(self._expand_bbox(a, b))
        return v_new - v_old

    def _bbox_volume(self, b: Optional[BBox]) -> float:
        if b is None:
            return 0.0
        dx = max(0.0, b[3] - b[0])
        dy = max(0.0, b[4] - b[1])
        dz = max(0.0, b[5] - b[2])
        return dx * dy * dz

    def _bbox_point_dist(self, b: Optional[BBox], p: Point3D) -> float:
        if b is None:
            # Treat empty as zero distance so children without bbox are visited early; they’ll expand soon.
            return 0.0
        x, y, z = p
        min_x, min_y, min_z, max_x, max_y, max_z = b
        dx = max(0, min_x - x, x - max_x)
        dy = max(0, min_y - y, y - max_y)
        dz = max(0, min_z - z, z - max_z)
        return math.sqrt(dx*dx + dy*dy + dz*dz)

    def _dist(self, a: Point3D, b: Point3D) -> float:
        return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2)

    def _farthest_pair(self, entries: List[SpatialEntry]) -> Tuple[int, int]:
        n = len(entries)
        if n <= 1:
            return 0, 0
        best = (0, 1)
        best_d = -1.0
        for i in range(n):
            for j in range(i+1, n):
                d = self._dist(entries[i].position, entries[j].position)
                if d > best_d:
                    best_d = d
                    best = (i, j)
        return best

    def _farthest_bbox_pair(self, boxes: List[Optional[BBox]]) -> Tuple[int, int]:
        def center(b: Optional[BBox]):
            if b is None:
                return (0.0, 0.0, 0.0)
            return ((b[0]+b[3])/2, (b[1]+b[4])/2, (b[2]+b[5])/2)
        n = len(boxes)
        if n <= 1:
            return 0, 0
        best = (0, 1)
        best_d = -1.0
        for i in range(n):
            ci = center(boxes[i])
            for j in range(i+1, n):
                cj = center(boxes[j])
                d = self._dist(ci, cj)
                if d > best_d:
                    best_d = d
                    best = (i, j)
        return best

# =============================================================================

# Columnar Compressed Storage
# =============================================================================

class RingBuffer:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.buffer = [None] * capacity
        self.head = 0
        self.size = 0
        self._stats_cache = None
        self._cache_dirty = True

    def append(self, item: Any) -> None:
        self.buffer[self.head] = item
        self.head = (self.head + 1) % self.capacity
        if self.size < self.capacity:
            self.size += 1
        self._cache_dirty = True

    def get_recent(self, count: Optional[int] = None) -> List[Any]:
        if count is None:
            count = self.size
        count = min(count, self.size)
        out = []
        for i in range(count):
            idx = (self.head - 1 - i) % self.capacity
            v = self.buffer[idx]
            if v is not None:
                out.append(v)
        return out

class CompressedLocationStorage:
    def __init__(self):
        self.location_ids: List[str] = []
        self.content_compressed: List[bytes] = []
        self.positions_x = np.array([], dtype=np.float32)
        self.positions_y = np.array([], dtype=np.float32)
        self.positions_z = np.array([], dtype=np.float32)
        self.bizarreness_factors = np.array([], dtype=np.float32)
        self.emotional_intensities = np.array([], dtype=np.float32)
        self.creation_timestamps = np.array([], dtype=np.int64)
        self.sensory_encodings = np.array([], dtype=np.uint64)
        self.id_to_index: Dict[str, int] = {}
        self.performance_histories: Dict[str, RingBuffer] = {}
        self.performance_buffer_size = 32

    # ---- public ----
    def add_location(self, location_id: str, content: str, position: Point3D,
                     bizarreness: float, emotional: float, sensory_encoding: Dict[str, Any]) -> int:
        import zlib
        compressed = zlib.compress(content.encode('utf-8'), level=6)
        sensory_bits = self._pack_sensory_encoding(sensory_encoding)
        idx = len(self.location_ids)
        self.location_ids.append(location_id)
        self.content_compressed.append(compressed)
        self.positions_x = np.append(self.positions_x, position[0])
        self.positions_y = np.append(self.positions_y, position[1])
        self.positions_z = np.append(self.positions_z, position[2])
        self.bizarreness_factors = np.append(self.bizarreness_factors, bizarreness)
        self.emotional_intensities = np.append(self.emotional_intensities, emotional)
        self.creation_timestamps = np.append(self.creation_timestamps, int(datetime.now().timestamp()))
        self.sensory_encodings = np.append(self.sensory_encodings, sensory_bits)
        self.id_to_index[location_id] = idx
        self.performance_histories[location_id] = RingBuffer(self.performance_buffer_size)
        return idx

    def get_location(self, location_id: str) -> Optional[Dict[str, Any]]:
        if location_id not in self.id_to_index:
            return None
        import zlib
        i = self.id_to_index[location_id]
        content = zlib.decompress(self.content_compressed[i]).decode('utf-8')
        return {
            'id': location_id,
            'content': content,
            'position': (float(self.positions_x[i]), float(self.positions_y[i]), float(self.positions_z[i])),
            'bizarreness_factor': float(self.bizarreness_factors[i]),
            'emotional_intensity': float(self.emotional_intensities[i]),
            'created_at': datetime.fromtimestamp(int(self.creation_timestamps[i])),
            'sensory_encoding': self._unpack_sensory_encoding(int(self.sensory_encodings[i]))
        }

    def bulk_ids(self) -> List[str]:
        return list(self.location_ids)

    def bulk_update_performance(self, updates: List[Tuple[str, Dict[str, Any]]]) -> None:
        for loc_id, data in updates:
            if loc_id in self.performance_histories:
                self.performance_histories[loc_id].append(data)

    # ---- packing ----
    def _pack_sensory_encoding(self, sensory: Dict[str, Any]) -> int:
        channels = ['visual', 'auditory', 'kinesthetic', 'olfactory', 'gustatory', 'emotional', 'spatial', 'temporal', 'synesthetic']
        val = 0
        for i, ch in enumerate(channels):
            v = hash(str(sensory.get(ch, 0))) % 128
            val |= (v << (i * 7))
        return val

    def _unpack_sensory_encoding(self, packed: int) -> Dict[str, int]:
        channels = ['visual', 'auditory', 'kinesthetic', 'olfactory', 'gustatory', 'emotional', 'spatial', 'temporal', 'synesthetic']
        out = {}
        for i, ch in enumerate(channels):
            out[ch] = (packed >> (i * 7)) & 0x7F
        return out

# =============================================================================
# Cross-Modal Coherence (lightweight but complete)
# =============================================================================

@dataclass
class SensoryProfile:
    user_id: str
    visual_intensity: float = 0.8
    auditory_sensitivity: float = 0.7
    haptic_preference: float = 0.6
    olfactory_sensitivity: float = 0.5
    dominant_modalities: List[str] = field(default_factory=lambda: ['visual', 'auditory'])
    synesthetic_experiences: bool = False
    processing_speed: float = 1.0

@dataclass
class CoherentMultiModalEncoding:
    visual: Dict[str, Any]
    auditory: Dict[str, Any]
    haptic: Dict[str, Any]
    olfactory: Dict[str, Any]
    coherence_scores: Dict[str, float]
    semantic_consistency: float
    user_profile_alignment: float

class EmotionalValenceAnalyzer:
    def analyze(self, content: str) -> float:
        pos = ['excellent', 'good', 'beneficial', 'advantage', 'success', 'rights', 'freedom']
        neg = ['bad', 'illegal', 'penalty', 'violation', 'breach', 'damages', 'liability']
        c = content.lower()
        p = sum(c.count(w) for w in pos)
        n = sum(c.count(w) for w in neg)
        total = max(1, len(content.split())/10)
        return max(-1.0, min(1.0, (p - n) / total))

class SemanticCategoryAnalyzer:
    def classify(self, content: str) -> str:
        c = content.lower()
        categories = {
            'legal': ['law', 'court', 'judge', 'statute', 'legal', 'judicial'],
            'property': ['property', 'real estate', 'land', 'ownership', 'deed'],
            'contract': ['contract', 'agreement', 'obligation', 'terms', 'parties'],
            'tort': ['negligence', 'liability', 'damages', 'injury', 'duty'],
            'criminal': ['crime', 'criminal', 'defendant', 'prosecution', 'guilty']
        }
        scores = {k: sum(c.count(w) for w in words) for k, words in categories.items()}
        best = max(scores, key=scores.get)
        return best if scores[best] > 0 else 'general'

class ComplexityAnalyzer:
    def analyze(self, content: str) -> float:
        words = content.split()
        if not words:
            return 0.0
        avg_len = sum(len(w) for w in words) / len(words)
        sentences = content.count('.') + content.count('!') + content.count('?') + 1
        avg_sent = len(words) / sentences
        complex_terms = ['pursuant', 'heretofore', 'notwithstanding', 'whereas', 'thereof']
        ratio = sum(1 for t in complex_terms if t in content.lower()) / max(1, len(words))
        val = (avg_len - 4)/6 * 0.3 + (avg_sent - 10)/20 * 0.4 + ratio * 10 * 0.3
        return max(0.0, min(1.0, val))

class UrgencyDetector:
    def detect(self, content: str) -> float:
        urg = ['immediate', 'urgent', 'critical', 'deadline', 'asap', 'emergency', 'must']
        mod = ['important', 'should', 'recommended', 'advised', 'timely']
        c = content.lower()
        u = sum(1 for w in urg if w in c)
        m = sum(1 for w in mod if w in c)
        if u:
            return min(1.0, 0.8 + 0.05 * u)
        if m:
            return min(1.0, 0.4 + 0.1 * m)
        return 0.2

class CrossModalCoherenceEngine:
    def __init__(self):
        self.content_analyzers = {
            'emotional_valence': EmotionalValenceAnalyzer(),
            'semantic_category': SemanticCategoryAnalyzer(),
            'complexity_analyzer': ComplexityAnalyzer(),
            'urgency_detector': UrgencyDetector(),
        }
        self.user_sensory_profiles: Dict[str, SensoryProfile] = {}

    async def generate_coherent_encoding(self, content: str, user_id: str,
                                         context: Optional[Dict[str, Any]] = None) -> CoherentMultiModalEncoding:
        val = self.content_analyzers['emotional_valence'].analyze(content)
        cat = self.content_analyzers['semantic_category'].classify(content)
        cmpx = self.content_analyzers['complexity_analyzer'].analyze(content)
        urg = self.content_analyzers['urgency_detector'].detect(content)
        profile = self.user_sensory_profiles.get(user_id, SensoryProfile(user_id))

        visual = self._visual_block(val, cat, cmpx, urg, profile)
        auditory = self._auditory_block(val, cat, cmpx, urg, profile)
        haptic = {'pattern': 'steady' if urg < 0.5 else 'pulse', 'intensity': 0.5 + 0.3*urg}
        olfactory = {'note': 'neutral', 'intensity': 0.2 + 0.1*val}

        coherence = {
            'visual_auditory': 0.85 - 0.1*abs(val),
            'auditory_haptic': 0.80 - 0.05*abs(urg-0.5),
            'visual_olfactory': 0.75,
            'cross_modal_temporal': 0.90,
        }
        semantic_consistency = 0.8 - 0.1*abs(0.5-cmpx)
        profile_alignment = 0.8 if 'visual' in profile.dominant_modalities else 0.7

        return CoherentMultiModalEncoding(
            visual=visual, auditory=auditory, haptic=haptic, olfactory=olfactory,
            coherence_scores=coherence, semantic_consistency=semantic_consistency,
            user_profile_alignment=profile_alignment,
        )

    # --- simple mappings ---
    def _visual_block(self, val, cat, cmpx, urg, profile) -> Dict[str, Any]:
        color_map = {
            'legal': 'gold', 'property': 'green', 'contract': 'blue', 'tort': 'purple', 'criminal': 'red', 'general': 'silver'
        }
        color = color_map.get(cat, 'silver')
        shapes = ['simple', 'circular', 'clean'] if cmpx < 0.4 else ['angular', 'structured', 'balanced'] if cmpx < 0.7 else ['complex_geometric', 'layered']
        motion = ['calm', 'stable'] if urg < 0.3 else ['steady', 'rhythmic'] if urg < 0.7 else ['rapid', 'pulsing']
        intensity = max(0.2, min(1.0, profile.visual_intensity * (0.6 + 0.3*max(0, val))))
        return {
            'primary_color': color,
            'shapes': shapes,
            'motion_patterns': motion,
            'intensity': intensity,
        }

    def _auditory_block(self, val, cat, cmpx, urg, profile) -> Dict[str, Any]:
        tone = 'warm_major' if val > 0.5 else 'tense_minor' if val < -0.3 else 'neutral_modal'
        rhythm = 'accelerating' if urg > 0.7 else 'complex_syncopated' if cmpx > 0.6 else 'steady'
        tempo = (140 + urg*40) if urg > 0.7 else (100 + cmpx*30) if cmpx > 0.6 else (80 + max(0, val)*40)
        return {
            'tone': tone,
            'rhythm': rhythm,
            'tempo': tempo * profile.auditory_sensitivity,
            'timbre': ['authoritative', 'clear'] if cat == 'legal' else ['balanced', 'articulate']
        }

# =============================================================================
# Adaptive Neuroplasticity
# =============================================================================

@dataclass
class CognitiveProfile:
    user_id: str
    baseline_strength: float  # 0.3-1.2
    forgetting_rate: float    # 0.1-1.0 (higher=faster)
    emotional_sensitivity: float  # 0-0.5
    interference_susceptibility: float  # 0-0.5
    consolidation_efficiency: float  # 0-1.0
    calibration_sessions: int = field(default=0)
    last_updated: datetime = field(default_factory=datetime.now)

class AdaptiveNeuroplasticityEngine:
    def __init__(self):
        self.consolidation_windows = {
            'immediate': timedelta(minutes=10),
            'protein_synthesis': timedelta(minutes=20),
            'early_ltp': timedelta(hours=2),
            'late_ltp': timedelta(hours=6),
            'systems_consolidation': timedelta(days=1),
            'schema_integration': timedelta(days=7),
            'semantic_consolidation': timedelta(days=30),
        }
        self.user_profiles: Dict[str, CognitiveProfile] = {}

    def calibrate_user_profile(self, user_id: str, performance_history: List[Dict[str, Any]]) -> CognitiveProfile:
        if len(performance_history) < 10:
            profile = CognitiveProfile(
                user_id=user_id,
                baseline_strength=0.75,
                forgetting_rate=0.5,
                emotional_sensitivity=0.3,
                interference_susceptibility=0.2,
                consolidation_efficiency=0.7,
            )
        else:
            # Simplified data-driven calibration
            acc = [p.get('accuracy', 0.5) for p in performance_history[-20:]]
            baseline_strength = max(0.3, min(1.2, float(np.mean(acc))))
            profile = CognitiveProfile(
                user_id=user_id,
                baseline_strength=baseline_strength,
                forgetting_rate=0.5,
                emotional_sensitivity=0.3,
                interference_susceptibility=0.2,
                consolidation_efficiency=0.7,
            )
        self.user_profiles[user_id] = profile
        return profile

    def calculate_retention_probability(self, location_data: Dict[str, Any], time_delta: timedelta, user_id: str) -> float:
        profile = self.user_profiles.get(user_id)
        if not profile:
            profile = self.calibrate_user_profile(user_id, [])
        emotional_intensity = location_data.get('emotional_intensity', 0) / 10
        biz = location_data.get('bizarreness_factor', 0) / 10
        S = profile.baseline_strength
        difficulty = max(0.5, location_data.get('difficulty_score', 1.0))
        D = (1.0 / profile.forgetting_rate) * (2.0 - difficulty)
        t_days = time_delta.total_seconds() / 86400.0
        base = S * math.exp(-t_days / max(0.25, D))
        boost = profile.emotional_sensitivity * (emotional_intensity + biz) * 0.5
        retention = base * (1 + boost)
        return float(max(0.01, min(0.99, retention)))

    def optimize_review_schedule(self, location_data: Dict[str, Any], user_id: str, target_retention: float = 0.85) -> List[datetime]:
        now = datetime.now()
        schedule = []
        intervals = [
            timedelta(minutes=10), timedelta(hours=1), timedelta(hours=8), timedelta(days=1),
            timedelta(days=3), timedelta(days=7), timedelta(days=14), timedelta(days=30)
        ]
        cur = now
        for base in intervals:
            pred = self.calculate_retention_probability(location_data, base, user_id)
            factor = max(0.2, min(2.0, pred / max(0.05, target_retention)))
            adj = base * factor
            schedule.append(cur + adj)
            cur = cur + adj
        return schedule

# =============================================================================
# Predictive Analytics (lightweight)
# =============================================================================

class PredictiveAnalyticsEngine:
    async def analyze_session_performance(self, session_data: Dict[str, Any], user_history: List[Dict[str, Any]]):
        acc = session_data.get('accuracy', 0.5)
        rt = session_data.get('average_response_time', 2.0)
        freq = min(1.0, len([s for s in user_history if (session_data['timestamp'] - s.get('timestamp', session_data['timestamp'])).days <= 7]) / 7.0) if user_history else 0.0
        retention_probability = 0.4*acc + 0.3*(1.0 - min(1.0, rt/10.0)) + 0.3*freq
        return {
            'retention_prediction': {
                'retention_probability': retention_probability,
                'confidence_interval': (max(0, retention_probability - 0.1), min(1, retention_probability + 0.1)),
            },
            'next_session_recommendations': {
                'items': 20 if acc >= 0.8 else 12,
                'focus': 'speed' if acc >= 0.85 else 'accuracy',
                'target_accuracy': 0.9,
            }
        }

# =============================================================================
# Main System
# =============================================================================

class OptimizedEliteMemoryPalaceSystem:
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        config = config or {}
        self.spatial_index = OptimizedSpatialIndex(max_entries=config.get('rtree_max_entries', 16))
        self.storage_engine = CompressedLocationStorage()
        self.neuroplasticity_engine = AdaptiveNeuroplasticityEngine()
        self.coherence_engine = CrossModalCoherenceEngine()
        self.analytics_engine = PredictiveAnalyticsEngine()
        self.palaces: Dict[str, Dict[str, Any]] = {}
        self.performance_metrics = {'spatial_query_times': [], 'encoding_times': []}
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
        logger.info("OptimizedEliteMemoryPalaceSystem ready")

    async def create_optimized_palace(self, name: str, category: str, user_id: str = 'default_user', layout_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        layout_config = layout_config or {'type': 'adaptive_radial', 'initial_capacity': 1000, 'expansion_strategy': 'organic_growth'}
        pid = hashlib.md5(f"{name}{datetime.now().isoformat()}".encode()).hexdigest()[:12]
        palace = {'id': pid, 'name': name, 'category': category, 'user_id': user_id, 'layout_config': layout_config, 'created_at': datetime.now(), 'location_count': 0, 'optimization_metrics': {'encoding_coherence': 0.0, 'retention_prediction': 0.0}}
        self.palaces[pid] = palace
        if user_id not in self.coherence_engine.user_sensory_profiles:
            self.coherence_engine.user_sensory_profiles[user_id] = SensoryProfile(user_id=user_id)
        if user_id not in self.neuroplasticity_engine.user_profiles:
            self.neuroplasticity_engine.calibrate_user_profile(user_id, [])
        return palace

    async def add_optimized_location(self, palace_id: str, content: str, position: Optional[Point3D] = None, user_id: str = 'default_user') -> Dict[str, Any]:
        if palace_id not in self.palaces:
            raise ValueError(f"Palace {palace_id} not found")
        palace = self.palaces[palace_id]
        if position is None:
            position = self._generate_position(palace['location_count'])
        encoding = await self.coherence_engine.generate_coherent_encoding(content, user_id, {'palace': palace})
        semantic_features = {
            'emotional_intensity': random.uniform(0, 10),
            'bizarreness_factor': random.uniform(0, 10),
            'difficulty_score': max(0.5, min(1.5, len(content.split())/25.0)),
            'performance_history': []
        }
        loc_id = hashlib.md5(f"{content}{datetime.now()}".encode()).hexdigest()[:8]
        self.storage_engine.add_location(loc_id, content, position, semantic_features['bizarreness_factor'], semantic_features['emotional_intensity'], encoding.visual)
        self.spatial_index.add_location(loc_id, position)
        review_schedule = self.neuroplasticity_engine.optimize_review_schedule(semantic_features, user_id, target_retention=0.90)
        palace['location_count'] += 1
        return {
            'location_id': loc_id,
            'position': position,
            'coherent_encoding': encoding,
            'review_schedule': review_schedule,
            'semantic_features': semantic_features,
        }

    async def practice_optimized_recall(self, palace_id: str, user_id: str = 'default_user', session_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if palace_id not in self.palaces:
            raise ValueError(f"Palace {palace_id} not found")
        palace = self.palaces[palace_id]
        session_config = session_config or {'max_items': 20, 'time_limit_seconds': 300}
        session_id = hashlib.md5(f"{palace_id}{user_id}{datetime.now()}".encode()).hexdigest()[:8]
        start = datetime.now()
        # choose items nearest to origin for demo
        ids = self.storage_engine.bulk_ids()[: session_config['max_items']]
        attempted = 0
        correct = 0
        acc_scores = []
        rts = []
        for loc_id in ids:
            data = self.storage_engine.get_location(loc_id)
            if not data:
                continue
            t_since = datetime.now() - data['created_at']
            # plug in difficulty
            data['difficulty_score'] = max(0.5, min(1.5, len(data['content'].split())/25.0))
            rp = self.neuroplasticity_engine.calculate_retention_probability(data, t_since, user_id)
            acc = max(0.0, min(1.0, rp + random.uniform(-0.1, 0.1)))
            rt = max(0.4, 2.0 * (1.5 - rp) + random.uniform(-0.3, 0.3))
            attempted += 1
            acc_scores.append(acc)
            rts.append(rt)
            if acc >= 0.8:
                correct += 1
            self.storage_engine.bulk_update_performance([(loc_id, {'timestamp': datetime.now(), 'accuracy': acc, 'response_time': rt, 'retention_probability': rp})])
        total = (datetime.now() - start).total_seconds()
        avg_acc = float(np.mean(acc_scores)) if acc_scores else 0.0
        avg_rt = float(np.mean(rts)) if rts else 0.0
        ipm = (attempted / total * 60) if total > 0 else 0.0
        analytics = await self.analytics_engine.analyze_session_performance({'session_id': session_id, 'timestamp': start, 'duration_seconds': total, 'items_attempted': attempted, 'accuracy': avg_acc, 'average_response_time': avg_rt, 'palace_size': palace['location_count'], 'session_type': 'practice'}, [])
        palace['optimization_metrics']['retention_prediction'] = analytics['retention_prediction']['retention_probability']
        palace['optimization_metrics']['encoding_coherence'] = 0.85
        return {
            'session_id': session_id,
            'palace_name': palace['name'],
            'duration_seconds': total,
            'items_attempted': attempted,
            'correct_recalls': correct,
            'accuracy_percentage': avg_acc * 100,
            'average_response_time': avg_rt,
            'items_per_minute': ipm,
            'predictive_analytics': analytics,
        }

    async def get_optimization_report(self, palace_id: str) -> Dict[str, Any]:
        if palace_id not in self.palaces:
            raise ValueError(f"Palace {palace_id} not found")
        palace = self.palaces[palace_id]
        return {
            'palace_overview': {
                'name': palace['name'], 'category': palace['category'], 'location_count': palace['location_count'], 'created_at': palace['created_at'].isoformat()
            },
            'performance_summary': {
                'multi_modal_coherence': f"{palace['optimization_metrics']['encoding_coherence']*100:.1f}%",
                'retention_prediction': f"{palace['optimization_metrics']['retention_prediction']*100:.1f}%",
            }
        }

    # --- helpers ---
    def _generate_position(self, count: int) -> Point3D:
        angle = count * (2 * math.pi / 12)
        radius = 5 + (count // 12) * 3
        height = (count % 6) * 2
        return (radius * math.cos(angle), radius * math.sin(angle), height)

# =============================================================================
# Demonstration
# =============================================================================

async def demonstrate():
    print("\n🚀 OPTIMIZED ELITE MEMORY PALACE SYSTEM DEMO\n" + "="*60)
    sys = OptimizedEliteMemoryPalaceSystem()
    palace = await sys.create_optimized_palace("Advanced Property Law Palace", "Legal Studies", user_id="law_student_001")
    print(f"Created palace: {palace['name']} ({palace['id']})")
    concepts = [
        "Fee Simple Absolute grants complete ownership with no conditions or limitations.",
        "Life Estate provides ownership during the life tenant's lifetime only.",
        "Adverse Possession requires hostile, actual, open, notorious, and continuous use.",
        "Joint Tenancy includes right of survivorship between co-owners.",
        "Easement grants a nonpossessory right to use another's land for a specific purpose.",
    ]
    for c in concepts:
        loc = await sys.add_optimized_location(palace['id'], c, user_id="law_student_001")
        print(f"  • Added {loc['location_id']} @ {tuple(round(v,2) for v in loc['position'])}")
    res = await sys.practice_optimized_recall(palace['id'], user_id="law_student_001")
    print(f"\nResults: accuracy={res['accuracy_percentage']:.1f}%, speed={res['items_per_minute']:.1f}/min")
    rep = await sys.get_optimization_report(palace['id'])
    print("Report:", rep['performance_summary'])

# =============================================================================
# Tests
# =============================================================================

import unittest

class TestSpatialIndex(unittest.TestCase):
    def test_nearest_simple_line(self):
        idx = OptimizedSpatialIndex(max_entries=4)
        for i in range(10):
            idx.add_location(f"id{i}", (float(i), 0.0, 0.0))
        n1 = idx.find_nearest((0.1, 0.0, 0.0), k=1)
        self.assertEqual(n1[0][0], "id0")
        n2 = idx.find_nearest((8.6, 0.0, 0.0), k=2)
        ids = [n2[0][0], n2[1][0]]
        self.assertIn("id8", ids)
        self.assertIn("id9", ids)

class TestStorage(unittest.TestCase):
    def test_add_and_get_location(self):
        store = CompressedLocationStorage()
        loc_id = "loc1234"
        content = "Test content for compression."
        store.add_location(loc_id, content, (1.0,2.0,3.0), 5.0, 7.0, {"visual": "blue"})
        got = store.get_location(loc_id)
        self.assertIsNotNone(got)
        self.assertEqual(got['id'], loc_id)
        self.assertIn("compression", got['content'])

class TestSystemFlow(unittest.IsolatedAsyncioTestCase):
    async def test_create_add_practice(self):
        sys = OptimizedEliteMemoryPalaceSystem()
        palace = await sys.create_optimized_palace("Test Palace", "UnitTests", user_id="u1")
        self.assertEqual(palace['location_count'], 0)
        loc = await sys.add_optimized_location(palace['id'], "Contract requires offer, acceptance, and consideration.", user_id="u1")
        self.assertIn('location_id', loc)
        self.assertGreater(sys.palaces[palace['id']]['location_count'], 0)
        res = await sys.practice_optimized_recall(palace['id'], user_id="u1", session_config={'max_items': 1, 'time_limit_seconds': 5})
        self.assertIn('accuracy_percentage', res)
        self.assertIn('predictive_analytics', res)

# =============================================================================
# CLI
# =============================================================================

def _main():
    parser = argparse.ArgumentParser(description="Optimized Elite Memory Palace System")
    parser.add_argument('--demo', action='store_true', help='Run demonstration (default)')
    parser.add_argument('--test', action='store_true', help='Run unit tests')
    args = parser.parse_args()

    if args.test:
        # Run unittest suite. exit=False so notebooks/sandboxes don't stop.
        unittest.main(argv=['ignored'], exit=False)
    else:
        _safe_asyncio_run(demonstrate())

if __name__ == '__main__':
    _main()
