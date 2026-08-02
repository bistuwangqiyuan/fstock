import { revalidatePath, revalidateTag } from "next/cache";
import { NextResponse } from "next/server";
import { SEED_SYMBOLS } from "@/lib/symbols";

export async function GET(req: Request) {
  const secret = process.env.CRON_SECRET;
  const auth = req.headers.get("authorization");
  if (!secret || auth !== `Bearer ${secret}`) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  for (const symbol of SEED_SYMBOLS) {
    revalidateTag(`yahoo:${symbol}`, "max");
  }
  revalidatePath("/");
  for (const symbol of SEED_SYMBOLS) {
    revalidatePath(`/symbol/${symbol}`);
  }

  return NextResponse.json({
    ok: true,
    revalidated: SEED_SYMBOLS.length,
    at: new Date().toISOString(),
  });
}
