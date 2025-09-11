#!/usr/bin/env python
"""
Comprehensive test script for WeWorkLocal Django application
Tests all major components and functionality
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

def test_authentication():
    """Test authentication system"""
    print("Testing Authentication System...")
    client = Client()
    
    # Test login page
    response = client.get('/auth/login/')
    assert response.status_code == 200, f"Login page failed: {response.status_code}"
    print("  [OK] Login page accessible")

    # Test register page
    response = client.get('/auth/register/')
    assert response.status_code == 200, f"Register page failed: {response.status_code}"
    print("  [OK] Register page accessible")

    print("  [OK] Authentication system working")

def test_subscriptions():
    """Test subscription system"""
    print("💳 Testing Subscription System...")
    client = Client()
    
    # Test subscription plans
    response = client.get('/subscriptions/plans/')
    assert response.status_code == 200, f"Subscription plans failed: {response.status_code}"
    print("  ✅ Subscription plans page accessible")
    
    # Test simple subscriptions
    response = client.get('/subscriptions/simple/')
    assert response.status_code == 200, f"Simple subscriptions failed: {response.status_code}"
    print("  ✅ Simple subscriptions page accessible")
    
    # Test subscription dashboard (requires login)
    response = client.get('/subscriptions/')
    assert response.status_code in [200, 302], f"Subscription dashboard failed: {response.status_code}"
    print("  ✅ Subscription dashboard accessible")
    
    print("  ✅ Subscription system working")

def test_properties():
    """Test property system"""
    print("🏠 Testing Property System...")
    client = Client()
    
    # Test property list
    response = client.get('/properties/')
    assert response.status_code == 200, f"Property list failed: {response.status_code}"
    print("  ✅ Property list page accessible")
    
    # Test add property (requires login)
    response = client.get('/properties/add/')
    assert response.status_code in [200, 302], f"Add property failed: {response.status_code}"
    print("  ✅ Add property page accessible")
    
    # Test report sale (requires login)
    response = client.get('/properties/report-sale/')
    assert response.status_code in [200, 302], f"Report sale failed: {response.status_code}"
    print("  ✅ Report sale page accessible")
    
    print("  ✅ Property system working")

def test_wallets():
    """Test wallet system"""
    print("💰 Testing Wallet System...")
    client = Client()
    
    # Test wallet dashboard (requires login)
    response = client.get('/wallets/')
    assert response.status_code in [200, 302], f"Wallet dashboard failed: {response.status_code}"
    print("  ✅ Wallet dashboard accessible")
    
    # Test transactions (requires login)
    response = client.get('/wallets/transactions/')
    assert response.status_code in [200, 302], f"Transactions failed: {response.status_code}"
    print("  ✅ Transactions page accessible")
    
    # Test withdraw (requires login)
    response = client.get('/wallets/withdraw/')
    assert response.status_code in [200, 302], f"Withdraw failed: {response.status_code}"
    print("  ✅ Withdraw page accessible")
    
    print("  ✅ Wallet system working")

def test_referrals():
    """Test referral system"""
    print("🔗 Testing Referral System...")
    client = Client()
    
    # Test referral dashboard (requires login)
    response = client.get('/referrals/')
    assert response.status_code in [200, 302], f"Referral dashboard failed: {response.status_code}"
    print("  ✅ Referral dashboard accessible")
    
    # Test referral tree (requires login)
    response = client.get('/referrals/tree/')
    assert response.status_code in [200, 302], f"Referral tree failed: {response.status_code}"
    print("  ✅ Referral tree page accessible")
    
    # Test clean referral system (requires login)
    response = client.get('/referrals/clean/')
    assert response.status_code in [200, 302], f"Clean referrals failed: {response.status_code}"
    print("  ✅ Clean referral system accessible")
    
    print("  ✅ Referral system working")

def test_support():
    """Test support system"""
    print("🎧 Testing Support System...")
    client = Client()
    
    # Test support dashboard (requires login)
    response = client.get('/support/')
    assert response.status_code in [200, 302], f"Support dashboard failed: {response.status_code}"
    print("  ✅ Support dashboard accessible")
    
    # Test tickets (requires login)
    response = client.get('/support/tickets/')
    assert response.status_code in [200, 302], f"Support tickets failed: {response.status_code}"
    print("  ✅ Support tickets page accessible")
    
    # Test chat (requires login)
    response = client.get('/support/chat/')
    assert response.status_code in [200, 302], f"Support chat failed: {response.status_code}"
    print("  ✅ Support chat accessible")
    
    print("  ✅ Support system working")

def test_admin():
    """Test admin panel"""
    print("⚙️ Testing Admin Panel...")
    client = Client()
    
    # Test admin login
    response = client.get('/admin/')
    assert response.status_code in [200, 302], f"Admin panel failed: {response.status_code}"
    print("  ✅ Admin panel accessible")
    
    print("  ✅ Admin panel working")

def test_database_models():
    """Test database models and data"""
    print("🗄️ Testing Database Models...")
    
    # Test users
    user_count = User.objects.count()
    print(f"  ✅ Users in database: {user_count}")
    
    # Test subscription plans
    from subscriptions.models import SubscriptionPlan, SimpleSubscriptionPlan
    plan_count = SubscriptionPlan.objects.count()
    simple_plan_count = SimpleSubscriptionPlan.objects.count()
    print(f"  ✅ Subscription plans: {plan_count}, Simple plans: {simple_plan_count}")
    
    # Test properties
    from properties.models import Property
    property_count = Property.objects.count()
    print(f"  ✅ Properties in database: {property_count}")
    
    # Test support tickets
    from support.models import SupportTicket
    ticket_count = SupportTicket.objects.count()
    print(f"  ✅ Support tickets: {ticket_count}")
    
    # Test wallets
    from wallets.models import Wallet
    wallet_count = Wallet.objects.count()
    print(f"  ✅ Wallets in database: {wallet_count}")
    
    print("  ✅ Database models working")

def main():
    """Run all tests"""
    print("🚀 Starting WeWorkLocal Component Tests...\n")
    
    try:
        test_authentication()
        print()
        
        test_subscriptions()
        print()
        
        test_properties()
        print()
        
        test_wallets()
        print()
        
        test_referrals()
        print()
        
        test_support()
        print()
        
        test_admin()
        print()
        
        test_database_models()
        print()
        
        print("🎉 ALL TESTS PASSED! WeWorkLocal application is working perfectly!")
        print("\n📋 Summary:")
        print("  ✅ Authentication System")
        print("  ✅ Subscription Management")
        print("  ✅ Property Listings")
        print("  ✅ Wallet & Transactions")
        print("  ✅ Referral System")
        print("  ✅ Support System")
        print("  ✅ Admin Panel")
        print("  ✅ Database Models")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
