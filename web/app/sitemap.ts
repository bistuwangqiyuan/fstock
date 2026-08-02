import type { MetadataRoute } from "next";
import { LEARN_ARTICLES } from "@/content/learn";
import { SEED_SYMBOLS } from "@/lib/symbols";

export default function sitemap(): MetadataRoute.Sitemap {
  const base = process.env.NEXT_PUBLIC_SITE_URL || "https://fstock.vercel.app";
  const staticRoutes = [
    "",
    "/methodology",
    "/learn",
    "/alerts",
    "/disclaimer",
    "/privacy",
  ].map((path) => ({
    url: `${base}${path}`,
    lastModified: new Date(),
    changeFrequency: "weekly" as const,
    priority: path === "" ? 1 : 0.7,
  }));

  const symbols = SEED_SYMBOLS.map((ticker) => ({
    url: `${base}/symbol/${ticker}`,
    lastModified: new Date(),
    changeFrequency: "daily" as const,
    priority: 0.8,
  }));

  const learn = LEARN_ARTICLES.map((a) => ({
    url: `${base}/learn/${a.slug}`,
    lastModified: new Date(a.date),
    changeFrequency: "monthly" as const,
    priority: 0.6,
  }));

  return [...staticRoutes, ...symbols, ...learn];
}
