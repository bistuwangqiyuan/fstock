import Link from "next/link";
import type { SymbolCard } from "@/lib/market";
import { Sparkline } from "./Sparkline";

function fmtPrice(price: number | null, currency: string): string {
  if (price == null) return "—";
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: currency || "USD",
    maximumFractionDigits: 2,
  }).format(price);
}

export function PulseCard({ card }: { card: SymbolCard }) {
  const ch = card.changePct;
  const chColor =
    ch == null ? "text-[#6e6e73]" : ch >= 0 ? "text-[#0f766e]" : "text-[#b91c1c]";

  return (
    <Link
      href={`/symbol/${card.symbol}`}
      className="group block rounded-2xl border border-black/[0.06] bg-white p-5 shadow-[0_20px_60px_rgba(0,0,0,0.04)] transition-transform hover:-translate-y-0.5"
    >
      <div className="flex items-start justify-between gap-3">
        <div>
          <div className="text-[13px] font-semibold tracking-tight text-[#1d1d1f]">
            {card.symbol}
          </div>
          <div className="mt-0.5 text-[12px] text-[#6e6e73] line-clamp-1">{card.name}</div>
        </div>
        <div className="text-right">
          <div className="text-[15px] font-semibold tabular-nums text-[#1d1d1f]">
            {fmtPrice(card.price, card.currency)}
          </div>
          <div className={`text-[12px] tabular-nums ${chColor}`}>
            {ch == null ? "—" : `${ch >= 0 ? "+" : ""}${ch.toFixed(2)}%`}
          </div>
        </div>
      </div>
      <div className="mt-4 flex items-end justify-between">
        <div>
          <div className="text-[11px] uppercase tracking-wide text-[#6e6e73]">Pulse</div>
          <div className="text-[28px] font-semibold tracking-tight text-[#1d1d1f] tabular-nums">
            {card.pulse.toFixed(1)}
          </div>
        </div>
        <Sparkline values={card.spark} />
      </div>
      <p className="mt-3 text-[11px] text-[#6e6e73]">
        Heuristic information score · not a recommendation
      </p>
    </Link>
  );
}
