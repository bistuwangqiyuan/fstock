import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { AdSlot } from "@/components/AdSlot";
import { Sparkline } from "@/components/Sparkline";
import { getSymbolCard } from "@/lib/market";
import { SEED_SYMBOLS, normalizeTicker, SYMBOL_NAMES } from "@/lib/symbols";

export const revalidate = 3600;

type Props = { params: Promise<{ ticker: string }> };

export async function generateStaticParams() {
  return SEED_SYMBOLS.map((ticker) => ({ ticker }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { ticker: raw } = await params;
  const ticker = normalizeTicker(raw);
  const name = SYMBOL_NAMES[ticker] || ticker;
  return {
    title: `${ticker} public pulse`,
    description: `Delayed public quote context and reproducible Market Pulse for ${name}. Not investment advice.`,
  };
}

export default async function SymbolPage({ params }: Props) {
  const { ticker: raw } = await params;
  const ticker = normalizeTicker(raw);
  if (!ticker) notFound();

  const card = await getSymbolCard(ticker);
  if (!card) notFound();

  const ch = card.changePct;
  const chColor =
    ch == null ? "text-[#6e6e73]" : ch >= 0 ? "text-[#0f766e]" : "text-[#b91c1c]";

  return (
    <div className="animate-rise pb-16 pt-12">
      <p className="text-[13px] text-[#6e6e73]">
        <Link href="/" className="hover:text-[#1d1d1f]">
          Pulse
        </Link>{" "}
        / {card.symbol}
      </p>
      <h1 className="mt-3 text-[40px] font-bold tracking-tight text-[#1d1d1f]">
        {card.symbol}
      </h1>
      <p className="mt-1 text-[18px] text-[#6e6e73]">{card.name}</p>

      <div className="mt-8 grid gap-4 sm:grid-cols-3">
        <div className="rounded-2xl border border-black/5 bg-white p-5 shadow-[0_20px_60px_rgba(0,0,0,0.04)]">
          <div className="text-[12px] text-[#6e6e73]">Delayed price</div>
          <div className="mt-2 text-[32px] font-semibold tabular-nums">
            {card.price == null
              ? "—"
              : new Intl.NumberFormat("en-US", {
                  style: "currency",
                  currency: card.currency || "USD",
                }).format(card.price)}
          </div>
          <div className={`mt-1 text-[14px] tabular-nums ${chColor}`}>
            {ch == null ? "—" : `${ch >= 0 ? "+" : ""}${ch.toFixed(2)}%`}
          </div>
        </div>
        <div className="rounded-2xl border border-black/5 bg-white p-5 shadow-[0_20px_60px_rgba(0,0,0,0.04)]">
          <div className="text-[12px] text-[#6e6e73]">Market Pulse</div>
          <div className="mt-2 text-[32px] font-semibold tabular-nums">
            {card.pulse.toFixed(1)}
          </div>
          <div className="mt-1 text-[12px] text-[#6e6e73]">
            Heuristic · 0–100 · not a rating
          </div>
        </div>
        <div className="rounded-2xl border border-black/5 bg-white p-5 shadow-[0_20px_60px_rgba(0,0,0,0.04)]">
          <div className="text-[12px] text-[#6e6e73]">Recent path</div>
          <div className="mt-4">
            <Sparkline values={card.spark} className="w-full max-w-none" />
          </div>
        </div>
      </div>

      <section className="mt-10 rounded-2xl border border-black/5 bg-white p-6">
        <h2 className="text-[20px] font-semibold tracking-tight">Pulse breakdown</h2>
        <dl className="mt-4 grid gap-3 text-[14px] sm:grid-cols-3">
          <div>
            <dt className="text-[#6e6e73]">z_ret</dt>
            <dd className="font-medium tabular-nums">{card.breakdown.zRet}</dd>
          </div>
          <div>
            <dt className="text-[#6e6e73]">z_vol</dt>
            <dd className="font-medium tabular-nums">{card.breakdown.zVol}</dd>
          </div>
          <div>
            <dt className="text-[#6e6e73]">s_news</dt>
            <dd className="font-medium tabular-nums">{card.breakdown.sNews}</dd>
          </div>
        </dl>
        <p className="mt-4 text-[13px] text-[#6e6e73]">
          Formula: Pulse = clip(50 + 15·z_ret + 10·z_vol + 10·s_news, 0, 100).{" "}
          <Link href="/methodology" className="text-[#0071e3]">
            Full methodology
          </Link>
        </p>
      </section>

      {card.fromFallback ? (
        <p className="mt-6 rounded-2xl border border-amber-200 bg-[#fff7ed] px-4 py-3 text-[13px] text-[#9a3412]">
          Showing seed fallback data because live chart fetch was unavailable.
          Values are illustrative until refresh succeeds.
        </p>
      ) : null}

      <p className="mt-6 text-[12px] text-[#6e6e73]">
        Fetched {new Date(card.fetchedAt).toUTCString()}. Delayed/unofficial
        public chart data. Not affiliated with the exchange or Yahoo. Not
        investment advice.
      </p>

      <div className="mt-10">
        <AdSlot slot="symbol" />
      </div>
    </div>
  );
}
