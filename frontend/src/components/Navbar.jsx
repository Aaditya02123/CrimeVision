import React from 'react';
import { 
  ShieldAlert, 
  Activity, 
  Eye, 
  Mic, 
  Video, 
  GitMerge, 
  Bot, 
  FileText, 
  CheckCircle2, 
  AlertCircle,
  FolderOpen
} from 'lucide-react';

export default function Navbar({ 
  activeTab, 
  setActiveTab, 
  cases = [], 
  selectedCaseId, 
  setSelectedCaseId, 
  healthInfo 
}) {
  const tabs = [
    { id: 'dashboard', label: 'Dashboard', icon: Activity },
    { id: 'image', label: 'Vision Forensics', icon: Eye },
    { id: 'audio', label: 'Audio Acoustics', icon: Mic },
    { id: 'video', label: 'Surveillance Video', icon: Video },
    { id: 'fusion', label: 'Timeline Fusion', icon: GitMerge },
    { id: 'chat', label: 'Investigator Copilot', icon: Bot },
    { id: 'report', label: 'PDF Dossier', icon: FileText },
  ];

  const isHealthy = healthInfo?.status === 'healthy';
  const isGeminiLive = healthInfo?.gemini_mode === 'live' || healthInfo?.gemini_api_key_configured;

  return (
    <header className="sticky top-0 z-50 border-b border-cyan-900/40 bg-[#060a16]/90 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Case Selector */}
          <div className="flex items-center gap-4">
            <div 
              className="flex items-center gap-2.5 cursor-pointer group"
              onClick={() => setActiveTab('dashboard')}
            >
              <div className="h-9 w-9 rounded-lg bg-cyan-950/80 border border-cyan-500/30 flex items-center justify-center text-cyan-400 group-hover:border-cyan-400/60 transition-all shadow-sm shadow-cyan-900/20">
                <ShieldAlert className="h-5 w-5" />
              </div>
              <div>
                <span className="font-extrabold text-base tracking-tight text-white flex items-center gap-1.5 font-mono">
                  CRIMEVISION<span className="text-cyan-400">AI</span>
                </span>
                <span className="text-[10px] uppercase tracking-widest text-cyan-500/80 block font-semibold">
                  Forensic Telemetry Station
                </span>
              </div>
            </div>

            {/* Active Case Selector */}
            <div className="hidden md:flex items-center gap-1.5 ml-4 pl-4 border-l border-slate-800">
              <FolderOpen className="h-3.5 w-3.5 text-slate-400" />
              <select
                value={selectedCaseId}
                onChange={(e) => setSelectedCaseId(e.target.value)}
                className="bg-slate-900/90 border border-slate-800 hover:border-slate-700 text-xs text-slate-200 rounded-md px-2.5 py-1 focus:outline-none focus:ring-1 focus:ring-cyan-500 font-mono"
              >
                {cases.length > 0 ? (
                  cases.map((c) => (
                    <option key={c.case_id} value={c.case_id}>
                      {c.case_id} • {c.title?.slice(0, 32)}...
                    </option>
                  ))
                ) : (
                  <>
                    <option value="CASE-2026-0891">CASE-2026-0891 • Metro Vault Breach</option>
                    <option value="CASE-2026-0412">CASE-2026-0412 • Pier 19 Intrusion</option>
                  </>
                )}
              </select>
            </div>
          </div>

          {/* System Health Status Pills */}
          <div className="flex items-center gap-3">
            <div className="hidden sm:flex items-center gap-2 text-xs">
              <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-medium border font-mono ${
                isHealthy 
                  ? 'bg-emerald-950/60 text-emerald-400 border-emerald-500/30' 
                  : 'bg-rose-950/60 text-rose-400 border-rose-500/30'
              }`}>
                {isHealthy ? <CheckCircle2 className="h-3 w-3" /> : <AlertCircle className="h-3 w-3" />}
                {isHealthy ? 'REST API OK' : 'API DISCONNECTED'}
              </span>

              <span className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[11px] font-medium border font-mono ${
                isGeminiLive
                  ? 'bg-cyan-950/60 text-cyan-400 border-cyan-500/30'
                  : 'bg-amber-950/60 text-amber-400 border-amber-500/30'
              }`}>
                {isGeminiLive ? '⚡ LIVE GEMINI' : '🛡️ SANDBOX ENGINE'}
              </span>
            </div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="flex space-x-1 overflow-x-auto pb-2 scrollbar-none">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-3 py-1.5 text-xs font-medium rounded-md whitespace-nowrap transition-all duration-150 cursor-pointer ${
                  isActive
                    ? 'bg-cyan-500/15 text-cyan-300 border border-cyan-500/30 shadow-sm'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/60'
                }`}
              >
                <Icon className={`h-3.5 w-3.5 ${isActive ? 'text-cyan-400' : 'text-slate-400'}`} />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>
      </div>
    </header>
  );
}
