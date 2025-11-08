import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "About Nexora | AI-Powered Strategic Intelligence",
  description: "Built by physicists and AI engineers to make sense of the world's information. Learn about Nexora's mission, team, and technology.",
};

export default function AboutLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <>{children}</>;
}

