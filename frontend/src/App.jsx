import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import DisclaimerBanner from './components/DisclaimerBanner';
import DashboardOverview from './components/DashboardOverview';
import EvidenceVision from './components/EvidenceVision';
import AudioForensics from './components/AudioForensics';
import VideoSurveillance from './components/VideoSurveillance';
import TimelineFusion from './components/TimelineFusion';
import CopilotChat from './components/CopilotChat';
import ReportGenerator from './components/ReportGenerator';
import { ArrowLeft } from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [selectedCaseId, setSelectedCaseId] = useState('CASE-2026-0891');
  const [cases, setCases] = useState([]);
  const [healthInfo, setHealthInfo] = useState({
    status: 'checking',
    gemini_mode: 'mock_sandbox',
    gemini_api_key_configured: false,
  });

  useEffect(() => {
    // Check backend health
    const checkHealth = async () => {
      try {
        const res = await fetch('/api/health');
        if (res.ok) {
          const data = await res.json();
          setHealthInfo(data);
        } else {
          setHealthInfo({ status: 'error', gemini_mode: 'mock_sandbox', gemini_api_key_configured: false });
        }
      } catch (err) {
        console.warn('Backend service offline or booting:', err);
        setHealthInfo({ status: 'error', gemini_mode: 'mock_sandbox', gemini_api_key_configured: false });
      }
    };

    // Fetch registered forensic cases
    const fetchCases = async () => {
      try {
        const res = await fetch('/api/v1/cases');
        if (res.ok) {
          const data = await res.json();
          if (Array.isArray(data) && data.length > 0) {
            setCases(data);
            setSelectedCaseId(data[0].case_id);
          }
        }
      } catch (err) {
        console.warn('Could not fetch registered cases:', err);
      }
    };

    checkHealth();
    fetchCases();
  }, []);

  return (
    <div className="min-h-screen flex flex-col bg-[#050811] text-slate-100 font-sans selection:bg-cyan-500 selection:text-slate-950">
      {/* Top Tactical Navigation */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        cases={cases}
        selectedCaseId={selectedCaseId}
        setSelectedCaseId={setSelectedCaseId}
        healthInfo={healthInfo}
      />

      {/* Main Forensic Tactical View */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <DisclaimerBanner />

        {/* Back to Dashboard Navigation Button */}
        {activeTab !== 'dashboard' && (
          <div className="mb-6">
            <button
              onClick={() => setActiveTab('dashboard')}
              className="inline-flex items-center gap-2 text-xs font-semibold text-slate-400 hover:text-cyan-400 transition-colors bg-slate-900 border border-slate-800 hover:border-slate-700 px-3 py-1.5 rounded-lg cursor-pointer shadow-sm font-mono"
            >
              <ArrowLeft className="h-3.5 w-3.5" />
              <span>RETURN TO WORKSTATION DASHBOARD</span>
            </button>
          </div>
        )}

        {/* Dynamic Telemetry Views */}
        {activeTab === 'dashboard' && (
          <DashboardOverview
            selectedCaseId={selectedCaseId}
            setActiveTab={setActiveTab}
          />
        )}

        {activeTab === 'image' && (
          <EvidenceVision selectedCaseId={selectedCaseId} />
        )}

        {activeTab === 'audio' && (
          <AudioForensics selectedCaseId={selectedCaseId} />
        )}

        {activeTab === 'video' && (
          <VideoSurveillance selectedCaseId={selectedCaseId} />
        )}

        {activeTab === 'fusion' && (
          <TimelineFusion selectedCaseId={selectedCaseId} />
        )}

        {activeTab === 'chat' && (
          <CopilotChat selectedCaseId={selectedCaseId} />
        )}

        {activeTab === 'report' && (
          <ReportGenerator selectedCaseId={selectedCaseId} />
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800/80 bg-[#04060d] py-6 text-center text-xs text-slate-500 font-mono">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-3">
          <span>CrimeVision AI • Intelligent Multimodal Forensic Analysis Platform</span>
          <span>FastAPI REST • Google Gemini 1.5 • ReportLab PDF • SQLite DB</span>
        </div>
      </footer>
    </div>
  );
}
