-- ==============================================================================
-- CinePulse Initial Database Schema & RLS Policies
-- PostgreSQL 15+ compatible for Supabase
-- ==============================================================================

-- 1. Profiles Table (Extends Supabase auth.users)
CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT,
    display_name TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

-- Trigger to automatically create a profile row when a new user signs up
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS trigger AS $$
BEGIN
    INSERT INTO public.profiles (id, email, display_name)
    VALUES (new.id, new.email, COALESCE(new.raw_user_meta_data->>'full_name', split_part(new.email, '@', 1)));
    RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE PROCEDURE public.handle_new_user();

-- 2. Watchlist (My List)
CREATE TABLE IF NOT EXISTS public.watchlist (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    movie_id INT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),
    CONSTRAINT unique_user_movie UNIQUE (user_id, movie_id)
);

CREATE INDEX IF NOT EXISTS idx_watchlist_user_id ON public.watchlist(user_id);

-- 3. Recommendation & Viewing History
CREATE TABLE IF NOT EXISTS public.recommendation_history (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    movie_id INT NOT NULL,
    viewed_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

CREATE INDEX IF NOT EXISTS idx_history_user_id ON public.recommendation_history(user_id);
CREATE INDEX IF NOT EXISTS idx_history_viewed_at ON public.recommendation_history(viewed_at DESC);

-- 4. User Preferences
CREATE TABLE IF NOT EXISTS public.user_preferences (
    user_id UUID PRIMARY KEY REFERENCES public.profiles(id) ON DELETE CASCADE,
    favorite_genres TEXT[] NOT NULL DEFAULT '{}',
    updated_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

-- 5. Subscriptions Table
CREATE TABLE IF NOT EXISTS public.subscriptions (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    plan_id TEXT NOT NULL DEFAULT 'free',
    status TEXT NOT NULL DEFAULT 'active', -- 'active', 'canceled', 'past_due'
    provider TEXT NOT NULL DEFAULT 'sandbox',
    provider_subscription_id TEXT,
    current_period_end TIMESTAMPTZ,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),
    CONSTRAINT unique_user_subscription UNIQUE (user_id)
);

CREATE INDEX IF NOT EXISTS idx_subscriptions_user_id ON public.subscriptions(user_id);

-- 6. Payment Events (Webhook Idempotency Log)
CREATE TABLE IF NOT EXISTS public.payment_events (
    event_id TEXT PRIMARY KEY,
    provider TEXT NOT NULL,
    payload JSONB NOT NULL,
    processed_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

-- ==============================================================================
-- Row-Level Security (RLS) Enablement & Policies
-- ==============================================================================

ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.watchlist ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.recommendation_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_preferences ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.subscriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.payment_events ENABLE ROW LEVEL SECURITY;

-- Profiles: Users can view and edit their own profile
CREATE POLICY "Users can view own profile" 
    ON public.profiles FOR SELECT 
    USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" 
    ON public.profiles FOR UPDATE 
    USING (auth.uid() = id);

-- Watchlist: Strict User Isolation
CREATE POLICY "Users can view own watchlist" 
    ON public.watchlist FOR SELECT 
    USING (auth.uid() = user_id);

CREATE POLICY "Users can add to own watchlist" 
    ON public.watchlist FOR INSERT 
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can remove from own watchlist" 
    ON public.watchlist FOR DELETE 
    USING (auth.uid() = user_id);

-- Recommendation History: Strict User Isolation
CREATE POLICY "Users can view own history" 
    ON public.recommendation_history FOR SELECT 
    USING (auth.uid() = user_id);

CREATE POLICY "Users can record own history" 
    ON public.recommendation_history FOR INSERT 
    WITH CHECK (auth.uid() = user_id);

-- User Preferences: Strict User Isolation
CREATE POLICY "Users can view own preferences" 
    ON public.user_preferences FOR SELECT 
    USING (auth.uid() = user_id);

CREATE POLICY "Users can upsert own preferences" 
    ON public.user_preferences FOR ALL 
    USING (auth.uid() = user_id);

-- Subscriptions: Read-only for authenticated user; writes ONLY via server service role
CREATE POLICY "Users can view own subscription" 
    ON public.subscriptions FOR SELECT 
    USING (auth.uid() = user_id);

-- Service role bypasses RLS automatically in Supabase, preventing client-side subscription manipulation.

-- Safe seed script for developer verification
INSERT INTO public.payment_events (event_id, provider, payload)
VALUES ('evt_init_sandbox_seed', 'sandbox', '{"status": "initialized", "test": true}')
ON CONFLICT (event_id) DO NOTHING;
