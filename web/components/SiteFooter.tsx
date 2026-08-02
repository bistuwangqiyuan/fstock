import Link from "next/link";
import { DISCLAIMER_SHORT } from "@/lib/compliance";

export function SiteFooter() {
  return (
    <footer className="mt-20 border-t border-black/5 bg-white/50">
      <div className="mx-auto max-w-5xl px-5 py-10 text-[12px] leading-relaxed text-[#6e6e73]">
        <p className="max-w-3xl">{DISCLAIMER_SHORT}</p>
        <div className="mt-6 flex flex-wrap gap-4">
          <Link href="/disclaimer" className="hover:text-[#1d1d1f]">
            Disclaimer
          </Link>
          <Link href="/privacy" className="hover:text-[#1d1d1f]">
            Privacy
          </Link>
          <Link href="/methodology" className="hover:text-[#1d1d1f]">
            Methodology
          </Link>
          <a
            href="https://github.com/bistuwangqiyuan/fstock"
            className="hover:text-[#1d1d1f]"
            rel="noreferrer"
            target="_blank"
          >
            Source
          </a>
        </div>
        <p className="mt-6">© {new Date().getFullYear()} F Stock · Unmanned information product</p>
      </div>
    </footer>
  );
}
