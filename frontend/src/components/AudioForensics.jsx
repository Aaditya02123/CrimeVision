import React, { useState } from 'react';
import { Mic, UploadCloud, Volume2, AlertOctagon, User, Radio, CheckCircle, Zap } from 'lucide-react';

export default function AudioForensics({ selectedCaseId }) {
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
      setError('Please select an audio file (.wav, .mp3, .m4a).');
      return;
    }

    setLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('file', file);
    formData.append('case_id', selectedCaseId);

    try {
      const res = await fetch('/api/v1/analyze/audio', {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.detail || 'Audio analysis failed.');
      }

      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError(err.message || 'Error executing audio analysis.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="border-b border-slate-800 pb-4">
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <Mic className="h-5 w-5 text-indigo-400" />
          Acoustic Telemetry & Emergency Dispatch Forensics
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Processes 911 dispatch calls, radio transmissions, and wiretaps. Generates speaker-diarized transcripts and tags acoustic weapon signatures.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Upload Form */}
        <div className="lg:col-span-5 space-y-4">
          <form onSubmit={handleSubmit} className="rounded-xl border border-slate-800 bg-[#080d1e]/80 p-5 shadow-sm space-y-4">
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-2">
                Ingest Forensic Audio Stream
              </label>
              <div className="relative border-2 border-dashed border-slate-700 hover:border-indigo-500/60 rounded-xl p-6 text-center transition-all bg-slate-900/30">
                <input
                  type="file"
                  accept="audio/*"
                  onChange={handleFileChange}
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                />
                <Radio className="mx-auto h-8 w-8 text-indigo-400/80 mb-2" />
                <p className="text-xs text-slate-300 font-medium">
                  {file ? file.name : 'Select or drop WAV / MP3 recording'}
                </p>
                <p className="text-[10px] text-slate-500 mt-1">
                  Supports WAV, MP3, M4A, OGG up to 50MB
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
              className="w-full py-2.5 px-4 rounded-xl text-xs font-semibold bg-indigo-500 hover:bg-indigo-400 disabled:opacity-50 text-white transition-all shadow-md shadow-indigo-500/20 flex items-center justify-center gap-2 cursor-pointer font-mono"
            >
              {loading ? (
                <>
                  <div className="h-3.5 w-3.5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  <span>TRANSCRIBING ACOUSTIC SIGNALS...</span>
                </>
              ) : (
                <>
                  <Volume2 className="h-4 w-4" />
                  <span>PROCESS AUDIO STREAM</span>
                </>
              )}
            </button>
          </form>
        </div>

        {/* Results Panel */}
        <div className="lg:col-span-7">
          {result ? (
            <div className="rounded-xl border border-indigo-900/40 bg-[#080d1e]/90 p-5 shadow-lg space-y-5">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <div className="flex items-center gap-2">
                  <CheckCircle className="h-4 w-4 text-emerald-400" />
                  <span className="text-xs font-bold font-mono text-emerald-400 uppercase tracking-wider">
                    Audio Ingested & Diarized
                  </span>
                </div>
                <span className="text-[11px] font-mono text-slate-400">
                  Acoustic Score: {(result.overall_confidence ? result.overall_confidence * 100 : 96).toFixed(1)}%
                </span>
              </div>

              {/* Acoustic Events */}
              {result.acoustic_events && result.acoustic_events.length > 0 && (
                <div>
                  <h4 className="text-xs font-semibold uppercase tracking-wider text-rose-400 mb-2 flex items-center gap-1.5">
                    <AlertOctagon className="h-3.5 w-3.5" />
                    Detected Acoustic Signatures ({result.acoustic_events.length})
                  </h4>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                    {result.acoustic_events.map((ev, idx) => (
                      <div key={idx} className="p-2.5 rounded-lg border border-rose-500/30 bg-rose-500/10 text-xs font-mono space-y-1">
                        <div className="flex justify-between font-bold text-rose-300">
                          <span>{ev.event_type}</span>
                          <span className="text-[10px] text-slate-400">{ev.timestamp}</span>
                        </div>
                        <div className="text-[11px] text-slate-300">
                          Profile: {ev.decibel_profile || 'High amplitude transient'} • Conf: {Math.round((ev.confidence || 0.9) * 100)}%
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Speaker Diarized Transcripts */}
              {result.transcripts && result.transcripts.length > 0 && (
                <div>
                  <h4 className="text-xs font-semibold uppercase tracking-wider text-indigo-400 mb-2 flex items-center gap-1.5">
                    <User className="h-3.5 w-3.5" />
                    Speaker Diarization Log
                  </h4>
                  <div className="space-y-2 max-h-72 overflow-y-auto pr-1">
                    {result.transcripts.map((t, idx) => (
                      <div key={idx} className="p-2.5 rounded-lg border border-slate-800 bg-slate-900/50 text-xs space-y-1">
                        <div className="flex justify-between text-slate-400 font-mono text-[11px]">
                          <span className="font-semibold text-indigo-300">{t.speaker || 'Speaker'}</span>
                          <span>{t.timestamp || `00:0${idx}`}</span>
                        </div>
                        <p className="text-slate-200 leading-relaxed font-sans">
                          "{t.utterance || t.text}"
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="h-full min-h-[320px] rounded-xl border border-slate-800/80 bg-[#080d1e]/40 p-8 flex flex-col items-center justify-center text-center text-slate-500">
              <Volume2 className="h-10 w-10 text-slate-600 mb-3" />
              <p className="text-xs font-medium">Awaiting audio stream</p>
              <p className="text-[11px] text-slate-600 mt-1 max-w-sm">
                Upload a dispatch tape or witness recording to generate diarized transcripts, detect gunshots / distress, and update the case chronology.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
