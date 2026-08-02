/**
 * Reproducible Market Pulse heuristics.
 *
 * Pulse = clip(50 + 15*z_ret + 10*z_vol + 10*s_news, 0, 100)
 *
 * - z_ret: 5-day return / 60-day daily-return stdev
 * - z_vol: clip(today_volume / 20-day avg volume - 1, -3, 3)
 * - s_news: simple headline polarity in [-1, 1] (0 if none)
 *
 * This is an information heuristic, NOT a forecast or investment recommendation.
 */

export type Bar = {
  close: number;
  volume: number;
};

export type PulseBreakdown = {
  zRet: number;
  zVol: number;
  sNews: number;
  pulse: number;
};

export function clip(x: number, lo: number, hi: number): number {
  return Math.min(hi, Math.max(lo, x));
}

export function stdev(values: number[]): number {
  if (values.length < 2) return 0;
  const mean = values.reduce((a, b) => a + b, 0) / values.length;
  const variance =
    values.reduce((acc, v) => acc + (v - mean) ** 2, 0) / (values.length - 1);
  return Math.sqrt(variance);
}

export function fiveDayReturn(closes: number[]): number {
  if (closes.length < 6) return 0;
  const last = closes[closes.length - 1];
  const prev = closes[closes.length - 6];
  if (prev <= 0) return 0;
  return last / prev - 1;
}

export function dailyReturns(closes: number[]): number[] {
  const out: number[] = [];
  for (let i = 1; i < closes.length; i++) {
    const prev = closes[i - 1];
    if (prev > 0) out.push(closes[i] / prev - 1);
  }
  return out;
}

export function zRetFromCloses(closes: number[]): number {
  const ret5 = fiveDayReturn(closes);
  const rets = dailyReturns(closes);
  const window = rets.slice(-60);
  const s = stdev(window);
  if (s <= 1e-12) return 0;
  return ret5 / s;
}

export function zVolFromVolumes(volumes: number[]): number {
  if (volumes.length < 21) return 0;
  const today = volumes[volumes.length - 1];
  const avg20 =
    volumes.slice(-21, -1).reduce((a, b) => a + b, 0) / 20;
  if (avg20 <= 0) return 0;
  return clip(today / avg20 - 1, -3, 3);
}

/** Tiny English finance polarity lexicon for headlines. */
const POSITIVE = [
  "surge",
  "soar",
  "rally",
  "beat",
  "growth",
  "record",
  "profit",
  "upgrade",
  "bull",
  "gain",
  "rise",
  "up",
];
const NEGATIVE = [
  "plunge",
  "crash",
  "fall",
  "miss",
  "loss",
  "downgrade",
  "bear",
  "cut",
  "drop",
  "decline",
  "lawsuit",
  "fraud",
];

export function headlinePolarity(headlines: string[]): number {
  if (!headlines.length) return 0;
  let score = 0;
  for (const h of headlines) {
    const t = h.toLowerCase();
    for (const w of POSITIVE) if (t.includes(w)) score += 1;
    for (const w of NEGATIVE) if (t.includes(w)) score -= 1;
  }
  const norm = score / (headlines.length * 2);
  return clip(norm, -1, 1);
}

export function computePulse(
  bars: Bar[],
  headlines: string[] = [],
): PulseBreakdown {
  const closes = bars.map((b) => b.close);
  const volumes = bars.map((b) => b.volume);
  const zRet = zRetFromCloses(closes);
  const zVol = zVolFromVolumes(volumes);
  const sNews = headlinePolarity(headlines);
  const pulse = clip(50 + 15 * zRet + 10 * zVol + 10 * sNews, 0, 100);
  return {
    zRet: round4(zRet),
    zVol: round4(zVol),
    sNews: round4(sNews),
    pulse: round2(pulse),
  };
}

function round4(x: number): number {
  return Math.round(x * 10000) / 10000;
}

function round2(x: number): number {
  return Math.round(x * 100) / 100;
}
