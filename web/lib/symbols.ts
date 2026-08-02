export const SEED_SYMBOLS = [
  "F",
  "SPY",
  "QQQ",
  "AAPL",
  "MSFT",
  "NVDA",
  "TSLA",
  "AMZN",
  "META",
  "GOOGL",
] as const;

export type SeedSymbol = (typeof SEED_SYMBOLS)[number];

export const SYMBOL_NAMES: Record<string, string> = {
  F: "Ford Motor Company",
  SPY: "SPDR S&P 500 ETF",
  QQQ: "Invesco QQQ Trust",
  AAPL: "Apple Inc.",
  MSFT: "Microsoft Corporation",
  NVDA: "NVIDIA Corporation",
  TSLA: "Tesla, Inc.",
  AMZN: "Amazon.com, Inc.",
  META: "Meta Platforms, Inc.",
  GOOGL: "Alphabet Inc.",
};

export function normalizeTicker(raw: string): string {
  return raw.trim().toUpperCase().replace(/[^A-Z0-9.\-]/g, "");
}

export function isSeedSymbol(ticker: string): boolean {
  return (SEED_SYMBOLS as readonly string[]).includes(ticker);
}
