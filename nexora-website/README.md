# Nexora Intelligence Engine - Marketing Website

A premium Next.js 14 marketing website for Nexora Intelligence Engine, designed for investors, clients, and enterprise leads.

## 🚀 Features

- **Modern Design**: Dark mode with gradient neon lines, animated particles, and smooth section transitions
- **Responsive**: Fully responsive design that works on all devices
- **Performance**: Optimized for speed with Next.js 14 App Router
- **SEO Ready**: Comprehensive meta tags and structured data
- **Animations**: Smooth animations powered by Framer Motion
- **Content Management**: Markdown-based briefs system
- **Contact Forms**: Functional contact form with API route

## 🛠️ Tech Stack

- **Next.js 14** (App Router)
- **TypeScript**
- **Tailwind CSS 3**
- **Framer Motion** (animations)
- **React Markdown** (markdown rendering)
- **Lucide React** (icons)

## 📦 Installation

1. Install dependencies:
```bash
npm install
```

2. Run the development server:
```bash
npm run dev
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser.

## 🏗️ Project Structure

```
nexora-website/
├── app/
│   ├── layout.tsx           # Root layout with metadata
│   ├── page.tsx             # Landing page
│   ├── about/
│   │   └── page.tsx         # About page
│   ├── contact/
│   │   └── page.tsx         # Contact page
│   ├── briefs/
│   │   ├── page.tsx         # Briefs listing page
│   │   ├── BriefsClient.tsx # Client component for briefs
│   │   └── [slug]/
│   │       └── page.tsx     # Individual brief page
│   ├── api/
│   │   └── contact/
│   │       └── route.ts     # Contact form API route
│   ├── components/
│   │   ├── Navbar.tsx
│   │   ├── Footer.tsx
│   │   ├── Hero.tsx
│   │   ├── FeatureCard.tsx
│   │   ├── BriefCard.tsx
│   │   ├── CTASection.tsx
│   │   ├── AnimatedBackground.tsx
│   │   └── SectionTitle.tsx
│   └── globals.css
├── lib/
│   └── markdown.ts          # Markdown utility functions
├── public/
│   └── posts/               # Markdown briefs
└── package.json
```

## 📝 Adding New Briefs

1. Create a new markdown file in `public/posts/`
2. Add frontmatter with title, excerpt, date, and tags:
```markdown
---
title: "Your Brief Title"
excerpt: "Brief description"
date: "2025-01-20"
tags: ["Tag1", "Tag2"]
---

Your markdown content here...
```

3. The brief will automatically appear on the briefs page

## 🚀 Deployment

### Deploy to Vercel (Recommended)

1. Push your code to GitHub:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main
```

2. Import your repository in [Vercel](https://vercel.com):
   - Go to https://vercel.com/new
   - Import your GitHub repository
   - Vercel will automatically detect Next.js and configure the build
   - Click "Deploy"

3. Your site will be live at `https://your-project.vercel.app`

### Environment Variables

No environment variables are required for basic functionality. For production contact form integration, you may want to add:
- Email service API keys (Resend, SendGrid, etc.)

To add environment variables in Vercel:
1. Go to your project settings
2. Navigate to "Environment Variables"
3. Add your API keys
4. Redeploy your application

### Building for Production

```bash
npm run build
npm start
```

This will create an optimized production build in the `.next` folder.

## 🎨 Customization

### Colors

Edit `tailwind.config.ts` to customize the color scheme:
- `background`: Main background color
- `accent`: Primary accent color
- `accent-secondary`: Secondary accent color
- `text`: Main text color
- `text-muted`: Muted text color

### Fonts

Fonts are configured in `app/layout.tsx`. Currently using:
- **Inter**: Headings
- **DM Sans**: Body text

## 📄 License

Copyright © 2025 Nexora Intelligence. All rights reserved.

## 🤝 Support

For questions or support, contact hello@nexora.ai

