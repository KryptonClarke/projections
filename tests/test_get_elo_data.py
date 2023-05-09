import pandera as pa
from pandera.typing import List


results_schema = pa.DataFrameSchema({
    "team": pa.Column(str),
    "results": pa.Column(List[int])
})