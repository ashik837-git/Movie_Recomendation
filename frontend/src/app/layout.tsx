import type { Metadata } from "next";
import "./globals.css";
import Navbar from "@/components/Navbar";

export const metadata: Metadata = {
  title: "CinePulse | Algorithmic Movie Discovery & Recommendations",
  description:
    "An advanced NLP content-based movie discovery platform featuring weighted metadata soups and truthful explanations.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-[#141414] text-white min-h-screen flex flex-col selection:bg-[#E50914] selection:text-white">
        <Navbar />
        <main className="flex-1">{children}</main>
        <footer className="bg-neutral-950 border-t border-neutral-900 py-10 px-4 sm:px-6 lg:px-8 mt-20 text-neutral-500 text-xs text-center space-y-3">
          <div className="flex items-center justify-center space-x-2 text-white font-bold">
            <span className="text-[#E50914]">◈</span>
            <span>CINEPULSE DISCOVERY ENGINE</span>
          </div>
          <p className="max-w-md mx-auto">
            Algorithmic natural language processing recommendation platform. Built with Next.js, FastAPI, and scikit-learn.
          </p>
          <p>© {new Date().getFullYear()} CinePulse. All rights reserved. Film metadata courtesy of TMDB API.</p>
        </footer>
      </body>
    </html>
  );
}
