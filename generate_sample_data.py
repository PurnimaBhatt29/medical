"""
Generate sample medical data for testing MedVision AI
Creates sample PDFs and images for demonstration
"""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import os


def create_sample_medical_report():
    """Create a sample medical report PDF"""
    filename = "sample_medical_report.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1*inch, height - 1*inch, "MEDICAL LABORATORY REPORT")
    
    # Patient Info
    c.setFont("Helvetica", 10)
    y = height - 1.5*inch
    
    c.drawString(1*inch, y, "Patient Name: John Doe")
    y -= 0.3*inch
    c.drawString(1*inch, y, "Patient ID: 12345")
    y -= 0.3*inch
    c.drawString(1*inch, y, "Date: 2024-03-15")
    y -= 0.3*inch
    c.drawString(1*inch, y, "Physician: Dr. Smith")
    
    # Test Results
    y -= 0.5*inch
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, y, "LABORATORY TEST RESULTS")
    
    y -= 0.4*inch
    c.setFont("Helvetica", 10)
    
    tests = [
        ("Complete Blood Count (CBC)", ""),
        ("  White Blood Cell Count", "12.5 x10^9/L (High)"),
        ("  Red Blood Cell Count", "4.8 x10^12/L (Normal)"),
        ("  Hemoglobin", "14.2 g/dL (Normal)"),
        ("  Platelet Count", "250 x10^9/L (Normal)"),
        ("", ""),
        ("Metabolic Panel", ""),
        ("  Glucose (Fasting)", "126 mg/dL (Elevated)"),
        ("  Creatinine", "1.1 mg/dL (Normal)"),
        ("  Blood Urea Nitrogen", "18 mg/dL (Normal)"),
        ("  Sodium", "140 mEq/L (Normal)"),
        ("  Potassium", "4.2 mEq/L (Normal)"),
        ("", ""),
        ("Lipid Panel", ""),
        ("  Total Cholesterol", "240 mg/dL (High)"),
        ("  LDL Cholesterol", "160 mg/dL (High)"),
        ("  HDL Cholesterol", "45 mg/dL (Low)"),
        ("  Triglycerides", "180 mg/dL (Borderline High)"),
    ]
    
    for test_name, result in tests:
        if test_name:
            c.drawString(1*inch, y, f"{test_name}: {result}")
        y -= 0.25*inch
    
    # Clinical Notes
    y -= 0.3*inch
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, y, "CLINICAL INTERPRETATION")
    
    y -= 0.4*inch
    c.setFont("Helvetica", 10)
    
    notes = [
        "1. Elevated fasting glucose suggests impaired glucose tolerance.",
        "   Recommend HbA1c test and diabetes screening.",
        "",
        "2. Lipid panel shows dyslipidemia with elevated LDL and low HDL.",
        "   Consider statin therapy and lifestyle modifications.",
        "",
        "3. Mild leukocytosis noted. May indicate infection or inflammation.",
        "   Clinical correlation recommended.",
        "",
        "4. Recommend follow-up in 3 months with repeat metabolic panel.",
    ]
    
    for note in notes:
        c.drawString(1*inch, y, note)
        y -= 0.25*inch
    
    # Footer
    c.setFont("Helvetica-Italic", 8)
    c.drawString(1*inch, 0.5*inch, "This is a computer-generated report. For medical advice, consult your physician.")
    
    c.save()
    print(f"✓ Created: {filename}")
    return filename


