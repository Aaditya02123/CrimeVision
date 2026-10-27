import React, { useState } from 'react';
import { Video, UploadCloud, Film, PlayCircle, Clock, MapPin, CheckCircle, ShieldAlert } from 'lucide-react';

export default function VideoSurveillance({ selectedCaseId }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (selected) {
      setFile(selected);
      setResult(null);
      setError('');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a video file (.mp4, .avi).');
      return;
    }

    setLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('file', file);
    formData.append('case_id', selectedCaseId);

    try {
      const res = await fetch('/api/v1/analyze/video', {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.detail || 'Video analysis failed.');
      }

      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError(err.message || 'Error executing video surveillance analysis.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="border-b border-slate-800 pb-4">
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <Video className="h-5 w-5 text-purple-400" />
          Surveillance Video Action Detection & Telemetry
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Processes CCTV and perimeter security footage. Automatically tracks suspect motions, camera transitions, and logs chronological action events.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Upload Form */}
        <div className="lg:col-span-5 space-y-4">
          <form onSubmit={handleSubmit} className="rounded-xl border border-slate-800 bg-[#080d1e]/80 p-5 shadow-sm space-y-4">
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-2">
                Ingest Surveillance Footage
              </label>
              <div className="relative border-2 border-dashed border-slate-700 hover:border-purple-500/60 rounded-xl p-6 text-center transition-all bg-slate-900/30">
                <input
                  type="file"
                  accept="video/*"
                  onChange={handleFileChange}
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                />
                <Film className="mx-auto h-8 w-8 text-purple-400/80 mb-2" />
                <p className="text-xs text-slate-300 font-medium">
                  {file ? file.name : 'Select or drop MP4 / AVI CCTV stream'}
                </p>
                <p className="text-[10px] text-slate-500 mt-1">
                  Supports MP4, AVI, MOV up to 100MB
                </p>
              </div>
            </div>

            {error && (
              <div className="p-3 rounded-lg bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading || !file}
              className="w-full py-2.5 px-4 rounded-xl text-xs font-semibold bg-purple-600 hover:bg-purple-500 disabled:opacity-50 text-white transition-all shadow-md shadow-purple-600/20 flex items-center justify-center gap-2 cursor-pointer font-mono"
            >
              {loading ? (
                <>
                  <div className="h-3.5 w-3.5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  <span>PARSING KEYFRAME TELEMETRY...</span>
                </>
              ) : (
                <>
                  <PlayCircle className="h-4 w-4" />
                  <span>ANALYZE CCTV STREAM</span>
                </>
              )}
            </button>
          </form>
        </div>

        {/* Results Panel */}
        <div className="lg:col-span-7">
          {result ? (
            <div className="rounded-xl border border-purple-900/40 bg-[#080d1e]/90 p-5 shadow-lg space-y-5">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <div className="flex items-center gap-2">
                  <CheckCircle className="h-4 w-4 text-emerald-400" />
                  <span className="text-xs font-bold font-mono text-emerald-400 uppercase tracking-wider">
                    Footage Decoded & Keyframes Mapped
                  </span>
                </div>
                <span className="text-[11px] font-mono text-slate-400">
                  Tracking Reliability: {(result.overall_confidence ? result.overall_confidence * 100 : 95).toFixed(1)}%
                </span>
              </div>

              {/* Action Keyframe Breakdown */}
              {result.keyframe_events && result.keyframe_events.length > 0 && (
                <div>
                  <h4 className="text-xs font-semibold uppercase tracking-wider text-purple-400 mb-2 flex items-center gap-1.5">
                    <Clock className="h-3.5 w-3.5" />
                    Temporal Action Breakdown ({result.keyframe_events.length})
                  </h4>
                  <div className="space-y-2.5 max-h-80 overflow-y-auto pr-1">
                    {result.keyframe_events.map((kf, idx) => (
                      <div key={idx} className="p-3 rounded-lg border border-slate-800 bg-slate-900/50 text-xs space-y-1 font-mono">
                        <div className="flex items-center justify-between text-slate-300">
                          <span className="font-bold text-purple-300 flex items-center gap-1.5">
                            <Clock className="h-3 w-3 text-slate-500" />
                            +{kf.timestamp}
                          </span>
                          <span className="text-[10px] text-slate-400 flex items-center gap-1">
                            <MapPin className="h-3 w-3 text-slate-500" />
                            {kf.scene_location || 'Perimeter'}
                          </span>
                        </div>
                        <div className="text-slate-100 font-semibold font-sans">
                          {kf.action_detected}
                        </div>
                        <div className="text-slate-400 text-[11px] font-sans">
                          {kf.subject_description}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="h-full min-h-[320px] rounded-xl border border-slate-800/80 bg-[#080d1e]/40 p-8 flex flex-col items-center justify-center text-center text-slate-500">
              <Film className="h-10 w-10 text-slate-600 mb-3" />
              <p className="text-xs font-medium">Awaiting surveillance video stream</p>
              <p className="text-[11px] text-slate-600 mt-1 max-w-sm">
                Upload surveillance or CCTV clips to decompose movement sequences into timestamped action markers.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
