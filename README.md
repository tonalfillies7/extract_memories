# ChatGPT Memories Extraction Script
## Complete Setup and Usage Guide

### Overview

This Python script automatically extracts the memories ChatGPT has saved through the HTML conversation files you can download. It finds instances of the phrase "Model set context updated" and captures the message that appears immediately before it, which is the saved memory.


---

## What the Script Does

The script searches for this HTML pattern:
```html
<pre class="message">
  <div class="author">ChatGPT</div>
  <div>Your saved memory here</div>
</pre>
<pre class="message">
  <div class="author">ChatGPT</div>
  <div>Model set context updated.</div>
</pre>
```

**Result:** Extracts "Your saved memory here" and saves it to a text file.

---

## 🛠️ Setup Instructions

### Step 1: Install Python
- **Windows:** Download from [python.org](https://python.org)
  - ⚠️ **IMPORTANT:** Check "Add Python to PATH" during installation
- **Mac:** Download from [python.org](https://python.org) or use Homebrew: `brew install python3`

### Step 2: Install Required Library
Open Command Prompt (Windows) or Terminal (Mac) and run:

**Windows:**
```bash
pip install beautifulsoup4
```

**Mac:**
```bash
pip3 install beautifulsoup4
```

**If pip doesn't work, try:**
```bash
python -m pip install beautifulsoup4
```

### Step 3: Get the Script
Save the provided Python script `extract_ChatGPT_memories.py` on your computer.

---
## Download your data from ChatGPT.
Follow these instructions to download your data: https://help.openai.com/en/articles/7260999-how-do-i-export-my-chatgpt-history-and-data
Then locate the chat.html file which contains all your conversations with ChatGPT and open it in a browser.

## Preparing Your HTML File

### Method 1: Save Complete Page (Recommended)
1. Open your conversation in the browser
2. **Right-click** → **"Save page as..."**
3. Choose **"Web Page, Complete"** format
4. Save to Desktop or Downloads folder

### Method 2: View Source Method (Most Reliable)
1. **Right-click** on the page → **"View Page Source"**
2. **Ctrl+A** to select all → **Ctrl+C** to copy
3. Open **Notepad** (Windows) or **TextEdit** (Mac)
4. **Paste** the content
5. **Save as** `.html` file

### Important Notes:
- **File size check:** A properly saved HTML file should be several MB, not just a few KB
- **Large script tags:** If your HTML file is huge (100MB+), you may need to remove large `<script>` tags that contain encoded data
- **1-byte files:** If your file is only 1 byte, the save failed - try again with Method 2

---

## How to Use the Script

### Step 1: Run the Script
**Windows:**
```bash
python extract_ChatGPT_memories.py
```

**Mac:**
```bash
python3 extract_ChatGPT_memories.py
```

### Step 2: Follow the Prompts
1. **Enter HTML file path:** Type the full path to your HTML file
   - You can drag and drop the file into the terminal to get the path
   - Example: `C:\Users\YourName\Downloads\chat.html`

2. **Choose output filename** (optional)
   - Press Enter to use default name
   - Or type a custom filename like `my_extracted_messages.txt`

### Step 3: Review Results
The script will:
- Show you how many messages were found
- Display a preview of the first few extracted messages
- Save all results to a text file

---

## Output Format

The generated text file contains:
- **Header:** Extraction date, source file, and summary
- **Numbered messages:** Each with author name and full content
- **Clean formatting:** Clear separators between messages

Example output:
```
Messages extracted before 'Model set context updated'
Extraction date: 2025-06-29 15:30:45
Source file: conversation.html
==================================================

Message 1 (Author: ChatGPT):
I am a poor lonesome cowboy far away from home.

------------------------------

Message 2 (Author: User):
Please analyze this data and provide insights.

------------------------------
```

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'bs4'"
**Solution:** BeautifulSoup isn't installed properly
```bash
python -m pip install beautifulsoup4
```

### "pip is not recognized as an internal command"
**Solution:** Python isn't in PATH or isn't installed
1. Reinstall Python with "Add to PATH" checked
2. Or use: `python -m pip install beautifulsoup4`

### "No messages found in HTML file"
**Solutions:**
1. **Check file size:** Should be several MB, not 1 byte
2. **Re-save HTML:** Try the "View Source" method
3. **Remove large script tags:** If file is 100MB+, remove `<script>` tags containing encoded data

### Script runs but finds 0 results
**Possible causes:**
- HTML structure is different than expected
- The phrase "Model set context updated" isn't in the file
- File didn't save properly

**Debug steps:**
1. Open the HTML file in a text editor
2. Search for "Model set context updated" - if not found, check the exact phrase
3. Look for `<pre class="message">` tags - if not found, the structure is different

---

## Advanced Tips

### File Paths with Spaces
If your file path contains spaces, wrap it in quotes:
```
"C:\Users\Your Name\Downloads\my conversation.html"
```

---

## Common Questions

**Q: Is this safe to use?**
A: Yes, the script only reads HTML files and creates text files. It doesn't modify your original files.

**Q: Can I use this with other chat platforms?**
A: The script is designed for the specific HTML structure of the ChatGPT conversation file. Other platforms may need modifications.

**Q: Can I extract different types of messages?**
A: Yes, modify the `target_phrase` variable to search for different text patterns.

---


*This script automates the tedious process of manually searching through conversation exports, saving hours of manual work. If you found this tool helpful, consider donating to ko-fi.com/tonalfillies7*
