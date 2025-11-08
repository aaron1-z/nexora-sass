"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { ArrowRight } from "lucide-react";

interface CTASectionProps {
  title?: string;
  subtitle?: string;
  primaryCTA?: string;
  primaryLink?: string;
  secondaryCTA?: string;
  secondaryLink?: string;
}

export default function CTASection({
  title = "Get Actionable Intelligence Now",
  subtitle = "Transform news into intelligence. Nexora delivers decision-grade Action Briefs for your focus areas — automatically reasoned from live data.",
  primaryCTA = "Request Demo",
  primaryLink = "/contact",
  secondaryCTA = "Join Beta",
  secondaryLink = "/contact",
}: CTASectionProps) {
  return (
    <section className="relative py-20 overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-br from-accent/10 to-accent-secondary/10" />
      
      <div className="relative z-10 max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          <h2 className="text-4xl md:text-5xl font-bold mb-6 gradient-text">
            {title}
          </h2>
          <p className="text-xl text-text-muted mb-12 max-w-2xl mx-auto">
            {subtitle}
          </p>
          
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              href={primaryLink}
              className="group px-8 py-4 bg-gradient-to-r from-accent to-accent-secondary text-background rounded-lg font-semibold text-lg hover:scale-105 transition-transform glow-accent flex items-center space-x-2"
            >
              <span>{primaryCTA}</span>
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Link>
            {secondaryCTA && (
              <Link
                href={secondaryLink}
                className="px-8 py-4 border-2 border-accent/50 text-accent rounded-lg font-semibold text-lg hover:bg-accent/10 transition-colors"
              >
                {secondaryCTA}
              </Link>
            )}
          </div>
        </motion.div>
      </div>
    </section>
  );
}

