"use client";

import { motion } from "framer-motion";
import SectionTitle from "../components/SectionTitle";
import { Brain, Target, Users, Zap, Code, Database } from "lucide-react";

export default function AboutPage() {
  const missionPoints = [
    {
      icon: Target,
      title: "Our Mission",
      description: "Build real-time intelligence for decision-makers. We believe that access to strategic intelligence shouldn't be limited to large corporations with massive budgets.",
    },
    {
      icon: Brain,
      title: "Our Vision",
      description: "To make real-time intelligence accessible to every decision-maker. We envision a world where anyone can turn data chaos into strategic clarity.",
    },
    {
      icon: Zap,
      title: "Our Approach",
      description: "Unlike search or dashboards, Nexora interprets—it doesn't just display. We use advanced AI reasoning to understand context, identify patterns, and provide actionable insights.",
    },
  ];

  const technologyFeatures = [
    {
      icon: Brain,
      title: "LLM Reasoning",
      description: "Advanced language models power our strategic analysis, generating comprehensive briefs with scenario planning and risk assessment.",
    },
    {
      icon: Database,
      title: "Trend Analytics",
      description: "Real-time trend detection and momentum analysis using advanced statistical models and pattern recognition.",
    },
    {
      icon: Code,
      title: "Alert System",
      description: "Intelligent monitoring system that tracks keywords, sentiment shifts, and market events with customizable triggers.",
    },
  ];

  const team = [
    {
      name: "Alex Chen",
      role: "Co-Founder & CEO",
      bio: "Former physicist turned AI engineer. Led intelligence systems at leading tech companies.",
      placeholder: "AC",
    },
    {
      name: "Sarah Martinez",
      role: "Co-Founder & CTO",
      bio: "AI researcher with expertise in NLP and strategic reasoning. PhD in Computer Science from Stanford.",
      placeholder: "SM",
    },
    {
      name: "David Kim",
      role: "Head of Product",
      bio: "Product strategist with 10+ years building intelligence platforms for enterprise clients.",
      placeholder: "DK",
    },
  ];

  return (
    <div className="relative pt-20">
      {/* Hero Section */}
      <section className="py-20 relative">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-5xl md:text-6xl font-bold mb-6 gradient-text"
          >
            About Nexora
          </motion.h1>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="text-xl text-text-muted"
          >
            Built by physicists and AI engineers to make sense of the world's information.
          </motion.p>
        </div>
      </section>

      {/* Mission Section */}
      <section className="py-20 relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <SectionTitle
            title="Our Mission"
            subtitle="Transforming how decision-makers access and use intelligence"
            center
          />
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {missionPoints.map((point, index) => {
              const Icon = point.icon;
              return (
                <motion.div
                  key={point.title}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  className="p-6 rounded-xl bg-gradient-to-br from-background/80 to-background/40 backdrop-blur-xl border border-accent/20"
                >
                  <div className="w-12 h-12 bg-gradient-to-br from-accent to-accent-secondary rounded-lg flex items-center justify-center mb-4 glow">
                    <Icon className="w-6 h-6 text-background" />
                  </div>
                  <h3 className="text-xl font-semibold mb-3 text-text">{point.title}</h3>
                  <p className="text-text-muted">{point.description}</p>
                </motion.div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Technology Section */}
      <section className="py-20 relative bg-gradient-to-b from-background to-background/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <SectionTitle
            title="Our Technology"
            subtitle="What powers the Nexora Intelligence Engine"
            center
          />
          <div className="max-w-3xl mx-auto mb-12">
            <p className="text-lg text-text-muted text-center mb-8">
              The Nexora Engine combines advanced AI reasoning with real-time data processing
              to transform global information into actionable intelligence. Our system uses
              state-of-the-art language models, trend analytics, and intelligent alerting to
              deliver comprehensive briefs that help you make better decisions.
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {technologyFeatures.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <motion.div
                  key={feature.title}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  className="p-6 rounded-xl bg-gradient-to-br from-background/80 to-background/40 backdrop-blur-xl border border-accent/20"
                >
                  <div className="w-12 h-12 bg-gradient-to-br from-accent to-accent-secondary rounded-lg flex items-center justify-center mb-4 glow">
                    <Icon className="w-6 h-6 text-background" />
                  </div>
                  <h3 className="text-xl font-semibold mb-3 text-text">{feature.title}</h3>
                  <p className="text-text-muted">{feature.description}</p>
                </motion.div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section className="py-20 relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <SectionTitle
            title="Our Team"
            subtitle="Built by experts in AI, physics, and strategic intelligence"
            center
          />
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {team.map((member, index) => (
              <motion.div
                key={member.name}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="p-6 rounded-xl bg-gradient-to-br from-background/80 to-background/40 backdrop-blur-xl border border-accent/20 text-center"
              >
                <div className="w-24 h-24 bg-gradient-to-br from-accent to-accent-secondary rounded-full flex items-center justify-center mx-auto mb-4 glow text-2xl font-bold text-background">
                  {member.placeholder}
                </div>
                <h3 className="text-xl font-semibold mb-2 text-text">{member.name}</h3>
                <p className="text-accent mb-3">{member.role}</p>
                <p className="text-text-muted text-sm">{member.bio}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 relative bg-gradient-to-b from-background/50 to-background">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="text-4xl font-bold mb-6 gradient-text">
              Ready to Transform Your Intelligence?
            </h2>
            <p className="text-xl text-text-muted mb-8">
              Join forward-thinking teams using Nexora to make better decisions faster.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <a
                href="/contact"
                className="px-8 py-4 bg-gradient-to-r from-accent to-accent-secondary text-background rounded-lg font-semibold text-lg hover:scale-105 transition-transform glow-accent"
              >
                Get Started
              </a>
              <a
                href="/briefs"
                className="px-8 py-4 border-2 border-accent/50 text-accent rounded-lg font-semibold text-lg hover:bg-accent/10 transition-colors"
              >
                View Briefs
              </a>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  );
}

