import pandas as pd
import numpy as np
# We need to import the function we want to test from our etl script
from etl import transform_data

def test_transform_data_calculates_moving_average():
    """
    Tests that the transform_data function correctly calculates the 50-day moving average.
    """
    # 1. Arrange: Create a sample DataFrame that includes the 'ticker' column.
    data = {
        'Close': np.arange(100.0, 151.0), # Prices from 100 to 150
        'ticker': 'TEST' # Add the missing ticker column
    }
    input_df = pd.DataFrame(data)

    # 2. Act: Run the function that we are testing.
    result_df = transform_data(input_df)

    # 3. Assert: Check if the result is what we expect.

    # The first valid moving average will be for the 50th data point (index 49).
    # The values are 100, 101, ..., 149. The average of these is 124.5.
    expected_moving_average = 124.5

    # The function drops rows with NaN, so the first row in the result should be index 49.
    calculated_moving_average = result_df.iloc[0]['moving_average_50']

    # Check that the new column exists
    assert 'moving_average_50' in result_df.columns
    # Check that the calculation is correct (allowing for small floating point differences)
    assert np.isclose(calculated_moving_average, expected_moving_average)
    # Check that the 'price' column was correctly renamed from 'Close'
    assert 'price' in result_df.columns