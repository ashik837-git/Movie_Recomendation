"use client";

import React, { useState, useEffect } from "react";
import { Bookmark, Film, Sparkles, ArrowRight } from "lucide-react";
import Link from "next/link";
import { Movie } from "@/types";
import { api } from "@/lib/api";
import MovieCard from "@/components/MovieCard";
import MovieDetailsModal from "@/components/MovieDetailsModal";
import TrailerModal from "@/components/TrailerModal";

export default function MyListPage() {
  const [watchlist, setWatchlist] = useState<Movie[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Modals
  const [selectedMovie, setSelectedMovie] = useState<Movie | null>(null);
  const [isDetailsOpen, setIsDetailsOpen] = useState(false);
  const [trailerMovie, setTrailerMovie] = useState<Movie | null>(null);
  const [isTrailerOpen, setIsTrailerOpen] = useState(false);

  useEffect(() => {
    // In dev / public demo mode, fetch watchlist with mock token
    api
      .getWatchlist("mock_user_demo")
      .then((items) => {
        setWatchlist(items);
        setIsLoading(false);
      })
      .catch(() => {
        // Fallback default
        setWatchlist([]);
        setIsLoading(false);
      });
  }, []);

  return (
    <div className="pt-24 pb-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-6">
      <div className="border-b border-neutral-800 pb-4">
        <h1 className="text-3xl font-extrabold text-white tracking-tight flex items-center space-x-2">
          <Bookmark className="w-7 h-7 text-[#E50914]" />
          <span>My Watchlist</span>
        </h1>
        <p className="text-sm text-neutral-400 mt-1">
          Films saved for discovery and personal recommendation alignment.
        </p>
      </div>

      {isLoading ? (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4 animate-pulse">
          {Array.from({ length: 5 }).map((_, i) => (
            <div key={i} className="aspect-[2/3] rounded-xl bg-neutral-800/50" />
          ))}
        </div>
      ) : watchlist.length === 0 ? (
        <div className="py-24 text-center space-y-4 max-w-md mx-auto">
          <div className="w-14 h-14 mx-auto rounded-full bg-neutral-900 border border-neutral-800 flex items-center justify-center text-neutral-500">
            <Bookmark className="w-6 h-6" />
          </div>
          <h2 className="text-xl font-bold text-white">Your list is empty</h2>
          <p className="text-sm text-neutral-400">
            Explore the catalog and click the "+" icon on any film card to save it to your personal watchlist.
          </p>
          <div className="pt-2">
            <Link
              href="/movies"
              className="inline-flex items-center space-x-2 px-5 py-2.5 rounded-xl bg-[#E50914] text-white font-semibold text-sm hover:bg-[#F40612] transition-colors"
            >
              <span>Explore Movies</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
          {watchlist.map((movie) => (
            <MovieCard
              key={movie.id}
              movie={movie}
              isWatchlisted={true}
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
