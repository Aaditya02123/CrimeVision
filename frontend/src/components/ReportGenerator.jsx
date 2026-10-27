import React, { useState } from 'react';
import { FileText, Download, CheckCircle, ShieldCheck, Printer, HardDrive, Hash } from 'lucide-react';

export default function ReportGenerator({ selectedCaseId }) {
  const [includeImage, setIncludeImage] = useState(true);
  const [includeAudio, setIncludeAudio] = useState(true);
  const [includeVideo, setIncludeVideo] = useState(true);
  const [includeTimeline, setIncludeTimeline] = useState(true);
  const [loading, setLoading] = useState(false);
  const [generatedReport, setGeneratedReport] = useState(null);
  const [error, setError] = useState('');

  const handleGenerate = async () => {
    setLoading(true);
    setError('');
    setGeneratedReport(null);

    try {
      const res = await fetch('/api/v1/report/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          case_id: selectedCaseId,
          include_image_analysis: includeImage,
          include_audio_transcripts: includeAudio,
          include_video_timeline: includeVideo,
          include_chain_of_custody: true,
        }),
      });

      if (!res.ok) {
        throw new Error('PDF Dossier generation failed.');
      }

      const data = await res.json();
      setGeneratedReport(data);
    } catch (err) {
      setError(err.message || 'Error generating PDF report.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="border-b border-slate-800 pb-4">
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <FileText className="h-5 w-5 text-rose-400" />
          Certified Police & Judicial PDF Dossier Generator
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Compiles full multimodal evidence findings, audio transcripts, surveillance timelines, and cryptographic verification seals into a court-ready ReportLab document.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Dossier Customization Form */}
        <div className="lg:col-span-6 space-y-4">
          <div className="rounded-xl border border-slate-800 bg-[#080d1e]/80 p-5 shadow-sm space-y-5">
            <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-300">
              Dossier Inclusions & Evidence Modules
            </h3>

            <div className="space-y-3">
              <label className="flex items-center gap-3 p-3 rounded-lg border border-slate-800 bg-slate-900/40 cursor-pointer hover:bg-slate-900/60">
                <input
                  type="checkbox"
                  checked={includeImage}
                  onChange={(e) => setIncludeImage(e.target.checked)}
                  className="rounded border-slate-700 text-cyan-500 focus:ring-0 h-4 w-4 bg-slate-800"
                />
                <div className="text-xs">
                  <div className="font-semibold text-white">Ballistics & Crime Scene Vision Exhibits</div>
                  <div className="text-slate-400 text-[11px]">Includes suspect counts, firearm classifications, and breach photos.</div>
                </div>
              </label>

              <label className="flex items-center gap-3 p-3 rounded-lg border border-slate-800 bg-slate-900/40 cursor-pointer hover:bg-slate-900/60">
                <input
                  type="checkbox"
                  checked={includeAudio}
                  onChange={(e) => setIncludeAudio(e.target.checked)}
                  className="rounded border-slate-700 text-cyan-500 focus:ring-0 h-4 w-4 bg-slate-800"
                />
                <div className="text-xs">
                  <div className="font-semibold text-white">Acoustic Telemetry & Emergency Transcripts</div>
                  <div className="text-slate-400 text-[11px]">Includes speaker diarization logs and weapon decibel signatures.</div>
                </div>
              </label>

              <label className="flex items-center gap-3 p-3 rounded-lg border border-slate-800 bg-slate-900/40 cursor-pointer hover:bg-slate-900/60">
                <input
                  type="checkbox"
                  checked={includeVideo}
                  onChange={(e) => setIncludeVideo(e.target.checked)}
                  className="rounded border-slate-700 text-cyan-500 focus:ring-0 h-4 w-4 bg-slate-800"
                />
                <div className="text-xs">
                  <div className="font-semibold text-white">Surveillance Action Sequence Logs</div>
                  <div className="text-slate-400 text-[11px]">Includes CCTV keyframe detections and movement timestamps.</div>
                </div>
              </label>

              <label className="flex items-center gap-3 p-3 rounded-lg border border-slate-800 bg-slate-900/40 cursor-pointer hover:bg-slate-900/60">
                <input
                  type="checkbox"
                  checked={includeTimeline}
                  onChange={(e) => setIncludeTimeline(e.target.checked)}
                  className="rounded border-slate-700 text-cyan-500 focus:ring-0 h-4 w-4 bg-slate-800"
                />
                <div className="text-xs">
                  <div className="font-semibold text-white">Unified Chronology & Statutory Penal Classifications</div>
                  <div className="text-slate-400 text-[11px]">Official legal element breakdown and state penal code citations.</div>
                </div>
              </label>
            </div>

            {error && (
              <div className="p-3 rounded-lg bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs">
                {error}
              </div>
            )}

            <button
              onClick={handleGenerate}
              disabled={loading}
              className="w-full py-2.5 px-4 rounded-xl text-xs font-semibold bg-rose-600 hover:bg-rose-500 disabled:opacity-50 text-white transition-all shadow-md shadow-rose-600/20 flex items-center justify-center gap-2 cursor-pointer font-mono"
            >
              {loading ? (
                <>
                  <div className="h-3.5 w-3.5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  <span>COMPILING REPORTLAB PDF DOSSIER...</span>
                </>
              ) : (
                <>
                  <Printer className="h-4 w-4" />
                  <span>GENERATE FORENSIC DOSSIER</span>
                </>
              )}
            </button>
          </div>
        </div>

        {/* Generated PDF Output & Actions */}
        <div className="lg:col-span-6">
          {generatedReport ? (
            <div className="rounded-xl border border-rose-900/40 bg-[#080d1e]/90 p-6 shadow-xl space-y-5">
              <div className="flex items-center gap-2 text-emerald-400 text-xs font-mono font-bold">
                <CheckCircle className="h-4 w-4" />
                <span>OFFICIAL DOSSIER COMPILED SUCCESSFULLY</span>
              </div>

              <div className="p-4 rounded-xl border border-slate-800 bg-slate-900/60 space-y-3 font-mono text-xs">
                <div className="flex justify-between border-b border-slate-800 pb-2">
                  <span className="text-slate-400">Case ID:</span>
                  <span className="text-white font-bold">{generatedReport.case_id}</span>
                </div>
                <div className="flex justify-between border-b border-slate-800 pb-2">
                  <span className="text-slate-400">Filename:</span>
                  <span className="text-cyan-300 text-[11px] truncate max-w-[240px]">{generatedReport.filename}</span>
                </div>
                <div className="flex justify-between border-b border-slate-800 pb-2">
                  <span className="text-slate-400">Timestamp:</span>
                  <span className="text-slate-300">{generatedReport.generated_at}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">File Size:</span>
                  <span className="text-slate-300">{Math.round((generatedReport.file_size_bytes || 0) / 1024)} KB</span>
                </div>
              </div>

              <div className="p-3 rounded-lg border border-cyan-900/40 bg-cyan-950/20 text-xs text-cyan-200/90 flex items-start gap-2.5">
                <ShieldCheck className="h-4 w-4 text-cyan-400 mt-0.5 flex-shrink-0" />
                <span className="text-[11px] leading-relaxed">
                  Dossier certified under digital verification protocol. Cryptographic hash stamped into judicial header block.
                </span>
              </div>

              <a
                href={`/api/v1/report/download/${selectedCaseId}`}
                target="_blank"
                rel="noreferrer"
                download
                className="w-full py-3 px-4 rounded-xl text-xs font-semibold bg-emerald-500 hover:bg-emerald-400 text-slate-950 transition-all shadow-md shadow-emerald-500/20 flex items-center justify-center gap-2 cursor-pointer font-mono"
              >
                <Download className="h-4 w-4" />
                <span>DOWNLOAD CERTIFIED PDF REPORT</span>
              </a>
            </div>
          ) : (
            <div className="h-full min-h-[320px] rounded-xl border border-slate-800/80 bg-[#080d1e]/40 p-8 flex flex-col items-center justify-center text-center text-slate-500">
              <FileText className="h-10 w-10 text-slate-600 mb-3" />
              <p className="text-xs font-medium">Ready to compile dossier</p>
              <p className="text-[11px] text-slate-600 mt-1 max-w-sm">
                Select your evidence modules on the left and click Generate to produce a downloadable PDF containing all ingested findings and timelines.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
