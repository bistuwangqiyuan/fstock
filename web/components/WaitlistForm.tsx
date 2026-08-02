"use client";

import { useState } from "react";

export function WaitlistForm() {
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState<"idle" | "loading" | "ok" | "err">("idle");
  const [message, setMessage] = useState("");

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setStatus("loading");
    setMessage("");
    try {
      const res = await fetch("/api/waitlist", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });
      const data = (await res.json()) as { ok?: boolean; message?: string; error?: string };
      if (!res.ok) {
        setStatus("err");
        setMessage(data.error || "Something went wrong.");
        return;
      }
      setStatus("ok");
      setMessage(data.message || "You’re on the list.");
      setEmail("");
    } catch {
      setStatus("err");
      setMessage("Network error. Please try again.");
    }
  }

  return (
    <form onSubmit={onSubmit} className="mt-6 flex flex-col gap-3 sm:flex-row">
      <label className="sr-only" htmlFor="email">
        Email
      </label>
      <input
        id="email"
        type="email"
        required
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="you@example.com"
        className="flex-1 rounded-full border border-black/10 bg-white px-5 py-3 text-[15px] text-[#1d1d1f] outline-none ring-[#0071e3] focus:ring-2"
      />
      <button
        type="submit"
        disabled={status === "loading"}
        className="rounded-full bg-[#0071e3] px-6 py-3 text-[15px] font-medium text-white transition hover:bg-[#0077ED] disabled:opacity-60"
      >
        {status === "loading" ? "Joining…" : "Join waitlist"}
      </button>
      {message ? (
        <p
          className={`sm:basis-full text-[13px] ${
            status === "err" ? "text-[#b91c1c]" : "text-[#0f766e]"
          }`}
        >
          {message}
        </p>
      ) : null}
    </form>
  );
}
