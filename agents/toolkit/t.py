from agents.toolkit.bag import BagOfTools

if __name__ == "__main__":
    bot = BagOfTools()
    tools = bot.get_tools()

    # Visualize file structure using the new tool
    file_structure_output = bot.visualize_file_structure('/home/gompert/workspace/llmas/')
    print(file_structure_output)
