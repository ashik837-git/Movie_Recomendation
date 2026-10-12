"use client";

import React, { useState } from "react";
import { Plus, Check, Star, Play, Info, Sparkles } from "lucide-react";
import { Movie } from "@/types";

interface MovieCardProps {
  movie: Movie;
  onSelect: (movie: Movie) => void;
  onPlayTrailer?: (movie: Movie) => void;
  isWatchlisted?: boolean;
  onToggleWatchlist?: (movieId: number) => void;
}

// Deterministic cinematic gradient generator based on title characters
function getPosterGradient(title: string, id: number): string {
  const gradients = [
    "from-purple-900 via-indigo-950 to-neutral-900",
    "from-red-950 via-rose-900 to-neutral-950",
    "from-blue-950 via-slate-900 to-neutral-900",
    "from-emerald-950 via-teal-900 to-neutral-950",
    "from-amber-950 via-yellow-900 to-neutral-900",
    "from-cyan-950 via-sky-900 to-neutral-950",
    "from-fuchsia-950 via-pink-900 to-neutral-900",
  ];
  const charCodeSum = title.split("").reduce((acc, char) => acc + char.charCodeAt(0), id);
  return gradients[charCodeSum % gradients.length];
}

export default function MovieCard({
  movie,
  onSelect,
  onPlayTrailer,
  isWatchlisted = false,
  onToggleWatchlist,
}: MovieCardProps) {
  const [inList, setInList] = useState(isWatchlisted);
  const gradientClass = getPosterGradient(movie.title, movie.id);

  const handleWatchlistClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    setInList(!inList);
    if (onToggleWatchlist) {
      onToggleWatchlist(movie.id);
    }
  };

  return (
    <div
      onClick={() => onSelect(movie)}
      tabIndex={0}
      role="button"
      onKeyDown={(e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          onSelect(movie);
        }
      }}
      className="group relative flex-shrink-0 w-44 sm:w-52 md:w-60 aspect-[2/3] rounded-xl overflow-hidden cursor-pointer select-none bg-neutral-900 border border-neutral-800 transition-all duration-300 transform-gpu hover:scale-105 hover:z-20 hover:shadow-2xl hover:shadow-black/90 focus:outline-none focus:ring-2 focus:ring-[#E50914]"
      aria-label={`${movie.title}, released in ${movie.release_year}`}
    >
      {/* Poster image or fallback gradient art */}
      <div className={`w-full h-full bg-gradient-to-br ${gradientClass} flex flex-col justify-between p-4 relative`}>
        {/* Subtle decorative grid/film overlay */}
        <div className="absolute inset-0 bg-black/30 backdrop-blur-[1px]" />

        {/* Top Badges */}
        <div className="relative z-10 flex items-center justify-between">
          <span className="px-2 py-0.5 rounded-md bg-black/60 backdrop-blur-md border border-white/10 text-[11px] font-bold text-neutral-300">
            {movie.release_year || "Film"}
          </span>

          {movie.weighted_rating > 0 && (
            <div className="flex items-center space-x-1 px-2 py-0.5 rounded-md bg-amber-500/20 border border-amber-500/30 text-amber-400 text-[11px] font-bold">
              <Star className="w-3 h-3 fill-amber-400" />
              <span>{movie.weighted_rating.toFixed(1)}</span>
            </div>
          )}
        </div>

        {/* Center Title Display on Fallback Artwork */}
        <div className="relative z-10 my-auto text-center px-2">
          <div className="w-10 h-10 mx-auto mb-2 rounded-full bg-white/10 flex items-center justify-center border border-white/10 group-hover:scale-110 transition-transform">
            <span className="text-[#E50914] text-lg font-black">◈</span>
          </div>
          <h4 className="text-white font-bold text-base line-clamp-2 leading-snug drop-shadow-md">
            {movie.title}
          </h4>
          {movie.director && (
            <p className="text-neutral-400 text-xs mt-1 truncate">
              dir. {movie.director}
            </p>
          )}
        </div>

        {/* Bottom Metadata & Primary Genre */}
        <div className="relative z-10 space-y-1">
          <div className="flex flex-wrap gap-1">
            {movie.genres.slice(0, 2).map((g) => (
              <span
                key={g}
                className="text-[10px] uppercase font-semibold px-1.5 py-0.5 rounded bg-white/10 text-neutral-300 backdrop-blur-sm"
              >
                {g}
              </span>
            ))}
          </div>

          {/* Similarity match chip if present */}
          {movie.similarity_score !== undefined && (
            <div className="inline-flex items-center space-x-1 text-[10px] text-emerald-400 font-bold bg-emerald-950/80 px-2 py-0.5 rounded-full border border-emerald-500/30">
              <Sparkles className="w-2.5 h-2.5" />
              <span>{Math.round(movie.similarity_score * 100)}% Match</span>
            </div>
          )}
        </div>

        {/* Hover / Focus Overlay with Action Buttons */}
        <div className="absolute inset-0 z-20 bg-gradient-to-t from-black via-black/75 to-transparent opacity-0 group-hover:opacity-100 group-focus:opacity-100 transition-opacity duration-300 flex flex-col justify-end p-4">
          <h4 className="text-white font-bold text-sm line-clamp-2 mb-1">{movie.title}</h4>
          <p className="text-neutral-300 text-[11px] line-clamp-2 mb-3 leading-relaxed">
            {movie.overview || movie.tagline || "No synopsis available."}
          </p>

          <div className="flex items-center justify-between pt-1 border-t border-white/10">
            <button
              onClick={(e) => {
                e.stopPropagation();
                if (onPlayTrailer) onPlayTrailer(movie);
                else onSelect(movie);
              }}
              className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-[#E50914] hover:bg-[#F40612] text-white text-xs font-bold transition-all shadow-md"
              aria-label={`Play trailer for ${movie.title}`}
            >
              <Play className="w-3.5 h-3.5 fill-white" />
              <span>Trailer</span>
            </button>

            <button
              onClick={handleWatchlistClick}
              className={`p-1.5 rounded-lg border transition-all ${
                inList
                  ? "bg-emerald-600/30 border-emerald-500/50 text-emerald-300"
                  : "bg-white/10 border-white/20 text-white hover:bg-white/20"
              }`}
              title={inList ? "In My List" : "Add to My List"}
              aria-label={inList ? `Remove ${movie.title} from My List` : `Add ${movie.title} to My List`}
            >
              {inList ? <Check className="w-4 h-4" /> : <Plus className="w-4 h-4" />}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
