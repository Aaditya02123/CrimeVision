import React from 'react';
import { AlertTriangle, ShieldCheck } from 'lucide-react';

export default function DisclaimerBanner() {
  return (
    <div className="mb-6 rounded-xl border border-amber-500/30 bg-amber-500/10 px-4 py-3 text-amber-200/90 shadow-sm backdrop-blur-sm">
      <div className="flex items-start gap-3">
        <AlertTriangle className="mt-0.5 h-5 w-5 flex-shrink-0 text-amber-400" />
        <div className="text-xs leading-relaxed">
          <strong className="font-semibold text-amber-300 uppercase tracking-wider block mb-0.5">
            Restricted Law Enforcement & Digital Forensic Telemetry Notice
          </strong>
          All multimodal evaluations (facial telemetry, acoustic signatures, ballistics detection, and automated timeline synthesis) are preliminary analytical aids. Final court evidentiary filing requires certified chain-of-custody corroboration under Federal Rules of Evidence Rule 901 / ISO/IEC 27037 standards.
        </div>
      </div>
    </div>
  );
}
