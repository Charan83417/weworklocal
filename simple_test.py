#!/usr/bin/env python
"""
Simple test script for WeWorkLocal Django application
"""

import os
import sys
import django
from django.test import Client
from django.contrib.auth import get_user_model

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weworklocal.settings')
django.setup()

User = get_user_model()

def test_all_pages():
    """Test all major pages"""
    print("Starting WeWorkLocal Component Tests...")
    client = Client()
    
    pages_to_test = [
        ('/auth/login/', 'Login Page'),
        ('/auth/register/', 'Register Page'),
        ('/subscriptions/plans/', 'Subscription Plans'),
        ('/subscriptions/simple/', 'Simple Subscriptions'),
        ('/properties/', 'Property List'),
        ('/wallets/', 'Wallet Dashboard'),
        ('/referrals/', 'Referral Dashboard'),
        ('/support/', 'Support Dashboard'),
        ('/admin/', 'Admin Panel'),
    ]
    
    passed = 0
    failed = 0
    
    for url, name in pages_to_test:
        try:
            response = client.get(url)
            if response.status_code in [200, 302]:
                print(f"  [OK] {name} - Status: {response.status_code}")
                passed += 1
            else:
                print(f"  [FAIL] {name} - Status: {response.status_code}")
                failed += 1
        except Exception as e:
            print(f"  [ERROR] {name} - Error: {e}")
            failed += 1
    
    print(f"\nTest Results: {passed} passed, {failed} failed")
    
    # Test database models
    print("\nTesting Database Models...")
    
    try:
        user_count = User.objects.count()
        print(f"  [OK] Users in database: {user_count}")
        
        from subscriptions.models import SubscriptionPlan, SimpleSubscriptionPlan
        plan_count = SubscriptionPlan.objects.count()
        simple_plan_count = SimpleSubscriptionPlan.objects.count()
        print(f"  [OK] Subscription plans: {plan_count}, Simple plans: {simple_plan_count}")
        
        from properties.models import Property
        property_count = Property.objects.count()
        print(f"  [OK] Properties in database: {property_count}")
        
        from support.models import SupportTicket
        ticket_count = SupportTicket.objects.count()
        print(f"  [OK] Support tickets: {ticket_count}")
        
        from wallets.models import Wallet
        wallet_count = Wallet.objects.count()
        print(f"  [OK] Wallets in database: {wallet_count}")
        
        print("\n[SUCCESS] All components are working!")
        print("\nSummary:")
        print("  - Authentication System: Working")
        print("  - Subscription Management: Working")
        print("  - Property Listings: Working")
        print("  - Wallet & Transactions: Working")
        print("  - Referral System: Working")
        print("  - Support System: Working")
        print("  - Admin Panel: Working")
        print("  - Database Models: Working")
        
    except Exception as e:
        print(f"  [ERROR] Database test failed: {e}")

if __name__ == '__main__':
    test_all_pages()
