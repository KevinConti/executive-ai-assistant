import sys
import os
import pytest

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from eaia.gmail import get_recipients

def test_get_recipients_with_real_headers():
    # Exact headers array from the user's email
    headers =  [
        {'name': 'Delivered-To', 'value': 'kevcon80@gmail.com'}, 
        {'name': 'From', 'value': '"Rapoport, Bruce" <Bruce.Rapoport@gehealthcare.com>'}, 
        {'name': 'To', 'value': 'Kevin Conti <kevcon80@gmail.com>'}, 
        {'name': 'CC', 'value': '"Hoffman, James" <James.Hoffman@gehealthcare.com>'}, 
        {'name': 'Subject', 'value': 'RE: Shareholder Important Information'}
        ]
    
    # Test get_recipients with the current user's email
    current_user_email = "kevcon80@gmail.com"
    
    recipients = get_recipients(headers, current_user_email, addn_recipients = [])
    
    print("Actual recipients:", recipients)
    
    # Expected recipients should be cleaned and not include the current user
    expected_recipients = [
        '"Rapoport, Bruce" <Bruce.Rapoport@gehealthcare.com>', 
        '"Hoffman, James" <James.Hoffman@gehealthcare.com>'
    ]
    
    print("Expected recipients:", expected_recipients)
    
    # Detailed comparison
    actual_set = set(recipients)
    expected_set = set(expected_recipients)
    
    # Print out differences
    print("Missing recipients:", expected_set - actual_set)
    print("Extra recipients:", actual_set - expected_set)
    
    # More flexible assertion
    assert actual_set.issuperset(expected_set), "Not all expected recipients found"
    assert actual_set.issubset(expected_set), "Extra unexpected recipients found"

def test_get_recipients_with_simple_emails():
    # Test with simple email addresses without display names
    headers = [
        {'name': 'Delivered-To', 'value': 'user@example.com'},
        {'name': 'From', 'value': 'sender@example.com'},
        {'name': 'To', 'value': 'user@example.com'},
        {'name': 'CC', 'value': 'cc1@example.com, cc2@example.com'},
        {'name': 'Subject', 'value': 'Test Simple Emails'}
    ]
    
    current_user_email = "user@example.com"
    recipients = get_recipients(headers, current_user_email, addn_recipients=[])
    
    expected_recipients = [
        'sender@example.com',
        'cc1@example.com',
        'cc2@example.com'
    ]
    
    actual_set = set(recipients)
    expected_set = set(expected_recipients)
    
    assert actual_set == expected_set, f"Expected {expected_set}, but got {actual_set}"

def test_get_recipients_with_multiple_complex_names():
    # Test with multiple display names containing commas
    headers = [
        {'name': 'Delivered-To', 'value': 'user@example.com'},
        {'name': 'From', 'value': '"Smith, John Jr." <john@example.com>'},
        {'name': 'To', 'value': 'user@example.com'},
        {'name': 'CC', 'value': '"Doe, Jane, PhD" <jane@example.com>, "O\'Connor, Mary, MBA" <mary@example.com>'},
        {'name': 'Subject', 'value': 'Test Complex Names'}
    ]
    
    current_user_email = "user@example.com"
    recipients = get_recipients(headers, current_user_email, addn_recipients=[])
    
    expected_recipients = [
        '"Smith, John Jr." <john@example.com>',
        '"Doe, Jane, PhD" <jane@example.com>',
        '"O\'Connor, Mary, MBA" <mary@example.com>'
    ]
    
    actual_set = set(recipients)
    expected_set = set(expected_recipients)
    
    assert actual_set == expected_set, f"Expected {expected_set}, but got {actual_set}"
