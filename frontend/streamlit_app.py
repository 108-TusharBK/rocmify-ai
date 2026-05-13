import streamlit as st

import json
import sys
import os
import zipfile
from io import BytesIO

st.write("XSRF:", st.get_option("server.enableXsrfProtection"))
st.write("CORS:", st.get_option("server.enableCORS"))

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)
from backend.llm_advisor import generate_llm_summary

from backend.analyzer import analyze_code

from backend.lim_explainer import explain_finding

st.title("🚀 ROCmify AI")
st.caption(
    "AI-powered copilot for migrating CUDA/PyTorch projects to AMD ROCm"
)

with st.sidebar:
    st.header("About")
    st.write(
        "ROCmify AI analyzes CUDA and PyTorch projects "
        "and recommends migration paths to AMD ROCm."
    )

def calculate_score(findings):
    score = 100

    penalties = {
        "high" : 25,
        "medium" : 15,
        "warning" : 10,
    }

    for item in findings:
        score -= penalties.get(item["severity"], 5)
    
    return max(score, 0)


def count_severities(findings):
    counts = {
        "high": 0,
        "medium": 0,
        "warning": 0,
    }

    for item in findings:
        severity = item["severity"]
        counts[severity] = counts.get(severity, 0) + 1

    return counts


uploaded_file = st.file_uploader(
    "Upload CUDA or PyTorch file",
    type = ["py", "txt", "zip"]
)


def build_replacement_table(findings):
    replacements = {
        "cuda": "HIP / ROCm",
        "torch.cuda": "ROCm-enabled PyTorch",
        "cudnn": "MIOpen",
        "nccl": "RCCL",
        "tensorrt": "ONNX Runtime or vLLM",
        "cupy": "ROCm-compatible CuPy or PyTorch",
        "torch.distributed": "PyTorch Distributed + RCCL",
        "tensorflow-gpu": "tensorflow-rocm",
        "nvidia": "ROCm-compatible alternative",
    }

    rows = []

    for item in findings:
        keyword = item["keyword"]

        if keyword in replacements:
            rows.append({
                "NVIDIA Component": keyword,
                "ROCm Alternative": replacements[keyword],
            })

    # Remove duplicates
    unique_rows = []
    seen = set()

    for row in rows:
        key = row["NVIDIA Component"]

        if key not in seen:
            unique_rows.append(row)
            seen.add(key)

    return unique_rows


def estimate_effort(score):
    if score >= 80:
        return "1-2 hours"
    elif score >= 50:
        return "0.5-2 days"
    elif score >= 30:
        return "2-5 days"
    else:
        return "1-2 weeks"


def generate_summary(score, effort, findings):
    if score >= 80:
        risk = "low"
    elif score >= 50:
        risk = "moderate"
    else:
        risk = "high"

    return (
        f"This project has a ROCm readiness score of {score}/100, "
        f"indicating {risk} migration risk. "
        f"The estimated engineering effort is {effort}. "
        f"{len(findings)} compatibility issue(s) were detected."
    )



def generate_markdown_report(
    filename,
    score,
    effort,
    findings,
    summary
):
    lines = [
        f"# ROCmify AI Report",
        "",
        f"**File:** {filename}",
        f"**ROCm Readiness Score:** {score}/100",
        f"**Estimated Migration Effort:** {effort}",
        f"**Total Issues:** {len(findings)}",
        "",
        "## Executive Summary",
        "",
        summary,
        "",
        "## Suggested Migration Plan",
        "",
        generate_migration_plan(findings),
        "",
        "## Findings",
        "",
    ]

    for item in findings:
        lines.extend([
            f"### {item['keyword']}",
            f"- Severity: {item['severity']}",
            f"- Issue: {item['issue']}",
            f"- Recommendation: {item['recommendation']}",
            "",
        ])

    return "\n".join(lines)


def extract_text_from_zip(uploaded_file):
    combined_text = []
    analyzed_files = 0

    with zipfile.ZipFile(BytesIO(uploaded_file.read())) as z:
        for file_name in z.namelist():
            # Only analyze relevant text files
            if (
                file_name.endswith(".py")
                or file_name.endswith(".txt")
                or file_name.endswith("requirements.txt")
                or file_name.endswith("Dockerfile")
            ):
                try:
                    content = z.read(file_name).decode(
                        "utf-8",
                        errors="ignore"
                    )

                    combined_text.append(content)
                    analyzed_files += 1

                except Exception:
                    pass

    return "\n".join(combined_text), analyzed_files


