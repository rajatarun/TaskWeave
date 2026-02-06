from agents.agent_initializer import create_agent


if __name__ == "__main__":
    agent, memory = create_agent()

    user_question = "Compare sales between Q1 and Q2 from API data"
    result = agent.invoke({"input": user_question})

    print("\nFinal Result:\n", result)
    print("\nShared Memory:\n", memory)
