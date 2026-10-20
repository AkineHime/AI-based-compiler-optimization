import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_color):
    """Set background color of a table cell."""
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    """Set cell padding in twips."""
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_table_borders(table, color="CBD5E0", sz="4", val="single"):
    """Set light borders around table."""
    tblPr = table._element.xpath('w:tblPr')
    if tblPr:
        borders = parse_xml(f'<w:tblBorders {nsdecls("w")}><w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/><w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/><w:left w:val="none"/><w:right w:val="none"/><w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/><w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/></w:tblBorders>')
        tblPr[0].append(borders)

def build_docx(filename="Compiler_Design_Project_Review_1_Report.docx"):
    doc = Document()

    # Set page margins: 0.5 in (36 pt)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.5)
        section.right_margin = Inches(0.5)
        
        # Header & Footer
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("Vellore Institute of Technology | CSE3005 - Compiler Design | Review-1 (Assessment-6)")
        hrun.font.name = "Calibri"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(100, 116, 139)

        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.LEFT
        frun1 = fp.add_run("Project: AI-Based Compiler Optimization for MiniC (Phase Ordering & Pass Selection)")
        frun1.font.name = "Calibri"
        frun1.font.size = Pt(8.5)
        frun1.font.color.rgb = RGBColor(100, 116, 139)

    # Base Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(9.5)
    normal_style.font.color.rgb = RGBColor(30, 41, 59)

    # ==========================================
    # PAGE 1: TITLE, TEAM, ABSTRACT, ARCHITECTURE, FRONTEND
    # ==========================================
    
    # Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(2)
    run_title = p_title.add_run("AI-BASED COMPILER OPTIMIZATION FOR MINIC")
    run_title.font.name = "Calibri"
    run_title.font.size = Pt(15)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(15, 35, 65) # Navy Blue

    # Subtitle
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(6)
    run_sub = p_sub.add_run("Phase Ordering & Static-Feature-Driven Pass Selection Using Machine Learning | Review-1 Report")
    run_sub.font.name = "Calibri"
    run_sub.font.size = Pt(10.5)
    run_sub.font.bold = True
    run_sub.font.color.rgb = RGBColor(43, 108, 176)

    # Team Table
    table_team = doc.add_table(rows=5, cols=4)
    table_team.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table_team)
    
    headers = ["S.No", "Student Name", "Reg. Number", "Project Role & Core Contribution Area"]
    col_widths = [Inches(0.5), Inches(1.5), Inches(1.2), Inches(4.3)]

    # Header row
    for j, text in enumerate(headers):
        cell = table_team.cell(0, j)
        cell.width = col_widths[j]
        set_cell_background(cell, "1A365D")
        set_cell_margins(cell, 60, 60, 80, 80)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(text)
        run.font.bold = True
        run.font.size = Pt(8.5)
        run.font.color.rgb = RGBColor(255, 255, 255)

    team_rows = [
        ("1", "Student 1 (Lead)", "22BCE0001", "Person A: Front-End (Lexer, BNF Parser, AST, Semantic Analyzer), TAC IR Lowering, Dominator Trees & 19 Static Features."),
        ("2", "Student 2", "22BCE0002", "Person B: 6 Optimization Passes (CF, DCE, CSE, LICM, SR, LU), 64-Combo Pass Controller, Fixed-Point Loop & Value-Semantics Codegen."),
        ("3", "Student 3", "22BCE0003", "Person C: Timing Harness (gcc -O0 least-of-15), 17,280-Run Dataset, Risk-Aware HistGBT Recommender & Interactive Web Playground."),
        ("4", "Student 4", "22BCE0004", "Person D: 270 Benchmark Programs Corpus (30 Handcrafted + 240 Parametric), Ground Truth Verification Oracle & Performance Analysis.")
    ]

    for i, row in enumerate(team_rows):
        bg = "F8FAFC" if i % 2 == 0 else "FFFFFF"
        for j, val in enumerate(row):
            cell = table_team.cell(i+1, j)
            cell.width = col_widths[j]
            set_cell_background(cell, bg)
            set_cell_margins(cell, 50, 50, 80, 80)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            run = p.add_run(val)
            run.font.size = Pt(8.2)

    doc.add_paragraph().paragraph_format.space_after = Pt(3)

    # 1. Abstract & Problem Statement
    h1 = doc.add_heading(level=1)
    h1.paragraph_format.space_before = Pt(4)
    h1.paragraph_format.space_after = Pt(2)
    h1.paragraph_format.keep_with_next = True
    r1 = h1.add_run("1. Abstract & Problem Motivation")
    r1.font.name = "Calibri"
    r1.font.size = Pt(11)
    r1.font.bold = True
    r1.font.color.rgb = RGBColor(15, 35, 65)

    p1 = doc.add_paragraph()
    p1.paragraph_format.space_before = Pt(0)
    p1.paragraph_format.space_after = Pt(4)
    p1.paragraph_format.line_spacing = 1.15
    p1.add_run(
        "Modern optimizing compilers (e.g., GCC, LLVM) rely on hardcoded heuristic levels like -O2 or -O3 that apply a predetermined, fixed sequence of optimization passes to all input programs. However, optimizing passes interact non-linearly: an earlier pass can destroy preconditions for a subsequent pass (the Phase-Ordering Problem), and indiscriminately enabling aggressive passes causes severe performance regressions due to instruction cache pressure, register spilling, and unroll overheads. In our empirical sweep across 270 benchmark programs, turning all optimization passes on produced performance regressions on over 243 out of 270 programs compared to the optimal per-program configuration.\n"
        "This project develops an end-to-end optimizing compiler and machine learning recommendation system for MiniC—a strongly-typed, pointer-free C dialect designed for provably safe transformations. By extracting a 27-dimensional static feature vector from Three-Address Code (TAC), our risk-aware Histogram Gradient Boosted Tree (HistGBT) model selects the optimal combination out of 64 pass configurations, achieving a geomean speedup of 1.23x on held-out unseen programs (capturing 44% of achievable oracle speedup) while suppressing the compiler regression rate to 9%."
    )

    # 2. System Architecture
    h2 = doc.add_heading(level=1)
    h2.paragraph_format.space_before = Pt(4)
    h2.paragraph_format.space_after = Pt(2)
    h2.paragraph_format.keep_with_next = True
    r2 = h2.add_run("2. System Architecture & End-to-End Pipeline")
    r2.font.name = "Calibri"
    r2.font.size = Pt(11)
    r2.font.bold = True
    r2.font.color.rgb = RGBColor(15, 35, 65)

    # Pipeline summary table
    pipe_tbl = doc.add_table(rows=2, cols=3)
    pipe_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(pipe_tbl)
    pwidths = [Inches(2.5), Inches(2.5), Inches(2.5)]
    
    stages = [
        ("Stage 1: Front-End Parser", "MiniC Source (.mc) -> Lexer -> BNF Parser -> AST -> Semantic Checking (Types, Array Dimensions, Struct Resolution)."),
        ("Stage 2: TAC IR & Features", "AST -> Three-Address Code (TAC) IR -> CFG Construction -> Dominator Trees & Natural Loops -> 27 Static Feature Vector Extractor."),
        ("Stage 3: ML Recommender", "27 Static Features -> HistGBT Regressor -> Risk-Aware Abstain-Margin Policy -> Recommended Pass Combination (Bitmask 0..63)."),
        ("Stage 4: Optimization Engine", "6 Modular Passes (CF, DCE, CSE, LICM, SR, LU) -> Iterated to Fixed-Point Convergence in Canonical Order."),
        ("Stage 5: Codegen & Timing", "Optimized TAC -> ANSI C with 1-field wrapper structs -> gcc -O0 compilation -> Least of 15 execution runs."),
        ("Stage 6: Correctness Oracle", "Strict verification gate: Exit code and return value of optimized binary must identically match baseline unoptimized binary.")
    ]

    for idx, (st_title, st_desc) in enumerate(stages):
        r_idx = idx // 3
        c_idx = idx % 3
        cell = pipe_tbl.cell(r_idx, c_idx)
        cell.width = pwidths[c_idx]
        set_cell_background(cell, "F1F5F9")
        set_cell_margins(cell, 40, 40, 60, 60)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        rt = p.add_run(st_title + "\n")
        rt.font.bold = True
        rt.font.size = Pt(8.5)
        rt.font.color.rgb = RGBColor(26, 54, 93)
        rd = p.add_run(st_desc)
        rd.font.size = Pt(7.8)

    doc.add_paragraph().paragraph_format.space_after = Pt(2)

    # 3. MiniC Language Design & Front-End
    h3 = doc.add_heading(level=1)
    h3.paragraph_format.space_before = Pt(4)
    h3.paragraph_format.space_after = Pt(2)
    h3.paragraph_format.keep_with_next = True
    r3 = h3.add_run("3. MiniC Language Specification & Front-End Engineering")
    r3.font.name = "Calibri"
    r3.font.size = Pt(11)
    r3.font.bold = True
    r3.font.color.rgb = RGBColor(15, 35, 65)

    p3 = doc.add_paragraph()
    p3.paragraph_format.space_before = Pt(0)
    p3.paragraph_format.space_after = Pt(4)
    p3.paragraph_format.line_spacing = 1.15
    p3.add_run(
        "MiniC Design Rationale: Traditional C optimization is notoriously constrained by pointer aliasing. In MiniC, dynamic memory (malloc/free) and raw pointers are excluded. Multi-dimensional arrays, strings, and nominal structs strictly obey value semantics. This ensures total alias freedom—variables never share mutable memory locations, allowing transformations such as common subexpression elimination, loop hoisting, and dead store elimination to be provably sound without expensive conservative alias analysis.\n"
        "Front-End Implementation: Implemented in src/minic/frontend/, the compiler features a robust tokenizing lexer and recursive-descent parser. The semantic analyzer enforces strict typing, struct member resolution, and array bounds. ASTs are lowered into Three-Address Code (TAC) instructions (alloc, assign, binop, unop, label, goto, ifFalse, param, call, return) in src/minic/ir/, structured into basic blocks with full dominator tree and natural loop analysis."
    )

    # PAGE BREAK TO PAGE 2
    doc.add_page_break()

    # ==========================================
    # PAGE 2: OPTIMIZATION PASSES, STATIC FEATURES & ML ARCHITECTURE
    # ==========================================
    h4 = doc.add_heading(level=1)
    h4.paragraph_format.space_before = Pt(0)
    h4.paragraph_format.space_after = Pt(2)
    h4.paragraph_format.keep_with_next = True
    r4 = h4.add_run("4. Modular Optimization Passes & Value-Semantics Codegen")
    r4.font.name = "Calibri"
    r4.font.size = Pt(11)
    r4.font.bold = True
    r4.font.color.rgb = RGBColor(15, 35, 65)

    p4_intro = doc.add_paragraph()
    p4_intro.paragraph_format.space_before = Pt(0)
    p4_intro.paragraph_format.space_after = Pt(2)
    p4_intro.add_run(
        "The optimization subsystem (src/minic/optimizer/) implements 6 independently toggleable passes controlled by a 6-bit mask (64 combinations). Passes run in canonical pipeline order (CF -> CSE -> LU -> LICM -> SR -> DCE) iterated until reaching a fixed point:"
    )

    passes = [
        ("Constant Folding & Propagation (CF - Bit 0):", " Evaluates compile-time constant expressions (e.g. 3 * 5 -> 15), eliminates unconditional branches (ifFalse 1 goto L), and propagates known constants across basic blocks."),
        ("Common Subexpression Elimination (CSE - Bit 1):", " Employs local value numbering per basic block to identify repeated identical binary computations, replacing redundant expressions with existing temporary variables."),
        ("Loop Unrolling (LU - Bit 2):", " Analyzes canonical while loops with constant/symbolic trip counts, unrolling loop bodies by a factor of 2 or 4 to eliminate branch overheads and expose instruction-level parallelism."),
        ("Loop-Invariant Code Motion (LICM - Bit 3):", " Uses dominator trees and natural loop boundaries to detect statements whose operands remain unchanged across loop iterations, hoisting them into pre-header basic blocks."),
        ("Strength Reduction (SR - Bit 4):", " Detects induction variables in loops and replaces expensive multiplication/modulo operations (e.g., i * 8) with fast incremental additions (t = t + 8)."),
        ("Dead Code Elimination (DCE - Bit 5):", " Performs backward liveness analysis to eliminate dead instructions and temporary allocations that have zero reachable downward-exposed uses."),
        ("Value-Semantics Codegen (src/minic/codegen/):", " Emits valid ANSI C code. To guarantee value semantics, arrays and strings are wrapped in single-field structs (e.g. typedef struct { int data[10]; } arr_10;), ensuring pass-by-value and assignment-copy behavior without pointer decay.")
    ]

    for p_name, p_desc in passes:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_before = Pt(0)
        bp.paragraph_format.space_after = Pt(1.5)
        r_name = bp.add_run(p_name)
        r_name.font.bold = True
        r_name.font.size = Pt(8.5)
        r_desc = bp.add_run(p_desc)
        r_desc.font.size = Pt(8.5)

    # 5. Static Features & ML Recommender
    h5 = doc.add_heading(level=1)
    h5.paragraph_format.space_before = Pt(4)
    h5.paragraph_format.space_after = Pt(2)
    h5.paragraph_format.keep_with_next = True
    r5 = h5.add_run("5. Static Feature Extraction & Machine Learning Recommender")
    r5.font.name = "Calibri"
    r5.font.size = Pt(11)
    r5.font.bold = True
    r5.font.color.rgb = RGBColor(15, 35, 65)

    p5 = doc.add_paragraph()
    p5.paragraph_format.space_before = Pt(0)
    p5.paragraph_format.space_after = Pt(3)
    p5.add_run(
        "To recommend pass combinations without expensive runtime execution, the compiler extracts a 27-dimensional static feature vector directly from the TAC IR and CFG (19 structural metrics + 8 optimization opportunity metrics):"
    )

    feat_tbl = doc.add_table(rows=3, cols=3)
    feat_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(feat_tbl)
    
    f_headers = ["Category", "Dims", "Extracted Code Metrics & Compiler Significance"]
    f_widths = [Inches(1.5), Inches(0.6), Inches(5.4)]

    for j, text in enumerate(f_headers):
        cell = feat_tbl.cell(0, j)
        cell.width = f_widths[j]
        set_cell_background(cell, "1A365D")
        set_cell_margins(cell, 50, 50, 80, 80)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(text)
        run.font.bold = True
        run.font.size = Pt(8.5)
        run.font.color.rgb = RGBColor(255, 255, 255)

    f_rows = [
        ("Structural Features (src/minic/features/)", "19", "Total instructions, basic block count, loop count, max loop nesting depth, branch count, branch density, arithmetic/multiplication/load/store/call histograms, named vs temp variables, array and struct access counts."),
        ("Opportunity Features (src/minic/features/opportunity.py)", "8", "Foldable constant expression count, loop-invariant candidate count, common subexpression candidate count, reducible induction multiplication count, unrollable loop count, dead store candidate ratio.")
    ]

    for i, row in enumerate(f_rows):
        bg = "F8FAFC" if i % 2 == 0 else "FFFFFF"
        for j, val in enumerate(row):
            cell = feat_tbl.cell(i+1, j)
            cell.width = f_widths[j]
            set_cell_background(cell, bg)
            set_cell_margins(cell, 40, 40, 80, 80)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            run = p.add_run(val)
            run.font.size = Pt(8.2)

    doc.add_paragraph().paragraph_format.space_after = Pt(2)

    p_ml = doc.add_paragraph()
    p_ml.paragraph_format.space_before = Pt(0)
    p_ml.paragraph_format.space_after = Pt(3)
    p_ml.paragraph_format.line_spacing = 1.15
    p_ml.add_run(
        "Risk-Aware Abstain-Margin Strategy: Standard argmax regression across predicted speedups suffers from high false-positive risk, causing regressions on 21% of unseen programs. To eliminate this, we formulated an abstain-margin policy: the Histogram Gradient Boosted Tree (HistGBT) regressor predicts speedup S(p, c). If max S(p, c) >= theta (theta = 1.12x), the model recommends argmax S(p, c); otherwise, it abstains to Combo 0 (no passes). This cut regressions to 9% while capturing 44% of oracle speedup.\n"
        "GroupKFold Cross-Validation: Cross-validation splits are grouped strictly by program_id across 5 folds. Since all 64 pass rows for a program share identical static features, standard random splits would cause severe feature leakage. GroupKFold guarantees genuine evaluation on unseen program structures."
    )

    # 6. Experimental Sweep Methodology
    h6 = doc.add_heading(level=1)
    h6.paragraph_format.space_before = Pt(3)
    h6.paragraph_format.space_after = Pt(2)
    h6.paragraph_format.keep_with_next = True
    r6 = h6.add_run("6. Empirical Benchmark Sweep & Timing Methodology")
    r6.font.name = "Calibri"
    r6.font.size = Pt(11)
    r6.font.bold = True
    r6.font.color.rgb = RGBColor(15, 35, 65)

    p6 = doc.add_paragraph()
    p6.paragraph_format.space_before = Pt(0)
    p6.paragraph_format.space_after = Pt(0)
    p6.paragraph_format.line_spacing = 1.15
    p6.add_run(
        "A comprehensive corpus of 270 benchmark programs was evaluated (30 hand-written algorithms spanning 2D arrays, structs, strings, recursion, numeric loops + 240 parametric synthetic benchmarks). Each program was emitted to C across all 64 pass combinations = 17,280 compiled configurations. Programs were compiled with gcc -O0 (isolating MiniC's optimizer contribution from C compiler passes) and executed 15 times, recording the minimum-interference wall-clock runtime after 4 warmup runs. Every build verified exit-code equivalence against baseline."
    )

    # PAGE BREAK TO PAGE 3
    doc.add_page_break()

    # ==========================================
    # PAGE 3: SCREENSHOTS, RESULTS & REVIEW-1 CONCLUSION
    # ==========================================
    h7 = doc.add_heading(level=1)
    h7.paragraph_format.space_before = Pt(0)
    h7.paragraph_format.space_after = Pt(2)
    h7.paragraph_format.keep_with_next = True
    r7 = h7.add_run("7. Implementation Screenshots & Execution Verification (Review-1 Demonstration)")
    r7.font.name = "Calibri"
    r7.font.size = Pt(11)
    r7.font.bold = True
    r7.font.color.rgb = RGBColor(15, 35, 65)

    p7_intro = doc.add_paragraph()
    p7_intro.paragraph_format.space_before = Pt(0)
    p7_intro.paragraph_format.space_after = Pt(2)
    p7_intro.add_run("The figures below demonstrate the working compiler optimization pipeline and web playground interface (demo/app.py) across two representative benchmark runs:")

    # Screenshots table (2x2 grid)
    img_tbl = doc.add_table(rows=4, cols=2)
    img_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # Run 1 images
    c00 = img_tbl.cell(0, 0)
    c01 = img_tbl.cell(0, 1)
    c00.paragraphs[0].paragraph_format.space_after = Pt(0)
    c01.paragraphs[0].paragraph_format.space_after = Pt(0)
    c00.paragraphs[0].add_run().add_picture("output-images/run1/image_370.png", width=Inches(3.6))
    c01.paragraphs[0].add_run().add_picture("output-images/run1/image_372.png", width=Inches(3.6))

    # Caption 1
    c10 = img_tbl.cell(1, 0)
    c11 = img_tbl.cell(1, 1)
    p_cap1a = c10.paragraphs[0]
    p_cap1a.paragraph_format.space_after = Pt(2)
    r_cap1a = p_cap1a.add_run("Fig 1(a): Run 1 TAC Diff (Combo 0 vs Combo 63) for Struct Distance.")
    r_cap1a.font.size = Pt(7.8)
    r_cap1a.font.italic = True
    
    p_cap1b = c11.paragraphs[0]
    p_cap1b.paragraph_format.space_after = Pt(2)
    r_cap1b = p_cap1b.add_run("Fig 1(b): Run 1 Performance: 2.52x Speedup (190.57 ms -> 75.49 ms; beats gcc -O2).")
    r_cap1b.font.size = Pt(7.8)
    r_cap1b.font.italic = True

    # Run 2 images
    c20 = img_tbl.cell(2, 0)
    c21 = img_tbl.cell(2, 1)
    c20.paragraphs[0].paragraph_format.space_after = Pt(0)
    c21.paragraphs[0].paragraph_format.space_after = Pt(0)
    c20.paragraphs[0].add_run().add_picture("output-images/run2/image_373.png", width=Inches(3.6))
    c21.paragraphs[0].add_run().add_picture("output-images/run2/image_375.png", width=Inches(3.6))

    # Caption 2
    c30 = img_tbl.cell(3, 0)
    c31 = img_tbl.cell(3, 1)
    p_cap2a = c30.paragraphs[0]
    p_cap2a.paragraph_format.space_after = Pt(2)
    r_cap2a = p_cap2a.add_run("Fig 2(a): Run 2 TAC Diff for Loop-Invariant Math (Loop Unrolling & LICM hoists).")
    r_cap2a.font.size = Pt(7.8)
    r_cap2a.font.italic = True
    
    p_cap2b = c31.paragraphs[0]
    p_cap2b.paragraph_format.space_after = Pt(2)
    r_cap2b = p_cap2b.add_run("Fig 2(b): Run 2 Performance: 1.93x Speedup (200.64 ms -> 104.10 ms).")
    r_cap2b.font.size = Pt(7.8)
    r_cap2b.font.italic = True

    # 8. Key Experimental Results
    h8 = doc.add_heading(level=1)
    h8.paragraph_format.space_before = Pt(3)
    h8.paragraph_format.space_after = Pt(2)
    h8.paragraph_format.keep_with_next = True
    r8 = h8.add_run("8. Key Experimental Results & Comparative Performance Analysis")
    r8.font.name = "Calibri"
    r8.font.size = Pt(11)
    r8.font.bold = True
    r8.font.color.rgb = RGBColor(15, 35, 65)

    res_tbl = doc.add_table(rows=5, cols=5)
    res_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(res_tbl)
    
    r_headers = ["Optimization Strategy", "Geomean Speedup", "Max Speedup", "Regression Rate (>2% Slower)", "Captured Oracle Potential"]
    r_widths = [Inches(2.4), Inches(1.2), Inches(1.0), Inches(1.6), Inches(1.3)]

    for j, text in enumerate(r_headers):
        cell = res_tbl.cell(0, j)
        cell.width = r_widths[j]
        set_cell_background(cell, "1A365D")
        set_cell_margins(cell, 40, 40, 60, 60)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(text)
        run.font.bold = True
        run.font.size = Pt(8.2)
        run.font.color.rgb = RGBColor(255, 255, 255)

    res_rows = [
        ("Baseline (Combo 0 - No Passes)", "1.00x", "1.00x", "0.0% (Reference)", "0.0%"),
        ("Default All-On (Combo 63 - Monolithic)", "1.21x", "4.57x", "18.5% (Unsafe on 243/270)", "38.9%"),
        ("ML Recommender (HistGBT + Abstain)", "1.23x (Held-Out)", "4.57x", "9.0% (Risk Controlled)", "44.0% of Achievable Gain"),
        ("Theoretical Oracle (Best Combo per Program)", "1.50x (Geomean)", "4.57x", "0.0% (Optimal Selection)", "100.0% (Upper Bound)")
    ]

    for i, row in enumerate(res_rows):
        bg = "EBF8FF" if i == 2 else ("F8FAFC" if i % 2 == 0 else "FFFFFF")
        for j, val in enumerate(row):
            cell = res_tbl.cell(i+1, j)
            cell.width = r_widths[j]
            set_cell_background(cell, bg)
            set_cell_margins(cell, 35, 35, 60, 60)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            run = p.add_run(val)
            if i == 2:
                run.font.bold = True
            run.font.size = Pt(8.0)

    doc.add_paragraph().paragraph_format.space_after = Pt(1)

    p_cat = doc.add_paragraph()
    p_cat.paragraph_format.space_before = Pt(0)
    p_cat.paragraph_format.space_after = Pt(2)
    p_cat.add_run("Category Speedup Highlights: Struct Operations: 3.08x | Nested Loops: 1.81x | Strings: 1.57x | Numeric: 1.37x | Recursion: 1.24x.")
    p_cat.runs[0].font.size = Pt(8.2)
    p_cat.runs[0].font.bold = True

    # 9. Conclusion & Review-2 Milestones
    h9 = doc.add_heading(level=1)
    h9.paragraph_format.space_before = Pt(2)
    h9.paragraph_format.space_after = Pt(1)
    h9.paragraph_format.keep_with_next = True
    r9 = h9.add_run("9. Review-1 Completion Summary & Review-2 Milestones")
    r9.font.name = "Calibri"
    r9.font.size = Pt(11)
    r9.font.bold = True
    r9.font.color.rgb = RGBColor(15, 35, 65)

    p9 = doc.add_paragraph()
    p9.paragraph_format.space_before = Pt(0)
    p9.paragraph_format.space_after = Pt(0)
    p9.paragraph_format.line_spacing = 1.15
    p9.add_run(
        "Review-1 Accomplishments: Delivered a fully functional end-to-end optimizing compiler for MiniC, featuring a 6-pass optimization engine, TAC intermediate representation, 27-dimensional static feature extractor, 17,280-sample benchmark timing dataset, risk-aware HistGBT recommendation model, and interactive web playground.\n"
        "Review-2 Roadmap: (1) Integrate dynamic hardware performance counter features (L1/L2 cache misses, branch mispredictions); (2) Apply Reinforcement Learning (PPO/DQN) for dynamic sequence ordering beyond fixed passes; (3) Implement Inter-Procedural Optimization (IPO) & Function Inlining."
    )
    p9.runs[0].font.size = Pt(8.2)

    doc.save(filename)
    print(f"Generated {filename} successfully.")

if __name__ == '__main__':
    # image paths and the output file are relative to reports/
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    build_docx()
