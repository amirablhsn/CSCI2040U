import csv
import os
import pytest
import tempfile
import edit_csv

@pytest.fixture
def sample_csv():
    """Create a temporary sample CSV file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['description', 'make', 'model', 'type', 'year', 'price', 
                       'engine', 'cylinders', 'fuel', 'transmission', 'trim', 
                       'body', 'doors', 'exterior_color', 'interior_color', 'drivetrain'])
        writer.writerow(['2022 Toyota Camry LE', 'toyota', 'camry', 'sedan', '2022', '25000.50', 
                        '2.5L', '4', 'gasoline', 'automatic', 'LE', 'sedan', '4', 'red', 'black', 'fwd'])
        writer.writerow(['2019 Ford F-150', 'ford', 'f-150', 'truck', '2019', '32,000', 
                        '5.0L', '8', 'gas', 'automatic', 'XLT', 'pickup', '4', 'blue', 'gray', '4wd'])
        writer.writerow(['2020 Tesla Model 3', '', 'model 3', 'sedan', '2020', '42999.99', 
                        '', '', 'electric', 'automatic', 'Standard', 'sedan', '', 'white', 'black', 'rwd'])
        writer.writerow(['Honda Civic', 'honda', 'civic', 'sedan', '2021', 'unknown', 
                        '1.5L', 'four', 'gasoline', 'cvt', 'EX', 'sedan', 'four', 'silver', 'black', 'fwd'])
    return f.name

@pytest.fixture
def setup_test_files(sample_csv):
    """Set up test files and restore original settings after test."""
    original_input = edit_csv.input_file
    original_output = edit_csv.output_file
    
    # Configure script to use our test files
    edit_csv.input_file = sample_csv
    output_file = f"{os.path.splitext(sample_csv)[0]}_edited.csv"
    edit_csv.output_file = output_file
    
    yield sample_csv, output_file
    
    # Clean up
    edit_csv.input_file = original_input
    edit_csv.output_file = original_output
    
    # Remove temporary files
    try:
        os.remove(sample_csv)
        os.remove(output_file)
    except OSError:
        pass

def test_edit_csv_runs_without_errors(setup_test_files):
    """Test that the script runs without throwing exceptions."""
    edit_csv.edit_csv()
    assert os.path.exists(setup_test_files[1])

def test_year_prefix_removed(setup_test_files):
    """Test that year prefixes are removed from description field."""
    edit_csv.edit_csv()
    
    with open(setup_test_files[1], 'r', newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
        assert rows[0]['description'] == 'Toyota Camry LE'
        assert rows[1]['description'] == 'Ford F-150'
        assert rows[2]['description'] == 'Tesla Model 3'
        # The last row didn't have a year prefix, should remain unchanged
        assert rows[3]['description'] == 'Honda Civic'

def test_make_model_uppercase(setup_test_files):
    """Test that make and model are converted to uppercase."""
    edit_csv.edit_csv()
    
    with open(setup_test_files[1], 'r', newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
        for row in rows:
            if row['make']:  # Skip empty make fields
                assert row['make'].isupper()
            if row['model']:  # Skip empty model fields
                assert row['model'].isupper()

def test_fuel_standardization(setup_test_files):
    """Test that fuel types are standardized."""
    edit_csv.edit_csv()
    
    with open(setup_test_files[1], 'r', newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
        assert rows[0]['fuel'] == 'Gasoline'
        assert rows[1]['fuel'] == 'Gasoline'  # 'gas' should become 'Gasoline'
        assert rows[2]['fuel'] == 'Electric'

def test_numeric_field_handling(setup_test_files):
    """Test that numeric fields are properly converted."""
    edit_csv.edit_csv()
    
    with open(setup_test_files[1], 'r', newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
        # Test cylinders
        assert rows[0]['cylinders'] == '4'
        assert rows[1]['cylinders'] == '8'
        assert rows[2]['cylinders'] == '4'  # Empty should become default 4
        assert rows[3]['cylinders'] == '4'  # 'four' should become 4
        
        # Test price
        assert float(rows[0]['price']) == 25000.50
        assert float(rows[1]['price']) == 32000.00  # Comma should be removed
        assert float(rows[2]['price']) == 42999.99
        assert float(rows[3]['price']) == 0.0  # 'unknown' should become 0.0
        
        # Test doors
        assert rows[0]['doors'] == '4'
        assert rows[1]['doors'] == '4'
        assert rows[2]['doors'] == '4'  # Empty should become default 4
        assert rows[3]['doors'] == '4'  # 'four' should become 4

def test_row_count_preserved(setup_test_files):
    """Test that the number of rows is the same in input and output."""
    edit_csv.edit_csv()
    
    with open(setup_test_files[0], 'r', newline='', encoding='utf-8-sig') as f_in:
        input_rows = list(csv.reader(f_in))
    
    with open(setup_test_files[1], 'r', newline='', encoding='utf-8-sig') as f_out:
        output_rows = list(csv.reader(f_out))
        
    assert len(input_rows) == len(output_rows)
    
def test_headers_preserved(setup_test_files):
    """Test that all headers are preserved in the output file."""
    edit_csv.edit_csv()
    
    with open(setup_test_files[0], 'r', newline='', encoding='utf-8-sig') as f_in:
        input_headers = next(csv.reader(f_in))
    
    with open(setup_test_files[1], 'r', newline='', encoding='utf-8-sig') as f_out:
        output_headers = next(csv.reader(f_out))
        
    assert input_headers == output_headers
