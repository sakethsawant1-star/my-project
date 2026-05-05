import React from 'react';

interface RecommendationProps {
  name: string;
  rationale: string;
  rank: number;
}

export function RecommendationCard({ name, rationale, rank }: RecommendationProps) {
  return (
    <div className="glass-card p-6 mb-4 group hover:-translate-y-1 hover:shadow-primary/20 transition-all duration-300 relative overflow-hidden">
      {/* Decorative rank number */}
      <div className="absolute -right-4 -top-6 text-[100px] font-black text-slate-700/10 group-hover:text-primary/10 transition-colors pointer-events-none select-none">
        {rank}
      </div>
      
      <div className="relative z-10">
        <h3 className="text-2xl font-bold text-slate-100 mb-3 flex items-center gap-3">
          <span className="flex items-center justify-center w-8 h-8 rounded-full bg-primary/20 text-primary text-sm">
            {rank}
          </span>
          {name}
        </h3>
        <div className="bg-slate-900/40 rounded-xl p-4 border border-slate-700/30">
          <p className="text-sm text-primary font-semibold mb-1 uppercase tracking-wider">AI Rationale</p>
          <p className="text-slate-300 leading-relaxed">{rationale}</p>
        </div>
      </div>
    </div>
  );
}
