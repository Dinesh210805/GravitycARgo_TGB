#!/usr/bin/env python3
"""
Slack Integration Test Script
Test the Slack commands locally for the hackathon demo
"""
import requests
import json

def test_slack_status_command():
    """Test the /optigenix-status command"""
    url = "http://localhost:5000/slack/commands"
    
    # Simulate Slack slash command payload
    data = {
        'token': 'test-token',
        'team_id': 'T1234567890',
        'team_domain': 'hackathon-team',
        'channel_id': 'C1234567890',
        'channel_name': 'logistics-team',
        'user_id': 'U1234567890',
        'user_name': 'demo-user',
        'command': '/optigenix-status',
        'text': '',
        'response_url': 'https://hooks.slack.com/commands/T1234567890/1234567890/test',
        'trigger_id': '123456789.123456789.test'
    }
    
    try:
        response = requests.post(url, data=data, timeout=10)
        print("✅ Status Command Test")
        print(f"Response Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return True
    except Exception as e:
        print(f"❌ Status Command Test Failed: {e}")
        return False

def test_slack_optimize_command():
    """Test the /optigenix-optimize command"""
    url = "http://localhost:5000/slack/commands"
    
    # Simulate Slack slash command payload
    data = {
        'token': 'test-token',
        'team_id': 'T1234567890',
        'team_domain': 'hackathon-team',
        'channel_id': 'C1234567890',
        'channel_name': 'logistics-team',
        'user_id': 'U1234567890',
        'user_name': 'demo-user',
        'command': '/optigenix-optimize',
        'text': 'urgent',
        'response_url': 'https://hooks.slack.com/commands/T1234567890/1234567890/test',
        'trigger_id': '123456789.123456789.test'
    }
    
    try:
        response = requests.post(url, data=data, timeout=10)
        print("\n✅ Optimize Command Test")
        print(f"Response Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return True
    except Exception as e:
        print(f"❌ Optimize Command Test Failed: {e}")
        return False

def test_slack_integration_health():
    """Test the Slack integration health"""
    url = "http://localhost:5000/slack/test"
    
    try:
        response = requests.post(url, timeout=10)
        print("\n✅ Integration Health Test")
        print(f"Response Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return True
    except Exception as e:
        print(f"❌ Integration Health Test Failed: {e}")
        return False

if __name__ == "__main__":
    print("🚛 OptiGenix Slack Integration Test")
    print("=" * 50)
    
    print("📋 Testing Slack commands locally...")
    print("Make sure your Flask app is running on localhost:5000")
    print()
    
    # Run tests
    tests_passed = 0
    total_tests = 3
    
    if test_slack_status_command():
        tests_passed += 1
    
    if test_slack_optimize_command():
        tests_passed += 1
        
    if test_slack_integration_health():
        tests_passed += 1
    
    print(f"\n📊 Test Results: {tests_passed}/{total_tests} passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Slack integration is ready for demo.")
    else:
        print("⚠️ Some tests failed. Check your Flask app and try again.")
