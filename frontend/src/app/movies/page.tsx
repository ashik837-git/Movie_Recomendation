"use client";

import React, { useState, useEffect } from "react";
import { Film, ChevronLeft, ChevronRight, Filter } from "lucide-react";
import { Movie, GenreItem, PaginatedMovies } from "@/types";
import { api } from "@/lib/api";
import MovieCard from "@/components/MovieCard";
import MovieDetailsModal from "@/components/MovieDetailsModal";
import TrailerModal from "@/components/TrailerModal";

export default function MoviesPage() {
  const [data, setData] = useState<PaginatedMovies | null>(null);
  const [page, setPage] = useState(1);
  const [selectedGenre, setSelectedGenre] = useState<string | null>(null);
  const [genres, setGenres] = useState<GenreItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Modals
  const [selectedMovie, setSelectedMovie] = useState<Movie | null>(null);
  const [isDetailsOpen, setIsDetailsOpen] = useState(false);
  const [trailerMovie, setTrailerMovie] = useState<Movie | null>(null);
  const [isTrailerOpen, setIsTrailerOpen] = useState(false);

  useEffect(() => {
    api.getGenres().then(setGenres).catch(() => {});
  }, []);

  useEffect(() => {
    setIsLoading(true);
    api
      .getMovies(page, 20, selectedGenre || undefined)
      .then((res) => {
        setData(res);
        setIsLoading(false);
      })
      .catch(() => {
        setData(null);
        setIsLoading(false);
      });
  }, [page, selectedGenre]);

  const handleGenreChange = (g: string | null) => {
    setSelectedGenre(g);
    setPage(1);
  };

  return (
    <div className="pt-24 pb-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-6">
      {/* Title & Filter Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-neutral-800 pb-4">
        <div>
          <h1 className="text-3xl font-extrabold text-white tracking-tight flex items-center space-x-2">
            <span>Movie Catalog</span>
          </h1>
          <p className="text-sm text-neutral-400">
            Browse verified titles preprocessed for our natural language recommendation engine.
          </p>
        </div>

        {/* Genre Selector */}
        {genres.length > 0 && (
          <div className="flex items-center space-x-2 overflow-x-auto no-scrollbar py-1">
            <button
              onClick={() => handleGenreChange(null)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-colors ${
                selectedGenre === null
                  ? "bg-[#E50914] text-white"
                  : "bg-neutral-800 text-neutral-400 hover:text-white"
              }`}
            >
              All Genres
            </button>
            {genres.map((g) => (
              <button
                key={g.name}
                onClick={() => handleGenreChange(selectedGenre === g.name ? null : g.name)}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-colors ${
                  selectedGenre === g.name
                    ? "bg-[#E50914] text-white"
                    : "bg-neutral-800 text-neutral-400 hover:text-white"
                }`}
              >
                {g.name} ({g.count})
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Grid Content */}
      {isLoading ? (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4 animate-pulse">
          {Array.from({ length: 15 }).map((_, i) => (
            <div key={i} className="aspect-[2/3] rounded-xl bg-neutral-800/50" />
          ))}
        </div>
      ) : !data || data.items.length === 0 ? (
        <div className="py-20 text-center text-neutral-400">
          <p>No movies found matching current filters.</p>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
            {data.items.map((movie) => (
              <MovieCard
                key={movie.id}
                movie={movie}
                onSelect={(m) => {
                  setSelectedMovie(m);
                  setIsDetailsOpen(true);
                }}
                onPlayTrailer={(m) => {
                  setTrailerMovie(m);
                  setIsTrailerOpen(true);
                }}
              />
            ))}
          </div>

          {/* Pagination Controls */}
          <div className="flex items-center justify-between pt-8 border-t border-neutral-800">
            <span className="text-xs text-neutral-400">
              Page {data.page} of {data.total_pages} ({data.total} total films)
            </span>

            <div className="flex items-center space-x-2">
              <button
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                disabled={data.page <= 1}
                className="p-2 rounded-lg bg-neutral-800 text-white hover:bg-neutral-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
                aria-label="Previous page"
              >
                <ChevronLeft className="w-5 h-5" />
              </button>
              <button
                onClick={() => setPage((p) => Math.min(data.total_pages, p + 1))}
                disabled={data.page >= data.total_pages}
                className="p-2 rounded-lg bg-neutral-800 text-white hover:bg-neutral-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
                aria-label="Next page"
              >
                <ChevronRight className="w-5 h-5" />
              </button>
            </div>
          </div>
        </>
      )}

      {/* Modals */}
      <MovieDetailsModal
        movie={selectedMovie}
        isOpen={isDetailsOpen}
        onClose={() => setIsDetailsOpen(false)}
        onPlayTrailer={(m) => {
          setTrailerMovie(m);
          setIsTrailerOpen(true);
        }}
        onSelectSimilar={(similar) => setSelectedMovie(similar)}
      />

      <TrailerModal
        movie={trailerMovie}
        isOpen={isTrailerOpen}
        onClose={() => setIsTrailerOpen(false)}
      />
    </div>
  );
}
