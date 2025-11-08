import { getAllBriefs, getAllTags } from "@/lib/markdown";
import BriefsClient from "./BriefsClient";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Research & Briefs | Nexora Intelligence",
  description: "Strategic intelligence reports and analysis briefs. Explore our collection of AI-generated Action Briefs on technology, markets, and trends.",
};

export default function BriefsPage() {
  const briefs = getAllBriefs();
  const tags = getAllTags();

  return <BriefsClient initialBriefs={briefs} initialTags={tags} />;
}
