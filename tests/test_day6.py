import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.demo import BankDemo

demo = BankDemo()
demo.run()
print('Day 6 demo finished')
