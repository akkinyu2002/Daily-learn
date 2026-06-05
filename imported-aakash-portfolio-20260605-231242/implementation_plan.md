# Aakash Nyupane Portfolio Website

Build a premium, human-crafted portfolio website that positions Aakash as a Video Editor, Graphic Designer, and Creative Technologist. Design inspired by Linear, Raycast, Framer — minimal, professional, interactive, fast.

## User Review Required

> [!IMPORTANT]
> **Tailwind CSS version**: Your PRD specifies Tailwind CSS. I'll use **Tailwind CSS v4** (latest, ships with Next.js 15). Please confirm this is OK or if you prefer v3.

> [!IMPORTANT]
> **Resend API Key**: The contact form requires a Resend API key. For now, I'll build the form with full validation and wire it to a server action that you can connect to Resend later by adding your API key to `.env.local`.

> [!WARNING]
> **No real project images/videos available**: Your GitHub repos and portfolio don't have downloadable media assets. I'll use **placeholder image components** with proper dimensions that you can replace with your actual project screenshots, thumbnails, and videos. The structure will be ready for drop-in replacement.

## Open Questions

> [!IMPORTANT]
> **GitHub username**: Your portfolio links to `neupaneakas` for some repos and your actual GitHub appears to be `akkinyu2002`. Which should I use for project links?

> [!IMPORTANT]
> **Resume PDF**: Should the Resume button link to a downloadable PDF (like your current site), or open a page? I'll default to a download link placeholder.

## Research Summary

**Current portfolio** (neupaneaakash.com.np): Static HTML/CSS/JS, single page, uses Outfit font, blob hero, 3 projects shown.

