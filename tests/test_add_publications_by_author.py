import os
import json
import unittest
import shutil
from textwrap import dedent

import src.python.add_publications_by_author as mod


class TestAddPublicationsByAuthor(unittest.TestCase):
    @classmethod
    def tearDown(self) -> None:
        out_dir = "tests/scratch/_posts/papers"
        if os.path.exists(out_dir):
            shutil.rmtree(out_dir)

    def add_publication_and_verify_all(self, author):
        with open(f"tests/data/add_publications_by_author/{author}/in.md") as f:
            issue_body = f.read()

        out = mod.main(issue_body, save_dir="tests/scratch/_posts/papers")
        papers = out["cleaned"]
        file2paper = {x["filename"]: x for x in papers}

        out_dir = f"tests/data/add_publications_by_author/{author}/out"

        for file in os.listdir(out_dir):
            with open(os.path.join(out_dir, file)) as f:
                expected_paper = f.read()
            error_msg = f"We did not find this paper in the list of all papers by {author}: {file}\nList of all papers: {file2paper.keys()}"
            self.assertIn(file, file2paper, msg=error_msg)
            self.assertEqual(file2paper[file]["content"], expected_paper)

        with open("ignored/semantic_scholar_paper_ids.json") as f:
            ignored = set(json.load(f))

        # test if the paper was added to the list of ignored papers in semantic scholar IDs file
        for paper_id in out["ignored"]:
            self.assertIn(paper_id, ignored)

    def test_main_siva(self):
        self.add_publication_and_verify_all("siva")

    def test_main_timothy(self):
        self.add_publication_and_verify_all("timothy")


if __name__ == "__main__":
    unittest.main()
