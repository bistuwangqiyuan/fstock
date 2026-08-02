import Link from "next/link";

const links = [
  { href: "/", label: "Pulse" },
  { href: "/methodology", label: "Methodology" },
  { href: "/learn", label: "Learn" },
  { href: "/alerts", label: "Alerts" },
];

export function SiteHeader() {
  return (
    <header className="border-b border-black/5 bg-white/70 backdrop-blur-md sticky top-0 z-40">
      <div className="mx-auto flex max-w-5xl items-center justify-between px-5 py-4">
        <Link href="/" className="text-[17px] font-semibold tracking-tight text-[#1d1d1f]">
          F Stock
        </Link>
        <nav className="flex flex-wrap items-center gap-4 text-[13px] text-[#6e6e73]">
          {links.map((l) => (
            <Link key={l.href} href={l.href} className="hover:text-[#1d1d1f] transition-colors">
              {l.label}
            </Link>
          ))}
        </nav>
      </div>
    </header>
  );
}
