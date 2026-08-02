import type { Metadata } from "next";
import Link from "next/link";
import { LEARN_ARTICLES } from "@/content/learn";

export const metadata: Metadata = {
  title: "Learn",
  description: "Investor education on public market information—without trade tips.",
};

export default function LearnIndexPage() {
  return (
    <div className="animate-rise pb-16 pt-12">
      <h1 className="text-[40px] font-bold tracking-tight text-[#1d1d1f]">Learn</h1>
      <p className="mt-4 max-w-2xl text-[18px] text-[#6e6e73]">
        Short explainers about public market data and why F Stock refuses to act
        like an adviser.
      </p>
      <ul className="mt-10 space-y-4">
        {LEARN_ARTICLES.map((a) => (
          <li key={a.slug}>
            <Link
              href={`/learn/${a.slug}`}
              className="block rounded-2xl border border-black/5 bg-white p-6 shadow-[0_20px_60px_rgba(0,0,0,0.04)] transition hover:-translate-y-0.5"
            >
              <div className="text-[12px] text-[#6e6e73]">{a.date}</div>
              <h2 className="mt-1 text-[22px] font-semibold tracking-tight text-[#1d1d1f]">
                {a.title}
              </h2>
              <p className="mt-2 text-[15px] text-[#6e6e73]">{a.description}</p>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
