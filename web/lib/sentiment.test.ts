import { describe, expect, it } from "vitest";
import {
  computePulse,
  fiveDayReturn,
  headlinePolarity,
  stdev,
  zRetFromCloses,
  zVolFromVolumes,
} from "./sentiment";

describe("sentiment math", () => {
  it("computes five-day return", () => {
    const closes = [100, 101, 102, 103, 104, 110];
    expect(fiveDayReturn(closes)).toBeCloseTo(0.1, 6);
  });

  it("computes sample stdev", () => {
    expect(stdev([2, 4, 4, 4, 5, 5, 7, 9])).toBeCloseTo(2.138, 2);
  });

  it("z_ret is return over volatility", () => {
    const closes: number[] = [];
    let p = 100;
    for (let i = 0; i < 70; i++) {
      p *= 1.001;
      closes.push(p);
    }
    // Force last 5 days upward jump
    closes[closes.length - 1] = closes[closes.length - 6] * 1.05;
    const z = zRetFromCloses(closes);
    expect(z).toBeGreaterThan(0);
  });

  it("z_vol detects volume spike", () => {
    const volumes = Array(25).fill(1000);
    volumes[volumes.length - 1] = 3000;
    expect(zVolFromVolumes(volumes)).toBeCloseTo(2, 5);
  });

  it("headline polarity bounds", () => {
    expect(headlinePolarity([])).toBe(0);
    expect(headlinePolarity(["Stock surges to record growth"])).toBeGreaterThan(0);
    expect(headlinePolarity(["Shares plunge after fraud lawsuit"])).toBeLessThan(0);
  });

  it("Pulse formula matches published equation", () => {
    const bars = Array.from({ length: 70 }, (_, i) => ({
      close: 100 + i * 0.1,
      volume: 1_000_000,
    }));
    bars[bars.length - 1] = {
      close: bars[bars.length - 6].close * 1.02,
      volume: 2_000_000,
    };
    const { zRet, zVol, sNews, pulse } = computePulse(bars, []);
    const expected = Math.min(
      100,
      Math.max(0, 50 + 15 * zRet + 10 * zVol + 10 * sNews),
    );
    expect(pulse).toBeCloseTo(expected, 1);
  });
});
