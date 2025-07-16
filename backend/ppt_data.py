from pptx import Presentation

def extract_text_from_pptx_only(file_path):
    prs = Presentation(file_path)
    slide_texts = []

    for slide in prs.slides:
        text_parts = []

        for shape in slide.shapes:
            if hasattr(shape, "text") and shape.text.strip():
                text_parts.append(shape.text.strip())

        combined_text = "\n".join(text_parts).strip()
        if combined_text:
            slide_texts.append(combined_text)

    return slide_texts
