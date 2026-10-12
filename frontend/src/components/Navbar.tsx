"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Search, Film, Bookmark, Sparkles, User, Menu, X, ShieldCheck } from "lucide-react";

export default function Navbar() {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const pathname = usePathname();

  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 30) {
        setIsScrolled(true);
      } else {
        setIsScrolled(false);
      }
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const navLinks = [
    { name: "Home", href: "/" },
    { name: "Movies", href: "/movies" },
    { name: "Search", href: "/search" },
    { name: "My List", href: "/my-list" },
    { name: "Pricing", href: "/pricing" },
  ];

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-40 transition-all duration-300 ${
        isScrolled
          ? "bg-[#141414]/95 backdrop-blur-md shadow-lg border-b border-white/5 py-3"
          : "bg-gradient-to-b from-black/80 via-black/40 to-transparent py-5"
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between">
        {/* Brand Logo & Wordmark */}
        <div className="flex items-center space-x-8">
          <Link
            href="/"
            className="flex items-center space-x-2 text-white font-black text-2xl tracking-tighter group focus:outline-none focus:ring-2 focus:ring-[#E50914] rounded-md px-1"
            aria-label="CinePulse Home"
          >
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-[#E50914] to-[#990000] flex items-center justify-center shadow-lg shadow-[#E50914]/30 group-hover:scale-105 transition-transform">
              <span className="text-white font-black text-lg">◈</span>
            </div>
            <span className="bg-gradient-to-r from-white via-neutral-200 to-neutral-400 bg-clip-text text-transparent group-hover:from-white group-hover:to-[#E50914] transition-colors">
              CINE<span className="text-[#E50914]">PULSE</span>
            </span>
          </Link>

          {/* Desktop Navigation Links */}
          <nav className="hidden md:flex items-center space-x-6" aria-label="Main Navigation">
            {navLinks.map((link) => {
              const isActive = pathname === link.href;
              return (
                <Link
                  key={link.name}
                  href={link.href}
                  className={`text-sm font-medium transition-colors hover:text-white ${
                    isActive ? "text-white font-semibold" : "text-neutral-400"
                  }`}
                >
                  {link.name}
                </Link>
              );
            })}
          </nav>
        </div>

        {/* Right Action Icons & Profile */}
        <div className="hidden md:flex items-center space-x-5">
          <Link
            href="/search"
            className="text-neutral-300 hover:text-white p-2 rounded-full hover:bg-white/10 transition-colors"
            aria-label="Search Catalog"
          >
            <Search className="w-5 h-5" />
          </Link>

          <Link
            href="/my-list"
            className="text-neutral-300 hover:text-white p-2 rounded-full hover:bg-white/10 transition-colors"
            aria-label="Saved Watchlist"
          >
            <Bookmark className="w-5 h-5" />
          </Link>

          <Link
            href="/pricing"
            className="flex items-center space-x-1.5 text-xs font-semibold uppercase tracking-wider text-neutral-200 hover:text-white bg-white/10 hover:bg-[#E50914] px-3 py-1.5 rounded-full transition-all duration-200"
          >
            <Sparkles className="w-3.5 h-3.5 text-amber-400" />
            <span>Upgrade</span>
          </Link>

          {/* User Profile Pill */}
          <Link
            href="/pricing"
            className="flex items-center space-x-2 pl-2 text-neutral-400 hover:text-white transition-colors"
            aria-label="Account Settings"
          >
            <div className="w-8 h-8 rounded-full bg-neutral-800 border border-neutral-700 flex items-center justify-center">
              <User className="w-4 h-4 text-neutral-300" />
            </div>
          </Link>
        </div>

        {/* Mobile Hamburger Toggle */}
        <div className="md:hidden flex items-center space-x-3">
          <Link
            href="/search"
            className="text-neutral-300 hover:text-white p-1"
            aria-label="Search"
          >
            <Search className="w-5 h-5" />
          </Link>
          <button
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            className="text-neutral-300 hover:text-white p-1 focus:outline-none"
            aria-label="Toggle navigation menu"
            aria-expanded={isMobileMenuOpen}
          >
            {isMobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </div>

      {/* Mobile Drawer */}
      {isMobileMenuOpen && (
        <div className="md:hidden bg-[#141414] border-b border-neutral-800 px-4 pt-3 pb-6 space-y-3 animate-fade-in">
          {navLinks.map((link) => (
            <Link
              key={link.name}
              href={link.href}
              onClick={() => setIsMobileMenuOpen(false)}
              className="block py-2 text-base font-medium text-neutral-300 hover:text-white border-b border-neutral-800/50"
            >
              {link.name}
            </Link>
          ))}
          <div className="pt-2">
            <Link
              href="/pricing"
              onClick={() => setIsMobileMenuOpen(false)}
              className="flex items-center justify-center w-full py-2.5 rounded-lg bg-[#E50914] text-white font-semibold text-sm"
            >
              <Sparkles className="w-4 h-4 mr-2" /> Upgrade to Premium
            </Link>
          </div>
        </div>
      )}
    </header>
  );
}
