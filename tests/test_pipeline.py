"""Offline smoke tests with synthetic TPM data; no scientific inference."""
import gzip
import tempfile
import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))
from build_tpm_matrix import build_matrix
from exploratory_deg import test_expression

class PipelineTests(unittest.TestCase):
    def test_build_and_welch(self):
        with tempfile.TemporaryDirectory() as root:
            src, out = Path(root) / "raw", Path(root) / "processed"
            src.mkdir()
            examples = [("Hs766T", 10), ("Pa02C", 12), ("HPAC", 2), ("PANC-1", 3)]
            for i, (line, val) in enumerate(examples):
                with gzip.open(src / f"GSMTEST{i}_{line}_Gene_TPM.txt.gz", "wt") as f:
                    f.write(f"Gene\tTPM\nLDHB\t{val}\nACTB\t5\n")
            mapping = Path(root) / "groups.csv"
            mapping.write_text("accession,group\nGSMTEST0,KRAS_Q61H\nGSMTEST1,KRAS_Q61H\nGSMTEST2,Non_Q61H\nGSMTEST3,Non_Q61H\n")
            report = build_matrix(src, out, mapping)
            self.assertEqual((report["samples"], report["shared_genes"]), (4, 2))
            stats = test_expression(out / "TPM_matrix.csv", out / "metadata.csv", out / "deg.csv")
            self.assertEqual(stats["genes_tested"], 2)
            self.assertEqual(stats["n_q61h"], 2)
            self.assertEqual(stats["n_comparison"], 2)

    def test_missing_groups_rejected(self):
        with tempfile.TemporaryDirectory() as root:
            src = Path(root) / "raw"
            src.mkdir()
            with gzip.open(src / "GSMTEST0_Hs766T_Gene_TPM.txt.gz", "wt") as f:
                f.write("Gene\tTPM\nLDHB\t10\n")
            mapping = Path(root) / "groups.csv"
            mapping.write_text("accession,group\nGSMTEST1,KRAS_Q61H\n")
            with self.assertRaises(ValueError):
                build_matrix(src, Path(root) / "out", mapping)

    def test_default_group_unverified(self):
        with tempfile.TemporaryDirectory() as root:
            src = Path(root) / "raw"
            src.mkdir()
            with gzip.open(src / "GSMTEST0_Hs766T_Gene_TPM.txt.gz", "wt") as f:
                f.write("Gene\tTPM\nLDHB\t10\n")
            build_matrix(src, Path(root) / "out")
            import pandas as pd
            meta = pd.read_csv(Path(root) / "out" / "metadata.csv")
            self.assertEqual(meta.loc[0, "group"], "UNVERIFIED")

if __name__ == "__main__":
    unittest.main()
