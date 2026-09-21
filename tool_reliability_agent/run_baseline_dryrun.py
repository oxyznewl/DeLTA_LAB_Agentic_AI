import csv
from models import TaskInput
from agent.agent_core import AgentCore
from tools.simulated_tools import SimulatedToolA, SimulatedToolB
from models import RoutingDecision
from config import NUM_TASKS, NUM_RUNS


class MockReliabilityManager:
    def get_all_scores(self):
        return {"tool_a": 0.5, "tool_b": 0.5}
    def update(self, result):
        pass


class MockBaselineRouter:
    def select_tool(self, task, candidate_tools, reliability_scores):
        import random
        selected = random.choice(candidate_tools)  # Baseline: 무작위/균등 선택
        return RoutingDecision(
            task_id=task.task_id,
            selected_tool=selected,
            reliability_scores=reliability_scores,
        )


all_logs = []
for run_id in range(1, NUM_RUNS + 1):
    tools = {"tool_a": SimulatedToolA(), "tool_b": SimulatedToolB()}
    agent = AgentCore(tools=tools, reliability_manager=MockReliabilityManager(), router=MockBaselineRouter())

    for task_id in range(1, NUM_TASKS + 1):
        task = TaskInput(task_id=task_id, query=f"topic_{task_id}")
        result = agent.run_task(task)
        all_logs.append({
            "run_id": run_id,
            "task_id": task_id,
            "selected_tool": result.tool_name,
            "tool_success": int(result.success),
            "latency_sec": result.latency_sec,
        })

with open("baseline_provisional_results.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=all_logs[0].keys())
    writer.writeheader()
    writer.writerows(all_logs)

print(f"{len(all_logs)}개 row 저장 완료")