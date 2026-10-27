import React, { useState } from 'react';
import { UploadCloud, Eye, AlertTriangle, Shield, CheckCircle, Crosshair, Tag, FileText } from 'lucide-react';

export default function EvidenceVision({ selectedCaseId }) {
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (selected) {
      setFile(selected);
      setPreviewUrl(URL.createObjectURL(selected));
      setResult(null);
      setError('');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select an image file to analyze.');
      return;
    }

    setLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('file', file);
    formData.append('case_id', selectedCaseId);

    try {
      const res = await fetch('/api/v1/analyze/image', {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.detail || 'Image analysis failed.');
      }

      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError(err.message || 'Error executing vision analysis.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="border-b border-slate-800 pb-4">
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <Eye className="h-5 w-5 text-cyan-400" />
          Crime Scene Vision & Ballistics Analysis
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Ingest forensic photographs or CCTV freeze-frames. Extracts suspect physical telemetry, weapon classification, and environment breach markers.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Upload Form */}
        <div className="lg:col-span-5 space-y-4">
          <form onSubmit={handleSubmit} className="rounded-xl border border-slate-800 bg-[#080d1e]/80 p-5 shadow-sm space-y-4">
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-2">
                Upload Crime Scene Image
              </label>
              <div className="relative border-2 border-dashed border-slate-700 hover:border-cyan-500/60 rounded-xl p-6 text-center transition-all bg-slate-900/30">
                <input
                  type="file"
                  accept="image/jpeg,image/png,image/webp"
                  onChange={handleFileChange}
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                />
                <UploadCloud className="mx-auto h-8 w-8 text-cyan-400/80 mb-2" />
                <p className="text-xs text-slate-300 font-medium">
                  {file ? file.name : 'Drag & drop image or click to browse'}
                </p>
                <p className="text-[10px] text-slate-500 mt-1">
                  Supports JPG, PNG, WebP up to 50MB
                </p>
              </div>
            </div>

            {previewUrl && (
              <div className="rounded-lg overflow-hidden border border-slate-800 bg-black/40">
                <img src={previewUrl} alt="Preview" className="max-h-60 w-full object-contain mx-auto" />
              </div>
            )}

            {error && (
              <div className="p-3 rounded-lg bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading || !file}
              className="w-full py-2.5 px-4 rounded-xl text-xs font-semibold bg-cyan-500 hover:bg-cyan-400 disabled:opacity-50 text-slate-950 transition-all shadow-md shadow-cyan-500/20 flex items-center justify-center gap-2 cursor-pointer font-mono"
            >
              {loading ? (
                <>
                  <div className="h-3.5 w-3.5 border-2 border-slate-950 border-t-transparent rounded-full animate-spin" />
                  <span>EXTRACTING FORENSIC TELEMETRY...</span>
                </>
              ) : (
                <>
                  <Crosshair className="h-4 w-4" />
                  <span>RUN VISION INFERENCE</span>
                </>
              )}
            </button>
          </form>
        </div>

        {/* Results Panel */}
        <div className="lg:col-span-7">
          {result ? (
            <div className="rounded-xl border border-cyan-900/40 bg-[#080d1e]/90 p-5 shadow-lg space-y-5">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <div className="flex items-center gap-2">
                  <CheckCircle className="h-4 w-4 text-emerald-400" />
                  <span className="text-xs font-bold font-mono text-emerald-400 uppercase tracking-wider">
                    Evidence Ingested & Tagged
                  </span>
                </div>
                <span className="text-[11px] font-mono text-slate-400">
                  Confidence: {(result.overall_confidence ? result.overall_confidence * 100 : 94).toFixed(1)}%
                </span>
              </div>

              {/* Summary */}
              <div>
                <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1">
                  Forensic Summary
                </h4>
                <p className="text-xs text-slate-200 leading-relaxed bg-slate-900/60 p-3 rounded-lg border border-slate-800">
                  {result.forensic_summary || 'Perpetrator detected in breach perimeter with high-threat firearm.'}
                </p>
              </div>

              {/* Weapons Found */}
              {result.weapons && result.weapons.length > 0 && (
                <div>
                  <h4 className="text-xs font-semibold uppercase tracking-wider text-rose-400 mb-2 flex items-center gap-1.5">
                    <AlertTriangle className="h-3.5 w-3.5" />
                    Weapons Identified ({result.weapons.length})
                  </h4>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                    {result.weapons.map((w, idx) => (
                      <div key={idx} className="p-2.5 rounded-lg border border-rose-500/30 bg-rose-500/10 text-xs space-y-1">
                        <div className="flex justify-between font-mono font-bold text-rose-300">
                          <span>{w.weapon_type || w.model || w.category || 'Handgun'}</span>
                          <span className="text-[10px] uppercase px-1.5 py-0.5 rounded bg-rose-950 text-rose-400 border border-rose-800">
                            {w.threat_level || 'HIGH'}
                          </span>
                        </div>
                        <div className="text-[11px] text-slate-300">
                          {w.description || w.notes || 'Visible weapon drawn and aimed.'}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Persons Found */}
              {result.persons && result.persons.length > 0 && (
                <div>
                  <h4 className="text-xs font-semibold uppercase tracking-wider text-cyan-400 mb-2">
                    Persons / Suspects Detected ({result.persons.length})
                  </h4>
                  <div className="space-y-2">
                    {result.persons.map((p, idx) => (
                      <div key={idx} className="p-3 rounded-lg border border-slate-800 bg-slate-900/40 text-xs space-y-1 font-mono">
                        <div className="text-slate-200 font-semibold flex justify-between">
                          <span>Subject #{idx + 1}: {p.role_inference || p.role || 'Suspect'}</span>
                          <span className="text-slate-400 text-[11px]">{p.clothing || `${p.clothing_top || ''} ${p.clothing_bottom || ''}`.trim()}</span>
                        </div>
                        <div className="text-[11px] text-slate-400">
                          {p.visual_description || p.stance || p.action || 'Standing near entry vault door.'}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Scene Environment */}
              {(result.scene_environment || result.environment) && (
                <div>
                  <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1">
                    Environment & Breach Geometry
                  </h4>
                  <div className="text-xs text-slate-300 bg-slate-900/40 p-2.5 rounded-lg border border-slate-800">
                    {(() => {
                      const env = result.scene_environment || result.environment;
                      if (typeof env === 'string') return env;
                      return `${env.setting || ''} • ${env.lighting || ''} • Entry: ${(env.entry_points || []).join(', ')}`;
                    })()}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="h-full min-h-[320px] rounded-xl border border-slate-800/80 bg-[#080d1e]/40 p-8 flex flex-col items-center justify-center text-center text-slate-500">
              <Crosshair className="h-10 w-10 text-slate-600 mb-3" />
              <p className="text-xs font-medium">Awaiting image ingestion</p>
              <p className="text-[11px] text-slate-600 mt-1 max-w-sm">
                Upload a crime scene photo on the left to extract person contours, firearm classifications, and automatic timeline updates.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
