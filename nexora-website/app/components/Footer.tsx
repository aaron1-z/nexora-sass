import Link from "next/link";
import { Linkedin, Twitter, Github, Mail } from "lucide-react";

export default function Footer() {
  const currentYear = new Date().getFullYear();

  const footerLinks = {
    product: [
      { href: "/about", label: "About" },
      { href: "/contact", label: "Contact" },
    ],
    company: [
      { href: "/about", label: "Our Mission" },
      { href: "/contact", label: "Get in Touch" },
    ],
  };

  const socialLinks = [
    { href: "https://linkedin.com/company/nexora", icon: Linkedin, label: "LinkedIn" },
    { href: "https://twitter.com/nexora", icon: Twitter, label: "Twitter" },
    { href: "https://github.com/nexora", icon: Github, label: "GitHub" },
    { href: "mailto:hello@nexora.ai", icon: Mail, label: "Email" },
  ];

  return (
    <footer className="bg-background border-t border-accent/10 mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="col-span-1 md:col-span-2">
            <Link href="/" className="flex items-center space-x-2 mb-4">
              <div className="w-8 h-8 bg-gradient-to-br from-accent to-accent-secondary rounded-lg flex items-center justify-center">
                <span className="text-background font-bold">N</span>
              </div>
              <span className="text-xl font-bold gradient-text">Nexora</span>
            </Link>
            <p className="text-text-muted text-sm mb-4 max-w-md">
              Transforming data chaos into strategic clarity. AI-powered intelligence
              for decision-makers.
            </p>
            <div className="flex space-x-4">
              {socialLinks.map((social) => {
                const Icon = social.icon;
                return (
                  <a
                    key={social.label}
                    href={social.href}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="w-10 h-10 rounded-lg bg-gradient-to-br from-accent/20 to-accent-secondary/20 flex items-center justify-center text-text/60 hover:text-accent hover:scale-110 transition-transform"
                    aria-label={social.label}
                  >
                    <Icon className="w-5 h-5" />
                  </a>
                );
              })}
            </div>
          </div>

          {/* Product Links */}
          <div>
            <h3 className="text-text font-semibold mb-4">Product</h3>
            <ul className="space-y-2">
              {footerLinks.product.map((link) => (
                <li key={link.href}>
                  <Link
                    href={link.href}
                    className="text-text-muted hover:text-accent transition-colors text-sm"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Company Links */}
          <div>
            <h3 className="text-text font-semibold mb-4">Company</h3>
            <ul className="space-y-2">
              {footerLinks.company.map((link) => (
                <li key={link.href}>
                  <Link
                    href={link.href}
                    className="text-text-muted hover:text-accent transition-colors text-sm"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-accent/10 flex flex-col md:flex-row justify-between items-center">
          <p className="text-text-muted text-sm">
            © {currentYear} Nexora Intelligence. All rights reserved.
          </p>
          <p className="text-text-muted text-sm mt-2 md:mt-0">
            Powered by{" "}
            <span className="gradient-text font-semibold">Nexora Engine</span>
          </p>
        </div>
      </div>
    </footer>
  );
}

