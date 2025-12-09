from iara.conversation.agent import Agent

def main():
    agent = Agent()
    
    print("Welcome to Iara! The COMPANYNAME's appointment booking assistant.")
    print("I can help you book an appointment. Let's get started!")

    response = agent.respond("")
    print("Iara:", response)

    while True:
        user_input = input("> ")

        if user_input.lower() in ["exit", "quit"]:
            print("Thank you for using Iara. Goodbye!")
            break

        response = agent.respond(user_input)
        print("Iara:", response)


if __name__ == "__main__":
    main()
