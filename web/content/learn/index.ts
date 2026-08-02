import { assertCompliant } from "@/lib/compliance";

export type LearnArticle = {
  slug: string;
  title: string;
  description: string;
  date: string;
  body: string[];
};

export const LEARN_ARTICLES: LearnArticle[] = [
  {
    slug: "what-is-f-stock",
    title: "What people mean by “F stock”",
    description:
      "A plain-language explainer of the Ford ticker and how to read public quotes without treating them as advice.",
    date: "2026-08-02",
    body: [
      "Search interest around “F stock” often points to Ford Motor Company (NYSE: F) and, more broadly, to retail curiosity about individual equity tickers.",
      "Public quote pages show delayed prices, volume, and simple historical context. They do not tell you whether a security is suitable for your situation.",
      "F Stock focuses on transparent information: delayed market data, a reproducible Market Pulse heuristic, and educational notes. We do not tell you which securities to trade.",
      "If you are evaluating any security, consider diversified sources, risk tolerance, time horizon, and licensed professionals when needed.",
    ],
  },
  {
    slug: "market-sentiment-basics",
    title: "Market sentiment basics (without the hype)",
    description:
      "How information products describe mood using price, volume, and headlines—and why that is not a crystal ball.",
    date: "2026-08-02",
    body: [
      "“Sentiment” in public dashboards usually means a compressed summary of recent price momentum, unusual volume, and sometimes news tone.",
      "Our Market Pulse score combines those ingredients with a published formula so anyone can recalculate it. A high or low Pulse is not a prediction of future returns.",
      "Markets can stay “overheated” or “depressed” longer than any heuristic expects. Treat scores as conversation starters about public data, not as trading instructions.",
      "Education works best when methods are open, limitations are stated, and users keep final decisions.",
    ],
  },
  {
    slug: "not-investment-advice",
    title: "Why this site is not investment advice",
    description:
      "A clear boundary between general information and regulated personalized advice.",
    date: "2026-08-02",
    body: [
      "In the United States, the Investment Advisers Act of 1940 generally covers compensated advice about the advisability of investing in securities. Courts have recognized a publisher’s exclusion for bona fide publications of general and regular circulation that are impersonal.",
      "F Stock is designed as a general-circulation information and education site: no personalized portfolios, no “you should trade X” messages, and no guaranteed-outcome claims.",
      "That boundary is intentional. It protects users from mistaking software for a fiduciary, and it keeps an unmanned operation inside a compliant product definition.",
      "When in doubt, assume you need human professional judgment for legal, tax, and investment decisions.",
    ],
  },
  {
    slug: "how-to-read-pulse",
    title: "How to read the Market Pulse score",
    description:
      "A walkthrough of z-scores, volume ratios, and headline polarity used in Pulse.",
    date: "2026-08-02",
    body: [
      "Pulse starts at 50. Positive five-day momentum relative to recent volatility pushes it up; the reverse pushes it down. Unusual volume relative to a 20-day average also moves the score.",
      "Optional headline polarity is a tiny lexicon over public titles. Missing headlines contribute zero. The formula is documented on the Methodology page and implemented in open source TypeScript.",
      "Use Pulse to ask better questions (“Did volume spike with the move?”) rather than to justify a trade.",
      "If numbers look wrong, compare them to the delayed chart and recompute with the published equations.",
    ],
  },
];

for (const article of LEARN_ARTICLES) {
  assertCompliant(
    [article.title, article.description, ...article.body].join("\n"),
    `learn/${article.slug}`,
  );
}

export function getArticle(slug: string): LearnArticle | undefined {
  return LEARN_ARTICLES.find((a) => a.slug === slug);
}
