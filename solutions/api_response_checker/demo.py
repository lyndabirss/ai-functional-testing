"""
API Response Quality Checker - Demonstration

This demo shows 4 real-world scenarios demonstrating the difference between:
- Automated API schema validation (structure checking)
- Quality Intelligence (context-aware analysis)

Each example is based on real testing challenges in recruitment systems.
"""

import sys
import os

def print_banner():
    print("\n" + "="*70)
    print(" "*15 + "API RESPONSE QUALITY CHECKER")
    print(" "*20 + "Demonstration Suite")
    print("="*70)
    print("\nThis tool demonstrates Quality Intelligence:")
    print("  Structure validation + AI-powered quality assessment")
    print("\n4 Real-world scenarios from recruitment system testing")
    print("="*70 + "\n")

def print_menu():
    print("\n" + "="*70)
    print("SELECT EXAMPLE TO RUN:")
    print("="*70)
    print("\n1. Candidate Status Dropdown - Hidden Field Detection")
    print("   Real issue: Internal test statuses appearing in user dropdowns")
    print("   Demonstrates: Context-aware validation")
    
    print("\n2. Candidate Search Results - Logical Consistency")
    print("   Real issue: Active candidates > Total candidates (impossible!)")
    print("   Demonstrates: Mathematical relationship checking")
    
    print("\n3. Dashboard Statistics - API/UI Integration Gap")
    print("   Real issue: Postman tests pass but UI doesn't update")
    print("   Demonstrates: Integration requirement validation")
    
    print("\n4. User Authentication - Progressive Testing Layers")
    print("   Shows: Structure → Quality → Intelligence progression")
    print("   Demonstrates: How testing sophistication builds")
    
    print("\n5. Run ALL examples")
    print("6. Exit")
    print("\n" + "="*70)

def run_example(example_num):
    """Run specified example script"""
    example_files = {
        1: "example_1_candidate_status_hidden_fields.py",
        2: "example_2_search_results_logical_consistency.py",
        3: "example_3_dashboard_stats_integration_gap.py",
        4: "example_4_authentication_progressive_layers.py"
    }
    
    if example_num not in example_files:
        print("\nInvalid selection")
        return
    
    example_file = example_files[example_num]
    
    # Check if running from examples directory
    if os.path.exists(example_file):
        filepath = example_file
    elif os.path.exists(f"examples/{example_file}"):
        filepath = f"examples/{example_file}"
    else:
        print(f"\nError: Could not find {example_file}")
        print("Make sure you're running from the api_response_checker directory")
        return
    
    print(f"\nRunning: {example_file}\n")
    
    # Execute the example
    with open(filepath, 'r') as f:
        code = f.read()
        exec(code, {'__name__': '__main__', '__file__': filepath})
    
    print("\n" + "="*70)
    print(f"Example {example_num} completed")
    print("="*70)

def run_all_examples():
    """Run all examples in sequence"""
    for i in range(1, 5):
        run_example(i)
        if i < 4:
            input("\nPress Enter to continue to next example...")

def main():
    """Main demo loop"""
    print_banner()
    
    # Check if --quick flag was passed
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        print("Running quick demo (Example 1 only)...\n")
        run_example(1)
        return
    
    # Check if --all flag was passed
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        print("Running all examples...\n")
        run_all_examples()
        return
    
    # Interactive menu
    while True:
        print_menu()
        try:
            choice = input("\nEnter selection (1-6): ").strip()
            
            if choice == '6':
                print("\nThank you for using API Response Quality Checker!")
                print("="*70 + "\n")
                break
            elif choice == '5':
                run_all_examples()
            elif choice in ['1', '2', '3', '4']:
                run_example(int(choice))
                input("\nPress Enter to return to menu...")
            else:
                print("\nInvalid selection. Please enter 1-6.")
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"\nError: {e}")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
