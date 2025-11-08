"use client";

import { useState, useMemo } from "react";
import { motion } from "framer-motion";
import SectionTitle from "../components/SectionTitle";
import BriefCard from "../components/BriefCard";
import { Search } from "lucide-react";

interface BriefPost {
  slug: string;
  title: string;
  excerpt: string;
  date: string;
  tags: string[];
}

interface BriefsClientProps {
  initialBriefs: BriefPost[];
  initialTags: string[];
}

export default function BriefsClient({ initialBriefs, initialTags }: BriefsClientProps) {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedTag, setSelectedTag] = useState<string | null>(null);

  const filteredBriefs = useMemo(() => {
    return initialBriefs.filter((brief) => {
      const matchesSearch =
        brief.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        brief.excerpt.toLowerCase().includes(searchQuery.toLowerCase());
      const matchesTag = selectedTag === null || brief.tags.includes(selectedTag);
      return matchesSearch && matchesTag;
    });
  }, [searchQuery, selectedTag, initialBriefs]);

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
      {/* Hero Section */}
      <section className="py-20 relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <SectionTitle
            title="Research & Briefs"
            subtitle="Strategic intelligence reports and analysis briefs"
            center
          />

          {/* Search and Filter */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="max-w-4xl mx-auto mb-12"
          >
            <div className="flex flex-col md:flex-row gap-4 mb-6">
              <div className="flex-1 relative">
                <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-text-muted" />
                <input
                  type="text"
                  placeholder="Search briefs..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-12 pr-4 py-3 bg-background/50 border border-accent/20 rounded-lg text-text placeholder-text-muted focus:outline-none focus:border-accent focus:ring-2 focus:ring-accent/20 transition-all"
                />
              </div>
            </div>

            {/* Tags Filter */}
            <div className="flex flex-wrap gap-2">
              <button
                onClick={() => setSelectedTag(null)}
                className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all ${
                  selectedTag === null
                    ? "bg-accent text-background glow"
                    : "bg-background/50 text-text-muted hover:bg-accent/10 hover:text-accent border border-accent/20"
                }`}
              >
                All
              </button>
              {initialTags.map((tag) => (
                <button
                  key={tag}
                  onClick={() => setSelectedTag(selectedTag === tag ? null : tag)}
                  className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all ${
                    selectedTag === tag
                      ? "bg-accent text-background glow"
                      : "bg-background/50 text-text-muted hover:bg-accent/10 hover:text-accent border border-accent/20"
                  }`}
                >
                  {tag}
                </button>
              ))}
            </div>
          </motion.div>

          {/* Briefs Grid */}
          {filteredBriefs.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredBriefs.map((brief, index) => (
                <BriefCard
                  key={brief.slug}
                  slug={brief.slug}
                  title={brief.title}
                  excerpt={brief.excerpt}
                  date={formatDate(brief.date)}
                  tags={brief.tags}
                  delay={index * 0.1}
                />
              ))}
            </div>
          ) : (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="text-center py-20"
            >
              <p className="text-text-muted text-lg">No briefs found matching your criteria.</p>
            </motion.div>
          )}
        </div>
      </section>
    </div>
  );
}

