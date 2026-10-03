Para que **Lovable** (o plataformas similares como v0 de Vercel o Bolt.new) genere una web espectacular a la primera, no podemos darle solo una descripción vaga. Estas IAs "piensan" en componentes de React, clases de Tailwind CSS y librerías de animación (Framer Motion). Tenemos que traducir nuestra dirección de arte a **instrucciones de arquitectura frontend**.

Aquí tienes el **Super Prompt de Arquitectura Web** diseñado específicamente para pegarlo en Lovable. He incluido la paleta de colores, la estructura de componentes, el copy (textos) y los efectos visuales.

---

### CÓPIA Y PEGA ESTO EN LOVABLE:

**Context & Project Goal:**
Build a high-end, immersive, single-page landing page for **"C11-C Studio"**, a neuro-cognitive visual training engine. The engine generates deterministic MP4 videos (Visual Drills) based on complex mathematics to train human eye tracking, saccadic speed, and cognitive load management.

**Art Direction & Vibe:**
The aesthetic is "Clinical Cyberpunk" / "90s Sci-Fi Analog meets Modern UI". Think Ghost in the Shell or Alien's Nostromo computers, but polished for 2026.

* **Theme:** STRICTLY DARK MODE. Background should be absolute deep dark (`#030405` or `bg-slate-950`).
* **Color Palette:** Primary accents are pure Neon Cyan (`#00f0ff`), Toxic Green (`#00ff66`), and Warning Amber (`#ff5500`).
* **Typography:** Use a highly legible sans-serif for body text (e.g., Inter) and a rigid Monospace font (e.g., JetBrains Mono, Fira Code, or Space Mono) for headers, numbers, and UI data elements.
* **Visual Effects:** Use subtle CRT scanline overlays (via CSS patterns), glowing text effects (text-shadow), and sharp, angular borders (no highly rounded corners, use `rounded-sm` or `rounded-none`).

**Tech Stack Requirements:**
Use React, Tailwind CSS, Shadcn UI components, and Framer Motion for smooth scroll-reveal animations and micro-interactions. Use Lucide React for icons.

**Page Structure & Content:**

**1. Navbar:**

* Glassmorphism effect but very dark.
* Left: Logo text `<C11-C/> MK-IV`.
* Right: Links (The Drills, Engine Specs, Docs) and a glowing Cyan button "Launch Studio".

**2. Hero Section:**

* **Layout:** Centered, highly cinematic.
* **Visual:** Add a subtle animated background (like a slowly rotating CSS radar or a moving sine wave using SVG). Add a very subtle CSS CRT flicker/scanline overlay on this section.
* **Copy:**
* Eyebrow (Monospace, Amber): `SYS.INIT // COGNITIVE OVERLOAD DETECTED`
* Main H1: "Visual Loops Orchestrator." (Make it massive, maybe a slight CSS glitch effect on hover).
* Subtitle: "Deterministic mathematical drills to push foveal tracking and saccadic inhibition to the absolute human limit."
* Buttons: Primary (Solid Cyan, black text): "Initialize Engine", Secondary (Outline outline-cyan): "View Telemetry".



**3. The Mechanics Grid (The 4 Drills):**

* Section Title: `[ MODULES: ACTIVE ]`
* Use a 2x2 CSS Grid of Shadcn Cards. The cards should have a dark background, a very subtle cyan border that glows brighter on hover, and a monospace index number (e.g., `01`, `02`).
* **Card 1: TRACKING.** Icon: Activity/Wave. Text: "Harmonic Loom. Continuous tracking of parametric Lissajous trajectories under dynamic occlusion."
* **Card 2: SACCADE.** Icon: Crosshair/Target. Text: "Quantum Jumps. Discrete ballistic eye movements mapped to deterministic Poisson disk spatial distributions."
* **Card 3: PURSUIT.** Icon: Focus/Eye. Text: "Foveal Monolith. Absolute central focus maintenance against depth-of-field illusions and isokinetic modulation."
* **Card 4: PERIPHERAL SCAN.** Icon: Radar. Text: "Split Attention. Central anchor fixation while discriminating rhythm-asynchronous stimuli in the peripheral vision."

**4. The Engine Architecture (Code & Logic section):**

* **Layout:** Two columns.
* **Left Column (Copy):** "Deterministic to the core. Every video is generated via a Smart ID (e.g., PST-04-A7X9) that drives the procedural math. Zero randomness, 100% reproducible biometric challenges."
* **Right Column (Visual):** Create a mock "Terminal Window" UI. Black background, red/green/cyan monospace text typing out a fake JSON payload:
`{ "tracking_id": "PSC-03-M9V2", "logical_seed": 3918274615, "mechanics_active": ["QUADRANT_COUNTING", "ASYNCHRONOUS_RHYTHM"] }`

**5. Call to Action (Footer):**

* Minimalist, centered.
* Text: "Ready to test your limits?"
* Button: "Generate Challenge" (Amber color to make it pop).
* Bottom text (small, monospace): `c11-c visual drills // build: 2026.1 // system healthy`

**Animations & Micro-interactions:**

* Add hover effects to all buttons (invert colors or add a drop-shadow glow).
* Fade in the 4 Mechanic cards sequentially using Framer Motion when scrolling into view.
* Ensure the site is fully responsive, breaking down the 2x2 grid to a 1-column stack on mobile.

---

### ¿Por qué este prompt es infalible para Lovable?

1. **Le quita la "libertad creativa" peligrosa:** Lovable tiende a hacer webs muy "SaaS genérico" (blancas, redondeadas, con ilustraciones vectoriales genéricas). Al especificarle *Shadows, Monospace, Sharp borders, CRT flicker*, lo fuerzas a salir de su zona de confort y programar en modo Sci-Fi.
2. **Define la librería de UI:** Al pedirle que use **Shadcn UI** y **Tailwind**, garantizas que el código que genere sea moderno, modular y fácil de exportar o modificar luego si tu equipo quiere integrarlo en la herramienta real.
3. **JSON & Terminal Mockup:** A Lovable se le da increíblemente bien crear "falsas ventanas de código" (Code blocks). Esto le dará a la web un aspecto técnico y profesional (ideal para mostrar que el `ChallengeEngine` es un motor de software duro, no solo un juego).

Pégalo tal cual (en inglés lo procesan mucho mejor) y mira cómo construye el frontend en tiempo real. ¡Te va a generar una web brutal!