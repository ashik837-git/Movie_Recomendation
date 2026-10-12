export interface Movie {
  id: number;
  title: string;
  overview: string;
  tagline: string;
  release_date: string;
  release_year: string;
  runtime: number;
  popularity: number;
  vote_average: number;
  vote_count: number;
  weighted_rating: number;
  genres: string[];
  keywords: string[];
  cast: string[];
  director: string | null;
  similarity_score?: number;
  recommendation_explanation?: RecommendationExplanation;
  poster_url?: string | null;
  backdrop_url?: string | null;
  trailer_url?: string | null;
}

export interface RecommendationExplanation {
  same_director: boolean;
  director: string | null;
  shared_cast: string[];
  shared_genres: string[];
  shared_keywords: string[];
  summary: string;
}

export interface PaginatedMovies {
  items: Movie[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface GenreItem {
  name: string;
  count: number;
}

export interface SubscriptionPlan {
  id: string;
  name: string;
  price_monthly: number;
  currency: string;
  recommendation_limit: string;
  features: string[];
  badge?: string;
}

export interface UserProfile {
  id: string;
  email: string;
  display_name: string;
}

export interface WatchlistEntry {
  movie_id: number;
  movie: Movie;
  added_at: string;
}
