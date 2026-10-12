"use client";

import React, { useState, useEffect } from "react";
import { Check, Sparkles, Shield, AlertCircle, ArrowRight, Zap, Info } from "lucide-react";
import { SubscriptionPlan } from "@/types";
import { api } from "@/lib/api";

export default function PricingPage() {
  const [plans, setPlans] = useState<SubscriptionPlan[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [checkoutLoading, setCheckoutLoading] = useState<string | null>(null);
  const [feedback, setFeedback] = useState<{ type: "success" | "canceled"; message: string } | null>(null);

  useEffect(() => {
    // Check URL parameters for simulated checkout returns
    if (typeof window !== "undefined") {
      const urlParams = new URLSearchParams(window.location.search);
      const status = urlParams.get("status");
      const plan = urlParams.get("plan");
      if (status === "success" || urlParams.get("session_id")) {
        setFeedback({
          type: "success",
          message: `Your ${plan ? plan.toUpperCase() : "Premium"} subscription checkout was completed successfully in test sandbox mode!`,
        });
      } else if (status === "canceled") {
        setFeedback({
          type: "canceled",
          message: "Checkout was canceled. No charges were simulated.",
        });
      }
    }

    api
      .getPlans()
      .then((data) => {
        setPlans(data);
        setIsLoading(false);
      })
      .catch(() => {
        setIsLoading(false);
      });
  }, []);

  const handleSubscribe = async (planId: string) => {
    if (planId === "free") {
      setFeedback({
        type: "success",
        message: "You are currently enjoying the Free Explorer tier with 25 recommendation queries daily.",
      });
      return;
    }

    setCheckoutLoading(planId);
    try {
      const currentUrl = window.location.origin + window.location.pathname;
      const res = await api.createCheckoutSession(
        planId,
        `${currentUrl}?status=success&plan=${planId}`,
        `${currentUrl}?status=canceled`
      );
      if (res.checkout_url) {
        window.location.href = res.checkout_url;
      }
    } catch (err: any) {
      setFeedback({
        type: "canceled",
        message: err.message || "Failed to create checkout session.",
      });
    } finally {
      setCheckoutLoading(null);
    }
  };

  return (
    <div className="pt-24 pb-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-12">
      {/* Title & Headline */}
      <div className="text-center max-w-3xl mx-auto space-y-3">
        <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-[#E50914]/15 border border-[#E50914]/30 text-[#E50914] text-xs font-bold uppercase tracking-wider">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Flexible Subscription Plans</span>
        </div>
        <h1 className="text-3xl sm:text-5xl font-black text-white tracking-tight">
          Supercharge Your Film Discovery
        </h1>
        <p className="text-neutral-400 text-sm sm:text-base max-w-xl mx-auto">
          Explore our algorithmic recommendation engine with zero friction. Upgrade for unlimited queries and high-priority ranking.
        </p>
      </div>

      {/* Status Notice if returned from checkout */}
      {feedback && (
        <div
          className={`max-w-2xl mx-auto p-4 rounded-xl border flex items-center space-x-3 text-sm ${
            feedback.type === "success"
              ? "bg-emerald-950/60 border-emerald-600/40 text-emerald-200"
              : "bg-amber-950/60 border-amber-600/40 text-amber-200"
          }`}
        >
          <Info className="w-5 h-5 flex-shrink-0" />
          <span>{feedback.message}</span>
        </div>
      )}

      {/* Bangladesh & Global Payment Compliance Banner */}
      <div className="max-w-3xl mx-auto bg-neutral-900/80 border border-neutral-800 rounded-xl p-4 flex items-start space-x-3 text-xs text-neutral-400">
        <Shield className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" />
        <div className="space-y-1">
          <p className="font-semibold text-neutral-300">Payment Provider Architecture Note:</p>
          <p>
            Operating in test sandbox mode. CinePulse implements a provider-agnostic PaymentProvider interface compatible with Stripe test mode, SSLCommerz (Bangladesh local payment gateway), and Merchant-of-Record providers. No real cards or transactions are charged.
          </p>
        </div>
      </div>

      {/* Pricing Cards Grid */}
      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 animate-pulse">
          {Array.from({ length: 3 }).map((_, i) => (
            <div key={i} className="h-96 rounded-2xl bg-neutral-900 border border-neutral-800" />
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 items-stretch">
          {plans.map((plan) => {
            const isFeatured = plan.id === "premium";
            return (
              <div
                key={plan.id}
                className={`relative rounded-2xl p-6 sm:p-8 flex flex-col justify-between border transition-all ${
                  isFeatured
                    ? "bg-gradient-to-b from-neutral-900 via-neutral-900 to-black border-[#E50914] shadow-2xl shadow-[#E50914]/20 scale-105 z-10"
                    : "bg-neutral-900/60 border-neutral-800 hover:border-neutral-700"
                }`}
              >
                {/* Badge */}
                {plan.badge && (
                  <div className="absolute -top-3.5 left-1/2 -translate-x-1/2 px-3 py-1 rounded-full bg-[#E50914] text-white text-[11px] font-black uppercase tracking-wider shadow-md">
                    {plan.badge}
                  </div>
                )}

                <div className="space-y-6">
                  <div>
                    <h3 className="text-xl font-bold text-white">{plan.name}</h3>
                    <p className="text-xs text-neutral-400 mt-1">{plan.recommendation_limit}</p>
                  </div>

                  <div className="flex items-baseline space-x-1">
                    <span className="text-4xl font-black text-white">${plan.price_monthly.toFixed(2)}</span>
                    <span className="text-xs text-neutral-400 font-medium">/ month</span>
                  </div>

                  {/* Feature Checklist */}
                  <ul className="space-y-3 pt-2">
                    {plan.features.map((feat, idx) => (
                      <li key={idx} className="flex items-start space-x-2.5 text-xs text-neutral-300">
                        <Check className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" />
                        <span>{feat}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="pt-8">
                  <button
                    onClick={() => handleSubscribe(plan.id)}
                    disabled={checkoutLoading !== null}
                    className={`w-full py-3 px-4 rounded-xl font-bold text-sm transition-all focus:outline-none flex items-center justify-center space-x-2 ${
                      isFeatured
                        ? "bg-[#E50914] hover:bg-[#F40612] text-white shadow-lg shadow-[#E50914]/30"
                        : "bg-white/10 hover:bg-white/20 text-white"
                    } ${checkoutLoading === plan.id ? "opacity-75 cursor-wait" : ""}`}
                  >
                    {checkoutLoading === plan.id ? (
                      <span>Initiating Checkout...</span>
                    ) : (
                      <>
                        <span>{plan.price_monthly === 0 ? "Current Plan" : "Choose Tier"}</span>
                        <ArrowRight className="w-4 h-4" />
                      </>
                    )}
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
