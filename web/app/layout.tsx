import type { Metadata } from "next";
import { DisclaimerBanner } from "@/components/DisclaimerBanner";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";
import "./globals.css";

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || "https://fstock.vercel.app";

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  title: {
    default: "F Stock — Public market pulse & investor education",
    template: "%s · F Stock",
  },
  description:
    "Public market information and investor education. Reproducible Market Pulse heuristics. Not investment advice.",
  openGraph: {
    title: "F Stock",
    description:
      "Public market pulse and investor education. Delayed quotes. Open methodology. Not investment advice.",
    type: "website",
    url: siteUrl,
  },
  robots: { index: true, follow: true },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="min-h-screen antialiased">
        <DisclaimerBanner />
        <SiteHeader />
        <main className="mx-auto max-w-5xl px-5">{children}</main>
        <SiteFooter />
      </body>
    </html>
  );
}
