import os
import sys
import torch
import whisperx
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import google.generativeai as genai

# =====================================================================
# 🔑 KEEP YOUR NEW API KEY HERE
# =====================================================================
API_KEY = "AQ.Ab8RN6IR43H15Gonv0wm_yXQiqSBZAe_RNvCbSVZfKw1EG5Hdw"

# =====================================================================
# DEEP FFMPEG COMPATIBILITY INJECTION
# =====================================================================
try:
    import ffmpeg_binaries
    ffmpeg_binaries.init()
    bin_dir = os.path.dirname(ffmpeg_binaries.FFMPEG_PATH)
    if bin_dir not in os.environ["PATH"]:
        os.environ["PATH"] = bin_dir + os.path.pathsep + os.environ["PATH"]
except Exception:
    pass

possible_paths = ["C:\\ffmpeg\\bin", "C:\\Program Files\\FFmpeg\\bin", os.path.expanduser("~\\AppData\\Local\\Microsoft\\WinGet\\Packages")]
for path in possible_paths:
    if os.path.exists(path) and path not in os.environ["PATH"]:
        os.environ["PATH"] += os.path.pathsep + path

# =====================================================================
# SYSTEM CONFIGURATION & INITIALIZATION
# =====================================================================
if API_KEY == "YOUR_WORKING_API_KEY" or not API_KEY:
    print("[ERROR] Please make sure your Gemini API key is active on line 11.")
    sys.exit(1)

genai.configure(api_key=API_KEY)
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"[INFO] Initializing pipeline using system computation layer: {device.upper()}")

# =====================================================================
# STAGE 1: SPEECH TRANSCRIPTION & PHONEME ALIGNMENT
# =====================================================================
def transcribe_audio(audio_path):
    print("[STAGE 1] Loading WhisperX model and transcribing audio...")
    compute_type = "float16" if device == "cuda" else "int8"
    
    model = whisperx.load_model("tiny", device, compute_type=compute_type)
    audio = whisperx.load_audio(audio_path)
    result = model.transcribe(audio, batch_size=16)
    
    print("[STAGE 1] Running phoneme alignment model for timing sync...")
    model_alignment, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
    aligned_result = whisperx.align(result["segments"], model_alignment, metadata, audio, device, return_char_alignments=False)
    
    raw_transcript = ""
    for segment in aligned_result["segments"]:
        start = f"[{int(segment['start'] // 60)}m {int(segment['start'] % 60)}s]"
        raw_transcript += f"{start} {segment['text']}\n"
        
    return raw_transcript

# =====================================================================
# STAGE 2: AI ORCHESTRATION VIA GEMINI CORE
# =====================================================================
def generate_structured_notes(transcript_text):
    print("[STAGE 2] Passing aligned transcript to Google Gemini Core Engine...")
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""
    You are an advanced executive assistant. Analyze the following meeting transcript and generate a highly professional text report.
    
    The summary must follow these structural sections exactly:
    EXECUTIVE SUMMARY
    KEY MILESTONES AND CORE DISCUSSIONS
    STRATEGIC ARCHITECTURAL DECISIONS
    ACTION ITEMS

    Avoid special markdown formatting symbols like triple asterisks or dense blocks. Keep formatting to standard sentences and simple bullet points.

    Raw Transcript Data:
    \"\"\"
    {transcript_text}
    \"\"\"
    """
    response = model.generate_content(prompt)
    return response.text

# =====================================================================
# STAGE 3: AUTOMATED PDF GENERATION (FPDF2 Modern Canvas Engine)
# =====================================================================
class PDFReport(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, "AUTOMATED EXECUTIVE INTELLIGENCE BRIEFING", align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def export_to_pdf(structured_text, output_filename="Verified_Executive_Notes.pdf"):
    print("[STAGE 3] Rendering structured output canvas into local vector PDF file...")
    pdf = PDFReport()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(24, 43, 73) 
    pdf.cell(0, 15, "AI Generated Knowledge Report", align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_fill_color(46, 117, 182)
    pdf.rect(10, 27, 190, 1.5, "F")
    pdf.ln(10)
    
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(40, 40, 40)
    
    lines = structured_text.split('\n')
    for line in lines:
        cleaned_line = line.replace("**", "").replace("*", "-").strip()
        if not cleaned_line:
            continue
            
        # Dynamically treat structural titles
        if cleaned_line.isupper() and len(cleaned_line) > 3:
            pdf.ln(4)
            pdf.set_font("Helvetica", "B", 14)
            pdf.set_text_color(46, 117, 182)
            pdf.cell(0, 8, cleaned_line, align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_font("Helvetica", "", 11)
            pdf.set_text_color(40, 40, 40)
        else:
            # Multi_cell dynamically handles long line wrapping correctly
            pdf.multi_cell(0, 6, cleaned_line, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            
    pdf.output(output_filename)
    print(f"[SUCCESS] Executive notes completely rendered! Output file: {output_filename}")

# =====================================================================
# MAIN RUNTIME INTERFACE EXECUTION
# =====================================================================
if __name__ == "__main__":
    TARGET_AUDIO = "test_meeting.mp3"
    
    if not os.path.exists(TARGET_AUDIO):
        print(f"[ERROR] Could not locate file '{TARGET_AUDIO}' in the active root folder.")
        sys.exit(1)
        
    try:
        transcript = transcribe_audio(TARGET_AUDIO)
        ai_notes = generate_structured_notes(transcript)
        export_to_pdf(ai_notes, output_filename="Verified_Executive_Notes.pdf")
    except Exception as e:
        print(f"\n[CRITICAL RUNTIME BREAK] Execution stopped: {str(e)}")