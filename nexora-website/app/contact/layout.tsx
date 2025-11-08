import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Contact Nexora | Get in Touch",
  description: "Reach out to the Nexora team. Let's discuss how intelligence automation can transform your decision-making.",
};

export default function ContactLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <>{children}</>;
}

