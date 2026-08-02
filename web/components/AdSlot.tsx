/** Renders only when NEXT_PUBLIC_ADSENSE_CLIENT is configured. */
export function AdSlot({ slot }: { slot?: string }) {
  const client = process.env.NEXT_PUBLIC_ADSENSE_CLIENT;
  if (!client) {
    return (
      <div className="rounded-2xl border border-dashed border-black/10 bg-white/60 px-4 py-6 text-center text-[12px] text-[#6e6e73]">
        Ad space reserved. Configure <code>NEXT_PUBLIC_ADSENSE_CLIENT</code> to enable
        display ads. We do not invent revenue.
        {slot ? ` · slot ${slot}` : null}
      </div>
    );
  }

  return (
    <div
      className="min-h-[90px] rounded-2xl border border-black/5 bg-white p-2"
      data-ad-client={client}
      data-ad-slot={slot}
    >
      {/* AdSense script is loaded only when publisher id is present (future). */}
      <p className="text-center text-[11px] text-[#6e6e73]">Sponsored</p>
    </div>
  );
}
