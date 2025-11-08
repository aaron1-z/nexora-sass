"use client";

import { motion } from "framer-motion";
import { LucideIcon } from "lucide-react";

interface FeatureCardProps {
  icon: LucideIcon;
  title: string;
  description: string;
  delay?: number;
}

export default function FeatureCard({ icon: Icon, title, description, delay = 0 }: FeatureCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.5, delay }}
      whileHover={{ scale: 1.05, y: -5 }}
      className="relative p-6 rounded-xl bg-gradient-to-br from-background/80 to-background/40 backdrop-blur-xl border border-accent/20 hover:border-accent/40 transition-all group"
    >
      <div className="absolute inset-0 bg-gradient-to-br from-accent/5 to-accent-secondary/5 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity" />
      
      <div className="relative z-10">
        <div className="w-12 h-12 bg-gradient-to-br from-accent to-accent-secondary rounded-lg flex items-center justify-center mb-4 glow">
          <Icon className="w-6 h-6 text-background" />
        </div>
        <h3 className="text-xl font-semibold mb-2 text-text">{title}</h3>
        <p className="text-text-muted">{description}</p>
      </div>
    </motion.div>
  );
}

