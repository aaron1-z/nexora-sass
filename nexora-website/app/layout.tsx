import type { Metadata } from "next";
import { Inter, DM_Sans } from "next/font/google";
import "./globals.css";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

const dmSans = DM_Sans({
  subsets: ["latin"],
  variable: "--font-dm-sans",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Nexora Intelligence Engine | AI-Powered Strategic Intelligence",
  description: "Transform data chaos into strategic clarity. Nexora delivers decision-grade Action Briefs for analysts, strategists, and investors through AI-powered intelligence automation.",
  keywords: "AI intelligence, strategic intelligence, market intelligence, action briefs, real-time alerts, AI reasoning, business intelligence",
  authors: [{ name: "Nexora Intelligence" }],
  openGraph: {
    title: "Nexora Intelligence Engine | AI-Powered Strategic Intelligence",
    description: "Transform data chaos into strategic clarity. Nexora delivers decision-grade Action Briefs for analysts, strategists, and investors.",
    type: "website",
    locale: "en_US",
  },
  twitter: {
    card: "summary_large_image",
    title: "Nexora Intelligence Engine",
    description: "Transform data chaos into strategic clarity with AI-powered strategic intelligence.",
  },
  robots: {
    index: true,
    follow: true,
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.variable} ${dmSans.variable} antialiased`}>
        <Navbar />
        <main className="min-h-screen">{children}</main>
        <Footer />
      </body>
    </html>
  );
}

