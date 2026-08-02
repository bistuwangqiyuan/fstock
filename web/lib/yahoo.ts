import type { Bar } from "./sentiment";

export type ChartPoint = {
  time: number;
  close: number;
  volume: number;
};

export type QuoteSnapshot = {
  symbol: string;
  currency: string;
  regularMarketPrice: number | null;
  previousClose: number | null;
  exchangeName: string | null;
  points: ChartPoint[];
  bars: Bar[];
  fetchedAt: string;
  source: "yahoo-chart-v8";
  delayedNote: string;
};

type YahooChartResponse = {
  chart?: {
    result?: Array<{
      meta?: {
        currency?: string;
        regularMarketPrice?: number;
        previousClose?: number;
        chartPreviousClose?: number;
        exchangeName?: string;
        symbol?: string;
      };
      timestamp?: number[];
      indicators?: {
        quote?: Array<{
          close?: Array<number | null>;
          volume?: Array<number | null>;
        }>;
      };
    }>;
    error?: { description?: string };
  };
};

const UA =
  "Mozilla/5.0 (compatible; FStockBot/1.0; +https://github.com/bistuwangqiyuan/fstock)";

export async function fetchYahooChart(
  symbol: string,
  range = "3mo",
  interval = "1d",
): Promise<QuoteSnapshot> {
  const url = new URL(
    `https://query1.finance.yahoo.com/v8/finance/chart/${encodeURIComponent(symbol)}`,
  );
  url.searchParams.set("range", range);
  url.searchParams.set("interval", interval);

  const res = await fetch(url.toString(), {
    headers: { "User-Agent": UA, Accept: "application/json" },
    next: { revalidate: 3600, tags: [`yahoo:${symbol}`] },
  });

  if (!res.ok) {
    throw new Error(`Yahoo chart HTTP ${res.status} for ${symbol}`);
  }

  const data = (await res.json()) as YahooChartResponse;
  const result = data.chart?.result?.[0];
  if (!result?.timestamp?.length) {
    throw new Error(
      data.chart?.error?.description || `No chart data for ${symbol}`,
    );
  }

  const closes = result.indicators?.quote?.[0]?.close ?? [];
  const volumes = result.indicators?.quote?.[0]?.volume ?? [];
  const points: ChartPoint[] = [];
  const bars: Bar[] = [];

  for (let i = 0; i < result.timestamp.length; i++) {
    const c = closes[i];
    const v = volumes[i];
    if (c == null || !Number.isFinite(c)) continue;
    const vol = v != null && Number.isFinite(v) ? v : 0;
    points.push({ time: result.timestamp[i], close: c, volume: vol });
    bars.push({ close: c, volume: vol });
  }

  const meta = result.meta ?? {};
  return {
    symbol: meta.symbol || symbol,
    currency: meta.currency || "USD",
    regularMarketPrice: meta.regularMarketPrice ?? points.at(-1)?.close ?? null,
    previousClose:
      meta.previousClose ?? meta.chartPreviousClose ?? points.at(-2)?.close ?? null,
    exchangeName: meta.exchangeName ?? null,
    points,
    bars,
    fetchedAt: new Date().toISOString(),
    source: "yahoo-chart-v8",
    delayedNote:
      "Delayed/unofficial public chart data via Yahoo Finance chart endpoint. Not a real-time feed. Not affiliated with Yahoo.",
  };
}
