import type { Metadata } from "next";
import { DISCLAIMER_LONG } from "@/lib/compliance";

export const metadata: Metadata = {
  title: "Disclaimer",
  description: "Legal and product boundary disclaimer for F Stock.",
};

export default function DisclaimerPage() {
  return (
    <article className="animate-rise max-w-2xl whitespace-pre-wrap pb-16 pt-12 text-[15px] leading-relaxed text-[#1d1d1f]">
      <h1 className="mb-6 text-[40px] font-bold tracking-tight">Disclaimer</h1>
      {DISCLAIMER_LONG}
    </article>
  );
}
