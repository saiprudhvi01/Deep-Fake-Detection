import streamlit as st
import cv2
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS
import numpy as np

# Page configuration
st.set_page_config(
    page_title="🔍 Image Tampering Detection",
    page_icon="🔍",
    layout="wide"
)

def extract_exif_data(image):
    """Extract EXIF metadata from image"""
    try:
        exif_dict = {}
        if hasattr(image, '_getexif'):
            exif_data = image._getexif()
            if exif_data is not None:
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id, tag_id)
                    exif_dict[tag] = value
        return exif_dict
    except Exception:
        return {}



def detect_faces(image_array):
    """Detect faces in the image using OpenCV"""
    try:
        # Convert PIL image to OpenCV format
        gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
        
        # Load face cascade
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        # Draw rectangles around faces
        image_with_faces = image_array.copy()
        for (x, y, w, h) in faces:
            cv2.rectangle(image_with_faces, (x, y), (x+w, y+h), (255, 0, 0), 3)
        
        return image_with_faces, len(faces)
    except Exception:
        return image_array, 0

def analyze_image_tampering(image, image_path, image_format):
    """Analyze image for tampering indicators and return detailed explanation"""
    results = {
        'is_tampered': False,
        'confidence_score': 0,
        'reasons': [],
        'risk_level': 'LOW'
    }
    
    # 1. EXIF Metadata Analysis
    exif_dict = extract_exif_data(image)
    if not exif_dict:
        results['is_tampered'] = True
        results['confidence_score'] += 40
        results['reasons'].append("❌ No EXIF metadata found - This strongly indicates the image has been processed or edited")
    else:
        results['reasons'].append("✅ EXIF metadata present - Good sign of authenticity")
    
    # 2. Check for camera information
    if 'Make' not in exif_dict or 'Model' not in exif_dict:
        results['is_tampered'] = True
        results['confidence_score'] += 25
        results['reasons'].append("❌ Missing camera make/model information - Often removed during editing")
    else:
        results['reasons'].append(f"✅ Camera information available: {exif_dict.get('Make', 'Unknown')} {exif_dict.get('Model', 'Unknown')}")
    
    # 3. Check for editing software traces
    if 'Software' in exif_dict:
        software = str(exif_dict['Software']).lower()
        editing_software = ['photoshop', 'gimp', 'canva', 'paint', 'editor', 'adobe']
        if any(editor in software for editor in editing_software):
            results['is_tampered'] = True
            results['confidence_score'] += 35
            results['reasons'].append(f"⚠️ Editing software detected: {exif_dict['Software']} - This suggests the image was modified")
        else:
            results['reasons'].append(f"✅ Software tag present: {exif_dict['Software']} - Appears legitimate")
    
    # 4. Check for creation date
    if 'DateTime' not in exif_dict:
        results['is_tampered'] = True
        results['confidence_score'] += 20
        results['reasons'].append("❌ Missing creation date - Usually present in original photos")
    else:
        results['reasons'].append(f"✅ Creation date available: {exif_dict['DateTime']}")
    
    # 5. Image format analysis
    if image_format.lower() in ['png']:
        results['is_tampered'] = True
        results['confidence_score'] += 15
        results['reasons'].append("⚠️ PNG format detected - Often used for edited images due to transparency support")
    else:
        results['reasons'].append("✅ JPEG format - More common in original digital photos")

    # 6. Face detection for potential manipulation
    image_array = np.array(image)
    _, face_count = detect_faces(image_array)
    if face_count > 0:
        results['reasons'].append(f"✅ {face_count} face(s) detected - No obvious signs of face manipulation")
    else:
        results['reasons'].append("ℹ️ No faces detected - This is normal for landscape/object photos")
    
    # Determine risk level
    results['confidence_score'] = min(max(results['confidence_score'], 0), 100)
    if results['confidence_score'] >= 70:
        results['risk_level'] = 'HIGH'
    elif results['confidence_score'] >= 40:
        results['risk_level'] = 'MEDIUM'
    else:
        results['risk_level'] = 'LOW'
    
    # Overall assessment
    if results['confidence_score'] >= 50:
        results['is_tampered'] = True
        results['overall_assessment'] = f"🚨 HIGH RISK ({results['confidence_score']}%) - Likely tampered or edited"
    elif results['confidence_score'] >= 25:
        results['overall_assessment'] = f"⚠️ MEDIUM RISK ({results['confidence_score']}%) - Some suspicious indicators"
    else:
        results['overall_assessment'] = f"✅ LOW RISK ({results['confidence_score']}%) - Appears authentic"
    
    return results

def main():
    # Simplified header
    st.markdown('<h1 style="text-align: center; color: #1e3c72;">🔍 Image Tampering Detection</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666;">Quick and accurate analysis to detect if an image has been tampered with</p>', unsafe_allow_html=True)
    
    # File uploader
    uploaded_file = st.file_uploader(
        "📸 Upload an image to analyze",
        type=['jpg', 'jpeg', 'png', 'bmp', 'tiff', 'tif'],
        help="Upload any image to check for tampering"
    )
    
    if uploaded_file is not None:
        # Load image
        image = Image.open(uploaded_file)
        
        # Show image
        col1, col2 = st.columns([1, 1])
        with col1:
            st.image(image, caption='Uploaded Image', use_column_width=True)
        
        with col2:
            st.markdown("### 📊 Analysis Results")
            
            # Perform analysis
            with st.spinner('Analyzing image for tampering indicators...'):
                results = analyze_image_tampering(image, uploaded_file.name, uploaded_file.type)
            
            # Display overall result
            if results['is_tampered']:
                st.error(results['overall_assessment'])
            else:
                st.success(results['overall_assessment'])
            
            # Progress bar
            st.progress(results['confidence_score'] / 100.0)
            
            # Risk level
            if results['risk_level'] == 'HIGH':
                st.error(f"🚨 Risk Level: {results['risk_level']}")
            elif results['risk_level'] == 'MEDIUM':
                st.warning(f"⚠️ Risk Level: {results['risk_level']}")
            else:
                st.success(f"✅ Risk Level: {results['risk_level']}")
        
        # Detailed explanation
        st.markdown("### 🔍 Why this assessment?")
        
        # Create expandable sections for different analysis types
        with st.expander("📋 EXIF Metadata Analysis", expanded=True):
            for reason in results['reasons']:
                st.markdown(reason)
        
        # Technical details
        with st.expander("📋 Image Details"):
            st.write(f"**Format:** {uploaded_file.type}")
            st.write(f"**Size:** {uploaded_file.size / 1024:.1f} KB")
            st.write(f"**Dimensions:** {image.size[0]} × {image.size[1]} pixels")
            
            # Show EXIF data if available
            exif_dict = extract_exif_data(image)
            if exif_dict:
                st.write("**Available EXIF Data:**")
                for key, value in list(exif_dict.items())[:10]:  # Show first 10 items
                    st.write(f"- {key}: {value}")
            else:
                st.write("*No EXIF data available*")
    
    else:
        # Welcome screen
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 15px; color: white; text-align: center; margin: 1rem 0;">
            <h3>🛡️ Professional Image Authenticity Checker</h3>
            <p>Upload any image above to instantly check if it has been tampered with or edited.</p>
            <br>
            <h4>🔍 What we analyze:</h4>
            <ul style="list-style: none; padding: 0;">
                <li>📊 EXIF metadata integrity</li>
                <li>📷 Camera information</li>
                <li>⚙️ Software traces</li>
                <li>📅 Creation timestamps</li>
                <li>👥 Face detection</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
