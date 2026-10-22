# Course reports

The project's university submissions (BCSE307P) and the scripts that generate them. They are not needed to
run or test the compiler.

| File | What |
|---|---|
| `Compiler_Design_Project_Review_1_Report.docx`, `PROJECT_REPORT_REVIEW_1.{md,html}` | Review 1 report (270-program initial sweep) |
| `Compiler_Design_Project_Review_2_Report.docx` | Review 2 report (initial 900-program results & 8-model comparison) |
| `Compiler_Design_Project_Review_3_Report.docx`, `Compiler_Design_Project_Final_Report.docx` | Review 3 / Final submission report (900-program results + per-pass interaction & non-additivity analysis, size-aware 2 MB HistGBT recommender, LU+LICM & determinism fixes, unified `minic.py` CLI, redesigned playground & visual results dashboard) |
| `output-images/` | Screenshots used in the reports |

To regenerate them you need three extra packages:

```bash
pip install python-docx reportlab pypdf
```

```bash
python reports/generate_report_docx.py
```

```bash
python reports/generate_final_report.py
```

`generate_final_report.py` fills the university's report template (using `~/Downloads/Project - Report Template.docx` if present, or falling back to `reports/Compiler_Design_Project_Review_2_Report.docx`).
