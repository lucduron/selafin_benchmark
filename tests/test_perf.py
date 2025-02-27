import time
from selafin_benchmark.selafin import Selafin
from selafin_benchmark.telemac_file import TelemacFile
from selafin_benchmark.selafin_io_pp import ppSELAFIN
from selafin_benchmark import Serafin
import pytest


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Time taken by {func.__name__}: {end - start} seconds")
        return result
    return wrapper

PERF = pytest.mark.parametrize(
    "f",
    [
        pytest.param("tests/data/r3d_tidal_flats.slf", id="3D"),
        pytest.param("tests/data/r2d_tidal_flats.slf", id="2D"),
    ],
)

# selafin
@PERF 
@timer
def selafin(f):
    slf = Selafin(f)
    slf.get_series([10])

# telemacFile
@timer
@PERF 
def telemac(f):
    tel = TelemacFile(f)
    tel.get_data_value(tel.varnames[0], 10)

# ppUtils
@timer
@PERF 
def ppUtils(f):
    ppslf = ppSELAFIN(f)
    ppslf.readHeader()
    ppslf.readVariables(10)

# PyTelTools
@timer
@PERF
def pyTelTools(f):
    with Serafin.Read(f, 'en') as resin:
        resin.read_header()  # fills resin.header (read mesh)
        resin.get_time()
        resin.read_var_in_frame(10,resin.header.var_IDs[0])
