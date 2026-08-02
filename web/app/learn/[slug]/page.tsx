import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { getArticle, LEARN_ARTICLES } from "@/content/learn";

type Props = { params: Promise<{ slug: string }> };

export function generateStaticParams() {
  return LEARN_ARTICLES.map((a) => ({ slug: a.slug }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const article = getArticle(slug);
  if (!article) return { title: "Learn" };
  return { title: article.title, description: article.description };
}

export default async function LearnArticlePage({ params }: Props) {
  const { slug } = await params;
  const article = getArticle(slug);
  if (!article) notFound();

  return (
    <article className="animate-rise mx-auto max-w-2xl pb-16 pt-12">
      <p className="text-[13px] text-[#6e6e73]">
        <Link href="/learn" className="hover:text-[#1d1d1f]">
          Learn
        </Link>{" "}
        / {article.date}
      </p>
      <h1 className="mt-3 text-[36px] font-bold tracking-tight text-[#1d1d1f]">
        {article.title}
      </h1>
      <p className="mt-3 text-[17px] text-[#6e6e73]">{article.description}</p>
      <div className="mt-10 space-y-5 text-[16px] leading-relaxed text-[#1d1d1f]">
        {article.body.map((p) => (
          <p key={p.slice(0, 48)}>{p}</p>
        ))}
      </div>
      <p className="mt-10 text-[13px] text-[#6e6e73]">
        Educational information only. Not investment advice.
      </p>
    </article>
  );
}
