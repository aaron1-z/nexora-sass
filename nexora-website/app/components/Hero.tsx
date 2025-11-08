"use client";

import { motion } from "framer-motion";
import { Play } from "lucide-react";
import AnimatedBackground from "./AnimatedBackground";

export default function Hero() {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden pt-16">
      <AnimatedBackground />
      
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <motion.h1
            className="text-5xl md:text-7xl font-bold mb-6"
            style={{ lineHeight: '1.15' }}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <span className="block" style={{ paddingBottom: '0.1em' }}>Turn Data Chaos into</span>
            <span className="gradient-text block" style={{ paddingBottom: '0.2em' }}>Strategic Clarity</span>
          </motion.h1>

          <motion.p
            className="text-xl md:text-2xl text-text-muted mb-12 max-w-3xl mx-auto"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
          >
            Nexora Intelligence Engine transforms global information into
            real-time, actionable intelligence briefs for analysts, strategists,
            and investors.
          </motion.p>

          <motion.div
            className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.6 }}
          >
            <button className="px-8 py-4 border-2 border-accent/50 text-accent rounded-lg font-semibold text-lg hover:bg-accent/10 transition-colors flex items-center space-x-2">
              <Play className="w-5 h-5" />
              <span>Watch Overview</span>
            </button>
          </motion.div>

          {/* Floating dashboard mockup */}
          <motion.div
            className="relative max-w-4xl mx-auto mt-20"
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.8 }}
          >
            <div className="relative bg-gradient-to-br from-background/80 to-background/40 backdrop-blur-xl rounded-2xl p-8 border border-accent/20 glow">
              <div className="space-y-4">
                <div className="h-4 bg-accent/20 rounded w-3/4 animate-pulse" />
                <div className="h-4 bg-accent-secondary/20 rounded w-1/2 animate-pulse" style={{ animationDelay: "0.2s" }} />
                <div className="h-4 bg-accent/20 rounded w-5/6 animate-pulse" style={{ animationDelay: "0.4s" }} />
              </div>
              <div className="mt-6 grid grid-cols-3 gap-4">
                {[1, 2, 3].map((i) => (
                  <div key={i} className="h-24 bg-gradient-to-br from-accent/10 to-accent-secondary/10 rounded-lg border border-accent/20" />
                ))}
              </div>
            </div>
          </motion.div>
        </motion.div>
      </div>
    </section>
  );
}

