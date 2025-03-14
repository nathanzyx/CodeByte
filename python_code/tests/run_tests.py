import pytest
import webbrowser
from pathlib import Path
import time

def main():
    try:
        # Get the directory containing this script
        current_dir = Path(__file__).parent
        
        # Run tests and generate report
        report_path = current_dir / "report.html"
        
        # Run pytest with HTML report generation
        result = pytest.main(["-v", f"--html={str(report_path)}"])
        
        # Give pytest time to finish writing the report
        time.sleep(1)
        
        # Check if report was generated
        if report_path.exists():
            # Convert to absolute path and format as URI
            abs_path = report_path.resolve()
            url = abs_path.as_uri()
            
            # Open in browser with new=2 to force a new tab
            webbrowser.open(url, new=2)
            
            # Keep script running for a moment
            time.sleep(2)
        else:
            print(f"Error: Report file not found at {report_path}")
            
    except Exception as e:
        print(f"Error running tests: {e}")

if __name__ == "__main__":
    main()