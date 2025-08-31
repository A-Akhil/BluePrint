## **1. MVP Vision**

**Goal:** Make the frontend **look fully functional and research-grade**, simulating a real deep-sea eDNA analysis pipeline using your ZHNSW/ANN logic—but without backend computation.

**Key Points:**

* Interactive, responsive, professional UI.
* Data-driven feel with charts, tables, and metrics.
* “Simulated intelligence” for taxonomic assignment, abundance, and novelty detection.
* Minimal technical debt: all logic runs in the browser with mock data.

---

## **2. Tech Stack (Frontend-Only, Production-Style)**

* **Framework:** React.js (functional components with hooks)
* **UI Library:** TailwindCSS for styling + HeadlessUI for components (modals, tabs, dropdowns)
* **Charts:** Recharts + D3.js (for advanced visualizations like cluster plots)
* **Routing:** React Router or Next.js (if you want multiple pages)
* **State Management:** React Context API + Zustand (lightweight)
* **Mock Data:** JSON files simulating sequence embeddings, taxa, abundance, and diversity metrics
* **Extras:**

  * Tooltips and modals for metadata on sequences
  * Download buttons (CSV/Excel) for results
  * Dark/light mode toggle for visual polish

---

## **3. Core MVP Features**

### **A. Landing Page**

* Project name: “DeepSea eDNA Biodiversity Explorer”
* Hero section: Image of deep sea + short description of eDNA & ZHNSW
* Buttons:

  * “Upload Sample” (simulate file upload)
  * “View Demo Analysis” (loads pre-populated mock results)
* Optional: Animated info panels for “Speed” and “Novelty Detection”

---

### **B. Analysis Page**

**1. Sequence Table**

* Columns:

  * Sequence ID
  * Predicted Taxon
  * Confidence Score (progress bar)
  * Novelty Flag (icon or colored tag)
  * Functional Role (optional: Protist, Metazoan, etc.)
* Interactive:

  * Search by taxon
  * Sort by confidence or novelty
  * Pagination for large datasets

**2. Abundance Visualization**

* Bar chart or pie chart of top taxa
* Hover tooltip showing counts
* Filters by taxon type or novelty

**3. Biodiversity Metrics**

* Cards showing:

  * Shannon Index
  * Simpson Index
  * Total sequences analyzed
* Optional: Small trend graphs (if you want “sample over time” simulation)

**4. Novelty Visualization**

* Scatterplot / t-SNE style chart:

  * Known taxa in one color
  * Novel sequences in another color
  * Hover shows sequence ID + taxon
* Interactive zoom/pan for realism

**5. Download & Export**

* Button to export:

  * CSV of sequence table
  * PDF summary of charts & metrics

**6. Optional: Map / Sampling Location**

* World map with pins for sample sites (simulated)
* Clicking a pin shows mock analysis summary

---

## **4. Mock Data Structure**

```json
{
  "sequences": [
    {"id":"seq001","taxon":"Protista sp.","confidence":0.92,"novel":false,"type":"Protist"},
    {"id":"seq002","taxon":"Cnidaria sp.","confidence":0.85,"novel":false,"type":"Cnidarian"},
    {"id":"seq003","taxon":"Unknown deep-sea eukaryote","confidence":0.45,"novel":true,"type":"Unknown"}
  ],
  "abundance": [
    {"taxon":"Protista sp.","count":120},
    {"taxon":"Cnidaria sp.","count":80},
    {"taxon":"Unknown deep-sea eukaryote","count":50}
  ],
  "diversity": {
    "shannon_index":2.35,
    "simpson_index":0.78,
    "total_sequences":250
  },
  "locations": [
    {"site":"Abyssal Plain 1","lat":-35.2,"lon":142.1},
    {"site":"Seamount X","lat":-12.3,"lon":150.4}
  ]
}
```

---

## **5. Frontend Flow**

1. **Landing page → Upload sample or Demo**
2. **Load mock JSON**

   * Optional: Animate “Analyzing sample…”
3. **Render analysis page**:

   * Sequence table with search/filter
   * Top taxa charts
   * Biodiversity metrics cards
   * Novel taxa scatterplot
   * Sample map with site info
4. **User interactions:**

   * Search/filter
   * Hover tooltips
   * Download results
   * Toggle dark/light mode

---

## **6. UI/UX Polishing for Screening Test**

* Clean, minimal, scientific feel: use navy/teal colors, clean fonts (Inter, Roboto).
* Tooltips on all metrics explaining what they mean.
* Animations for charts (Recharts supports smooth transitions).
* Responsive design (mobile + desktop).
* Optional sidebar with “About ZHNSW / Pipeline” to show your algorithm knowledge.

---

## **7. Developer LLM Prompt (Supercharged)**

Feed this to an LLM to generate your frontend MVP:

```
I want to build a **frontend MVP** for a deep-sea eDNA biodiversity project. 
Requirements:

1. Tech stack: React.js (functional components), TailwindCSS, Recharts/D3.js, React Router.
2. Landing page with project name, hero image, description, buttons: 'Upload Sample' and 'View Demo Analysis'.
3. Analysis page:
   - Table of sequences: Sequence ID, Predicted Taxon, Confidence (progress bar), Novelty Flag, Type
   - Abundance chart: bar/pie chart of top taxa
   - Biodiversity metrics: Shannon index, Simpson index, Total sequences
   - Novelty visualization: scatterplot with known vs novel sequences
   - Interactive search/filter and pagination
   - Download CSV/PDF buttons
   - Optional map showing sampling sites
4. Use **mock JSON data** to simulate backend:
{
  "sequences": [...],
  "abundance": [...],
  "diversity": {...},
  "locations": [...]
}
5. Responsive design, professional scientific UI, tooltips on metrics, smooth chart animations.
6. Generate complete React component code, including layout, charts, table, mock data handling, filters, and styling.

Make it **production-like**, fully functional in browser without backend.
```
