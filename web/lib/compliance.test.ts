import { describe, expect, it } from "vitest";
import { assertCompliant, findBannedPhrases } from "./compliance";
import { LEARN_ARTICLES } from "@/content/learn";

describe("compliance", () => {
  it("flags banned phrases", () => {
    expect(findBannedPhrases("This is a strong buy tip")).toContain("strong buy");
    expect(findBannedPhrases("Public delayed quote")).toHaveLength(0);
  });

  it("learn articles are compliant", () => {
    for (const a of LEARN_ARTICLES) {
      expect(() =>
        assertCompliant(
          [a.title, a.description, ...a.body].join("\n"),
          a.slug,
        ),
      ).not.toThrow();
    }
  });
});
