import { DISCLAIMER_SHORT } from "@/lib/compliance";

export function DisclaimerBanner() {
  return (
    <div className="border-b border-amber-200/80 bg-[#fff7ed] text-[12px] text-[#9a3412]">
      <div className="mx-auto max-w-5xl px-5 py-2.5">{DISCLAIMER_SHORT}</div>
    </div>
  );
}
