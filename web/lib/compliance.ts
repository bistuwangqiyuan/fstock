/** Compliance copy and banned-phrase guardrails. Not legal advice. */

export const DISCLAIMER_SHORT =
  "F Stock provides public market information and investor education only. It is not investment advice, a recommendation to buy or sell any security, or a substitute for professional counsel.";

export const DISCLAIMER_LONG = `${DISCLAIMER_SHORT}

Pulse scores are reproducible heuristics based on delayed public price/volume data and optional headline polarity. They are not forecasts, ratings, or instructions to trade a security.

Securities laws in many jurisdictions regulate personalized investment advice. This product intentionally stays within general-circulation information and education. You alone decide whether and how to use public information.`;

/** Phrases that must never appear in product UI or educational content. */
export const BANNED_PHRASES = [
  "strong buy",
  "strong sell",
  "buy now",
  "sell now",
  "guaranteed returns",
  "guaranteed profit",
  "guaranteed return",
  "can't lose",
  "cannot lose",
  "risk-free returns",
  "risk free returns",
  "hot tip",
  "sure thing",
  "get rich",
  "double your money",
  "personalized recommendation",
  "you should buy",
  "you should sell",
  "we recommend buying",
  "we recommend selling",
] as const;

export function findBannedPhrases(text: string): string[] {
  const lower = text.toLowerCase();
  return BANNED_PHRASES.filter((p) => lower.includes(p));
}

export function assertCompliant(text: string, context: string): void {
  const hits = findBannedPhrases(text);
  if (hits.length > 0) {
    throw new Error(`[compliance] Banned phrases in ${context}: ${hits.join(", ")}`);
  }
}
