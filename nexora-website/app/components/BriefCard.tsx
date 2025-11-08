"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { Calendar, Tag } from "lucide-react";

interface BriefCardProps {
  slug: string;
  title: string;
  excerpt: string;
  date: string;
  tags: string[];
  delay?: number;
}

export default function BriefCard({ slug, title, excerpt, date, tags, delay = 0 }: BriefCardProps) {
  return (
    <motion.article
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.5, delay }}
      whileHover={{ scale: 1.02, y: -5 }}
      className="group"
    >
      <Link href={`/briefs/${slug}`}>
        <div className="relative p-6 rounded-xl bg-gradient-to-br from-background/80 to-background/40 backdrop-blur-xl border border-accent/20 hover:border-accent/40 transition-all h-full">
          <div className="absolute inset-0 bg-gradient-to-br from-accent/5 to-accent-secondary/5 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity" />
          
          <div className="relative z-10">
            <div className="flex items-center space-x-4 mb-3 text-sm text-text-muted">
              <div className="flex items-center space-x-1">
                <Calendar className="w-4 h-4" />
                <span>{date}</span>
              </div>
            </div>
            
            <h3 className="text-xl font-semibold mb-3 text-text group-hover:text-accent transition-colors">
              {title}
            </h3>
            
            <p className="text-text-muted mb-4 line-clamp-3">
              {excerpt}
            </p>
            
            {tags.length > 0 && (
              <div className="flex flex-wrap gap-2">
                {tags.map((tag) => (
                  <span
                    key={tag}
                    className="px-3 py-1 text-xs bg-accent/10 text-accent rounded-full border border-accent/20 flex items-center space-x-1"
                  >
                    <Tag className="w-3 h-3" />
                    <span>{tag}</span>
                  </span>
                ))}
              </div>
            )}
          </div>
        </div>
      </Link>
    </motion.article>
  );
}

