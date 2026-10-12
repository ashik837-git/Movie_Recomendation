"use client";

import React, { useEffect, useState } from "react";
import { X, Play, Plus, Check, Star, Sparkles, User, Tag, Calendar, Clock, Film } from "lucide-react";
import { Movie } from "@/types";
import { api } from "@/lib/api";

interface MovieDetailsModalProps {
  movie: Movie | null;
  isOpen: boolean;
  onClose: () => void;
  onPlayTrailer: (movie: Movie) => void;
  onSelectSimilar: (movie: Movie) => void;
}

export default function MovieDetailsModal({
  movie,
  isOpen,
  onClose,
  onPlayTrailer,
  onSelectSimilar,
}: MovieDetailsModalProps) {
  const [similarMovies, setSimilarMovies] = useState<Movie[]>([]);
  const [isLoadingSimilar, setIsLoadingSimilar] = useState(false);
  const [inWatchlist, setInWatchlist] = useState(false);

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

  // Fetch similar recommendations on movie change
  useEffect(() => {
    if (!movie) return;
    let isMounted = true;
    setIsLoadingSimilar(true);
    api
      .getSimilarMovies(movie.id, 6)
      .then((data) => {
        if (isMounted) {
          setSimilarMovies(data);
          setIsLoadingSimilar(false);
        }
      })
      .catch(() => {
        if (isMounted) {
          setSimilarMovies([]);
          setIsLoadingSimilar(false);
        }
      });

    return () => {
      isMounted = false;
    };
  }, [movie]);

  if (!isOpen || !movie) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 bg-black/85 backdrop-blur-md overflow-y-auto animate-fade-in"
      role="dialog"
      aria-modal="true"
      aria-labelledby="movie-details-title"
    >
      {/* Background backdrop click */}
      <div className="fixed inset-0" onClick={onClose} />

      <div className="relative w-full max-w-4xl my-auto bg-[#181818] border border-neutral-800 rounded-2xl overflow-hidden shadow-2xl z-10 animate-scale-up max-h-[90vh] flex flex-col">
        {/* Header Banner / Poster Backdrop */}
        <div className="relative h-64 sm:h-80 bg-gradient-to-r from-red-950 via-neutral-900 to-black p-6 flex flex-col justify-end">
          <div className="absolute inset-0 bg-gradient-to-t from-[#181818] via-transparent to-black/60" />

          {/* Close button */}
          <button
            onClick={onClose}
            className="absolute top-4 right-4 z-20 p-2 rounded-full bg-black/60 hover:bg-neutral-800 text-neutral-300 hover:text-white transition-colors focus:outline-none"
            aria-label="Close details"
          >
            <X className="w-5 h-5" />
          </button>

          {/* Title & Key Stats */}
          <div className="relative z-10 space-y-2">
            <div className="flex flex-wrap items-center gap-2">
              <span className="px-2.5 py-0.5 rounded-full bg-[#E50914] text-white text-xs font-bold">
                {movie.release_year}
              </span>
              {movie.runtime > 0 && (
                <span className="text-xs text-neutral-300 font-medium">
                  {movie.runtime} min
                </span>
              )}
              {movie.weighted_rating > 0 && (
                <div className="flex items-center space-x-1 text-xs text-amber-400 font-bold bg-amber-500/10 px-2 py-0.5 rounded-full border border-amber-500/20">
                  <Star className="w-3 h-3 fill-amber-400" />
                  <span>{movie.weighted_rating.toFixed(1)} IMDb Score</span>
                </div>
              )}
            </div>

            <h2 id="movie-details-title" className="text-2xl sm:text-4xl font-black text-white tracking-tight">
              {movie.title}
            </h2>

            {movie.tagline && (
              <p className="text-xs sm:text-sm text-neutral-300 italic font-medium">
                "{movie.tagline}"
              </p>
            )}
          </div>
        </div>

        {/* Modal Scrollable Body */}
        <div className="p-6 sm:p-8 space-y-8 overflow-y-auto">
          {/* Action Row */}
          <div className="flex flex-wrap items-center gap-4 border-b border-neutral-800 pb-6">
            <button
              onClick={() => onPlayTrailer(movie)}
              className="flex items-center space-x-2 px-6 py-2.5 rounded-xl bg-[#E50914] hover:bg-[#F40612] text-white font-bold text-sm shadow-lg shadow-[#E50914]/25 transition-all"
            >
              <Play className="w-4 h-4 fill-white" />
              <span>Watch Trailer</span>
            </button>

            <button
              onClick={() => setInWatchlist(!inWatchlist)}
              className={`flex items-center space-x-2 px-5 py-2.5 rounded-xl border font-semibold text-sm transition-all ${
                inWatchlist
                  ? "bg-emerald-600/20 border-emerald-500 text-emerald-300"
                  : "bg-white/10 border-white/20 text-white hover:bg-white/20"
              }`}
            >
              {inWatchlist ? <Check className="w-4 h-4" /> : <Plus className="w-4 h-4" />}
              <span>{inWatchlist ? "Saved in My List" : "Add to My List"}</span>
            </button>
          </div>

          {/* Synopsis & Key Credits Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="md:col-span-2 space-y-4">
              <h3 className="text-sm font-bold uppercase tracking-wider text-neutral-400">Synopsis</h3>
              <p className="text-neutral-200 text-sm sm:text-base leading-relaxed">
                {movie.overview || "No extended overview recorded for this title."}
              </p>

              {/* Keywords chips */}
              {movie.keywords && movie.keywords.length > 0 && (
                <div className="pt-2">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-neutral-500 mb-2">Thematic Motifs</h4>
                  <div className="flex flex-wrap gap-1.5">
                    {movie.keywords.map((kw) => (
                      <span
                        key={kw}
                        className="text-xs px-2.5 py-1 rounded-full bg-neutral-800/80 text-neutral-300 border border-neutral-700/50"
                      >
                        #{kw}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Right Column: Cast, Director, Genres */}
            <div className="space-y-4 bg-neutral-900/60 p-5 rounded-xl border border-neutral-800">
              {movie.director && (
                <div>
                  <span className="text-xs font-bold uppercase tracking-wider text-neutral-400 block mb-1">
                    Director
                  </span>
                  <p className="text-white text-sm font-semibold">{movie.director}</p>
                </div>
              )}

              {movie.cast && movie.cast.length > 0 && (
                <div>
                  <span className="text-xs font-bold uppercase tracking-wider text-neutral-400 block mb-1">
                    Top Cast
                  </span>
                  <p className="text-neutral-300 text-xs sm:text-sm leading-relaxed">
                    {movie.cast.join(", ")}
                  </p>
                </div>
              )}

              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-neutral-400 block mb-1">
                  Genres
                </span>
                <div className="flex flex-wrap gap-1 mt-1">
                  {movie.genres.map((g) => (
                    <span
                      key={g}
                      className="text-xs font-medium px-2 py-0.5 rounded bg-white/10 text-neutral-200"
                    >
                      {g}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Algorithmic NLP Recommendations with Truthful Explanations */}
          <div className="space-y-4 pt-4 border-t border-neutral-800">
            <div className="flex items-center space-x-2">
              <Sparkles className="w-5 h-5 text-[#E50914]" />
              <h3 className="text-lg font-bold text-white">
                More Like This <span className="text-xs font-normal text-neutral-400">(NLP Similarity Engine)</span>
              </h3>
            </div>

            {isLoadingSimilar ? (
              <div className="h-40 flex items-center justify-center text-neutral-500 text-sm animate-pulse">
                Computing sparse cosine similarity...
              </div>
            ) : similarMovies.length === 0 ? (
              <p className="text-neutral-500 text-sm">No closely matching titles found in catalog.</p>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                {similarMovies.map((similar) => {
                  const expl = similar.recommendation_explanation;
                  return (
                    <div
                      key={similar.id}
                      onClick={() => onSelectSimilar(similar)}
                      className="group p-3.5 rounded-xl bg-neutral-900 border border-neutral-800 hover:border-[#E50914]/50 cursor-pointer transition-all hover:bg-neutral-850 flex flex-col justify-between space-y-2.5"
                    >
                      <div>
                        <div className="flex items-center justify-between text-xs text-neutral-400 mb-1">
                          <span>{similar.release_year}</span>
                          {similar.similarity_score !== undefined && (
                            <span className="text-emerald-400 font-bold">
                              {Math.round(similar.similarity_score * 100)}% Match
                            </span>
                          )}
                        </div>
                        <h4 className="text-sm font-bold text-white group-hover:text-[#E50914] transition-colors line-clamp-1">
                          {similar.title}
                        </h4>
                        {similar.director && (
                          <p className="text-[11px] text-neutral-400 truncate">dir. {similar.director}</p>
                        )}
                      </div>

                      {/* Truthful Recommendation Explanation Chips */}
                      {expl && (
                        <div className="pt-2 border-t border-neutral-800/80 space-y-1">
                          <span className="text-[10px] uppercase font-bold text-neutral-500 tracking-wider">
                            Why Recommended:
                          </span>
                          <p className="text-[11px] text-neutral-300 font-medium line-clamp-2 leading-snug">
                            {expl.summary}
                          </p>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
