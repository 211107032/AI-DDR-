import os
from fpdf import FPDF
import markdown

class ReportGenerator:
    def __init__(self):
        pass

    def generate_markdown(self, final_data: dict) -> str:
        """
        Formats the reasoned and mapped data into a strict Markdown structure.
        """
        md = "# Detailed Diagnostic Report (DDR)\n\n"
        
        md += "## 1. Property Issue Summary\n"
        md += f"{final_data.get('property_issue_summary', 'Not Available')}\n\n"
        
        md += "## 2. Area-wise Observations\n"
        for obs in final_data.get('area_wise_observations', []):
            md += f"### Area: {obs.get('area', 'Unknown')}\n"
            md += f"**Findings:** {obs.get('findings', 'Not Available')}\n"
            if obs.get('conflict_detected'):
                md += f"**🚨 Conflict Detected:** {obs.get('conflict_details', 'Not Available')}\n"
            if obs.get('missing_data') and obs.get('missing_data').lower() != "none":
                md += f"**Missing Data:** {obs.get('missing_data')}\n"
            if obs.get('image_path') and obs.get('image_path') != "Image Not Available":
                md += f"**Image Reference:** {os.path.basename(obs.get('image_path'))} (Available in output folder)\n"
            md += "\n"
            
        md += "## 3. Probable Root Cause\n"
        if final_data.get('probable_root_causes'):
            for cause in final_data['probable_root_causes']:
                md += f"- {cause}\n"
        else:
            md += "Not Available\n"
        md += "\n"
            
        md += "## 4. Severity Assessment\n"
        md += f"{final_data.get('severity_assessment', 'Not Available')}\n\n"
        
        md += "## 5. Recommended Actions\n"
        if final_data.get('recommended_actions'):
            for act in final_data['recommended_actions']:
                md += f"- {act}\n"
        else:
            md += "Not Available\n"
        md += "\n"
            
        md += "## 6. Additional Notes\n"
        md += f"{final_data.get('additional_notes', 'Not Available')}\n\n"
        
        md += "## 7. Missing or Unclear Information\n"
        md += f"{final_data.get('missing_or_unclear_information', 'Not Available')}\n"
        
        return md

    def export_to_pdf(self, markdown_text: str, output_path: str = "DDR_Report.pdf"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        import textwrap
        for raw_line in markdown_text.split('\n'):
            # Extremely safe ascii sanitation to prevent FPDF unicode math crashes
            safe_line = raw_line.encode('ascii', 'ignore').decode('ascii')
            
            # Split giant uninterrupted tokens (URLs, hashes) that crash FPDF
            safe_tokens = []
            for token in safe_line.split(' '):
                if len(token) > 60:
                    safe_tokens.append(token[:60] + "... ")
                else:
                    safe_tokens.append(token)
            safe_line = " ".join(safe_tokens)
            
            wrapped_lines = textwrap.wrap(safe_line, width=100) if safe_line.strip() else [""]
            
            for line in wrapped_lines:
                try:
                    if line.startswith('# '):
                        pdf.set_font("Helvetica", style="B", size=16)
                        pdf.multi_cell(0, 10, line.replace('# ', ''))
                    elif line.startswith('## '):
                        pdf.set_font("Helvetica", style="B", size=14)
                        pdf.cell(0, 10, "", ln=True)
                        pdf.multi_cell(0, 8, line.replace('## ', ''))
                    elif line.startswith('### '):
                        pdf.set_font("Helvetica", style="B", size=12)
                        pdf.multi_cell(0, 6, line.replace('### ', ''))
                    elif line.startswith('**'):
                        pdf.set_font("Helvetica", style="B", size=11)
                        pdf.multi_cell(0, 6, line.replace('**', ''))
                    else:
                        pdf.set_font("Helvetica", size=11)
                        pdf.multi_cell(0, 6, line)
                except Exception:
                    # Absolute fallback to prevent any unhandled crash
                    pdf.set_font("Helvetica", size=11)
                    pdf.write(6, line + '\n')
                
        pdf.output(output_path)
        return output_path
