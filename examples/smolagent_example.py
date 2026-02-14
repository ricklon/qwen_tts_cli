"""Example of using Qwen-TTS CLI as a smolagents tool.

This example demonstrates how to use the Qwen-TTS tool with smolagents
to create an AI agent that can generate speech from text.
"""

from smolagents import CodeAgent, HfApiModel
from qwen_tts_cli.smolagent_tool import QwenTTSTool, create_qwen_tts_tool


def example_with_tool_class():
    """Example using the full Tool class."""
    print("=== Example 1: Using QwenTTSTool class ===\n")

    # Initialize the tool
    tts_tool = QwenTTSTool()

    # Create an agent with the tool
    # Note: You'll need to set up your HF token and model
    model = HfApiModel(model_id="Qwen/Qwen2.5-Coder-32B-Instruct")
    agent = CodeAgent(
        tools=[tts_tool],
        model=model,
        add_base_tools=True
    )

    # Use the agent to generate speech
    result = agent.run(
        "Generate an Italian greeting in a friendly teacher's voice, "
        "saying 'Welcome to today's lesson!' and save it as welcome.wav"
    )

    print(f"Agent result: {result}\n")


def example_with_decorator():
    """Example using the @tool decorator version."""
    print("=== Example 2: Using decorator-based tool ===\n")

    # Create the tool using the decorator
    tts_tool = create_qwen_tts_tool()

    # Create an agent with the tool
    model = HfApiModel(model_id="Qwen/Qwen2.5-Coder-32B-Instruct")
    agent = CodeAgent(
        tools=[tts_tool],
        model=model,
        add_base_tools=True
    )

    # Use the agent
    result = agent.run(
        "Create a Spanish audio file with the text 'Hola, buenos días' "
        "in a news anchor style voice"
    )

    print(f"Agent result: {result}\n")


def example_direct_tool_usage():
    """Example of calling the tool directly without an agent."""
    print("=== Example 3: Direct tool usage ===\n")

    # Initialize the tool
    tts_tool = QwenTTSTool()

    # Call it directly
    result = tts_tool(
        text="Bonjour! Comment allez-vous?",
        language="French",
        instruct="Friendly conversational tone",
        output_filename="french_greeting.wav",
        device="cpu"
    )

    print(f"Direct tool result: {result}\n")


def example_language_learning_assistant():
    """Example: Language learning assistant that generates pronunciation exercises."""
    print("=== Example 4: Language Learning Assistant ===\n")

    tts_tool = QwenTTSTool()
    model = HfApiModel(model_id="Qwen/Qwen2.5-Coder-32B-Instruct")

    agent = CodeAgent(
        tools=[tts_tool],
        model=model,
        add_base_tools=True
    )

    # Ask the agent to create a series of language exercises
    result = agent.run(
        "Create three Italian pronunciation exercises: "
        "1. Airport vocabulary (save as airport_vocab.wav) "
        "2. Restaurant phrases (save as restaurant.wav) "
        "3. Greetings (save as greetings.wav). "
        "Use a slow, clear teacher voice for all three."
    )

    print(f"Language learning assistant result: {result}\n")


if __name__ == "__main__":
    print("Qwen-TTS Smolagents Examples")
    print("=" * 50 + "\n")

    # Choose which example to run
    print("Choose an example to run:")
    print("1. Tool class example")
    print("2. Decorator-based tool example")
    print("3. Direct tool usage (no agent)")
    print("4. Language learning assistant")
    print()

    choice = input("Enter choice (1-4, or 'all' to run all): ").strip()

    if choice == "1":
        example_with_tool_class()
    elif choice == "2":
        example_with_decorator()
    elif choice == "3":
        example_direct_tool_usage()
    elif choice == "4":
        example_language_learning_assistant()
    elif choice.lower() == "all":
        example_direct_tool_usage()  # This one doesn't need API access
        # example_with_tool_class()
        # example_with_decorator()
        # example_language_learning_assistant()
        print("\nNote: Examples 1, 2, and 4 require HuggingFace API access.")
        print("Set your HF_TOKEN environment variable to run them.")
    else:
        print("Invalid choice. Running direct tool usage example...")
        example_direct_tool_usage()
