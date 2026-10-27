import React, { useState, useEffect } from 'react';
import { 
  Eye, 
  Mic, 
  Video, 
  GitMerge, 
  Bot, 
  FileText, 
  ShieldCheck, 
  AlertOctagon, 
  Clock, 
  Layers, 
  ChevronRight,
  Crosshair,
  Sparkles
} from 'lucide-react';

export default function DashboardOverview({ selectedCaseId, setActiveTab }) {
  const [caseData, setCaseData] = useState(null);
  const [evidenceList, setEvidenceList] = useState([]);
  const [timeline, setTimeline] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCaseDetails = async () => {
      setLoading(true);
      try {
        const [cRes, eRes, tRes, sRes] = await Promise.all([
          fetch(`/api/v1/cases/${selectedCaseId}`).catch(() => null),
          fetch(`/api/v1/cases/${selectedCaseId}/evidence`).catch(() => null),
          fetch(`/api/v1/cases/${selectedCaseId}/timeline`).catch(() => null),
          fetch(`/api/v1/cases/${selectedCaseId}/stats`).catch(() => null),
        ]);

        if (cRes && cRes.ok) setCaseData(await cRes.json());
        if (eRes && eRes.ok) setEvidenceList(await eRes.json());
        if (tRes && tRes.ok) setTimeline(await tRes.json());
        if (sRes && sRes.ok) setStats(await sRes.json());
      } catch (err) {
        console.error('Error fetching dashboard details:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchCaseDetails();
  }, [selectedCaseId]);

  return (
    <div className="space-y-6">
      {/* Case Header Banner */}
      <div className="relative overflow-hidden rounded-2xl border border-cyan-900/50 bg-gradient-to-br from-[#0a1226] via-[#070b18] to-[#040711] p-6 shadow-xl">
        <div className="absolute top-0 right-0 h-48 w-48 bg-cyan-500/5 blur-3xl rounded-full pointer-events-none" />
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1.5">
            <div className="flex items-center gap-2">
              <span className="px-2.5 py-0.5 rounded text-[11px] font-mono font-bold bg-cyan-500/20 text-cyan-300 border border-cyan-500/40">
                {selectedCaseId}
              </span>
              <span className="px-2 py-0.5 rounded text-[11px] font-medium bg-emerald-500/15 text-emerald-400 border border-emerald-500/30">
                {caseData?.status || 'Active Investigation'}
              </span>
              <span className="text-xs text-slate-400 font-mono">
                {caseData?.crime_type || 'ARMED_ROBBERY_BURGLARY'}
              </span>
            </div>
            <h1 className="text-xl sm:text-2xl font-bold text-white tracking-tight">
              {caseData?.title || 'Case Investigation Workstation'}
            </h1>
            <p className="text-xs sm:text-sm text-slate-300 max-w-3xl leading-relaxed">
              {caseData?.description || 'Active multimodal investigation aggregating forensic image, audio dispatch telemetries, and surveillance video streams into unified timeline synthesis.'}
            </p>
          </div>

          <div className="flex items-center gap-2 self-start md:self-auto">
            <button
              onClick={() => setActiveTab('report')}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold bg-cyan-500 hover:bg-cyan-400 text-slate-950 transition-all shadow-lg shadow-cyan-500/20 cursor-pointer"
            >
              <FileText className="h-4 w-4" />
              <span>Export PDF Dossier</span>
            </button>
          </div>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="rounded-xl border border-slate-800/80 bg-[#080d1e]/80 p-4 shadow-sm backdrop-blur-sm">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-medium uppercase tracking-wider">Ingested Items</span>
            <Layers className="h-4 w-4 text-cyan-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-white">
            {stats?.total_evidence ?? evidenceList.length ?? 3}
          </div>
          <div className="text-[11px] text-cyan-400/80 mt-1 flex items-center gap-1 font-mono">
            <span>Image • Audio • Video</span>
          </div>
        </div>

        <div className="rounded-xl border border-slate-800/80 bg-[#080d1e]/80 p-4 shadow-sm backdrop-blur-sm">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-medium uppercase tracking-wider">Timeline Markers</span>
            <Clock className="h-4 w-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-white">
            {stats?.timeline_events ?? timeline.length ?? 6}
          </div>
          <div className="text-[11px] text-emerald-400/80 mt-1 flex items-center gap-1 font-mono">
            <span>Chronological Fusion</span>
          </div>
        </div>

        <div className="rounded-xl border border-slate-800/80 bg-[#080d1e]/80 p-4 shadow-sm backdrop-blur-sm">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-medium uppercase tracking-wider">Threat Level</span>
            <AlertOctagon className="h-4 w-4 text-rose-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-rose-400">
            CRITICAL
          </div>
          <div className="text-[11px] text-rose-400/80 mt-1 flex items-center gap-1 font-mono">
            <span>Lethal Arms Identified</span>
          </div>
        </div>

        <div className="rounded-xl border border-slate-800/80 bg-[#080d1e]/80 p-4 shadow-sm backdrop-blur-sm">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-medium uppercase tracking-wider">AI Reliability</span>
            <Sparkles className="h-4 w-4 text-amber-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-white">
            94.8%
          </div>
          <div className="text-[11px] text-amber-400/80 mt-1 flex items-center gap-1 font-mono">
            <span>Multimodal Cross-Valid</span>
          </div>
        </div>
      </div>

      {/* Quick Launch Cards */}
      <div>
        <h2 className="text-sm font-semibold uppercase tracking-wider text-slate-400 mb-3 flex items-center gap-2">
          <Crosshair className="h-4 w-4 text-cyan-400" />
          Forensic Telemetry Modules
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div
            onClick={() => setActiveTab('image')}
            className="group rounded-xl border border-slate-800/80 hover:border-cyan-500/50 bg-[#080d1e]/60 hover:bg-[#0c142b]/80 p-5 transition-all cursor-pointer shadow-sm"
          >
            <div className="flex items-center justify-between mb-3">
              <div className="h-9 w-9 rounded-lg bg-cyan-950/70 border border-cyan-500/30 flex items-center justify-center text-cyan-400">
                <Eye className="h-5 w-5" />
              </div>
              <ChevronRight className="h-4 w-4 text-slate-500 group-hover:text-cyan-400 transition-colors" />
            </div>
            <h3 className="text-sm font-bold text-white group-hover:text-cyan-300 transition-colors">
              Vision & Ballistics Analysis
            </h3>
            <p className="text-xs text-slate-400 mt-1 line-clamp-2">
              Ingest crime scene photos to identify perpetrators, firearms, ammunition signatures, and breach points.
            </p>
          </div>

          <div
            onClick={() => setActiveTab('audio')}
            className="group rounded-xl border border-slate-800/80 hover:border-cyan-500/50 bg-[#080d1e]/60 hover:bg-[#0c142b]/80 p-5 transition-all cursor-pointer shadow-sm"
          >
            <div className="flex items-center justify-between mb-3">
              <div className="h-9 w-9 rounded-lg bg-indigo-950/70 border border-indigo-500/30 flex items-center justify-center text-indigo-400">
                <Mic className="h-5 w-5" />
              </div>
              <ChevronRight className="h-4 w-4 text-slate-500 group-hover:text-indigo-400 transition-colors" />
            </div>
            <h3 className="text-sm font-bold text-white group-hover:text-indigo-300 transition-colors">
              Acoustic Telemetry & Dispatch
            </h3>
            <p className="text-xs text-slate-400 mt-1 line-clamp-2">
              Diarize speaker channels, identify gunshots / sirens, and isolate high-stress distress communications.
            </p>
          </div>

          <div
            onClick={() => setActiveTab('video')}
            className="group rounded-xl border border-slate-800/80 hover:border-cyan-500/50 bg-[#080d1e]/60 hover:bg-[#0c142b]/80 p-5 transition-all cursor-pointer shadow-sm"
          >
            <div className="flex items-center justify-between mb-3">
              <div className="h-9 w-9 rounded-lg bg-purple-950/70 border border-purple-500/30 flex items-center justify-center text-purple-400">
                <Video className="h-5 w-5" />
              </div>
              <ChevronRight className="h-4 w-4 text-slate-500 group-hover:text-purple-400 transition-colors" />
            </div>
            <h3 className="text-sm font-bold text-white group-hover:text-purple-300 transition-colors">
              Surveillance Video Tracking
            </h3>
            <p className="text-xs text-slate-400 mt-1 line-clamp-2">
              Segment CCTV streams into keyframe intervals, extract suspect trajectory vectors, and log movement timestamps.
            </p>
          </div>

          <div
            onClick={() => setActiveTab('fusion')}
            className="group rounded-xl border border-slate-800/80 hover:border-cyan-500/50 bg-[#080d1e]/60 hover:bg-[#0c142b]/80 p-5 transition-all cursor-pointer shadow-sm"
          >
            <div className="flex items-center justify-between mb-3">
              <div className="h-9 w-9 rounded-lg bg-emerald-950/70 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
                <GitMerge className="h-5 w-5" />
              </div>
              <ChevronRight className="h-4 w-4 text-slate-500 group-hover:text-emerald-400 transition-colors" />
            </div>
            <h3 className="text-sm font-bold text-white group-hover:text-emerald-300 transition-colors">
              Timeline Fusion & Penal Classifier
            </h3>
            <p className="text-xs text-slate-400 mt-1 line-clamp-2">
              Synthesize cross-modality evidence into one unified chronology and automatically cite state penal codes.
            </p>
          </div>

          <div
            onClick={() => setActiveTab('chat')}
            className="group rounded-xl border border-slate-800/80 hover:border-cyan-500/50 bg-[#080d1e]/60 hover:bg-[#0c142b]/80 p-5 transition-all cursor-pointer shadow-sm"
          >
            <div className="flex items-center justify-between mb-3">
              <div className="h-9 w-9 rounded-lg bg-cyan-950/70 border border-cyan-500/30 flex items-center justify-center text-cyan-400">
                <Bot className="h-5 w-5" />
              </div>
              <ChevronRight className="h-4 w-4 text-slate-500 group-hover:text-cyan-400 transition-colors" />
            </div>
            <h3 className="text-sm font-bold text-white group-hover:text-cyan-300 transition-colors">
              Investigator AI Copilot
            </h3>
            <p className="text-xs text-slate-400 mt-1 line-clamp-2">
              Query case evidence interactively to uncover contradictions, alibi discrepancies, and ballistic matches.
            </p>
          </div>

          <div
            onClick={() => setActiveTab('report')}
            className="group rounded-xl border border-slate-800/80 hover:border-cyan-500/50 bg-[#080d1e]/60 hover:bg-[#0c142b]/80 p-5 transition-all cursor-pointer shadow-sm"
          >
            <div className="flex items-center justify-between mb-3">
              <div className="h-9 w-9 rounded-lg bg-rose-950/70 border border-rose-500/30 flex items-center justify-center text-rose-400">
                <FileText className="h-5 w-5" />
              </div>
              <ChevronRight className="h-4 w-4 text-slate-500 group-hover:text-rose-400 transition-colors" />
            </div>
            <h3 className="text-sm font-bold text-white group-hover:text-rose-300 transition-colors">
              Certified PDF Dossier Exporter
            </h3>
            <p className="text-xs text-slate-400 mt-1 line-clamp-2">
              Render court-ready multi-page ReportLab PDF dossiers containing chain-of-custody verification hashes.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
