"use client";

import React, { useState, useEffect, useCallback } from "react";
import { Search as SearchIcon, X, Filter, Sparkles } from "lucide-react";
import { Movie, GenreItem } from "@/types";
import { api } from "@/lib/api";
import MovieCard from "@/components/MovieCard";
import MovieDetailsModal from "@/components/MovieDetailsModal";
import TrailerModal from "@/components/TrailerModal";

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [debouncedQuery, setDebouncedQuery] = useState("");
  const [selectedGenre, setSelectedGenre] = useState<string | null>(null);
  const [genres, setGenres] = useState<GenreItem[]>([]);
  const [results, setResults] = useState<Movie[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  // Modals
  const [selectedMovie, setSelectedMovie] = useState<Movie | null>(null);
  const [isDetailsOpen, setIsDetailsOpen] = useState(false);
  const [trailerMovie, setTrailerMovie] = useState<Movie | null>(null);
  const [isTrailerOpen, setIsTrailerOpen] = useState(false);

  // Debounce search input (300ms)
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedQuery(query);
    }, 300);
    return () => clearTimeout(timer);
  }, [query]);

  // Load genre list on mount
  useEffect(() => {
    api.getGenres().then(setGenres).catch(() => {});
  }, []);

  // Execute search
  const performSearch = useCallback(async () => {
    if (!debouncedQuery.trim() && !selectedGenre) {
      // Show popular movies when no query
      api.getPopularMovies(20).then(setResults).catch(() => setResults([]));
      return;
    }
    setIsLoading(true);
    try {
      const data = await api.searchMovies(debouncedQuery, selectedGenre || undefined, 30);
      setResults(data);
    } catch {
      setResults([]);
    } finally {
      setIsLoading(false);
    }
  }, [debouncedQuery, selectedGenre]);

  useEffect(() => {
    performSearch();
  }, [performSearch]);

  return (
    <div className="pt-24 pb-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-8">
      {/* Search Input Bar */}
      <div className="max-w-2xl mx-auto space-y-4 text-center">
        <h1 className="text-3xl font-extrabold text-white tracking-tight">
          Search the <span className="text-[#E50914]">CinePulse</span> Catalog
        </h1>
        <p className="text-sm text-neutral-400">
          Ranked NLP search across titles, directors, cast, and thematic keywords.
        </p>

        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-neutral-400">
            <SearchIcon className="w-5 h-5" />
          </div>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search by title, director (e.g. Elena Vance), actor, or theme..."
            className="w-full pl-12 pr-12 py-3.5 rounded-2xl bg-neutral-900 border border-neutral-700/80 text-white placeholder-neutral-500 text-sm focus:outline-none focus:ring-2 focus:ring-[#E50914] focus:border-transparent transition-all shadow-inner"
          />
          {query && (
            <button
              onClick={() => setQuery("")}
              className="absolute inset-y-0 right-0 pr-4 flex items-center text-neutral-400 hover:text-white"
              aria-label="Clear query"
            >
              <X className="w-5 h-5" />
            </button>
          )}
        </div>

        {/* Genre Pill Filters */}
        {genres.length > 0 && (
          <div className="flex flex-wrap items-center justify-center gap-2 pt-2">
            <button
              onClick={() => setSelectedGenre(null)}
              className={`px-3 py-1 rounded-full text-xs font-semibold transition-all ${
                selectedGenre === null
                  ? "bg-[#E50914] text-white shadow-md shadow-[#E50914]/20"
                  : "bg-neutral-800 text-neutral-400 hover:text-white"
              }`}
            >
              All Genres
            </button>
            {genres.slice(0, 8).map((g) => (
              <button
                key={g.name}
                onClick={() => setSelectedGenre(selectedGenre === g.name ? null : g.name)}
                className={`px-3 py-1 rounded-full text-xs font-semibold transition-all ${
                  selectedGenre === g.name
                    ? "bg-[#E50914] text-white shadow-md shadow-[#E50914]/20"
                    : "bg-neutral-800 text-neutral-400 hover:text-white"
                }`}
              >
                {g.name}
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Results Header */}
      <div className="flex items-center justify-between border-b border-neutral-800 pb-3">
        <span className="text-sm font-semibold text-neutral-400">
          {isLoading
            ? "Searching catalog..."
            : results.length === 0
            ? "No movies found"
            : `Found ${results.length} results ${debouncedQuery ? `for "${debouncedQuery}"` : ""}`}
        </span>
      </div>

      {/* Results Grid */}
      {isLoading ? (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4 animate-pulse">
          {Array.from({ length: 10 }).map((_, i) => (
            <div key={i} className="aspect-[2/3] rounded-xl bg-neutral-800/50" />
          ))}
        </div>
      ) : results.length === 0 ? (
        <div className="py-20 text-center space-y-3">
          <div className="w-12 h-12 mx-auto rounded-full bg-neutral-800 flex items-center justify-center text-neutral-500">
            <SearchIcon className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-white">No exact matches found</h3>
          <p className="text-sm text-neutral-400 max-w-sm mx-auto">
            Try adjusting your search terms or selecting a different genre filter.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
          {results.map((movie) => (
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
