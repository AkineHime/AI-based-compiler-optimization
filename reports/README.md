# Course reports

The project's university submissions (BCSE307P) and the scripts that generate them. They are not needed to
run or test the compiler.

| File | What |
|---|---|
| `Compiler_Design_Project_Review_1_Report.docx`, `PROJECT_REPORT_REVIEW_1.{md,html}` | Review 1 report |
| `Compiler_Design_Project_Final_Report.docx` | Final report (900-program results) |
| `output-images/` | Screenshots used in the Review 1 report |

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

`generate_final_report.py` fills the university's report template, which it expects at
`~/Downloads/Project - Report Template.docx`.
