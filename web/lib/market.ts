import { computePulse, type PulseBreakdown } from "./sentiment";
import { SEED_SYMBOLS, SYMBOL_NAMES } from "./symbols";
import { fetchYahooChart, type QuoteSnapshot } from "./yahoo";
import seed from "@/data/snapshots/market.json";

export type SymbolCard = {
  symbol: string;
  name: string;
  price: number | null;
  changePct: number | null;
  pulse: number;
  breakdown: PulseBreakdown;
  currency: string;
  spark: number[];
  headlines: string[];
  fetchedAt: string;
  fromFallback: boolean;
};

export type MarketBundle = {
  updatedAt: string;
  symbols: SymbolCard[];
};

type SeedFile = {
  updatedAt: string;
  symbols: Array<{
    symbol: string;
    name: string;
    price: number | null;
    changePct: number | null;
    pulse: number;
    breakdown: PulseBreakdown;
    currency: string;
    spark: number[];
    headlines: string[];
    fetchedAt: string;
  }>;
};

function changePct(price: number | null, prev: number | null): number | null {
  if (price == null || prev == null || prev === 0) return null;
  return Math.round(((price / prev - 1) * 10000)) / 100;
}

function cardFromQuote(
  quote: QuoteSnapshot,
  headlines: string[] = [],
  fromFallback = false,
): SymbolCard {
  const breakdown = computePulse(quote.bars, headlines);
  const spark = quote.points.slice(-30).map((p) => p.close);
  return {
    symbol: quote.symbol,
    name: SYMBOL_NAMES[quote.symbol] || quote.symbol,
    price: quote.regularMarketPrice,
    changePct: changePct(quote.regularMarketPrice, quote.previousClose),
    pulse: breakdown.pulse,
    breakdown,
    currency: quote.currency,
    spark,
    headlines,
    fetchedAt: quote.fetchedAt,
    fromFallback,
  };
}

export function loadSeedMarket(): MarketBundle {
  const data = seed as SeedFile;
  return {
    updatedAt: data.updatedAt,
    symbols: data.symbols.map((s) => ({ ...s, fromFallback: true })),
  };
}

export async function fetchLiveMarket(
  tickers: readonly string[] = SEED_SYMBOLS,
): Promise<MarketBundle> {
  const results = await Promise.allSettled(
    tickers.map((t) => fetchYahooChart(t)),
  );
  const symbols: SymbolCard[] = [];
  for (let i = 0; i < tickers.length; i++) {
    const r = results[i];
    if (r.status === "fulfilled") {
      symbols.push(cardFromQuote(r.value));
    } else {
      const fallback = loadSeedMarket().symbols.find(
        (s) => s.symbol === tickers[i],
      );
      if (fallback) symbols.push(fallback);
    }
  }
  return {
    updatedAt: new Date().toISOString(),
    symbols,
  };
}

export async function getMarketBundle(): Promise<MarketBundle> {
  try {
    const live = await fetchLiveMarket();
    if (live.symbols.length > 0) return live;
  } catch {
    // fall through
  }
  return loadSeedMarket();
}

export async function getSymbolCard(ticker: string): Promise<SymbolCard | null> {
  try {
    const quote = await fetchYahooChart(ticker);
    return cardFromQuote(quote);
  } catch {
    const seedCard = loadSeedMarket().symbols.find((s) => s.symbol === ticker);
    return seedCard ?? null;
  }
}
