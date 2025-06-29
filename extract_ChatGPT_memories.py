import os
import re
from bs4 import BeautifulSoup
from datetime import datetime

def extract_and_debug_paragraphs(html_file_path, output_file_path, target_phrase="Model set context updated"):
    """
    Extract paragraphs and provide detailed debug information about skipped messages.
    
    Args:
        html_file_path (str): Path to the HTML file
        output_file_path (str): Path to the output text file
        target_phrase (str): The phrase to search for
    """
    
    try:
        # Read the HTML file
        with open(html_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find all <pre class="message"> elements
        message_blocks = soup.find_all('pre', class_='message')
        
        print(f"=== EXTRACTION AND DEBUG REPORT ===")
        print(f"Total <pre class='message'> blocks found: {len(message_blocks)}")
        
        target_instances = []
        skipped_instances = []
        extracted_messages = []
        seen_content = set()
        

        
        for i, block in enumerate(message_blocks):
            # Check if this block contains the target phrase
            block_text = block.get_text()
            
            if target_phrase.lower() in block_text.lower():
                # Check if this is a ChatGPT message with the target phrase
                author_div = block.find('div', class_='author')
                if author_div and 'ChatGPT' in author_div.get_text():
                    
                    instance_info = {
                        'position': i,
                        'block_index': i,
                        'has_previous': i > 0,
                        'previous_content': None,
                        'reason_skipped': None,
                        'block_text_preview': block_text[:100] + "..." if len(block_text) > 100 else block_text
                    }
                    
                    # Find the previous message block
                    if i > 0:
                        prev_block = message_blocks[i - 1]
                        
                        # Extract author and content from previous block
                        prev_author_div = prev_block.find('div', class_='author')
                        prev_content_divs = prev_block.find_all('div')
                        
                        if prev_author_div and len(prev_content_divs) >= 2:
                            author = prev_author_div.get_text(strip=True)
                            content_div = prev_content_divs[1]
                            content = content_div.get_text(strip=True)
                            
                            instance_info['previous_content'] = content
                            instance_info['previous_author'] = author
                            
                            if content:  # Only add if there's actual content
                                # Check for duplicates
                                if content in seen_content:
                                    instance_info['reason_skipped'] = 'Duplicate content'
                                    skipped_instances.append(instance_info)
                                else:
                                    # Add to extracted messages
                                    message_info = {
                                        'author': author,
                                        'content': content,
                                        'position': i
                                    }
                                    extracted_messages.append(message_info)
                                    seen_content.add(content)
                                    target_instances.append(instance_info)
                            else:
                                instance_info['reason_skipped'] = 'Empty previous content'
                                skipped_instances.append(instance_info)
                        else:
                            instance_info['reason_skipped'] = 'Invalid previous block structure'
                            skipped_instances.append(instance_info)
                    else:
                        instance_info['reason_skipped'] = 'No previous message (first in conversation)'
                        skipped_instances.append(instance_info)
        
        # Write results to output file
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(f"Memories are the paragraph before the phrase: '{target_phrase}'\n")
            output_file.write(f"Extraction date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            output_file.write(f"Source file: {html_file_path}\n")
            output_file.write(f"Total memories found: {len(target_instances) + len(skipped_instances)}\n")
            output_file.write(f"Successfully extracted memories: {len(extracted_messages)}\n")
            output_file.write(f"Skipped memory records: {len(skipped_instances)}\n")
            output_file.write("=" * 50 + "\n\n")
            
            # Write extracted messages
            output_file.write("EXTRACTED MEMORIES:\n")
            output_file.write("=" * 30 + "\n\n")
            
            for i, message in enumerate(extracted_messages, 1):
                output_file.write(f"Memory {i} (Author: {message['author']}):\n")
                output_file.write(f"Block position: {message['position']}\n")
                output_file.write(f"Content: {message['content']}\n")
                output_file.write("\n" + "-" * 30 + "\n\n")
            
            # Write skipped messages debug info
            if skipped_instances:
                output_file.write("\n\nSKIPPED MEMORIES DEBUG INFO:\n")
                output_file.write("=" * 35 + "\n\n")
                
                skip_reasons = {}
                for instance in skipped_instances:
                    reason = instance['reason_skipped']
                    if reason not in skip_reasons:
                        skip_reasons[reason] = []
                    skip_reasons[reason].append(instance)
                
                for reason, instances in skip_reasons.items():
                    output_file.write(f"{reason.upper()}: {len(instances)} memories\n")
                    output_file.write("-" * 40 + "\n")
                    
                    for i, instance in enumerate(instances, 1):
                        output_file.write(f"\nSkipped memory record {i}:\n")
                        output_file.write(f"  Block position: {instance['position']} (out of {len(message_blocks)} total blocks)\n")
                        if instance['previous_content']:
                            output_file.write(f"  Memory: {instance['previous_content']}\n")
                        output_file.write(f"  {'-' * 30}\n")
                    
                    output_file.write("\n")
                
                output_file.write("\nHOW TO FIND BLOCKS MANUALLY:\n")
                output_file.write("1. Open your HTML file in a text editor (Notepad++, VS Code, etc.)\n")
                output_file.write("2. Use Ctrl+F to search for the text previews shown above\n")
                output_file.write("3. Block position X means it's the X-th <pre class=\"message\"> tag in the file\n")
                output_file.write("4. You can also search for '<pre class=\"message\">' and count to find the right block\n")
                output_file.write("If you found this tool helpful, consider donating to ko-fi.com/tonalfillies7\n")
        
        # Console output
        print(f"\nTotal instances of '{target_phrase}' found: {len(target_instances) + len(skipped_instances)}")
        print(f"Successfully extracted: {len(extracted_messages)}")
        print(f"Skipped instances: {len(skipped_instances)}")
        
        if skipped_instances:
            print(f"\n=== SKIPPED MEMORIES SUMMARY ===")
            skip_reasons = {}
            for instance in skipped_instances:
                reason = instance['reason_skipped']
                if reason not in skip_reasons:
                    skip_reasons[reason] = []
                skip_reasons[reason].append(instance)
            
            for reason, instances in skip_reasons.items():
                print(f"{reason}: {len(instances)} instances")
                for i, instance in enumerate(instances, 1):
                    print(f"  {i}. Block {instance['position']}")
                    if instance['previous_content']:
                        preview = instance['previous_content'][:60]
                        print(f"     Content: {preview}{'...' if len(instance['previous_content']) > 60 else ''}")
        
        print(f"\nResults saved to: {output_file_path}")
        print(f"Full debug information written to the output file!")
        
        # Manual count verification
        manual_count = html_content.lower().count(target_phrase.lower())
        print(f"\nVerification: Manual count of '{target_phrase}' in HTML: {manual_count}")
        
        return extracted_messages
        
    except FileNotFoundError:
        print(f"Error: HTML file not found at {html_file_path}")
        return []
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return []

def main():
    """
    Main function to run the combined extraction and debug script
    """
    # Configuration
    html_file_path = input("Enter the path to your HTML file: ").strip()
    
    # Remove quotes if user pasted path with quotes
    html_file_path = html_file_path.strip('"\'')
    
    # Check if file exists
    if not os.path.exists(html_file_path):
        print(f"File not found: {html_file_path}")
        return
    
    # Generate output file name
    base_name = os.path.splitext(os.path.basename(html_file_path))[0]
    output_file_path = f"{base_name}_extracted_with_debug.txt"
    
    # Ask user if they want to specify a different output location
    custom_output = input(f"Output will be saved as '{output_file_path}'. Press Enter to continue or type a new filename: ").strip()
    if custom_output:
        output_file_path = custom_output
    
    # Extract and debug
    print("Processing HTML file...")
    messages = extract_and_debug_paragraphs(html_file_path, output_file_path)
    
    if messages:
        print(f"\nExtracted memories preview:")
        for i, msg in enumerate(messages[:3], 1):  # Show first 3 messages
            print(f"\n{i}. Author: {msg['author']}")
            print(f"   Memory: {msg['content'][:100]}{'...' if len(msg['content']) > 100 else ''}")
            print(f"   Location: Block {msg['position']}")
        
        if len(messages) > 3:
            print(f"\n... and {len(messages) - 3} more memories")
    
    print(f"\nCheck the output file for complete results and debug information!")

if __name__ == "__main__":
    # Check if BeautifulSoup is installed
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        print("BeautifulSoup4 is required. Please install it by running:")
        print("pip install beautifulsoup4")
        exit(1)
    
    main()
