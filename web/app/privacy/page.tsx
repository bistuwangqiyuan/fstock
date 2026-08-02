import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Privacy",
  description: "Privacy practices for F Stock.",
};

export default function PrivacyPage() {
  return (
    <article className="animate-rise max-w-2xl pb-16 pt-12 text-[15px] leading-relaxed text-[#1d1d1f]">
      <h1 className="text-[40px] font-bold tracking-tight">Privacy</h1>
      <p className="mt-6 text-[#6e6e73]">
        We collect the minimum needed to operate an unmanned information site.
      </p>
      <ul className="mt-6 list-disc space-y-3 pl-5 text-[#6e6e73]">
        <li>
          <strong className="text-[#1d1d1f]">Waitlist email:</strong> only if you
          submit the alerts form. Stored or emailed via Resend when configured;
          otherwise not persisted beyond the request response.
        </li>
        <li>
          <strong className="text-[#1d1d1f]">Hosting logs:</strong> Vercel may
          process standard request logs (IP, user agent) per its platform
          policies.
        </li>
        <li>
          <strong className="text-[#1d1d1f]">Ads:</strong> if AdSense is later
          enabled, Google may set cookies per their policies. Ads are off until
          a publisher id is configured.
        </li>
        <li>
          We do not sell personal data. We do not build personalized investment
          profiles.
        </li>
      </ul>
      <p className="mt-8 text-[#6e6e73]">
        Contact via the GitHub repository issues for privacy requests.
      </p>
    </article>
  );
}
