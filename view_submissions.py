#!/usr/bin/env python3
"""View all submissions from the submissions.json file."""

import json
from pathlib import Path
from datetime import datetime

SUBMISSIONS_FILE = "submissions.json"

def view_submissions():
    """Display all submissions in a readable format."""
    
    if not Path(SUBMISSIONS_FILE).exists():
        print(f"❌ No submissions file found ({SUBMISSIONS_FILE})")
        print("💡 Submissions will be created when users submit forms.")
        return
    
    try:
        with open(SUBMISSIONS_FILE, 'r', encoding='utf-8') as f:
            submissions = json.load(f)
    except json.JSONDecodeError:
        print(f"❌ Error reading {SUBMISSIONS_FILE}")
        return
    
    if not submissions:
        print(f"📭 No submissions yet.")
        return
    
    print(f"\n{'='*70}")
    print(f"📊 TOTAL SUBMISSIONS: {len(submissions)}")
    print(f"{'='*70}\n")
    
    for i, submission in enumerate(submissions, 1):
        print(f"{'─'*70}")
        print(f"📝 SUBMISSION #{i}")
        print(f"{'─'*70}")
        print(f"🆔 ID: {submission.get('submission_id', 'N/A')}")
        print(f"📅 Date: {submission.get('timestamp', 'N/A')}")
        print(f"📋 Form Type: {submission.get('form_type', 'N/A')}")
        print(f"🔘 Button: {submission.get('button_text', 'N/A')}")
        
        user_info = submission.get('user_info', {})
        print(f"\n👤 USER INFO:")
        print(f"   • ID: {user_info.get('user_id', 'N/A')}")
        print(f"   • Username: @{user_info.get('username', 'N/A')}")
        print(f"   • Name: {user_info.get('first_name', '')} {user_info.get('last_name', '')}")
        
        data = submission.get('data', {})
        if data:
            print(f"\n📝 SUBMITTED DATA:")
            for key, value in data.items():
                print(f"   • {key}: {value}")
        
        print()
    
    print(f"{'='*70}\n")

def export_to_csv():
    """Export submissions to CSV format."""
    import csv
    
    if not Path(SUBMISSIONS_FILE).exists():
        print(f"❌ No submissions file found")
        return
    
    try:
        with open(SUBMISSIONS_FILE, 'r', encoding='utf-8') as f:
            submissions = json.load(f)
    except json.JSONDecodeError:
        print(f"❌ Error reading submissions file")
        return
    
    if not submissions:
        print(f"📭 No submissions to export.")
        return
    
    csv_file = "submissions.csv"
    
    # Collect all possible fields
    all_fields = set()
    for submission in submissions:
        all_fields.update(submission.get('data', {}).keys())
    
    # Create CSV
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['timestamp', 'submission_id', 'form_type', 'button_text', 
                     'user_id', 'username', 'first_name', 'last_name'] + sorted(all_fields)
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for submission in submissions:
            row = {
                'timestamp': submission.get('timestamp'),
                'submission_id': submission.get('submission_id'),
                'form_type': submission.get('form_type'),
                'button_text': submission.get('button_text'),
                'user_id': submission.get('user_info', {}).get('user_id'),
                'username': submission.get('user_info', {}).get('username'),
                'first_name': submission.get('user_info', {}).get('first_name'),
                'last_name': submission.get('user_info', {}).get('last_name'),
            }
            row.update(submission.get('data', {}))
            writer.writerow(row)
    
    print(f"✅ Exported {len(submissions)} submissions to {csv_file}")

def show_stats():
    """Show statistics about submissions."""
    if not Path(SUBMISSIONS_FILE).exists():
        print(f"❌ No submissions file found")
        return
    
    try:
        with open(SUBMISSIONS_FILE, 'r', encoding='utf-8') as f:
            submissions = json.load(f)
    except json.JSONDecodeError:
        print(f"❌ Error reading submissions file")
        return
    
    if not submissions:
        print(f"📭 No submissions yet.")
        return
    
    # Calculate statistics
    form_types = {}
    button_texts = {}
    
    for submission in submissions:
        form_type = submission.get('form_type', 'Unknown')
        button_text = submission.get('button_text', 'Unknown')
        
        form_types[form_type] = form_types.get(form_type, 0) + 1
        button_texts[button_text] = button_texts.get(button_text, 0) + 1
    
    print(f"\n{'='*70}")
    print(f"📊 SUBMISSION STATISTICS")
    print(f"{'='*70}\n")
    
    print(f"📋 Total Submissions: {len(submissions)}")
    print(f"\n📂 By Form Type:")
    for form_type, count in sorted(form_types.items(), key=lambda x: x[1], reverse=True):
        print(f"   • {form_type}: {count}")
    
    print(f"\n🔘 By Button:")
    for button, count in sorted(button_texts.items(), key=lambda x: x[1], reverse=True):
        print(f"   • {button}: {count}")
    
    # Latest submission
    if submissions:
        latest = submissions[-1]
        print(f"\n📅 Latest Submission:")
        print(f"   • Date: {latest.get('timestamp')}")
        print(f"   • Type: {latest.get('form_type')}")
        print(f"   • From: @{latest.get('user_info', {}).get('username', 'N/A')}")
    
    print(f"\n{'='*70}\n")

def main():
    """Main menu."""
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "stats":
            show_stats()
        elif command == "export":
            export_to_csv()
        else:
            view_submissions()
    else:
        print("\n📋 SUBMISSIONS VIEWER")
        print("="*40)
        print("1. View all submissions")
        print("2. Show statistics")
        print("3. Export to CSV")
        print("4. Exit")
        print("="*40)
        
        choice = input("\nChoose an option (1-4): ").strip()
        
        if choice == "1":
            view_submissions()
        elif choice == "2":
            show_stats()
        elif choice == "3":
            export_to_csv()
        elif choice == "4":
            print("👋 Goodbye!")
        else:
            print("❌ Invalid option")

if __name__ == "__main__":
    main()

