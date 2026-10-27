import React, { useState, useEffect } from 'react';
import { 
  GitMerge, 
  Scale, 
  Clock, 
  AlertTriangle, 
  BookOpen, 
  ShieldCheck, 
  RefreshCw, 
  Eye, 
  Mic, 
  Video 
} from 'lucide-react';

export default function TimelineFusion({ selectedCaseId }) {
  const [fusionData, setFusionData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchFusion = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await fetch(`/api/v1/fusion/timeline/${selectedCaseId}`);
      if (!res.ok) {
        throw new Error('Failed to fuse case timeline.');
      }
      const data = await res.json();
      setFusionData(data);
    } catch (err) {
      setError(err.message || 'Error executing evidence fusion.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFusion();
  }, [selectedCaseId]);

  const getModalityIcon = (modality) => {
    switch (modality?.toUpperCase()) {
      case 'IMAGE':
        return <Eye className="h-3.5 w-3.5 text-cyan-400" />;
      case 'AUDIO':
        return <Mic className="h-3.5 w-3.5 text-indigo-400" />;
      case 'VIDEO':
        return <Video className="h-3.5 w-3.5 text-purple-400" />;
      default:
        return <Clock className="h-3.5 w-3.5 text-slate-400" />;
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-800 pb-4 gap-3">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <GitMerge className="h-5 w-5 text-emerald-400" />
            Multimodal Timeline Fusion & Crime Classifier
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Synthesizes vision frames, acoustic signatures, and surveillance actions into one unified sequence with automated statutory offense classification.
          </p>
        </div>
        <button
          onClick={fetchFusion}
          disabled={loading}
          className="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-900 border border-slate-700 hover:border-slate-600 text-slate-200 transition-colors cursor-pointer self-start sm:self-auto font-mono"
        >
          <RefreshCw className={`h-3.5 w-3.5 ${loading ? 'animate-spin' : ''}`} />
          <span>RE-FUSE EVIDENCE</span>
        </button>
      </div>

      {loading ? (
        <div className="min-h-[300px] rounded-xl border border-slate-800 bg-[#080d1e]/40 p-12 flex flex-col items-center justify-center text-center">
          <div className="h-8 w-8 border-2 border-emerald-400 border-t-transparent rounded-full animate-spin mb-3" />
          <p className="text-xs font-medium text-slate-300 font-mono">
            SYNTHESIZING CROSS-MODAL FORENSIC TIMELINE...
          </p>
        </div>
      ) : error ? (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs">
          {error}
        </div>
      ) : fusionData ? (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Statutory Classification Card */}
          <div className="lg:col-span-5 space-y-4">
            <div className="rounded-xl border border-emerald-900/40 bg-[#080d1e]/90 p-5 shadow-lg space-y-4">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <div className="flex items-center gap-2">
                  <Scale className="h-4 w-4 text-emerald-400" />
                  <span className="text-xs font-bold font-mono text-emerald-400 uppercase tracking-wider">
                    Statutory Classification
                  </span>
                </div>
                <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-rose-950/80 text-rose-400 border border-rose-800 font-bold">
                  {fusionData.classification?.severity || 'CLASS A FELONY'}
                </span>
              </div>

              <div>
                <h3 className="text-base font-bold text-white">
                  {fusionData.classification?.primary_offense || 'Aggravated Armed Commercial Robbery'}
                </h3>
                <p className="text-xs text-slate-300 mt-1 leading-relaxed">
                  {fusionData.classification?.summary || 'Multiple offenders conducted armed intrusion utilizing unauthorized access and brandishing firearms.'}
                </p>
              </div>

              {/* Statute Citations */}
              {fusionData.classification?.statute_citations && (
                <div>
                  <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2 flex items-center gap-1.5">
                    <BookOpen className="h-3.5 w-3.5" />
                    Applicable Legal Statutes
                  </h4>
                  <div className="space-y-1.5">
                    {fusionData.classification.statute_citations.map((stat, idx) => (
                      <div key={idx} className="p-2 rounded bg-slate-900/60 border border-slate-800 text-xs font-mono text-slate-300">
                        § {stat}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Elements of Proof */}
              {fusionData.classification?.elements_established && (
                <div>
                  <h4 className="text-xs font-semibold uppercase tracking-wider text-emerald-400 mb-2 flex items-center gap-1.5">
                    <ShieldCheck className="h-3.5 w-3.5" />
                    Established Elements of Crime
                  </h4>
                  <ul className="space-y-1.5 text-xs text-slate-300 list-disc list-inside">
                    {fusionData.classification.elements_established.map((elem, idx) => (
                      <li key={idx} className="leading-relaxed">
                        {elem}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            {/* Contradictions / Discrepancies if any */}
            {fusionData.contradictions && fusionData.contradictions.length > 0 && (
              <div className="rounded-xl border border-amber-900/40 bg-amber-950/20 p-4 space-y-2">
                <div className="flex items-center gap-2 text-amber-400 text-xs font-bold font-mono">
                  <AlertTriangle className="h-4 w-4" />
                  <span>MODALITY CONTRADICTION DETECTED</span>
                </div>
                {fusionData.contradictions.map((c, idx) => (
                  <p key={idx} className="text-xs text-amber-200/90 leading-relaxed">
                    {c}
                  </p>
                ))}
              </div>
            )}
          </div>

          {/* Unified Timeline Sequence */}
          <div className="lg:col-span-7">
            <div className="rounded-xl border border-slate-800 bg-[#080d1e]/80 p-5 shadow-sm space-y-4">
              <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-2">
                <Clock className="h-4 w-4 text-cyan-400" />
                Chronological Multimodal Sequence ({fusionData.timeline?.length || 0} Events)
              </h3>

              <div className="relative border-l-2 border-slate-800 ml-3 pl-5 space-y-6">
                {fusionData.timeline?.map((ev, idx) => (
                  <div key={idx} className="relative group">
                    {/* Node Dot */}
                    <div className="absolute -left-[27px] top-1 h-3.5 w-3.5 rounded-full border-2 border-[#080d1e] bg-cyan-400 shadow-sm" />

                    <div className="p-3 rounded-lg border border-slate-800/80 bg-slate-900/50 hover:bg-slate-900/80 transition-colors space-y-1">
                      <div className="flex items-center justify-between text-xs">
                        <span className="font-mono font-bold text-cyan-300">
                          {ev.timestamp_marker || ev.timestamp || 'T+00:00'}
                        </span>
                        <div className="flex items-center gap-1.5 font-mono text-[10px] uppercase px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
                          {getModalityIcon(ev.source_modality)}
                          <span>{ev.source_modality || 'FUSION'}</span>
                        </div>
                      </div>
                      <div className="text-xs font-bold text-slate-100 font-mono">
                        {ev.event_type || 'INCIDENT_EVENT'}
                      </div>
                      <p className="text-xs text-slate-300 leading-relaxed font-sans">
                        {ev.description}
                      </p>
                      {ev.confidence && (
                        <div className="text-[10px] text-slate-500 font-mono text-right">
                          Confidence: {Math.round(ev.confidence * 100)}%
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      ) : null}
    </div>
  );
}
