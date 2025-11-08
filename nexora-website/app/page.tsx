"use client";

import Hero from "./components/Hero";
import SectionTitle from "./components/SectionTitle";
import FeatureCard from "./components/FeatureCard";
import { FileText, Zap, TrendingUp, Bell, BarChart3, Brain, Shield, Target } from "lucide-react";
import { motion } from "framer-motion";

export default function Home() {
  const features = [
    {
      icon: FileText,
      title: "Action Briefs",
      description: "AI-generated executive reports that transform raw data into strategic insights. Get comprehensive analyses with scenarios, forecasts, and actionable recommendations.",
    },
    {
      icon: Zap,
      title: "Live Intelligence Feed",
      description: "Real-time event detection and monitoring. Stay ahead with instant notifications about critical developments in your focus areas.",
    },
    {
      icon: TrendingUp,
      title: "Strategic Forecasts",
      description: "Scenario & risk modeling powered by advanced AI reasoning. Explore bull/base/bear scenarios with probability assessments.",
    },
    {
      icon: Bell,
      title: "Custom Alerts",
      description: "Triggered by keywords, sentiment shifts, or market events. Set up intelligent monitoring that adapts to your priorities.",
    },
    {
      icon: BarChart3,
      title: "Market Intelligence Dashboards",
      description: "Visualize trends, momentum, and volatility. Get comprehensive analytics on entities, catalysts, and sentiment patterns.",
    },
    {
      icon: Brain,
      title: "AI Reasoning",
      description: "Advanced LLM-powered analysis that doesn't just display data—it interprets context, identifies patterns, and provides strategic insights.",
    },
  ];

  const useCases = [
    {
      icon: Target,
      title: "For Analysts & Researchers",
      description: "Reduce research time by 80%. Get comprehensive briefs on any topic with automatically generated scenarios and forecasts.",
      metric: "80% faster research",
    },
    {
      icon: BarChart3,
      title: "For Strategy Teams",
      description: "Make data-driven decisions with real-time intelligence. Understand market dynamics and competitive landscapes instantly.",
      metric: "Real-time insights",
    },
    {
      icon: Shield,
      title: "For Investors & Risk Officers",
      description: "Monitor risks and opportunities 24/7. Get alerted to critical developments before they impact your portfolio.",
      metric: "24/7 monitoring",
    },
  ];

  const testimonials = [
    {
      quote: "Feels like BloombergGPT for everyone. Nexora has transformed how we track market intelligence.",
      author: "Sarah Chen",
      role: "Head of Strategy, TechCorp",
    },
    {
      quote: "The Action Briefs are incredibly detailed. It's like having a team of analysts working 24/7.",
      author: "Michael Rodriguez",
      role: "Investment Analyst, Capital Partners",
    },
    {
      quote: "Finally, an AI that interprets data instead of just showing it. This is the future of intelligence.",
      author: "Dr. Emily Watson",
      role: "Research Director, Innovation Labs",
    },
  ];

  return (
    <div className="relative">
      {/* Hero Section */}
      <Hero />

      {/* Key Features Section */}
      <section className="py-20 relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <SectionTitle
            title="Powerful Features"
            subtitle="Everything you need to transform data into strategic intelligence"
            center
          />
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature, index) => (
              <FeatureCard
                key={feature.title}
                icon={feature.icon}
                title={feature.title}
                description={feature.description}
                delay={index * 0.1}
              />
            ))}
          </div>
        </div>
      </section>

      {/* Use Cases Section */}
      <section className="py-20 relative bg-gradient-to-b from-background to-background/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <SectionTitle
            title="Built for Decision-Makers"
            subtitle="Whether you're analyzing markets, planning strategy, or managing risk"
            center
          />
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {useCases.map((useCase, index) => {
              const Icon = useCase.icon;
              return (
                <motion.div
                  key={useCase.title}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  className="relative p-8 rounded-xl bg-gradient-to-br from-background/80 to-background/40 backdrop-blur-xl border border-accent/20 hover:border-accent/40 transition-all"
                >
                  <div className="w-16 h-16 bg-gradient-to-br from-accent to-accent-secondary rounded-lg flex items-center justify-center mb-6 glow">
                    <Icon className="w-8 h-8 text-background" />
                  </div>
                  <h3 className="text-2xl font-semibold mb-3 text-text">{useCase.title}</h3>
                  <p className="text-text-muted mb-4">{useCase.description}</p>
                  <div className="px-4 py-2 bg-accent/10 text-accent rounded-lg text-sm font-semibold inline-block border border-accent/20">
                    {useCase.metric}
                  </div>
                </motion.div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Action Brief Demo Section */}
      <section className="py-20 relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <SectionTitle
            title="See It In Action"
            subtitle="From query to comprehensive intelligence brief in seconds"
            center
          />
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6 }}
              className="space-y-4"
            >
              <div className="p-6 rounded-xl bg-gradient-to-br from-background/80 to-background/40 backdrop-blur-xl border border-accent/20">
                <h4 className="text-sm text-text-muted mb-2">Input Query</h4>
                <div className="text-2xl font-semibold text-accent">AI Chips Market</div>
              </div>
              <div className="flex items-center justify-center py-4">
                <motion.div
                  animate={{ y: [0, 10, 0] }}
                  transition={{ duration: 1.5, repeat: Infinity }}
                >
                  <Zap className="w-8 h-8 text-accent" />
                </motion.div>
              </div>
            </motion.div>
            
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6 }}
              className="p-8 rounded-xl bg-gradient-to-br from-background/80 to-background/40 backdrop-blur-xl border border-accent/20 glow"
            >
              <h4 className="text-sm text-text-muted mb-4">Output: Executive Summary</h4>
              <div className="space-y-3">
                <div className="h-4 bg-accent/20 rounded w-full animate-pulse" />
                <div className="h-4 bg-accent-secondary/20 rounded w-5/6 animate-pulse" style={{ animationDelay: "0.2s" }} />
                <div className="h-4 bg-accent/20 rounded w-4/5 animate-pulse" style={{ animationDelay: "0.4s" }} />
                <div className="h-4 bg-accent-secondary/20 rounded w-full animate-pulse" style={{ animationDelay: "0.6s" }} />
              </div>
              <div className="mt-6 pt-6 border-t border-accent/20">
                <h4 className="text-sm text-text-muted mb-3">Forecast Scenarios</h4>
                <div className="grid grid-cols-3 gap-3">
                  {["Bull", "Base", "Bear"].map((scenario) => (
                    <div key={scenario} className="p-3 bg-accent/10 rounded-lg text-center border border-accent/20">
                      <div className="text-sm font-semibold text-accent">{scenario}</div>
                      <div className="text-xs text-text-muted mt-1">65% prob</div>
                    </div>
                  ))}
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-20 relative bg-gradient-to-b from-background/50 to-background">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <SectionTitle
            title="What Our Users Say"
            subtitle="Trusted by analysts, strategists, and investors worldwide"
            center
          />
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="p-6 rounded-xl bg-gradient-to-br from-background/80 to-background/40 backdrop-blur-xl border border-accent/20"
              >
                <p className="text-text-muted mb-6 italic">"{testimonial.quote}"</p>
                <div>
                  <div className="font-semibold text-text">{testimonial.author}</div>
                  <div className="text-sm text-text-muted">{testimonial.role}</div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

    </div>
  );
}
