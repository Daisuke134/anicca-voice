"""The submitted demo must select Twilio in both directions and cap the call."""
import json
import pathlib
import unittest


class DemoConfigTest(unittest.TestCase):
    def test_twilio_demo_contract(self):
        config = json.loads(pathlib.Path(__file__).with_name("agent.json").read_text())
        tasks = config["agent_config"]["tasks"]
        self.assertEqual(len(tasks), 1)
        task = tasks[0]
        for direction in ("input", "output"):
            self.assertEqual(task["tools_config"][direction]["provider"], "twilio")
        self.assertGreater(task["task_config"]["call_terminate"], 0)
        self.assertLessEqual(task["task_config"]["call_terminate"], 60)


if __name__ == "__main__":
    unittest.main()
