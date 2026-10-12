import { Movie, PaginatedMovies, GenreItem, SubscriptionPlan } from "@/types";

const getBaseUrl = (): string => {
  if (process.env.NEXT_PUBLIC_API_BASE_URL) {
    return process.env.NEXT_PUBLIC_API_BASE_URL.replace(/\/$/, "");
  }
  if (typeof window !== "undefined") {
    return "/api/v1";
  }
  return "http://127.0.0.1:8000/api/v1";
};

class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = "ApiError";
  }
}

async function request<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const cleanEndpoint = endpoint.startsWith("/") ? endpoint : `/${endpoint}`;
  const url = `${getBaseUrl()}${cleanEndpoint}`;
  try {
    const res = await fetch(url, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options?.headers,
      },
    });

    if (!res.ok) {
      let errorMsg = `API request failed with status ${res.status}`;
      try {
        const errorData = await res.json();
        if (errorData.detail) errorMsg = errorData.detail;
      } catch {
        // ignore json parse error
      }
      throw new ApiError(res.status, errorMsg);
    }

    return await res.json();
  } catch (err) {
    if (err instanceof ApiError) throw err;
    throw new ApiError(500, `Network connection error: Unable to reach CinePulse backend at ${API_BASE_URL}`);
  }
}

export const api = {
  // Catalog & Movies
  getFeaturedMovie: async (): Promise<Movie> => {
    return request<Movie>("/featured");
  },

  getPopularMovies: async (limit = 20, genre?: string): Promise<Movie[]> => {
    const params = new URLSearchParams({ limit: limit.toString() });
    if (genre) params.append("genre", genre);
    return request<Movie[]>(`/popular?${params.toString()}`);
  },

  getMovies: async (page = 1, pageSize = 20, genre?: string): Promise<PaginatedMovies> => {
    const params = new URLSearchParams({ page: page.toString(), page_size: pageSize.toString() });
    if (genre) params.append("genre", genre);
    return request<PaginatedMovies>(`/movies?${params.toString()}`);
  },

  getMovieById: async (id: number): Promise<Movie> => {
    return request<Movie>(`/movies/${id}`);
  },

  getSimilarMovies: async (id: number, limit = 10): Promise<Movie[]> => {
    return request<Movie[]>(`/movies/${id}/similar?limit=${limit}`);
  },

  searchMovies: async (query: string, genre?: string, limit = 24): Promise<Movie[]> => {
    const params = new URLSearchParams({ q: query, limit: limit.toString() });
    if (genre) params.append("genre", genre);
    return request<Movie[]>(`/search?${params.toString()}`);
  },

  getGenres: async (): Promise<GenreItem[]> => {
    return request<GenreItem[]>("/genres");
  },

  // Subscriptions & Plans
  getPlans: async (): Promise<SubscriptionPlan[]> => {
    return request<SubscriptionPlan[]>("/payments/plans");
  },

  createCheckoutSession: async (planId: string, successUrl: string, cancelUrl: string, token?: string) => {
    return request<{ checkout_url: string; session_id: string }>("/payments/create-checkout-session", {
      method: "POST",
      headers: token ? { Authorization: `Bearer ${token}` } : {},
      body: JSON.stringify({ plan_id: planId, success_url: successUrl, cancel_url: cancelUrl }),
    });
  },

  // User Watchlist & History
  getWatchlist: async (token: string): Promise<Movie[]> => {
    return request<Movie[]>("/user/watchlist", {
      headers: { Authorization: `Bearer ${token}` },
    });
  },

  addToWatchlist: async (movieId: number, token: string): Promise<{ success: boolean }> => {
    return request<{ success: boolean }>("/user/watchlist", {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
      body: JSON.stringify({ movie_id: movieId }),
    });
  },

  removeFromWatchlist: async (movieId: number, token: string): Promise<{ success: boolean }> => {
    return request<{ success: boolean }>(`/user/watchlist/${movieId}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    });
  },

  recordHistory: async (movieId: number, token?: string): Promise<void> => {
    if (!token) return;
    try {
      await request<void>("/user/history", {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
        body: JSON.stringify({ movie_id: movieId }),
      });
    } catch {
      // Non-blocking history record
    }
  },
};
