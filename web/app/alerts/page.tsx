import type { Metadata } from "next";
import { WaitlistForm } from "@/components/WaitlistForm";

export const metadata: Metadata = {
  title: "Fact alerts waitlist",
  description:
    "Join the waitlist for impersonal price/threshold fact alerts. Not investment advice.",
};

export default function AlertsPage() {
  return (
    <div className="animate-rise max-w-2xl pb-16 pt-12">
      <h1 className="text-[40px] font-bold tracking-tight text-[#1d1d1f]">
        Fact alerts
      </h1>
      <p className="mt-4 text-[18px] text-[#6e6e73]">
        Phase 0 is a waitlist for impersonal threshold notices—for example, “F
        last delayed close crossed a level you set.” Alerts will never say buy
        or sell.
      </p>
      <div className="mt-8 rounded-2xl border border-black/5 bg-white p-6 shadow-[0_20px_60px_rgba(0,0,0,0.04)]">
        <h2 className="text-[18px] font-semibold">Join the waitlist</h2>
        <p className="mt-2 text-[14px] text-[#6e6e73]">
          If <code>RESEND_API_KEY</code> is configured, we email a confirmation.
          Otherwise we validate your address and honestly tell you capture is
          pending ops setup—we do not fake a CRM.
        </p>
        <WaitlistForm />
      </div>
      <ul className="mt-8 list-disc space-y-2 pl-5 text-[14px] text-[#6e6e73]">
        <li>No trade instructions tailored to you</li>
        <li>No guaranteed outcomes</li>
        <li>Stripe paid tiers intentionally deferred to later phases</li>
      </ul>
    </div>
  );
}
