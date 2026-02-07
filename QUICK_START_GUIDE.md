# 🚀 Enhanced Workforce Intelligence Dashboard - Quick Start Guide

## Installation & Setup

### Step 1: Install Core Dependencies
```bash
cd "/home/julius/Capstone DS4"

# Install required packages
pip install streamlit pandas numpy plotly altair

# Optional: For full export capabilities (PDF + Excel)
pip install reportlab openpyxl
```

### Step 2: Launch the Dashboard
```bash
streamlit run SGJOB_Dashboard.py
```

The dashboard will open in your default browser at `http://localhost:8501`

---

## 🎯 What's New in Version 2.0

### ✨ Enhanced Features

| Feature | Description | Benefit |
|---------|-------------|---------|
| **Sankey Diagrams** | Skill progression visualization | See career pathways clearly |
| **Moving Average Trends** | Predictive overlay on job data | Forecast market movements |
| **90th Percentile Matching** | Advanced recommendation engine | Data-driven salary negotiations |
| **Multi-Format Export** | CSV, Excel, PDF downloads | Share reports professionally |
| **Collapsible Filters** | Organized sidebar sections | Cleaner, less overwhelming UI |
| **Persona-Specific KPIs** | Customized metrics per user | Relevant data at a glance |
| **Skills Distribution Chart** | Market demand visualization | Identify emerging skills |
| **Trend Analysis Tab** | Flexible trend exploration | Deep-dive analytics |

---

## 👥 Using Each Persona

### 🎓 For Job Seekers (Individual)

**What You'll See:**
1. **Your Profile** - Enter current skills and target salary
2. **Career Roadmap** - Sankey diagram showing progression paths
3. **Upskill Opportunities** - Specific skills to learn with salary impact
4. **Growth Sectors** - Industries aligned with your skills
5. **Salary Trends** - How different sectors compensate

**How to Use:**
```
1. Select "Individual" from sidebar
2. Enter your skills: Python, SQL, Cloud (examples)
3. Set target salary: SGD 7,000/month
4. View recommended upskilling pathways
5. Download PDF with personalized recommendations
```

**Key Insight:** "Learn Cloud to unlock SGD 2,500 salary increase"

---

### 🏛️ For Government (Government Agency)

**What You'll See:**
1. **Labor Shortage Index** - Critical shortage areas highlighted
2. **Employment Heatmap** - Hiring patterns by sector over time
3. **Trend Analysis** - Moving average forecasting
4. **Sector Statistics** - Comprehensive industry breakdown
5. **Multi-Format Reports** - Excel, PDF, CSV exports

**How to Use:**
```
1. Select "Government Agency" from sidebar
2. Adjust "Focus on High-Shortage Sectors" slider
3. Monitor top 5 shortage areas (🔴 🟡 🟢 indicators)
4. Analyze 3-month trend overlay for forecasting
5. Export full intelligence report in Excel/PDF
```

**Key Insight:** "Healthcare sector shortage index: 78 (Critical)"

---

### 💼 For Recruiters (Recruiter)

**What You'll See:**
1. **Talent Pool Metrics** - Open positions by sector
2. **Hiring Velocity** - Top companies with most openings
3. **Salary Benchmarks** - Box & whisker charts by position level
4. **Skill Demand** - Top 10 in-demand skills heatmap
5. **Competitive Landscape** - Top 12 hiring competitors

**How to Use:**
```
1. Select "Recruiter" from sidebar
2. Review "High-Velocity Talent Pools" chart
3. Benchmark salaries for Software Engineer roles
4. Identify emerging skills (Cloud, AI/ML)
5. Track competitor hiring activity
6. Export recruitment intelligence data
```

**Key Insight:** "Finance sector has 450 open positions, avg salary SGD 6,500"

---

## 📊 Key Features Explained

### Sankey Diagram (Individual View)
```
Your Skills (Blue) 
    ↓
    → Emerging Skills (Green)
    ↓
    → Growth Sectors (Orange)
```
**Shows:** How your current skills connect to job opportunities

---

### Moving Average Trend (Government View)
```
Actual Line (Blue)     = Real job posting numbers
MA Line (Green)        = 3-month smoothed trend
Confidence Band (Gray) = ±15% range for forecasting
```
**Shows:** Trend direction without daily noise

---

### Labor Shortage Index (Government View)
**Calculation Formula:**
```
Score = (40% Volume) + (20% Views) + (30% Apps) + (20% Salary)
Range: 0 (Excess Supply) → 100 (Critical Shortage)
```
**Colors:**
- 🔴 Red (70-100): Critical shortage
- 🟡 Yellow (50-70): Moderate shortage  
- 🟢 Green (0-50): Adequate supply

---

### Skill Gap Premium (Individual View)
**What it means:**
```
Example: "Learning Cloud could increase salary by SGD 2,500"

This is based on:
- 90th percentile salary for Cloud jobs: SGD 9,500
- Your target salary: SGD 7,000
- Potential increase: SGD 2,500
```

---

## 🔍 Sidebar Filters

### Universal Filters (All Personas)
- **Time Period:** Select years to analyze
- **Industry Sectors:** Choose 1 or more sectors
- **Employment Type:** Filter by Full-time, Part-time, etc.

### Individual-Specific
- **Your Current Skills:** Multi-select from 9 skills
- **Target Salary:** Slider SGD 1,000 - 15,000
- **Preferred Role:** Analyst, Developer, Engineer, Manager, Any

