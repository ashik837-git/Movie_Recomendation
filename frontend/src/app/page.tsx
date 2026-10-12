"use client";

import React, { useEffect, useState } from "react";
import HeroBanner from "@/components/HeroBanner";
import MovieRow from "@/components/MovieRow";
import MovieDetailsModal from "@/components/MovieDetailsModal";
import TrailerModal from "@/components/TrailerModal";
import { Movie } from "@/types";
import { api } from "@/lib/api";

export default function HomePage() {
  const [featuredMovie, setFeaturedMovie] = useState<Movie | null>(null);
  const [popularMovies, setPopularMovies] = useState<Movie[]>([]);
  const [sciFiMovies, setSciFiMovies] = useState<Movie[]>([]);
  const [actionMovies, setActionMovies] = useState<Movie[]>([]);
  const [becauseYouViewedMovies, setBecauseYouViewedMovies] = useState<Movie[]>([]);
  const [referenceMovieTitle, setReferenceMovieTitle] = useState<string>("Quantum Horizon");

  // Interactive modal states
  const [selectedMovie, setSelectedMovie] = useState<Movie | null>(null);
  const [isDetailsOpen, setIsDetailsOpen] = useState(false);
  const [trailerMovie, setTrailerMovie] = useState<Movie | null>(null);
  const [isTrailerOpen, setIsTrailerOpen] = useState(false);

  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;
    async function loadCatalog() {
      try {
        setIsLoading(true);
        // Load featured spotlight and popular weighted movies
        const [featured, popular, sciFi, action] = await Promise.all([
          api.getFeaturedMovie().catch(() => null),
          api.getPopularMovies(15).catch(() => []),
          api.getPopularMovies(15, "Science Fiction").catch(() => []),
          api.getPopularMovies(15, "Action").catch(() => []),
        ]);

        if (isMounted) {
          setFeaturedMovie(featured || (popular.length > 0 ? popular[0] : null));
          setPopularMovies(popular);
          setSciFiMovies(sciFi);
          setActionMovies(action);

          // Build dynamic "Because You Viewed X" from the real NLP engine using the first popular movie
          const anchorMovie = featured || popular[0];
          if (anchorMovie) {
            setReferenceMovieTitle(anchorMovie.title);
            api.getSimilarMovies(anchorMovie.id, 12).then((similar) => {
              if (isMounted) setBecauseYouViewedMovies(similar);
            }).catch(() => {});
          }
          setIsLoading(false);
        }
      } catch (err: any) {
        if (isMounted) {
          setError(err.message || "Failed to load movie catalog from backend");
          setIsLoading(false);
        }
      }
    }

    loadCatalog();
    return () => {
      isMounted = false;
    };
  }, []);

  const handleSelectMovie = (movie: Movie) => {
    setSelectedMovie(movie);
    setIsDetailsOpen(true);
  };

  const handlePlayTrailer = (movie: Movie) => {
    setTrailerMovie(movie);
    setIsTrailerOpen(true);
  };

  return (
    <div className="relative pb-24">
      {/* Spotlight Hero Banner */}
      <HeroBanner
        movie={featuredMovie}
        onPlayTrailer={handlePlayTrailer}
        onMoreInfo={handleSelectMovie}
      />

      {/* Main Carousels Stream */}
      <div className="-mt-16 sm:-mt-24 relative z-20 space-y-6">
        {error && (
          <div className="max-w-4xl mx-auto my-4 p-4 rounded-xl bg-red-950/50 border border-red-800 text-red-200 text-sm">
            <p className="font-bold">Backend Connection Notice:</p>
            <p>{error}</p>
          </div>
        )}

        {/* 1. Popular / Weighted High-Ranked Titles */}
        <MovieRow
          title="Trending & Critically Acclaimed"
          subtitle="Ranked with IMDb Bayesian weighted formula"
          movies={popularMovies}
          onSelectMovie={handleSelectMovie}
          onPlayTrailer={handlePlayTrailer}
        />

        {/* 2. Algorithmic Similarity Row */}
        {becauseYouViewedMovies.length > 0 && (
          <MovieRow
            title={`Because you viewed "${referenceMovieTitle}"`}
            subtitle="Calculated on demand using TF-IDF sparse cosine similarity"
            movies={becauseYouViewedMovies}
            onSelectMovie={handleSelectMovie}
            onPlayTrailer={handlePlayTrailer}
          />
        )}

        {/* 3. Science Fiction Category */}
        <MovieRow
          title="Science Fiction & Dystopia"
          subtitle="Space exploration, cybernetics, and alternate timelines"
          movies={sciFiMovies}
          onSelectMovie={handleSelectMovie}
          onPlayTrailer={handlePlayTrailer}
        />

        {/* 4. Action & High Stakes */}
        <MovieRow
          title="Action, Heists & Espionage"
          subtitle="High adrenaline tactical thrillers"
          movies={actionMovies}
          onSelectMovie={handleSelectMovie}
          onPlayTrailer={handlePlayTrailer}
        />
      </div>

      {/* Movie Details Modal */}
      <MovieDetailsModal
        movie={selectedMovie}
        isOpen={isDetailsOpen}
        onClose={() => setIsDetailsOpen(false)}
        onPlayTrailer={handlePlayTrailer}
        onSelectSimilar={(similar) => {
          setSelectedMovie(similar);
        }}
      />

      {/* Trailer Dialog Modal */}
      <TrailerModal
        movie={trailerMovie}
        isOpen={isTrailerOpen}
        onClose={() => setIsTrailerOpen(false)}
      />
    </div>
  );
}