def create_sample_prescription():
    """Create a sample prescription PDF"""
    filename = "sample_prescription.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1*inch, height - 1*inch, "MEDICAL PRESCRIPTION")
    
    # Doctor Info
    c.setFont("Helvetica", 10)
    y = height - 1.5*inch
    
    c.drawString(1*inch, y, "Dr. Sarah Johnson, MD")
    y -= 0.2*inch
    c.drawString(1*inch, y, "Internal Medicine")
    y -= 0.2*inch
    c.drawString(1*inch, y, "License #: MD123456")
    
    # Patient Info
    y -= 0.5*inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y, "Patient Information:")
    
    y -= 0.3*inch
    c.setFont("Helvetica", 10)
    c.drawString(1*inch, y, "Name: Jane Smith")
    y -= 0.2*inch
    c.drawString(1*inch, y, "Date: March 15, 2024")
    y -= 0.2*inch
    c.drawString(1*inch, y, "DOB: 01/15/1975")
    
    # Prescriptions
    y -= 0.5*inch
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, y, "Rx:")
    
    y -= 0.4*inch
    c.setFont("Helvetica", 11)
    
    prescriptions = [
        "1. Metformin 500mg",
        "   Sig: Take 1 tablet twice daily with meals",
        "   Disp: 60 tablets",
        "   Refills: 3",
        "",
        "2. Lisinopril 10mg",
        "   Sig: Take 1 tablet once daily in the morning",
        "   Disp: 30 tablets",
        "   Refills: 3",
        "",
        "3. Atorvastatin 20mg",
        "   Sig: Take 1 tablet once daily at bedtime",
        "   Disp: 30 tablets",
        "   Refills: 3",
        "",
        "4. Aspirin 81mg (Low-dose)",
        "   Sig: Take 1 tablet once daily",
        "   Disp: 30 tablets",
        "   Refills: 3",
    ]
    
    for line in prescriptions:
        c.drawString(1.2*inch, y, line)
        y -= 0.25*inch
    
    # Instructions
    y -= 0.3*inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y, "Special Instructions:")
    
    y -= 0.3*inch
    c.setFont("Helvetica", 10)
    instructions = [
        "- Take Metformin with food to reduce stomach upset",
        "- Monitor blood pressure regularly while on Lisinopril",
        "- Report any muscle pain or weakness while taking Atorvastatin",
        "- Follow up in 3 months for lab work",
    ]
    
    for instruction in instructions:
        c.drawString(1.2*inch, y, instruction)
        y -= 0.25*inch
    
    # Signature
    y -= 0.5*inch
    c.setFont("Helvetica-Italic", 10)
    c.drawString(1*inch, y, "Signature: ___________________________")
    y -= 0.3*inch
    c.drawString(1*inch, y, "Dr. Sarah Johnson, MD")
    
    c.save()
    print(f"✓ Created: {filename}")
    return filename


def create_readme_for_samples():
    """Create README for sample data"""
    content = """# Sample Medical Data

This directory contains sample medical documents for testing MedVision AI.

## Files

### sample_medical_report.pdf
A sample laboratory report containing:
- Complete Blood Count (CBC)
- Metabolic Panel
- Lipid Panel
- Clinical interpretation notes

**Use with**: Report Analyzer feature

### sample_prescription.pdf
A sample prescription containing:
- Metformin 500mg (diabetes medication)
- Lisinopril 10mg (blood pressure medication)
- Atorvastatin 20mg (cholesterol medication)
- Aspirin 81mg (antiplatelet)

**Use with**: Prescription Analyzer feature

## Testing Instructions

1. Launch MedVision AI: `streamlit run app.py`
2. Navigate to the appropriate feature
3. Upload the sample PDF
4. Click analyze button
5. Review the AI-generated analysis

## Disclaimer

These are fictional medical documents created for testing purposes only.
They do not represent real patient data.
"""
    
    with open("SAMPLE_DATA_README.md", "w") as f:
        f.write(content)
    
    print("✓ Created: SAMPLE_DATA_README.md")


def main():
    """Generate all sample data"""
    print("\n" + "="*60)
    print("Generating Sample Medical Data")
    print("="*60 + "\n")
    
    try:
        # Check if reportlab is installed
        import reportlab
    except ImportError:
        print("⚠️ reportlab not installed")
        print("\nInstall it with:")
        print("  pip install reportlab")
        print("\nOr skip sample generation and use your own medical PDFs.")
        return
    
    # Create sample files
    create_sample_medical_report()
    create_sample_prescription()
    create_readme_for_samples()
    
    print("\n" + "="*60)
    print("Sample Data Generation Complete!")
    print("="*60)
    print("\nGenerated files:")
    print("  - sample_medical_report.pdf")
    print("  - sample_prescription.pdf")
    print("  - SAMPLE_DATA_README.md")
    print("\nYou can now test MedVision AI with these sample files!")


if __name__ == "__main__":
    main()
