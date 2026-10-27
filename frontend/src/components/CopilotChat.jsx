import React, { useState } from 'react';
import { Bot, Send, User, Sparkles, CornerDownLeft, Shield, Clock } from 'lucide-react';

export default function CopilotChat({ selectedCaseId }) {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: `Forensic AI Copilot online for case ${selectedCaseId}. I have ingested the case evidence records, audio dispatch logs, and surveillance keyframes. Ask me anything regarding weapon classifications, suspect statements, or timeline contradictions.`,
      citations: []
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const suggestedQuestions = [
    'What firearms and weapons were identified at the breach point?',
    'Did any audio transcripts contradict the surveillance timeline?',
    'What are the statutory legal elements for this indictment?',
    'Summarize suspect physical attributes and movements.'
  ];

  const handleSend = async (queryText) => {
    const textToSend = queryText || input;
    if (!textToSend.trim() || loading) return;

    const userMsg = { role: 'user', content: textToSend, citations: [] };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const res = await fetch('/api/v1/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          case_id: selectedCaseId,
          message: textToSend
        }),
      });

      if (!res.ok) {
        throw new Error('AI Copilot request failed.');
      }

      const data = await res.json();
      const botMsg = {
        role: 'assistant',
        content: data.reply || 'No analysis returned.',
        citations: data.citations || []
      };
      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: 'Unable to query forensic knowledge base. Please check backend connection.',
          citations: []
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="border-b border-slate-800 pb-4">
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <Bot className="h-5 w-5 text-cyan-400" />
          Forensic Investigator AI Copilot
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Direct multimodal inquiry assistant trained on criminalistics evidence matrices, statutory codes, and forensic event logs.
        </p>
      </div>

      <div className="rounded-xl border border-slate-800 bg-[#080d1e]/90 shadow-xl flex flex-col h-[600px] overflow-hidden">
        {/* Messages Stream */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((msg, idx) => {
            const isUser = msg.role === 'user';
            return (
              <div key={idx} className={`flex items-start gap-3 ${isUser ? 'flex-row-reverse' : ''}`}>
                <div className={`h-8 w-8 rounded-lg flex items-center justify-center flex-shrink-0 text-xs ${
                  isUser 
                    ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30' 
                    : 'bg-indigo-500/20 text-indigo-400 border border-indigo-500/30'
                }`}>
                  {isUser ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
                </div>

                <div className={`max-w-[80%] rounded-2xl p-4 text-xs space-y-2 leading-relaxed ${
                  isUser 
                    ? 'bg-cyan-600/20 border border-cyan-500/30 text-white rounded-tr-none' 
                    : 'bg-slate-900/80 border border-slate-800 text-slate-200 rounded-tl-none shadow-sm'
                }`}>
                  <p className="whitespace-pre-wrap">{msg.content}</p>

                  {msg.citations && msg.citations.length > 0 && (
                    <div className="pt-2 border-t border-slate-800 flex flex-wrap gap-1.5 font-mono text-[10px]">
                      <span className="text-slate-500">Evidence Citations:</span>
                      {msg.citations.map((c, cIdx) => (
                        <span key={cIdx} className="px-1.5 py-0.5 rounded bg-slate-800 text-cyan-400 border border-slate-700">
                          {typeof c === 'object' && c !== null ? `${c.source || ''} ${c.timestamp ? '@ ' + c.timestamp : ''}: ${c.details || ''}`.trim() : String(c)}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            );
          })}

          {loading && (
            <div className="flex items-start gap-3">
              <div className="h-8 w-8 rounded-lg bg-indigo-500/20 text-indigo-400 border border-indigo-500/30 flex items-center justify-center flex-shrink-0">
                <Bot className="h-4 w-4" />
              </div>
              <div className="rounded-2xl rounded-tl-none p-3.5 bg-slate-900/80 border border-slate-800 text-xs text-slate-400 flex items-center gap-2 font-mono">
                <div className="h-3 w-3 border-2 border-cyan-400 border-t-transparent rounded-full animate-spin" />
                <span>CROSS-REFERENCING FORENSIC KNOWLEDGE BASE...</span>
              </div>
            </div>
          )}
        </div>

        {/* Suggested Prompts */}
        <div className="p-3 border-t border-slate-800/80 bg-slate-950/40">
          <div className="flex items-center gap-2 overflow-x-auto pb-1 scrollbar-none">
            <span className="text-[11px] text-slate-500 whitespace-nowrap font-mono flex items-center gap-1">
              <Sparkles className="h-3 w-3 text-cyan-400" /> Prompts:
            </span>
            {suggestedQuestions.map((q, idx) => (
              <button
                key={idx}
                onClick={() => handleSend(q)}
                disabled={loading}
                className="text-[11px] px-2.5 py-1 rounded-full bg-slate-900 border border-slate-800 hover:border-cyan-500/40 text-slate-300 hover:text-cyan-300 whitespace-nowrap transition-colors cursor-pointer"
              >
                {q}
              </button>
            ))}
          </div>
        </div>

        {/* Input Bar */}
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSend();
          }}
          className="p-3 border-t border-slate-800 bg-[#060a16] flex items-center gap-2"
        >
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={`Query evidence records for ${selectedCaseId}...`}
            className="flex-1 bg-slate-900/90 border border-slate-800 focus:border-cyan-500 text-xs text-white rounded-xl px-4 py-2.5 focus:outline-none font-sans placeholder-slate-500"
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="h-10 w-10 rounded-xl bg-cyan-500 hover:bg-cyan-400 disabled:opacity-40 text-slate-950 flex items-center justify-center transition-all cursor-pointer flex-shrink-0"
          >
            <Send className="h-4 w-4" />
          </button>
        </form>
      </div>
    </div>
  );
}
