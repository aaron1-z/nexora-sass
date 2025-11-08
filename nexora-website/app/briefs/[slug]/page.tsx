import { notFound } from "next/navigation";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Calendar, Tag, ArrowLeft } from "lucide-react";
import Link from "next/link";
import { getBriefBySlug, getAllBriefs } from "@/lib/markdown";
import type { Metadata } from "next";

interface PageProps {
  params: {
    slug: string;
  };
}

export async function generateStaticParams() {
  const briefs = getAllBriefs();
  return briefs.map((brief) => ({
    slug: brief.slug,
  }));
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const brief = getBriefBySlug(params.slug);

  if (!brief) {
    return {
      title: "Brief Not Found",
    };
  }

  return {
    title: `${brief.title} | Nexora Intelligence`,
    description: brief.excerpt,
    keywords: brief.tags.join(", "),
  };
}

export default function BriefPage({ params }: PageProps) {
  const brief = getBriefBySlug(params.slug);

  if (!brief) {
    notFound();
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  };

  return (
    <div className="relative pt-20">
      <article className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Back Button */}
        <Link
          href="/briefs"
          className="inline-flex items-center space-x-2 text-text-muted hover:text-accent transition-colors mb-8"
        >
          <ArrowLeft className="w-5 h-5" />
          <span>Back to Briefs</span>
        </Link>

        {/* Header */}
        <header className="mb-8">
          <h1 className="text-4xl md:text-5xl font-bold mb-6 gradient-text">
            {brief.title}
          </h1>
          <div className="flex flex-wrap items-center gap-6 text-sm text-text-muted">
            <div className="flex items-center space-x-2">
              <Calendar className="w-4 h-4" />
              <span>{formatDate(brief.date)}</span>
            </div>
            {brief.tags.length > 0 && (
              <div className="flex items-center space-x-2 flex-wrap gap-2">
                <Tag className="w-4 h-4" />
                {brief.tags.map((tag) => (
                  <span
                    key={tag}
                    className="px-3 py-1 bg-accent/10 text-accent rounded-full border border-accent/20"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            )}
          </div>
        </header>

        {/* Content */}
        <div className="prose prose-invert prose-lg max-w-none">
          <div className="markdown-content">
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              components={{
                h1: ({ node, ...props }) => (
                  <h1 className="text-3xl font-bold mt-8 mb-4 gradient-text" {...props} />
                ),
                h2: ({ node, ...props }) => (
                  <h2 className="text-2xl font-semibold mt-6 mb-3 text-text" {...props} />
                ),
                h3: ({ node, ...props }) => (
                  <h3 className="text-xl font-semibold mt-4 mb-2 text-text" {...props} />
                ),
                p: ({ node, ...props }) => (
                  <p className="text-text-muted mb-4 leading-relaxed" {...props} />
                ),
                a: ({ node, ...props }) => (
                  <a
                    className="text-accent hover:text-accent-secondary underline"
                    {...props}
                  />
                ),
                ul: ({ node, ...props }) => (
                  <ul className="list-disc list-inside mb-4 text-text-muted space-y-2" {...props} />
                ),
                ol: ({ node, ...props }) => (
                  <ol className="list-decimal list-inside mb-4 text-text-muted space-y-2" {...props} />
                ),
                code: ({ node, ...props }) => (
                  <code
                    className="px-2 py-1 bg-background/50 border border-accent/20 rounded text-accent text-sm"
                    {...props}
                  />
                ),
                blockquote: ({ node, ...props }) => (
                  <blockquote
                    className="border-l-4 border-accent pl-4 italic text-text-muted my-4"
                    {...props}
                  />
                ),
              }}
            >
              {brief.content}
            </ReactMarkdown>
          </div>
        </div>

      </article>
    </div>
  );
}

