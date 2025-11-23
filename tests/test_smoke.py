def test_imports():
    import pandas as pd
    import numpy as np
    assert pd.__version__ is not None
    assert np.__version__ is not None
