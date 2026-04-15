import streamlit as st
import os

from ingestion import IngestionModule
from extraction import ExtractionModule
from reasoning import ReasoningModule
from validation import ValidationModule
from report_generator import ReportGenerator
from image_mapper import ImageMapper
from utils import save_uploaded_file, cleanup_files

st.set_page_config(page_title="AI DDR Report Generator", page_icon="🧠", layout="wide")

st.title("🧠 AI DDR Report Generator")
st.markdown("Convert Inspection & Thermal PDFs into a structured Detailed Diagnostic Report (DDR).")

# Sidebar for Setup
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Groq API Key", type="password", value="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")

st.sidebar.markdown("---")
st.sidebar.header("Upload Reports")
inspection_pdf = st.sidebar.file_uploader("Inspection Report (PDF)", type=["pdf"])
thermal_pdf = st.sidebar.file_uploader("Thermal Report (PDF)", type=["pdf"])

if st.sidebar.button("Generate DDR") and inspection_pdf and thermal_pdf:
    if not api_key:
        st.sidebar.error("Please enter your OpenAI API Key.")
    else:
        with st.spinner("Processing documents..."):
            # 1. Setup
            insp_path = save_uploaded_file(inspection_pdf)
            therm_path = save_uploaded_file(thermal_pdf)
            
            # Module instances
            ingestor = IngestionModule()
            extractor = ExtractionModule(api_key=api_key)
            reasoner = ReasoningModule(api_key=api_key)
            validator = ValidationModule(api_key=api_key)
            mapper = ImageMapper()
            reporter = ReportGenerator()
            
            # 2. Ingestion
            st.toast("Ingesting PDFs and extracting images...")
            insp_raw = ingestor.process_pdf(insp_path, "Inspection")
            therm_raw = ingestor.process_pdf(therm_path, "Thermal")
            
            # 3. Extraction
            st.toast("Extracting structured data (OpenAI)...")
            insp_data = extractor.extract_data(insp_raw)
            therm_data = extractor.extract_data(therm_raw)
            
            # 4. Reasoning
            st.toast("Reasoning & Merging data...")
            reasoned_data = reasoner.process(insp_data, therm_data)
            
            # 5. Validation
            st.toast("Validating report logic...")
            is_valid, validation_msg = validator.validate(reasoned_data)
            if not is_valid:
                st.error(f"Validation Failed: {validation_msg}\nRegenerating might be required.")
                st.warning("Proceeding to render output anyway for debugging, but be aware it failed validation.")
            else:
                st.success("Validation Passed!")
                
            # 6. Mapping Images
            all_images = insp_raw["images"] + therm_raw["images"]
            final_data = mapper.map_images_to_observations(reasoned_data, all_images)
            
            # 7. Generate Outputs
            st.toast("Generating final Markdown & PDF...")
            markdown_report = reporter.generate_markdown(final_data)
            pdf_out_path = reporter.export_to_pdf(markdown_report, output_path="DDR_Output.pdf")
            
            st.divider()
            st.subheader("📄 Generated Detailed Diagnostic Report")
            st.markdown(markdown_report)
            
            with open(pdf_out_path, "rb") as pdf_file:
                st.download_button(
                    label="⬇️ Download DDR as PDF",
                    data=pdf_file,
                    file_name="Detailed_Diagnostic_Report.pdf",
                    mime="application/pdf"
                )
                
            # Cleanup
            cleanup_files(insp_path, therm_path)
            
elif not inspection_pdf or not thermal_pdf:
    st.info("Please upload both the Inspection Report and Thermal Report to proceed.")
