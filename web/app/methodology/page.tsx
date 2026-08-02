import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Methodology",
  description:
    "Reproducible Market Pulse formulas, data sources, update cadence, and limitations.",
};

export default function MethodologyPage() {
  return (
    <article className="animate-rise prose-none max-w-3xl pb-16 pt-12">
      <h1 className="text-[40px] font-bold tracking-tight text-[#1d1d1f]">
        Methodology
      </h1>
      <p className="mt-4 text-[18px] text-[#6e6e73]">
        Every number on F Stock should be inspectable. Pulse is a published
        heuristic, not a proprietary black-box tip sheet.
      </p>

      <section className="mt-12">
        <h2 className="text-[24px] font-semibold tracking-tight">Data sources</h2>
        <ul className="mt-4 list-disc space-y-2 pl-5 text-[15px] text-[#1d1d1f]">
          <li>
            Delayed OHLCV from Yahoo Finance chart v8 (
            <code className="text-[13px]">query1.finance.yahoo.com/v8/finance/chart</code>
            ). Unofficial public endpoint; may rate-limit or change.
          </li>
          <li>
            Seed JSON fallback in{" "}
            <code className="text-[13px]">web/data/snapshots/market.json</code>{" "}
            when live fetch fails.
          </li>
          <li>Optional headline polarity when titles are supplied (often empty).</li>
        </ul>
      </section>

      <section className="mt-12">
        <h2 className="text-[24px] font-semibold tracking-tight">Pulse formula</h2>
        <pre className="mt-4 overflow-x-auto rounded-2xl bg-[#1d1d1f] p-5 text-[13px] leading-relaxed text-[#f5f5f7]">
{`z_ret  = five_day_return / stdev(last_60_daily_returns)
z_vol  = clip(today_volume / avg_volume_20 - 1, -3, 3)
s_news = clip(headline_polarity, -1, 1)   # 0 if no headlines
Pulse  = clip(50 + 15*z_ret + 10*z_vol + 10*s_news, 0, 100)`}
        </pre>
        <p className="mt-4 text-[15px] text-[#6e6e73]">
          Implementation: <code>web/lib/sentiment.ts</code>. Unit tests in{" "}
          <code>web/lib/sentiment.test.ts</code>.
        </p>
      </section>

      <section className="mt-12">
        <h2 className="text-[24px] font-semibold tracking-tight">Update cadence</h2>
        <p className="mt-4 text-[15px] text-[#6e6e73]">
          Pages revalidate about every hour (ISR). A Vercel Cron hits{" "}
          <code>/api/cron/refresh</code> daily to revalidate tagged market data.
          Cron requires <code>CRON_SECRET</code>.
        </p>
      </section>

      <section className="mt-12">
        <h2 className="text-[24px] font-semibold tracking-tight">Limitations</h2>
        <ul className="mt-4 list-disc space-y-2 pl-5 text-[15px] text-[#6e6e73]">
          <li>Not real-time. Not exchange-grade. Not affiliated with Yahoo.</li>
          <li>Pulse is not a forecast, credit rating, or investment recommendation.</li>
          <li>No personalized portfolios or buy/sell instructions—by design.</li>
          <li>Live fetch may fail; UI discloses seed fallback when used.</li>
        </ul>
      </section>

      <section className="mt-12 rounded-2xl border border-black/5 bg-white p-6">
        <h2 className="text-[20px] font-semibold">How to verify</h2>
        <ol className="mt-3 list-decimal space-y-2 pl-5 text-[14px] text-[#6e6e73]">
          <li>
            Clone the repo and run <code>cd web &amp;&amp; npm test</code>.
          </li>
          <li>Open a symbol page and compare breakdown fields to the formula.</li>
          <li>
            Hand-check a short close series: compute 5-day return and 60-day
            return stdev, then z_ret.
          </li>
        </ol>
      </section>
    </article>
  );
}
