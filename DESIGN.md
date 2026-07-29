# DESIGN.md - Design System Specification for Quiz Exam System 2026

## 1. Visual Identity & Design Tokens

### Color Palette
- **Primary / Brand Accent**: `#4F46E5` (Indigo 600) -> `#6366F1` (Indigo 500)
- **Secondary Accent**: `#7C3AED` (Violet 600) -> `#8B5CF6` (Violet 500)
- **Success / Passed**: `#10B981` (Emerald 500) / `#D1FAE5` (Emerald 100)
- **Warning / Pending**: `#F59E0B` (Amber 500) / `#FEF3C7` (Amber 100)
- **Danger / Incorrect**: `#EF4444` (Rose 500) / `#FEE2E2` (Rose 100)
- **Surfaces**:
  - Light Background: `#F8FAFC` (Slate 50)
  - Card Background: `#FFFFFF` with `backdrop-filter: blur(16px)`
  - Surface Borders: `1px solid rgba(226, 232, 240, 0.8)` (Slate 200)

### Typography
- **Primary UI Font**: `Inter`, system-ui, -apple-system, sans-serif
- **Headings & Display**: `Outfit`, `Inter`, sans-serif
- **Timer & Mono Stats**: `ui-monospace`, `SFMono-Regular`, `Menlo`, monospace

### Scale & Spacing
- Container Max Width: `1200px` (Max-w-6xl)
- Card Padding: `1.5rem` (24px) / `2rem` (32px)
- Radius Tokens:
  - Small Elements (Buttons, Badges): `0.75rem` (12px - `rounded-xl`)
  - Containers & Modals: `1rem` (16px - `rounded-2xl`)

---

## 2. Component Guidelines

### Header & Navigation
- Backdrop Blur: `backdrop-filter: blur(12px)`
- Sticky top positioning with subtle `border-b border-slate-200/80`
- Animated trophy & admin access badges with subtle scale on hover

### Option Cards (Exam Room)
- Hover State: `transform: translateY(-2px)`, `border-color: #818CF8`, `background: #EEF2FF`
- Checked State: `border-color: #4F46E5`, `background: #EEF2FF`, bold font styling
- Micro-badge: Option letters A, B, C, D in indigo pills

### Leaderboard Podium
- Top 1 (Gold 🥇): Golden aura badge `#FEF3C7` with amber border
- Top 2 (Silver 🥈): Slate silver badge `#F1F5F9`
- Top 3 (Bronze 🥉): Warm bronze badge `#FFF7ED`

---

## 3. Micro-Interactions & Animation
- **Timer Ring**: Glowing pulse ring on active countdown
- **Question Flagging**: Interactive toggle with animation and navigator dot indicator
- **Button CTA**: Hover scale `scale-[1.01]`, shadow elevation `shadow-indigo-500/20`
