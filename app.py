import streamlit as st
import os
from organizer import *

st.set_page_config(page_title="Smart File Organizer", layout="centered")

# Sidebar
st.sidebar.title("📂 Smart Organizer")
st.sidebar.write("Clean, organize & optimize your files automatically.")

# Title
st.title("📂 Smart File Organizer")
st.markdown("### Organize your files in one click")

# Default path (cross-platform)
default_path = os.path.expanduser("~/Downloads")

# Input
download_path = st.text_input(
    "📁 Enter Folder Path",
    value=default_path
)

# Options
st.markdown("### ⚙️ Options")

remove_duplicates = st.checkbox("Remove Duplicates", value=True)
enable_renaming = st.checkbox("Rename Files", value=True)

# Progress
progress = st.progress(0)

# Run button
if st.button("🚀 Run Organizer"):

    if not os.path.exists(download_path):
        st.error("❌ Invalid folder path")

    else:
        organizer_path = os.path.join(download_path, "SmartOrganizer")

        st.info("🔄 Processing started...")

        log = []

        # Step 1: Create folders
        create_folders(organizer_path)
        log.append("Folders created")
        progress.progress(20)

        # Step 2: Scan files
        files = scan_files(download_path)
        log.append(f"Scanned {len(files)} files")

        # Step 3: Duplicate removal
        if remove_duplicates:
            duplicates = find_duplicates(files)
            move_duplicates(duplicates, organizer_path)
            log.append(f"Removed {len(duplicates)} duplicates")
        else:
            duplicates = []
            log.append("Duplicate removal skipped")

        progress.progress(50)

        # Step 4: Re-scan after cleanup
        files = scan_files(download_path)

        # Step 5: Organize files
        move_files(files, organizer_path)
        log.append("Files organized successfully")

        progress.progress(100)

        # Success
        st.success("✅ Done!")

        # Summary
        st.markdown("### 📊 Summary")
        st.write(f"Total Files Processed: {len(files)}")
        st.write(f"Duplicates Removed: {len(duplicates)}")

        # Logs
        st.markdown("### 📝 Activity Log")
        for item in log:
            st.write("•", item)