def generate_migration_plan(findings):
    steps = []

    for i, item in enumerate(findings, start=1):
        steps.append(
            f"{i}. {item['recommendation']}"
        )

    return "\n".join(steps)


if uploaded_file:

    if uploaded_file.name.endswith(".zip"):
        content, analyzed_files = extract_text_from_zip(uploaded_file)

        if not content.strip():
            st.error("No supported files found inside ZIP.")
            st.stop()
    
    else:
        raw_data = uploaded_file.read()

        if not raw_data:
            st.error("Uploaded file is empty.")
            st.stop()

        content = raw_data.decode(
            "utf-8",
            errors = "ignore"
        )

        analyzed_files = 1

    findings = analyze_code(content)

    if uploaded_file.name.endswith(".zip"):
        st.success(
            f"Repository uploaded: {uploaded_file.name}"
        )
    else:
        st.success(
            f"Uploaded: {uploaded_file.name}"
        )

    st.write(
        f"File type: {uploaded_file.type}"
    )

    st.write(
        f"Files analyzed: {analyzed_files}"
    )

    if findings:

        st.subheader("Migration Summary")
        st.write(f"Total issues found: {len(findings)}")

        counts = count_severities(findings)

        st.write(
            f"High: {counts['high']} | "
            f"Medium: {counts['medium']} | "
            f"Warning: {counts['warning']}"
        )

        score = calculate_score(findings)

        st.metric(
            "Rocm Readiness Score",
            f"{score}/100"
        )

        if score >= 80:
            st.success("✅ Highly compatible with ROCm.")

        elif score >= 50:
            st.warning("⚠️ Moderate migration effort required.")

        else:
            st.error("❌ Significant migration work required.")

        effort = estimate_effort(score)

        st.metric(
            "Estimated Migration Effort",
            effort
        )

        summary = generate_summary(score, effort, findings)

        llm_summary = generate_llm_summary(
            score,
            effort,
            findings
        )

        st.subheader("Executive Summary")

        if llm_summary:
            summary = llm_summary
            st.success("🤖 AI-generated summary")
            st.info(llm_summary)
        else:
            st.warning("Using rule-based summary")
            st.info(summary)

        st.subheader("Suggested ROCm Replacements")

        replacement_rows = build_replacement_table(findings)

        if replacement_rows:
            st.table(replacement_rows)

        st.subheader("Suggested Migration Plan")

        Migration_plan = generate_migration_plan(findings)

        st.markdown(Migration_plan)

        for item in findings:

            severity = item["severity"]

            if severity == "high":
                st.error(
                    f"{item['keyword']} → "
                    f"{item['issue']}"
                )

                st.write(
                    explain_finding(item["keyword"])
                )
                
                st.info(
                    f"Recommendation: "
                    f"{item['recommendation']}"
                )

            elif severity == "medium":
                st.warning(
                    f"{item['keyword']} → "
                    f"{item['issue']}"
                )

                st.write(
                    explain_finding(item["keyword"])
                )

                st.info(
                    f"Recommendation: "
                    f"{item['recommendation']}"
                )

            else:
                st.info(
                    f"{item['keyword']} → "
                    f"{item['issue']}"
                )

                st.write(
                    explain_finding(item["keyword"])
                )

                st.info(
                    f"Recommendation: "
                    f"{item['recommendation']}"
                )

        report = {
            "filename": uploaded_file.name,
            "files_analyzed": analyzed_files,
            "total_issues": len(findings),
            "severity_counts": counts,
            "score": score,
            "estimated_effort": effort,
            "summary": summary,
            "replacement_table": replacement_rows,
            "migration_plan": generate_migration_plan(findings),
            "findings": findings,
        }

        st.download_button(
            label="Download JSON Report",
            data=json.dumps(report, indent=2),
            file_name="rocmify_report.json",
            mime="application/json",
        )

        markdown_report = generate_markdown_report(
            uploaded_file.name,
            score,
            effort,
            findings,
            summary          
        )

        st.download_button(
            label = "Download Markdown Report",
            data = markdown_report,
            file_name = "rocmify_report.md",
            mime = "text/markdown",
        )

    else:

        st.success(
            "No obvious CUDA-specific issues detected."
        )

