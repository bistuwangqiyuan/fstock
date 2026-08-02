import { AdSlot } from "@/components/AdSlot";
import { PulseCard } from "@/components/PulseCard";
import { getMarketBundle } from "@/lib/market";

export const revalidate = 3600;

export default async function HomePage() {
  const market = await getMarketBundle();
  const featured = market.symbols.find((s) => s.symbol === "F") ?? market.symbols[0];

  return (
    <div className="pb-16">
      <section className="animate-rise flex min-h-[70vh] flex-col justify-end border-b border-black/5 pb-14 pt-16">
        <p className="mb-4 inline-flex w-fit items-center gap-2 rounded-full border border-black/5 bg-white px-3 py-1 text-[12px] text-[#6e6e73]">
          <span className="h-1.5 w-1.5 rounded-full bg-[#0071e3]" />
          Full-AI unmanned · public information only
        </p>
        <h1 className="max-w-3xl text-[clamp(40px,7vw,72px)] font-bold leading-[1.05] tracking-[-0.035em] text-[#1d1d1f]">
          F Stock
        </h1>
        <p className="mt-5 max-w-xl text-[21px] leading-snug text-[#6e6e73]">
          Public market pulse and investor education—delayed quotes, open
          methodology, and no trade instructions tailored to you.
        </p>
        <div className="mt-8 flex flex-wrap gap-3 text-[13px] text-[#6e6e73]">
          <span>Updated {new Date(market.updatedAt).toUTCString()}</span>
          <span>·</span>
          <span>Not investment advice</span>
        </div>
      </section>

      {featured ? (
        <section className="animate-rise py-12">
          <h2 className="text-[28px] font-semibold tracking-tight text-[#1d1d1f]">
            Spotlight · {featured.symbol}
          </h2>
          <p className="mt-2 max-w-2xl text-[16px] text-[#6e6e73]">
            Search interest in “F stock” often maps to Ford (NYSE: F). Here is a
            delayed public snapshot and a reproducible Pulse score—not a buy or
            sell call.
          </p>
          <div className="mt-6 max-w-md">
            <PulseCard card={featured} />
          </div>
        </section>
      ) : null}

      <section className="py-8">
        <h2 className="text-[28px] font-semibold tracking-tight text-[#1d1d1f]">
          Market pulse
        </h2>
        <p className="mt-2 text-[16px] text-[#6e6e73]">
          Heuristic scores from price momentum and volume. See Methodology for
          the exact formula.
        </p>
        <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {market.symbols.map((card) => (
            <PulseCard key={card.symbol} card={card} />
          ))}
        </div>
      </section>

      <section className="py-10">
        <AdSlot slot="home-mid" />
      </section>
    </div>
  );
}