**GitHub** (akkinyu2002): 42 repos. Notable projects for the portfolio:
- Portfolio Website (HTML/CSS/JS, hosted)
- Hostel Mess Management (Android Studio, C#, SQL)
- Graphic Design Portfolio (Photoshop, Illustrator, Branding)
- 3D-port, Landing-page, Nursery-Website, Pomodoro, Expense tracker, Todo app

**Social links**:
- LinkedIn: linkedin.com/in/aakash-nyupane-4bb97031a
- Behance: behance.net/akashneupane5
- Instagram: @theskynyupane
- Phone: +977 9860212330
- Location: Nepal

---

## Design System

### Philosophy
- **No AI aesthetic** — no particles, neon, glassmorphism, cyberpunk
- **Inspired by**: Linear (clean typography), Raycast (dark mode elegance), Framer (micro-interactions), Notion (content-first)
- **Color palette**: Warm neutral base with a single accent color (indigo/slate tone)
- **Typography**: Inter (headings + body), monospace for code/tags
- **Spacing**: Generous whitespace, 8px grid system
- **Motion**: Subtle, purposeful — entrance animations, hover states, page transitions. No flashy effects.

### Theme
- Light mode: Off-white backgrounds (#FAFAFA), dark text (#0A0A0A)
- Dark mode: Deep charcoal (#0A0A0A), light text (#FAFAFA)
- Accent: Indigo (#4F46E5) for CTAs, links, highlights
- System preference detection with manual override

---

## Proposed Changes

### Phase 1: Project Setup & Design System

#### [NEW] Next.js 15 project initialization
- Initialize with `npx -y create-next-app@latest ./` using TypeScript, Tailwind CSS, App Router, src/ directory
- Install dependencies: `framer-motion`, `@radix-ui/react-*` (via shadcn), `lucide-react`, `resend`
- Configure `shadcn/ui` components

#### [NEW] `src/app/globals.css`
- CSS custom properties for the design system
- Tailwind v4 theme configuration
- Custom utility classes for animations
- Typography scale

#### [NEW] `src/lib/fonts.ts`
- Inter font configuration via `next/font/google`

#### [NEW] `tailwind.config.ts`
- Extended theme with custom colors, spacing, animations
- Custom keyframes for subtle entrance animations

---

### Phase 2: Global Layout & Navigation

#### [NEW] `src/components/layout/navbar.tsx`
- Sticky navigation with transparent-on-top, solid-on-scroll behavior
- Logo: "Aakash" with accent dot
- Links: Work, Services, About, Contact
- Buttons: Resume (download), Hire Me (links to contact)
- Mobile hamburger menu with Framer Motion slide
- Theme switcher (light/dark/system)

#### [NEW] `src/components/layout/footer.tsx`
- Clean footer with social links (LinkedIn, Behance, Instagram, GitHub)
- Quick navigation links
- Copyright notice

#### [NEW] `src/components/layout/scroll-progress.tsx`
- Thin progress bar at top of page
- Uses scroll position calculation

#### [NEW] `src/app/layout.tsx`
- Root layout with Navbar, Footer, scroll progress
- Theme provider (next-themes)
- Metadata, Open Graph, structured data
- Smooth page transitions wrapper

---

### Phase 3: Home Page (All Sections)

#### [NEW] `src/app/page.tsx`
- Home page assembling all sections below

#### [NEW] `src/components/home/hero.tsx`
- Two-column layout
- Left: Name, title roles, description, CTA buttons
- Right: Auto-rotating showcase cards (Video Editing, Thumbnail Design, Social Media Graphics, Web Projects) with smooth fade transitions
- Entrance animations with Framer Motion

#### [NEW] `src/components/home/tools-section.tsx`
- "Tools I Work With" grid
- Monochrome SVG icons for: CapCut, Premiere Pro, After Effects, Photoshop, Illustrator, Figma, ChatGPT, Claude, Notion
- Subtle hover effects

#### [NEW] `src/components/home/featured-work.tsx`
- "Selected Projects" — 6 project cards
- Card: cover image placeholder, project name, category tag, short description
- Hover: slight lift + soft shadow
- Links to Work page / project detail

#### [NEW] `src/components/home/video-showcase.tsx`
- Tabbed sections: Short Form / Long Form
- Video cards with placeholder thumbnails, duration badge, category tag
- Hover-to-play behavior (placeholder for now, ready for video embeds)

#### [NEW] `src/components/home/thumbnail-gallery.tsx`
- Masonry grid layout
- Hover zoom effect
- Before/After toggle placeholder
- Fullscreen lightbox view
- Category filters: YouTube, Business, Social Media

#### [NEW] `src/components/home/services-preview.tsx`
- 3 service cards: Video Editing, Graphic Design, AI Content Systems
- Each with icon, description, deliverables list
- Link to full Services page

#### [NEW] `src/components/home/process-section.tsx`
- Timeline design: Discovery → Planning → Creation → Delivery
- Each step: number, title, description
- Animated timeline connector

#### [NEW] `src/components/home/about-preview.tsx`
- Photo placeholder + short intro text
- Highlights: IT Background, AI Knowledge, Creative Editing, Graphic Design
- "Read Full Story" button → About page

#### [NEW] `src/components/home/testimonials.tsx`
- Empty placeholder component
- Card layout ready for: photo, name, role, testimonial
- Message: "Testimonials coming soon" — no fake quotes

#### [NEW] `src/components/home/metrics-section.tsx`
- Animated counters: 50+ Projects, 100+ Videos, 1M+ Views, 3 Languages
- Count-up animation on scroll into view

#### [NEW] `src/components/home/cta-section.tsx`
- "Have a project in mind?"
- Two buttons: Start a Project, Contact Me

---

### Phase 4: Work Page

#### [NEW] `src/app/work/page.tsx`
- All projects displayed
- Filter buttons: Video Editing, Graphic Design, Web Design, AI Projects
- Search bar
- Project grid with cards

#### [NEW] `src/components/work/project-modal.tsx`
- Modal/sheet for project details
- Sections: Challenge, Process, Tools Used, Outcome
- Close button, smooth open/close animation

#### [NEW] `src/lib/data/projects.ts`
- Project data array with real project info from GitHub:
  1. Portfolio Website (Web Design) — HTML/CSS/JS
  2. Hostel Mess Management (App Dev) — Android Studio, C#, SQL
  3. Graphic Design Portfolio (Graphic Design) — Photoshop, Illustrator
  4. Nursery Website (Web Design) — HTML/CSS
  5. Landing Page (Web Design) — HTML/CSS/JS
  6. 3D Portfolio (Web Design) — Three.js
- Plus placeholder slots for video editing and AI projects

---

### Phase 5: Services Page

#### [NEW] `src/app/services/page.tsx`
- Detailed breakdown of 3 service areas
- Each with: description, deliverables, process, pricing tiers
- Pricing: Starter / Standard / Custom (inquiry only, no checkout)
- CTA to contact for each service

---

### Phase 6: About Page

#### [NEW] `src/app/about/page.tsx`
- Sections: Story, Education, Skills, Tools (visual grid), Fun Facts
- Personal journey narrative
- Diploma in IT mention
- Skills grid: Video Editing, Graphic Design, UI Design, AI Tools, Web Development
- Fun facts: humanizing section

---

### Phase 7: Contact Page

#### [NEW] `src/app/contact/page.tsx`
- Clean form: Name, Email, Project Type (dropdown), Budget (range), Message
- Client-side validation
- Animated success state

#### [NEW] `src/app/api/contact/route.ts`
- Server action for form submission
- Resend integration (with env variable check)
- Rate limiting placeholder

---

### Phase 8: Advanced Features

#### [NEW] `src/components/command-palette.tsx`
- CTRL+K shortcut
- Search across projects, services, pages
- Framer Motion animated overlay
- Keyboard navigation

#### [NEW] `src/components/ui/theme-switcher.tsx`
- Light / Dark / System toggle
- Uses next-themes

#### [NEW] `src/components/page-transition.tsx`
- Framer Motion AnimatePresence wrapper
- Fast, subtle fade+slide transitions

---

### Phase 9: SEO & Metadata

#### [MODIFY] `src/app/layout.tsx`
- Comprehensive metadata: title templates, descriptions, OG images
- Structured data (JSON-LD) for Person schema
- Canonical URLs

#### [NEW] `src/app/sitemap.ts`
- Auto-generated sitemap

#### [NEW] `src/app/robots.ts`
- Robots.txt configuration

---

## Project Data (From GitHub Research)

| # | Project Name | Category | Tech Stack | Description |
|---|-------------|----------|------------|-------------|
| 1 | Portfolio Website | Web Design | HTML, CSS, JS | Personal portfolio showcasing skills and work |
| 2 | Hostel Mess Management | App Development | Android Studio, C#, SQL | Mobile and Windows app for hostel mess operations |
| 3 | Graphic Design Portfolio | Graphic Design | Photoshop, Illustrator | Logos, posters, social media visuals |
| 4 | Nursery Website | Web Design | HTML, CSS | Website for a nursery business |
| 5 | Landing Page | Web Design | HTML, CSS, JS | Marketing landing page |
| 6 | 3D Portfolio | Web Design | Three.js, HTML | 3D interactive portfolio experiment |

---

## File Structure

```
src/
├── app/
│   ├── layout.tsx
│   ├── page.tsx              # Home
│   ├── globals.css
│   ├── sitemap.ts
│   ├── robots.ts
│   ├── work/
│   │   └── page.tsx
│   ├── services/
│   │   └── page.tsx
│   ├── about/
│   │   └── page.tsx
│   ├── contact/
│   │   └── page.tsx
│   └── api/
│       └── contact/
│           └── route.ts
├── components/
│   ├── layout/
│   │   ├── navbar.tsx
│   │   ├── footer.tsx
│   │   └── scroll-progress.tsx
│   ├── home/
│   │   ├── hero.tsx
│   │   ├── tools-section.tsx
│   │   ├── featured-work.tsx
│   │   ├── video-showcase.tsx
│   │   ├── thumbnail-gallery.tsx
│   │   ├── services-preview.tsx
│   │   ├── process-section.tsx
│   │   ├── about-preview.tsx
│   │   ├── testimonials.tsx
│   │   ├── metrics-section.tsx
│   │   └── cta-section.tsx
│   ├── work/
│   │   └── project-modal.tsx
│   ├── command-palette.tsx
│   ├── page-transition.tsx
│   └── ui/
│       ├── theme-switcher.tsx
│       └── ... (shadcn components)
├── lib/
│   ├── data/
│   │   └── projects.ts
│   ├── fonts.ts
│   └── utils.ts
└── types/
    └── index.ts
```

---

## Verification Plan

### Automated Tests
- `npm run build` — ensure zero build errors
- `npm run lint` — ESLint passes
- Manual Lighthouse audit target: 95+ on Performance, Accessibility, SEO

### Manual Verification
- Run `npm run dev` and verify all 5 pages render correctly
- Test theme switching (light/dark/system)
- Test command palette (Ctrl+K)
- Test responsive design at mobile (375px), tablet (768px), desktop (1440px)
- Test all navigation links work
- Test contact form validation
- Verify smooth animations and page transitions
- Check keyboard navigation and focus states

---

## Execution Order

1. **Phase 1**: Project setup, install deps, design system → ~foundation
2. **Phase 2**: Layout (navbar, footer, scroll progress) → ~navigation
3. **Phase 3**: Home page (all 11 sections) → ~core content
4. **Phase 4**: Work page + project modal → ~portfolio
5. **Phase 5**: Services page → ~services
6. **Phase 6**: About page → ~personal
7. **Phase 7**: Contact page + API → ~conversion
8. **Phase 8**: Command palette, theme switcher, transitions → ~polish
9. **Phase 9**: SEO, sitemap, robots → ~discoverability
