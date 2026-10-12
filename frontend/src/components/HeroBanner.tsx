"use client";

import React from "react";
import { Play, Info, Star, Clock, Calendar, Sparkles } from "lucide-react";
import { Movie } from "@/types";

interface HeroBannerProps {
  movie: Movie | null;
  onPlayTrailer: (movie: Movie) => void;
  onMoreInfo: (movie: Movie) => void;
}

export default function HeroBanner({ movie, onPlayTrailer, onMoreInfo }: HeroBannerProps) {
  if (!movie) {
    return (
      <div className="relative h-[65vh] md:h-[75vh] w-full bg-[#181818] animate-pulse flex items-center justify-center">
        <span className="text-neutral-500 font-medium">Loading featured film spotlight...</span>
      </div>
    );
  }

  return (
    <div className="relative h-[65vh] md:h-[80vh] w-full select-none overflow-hidden bg-neutral-950">
      {/* Background with dynamic atmospheric cinema gradient */}
      <div className="absolute inset-0 bg-gradient-to-r from-red-950/40 via-neutral-900 to-black/90">
        {/* Film grain effect & lighting accents */}
        <div className="absolute inset-0 bg-radial-vignette opacity-80" />
      </div>

      {/* Deep cinematic gradient overlays for text readability */}
      <div className="absolute inset-0 bg-gradient-to-t from-[#141414] via-[#141414]/40 to-transparent" />
      <div className="absolute inset-0 bg-gradient-to-r from-[#141414] via-[#141414]/80 to-transparent w-full md:w-3/4" />

      {/* Featured Content Spotlight */}
      <div className="relative z-10 max-w-7xl mx-auto h-full px-4 sm:px-6 lg:px-8 flex flex-col justify-end pb-16 md:pb-24">
        <div className="max-w-2xl space-y-4 animate-fade-in">
          {/* Top Pill Badges */}
          <div className="flex flex-wrap items-center gap-2">
            <span className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-[#E50914]/20 border border-[#E50914]/40 text-[#E50914] text-xs font-black uppercase tracking-wider">
              <Sparkles className="w-3.5 h-3.5" />
              <span>CinePulse Spotlight</span>
            </span>

            {movie.weighted_rating > 0 && (
              <span className="inline-flex items-center space-x-1 px-2.5 py-1 rounded-full bg-amber-500/10 border border-amber-500/20 text-amber-400 text-xs font-bold">
                <Star className="w-3.5 h-3.5 fill-amber-400" />
                <span>{movie.weighted_rating.toFixed(1)} IMDb Weighted</span>
              </span>
            )}

            <span className="text-xs text-neutral-400 font-medium">
              {movie.release_year} • {movie.runtime ? `${movie.runtime} min` : "Feature"}
            </span>
          </div>

          {/* Title */}
          <h1 className="text-3xl sm:text-5xl md:text-6xl font-black text-white tracking-tight leading-tight drop-shadow-lg">
            {movie.title}
          </h1>

          {/* Tagline */}
          {movie.tagline && (
            <p className="text-sm sm:text-base text-neutral-300 italic font-medium">
              "{movie.tagline}"
            </p>
          )}

          {/* Synopsis */}
          <p className="text-sm sm:text-base text-neutral-300 line-clamp-3 leading-relaxed drop-shadow-md">
            {movie.overview}
          </p>

          {/* Genre tags */}
          <div className="flex flex-wrap gap-2 pt-1">
            {movie.genres.map((genre) => (
              <span
                key={genre}
                className="text-xs font-medium px-2.5 py-1 rounded-md bg-white/10 text-neutral-200 border border-white/5 backdrop-blur-sm"
              >
                {genre}
              </span>
            ))}
          </div>

          {/* Action CTAs */}
          <div className="flex items-center space-x-4 pt-4">
            <button
              onClick={() => onPlayTrailer(movie)}
              className="flex items-center space-x-2 px-6 py-3 rounded-xl bg-[#E50914] hover:bg-[#F40612] text-white font-bold text-sm sm:text-base shadow-lg shadow-[#E50914]/30 hover:scale-105 transition-all focus:ring-2 focus:ring-white"
            >
              <Play className="w-5 h-5 fill-white" />
              <span>Watch Trailer</span>
            </button>

            <button
              onClick={() => onMoreInfo(movie)}
              className="flex items-center space-x-2 px-6 py-3 rounded-xl bg-white/20 hover:bg-white/30 text-white font-semibold text-sm sm:text-base backdrop-blur-md transition-all focus:ring-2 focus:ring-white"
            >
              <Info className="w-5 h-5" />
              <span>More Info</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
