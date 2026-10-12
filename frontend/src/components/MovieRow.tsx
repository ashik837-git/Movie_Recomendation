"use client";

import React, { useRef, useState } from "react";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { Movie } from "@/types";
import MovieCard from "./MovieCard";

interface MovieRowProps {
  title: string;
  subtitle?: string;
  movies: Movie[];
  onSelectMovie: (movie: Movie) => void;
  onPlayTrailer?: (movie: Movie) => void;
}

export default function MovieRow({
  title,
  subtitle,
  movies,
  onSelectMovie,
  onPlayTrailer,
}: MovieRowProps) {
  const rowRef = useRef<HTMLDivElement>(null);
  const [showLeftArrow, setShowLeftArrow] = useState(false);
  const [showRightArrow, setShowRightArrow] = useState(true);

  const handleScroll = () => {
    if (rowRef.current) {
      const { scrollLeft, scrollWidth, clientWidth } = rowRef.current;
      setShowLeftArrow(scrollLeft > 20);
      setShowRightArrow(scrollLeft < scrollWidth - clientWidth - 20);
    }
  };

  const scroll = (direction: "left" | "right") => {
    if (rowRef.current) {
      const { clientWidth } = rowRef.current;
      const scrollAmount = direction === "left" ? -clientWidth * 0.75 : clientWidth * 0.75;
      rowRef.current.scrollBy({ left: scrollAmount, behavior: "smooth" });
    }
  };

  if (!movies || movies.length === 0) return null;

  return (
    <section className="relative my-8 px-4 sm:px-6 lg:px-8 space-y-3">
      {/* Row Header */}
      <div className="flex items-baseline justify-between">
        <div>
          <h2 className="text-xl sm:text-2xl font-bold text-white tracking-tight flex items-center space-x-2">
            <span>{title}</span>
          </h2>
          {subtitle && <p className="text-xs sm:text-sm text-neutral-400 mt-0.5">{subtitle}</p>}
        </div>
      </div>

      {/* Carousel Container */}
      <div className="relative group">
        {/* Left Arrow Button (Desktop) */}
        {showLeftArrow && (
          <button
            onClick={() => scroll("left")}
            className="hidden md:flex absolute -left-4 top-1/2 -translate-y-1/2 z-30 w-10 h-20 items-center justify-center bg-black/70 hover:bg-black/95 text-white rounded-r-lg border-y border-r border-neutral-700/60 shadow-xl transition-all focus:outline-none"
            aria-label={`Scroll ${title} left`}
          >
            <ChevronLeft className="w-6 h-6" />
          </button>
        )}

        {/* Scrollable Track */}
        <div
          ref={rowRef}
          onScroll={handleScroll}
          className="flex space-x-4 overflow-x-auto no-scrollbar scroll-smooth py-4 px-1"
          tabIndex={0}
          role="region"
          aria-label={`${title} movie carousel`}
        >
          {movies.map((movie) => (
            <MovieCard
              key={`${title}-${movie.id}`}
              movie={movie}
              onSelect={onSelectMovie}
              onPlayTrailer={onPlayTrailer}
            />
          ))}
        </div>

        {/* Right Arrow Button (Desktop) */}
        {showRightArrow && (
          <button
            onClick={() => scroll("right")}
            className="hidden md:flex absolute -right-4 top-1/2 -translate-y-1/2 z-30 w-10 h-20 items-center justify-center bg-black/70 hover:bg-black/95 text-white rounded-l-lg border-y border-l border-neutral-700/60 shadow-xl transition-all focus:outline-none"
            aria-label={`Scroll ${title} right`}
          >
            <ChevronRight className="w-6 h-6" />
          </button>
        )}
      </div>
    </section>
  );
}
