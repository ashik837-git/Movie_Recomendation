"use client";

import React, { useEffect } from "react";
import { X, Play, AlertCircle, ExternalLink, Film } from "lucide-react";
import { Movie } from "@/types";

interface TrailerModalProps {
  movie: Movie | null;
  isOpen: boolean;
  onClose: () => void;
}

export default function TrailerModal({ movie, isOpen, onClose }: TrailerModalProps) {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    if (isOpen) {
      document.body.style.overflow = "hidden";
      window.addEventListener("keydown", handleKeyDown);
    }
    return () => {
      document.body.style.overflow = "auto";
      window.removeEventListener("keydown", handleKeyDown);
    };
  }, [isOpen, onClose]);

  if (!isOpen || !movie) return null;

  const searchQuery = encodeURIComponent(`${movie.title} ${movie.release_year} official trailer`);
  const youtubeUrl = `https://www.youtube.com/results?search_query=${searchQuery}`;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-fade-in"
      role="dialog"
      aria-modal="true"
      aria-labelledby="trailer-modal-title"
    >
      {/* Click outside backdrop */}
      <div className="absolute inset-0" onClick={onClose} />

      <div className="relative w-full max-w-2xl bg-[#181818] border border-neutral-800 rounded-2xl overflow-hidden shadow-2xl z-10 animate-scale-up">
        {/* Modal Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-neutral-800 bg-[#141414]">
          <div className="flex items-center space-x-2">
            <Film className="w-5 h-5 text-[#E50914]" />
            <h2 id="trailer-modal-title" className="text-lg font-bold text-white truncate max-w-md">
              {movie.title} ({movie.release_year})
            </h2>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-full text-neutral-400 hover:text-white hover:bg-neutral-800 transition-colors focus:outline-none"
            aria-label="Close dialog"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content Box */}
        <div className="p-6 space-y-6">
          <div className="relative aspect-video rounded-xl bg-gradient-to-br from-neutral-900 to-black border border-neutral-800 flex flex-col items-center justify-center p-6 text-center">
            {/* Disclaimer pill */}
            <div className="mb-4 inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/20 text-amber-400 text-xs font-semibold">
              <AlertCircle className="w-3.5 h-3.5" />
              <span>Discovery Platform • Non-Streaming Engine</span>
            </div>

            <h3 className="text-xl font-bold text-white mb-2">Official Trailer Preview</h3>
            <p className="text-sm text-neutral-400 max-w-md mb-6">
              CinePulse provides algorithmic NLP recommendations. In accordance with copyright compliance, full-length feature playback is not hosted.
            </p>

            <a
              href={youtubeUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center space-x-2 px-6 py-3 rounded-xl bg-[#E50914] hover:bg-[#F40612] text-white font-bold text-sm shadow-lg shadow-[#E50914]/30 hover:scale-105 transition-all focus:ring-2 focus:ring-white"
            >
              <Play className="w-4 h-4 fill-white" />
              <span>Watch Official Trailer on YouTube</span>
              <ExternalLink className="w-4 h-4 ml-1 opacity-75" />
            </a>
          </div>

          <div className="flex items-start space-x-3 text-xs text-neutral-500 bg-neutral-900/60 p-3 rounded-lg border border-neutral-800">
            <span className="font-semibold text-neutral-400">Notice:</span>
            <span>
              Metadata attributed to TMDB. All trailers belong to their respective production studios and distributors.
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