### Government-Specific
- **Shortage Sensitivity:** 0.0 (less focus) to 1.0 (high focus)
- **Export Format:** CSV, Excel, or PDF preferred

### Recruiter-Specific
- **Focus Area:** High Growth, High Salary, High Volume, Emerging Skills
- **Minimum Vacancies:** Filter by posting size

---

## 📥 Exporting Data

### CSV Export
✅ **Always Available**
- Lightweight format
- Compatible with Excel, Python, R
- Includes: Job title, company, salary, level, sector

### Excel Export
✅ **If openpyxl installed** (`pip install openpyxl`)
- 3 sheets: Summary, Sector Analysis, Job Listings
- Professional formatting and styling
- Auto-width columns

### PDF Export
✅ **If reportlab installed** (`pip install reportlab`)
- Executive summary page
- Sector breakdown table
- Professional typography
- Print-ready format

---

## 🎨 Dark Mode Features

All visualizations automatically styled with:
- **Dark blue background** (#0f1419)
- **High-contrast text** (#e0e7ff)
- **Gradient cards** with subtle shadows
- **Color-coded metrics** (green=good, orange=caution, red=critical)

No manual color selection needed - everything matches the theme!

---

## ⚡ Performance Tips

1. **First Load:** Give it 5-10 seconds to load the CSV (cached after)
2. **Filtering:** Use sidebar filters to reduce data before viewing charts
3. **Large Exports:** Excel/PDF generation for 100k+ records may take 30 seconds
4. **Browser:** Use Chrome or Firefox for best performance

---

## 🐛 Troubleshooting

### Dashboard Won't Load
```bash
# Ensure Python 3.8+
python --version

# Reinstall core packages
pip install --upgrade streamlit pandas plotly
```

### Charts Not Displaying
```bash
# Check if Plotly renders (needs JavaScript)
# Try refreshing browser (Ctrl+R or Cmd+R)
# Clear cache: Press "R" in terminal or delete .streamlit folder
```

### PDF/Excel Export Unavailable
```bash
# Install optional dependencies
pip install reportlab openpyxl
# Restart dashboard (Ctrl+C then streamlit run...)
```

### Data Too Large / Out of Memory
```bash
# Reduce dataset with sidebar filters first
# Or increase system memory available to Streamlit
```

---

## 📈 Example Use Cases

### Individual: Career Planning
```
1. I'm a Python developer earning SGD 5,000/month
2. I select "Python" as current skill
3. Dashboard shows: "Learn Cloud for +SGD 2,500 potential"
4. I see Finance sector has 150 Cloud engineer roles at SGD 7,500
5. I download PDF report to discuss with mentor
```

### Government: Policy Planning
```
1. Sector: Information Technology
2. I notice shortage index trending to 85 (Critical)
3. Moving average shows no recovery in next 3 months
4. I export detailed sector report to brief policy team
5. Decision: Increase tech immigration quotas
```

### Recruiter: Hiring Strategy
```
1. I see Healthcare sector has 320 open positions
2. Highest paid is Manager level (SGD 8,000 avg)
3. Top in-demand skill is "Cloud" (appearing in 45% of listings)
4. Top competitor is Hospital Corp (40 openings)
5. I adjust salary offer to SGD 7,800 to be competitive
```

---

## 📱 Responsive Design

Dashboard automatically adjusts for:
- **Wide Monitors:** 4-column layouts
- **Laptops:** 2-column layouts
- **Tablets:** Single column with scroll
- **Mobile:** Stacked vertical layout

All visualizations are interactive - try hovering, clicking, zooming!

---

## 🔐 Data & Privacy

- **No data leaves your server** - All processing local
- **No cloud uploads** - Fully self-contained
- **No tracking** - No telemetry sent
- **Full control** - You decide what to export

---

## 📞 Quick Help

| Question | Answer |
|----------|--------|
| How do I change personas? | Select from radio buttons in sidebar |
| Can I filter by multiple sectors? | Yes - use multi-select checkboxes |
| How is salary potential calculated? | 90th percentile of earners with that skill |
| What's the moving average? | 3-month smoothed trend line |
| Can I export without installing Excel libs? | Yes - CSV always works |

---

## 🎓 Advanced Features

### Custom Trend Analysis
```
In "Trend Analysis" tab:
1. Select metric (Job Postings, Salary, Applications, Views)
2. Adjust MA window (2-6 months)
3. View trend with confidence band
4. Identify inflection points
```

### Deep Sector Analysis
```
In "Sector Deep-Dive" tab:
1. Select sector from dropdown
2. View top 12 positions by frequency
3. See salary distribution
4. Identify top companies
```

### Advanced Job Search
```
In "Job Search" tab:
1. Search "Python AWS" to find Python + AWS jobs
2. Returns 25 best matches
3. Shows salary, level, company, sector
4. Click to expand full job posting
```

---

## 🚀 Next Steps

1. **Run the dashboard:** `streamlit run SGJOB_Dashboard.py`
2. **Select your persona** from the sidebar
3. **Adjust filters** to your needs
4. **Explore visualizations** - hover for details
5. **Export your insights** in your preferred format
6. **Share reports** with team/mentors

---

## 📚 Additional Resources

- **REFACTORING_SUMMARY.md** - Technical architecture & design decisions
- **READABILITY_IMPROVEMENTS.md** - Previous enhancement history
- **SGJobData.csv** - Complete dataset (1M+ job records)

---

**Welcome to the enhanced Workforce Intelligence Dashboard! 🎉**

For the best experience, use Chrome/Firefox, install all optional packages, and explore all three personas.

Good luck! 🚀
