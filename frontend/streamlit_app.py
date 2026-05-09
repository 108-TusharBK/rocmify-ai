import streamlit as st

import json
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from backend.analyzer import analyze_code

from backend.lim_explainer import explain_finding

st.title("ROCmify AI")

def calculate_score(findings):
    score = 100

    penalties = {
        "high" : 25,
        "medium" : 15,
        "warning" : 10,
    }

    for item in findings:
        score -= penalties.get(item["severity"], 5)

    if score >= 80:
        st.success("✅ Highly compatible with ROCm.")

    elif score >= 50:
        st.warning("⚠️ Moderate migration effort required.")

    else:
        st.error("❌ Significant migration work required.")
    
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
    "Upload CUDA or PyTorch file"
)

if uploaded_file:

    raw_data = uploaded_file.read()

    if not raw_data:
        st.error("Uploaded file is empty")
        st.stop()

    content = raw_data.decode(
        "utf-8",
        errors = "ignore"
    )

    findings = analyze_code(content)

    st.success(
        f"Uploaded: {uploaded_file.name}"
    )

    st.write(
        f"File type: {uploaded_file.type}"
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
            "total_issues": len(findings),
            "score": score,
            "findings": findings,
        }

        st.download_button(
            label="Download JSON Report",
            data=json.dumps(report, indent=2),
            file_name="rocmify_report.json",
            mime="application/json",
        )
    else:

        st.success(
            "No obvious CUDA-specific issues detected."
        )

